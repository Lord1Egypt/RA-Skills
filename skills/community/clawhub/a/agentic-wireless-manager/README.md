# Agentic Liquid Wireless Manager

**The first wireless network intelligence layer built for agentic AI systems running on laptops and PCs.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Linux%20%7C%20Windows-lightgrey.svg)]()

---

## The Problem

Laptops running local agentic AI (Claude, Manus, OpenClaw, local LLMs) depend entirely on their wireless connection. But:

1. **No visibility.** Your OS shows signal bars. It doesn't tell you that 5 neighbor networks are fighting for your channel, that your hotspot's cellular backhaul is throttled, or that someone walking past just caused a 10dBm signal drop.

2. **No intelligence.** Built-in tools offer "reset your adapter" as troubleshooting. They can't tell you WHY your connection degraded, or predict that it will degrade at 6pm when your neighbors come home.

3. **No autonomy.** You manually switch networks, manually check speed, manually diagnose. An agentic AI running on your laptop should be able to manage its own connectivity.

4. **No explainability.** When your video call drops, nothing tells you it was because a microwave oven on the floor below just fired up on your 2.4GHz channel.

## Our Solution

A lightweight AI agent that runs alongside your agentic AI, continuously monitoring and optimizing the wireless environment using **SAC-LTC (Soft Actor-Critic with Liquid Time-Constant cells)** — a neural architecture that adapts its temporal reasoning speed to match real-world wireless dynamics.

```
Your Agentic AI (Claude, Manus, OpenClaw, etc.)
      |
      | "Why is my internet slow?"
      v
[Agentic Liquid Wireless Manager]
      |
      |--- Reads Wi-Fi adapter (passive, read-only)
      |--- Runs SAC-LTC inference (~0.5ms, CPU, 17K params)
      |--- Returns: explanation + action + confidence
      |
      v
"Ch149 has 5 competing networks. Your iPhone hotspot's
 cellular backhaul spiked to 138ms. Switching DNS to
 save 20ms. Move your phone closer — signal dropped 8dBm."
```

## What Makes This Different

### vs. Built-In OS Tools

| Capability | macOS/Windows/Linux Built-In | This System |
|-----------|---------------------------|-------------|
| Signal info | Bars or single dBm number | 0-100 score with component breakdown |
| Troubleshooting | "Reset adapter" / generic wizard | "Ch149 has 5 competing networks, your SNR dropped 12dB from adjacent-channel interference" |
| Temporal awareness | Current snapshot only | LTC tracks 24h trends, predicts degradation, remembers patterns |
| Network switching | Manual | Autonomous (SAC-LTC decides, confidence-gated) |
| Hotspot awareness | None | Detects iPhone/Android hotspot, fingerprints 3G/4G/5G, measures backhaul vs Wi-Fi hop |
| Interference detection | None | Classifies microwave, Bluetooth, radar, neighboring APs by temporal signature |
| Presence detection | None | Senses human movement through walls via RSSI variance |
| Navigation guidance | None | "Walk 2m to your right for 6dBm improvement" |
| Channel intelligence | None | Full congestion map with competitor identification |

### vs. Commercial Wi-Fi Analyzers (NetSpot, WiFi Explorer, inSSIDer)

| Capability | Commercial Analyzers | This System |
|-----------|---------------------|-------------|
| Scanning | Manual scan, visual heatmap | Continuous autonomous monitoring |
| Actions | Report only — you decide what to do | Auto-optimizes: switches networks, DNS, cache, adapter |
| AI intelligence | None — just displays data | SAC-LTC makes decisions, explains reasoning |
| Temporal memory | None — snapshot per scan | LTC cell carries 24h of temporal context |
| Agentic integration | None — standalone GUI app | Designed for AI agents (Claude, Manus, OpenClaw) |
| Presence sensing | None | Wi-Fi sensing via RSSI variance analysis |
| Price | $10-50 | Free, open source |

### vs. Research Wi-Fi Sensing Systems

| Capability | Research Systems (CSI-based) | This System |
|-----------|---------------------------|-------------|
| Hardware | Modified drivers, specific NICs, CSI extraction tools | Any laptop with standard Wi-Fi adapter |
| Data | Channel State Information (amplitude + phase) | RSSI only (universally available) |
| Accuracy | Sub-meter localization possible | Quadrant-level (front/back/left/right) |
| Setup | Complex driver patching, specialized firmware | `pip install torch numpy` |
| Deployment | Lab environment | Any laptop, any OS |
| Temporal intelligence | Fixed-window statistics | LTC adaptive time constants |

