# Training Pipeline: Complete Disclosure

Every aspect of how the SAC-LTC model is trained — the data sources, physics models, reward function, and results.

## Data Source: Physics-Grounded RF Environment Generation

We do NOT use a pre-packaged static dataset. Instead, each training episode generates a **physically realistic wireless environment** using real propagation models from ITU-R and 3GPP standards.

This is more rigorous than a static dataset because:
1. Every episode is unique (different network layouts, distances, channels)
2. The physics are real (ITU-R path loss, Shannon capacity, thermal noise)
3. Temporal dynamics are realistic (congestion patterns, movement events, interference)
4. The agent must generalize across environments, not memorize one

### Why Not a Real-World Dataset?

Real-world Wi-Fi datasets (e.g., from wardriving) only capture snapshots of signal levels. They do NOT capture:
- The reward from switching networks (you'd need to actually switch and measure)
- Temporal dynamics over minutes/hours at a single location
- The effect of human movement on signals
- Controlled interference events

Our physics-based environment provides all of this with controllable parameters.

---

## Physics Models Used (All from Published Standards)

### 1. ITU-R P.1238: Indoor Propagation

**Source:** International Telecommunication Union, Recommendation P.1238-10

```
Path Loss (dB) = FSPL + excess_loss + wall_penetration

FSPL = 20*log10(distance_m) + 20*log10(frequency_MHz) + 32.44

Excess loss (distance-dependent, indoor):
  excess = 10 * (N/20 - 1) * log10(distance_m)
  N = 28 for 2.4 GHz residential
  N = 30 for 5 GHz residential

Wall penetration:
  Each wall adds 5.0 dB loss (configurable)
  Range: 0-3 walls per path
```

**Implementation:** `train_sac_ltc.py`, class `RFPhysics`, method `indoor_path_loss_itu()`

### 2. ITU-R P.838-3: Rain Attenuation

**Source:** ITU-R Recommendation P.838-3

```
Specific attenuation: gamma_R = k * R^alpha (dB/km)

Coefficients (horizontal polarization):
  < 5 GHz:   k = 0.000387, alpha = 0.912
  5-10 GHz:  k = 0.00887,  alpha = 1.264
  10-30 GHz: k = 0.167,    alpha = 1.032
  > 30 GHz:  k = 0.751,    alpha = 0.843

Total attenuation = gamma_R * path_length_km
```

**Implementation:** `train_sac_ltc.py`, class `RFPhysics`, method `rain_attenuation_itu()`

### 3. 3GPP TR 38.901: Urban Macro NLOS Path Loss

**Source:** 3GPP Technical Report 38.901, Table 7.4.1-1

```
Path Loss (UMa NLOS):
  PL = 13.54 + 39.08 * log10(d_3D) + 20 * log10(fc_GHz)

  Valid for: 7-24 GHz (FR3 range)
  d_3D: 3D distance in meters (minimum 10m)
  fc_GHz: carrier frequency in GHz
```

**Implementation:** `train_sac_ltc.py`, class `RFPhysics`, method `uma_nlos_3gpp()`

### 4. Shannon-Hartley Theorem: Channel Capacity

**Source:** Claude Shannon, 1948. Universal information theory.

```
Capacity (Mbps) = Bandwidth_MHz * log2(1 + SNR_linear)

SNR_linear = 10^(SNR_dB / 10)
```

This gives the theoretical maximum throughput for a given bandwidth and signal-to-noise ratio. Actual throughput is lower due to overhead, congestion, and backhaul limits.

**Implementation:** `train_sac_ltc.py`, class `RFPhysics`, method `shannon_capacity_mbps()`

### 5. Thermal Noise Model

**Source:** Fundamental physics (Johnson-Nyquist noise)

```
Noise power (dBm) = 10 * log10(k * T * BW * 1000)

k = 1.38e-23 J/K (Boltzmann constant)
T = 290 K (standard temperature, ~17°C)
BW = bandwidth in Hz
```

For typical bandwidths:
- 20 MHz: -101 dBm
- 40 MHz: -98 dBm
- 80 MHz: -95 dBm
- 160 MHz: -92 dBm

**Implementation:** `train_sac_ltc.py`, class `RFPhysics`, method `thermal_noise_dbm()`

---

## Environment Generation (Per Episode)

Each training episode creates a new random environment:

### Network Generation

```
For each of 5 networks:
  Type: 70% infrastructure AP, 30% mobile hotspot

  Infrastructure AP:
    Distance: 3-30 meters (uniform random)
    Frequency: 33% 2.4GHz, 67% 5GHz
    Bandwidth: random choice from [20, 40, 80, 160] MHz
    Tx power: 15-23 dBm (uniform)
    Walls: 0-3 (based on distance)
    Backhaul: 100-1000 Mbps (wired)
    Backhaul latency: 2-10 ms
    Channel: weighted random from popular channels
      2.4 GHz: [1, 1, 6, 6, 11, 11, 1, 6, 3, 9]
      5 GHz: [36, 44, 149, 149, 149, 153, 157, 161]

  Mobile Hotspot:
    Distance: 1-8 meters
    Frequency: 30% 2.4GHz, 70% 5GHz
    Bandwidth: random choice from [20, 40, 80] MHz
    Tx power: 10-18 dBm (phones transmit lower)
    Walls: 0
    Cellular generation: random from [3G, 4G, 4G, 5G, 5G]
      3G backhaul: 1-5 Mbps, 80-200 ms latency
      4G backhaul: 10-50 Mbps, 20-60 ms latency
      5G backhaul: 50-300 Mbps, 8-25 ms latency
    Movement speed: 0.5-2.0 m/step (phones drift)
```

### Per-Step Dynamics

Each of the 100 steps per episode (simulating ~30 seconds each):

```
1. Time of day advances 30 seconds
   Congestion multiplier = 1.0 + 0.5 * exp(-((hour - 20)^2) / 8)
   Peak at 8pm (20:00), natural residential pattern

2. Random events:
   15% chance: human movement event
     Body absorption: 3-12 dB loss (exponential decay with distance)
   5% chance: interference event
     Noise increase: 5-15 dB on affected band (70% chance 2.4GHz)

3. Hotspot drift:
   Distance += gaussian(0, 0.3) meters
   Clamped to [1, 15] meters

4. RSSI computation:
   rssi = tx_power - indoor_path_loss(freq, distance, walls) - body_loss
   Clamped to [-100, -20] dBm

5. Noise computation:
   noise = thermal_noise(bandwidth) + noise_figure + co_channel_interference
   Co-channel: +3 dB per network on same channel

6. Throughput:
   capacity = shannon_capacity(bandwidth, snr)
   effective = capacity / (1 + congestion * 0.3)
   throughput = min(effective, backhaul_mbps) + gaussian(0, 5%)

7. Latency:
   latency = 2ms + distance*0.01 + congestion*random(2,8) + backhaul_latency
   + gaussian(0, 10%)

8. Packet loss:
   loss = 0
   if snr < 10: loss += random(1, 5)%
   if congestion > 5: loss += random(0.5, 3)%
```

---

## Reward Function

```python
def get_reward(action, observations):
    obs = observations[action]
    reward = (
        math.log2(max(1, obs["throughput_mbps"])) / 10    # Throughput (log scale)
        - obs["latency_ms"] / 200                          # Latency penalty
        - obs["packet_loss_pct"] / 5                       # Loss penalty
        + max(0, obs["snr_db"]) / 60                       # Signal quality bonus
    )
    if action != previous_action:
        reward -= 0.3    # Switching penalty (hysteresis)
    return reward
```

### Why This Reward Design

| Component | Rationale |
|-----------|-----------|
| `log2(throughput)/10` | Log scale prevents very fast networks from dominating. Diminishing returns above 50 Mbps. |
| `-latency/200` | Linear penalty. 200ms = -1.0 reward. Strongly discourages high-latency networks. |
| `-loss/5` | 5% loss = -1.0 reward. Packet loss is very bad for real-time applications. |
| `+snr/60` | Bonus for clean signal. Encourages picking networks with margin. |
| `-0.3 switch` | Prevents oscillation. Real switching costs ~2 seconds of downtime. |

---

## Training Results

### Final Metrics

```
Model parameters:     17,274
Training episodes:    1,000
Steps per episode:    100
Total training steps: 100,000
Replay buffer size:   50,000
Training time:        536 seconds (8.9 minutes)
Hardware:             Apple M1, CPU only
PyTorch version:      2.8.0
```

### Learning Curve

```
Episode  100: Avg reward -43.80 | Best -21.56 | Alpha 0.380
Episode  200: Avg reward -43.11 | Best -21.56 | Alpha 0.231
Episode  300: Avg reward -45.50 | Best -21.56 | Alpha 0.233
Episode  400: Avg reward -45.89 | Best -17.35 | Alpha 0.211
Episode  500: Avg reward -43.14 | Best -17.35 | Alpha 0.204
Episode  600: Avg reward -43.62 | Best -17.35 | Alpha 0.217
Episode  700: Avg reward -43.55 | Best -17.35 | Alpha 0.194
Episode  800: Avg reward -46.61 | Best -17.35 | Alpha 0.219
Episode  900: Avg reward -43.49 | Best -17.35 | Alpha 0.185
Episode 1000: Avg reward -43.58 | Best -17.35 | Alpha 0.172
```

### Evaluation (50 Unseen Episodes)

```
SAC-LTC Agent:
  Mean reward:  -27.05
  Std reward:    21.86
  Min reward:  -106.55
  Max reward:    10.10

Random Baseline:
  Mean reward:  -42.43

Improvement: 36.2% over random selection
```

### What the Numbers Mean

- **Negative rewards are normal**: latency always costs something (-latency/200), and switching costs -0.3. A score of -27 means the agent finds good networks with reasonable throughput and low latency.
- **Random scores -42**: because it constantly switches (paying the penalty) and often picks poor networks.
- **Best episode at +10**: the agent found a very good network early and stayed on it (low latency, high throughput, no switching).
- **Worst episode at -106**: extremely challenging environment (high congestion, all networks poor).

---

## Reproducibility

To reproduce the exact training run:

```bash
# Install dependencies
pip install torch numpy

# Train with same parameters
python3 train_sac_ltc.py --episodes 1000

# Evaluate
python3 train_sac_ltc.py --eval
```

Random seeds are set per episode (`seed = episode_number`), so the environments are deterministic. However, PyTorch's stochastic operations (sampling actions, random batches) introduce some variance. Results will be close but not bit-identical across runs.

## Data Export

Sample training data is exported to `data/` directory:
- `sample_episode.json` — one complete episode with all observations, actions, and rewards
- `sample_environment.json` — one environment configuration showing network parameters
- `training_log.json` — episode-by-episode reward history
