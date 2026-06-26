# Cross-Platform Command Reference

Every OS-specific command used by the system, with exact syntax.

## OS Detection

| OS | Command | Expected Output |
|----|---------|----------------|
| macOS | `uname -s` | `Darwin` |
| Linux | `uname -s` | `Linux` |
| Windows | `$env:OS` (PowerShell) | `Windows_NT` |

## Wi-Fi Interface Discovery

**macOS:**
```bash
networksetup -listallhardwareports | grep -A 1 "Wi-Fi" | grep Device | awk '{print $2}'
# Returns: en0 (typically)
```

**Linux:**
```bash
iw dev 2>/dev/null | grep Interface | head -1 | awk '{print $2}'
# Fallback:
nmcli -t -f DEVICE,TYPE dev | grep wifi | cut -d: -f1 | head -1
# Returns: wlan0, wlp2s0, etc.
```

**Windows (PowerShell):**
```powershell
(Get-NetAdapter | Where-Object {$_.MediaType -eq "802.11"} | Select-Object -First 1).Name
# Returns: Wi-Fi (typically)
```

## Network Scanning

### Connected Network Info

**macOS:**
```bash
system_profiler SPAirPortDataType
# Returns: SSID, PHY mode, channel, signal/noise, tx rate, MCS, security
# Also lists ALL nearby networks with their channels and PHY modes
# Some nearby networks include signal/noise (typically those on nearby channels)
```

**Linux:**
```bash
# Connected network
iwconfig $WIFI_IF 2>/dev/null
# Returns: SSID, frequency, signal level, noise level, bit rate, link quality

# All visible networks
nmcli -f SSID,BSSID,SIGNAL,FREQ,CHAN,RATE,SECURITY,MODE dev wifi list
# Returns: tabulated list of all visible networks
```

**Windows (PowerShell):**
```powershell
# Connected network
netsh wlan show interfaces
# Returns: SSID, BSSID, signal (%), channel, radio type, authentication

# All visible networks
netsh wlan show networks mode=bssid
# Returns: SSID, BSSID, signal (%), channel, authentication for all visible
```

### Signal Conversion (Windows)

Windows reports signal as percentage. Approximate conversion:
```
dBm ≈ (signal_percent / 2) - 100
# 100% → -50 dBm, 80% → -60 dBm, 50% → -75 dBm, 20% → -90 dBm
```

Windows does NOT expose noise floor. Estimate -90 dBm for indoor environments.

## Performance Testing

### Latency and Packet Loss

**macOS / Linux:**
```bash
ping -c 10 -q 8.8.8.8
# Parse: "round-trip min/avg/max/stddev = X/X/X/X ms"
# Parse: "X% packet loss"
```

**Windows (PowerShell):**
```powershell
Test-Connection 8.8.8.8 -Count 10 | Measure-Object -Property Latency -Average -Maximum -Minimum
# Or:
ping -n 10 8.8.8.8
```

### DNS Speed

**macOS / Linux:**
```bash
# Current DNS
dig google.com +noall +stats 2>&1 | grep "Query time"

# Compare alternatives
dig google.com @1.1.1.1 +noall +stats 2>&1 | grep "Query time"
dig google.com @8.8.8.8 +noall +stats 2>&1 | grep "Query time"
```

**Windows (PowerShell):**
```powershell
Measure-Command { Resolve-DnsName google.com -DnsOnly } | Select TotalMilliseconds
Measure-Command { Resolve-DnsName google.com -Server 1.1.1.1 -DnsOnly } | Select TotalMilliseconds
```

### Throughput (Download Speed)

**macOS / Linux:**
```bash
curl -o /dev/null -w '{"speed_bytes_sec": %{speed_download}, "time_sec": %{time_total}}' \
  -s --max-time 15 http://speedtest.tele2.net/1MB.zip
# Returns JSON with download speed in bytes/sec
# Convert: Mbps = speed_bytes_sec * 8 / 1000000
```

**Windows (PowerShell):**
```powershell
# curl.exe is built-in on Windows 10+
curl.exe -o NUL -w "%{speed_download}" -s --max-time 15 http://speedtest.tele2.net/1MB.zip
```

