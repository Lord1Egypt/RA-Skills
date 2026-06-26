# Changelog

All notable changes to Agentic Liquid Wireless Manager are documented here.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Versioning follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-04-05

### Added

**Core Agent**
- SAC-LTC (Soft Actor-Critic with Liquid Time-Constant) inference engine
- LTC cell with continuous-time ODE and input-dependent time constants
- KAN (Kolmogorov-Arnold Network) actor with interpretable spline activations
- Pure Python fallback (runs without PyTorch via numpy-only implementation)
- Feature normalization pipeline (8 RF features normalized to [0,1])
- Network scoring heuristic (0-100 composite score)

**Training Pipeline**
- Physics-grounded RF environment generation (not mocked/simulated)
- ITU-R P.1238 indoor propagation model
- ITU-R P.838-3 rain attenuation model
- 3GPP TR 38.901 UMa NLOS path loss model
- Shannon-Hartley channel capacity computation
- Thermal noise floor calculation (kTB)
- Soft Actor-Critic with twin critics, Polyak target networks, entropy tuning
- 17,274 parameter model trained in ~9 minutes on CPU
- 36.2% improvement over random baseline on 50 evaluation episodes

**Wireless Intelligence**
- Wi-Fi signal diagnostics (RSSI, noise, SNR, channel, PHY mode, MCS)
- Channel congestion mapping (co-channel and adjacent-channel analysis)
- Interference classification (microwave, Bluetooth, radar, neighboring APs)
- Hotspot detection via IP subnet analysis (iPhone 172.20.10.x, Android 192.168.43.x)
- Cellular generation fingerprinting (3G/4G/5G from latency/throughput signatures)
- Backhaul vs Wi-Fi hop quality separation
- RSSI-to-distance estimation using ITU-R indoor path loss model
- Competitor identification (which networks share your channel)
- Navigation guidance (direction and distance to better signal)

**Presence Detection**
- RSSI variance analysis for human movement detection
- Autocorrelation-based pattern classification (human vs appliance)
- Directional sensing via spatial calibration (body-blocking method)
- Confidence scoring with false-positive mitigation for periodic interference

**Explainability**
- Finite-difference feature attribution (which RF factors drove each decision)
- LTC time constant analysis (what the model is tracking: fast changes vs slow trends)
- Plain English output generation (layman-friendly explanations)
- Full technical deep-dive mode available on request

**Operating Modes**
- Quick Scan: one-shot diagnosis with scoring and recommendations
- Monitor Mode: autonomous background optimization (CronCreate, 2-min interval)
- Sentinel Mode: live spatial awareness with presence detection (10-sec interval)
- Query Mode: conversational answers from monitoring history + SAC-LTC reasoning

**Cross-Platform Support**
- macOS: system_profiler, networksetup, ifconfig
- Linux/Ubuntu: nmcli, iw, iwconfig, ip, resolvectl
- Windows: netsh wlan, Get-NetAdapter, PowerShell cmdlets

**Auto-Optimization Actions**
- DNS server switching (to fastest available)
- DNS cache flushing
- DHCP lease renewal
- Network switching (SAC-LTC confidence-gated)
- Adapter restart (on sustained packet loss)

**Documentation**
- SAC_LTC_ARCHITECTURE.md: Complete neural architecture disclosure
- TRAINING_PIPELINE.md: All physics models, data generation, training results
- PERMISSIONS_AND_CONTROLS.md: Every permission and command disclosed
- RF_ENVIRONMENT_INTELLIGENCE.md: All analysis techniques documented
- CROSS_PLATFORM_COMMANDS.md: Every OS command with exact syntax

**Data**
- sample_environment.json: One training environment (5 networks)
- sample_episode.json: One complete episode (20 steps with full observations)
- training_log.json: Hyperparameters and training results

**Plugin Metadata**
- plugin.yaml: Plugin manifest with type classification, host targets, OS targets
- package.json: npm-compatible project metadata with scripts
- CHANGELOG.md: This file
- LICENSE: MIT
- CONTRIBUTING.md: Contribution guidelines

**Host Target Integrations**
- Claude Code: SKILL.md with /net-intel invocation
- Manus: Tool YAML configuration
- OpenClaw: Skill registration YAML
- Generic LLM agents: CLI interface (--explain, --sense, --decide)

### Source

- Repository: https://github.com/Danielfoojunwei/Agentic-Liquid-Wireless-Manager
- Initial commit: `3d740ff`
- This release commit: `a323de3`
- Ref: `v1.0.0`
- Branch: `main`
- Derived from: [PreceptualAI UHCI](https://github.com/Danielfoojunwei/PreceptualAI-Universal-Heterogeneous-Connectivity-Intelligence-UHCI-)

[1.0.0]: https://github.com/Danielfoojunwei/Agentic-Liquid-Wireless-Manager/releases/tag/v1.0.0
