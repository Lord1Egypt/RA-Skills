# SAC-LTC Architecture: Complete Technical Disclosure

This document fully discloses every component of the SAC-LTC (Soft Actor-Critic with Liquid Time-Constant) architecture used in UHCI Net-Intel. Nothing is hidden.

## Table of Contents

1. [Overview](#overview)
2. [Liquid Time-Constant (LTC) Cell](#liquid-time-constant-ltc-cell)
3. [Kolmogorov-Arnold Network (KAN) Actor](#kolmogorov-arnold-network-kan-actor)
4. [Twin Critics](#twin-critics)
5. [SAC Algorithm](#sac-algorithm)
6. [Feature Normalization](#feature-normalization)
7. [Scoring Heuristic](#scoring-heuristic)
8. [Presence Sensing](#presence-sensing)
9. [Explainability Mechanism](#explainability-mechanism)
10. [Parameter Count Breakdown](#parameter-count-breakdown)
11. [Weight Initialization](#weight-initialization)

---

## Overview

The system has three modes of operation:

1. **Inference only** (deployed on laptop): LTC Cell + KAN Actor. No critics needed. ~5K parameters.
2. **Training** (one-time): Full SAC with LTC Cell + KAN Actor + Twin Critics + Target Networks + Entropy Tuning. ~17K parameters.
3. **Heuristic fallback** (no PyTorch): Rule-based scoring with same feature normalization. 0 parameters.

```
Architecture Diagram:

INPUT: 8 normalized features per network observation
  [rssi, snr, latency, throughput, packet_loss, congestion, is_5ghz, is_hotspot]
  All values in [0, 1]

TEMPORAL ENCODING:
  Sliding window of last 8 observations → (1, 8, 8) tensor
  Each timestep fed sequentially through LTC Cell
  Hidden state carries temporal memory forward

LTC CELL (input_dim=8, hidden_dim=32):
  For each timestep t:
    f(x,h) = tanh(W_x * x_t + W_h * h_{t-1} + b)
    tau(x) = tau_base + softplus(W_tau * x_t + b_tau)
    h_t = h_{t-1} + (dt / tau(x)) * (-h_{t-1} + f(x,h))
  Output: h_final (32-dim hidden state)

KAN ACTOR (for inference):
  h_final (32) → KANLinear(32, 16) → LayerNorm(16) → KANLinear(16, N_actions) → Softmax
  Output: probability distribution over N available networks

TWIN CRITICS (for training only):
  Q1: h_final (32) → Linear(32, 64) → LayerNorm → SiLU → Linear(64, N_actions)
  Q2: h_final (32) → Linear(32, 64) → LayerNorm → SiLU → Linear(64, N_actions)
  Output: Q-value per action (how good is each network choice)
```

---

## Liquid Time-Constant (LTC) Cell

### What It Is

A neural ODE cell where the time constant (how fast the cell reacts) depends on the input. This is fundamentally different from LSTM/GRU where time dynamics are fixed.

### The Differential Equation

```
Continuous form:
  tau(x) * dh/dt = -h + f(x, h)

Where:
  h          = hidden state vector (32 dimensions)
  x          = input features (8 dimensions)
  f(x, h)    = tanh(W_x * x + W_h * h + b)    [nonlinear activation]
  tau(x)     = tau_base + softplus(W_tau * x + b_tau)  [input-dependent time constant]
  softplus(z) = log(1 + exp(z))                 [ensures tau > 0 always]
  tau_base   = learnable parameter, initialized to 1.0  [minimum time constant]
```

### Euler Discretization

Since we sample at discrete intervals, we discretize the ODE:

```
h_new = h_old + (dt / tau(x)) * (-h_old + f(x, h_old))

Where dt = 1.0 (one timestep)
```

This means:
- Large tau(x) → small update → cell changes slowly → remembers long-term trends
- Small tau(x) → large update → cell reacts quickly → tracks fast changes

### Weight Matrices

| Weight | Shape | Purpose |
|--------|-------|---------|
| `W_x` | (8, 32) | Maps input features to hidden state activation |
| `W_h` | (32, 32) | Maps previous hidden state to current activation |
| `b` | (32,) | Bias for activation function |
| `W_tau` | (8, 32) | Maps input features to time constant modulation |
| `b_tau` | (32,) | Bias for time constant |
| `tau_base` | (32,) | Learnable base time constant (initialized to 1.0) |

**Total LTC parameters: 8*32 + 32*32 + 32 + 8*32 + 32 + 32 = 1,632**

### Why LTC and Not LSTM

| Property | LSTM | LTC |
|----------|------|-----|
| Time dynamics | Fixed gates | Input-dependent tau |
| Irregular sampling | Requires special handling | Natural via dt parameter |
| Interpretability | Black-box gates | tau values show what cell is tracking |
| Continuous time | Discrete only | Native ODE formulation |
| Hysteresis | Must be engineered | Emerges naturally from large tau |

### Code Reference

**PyTorch** (`train_sac_ltc.py`, class `TorchLTCCell`):
```python
def forward(self, x, h):
    f = torch.tanh(self.W_x(x) + self.W_h(h))
    tau = self.tau_base + F.softplus(self.W_tau(x))
    h_new = h + (self.dt / tau) * (-h + f)
    return h_new, tau
```

**Pure Python** (`sac_ltc_agent.py`, class `NumpyLTCCell`):
```python
def forward(self, x, h):
    f = [tanh(sum(W_x[i][j]*x[i]) + sum(W_h[i][j]*h[i]) + b[j]) for j in range(hidden_dim)]
    tau = [tau_base[j] + softplus(sum(W_tau[i][j]*x[i]) + b_tau[j]) for j in range(hidden_dim)]
    h_new = [h[j] + (dt/tau[j]) * (-h[j] + f[j]) for j in range(hidden_dim)]
    return h_new, tau
```

---

## Kolmogorov-Arnold Network (KAN) Actor

### What It Is

KAN layers replace traditional Linear+ReLU layers with learnable activation functions. Each connection has its own learned curve shape using B-spline basis functions.

### Structure

Each KAN layer computes:

```
output = base_function(x) + spline_function(x)

base_function:
  base_out[j] = sum_i(base_weight[i][j] * SiLU(x[i]))
  SiLU(x) = x * sigmoid(x)   [also called Swish]

spline_function:
  For each input dimension i, evaluate RBF basis at grid points:
    basis[k] = exp(-0.5 * ((x[i] - grid[k]) / 0.3)^2)
  spline_out[j] = sum_i sum_k (spline_weight[i][k][j] * basis[k])

Grid: 8 evenly spaced points from -1 to +1 (grid_size=5, spline_order=3, n_basis=8)
```

### Actor Pipeline

```
Input: LTC hidden state h (32 dimensions)
  |
  v
KANLinear Layer 1:
  input_dim=32, output_dim=16
  base_weight: (32, 16) = 512 parameters
  spline_weight: (32, 8, 16) = 4,096 parameters
  Total: 4,608 parameters
  |
  v
LayerNorm(16):
  gamma: (16,), beta: (16,) = 32 parameters
  |
  v
KANLinear Layer 2:
  input_dim=16, output_dim=N_actions (default 5)
  base_weight: (16, 5) = 80 parameters
  spline_weight: (16, 8, 5) = 640 parameters
  Total: 720 parameters
  |
  v
Softmax:
  probs[i] = exp(logit[i]) / sum(exp(logit[j]))
  Output: probability distribution over N actions
```

### Why KAN and Not MLP

KAN's spline activations are **interpretable**: we can examine the learned curves to see how each input feature maps to the output. This is how the `explain()` method works — it perturbs each input feature and measures how the output changes through the spline functions.

### Code Reference

**PyTorch** (`train_sac_ltc.py`, class `TorchKANLinear`):
```python
def forward(self, x):
    base = self.base_weight(F.silu(x))
    x_expand = x.unsqueeze(-1)
    basis = torch.exp(-0.5 * ((x_expand - self.grid) / 0.3) ** 2)
    spline = torch.einsum("bin,ino->bo", basis, self.spline_weight)
    return base + spline
```

---

## Twin Critics

Used during training only. Not deployed on the laptop.

### Architecture

```
Q1 Network:
  Linear(32 → 64) → LayerNorm(64) → SiLU → Linear(64 → N_actions)

Q2 Network (identical architecture, different weights):
  Linear(32 → 64) → LayerNorm(64) → SiLU → Linear(64 → N_actions)

Each outputs one Q-value per possible action.
The minimum of Q1 and Q2 is used (double-Q trick to prevent overestimation).
```

### Target Networks

Separate copies of Q1 and Q2 that update slowly:

```
Every training step:
  theta_target = (1 - tau_polyak) * theta_target + tau_polyak * theta
  tau_polyak = 0.005 (very slow blending)
```

This stabilizes training by preventing the target from changing too fast.

### Parameter Count

```
Q1: 32*64 + 64 + 64 + 64*5 + 5 = 2,048 + 64 + 64 + 320 + 5 = 2,501
Q2: same = 2,501
Q1_target: same (copies of Q1) = 2,501
Q2_target: same (copies of Q2) = 2,501
Total critics: 10,004 parameters (training only)
```

---

## SAC Algorithm

### Core Idea

Soft Actor-Critic maximizes **reward + entropy**. The entropy bonus encourages exploration and prevents the policy from becoming too deterministic too early.

### Objective Functions

**Critic Loss (TD Learning):**
```
For each (state, action, reward, next_state, done) in batch:
  # What the next state is worth
  next_probs = actor(next_state)
  next_q_min = min(Q1_target(next_state), Q2_target(next_state))
  V_next = sum(next_probs * (next_q_min - alpha * log(next_probs)))

  # TD target
  target = reward + gamma * (1 - done) * V_next

  # Loss
  critic_loss = MSE(Q1(state, action), target) + MSE(Q2(state, action), target)
```

**Actor Loss (Policy Gradient with Entropy):**
```
probs = actor(state)
q_min = min(Q1(state), Q2(state))
log_probs = log(probs)
actor_loss = mean(sum(probs * (alpha * log_probs - q_min)))
```

**Entropy Temperature (alpha) Loss:**
```
entropy = -sum(probs * log(probs))
target_entropy = -0.98 * log(1 / N_actions)
alpha_loss = log(alpha) * (entropy - target_entropy)
```

### Hyperparameters (All Disclosed)

| Parameter | Value | Purpose |
|-----------|-------|---------|
| `gamma` | 0.99 | Discount factor — how much future rewards matter |
| `tau_polyak` | 0.005 | Target network soft update rate |
| `lr_actor` | 3e-4 | Actor learning rate (Adam optimizer) |
| `lr_critic` | 3e-4 | Critic learning rate |
| `lr_alpha` | 3e-4 | Entropy temperature learning rate |
| `batch_size` | 128 | Samples per training step |
| `replay_buffer_size` | 50,000 | Maximum stored transitions |
| `gradient_clip` | 1.0 | Max gradient norm (prevents explosion) |
| `target_entropy_ratio` | 0.98 | How much exploration to maintain |
| `switch_penalty` | 0.3 | Reward penalty for changing networks |
| `episodes` | 1,000 | Training episodes |
| `steps_per_episode` | 100 | Environment steps per episode |
| `sequence_length` | 8 | LTC input window |

### Training Loop (Step by Step)

```
For each episode (1 to 1000):
  1. Create new RFEnvironment with random seed = episode number
  2. Initialize LTC hidden state to zeros
  3. Warm up: run 8 environment steps to fill the observation window

  For each step (1 to 100):
    4. Get current observation window (8 x 8 features)
    5. Forward pass through LTC → KAN → get action probabilities
    6. Sample action from probability distribution
    7. Execute action in environment, get reward
    8. Store (state, action, reward, next_state, done) in replay buffer

    If replay buffer has enough samples (>128):
      9. Sample random batch of 128 transitions
      10. Compute critic loss and update Q1, Q2
      11. Compute actor loss and update LTC + KAN
      12. Compute alpha loss and update entropy temperature
      13. Soft-update target networks (Q1_target, Q2_target)

  14. Log episode reward
  15. Every 100 episodes, print progress
```

---

## Feature Normalization

Raw sensor readings are normalized to [0, 1] before feeding to the model.

### Normalization Functions

| Feature | Raw Range | Formula | Normalized Range |
|---------|-----------|---------|-----------------|
| `rssi` | -100 to -20 dBm | `(rssi + 100) / 60` | 0 (unusable) to 1 (excellent) |
| `snr` | 0 to 60 dB | `(rssi - noise) / 60` | 0 (no signal) to 1 (pristine) |
| `latency` | 0 to 200+ ms | `1 - (latency / 200)` | 0 (very slow) to 1 (instant) |
| `throughput` | 0 to 100+ Mbps | `throughput / 100` | 0 (no data) to 1 (fast) |
| `packet_loss` | 0 to 10+% | `1 - (loss / 10)` | 0 (heavy loss) to 1 (perfect) |
| `congestion` | 0 to 10 networks | `1 - (count / 10)` | 0 (very crowded) to 1 (empty) |
| `is_5ghz` | boolean | `1.0 if 5GHz else 0.0` | Binary |
| `is_hotspot` | boolean | `1.0 if hotspot else 0.0` | Binary |

All values are clamped to [0, 1] after computation.

---

## Scoring Heuristic

Used for the 0-100 score displayed to the user. Independent of the SAC-LTC model.

```
Score = Signal + SNR + Latency + Throughput + Stability

Signal (30 points):
  > -50 dBm:       30 (excellent)
  -50 to -60 dBm:  22 (good)
  -60 to -70 dBm:  15 (fair)
  < -70 dBm:        7 (poor)

SNR (15 points):
  > 40 dB:          15 (excellent)
  25 to 40 dB:      11 (good)
  15 to 25 dB:       7 (fair)
  < 15 dB:           3 (poor)

Latency (25 points):
  < 20 ms:          25 (excellent)
  20 to 50 ms:      19 (good)
  50 to 100 ms:     12 (fair)
  > 100 ms:          5 (poor)

Throughput (20 points):
  > 50 Mbps:        20 (excellent)
  10 to 50 Mbps:    15 (good)
  1 to 10 Mbps:     10 (fair)
  < 1 Mbps:          3 (poor)

Stability (10 points):
  0% packet loss:   10 (excellent)
  < 1% loss:         7 (good)
  1-5% loss:         4 (fair)
  > 5% loss:         0 (poor)
```

---

## Presence Sensing

### How It Works

Wi-Fi signals travel between APs and your laptop. When a person moves through this signal path, their body (60% water) absorbs and reflects the radio waves, causing measurable RSSI fluctuations.

### Detection Algorithm

```
Input: list of RSSI readings sampled at ~1/second for 10-60 seconds

For each AP:
  1. Compute mean RSSI
  2. Compute variance of RSSI
  3. Compute peak-to-peak range (max - min)
  4. Compute autocorrelation at lag 1 (detects periodicity)
  5. Compute variance_ratio = variance / baseline_variance

Classification:
  variance_ratio > 5:    "active_movement"   (confidence 0.7-0.95)
  variance_ratio > 3:    "likely"             (confidence 0.5-0.85)
  variance_ratio > 1.5:  "possible"           (confidence 0.3-0.6)
  variance_ratio <= 1.5: "none"               (confidence 0.5-0.95)

Pattern detection:
  |autocorrelation| > 0.5: "periodic" → likely appliance (microwave), not human
  peak_to_peak > 6 dBm:   "walking" → active human movement
  peak_to_peak > 3 dBm:   "subtle_movement" → slow movement or nearby
  else:                    "stationary" → no movement
```

### Directional Sensing (with calibration)

After spatial calibration (mapping each AP to a direction relative to the user), presence detection becomes directional:

```
For each direction (front, back, left, right):
  - Get APs calibrated to that direction
  - Run RSSI variance analysis on those APs only
  - Report presence per direction
```

### Limitations (Disclosed)

- RSSI only (no Channel State Information on consumer hardware)
- Cannot detect stationary people (only movement causes RSSI changes)
- 2.4 GHz works better through walls than 5 GHz
- 30-60 seconds of sampling needed for reliable detection
- Pets, fans, and moving objects can cause false positives
- Accuracy is quadrant-level (front/back/left/right), not degree-level
- Minimum 3 APs in different directions needed for spatial sensing

---

## Explainability Mechanism

### How explain() Works

The system generates human-readable explanations for every decision using **finite-difference feature attribution**:

```
1. Run forward pass to get base logits for chosen action
2. For each of the 8 input features:
   a. Create perturbed copy: feature[i] += 0.1
   b. Re-run LTC + KAN with perturbed input
   c. Measure change in chosen action's logit
   d. attribution[i] = perturbed_logit - base_logit
3. Normalize: divide all attributions by max |attribution|
4. Sort by |attribution| descending
5. Map to plain English: top 2-3 factors become the "reason"
```

### Temporal Trend Detection

```
From LTC time constants tau(x):
  avg_tau_now vs avg_tau_3_steps_ago:
    tau increasing → "stabilizing" (cell is integrating over longer periods)
    tau decreasing → "reacting to change" (cell is tracking fast changes)
    tau unchanged  → "stable" (environment is steady)
```

### Layman Summary Generation

```
Read current normalized features:
  rssi < 0.4       → "signal is weak"
  latency < 0.3    → "response time is slow"
  packet_loss < 0.8 → "some data is getting lost"
  congestion < 0.4  → "your channel is crowded"

If no issues: "Your connection looks good. No action needed."
Else: "Issues: " + join(issues)
```

---

## Parameter Count Breakdown

### Inference Model (deployed on laptop)

| Component | Parameters | Calculation |
|-----------|-----------|-------------|
| LTC W_x | 256 | 8 * 32 |
| LTC W_h | 1,024 | 32 * 32 |
| LTC b | 32 | 32 |
| LTC W_tau | 256 | 8 * 32 |
| LTC b_tau | 32 | 32 |
| LTC tau_base | 32 | 32 |
| **LTC Total** | **1,632** | |
| KAN1 base_weight | 512 | 32 * 16 |
| KAN1 spline_weight | 4,096 | 32 * 8 * 16 |
| KAN1 grid (buffer) | 8 | 8 (not trained) |
| **KAN1 Total** | **4,608** | |
| LayerNorm gamma + beta | 32 | 16 + 16 |
| KAN2 base_weight | 80 | 16 * 5 |
| KAN2 spline_weight | 640 | 16 * 8 * 5 |
| **KAN2 Total** | **720** | |
| **Inference Total** | **6,992** | |

### Training Model (includes critics)

| Component | Parameters |
|-----------|-----------|
| Inference model | 6,992 |
| Q1 network | 2,501 |
| Q2 network | 2,501 |
| Q1 target | 2,501 |
| Q2 target | 2,501 |
| log_alpha | 1 |
| **Training Total** | **16,997** |

Note: PyTorch reports 17,274 due to additional bias terms in Linear layers.

---

## Weight Initialization

### Heuristic Pre-training (init_heuristic_weights)

When no trained model is available, we initialize weights with domain knowledge:

```python
# Feature importance encoding (higher = more influence on hidden state)
importance = [1.0,   # rssi — most important
              0.7,   # snr
              0.9,   # latency — critical for QoS
              0.8,   # throughput
              0.6,   # packet_loss
              0.5,   # congestion
              0.3,   # is_5ghz — slight preference
              -0.2]  # is_hotspot — slight penalty

# Time constant sensitivity (higher = tau responds more to this feature)
tau_sensitivity = [0.3,   # rssi — moderate
                   0.3,   # snr
                   0.5,   # latency — react to latency changes
                   0.5,   # throughput
                   0.8,   # packet_loss — react quickly to loss
                   0.4,   # congestion
                   0.1,   # is_5ghz — slow
                   0.1]   # is_hotspot — slow

# Base time constant: 2.0 (high = resist oscillation)
tau_base = 2.0 ± 0.1 (per hidden unit)
```

### Xavier Initialization (for full training)

All weight matrices use Xavier uniform initialization:
```
W ~ Uniform(-sqrt(6/(fan_in + fan_out)), +sqrt(6/(fan_in + fan_out)))
```

Biases initialized to zero. tau_base initialized to 1.0.