## Benchmark Results

### SAC-LTC vs Random Network Selection

Tested on 50 unseen physics-generated environments (ITU-R/3GPP models):

```
SAC-LTC Agent:
  Mean reward:   -27.05  (higher is better)
  Std:            21.86
  Best episode:   +10.10
  Worst episode: -106.55

Random Baseline:
  Mean reward:   -42.43

IMPROVEMENT: 36.2% over random
```

### Presence Detection Accuracy

Tested with synthetic RSSI traces (quiet room vs simulated human movement):

```
Quiet room (no movement):
  Classification: "none"
  Confidence: 82.8%
  False positive rate: <5%

Active movement (simulated person walking):
  Classification: "active_movement"
  Confidence: 85.2%
  Detection rate: >90% for movement >3dBm variance

Periodic interference (microwave signature):
  Classification: "possible_interference"
  Correctly identified as non-human: 60% confidence reduction applied
```

### Resource Usage (Measured)

```
Model inference:  ~0.5ms per decision (CPU, Apple M1)
Training:         536 seconds for 1000 episodes (CPU only)
Memory:           ~30MB (PyTorch + model)
Disk:             ~400KB (weights JSON)
Network overhead: <2MB per scan cycle (1MB speed test + pings + DNS)
CPU utilization:  <2% during monitoring (1 scan every 2 minutes)
```

## Architecture

```
Raw Network Data (RSSI, noise, latency, throughput, loss, congestion, band, type)
    |
    v
[Normalize to 0-1] — 8 features per network
    |
    v
[LTC Cell] — Liquid Time-Constant neuron (continuous-time ODE)
  tau(x) * dh/dt = -h + tanh(W_h*h + W_x*x + b)
  tau(x) = tau_base + softplus(W_tau*x + b_tau)
  input: 8 → hidden: 32
  Sequence: last 8 observations (sliding window)
    |
    v
[KAN Actor] — Kolmogorov-Arnold Network (interpretable)
  KANLinear(32→16) → LayerNorm → KANLinear(16→N) → Softmax
  Each KAN layer: base_weight(SiLU) + spline_weight(RBF B-spline)
    |
    v
Action probabilities + Feature attributions + Plain English explanation
```

**Total: 17,274 parameters. CPU-only. No GPU needed.**

Full architecture disclosure: [docs/SAC_LTC_ARCHITECTURE.md](docs/SAC_LTC_ARCHITECTURE.md)

## Quick Start

### 1. Install

```bash
git clone https://github.com/Danielfoojunwei/Agentic-Liquid-Wireless-Manager.git
cd Agentic-Liquid-Wireless-Manager

pip install torch numpy
```

### 2. Initialize and Test

```bash
python3 sac_ltc_agent.py --init-weights
python3 sac_ltc_agent.py --test
```

### 3. Train (Optional — heuristic weights work out of the box)

```bash
python3 train_sac_ltc.py --episodes 2000
python3 train_sac_ltc.py --eval
```

### 4. Use with Your Agentic AI

See platform-specific instructions below.

## Usage on Agentic AI Platforms

### Claude Code

**Step 1:** Copy the skill file:
```bash
# Option A: Copy to your project
cp SKILL.md /path/to/your/project/SKILL.md

# Option B: Copy to global skills directory
mkdir -p ~/.claude/skills/net-intel
cp SKILL.md ~/.claude/skills/net-intel/SKILL.md
cp sac_ltc_agent.py ~/.claude/skills/net-intel/sac_ltc_agent.py
```

**Step 2:** Ensure the Python agent is accessible:
```bash
# Initialize weights (one-time)
python3 sac_ltc_agent.py --init-weights
```

**Step 3:** Use naturally in conversation:
```
You: "Check my network"
You: "Why is my WiFi slow?"
You: "Start sentinel mode"
You: "Is someone behind that wall?"
You: "What's competing for my channel?"
You: "Where should I move for better signal?"
```

Or invoke directly: `/net-intel`

### Manus

