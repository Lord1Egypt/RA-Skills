# RF Environment Intelligence: How the System Understands Your Wireless World

The system turns raw signal data into a complete picture of the electromagnetic landscape around you. This document explains every analysis technique.

## What We Measure

From your laptop's Wi-Fi adapter (passive, read-only):

| Measurement | Source | What It Tells Us |
|------------|--------|-----------------|
| RSSI (dBm) | Beacon frames from each AP | How strong each signal is at your location |
| Noise floor (dBm) | Adapter's noise measurement | Background electromagnetic noise level |
| SNR (dB) | RSSI minus noise | How clearly your laptop can hear the AP |
| Channel number | Beacon frame | Which frequency each AP uses |
| Bandwidth (MHz) | Beacon HT/VHT/HE IEs | How wide each channel is (20/40/80/160) |
| PHY mode | Beacon capabilities | Wi-Fi generation (a/b/g/n/ac/ax) |
| BSSID | Beacon header | Unique AP identifier |
| Security | Beacon RSN IE | Encryption type |

From active tests (using existing connection only):

| Test | Method | What It Tells Us |
|------|--------|-----------------|
| Latency | ICMP ping (10 packets to 8.8.8.8) | Round-trip time to internet |
| Packet loss | Same ping test | Reliability of connection |
| DNS speed | dig queries to current and alternative DNS | Name resolution performance |
| Throughput | HTTP download of 1MB file | Actual download speed |

---

## Congestion Analysis

### Co-Channel Congestion (CCI)

When multiple APs share the same channel, they must take turns transmitting (CSMA/CA protocol). More APs = more waiting = slower speeds.

```
Detection:
  Count all visible BSSIDs on the same channel as your connection.

Impact estimation:
  1 network (you alone): 100% airtime available
  2 networks: ~50% airtime (moderate)
  3-4 networks: ~25-33% airtime (crowded)
  5+ networks: <20% airtime (very congested)

  Note: actual impact depends on traffic load of each network.
  Idle APs still send beacons but don't consume much airtime.
```

### Adjacent-Channel Interference (ACI)

Especially important on 2.4 GHz where only channels 1, 6, and 11 are non-overlapping.

```
2.4 GHz:
  Each channel is 22 MHz wide, spaced 5 MHz apart.
  Channel 1 (2412 MHz) overlaps with channels 2, 3, 4, 5.
  Only channels 1, 6, 11 are completely non-overlapping.
  A network on channel 3 interferes with BOTH channel 1 and channel 6.

5 GHz:
  Channels are wider but non-overlapping at 20 MHz.
  However, 80 MHz channels span 4x 20 MHz channels:
    Ch149 (80MHz) occupies channels 149, 153, 157, 161.
    A 20 MHz network on Ch153 sits inside your 80 MHz band.
```

### Channel Heat Map

The system builds a complete picture of every channel's congestion:

```
For each channel in the band:
  Count: number of networks
  Power: sum of all RSSI values (total interference power)
  Overlap: number of networks with overlapping bandwidth
  Score: lower is better (fewer networks, less power)

Recommendation: the channel with the lowest score is the best choice.
```

---

## Interference Classification

The system identifies interference sources by their temporal signature in the RSSI/noise data.

### Microwave Oven (2.4 GHz)
```
Signature:
  - 2.4 GHz only (does not affect 5 GHz)
  - Periodic noise spikes: ~15 seconds on, ~5 seconds off
  - Noise increase: 10-20 dB during active periods
  - Correlates with meal times (12:00, 18:00-19:00)
  - Duration: 1-5 minutes per event

Detection:
  If noise spikes are periodic (autocorrelation > 0.5)
  AND only on 2.4 GHz
  AND duration matches cooking cycle
  → classify as "microwave"
```

### Bluetooth Devices (2.4 GHz)
```
Signature:
  - 2.4 GHz only
  - Rapid, random SNR fluctuations
  - Frequency hopping causes intermittent interference
  - Constant low-level, not periodic
  - Variance > 5 dBm in SNR over 30 seconds

Detection:
  If SNR variance is high AND not periodic AND 2.4 GHz only
  → classify as "Bluetooth/frequency hopping"
```

### Radar (5 GHz DFS Channels)
```
Signature:
  - 5 GHz channels 52-144 only (DFS channels)
  - Adapter suddenly changes channel
  - Brief disconnection (1-2 seconds)
  - Required by regulation — adapter MUST vacate if radar detected

Detection:
  If monitoring history shows sudden channel change on DFS channel
  AND brief connectivity gap
  → classify as "DFS radar event"
```

### Neighboring AP (Co-Channel)
```
Signature:
  - Visible as a BSSID in scan results
  - Consistent signal level (not intermittent)
  - Same channel as your connection
  - Competing for airtime via CSMA/CA

Detection:
  Direct observation from network scan.
  Quantified by RSSI (stronger = more impact).
```

---

## Hotspot Intelligence

### Cellular Generation Fingerprinting

When connected to a mobile hotspot, the system infers the cellular technology from measured characteristics:

| Generation | Latency | Throughput | Jitter | Confidence |
|-----------|---------|------------|--------|------------|
| 3G | 80-200+ ms | 1-5 Mbps | >30 ms | High |
| 4G/LTE | 20-60 ms | 5-50 Mbps | 10-20 ms | High |
| 5G Sub-6 | 10-30 ms | 50-300 Mbps | <10 ms | Medium |
| 5G mmWave | <10 ms | 300-1000+ Mbps | <5 ms | Low (rare) |

### iPhone Hotspot Detection

```
Method: IP address subnet analysis
  172.20.10.x/28 (subnet mask 255.255.255.240) = iPhone hotspot
  192.168.43.x or 192.168.49.x = Android hotspot
  Other 192.168.x.x = likely infrastructure router

This is 100% reliable — Apple and Google use fixed subnets for tethering.
```

### Backhaul Quality Assessment

```
The "backhaul" is the phone's cellular connection to the tower.
The "Wi-Fi hop" is the wireless link from your laptop to the phone.

If RSSI to phone is strong (-40 to -50 dBm)
BUT latency is high (>80ms) or throughput is low (<5 Mbps):
  → Bottleneck is the cellular backhaul, not the Wi-Fi hop.
  → Nothing the system can do except advise:
    "Move your phone near a window for better cell reception"

If RSSI to phone is weak (-65+ dBm)
AND latency is high:
  → Both Wi-Fi hop AND backhaul may be problems.
  → Advise: "Move your phone closer to your laptop"
```

---

## RSSI-to-Distance Estimation

Using the ITU-R P.1238 indoor propagation model in reverse:

```
Given: RSSI (measured), TxPower (estimated), frequency
Find: distance

Path Loss = TxPower - RSSI
FSPL = 20*log10(d) + 20*log10(f_MHz) + 32.44
Indoor excess = 10 * (N/20 - 1) * log10(d)

For 5 GHz (N=30):
  d = 10^((PathLoss - 46.2) / 30) meters

For 2.4 GHz (N=28):
  d = 10^((PathLoss - 40.2) / 28) meters

Assumed TxPower:
  Infrastructure AP: 20 dBm
  Phone hotspot: 18 dBm
```

### Accuracy Limitations

- Walls reduce signal by 5-10 dB each → makes distance appear farther
- Multipath reflections can increase or decrease signal unpredictably
- Antenna orientation affects RSSI by 3-5 dB
- Accuracy: ±50% (useful for "same room" vs "next room", not precise meters)

---

## Presence Detection: Deep Dive

### The Physics

A human body is approximately 60% water. Water absorbs 2.4 GHz radiation very effectively (this is how microwave ovens work). When a person moves through a Wi-Fi signal path:

1. **Absorption**: body absorbs 3-10 dBm of signal energy
2. **Reflection**: body reflects signal, creating multipath changes
3. **Diffraction**: signal bends around the body, changing phase

These effects cause the RSSI measured by your laptop to fluctuate.

### Why LTC is Better for Sensing

Normal sensing: fixed 10-second window, compute variance, apply threshold.

LTC sensing: adaptive time constant adjusts to match the movement pattern.

```
Person walking fast:
  RSSI changes every 0.5-1 second
  Normal: 10-sec window catches it but smears the peaks
  LTC: tau shrinks to ~1 second, tracks individual footsteps

Person walking slowly:
  RSSI changes over 3-5 seconds
  Normal: 10-sec window may attribute it to noise
  LTC: tau grows to ~3 seconds, integrates the slow trend

Microwave interference:
  Periodic 15-second on/off cycle
  Normal: may confuse with human movement
  LTC: tau locks to the cycle period, autocorrelation detects periodicity
  → classified as "appliance", not "person"
```

### Spatial Calibration

Prerequisite for directional sensing. Maps each visible AP to a direction relative to the user.

```
Method 1: User tells the system
  "My router is to my right, my phone is in front of me"
  → Simple mapping, less precise

Method 2: Body-blocking
  The human body absorbs ~10-15 dBm at 2.4 GHz.
  By turning in the chair, the user's body blocks signals from one direction.

  Step 1: Face forward (baseline for all APs)
  Step 2: Turn LEFT → body blocks RIGHT → APs that drop are to the RIGHT
  Step 3: Turn RIGHT → body blocks LEFT → APs that drop are to the LEFT
  Step 4: Lean forward → body blocks BEHIND → APs that drop are BEHIND

  The direction with the largest RSSI drop for each AP = that AP's direction
```

### Detection Confidence Levels

```
variance_ratio = measured_variance / baseline_variance

> 5.0: "active_movement"    → high confidence (75-95%)
> 3.0: "likely"              → moderate confidence (50-85%)
> 1.5: "possible"            → low confidence (25-60%)
≤ 1.5: "none"               → high confidence of NO movement (80-95%)

Autocorrelation > 0.5: reclassify as "possible_interference" (periodic source)
Confidence reduced by 40% for periodic patterns.
```
