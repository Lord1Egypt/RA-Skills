---
name: net-intel
description: >
  UHCI Network Intelligence — AI-powered wireless network manager with SAC-LTC.
  Diagnoses, optimizes, and manages Wi-Fi and 3G/4G/5G hotspot switching.
  Provides deep RF environment awareness: signal quality, interference sources,
  channel congestion, presence detection, and navigation guidance.
  Use when: wifi slow, network issues, internet problems, signal weak,
  hotspot management, check connection, speed test, fix network, optimize wifi,
  why is my internet slow, network switch, net intel, sentinel mode,
  is someone nearby, interference, congestion, which direction, channel map,
  what is fighting for my network, which AP is best, walk towards signal.
---

# UHCI Net-Intel: Universal Heterogeneous Connectivity Intelligence

Derived from [PreceptualAI UHCI](https://github.com/Danielfoojunwei/PreceptualAI-Universal-Heterogeneous-Connectivity-Intelligence-UHCI-).
SAC-LTC (Soft Actor-Critic with Liquid Time-Constant cells) for intelligent network management.

## Hardware Requirements

```
REQUIRED:
  Wi-Fi adapter (built-in or USB) — for reading signal data
  Internet connection (Wi-Fi or hotspot) — for speed/latency tests
  Terminal: Bash (macOS/Linux) or PowerShell (Windows)
  Python 3.8+ with PyTorch and NumPy — for SAC-LTC inference

OPTIONAL:
  Admin/sudo access — for DNS optimization, DHCP renewal, adapter restart

RESOURCE USAGE:
  CPU: < 2% (tiny model, ~15K parameters)
  RAM: < 30 MB (PyTorch + model)
  GPU: None needed
  Disk: < 2 MB (model weights + history)
  Network: < 2 MB per full scan cycle
```

## Permissions Required

### From the User / Hardware Owner
Before running, confirm the user grants:
1. **Wi-Fi adapter read access** — to read RSSI, noise, channel from the adapter
2. **Network scan permission** — OS may prompt for location/Wi-Fi access
3. **Terminal execution** — to run OS network commands
4. **Python execution** — for SAC-LTC inference engine
5. **Admin/sudo** (optional) — only for auto-optimization actions
6. **File write to ~/.net-intel/** — for history, weights, spatial calibration
7. **Background execution** — for monitor and sentinel modes

### From Access Points
**NOTHING.** We are a client device only. We passively receive AP beacon signals that are publicly broadcast per 802.11 spec. We never authenticate to, communicate with, or modify any AP we are not connected to.

## Setup

Run these checks on first use:

```bash
# Check OS
uname -s 2>/dev/null || echo "Windows"

# Check Python + dependencies
python3 -c "import torch; import numpy; print('Dependencies OK')" 2>&1

# If missing, install:
# pip3 install torch numpy

# Create data directory
mkdir -p ~/.net-intel

# Initialize or check model weights
WEIGHTS="$HOME/.net-intel/weights.json"
if [ ! -f "$WEIGHTS" ]; then
  python3 "$(dirname "$0")/sac_ltc_agent.py" --init-weights
fi
```

If Python/PyTorch is not available, the skill falls back to heuristic-only mode (no SAC-LTC AI decisions, but all diagnostics and monitoring still work).

## Step 1: Detect OS and Wi-Fi Interface

Detect the platform and find the Wi-Fi interface name.

**macOS:**
```bash
WIFI_IF=$(networksetup -listallhardwareports | grep -A 1 "Wi-Fi" | grep Device | awk '{print $2}')
echo "Interface: $WIFI_IF"
```

**Linux:**
```bash
WIFI_IF=$(iw dev 2>/dev/null | grep Interface | head -1 | awk '{print $2}')
[ -z "$WIFI_IF" ] && WIFI_IF=$(nmcli -t -f DEVICE,TYPE dev | grep wifi | cut -d: -f1 | head -1)
echo "Interface: $WIFI_IF"
```

**Windows (PowerShell):**
```powershell
$wifiAdapter = Get-NetAdapter | Where-Object {$_.MediaType -eq "802.11" -or $_.InterfaceDescription -like "*Wi-Fi*"} | Select-Object -First 1
$WIFI_IF = $wifiAdapter.Name
Write-Output "Interface: $WIFI_IF"
```

## Step 2: Scan All Visible Networks

Gather RSSI, noise, channel, SSID, BSSID for ALL visible networks (not just connected).

**macOS:**
```bash
# Connected network details + ALL nearby networks
system_profiler SPAirPortDataType 2>/dev/null
```

Parse this output to extract for EACH visible network:
- SSID, BSSID
- RSSI (dBm), Noise (dBm) → compute SNR = RSSI - Noise
- Channel number, band (2.4/5/6 GHz), bandwidth (20/40/80/160 MHz)
- PHY mode (802.11a/b/g/n/ac/ax)
- Security type
- Whether it's a hotspot (detect by SSID patterns: "iPhone", "Android", "Galaxy", "Pixel", "Hotspot", "Mobile", "Moto", "OnePlus", "Samsung", "Xiaomi")

**Linux:**
```bash
# All visible networks with signal, channel, frequency, rate
nmcli -f SSID,BSSID,SIGNAL,FREQ,CHAN,RATE,SECURITY,MODE dev wifi list 2>/dev/null
# For noise floor (if available)
iwconfig $WIFI_IF 2>/dev/null | grep -i noise
```

**Windows (PowerShell):**
```powershell
# All visible networks with BSSID, signal, channel
netsh wlan show networks mode=bssid
# Connected interface details
netsh wlan show interfaces
```

**Note on Windows:** Windows reports signal as percentage (0-100%), not dBm. Convert approximately: `dBm = (signal_pct / 2) - 100`. Windows does not expose noise floor; estimate noise at -90dBm for typical indoor environments.

## Step 3: Performance Tests (Automatic)

Run these automatically every monitoring cycle. All tests are lightweight.

**Latency + Packet Loss:**
```bash
# macOS/Linux
ping -c 10 -q 8.8.8.8 2>&1 | tail -2
# Parse: avg latency (ms), packet loss (%)
```
```powershell
# Windows
ping -n 10 8.8.8.8 | Select-String "Average|Lost"
```

**DNS Speed:**
```bash
# Test current DNS
dig google.com +noall +stats 2>&1 | grep "Query time"
# Compare with fast public DNS
dig google.com @1.1.1.1 +noall +stats 2>&1 | grep "Query time"
dig google.com @8.8.8.8 +noall +stats 2>&1 | grep "Query time"
```
```powershell
# Windows
Measure-Command { Resolve-DnsName google.com -DnsOnly } | Select TotalMilliseconds
Measure-Command { Resolve-DnsName google.com -Server 1.1.1.1 -DnsOnly } | Select TotalMilliseconds
```

**Throughput:**
```bash
# Download 1MB test file, measure speed
curl -o /dev/null -w '{"speed_bytes_sec": %{speed_download}, "time_sec": %{time_total}}' \
  -s --max-time 15 http://speedtest.tele2.net/1MB.zip 2>/dev/null
```

## Step 4: Score All Networks (0-100)

For each visible network, compute a quality score using these weights:

| Component | Weight | Excellent | Good | Fair | Poor |
|-----------|--------|-----------|------|------|------|
| Signal (RSSI) | 30 pts | >-50dBm: 30 | -50 to -60: 22 | -60 to -70: 15 | <-70: 7 |
| SNR | 15 pts | >40dB: 15 | 25-40: 11 | 15-25: 7 | <15: 3 |
| Latency | 25 pts | <20ms: 25 | 20-50: 19 | 50-100: 12 | >100: 5 |
| Throughput | 20 pts | >50Mbps: 20 | 10-50: 15 | 1-10: 10 | <1: 3 |
| Stability | 10 pts | 0% loss: 10 | <1%: 7 | 1-5%: 4 | >5%: 0 |

For networks we're not connected to (no latency/throughput data), estimate from signal strength:
- Estimated throughput: use Shannon capacity from SNR and bandwidth
- Estimated latency: 10ms base + 5ms per wall (inferred from RSSI vs expected FSPL)

## Step 5: SAC-LTC Decision + Explanation

Run the SAC-LTC inference engine:

```bash
# Collect all network data as JSON array
NETWORKS='[{"ssid":"MyWiFi","rssi_dbm":-47,"noise_dbm":-94,"latency_ms":12,...}, ...]'

# Get AI decision with full explanation
python3 ~/.net-intel/sac_ltc_agent.py --explain "$NETWORKS"
```

The agent returns:
- **action**: which network index to use
- **confidence**: 0-1 probability
- **feature_weights**: which RF factors drove the decision
- **temporal_trend**: stable / improving / degrading / reacting to change
- **reason**: technical explanation
- **layman_summary**: plain English explanation

## Step 6: Channel Congestion & Interference Map

Build a complete picture of the RF environment from the scan data.

### Channel Congestion Map
Group all visible networks by channel. For each channel:
- Count networks (co-channel congestion)
- Calculate total interference power: sum of all other networks' RSSI on that channel
- Check adjacent channels (within +/-2 for 2.4GHz, overlapping bands for 5GHz 80/160MHz)
- Identify the LEAST congested channel in each band

### Interference Identification
From the monitoring history, classify interference sources:

| Pattern | Likely Source | How to Identify |
|---------|-------------|-----------------|
| Periodic noise spikes (2.4GHz, 1-3min cycles) | Microwave oven | Correlates with meal times, 2.4GHz only, periodic with ~15s on/off |
| Rapid SNR fluctuations (2.4GHz) | Bluetooth devices | Frequency hopping signature, constant low-level interference |
| Persistent elevated noise (one channel) | Baby monitor / cordless phone | Narrowband, doesn't move, constant |
| Sudden channel change (5GHz DFS channels) | Radar detected | Adapter forced to vacate Ch52-144, brief disconnection |
| Broadband noise all channels | Power line / LED driver | Noise floor elevated equally across all channels |
| Intermittent strong signal on your channel | Neighbor's AP / competing device | Identifiable by BSSID, consistent presence |

### Competing Devices on Your Connection
List every device/network that shares your channel or adjacent channels:
```
WHAT'S COMPETING FOR YOUR AIRSPACE:
  Your channel: 149 (5GHz, 80MHz width)

  SAME CHANNEL (direct competition):
    "Neighbor_5G"    -52dBm  Ch149  [STRONG competitor]
    "Office_Main"    -71dBm  Ch149  [Moderate]
    "IoT_Network"    -78dBm  Ch149  [Weak but adds noise]

  OVERLAPPING CHANNELS (partial interference):
    "Guest_WiFi"     -65dBm  Ch153  [80MHz overlaps yours]

  TOTAL INTERFERENCE LOAD: High
  Your signal has to compete with 3 strong transmitters.

  WHAT YOU CAN DO:
    - Ask the "IoT_Network" owner to move to Ch44 (empty)
    - Switch your own router to Ch36 (only 1 weak network)
    - Or: the system can switch you to your 5G hotspot
      which currently scores higher (78 vs 71)
```

## Step 7: Navigation Guidance

**This is a paradigm shift:** The system tells the user exactly WHERE to move for better connectivity and WHICH device to get closer to.

### Signal Direction & Distance Estimation

From RSSI readings + calibrated spatial map, provide walking directions:

```
NAVIGATION GUIDANCE
===================
Your current connection: MyWiFi (score 65/100)

FOR BETTER WI-FI:
  Walk towards your RIGHT (that's where MyRouter is)
  Moving ~2 meters closer should improve signal by
  about 6dBm, boosting your score to ~80/100.

  Your signal: -62dBm (fair)
  Estimated at 2m closer: -56dBm (good)
  At the router: -42dBm (excellent)

FOR BEST HOTSPOT:
  Your "iPhone-Dan" hotspot is to your LEFT and BEHIND
  you. Signal is currently -68dBm (weak).
  Moving 3m towards it (left and back) would give
  you -55dBm and much better 5G speeds.

BEST OPTION RIGHT NOW:
  Stay where you are and I'll switch you to "Office_5G"
  which has the strongest signal from your current
  position (-49dBm, score 82/100). It's in FRONT of
  you and slightly to the LEFT.

AVOID:
  Don't move towards the back-right corner — that's
  where the interference source is (probably a
  microwave or Bluetooth speaker causing noise on
  your channel).
```

### How Navigation Works

1. **RSSI-to-distance estimation**: Using the indoor path loss model:
   `distance_m = 10^((tx_power - rssi - constant) / (10 * n))`
   where n=2.8 for indoor, constant accounts for frequency

2. **Direction from spatial calibration**: Each AP is mapped to a direction relative to the user (from calibration in Step 8)

3. **Signal improvement prediction**: For each potential position:
   - Closer to AP: RSSI improves ~6dB per halving of distance
   - Through walls: each wall costs ~5-10dB
   - The LTC temporal data predicts whether the signal at a location is stable or fluctuating

4. **Interference source localization**: If noise is directional (affects some APs more than others), infer the interference source's approximate direction

## Step 8: Spatial Calibration (One-Time Setup)

Map where each AP's signal is coming from relative to the user.

### Quick Calibration (tell the system)
User says: "My router is to my right, my phone is in my pocket, the office AP is behind me"
→ Map SSIDs to directions: {MyRouter: right, iPhone: pocket/near, Office_AP: behind}

### Precise Calibration (body-blocking method)
The human body absorbs 10-15dBm of 2.4GHz signal. By turning in the chair:

1. Face normally → record baseline RSSI for all APs
2. Turn LEFT (body blocks RIGHT) → APs that drop are to the RIGHT
3. Turn RIGHT (body blocks LEFT) → APs that drop are to the LEFT
4. Lean forward (body blocks BEHIND) → APs that drop are BEHIND

```bash
# Run 4 scans during calibration, save to spatial map
# macOS
system_profiler SPAirPortDataType > /tmp/cal_baseline.txt
echo "Turn LEFT now, wait 5 seconds..."
sleep 5
system_profiler SPAirPortDataType > /tmp/cal_left.txt
# ... repeat for each direction
```

Save spatial map to `~/.net-intel/spatial_map.json`:
```json
{
  "calibrated": "2026-04-05T11:30:00",
  "access_points": [
    {"bssid": "AA:BB:CC:DD:EE:01", "ssid": "MyRouter",
     "direction": "right", "baseline_rssi": -47},
    {"bssid": "AA:BB:CC:DD:EE:02", "ssid": "iPhone-Dan",
     "direction": "left", "baseline_rssi": -61}
  ]
}
```

## Step 9: Auto-Optimization Actions

These run automatically when conditions are met. The system logs what it did.

| Condition | Action | Command (macOS) | Command (Linux) | Command (Windows) |
|-----------|--------|-----------------|-----------------|-------------------|
| DNS >2x slower than 1.1.1.1 | Switch DNS | `networksetup -setdnsservers Wi-Fi 1.1.1.1 1.0.0.1` | `resolvectl dns $IF 1.1.1.1 1.0.0.1` | `Set-DnsClientServerAddress -InterfaceAlias Wi-Fi -ServerAddresses 1.1.1.1,1.0.0.1` |
| Stale DNS responses | Flush cache | `sudo dscacheutil -flushcache && sudo killall -HUP mDNSResponder` | `sudo systemd-resolve --flush-caches` | `Clear-DnsClientCache` |
| DHCP lease expiring | Renew | `sudo ipconfig set $IF DHCP` | `sudo dhclient -r $IF && sudo dhclient $IF` | `ipconfig /renew` |
| SAC-LTC confidence >0.7 for different network | Switch network | `networksetup -setairportnetwork $IF SSID [password]` | `nmcli dev wifi connect SSID` | `netsh wlan connect name=SSID` |
| Packet loss >10% for 3+ cycles | Restart adapter | `networksetup -setairportpower $IF off && sleep 2 && networksetup -setairportpower $IF on` | `sudo nmcli radio wifi off && sleep 2 && sudo nmcli radio wifi on` | `Disable-NetAdapter -Name Wi-Fi -Confirm:$false; Start-Sleep 2; Enable-NetAdapter -Name Wi-Fi -Confirm:$false` |

After each auto-action, log to `~/.net-intel/actions.log` and verify the action improved the connection by re-scanning after 10 seconds.

## Step 10: Log to History

Append every scan cycle to `~/.net-intel/history.json` (one JSON object per line, JSONL format):

```json
{"ts":"2026-04-05T11:32:00","nets":[{"ssid":"MyWiFi","rssi":-47,"noise":-94,"snr":47,"ch":149,"bw":80,"ping":12,"loss":0,"mbps":45,"score":85,"connected":true},{"ssid":"iPhone-Dan","rssi":-61,"noise":-90,"snr":29,"ch":6,"bw":40,"score":62,"connected":false,"is_hotspot":true,"cell_gen":"5g"}],"action":"stay","conf":0.92,"explain":"Strong signal + lowest latency","congestion":{"ch149":5,"ch44":0,"ch36":1},"interference":"none"}
```

Auto-prune entries older than 24 hours to keep file under 500KB.

## Modes of Operation

### Mode 1: Quick Scan (default, on-demand)
Run Steps 1-7 once, display results, done.

Output format (phone-friendly, plain English):
```
YOUR CONNECTION: Good (85/100)
================================
You're on MyWiFi — strong signal, fast speed.

SPEED: Downloads 45 Mbps, response 12ms
CHANNEL: 149 (5GHz) — a bit crowded (5 networks)

BEST OPTIONS:
  1. MyWiFi       85/100 [YOU ARE HERE]
  2. Office_5G    78/100 [in front of you]
  3. iPhone-Dan   62/100 [5G hotspot, to your left]

WHAT'S COMPETING WITH YOU:
  3 other networks on your channel.
  Strongest competitor: "Neighbor_5G" at -52dBm.

TO IMPROVE:
  Move ~2m to your right (closer to router)
  → estimated score improvement: 85 → 92

WHAT I DID: Switched DNS (saves 20ms per page)

Scanned: 11:32 AM
```

### Mode 2: Monitor (autonomous background)
Start with: "start monitoring" or "monitor my network"

Uses CronCreate with 2-minute interval. Each cycle:
1. Run Steps 2-6 (scan, test, score, decide)
2. Auto-execute optimization actions (Step 9)
3. Log to history (Step 10)
4. Alert on significant changes

The monitoring prompt for CronCreate:
```
Run /net-intel in monitor mode: scan networks, test speed, run SAC-LTC decision, auto-optimize, log to ~/.net-intel/history.json. Only report if something changed significantly (score dropped >15 points, switched networks, detected new interference, or detected presence).
```

### Mode 3: Sentinel (live spatial awareness)
Start with: "sentinel mode" or "watch around me"

High-frequency passive RSSI monitoring (every 10 seconds) for presence detection.
Uses only passive beacon RSSI reads — zero bandwidth consumption.

```
SENTINEL [LIVE] 11:32:45
========================
         FRONT
         clear
           |
LEFT ---- YOU ---- RIGHT
movement    |    clear
(72%)       |
         BEHIND
         clear

Someone is moving to your LEFT.
The signal from "Neighbor_5G" (to your left)
is wobbling — consistent with a person walking
through the signal path.

NETWORK: MyWiFi 85/100 | stable
```

Proactive alerts when movement detected, interference changes, or signal anomalies occur.

### Mode 4: Query (conversational, anytime)
User asks natural questions. The system answers from monitoring history + current scan + SAC-LTC reasoning:

- "Why is my wifi slow?" → explains from data
- "Should I switch to my hotspot?" → compares with reasoning
- "What happened at 3pm?" → reviews history log
- "Is someone behind me?" → runs sensing on calibrated APs
- "Where should I sit for best signal?" → navigation guidance
- "What's fighting for my channel?" → lists competing networks
- "Which direction is the interference coming from?" → spatial analysis

## SAC-LTC: Why It's Better Than Normal Tools

The Liquid Time-Constant cell has adaptive time constants τ(x) that automatically adjust:
- Fast RSSI changes → τ shrinks → catches fast-moving person or sudden interference
- Slow signal drift → τ grows → detects gradual degradation over hours
- Periodic patterns → τ locks to the cycle → distinguishes microwave from human movement

Normal tools use fixed thresholds. Our LTC adapts to whatever pattern is actually there.

The KAN (Kolmogorov-Arnold Network) actor is inherently interpretable — we can read which features drove every decision, making the system explainable rather than a black box.

## Privacy & Ethics

- All processing is local — no data leaves the device
- We only passively receive public AP beacon signals (broadcast by design per 802.11)
- Presence detection works by sensing signal disruptions, not identifying individuals
- History stored only in ~/.net-intel/, user-controlled
- Sentinel mode requires explicit user activation
- No beacon frames or payload data is captured — only signal strength values

## Embedded Python Agent

The SAC-LTC agent is in `sac_ltc_agent.py` alongside this skill file. It provides:
- `--test` — self-test to verify installation
- `--init-weights` — generate initial heuristic weights
- `--decide '<json>'` — get switching decision
- `--sense '<json>'` — presence detection from RSSI samples
- `--explain '<json>'` — full RF environment explanation

To train a better model with real RF physics:
```bash
python3 train_sac_ltc.py --episodes 2000
python3 train_sac_ltc.py --eval
```

The training uses real ITU-R P.1238 indoor propagation, 3GPP path loss models, and Shannon capacity — not mocks or stubs.