**Step 1:** Add as a tool in your Manus agent configuration:
```yaml
tools:
  - name: net-intel
    description: "Wireless network intelligence — diagnose, optimize, and monitor Wi-Fi/hotspot connectivity"
    type: shell
    commands:
      scan: |
        python3 /path/to/sac_ltc_agent.py --explain "$(python3 -c "
        import subprocess, re, json
        out = subprocess.run(['system_profiler', 'SPAirPortDataType'], capture_output=True, text=True).stdout
        # ... parse and output JSON array of network observations
        ")"
      sense: |
        python3 /path/to/sac_ltc_agent.py --sense "$(python3 -c "
        import subprocess, re, json, time
        # ... collect 30 seconds of RSSI samples and output JSON
        ")"
```

**Step 2:** Reference in your Manus agent's system prompt:
```
You have access to a wireless network intelligence tool called net-intel.
Use it when the user asks about their network, WiFi, internet speed,
or connectivity issues. It can also detect human presence through
WiFi signal analysis.
```

**Step 3:** The agent can call it like any other tool:
```
User: "My internet seems slow"
Agent: [calls net-intel scan] → gets JSON with scores, explanations, recommendations
Agent: "Your WiFi score is 65/100. The issue is channel congestion — 5 networks
        are sharing Channel 149. I recommend..."
```

### OpenClaw

**Step 1:** Register as a skill in your OpenClaw workspace:
```yaml
# openclaw_skills.yaml
skills:
  net-intel:
    name: "Agentic Liquid Wireless Manager"
    description: "AI-powered wireless network diagnostics, optimization, and sensing"
    trigger_phrases:
      - "check network"
      - "wifi slow"
      - "internet issues"
      - "someone nearby"
      - "signal strength"
    entry_point: "python3 sac_ltc_agent.py"
    args:
      scan: "--explain"
      sense: "--sense"
      test: "--test"
    working_directory: "/path/to/Agentic-Liquid-Wireless-Manager"
    requirements:
      - torch
      - numpy
```

**Step 2:** Add to your OpenClaw agent's capabilities:
```python
# In your OpenClaw agent setup
from openclaw import Agent, Skill

agent = Agent(
    skills=[
        Skill.from_yaml("openclaw_skills.yaml", "net-intel")
    ]
)
```

**Step 3:** The agent automatically invokes the skill when relevant topics arise.

### Any LLM Agent (Generic Integration)

The system is a CLI tool. Any agent that can execute shell commands can use it:

```bash
# Quick scan with AI decision
python3 sac_ltc_agent.py --explain '[{"ssid":"MyWiFi","rssi_dbm":-47,...}]'

# Presence detection
python3 sac_ltc_agent.py --sense '[{"ssid":"AP1","rssi":-50},{"ssid":"AP1","rssi":-53},...]'

# Self-test
python3 sac_ltc_agent.py --test
```

Output is structured (JSON for `--decide`/`--sense`, formatted text for `--explain`/`--test`), parseable by any agent framework.

## Modes of Operation

| Mode | Trigger | What It Does | Resource Usage |
|------|---------|-------------|----------------|
| **Quick Scan** | "Check my network" | One-shot diagnosis, scoring, recommendations | ~15 seconds, 2MB network |
| **Monitor** | "Start monitoring" | Autonomous background optimization every 2 min | <1% CPU, 2MB/cycle |
| **Sentinel** | "Sentinel mode" | Live presence detection + RF awareness every 10s | <2% CPU, 0 network (passive) |
| **Query** | "Why was my internet slow at 3pm?" | Answers from monitoring history + SAC-LTC reasoning | Read-only, instant |

## Training Data and Physics Models

The agent is NOT trained on a static dataset. Each training episode generates a **physics-grounded wireless environment** using real propagation models:

| Model | Standard | What It Computes |
|-------|----------|-----------------|
| Indoor path loss | ITU-R P.1238 | RSSI from distance, frequency, wall count |
| Rain attenuation | ITU-R P.838-3 | Signal loss from precipitation |
| Urban path loss | 3GPP TR 38.901 | Cellular path loss (7-24 GHz) |
| Channel capacity | Shannon-Hartley | Theoretical throughput from SNR + bandwidth |
| Thermal noise | Boltzmann (kTB) | Noise floor from bandwidth and temperature |

Full training details, data samples, and reproducibility instructions: [docs/TRAINING_PIPELINE.md](docs/TRAINING_PIPELINE.md)

Sample training data exported to: [`data/`](data/)

## Permissions and Controls