## Network Configuration

### DNS Servers

**macOS:**
```bash
# Read
networksetup -getdnsservers Wi-Fi

# Write (requires sudo)
sudo networksetup -setdnsservers Wi-Fi 1.1.1.1 1.0.0.1

# Reset to DHCP default
sudo networksetup -setdnsservers Wi-Fi empty
```

**Linux:**
```bash
# Read
resolvectl status 2>/dev/null || cat /etc/resolv.conf

# Write
sudo resolvectl dns $WIFI_IF 1.1.1.1 1.0.0.1
```

**Windows (PowerShell):**
```powershell
# Read
Get-DnsClientServerAddress -InterfaceAlias "Wi-Fi"

# Write (requires admin)
Set-DnsClientServerAddress -InterfaceAlias "Wi-Fi" -ServerAddresses 1.1.1.1,1.0.0.1

# Reset to DHCP default
Set-DnsClientServerAddress -InterfaceAlias "Wi-Fi" -ResetServerAddresses
```

### DNS Cache Flush

**macOS:**
```bash
sudo dscacheutil -flushcache && sudo killall -HUP mDNSResponder
```

**Linux:**
```bash
sudo systemd-resolve --flush-caches 2>/dev/null || sudo resolvectl flush-caches
```

**Windows (PowerShell):**
```powershell
Clear-DnsClientCache
```

### DHCP Lease Renewal

**macOS:**
```bash
sudo ipconfig set $WIFI_IF DHCP
```

**Linux:**
```bash
sudo dhclient -r $WIFI_IF && sudo dhclient $WIFI_IF
# Or with NetworkManager:
sudo nmcli connection down $CONNECTION && sudo nmcli connection up $CONNECTION
```

**Windows (PowerShell):**
```powershell
ipconfig /release "Wi-Fi"
ipconfig /renew "Wi-Fi"
```

### Network Switching

**macOS:**
```bash
networksetup -setairportnetwork $WIFI_IF "TargetSSID" "password"
# Note: password only needed for first connection to a new network
```

**Linux:**
```bash
nmcli dev wifi connect "TargetSSID" password "password"
# For saved networks:
nmcli dev wifi connect "TargetSSID"
```

**Windows (PowerShell):**
```powershell
netsh wlan connect name="TargetSSID"
# Must have a saved profile. To create one first:
netsh wlan add profile filename="profile.xml"
```

### Adapter Restart

**macOS:**
```bash
networksetup -setairportpower $WIFI_IF off
sleep 2
networksetup -setairportpower $WIFI_IF on
```

**Linux:**
```bash
sudo nmcli radio wifi off
sleep 2
sudo nmcli radio wifi on
```

**Windows (PowerShell):**
```powershell
Disable-NetAdapter -Name "Wi-Fi" -Confirm:$false
Start-Sleep 2
Enable-NetAdapter -Name "Wi-Fi" -Confirm:$false
```

## Hotspot Detection

### By IP Subnet

```
172.20.10.x/28  → iPhone hotspot (Apple)
192.168.43.x    → Android hotspot (older)
192.168.49.x    → Android hotspot (newer)
Other           → Infrastructure router
```

### By SSID Pattern

```
Keywords: iPhone, Android, Galaxy, Pixel, Hotspot, Mobile,
          Moto, OnePlus, Samsung, Xiaomi, Huawei, OPPO,
          Redmi, Vivo, Realme
```

## Proxy Detection

**macOS:**
```bash
networksetup -getwebproxy Wi-Fi
networksetup -getsecurewebproxy Wi-Fi
```

**Linux:**
```bash
env | grep -i proxy
```

**Windows (PowerShell):**
```powershell
Get-ItemProperty 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Internet Settings' |
  Select ProxyEnable, ProxyServer
```

## Routing Table

**macOS:**
```bash
netstat -rn -f inet | head -20
```

**Linux:**
```bash
ip route show
```

**Windows (PowerShell):**
```powershell
Get-NetRoute -DestinationPrefix 0.0.0.0/0
```
