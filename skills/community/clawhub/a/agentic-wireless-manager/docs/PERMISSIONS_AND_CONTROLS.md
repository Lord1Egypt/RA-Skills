# Permissions and Controls: Full Disclosure

Every permission, access point, data flow, and control mechanism — fully transparent.

## Principle: Client-Only, Passive-First

This system runs exclusively as a **client device**. It has zero access to or control over any access point, router, or network infrastructure. Everything it knows comes from passively reading signals received by the laptop's own Wi-Fi adapter.

---

## Permissions Required from the User

| # | Permission | Why Needed | What Happens Without It | Risk Level |
|---|-----------|------------|------------------------|------------|
| 1 | **Wi-Fi adapter read** | Read RSSI, noise, channel from adapter | System cannot function | None — read only |
| 2 | **Network scan** | See nearby networks (OS may prompt for location) | Only sees connected network | Low — OS controls this |
| 3 | **Terminal execution** | Run OS network commands | No data collection | Low — standard tools |
| 4 | **Python execution** | Run SAC-LTC inference | Falls back to heuristic mode | Low — local only |
| 5 | **File write (~/.net-intel/)** | Store history, weights, calibration | No persistence between sessions | None — user's own directory |
| 6 | **Background execution** | Monitor and sentinel modes | On-demand scans only | Low — user starts/stops |
| 7 | **Admin/sudo** (optional) | DNS changes, DHCP renew, adapter restart | Can diagnose but not fix | Medium — modifies network settings |

### Consent Flow

On first run, the skill must:
1. List all permissions needed
2. Explain what each one does
3. Ask the user to confirm
4. Allow partial permission (e.g., read-only mode without auto-optimization)

### What Admin/Sudo Commands Do (Fully Disclosed)

| Command | OS | What It Does | Reversible? |
|---------|-----|-------------|-------------|
| `dscacheutil -flushcache` | macOS | Clears DNS cache (stale name resolutions) | Yes — cache rebuilds automatically |
| `killall -HUP mDNSResponder` | macOS | Restarts DNS resolver process | Yes — auto-restarts |
| `ipconfig set en0 DHCP` | macOS | Renews IP address lease from router | Yes — ~1-2 second reconnect |
| `networksetup -setdnsservers Wi-Fi 1.1.1.1` | macOS | Changes DNS server to Cloudflare | Yes — revert with same command |
| `networksetup -setairportnetwork en0 SSID` | macOS | Switches to a different Wi-Fi network | Yes — switch back anytime |
| `networksetup -setairportpower en0 off/on` | macOS | Turns Wi-Fi adapter off then on | Yes — ~3 second reconnect |
| `systemd-resolve --flush-caches` | Linux | Clears DNS cache | Yes — cache rebuilds |
| `dhclient -r && dhclient` | Linux | Releases and renews DHCP lease | Yes — ~2 second reconnect |
| `nmcli dev wifi connect SSID` | Linux | Switches Wi-Fi network | Yes — switch back |
| `nmcli radio wifi off/on` | Linux | Restarts Wi-Fi adapter | Yes — ~3 second reconnect |
| `Clear-DnsClientCache` | Windows | Clears DNS cache | Yes — cache rebuilds |
| `ipconfig /renew` | Windows | Renews DHCP lease | Yes — ~2 second reconnect |
| `Set-DnsClientServerAddress` | Windows | Changes DNS server | Yes — revert with same command |
| `netsh wlan connect name=SSID` | Windows | Switches Wi-Fi network | Yes — switch back |

**Every admin command is reversible.** None modify system files, registry entries, firewall rules, or any persistent system configuration beyond standard network preferences.

---

## Permissions Required from Access Points

**NONE.**

| What We Use | How We Get It | AP's Involvement |
|-------------|--------------|-----------------|
| RSSI (signal strength) | Our adapter measures it | AP broadcasts beacons — this is mandatory per 802.11 spec |
| SSID (network name) | In beacon frame | Publicly broadcast (hidden SSIDs still have beacons, just unnamed) |
| Channel / frequency | In beacon frame | Publicly broadcast |
| BSSID (MAC address) | In beacon frame header | Publicly broadcast |
| Security type | In beacon RSN/WPA IE | Publicly broadcast |
| PHY mode | In beacon HT/VHT/HE IEs | Publicly broadcast |

### What We NEVER Do

- Authenticate to any AP we're not connected to
- Send probe requests to specific APs
- Access AP management interfaces
- Modify AP settings (can only recommend router-side changes to the user)
- Deauthenticate any device
- Inject packets
- Capture payload data from beacon frames
- Perform active scanning that affects AP operation