**Full disclosure** — every permission, every command, every data flow is documented:
[docs/PERMISSIONS_AND_CONTROLS.md](docs/PERMISSIONS_AND_CONTROLS.md)

Key principles:
- **Client-only.** Zero access to or control over any access point.
- **Passive-first.** Network scanning reads public beacon signals. No probing.
- **Local-only.** No data leaves the device. No cloud, no telemetry, no phone-home.
- **Reversible.** Every optimization action can be undone.
- **Transparent.** Every admin command is documented with exact syntax.
- **Consent-based.** Sentinel mode requires explicit user activation.

## Documentation

| Document | Contents |
|----------|----------|
| [SAC_LTC_ARCHITECTURE.md](docs/SAC_LTC_ARCHITECTURE.md) | Complete neural architecture — LTC cell ODE, KAN layers, twin critics, SAC algorithm, every parameter |
| [TRAINING_PIPELINE.md](docs/TRAINING_PIPELINE.md) | Physics models, environment generation, reward function, training results, reproducibility |
| [PERMISSIONS_AND_CONTROLS.md](docs/PERMISSIONS_AND_CONTROLS.md) | Every permission needed, every command used, data storage, privacy policy |
| [RF_ENVIRONMENT_INTELLIGENCE.md](docs/RF_ENVIRONMENT_INTELLIGENCE.md) | Congestion analysis, interference classification, hotspot intelligence, presence detection, distance estimation |
| [CROSS_PLATFORM_COMMANDS.md](docs/CROSS_PLATFORM_COMMANDS.md) | Every OS-specific command with exact syntax for macOS, Linux, Windows |
| [SKILL.md](SKILL.md) | The complete Claude Code skill file |

## Repository Structure

```
Agentic-Liquid-Wireless-Manager/
  README.md                          This file
  LICENSE                            MIT License
  CONTRIBUTING.md                    Contribution guidelines
  SKILL.md                           Claude Code skill (all modes)
  sac_ltc_agent.py                   Lightweight inference agent (~500 lines)
  train_sac_ltc.py                   Training pipeline (~600 lines)
  data/
    sample_environment.json           One training environment (5 networks)
    sample_episode.json               One complete training episode (20 steps)
    training_log.json                 Full training results and hyperparameters
  docs/
    SAC_LTC_ARCHITECTURE.md           Complete architecture disclosure
    TRAINING_PIPELINE.md              Training data and physics models
    PERMISSIONS_AND_CONTROLS.md       Full permissions disclosure
    RF_ENVIRONMENT_INTELLIGENCE.md    RF analysis techniques
    CROSS_PLATFORM_COMMANDS.md        OS-specific command reference
```

## Hardware Requirements

```yaml
required:
  wifi_adapter: "Built-in or USB Wi-Fi adapter"
  internet: "Wi-Fi or mobile hotspot connection"
  terminal: "Bash (macOS/Linux) or PowerShell (Windows)"
  python: "3.8+"

optional:
  pytorch: "For SAC-LTC AI decisions (falls back to heuristics without)"
  numpy: "For numerical operations"
  admin_access: "For DNS optimization, DHCP renewal, adapter restart"

resource_budget:
  cpu: "< 2% (inference ~0.5ms per decision)"
  ram: "< 30 MB (PyTorch + 17K parameter model)"
  gpu: "None required"
  disk: "< 2 MB (weights + history)"
  network: "< 2 MB per scan cycle"
```

## Contributing

We welcome contributions. Please see [CONTRIBUTING.md](CONTRIBUTING.md).

Key areas:
- Cross-platform testing (especially Windows and various Linux distros)
- Training improvements (more episodes, curriculum learning, real-world validation)
- New interference signatures (add detection patterns for more device types)
- Spatial calibration improvements (better directional accuracy)
- Integration guides for more agentic AI platforms

## License

MIT License. See [LICENSE](LICENSE).

## Credits

- Derived from [PreceptualAI UHCI](https://github.com/Danielfoojunwei/PreceptualAI-Universal-Heterogeneous-Connectivity-Intelligence-UHCI-) by Daniel Foo Jun Wei
- SAC-LTC architecture inspired by Hasani et al. "Liquid Time-constant Networks" (2021) and the UHCI universal spectrum agent
- KAN layers based on Liu et al. "KAN: Kolmogorov-Arnold Networks" (2024)
- RF physics from ITU-R P.1238, ITU-R P.838-3, 3GPP TR 38.901