### For Our Connected AP

We use the existing authenticated connection (the user already entered the Wi-Fi password) to run standard internet tests:
- ICMP ping (10 packets, 560 bytes total)
- DNS queries (single UDP packet each)
- HTTP download (1 MB file for speed test)

This is normal network traffic indistinguishable from regular internet use.

---

## OS-Specific Permission Details

### macOS

| Permission | How to Grant | System Prompt |
|-----------|-------------|---------------|
| Wi-Fi scan (nearby networks) | System Preferences → Privacy & Security → Location Services → Terminal | macOS Sonoma+ requires Location Services for Wi-Fi scanning |
| system_profiler access | Default allowed | No prompt needed |
| ping | Default allowed | No prompt needed |
| curl | Default allowed | No prompt needed |
| dig | Default allowed | No prompt needed |
| networksetup (read) | Default allowed | No prompt needed |
| networksetup (write) | Requires sudo | Password prompt |
| dscacheutil (flush) | Requires sudo | Password prompt |

### Linux / Ubuntu

| Permission | How to Grant | Notes |
|-----------|-------------|-------|
| nmcli (read) | Default for `netdev` group | Most Ubuntu users are in this group |
| nmcli (write) | Requires sudo or PolicyKit | May prompt for password |
| iw / iwconfig | Default allowed | Read-only operations |
| ip addr / ip route | Default allowed | Read-only |
| iwlist scan | May require root | Use `nmcli dev wifi list` as alternative |
| resolvectl | Default allowed | Read-only |
| dhclient | Requires sudo | DHCP operations |
| ping | Default allowed via setcap | No prompt needed |

### Windows

| Permission | How to Grant | Notes |
|-----------|-------------|-------|
| netsh wlan show (read) | Default for all users | No elevation needed |
| netsh wlan connect | Requires admin | UAC prompt |
| Get-NetAdapter | Default allowed | PowerShell |
| Set-DnsClientServerAddress | Requires admin | UAC prompt |
| Clear-DnsClientCache | Default in PowerShell | No elevation needed |
| ping / Test-Connection | Default allowed | No prompt |
| Resolve-DnsName | Default allowed | No prompt |
| curl.exe | Built-in on Windows 10+ | No prompt |

---

## Data Storage

### What Is Stored

| File | Location | Contents | Retention |
|------|----------|----------|-----------|
| `weights.json` | `~/.net-intel/` | SAC-LTC model weights (17K parameters as JSON) | Permanent until retrained |
| `trained_model.pt` | `~/.net-intel/` | PyTorch model checkpoint | Permanent until retrained |
| `history.jsonl` | `~/.net-intel/` | Scan history (RSSI, ping, score per cycle) | Auto-pruned to last 24 hours |
| `sentinel_baseline.json` | `~/.net-intel/` | Baseline RSSI readings for presence detection | Updated on calibration |
| `spatial_map.json` | `~/.net-intel/` | AP direction mapping (front/back/left/right) | Updated on calibration |
| `actions.log` | `~/.net-intel/` | Log of automatic optimization actions taken | Rolling, last 7 days |

### What Is NOT Stored

- No Wi-Fi passwords
- No beacon frame contents or payloads
- No personal information
- No MAC addresses of other people's devices (only APs)
- No browsing history or traffic data
- No location data (we don't use GPS)

### Data Never Leaves the Device

All processing is local. No data is transmitted to any server, cloud service, or external API. The system operates entirely offline after initial setup (pip install).

---

## Privacy and Ethics

### Wi-Fi Sensing (Presence Detection)

This feature detects human movement through RSSI fluctuations. Important disclosures:

1. **Cannot identify individuals** — only detects "something is moving", not "John is moving"
2. **Cannot see through walls precisely** — quadrant-level direction only
3. **Cannot detect stationary people** — only movement causes RSSI changes
4. **User must explicitly start sentinel mode** — never runs without consent
5. **No recordings** — only real-time variance statistics, not signal recordings
6. **False positives** — pets, fans, and moving objects trigger detection

### Ethical Use Guidelines

- Do NOT use presence detection to monitor people without their knowledge
- Do NOT use in workplaces to surveil employees
- This is a personal tool for the laptop owner's awareness of their own environment
- The presence detection feature is inherently imprecise and should not be relied upon for security purposes

### Open Source Transparency

Every line of code is open source. Every algorithm is documented. Every weight can be inspected. There are no hidden capabilities, phone-home mechanisms, or obfuscated code.
