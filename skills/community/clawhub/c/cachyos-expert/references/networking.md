# Netzwerk, Firewall & Connectivity — CachyOS

## Inhaltsverzeichnis
1. NetworkManager
2. iwd (WiFi)
3. systemd-networkd
4. Firewall (firewalld, nftables, iptables)
5. DNS-Konfiguration
6. VPN (WireGuard, OpenVPN, Tailscale)
7. Bluetooth
8. Netzwerk-Diagnose
9. Bridge / VLAN / Bonding

---

## 1. NetworkManager (CachyOS Default)

```bash
# Status
systemctl status NetworkManager
nmcli general status
nmcli device status

# Verbindungen auflisten
nmcli connection show
nmcli connection show --active

# WiFi
nmcli device wifi list
nmcli device wifi connect "<SSID>" password "<pass>"
nmcli device wifi connect "<SSID>" password "<pass>" hidden yes

# Statische IP
nmcli connection modify "<conn>" ipv4.method manual \
  ipv4.addresses "192.168.1.100/24" \
  ipv4.gateway "192.168.1.1" \
  ipv4.dns "1.1.1.1,9.9.9.9"
nmcli connection up "<conn>"

# DHCP zurück
nmcli connection modify "<conn>" ipv4.method auto
nmcli connection up "<conn>"

# DNS manuell setzen (trotz DHCP)
nmcli connection modify "<conn>" ipv4.dns "1.1.1.1 9.9.9.9"
nmcli connection modify "<conn>" ipv4.ignore-auto-dns yes

# Hotspot erstellen
nmcli device wifi hotspot ifname wlan0 ssid "MeinHotspot" password "sicheres-pw"

# Verbindung löschen
nmcli connection delete "<conn>"

# MAC-Randomisierung
# /etc/NetworkManager/conf.d/mac-random.conf
[device]
wifi.scan-rand-mac-address=yes
[connection]
wifi.cloned-mac-address=random
ethernet.cloned-mac-address=random
```

---

## 2. iwd (WiFi-Backend)

```bash
# CachyOS nutzt optional iwd als WiFi-Backend für NM
sudo pacman -S iwd

# Standalone nutzen
sudo systemctl enable --now iwd.service

# Interaktive Shell
iwctl
[iwd]# station wlan0 scan
[iwd]# station wlan0 get-networks
[iwd]# station wlan0 connect "<SSID>"
[iwd]# station wlan0 show

# iwd als Backend für NetworkManager
# /etc/NetworkManager/conf.d/wifi-backend.conf
[device]
wifi.backend=iwd

sudo systemctl restart NetworkManager
```

---

## 3. systemd-networkd (Server/Minimal)

```bash
# Aktivieren (deaktiviert NetworkManager!)
sudo systemctl disable --now NetworkManager
sudo systemctl enable --now systemd-networkd systemd-resolved

# /etc/systemd/network/20-wired.network
[Match]
Name=enp*

[Network]
DHCP=yes
DNS=1.1.1.1
DNS=9.9.9.9

# Statisch:
# [Network]
# Address=192.168.1.100/24
# Gateway=192.168.1.1
# DNS=1.1.1.1

# Status
networkctl status
networkctl list
resolvectl status
```

---

## 4. Firewall

### firewalld (CachyOS Default)

```bash
sudo pacman -S firewalld
sudo systemctl enable --now firewalld

# Status
sudo firewall-cmd --state
sudo firewall-cmd --list-all

# Zone anzeigen
sudo firewall-cmd --get-active-zones
sudo firewall-cmd --get-default-zone

# Port öffnen
sudo firewall-cmd --add-port=8080/tcp --permanent
sudo firewall-cmd --add-service=ssh --permanent
sudo firewall-cmd --reload

# Port schließen
sudo firewall-cmd --remove-port=8080/tcp --permanent
sudo firewall-cmd --reload

# Alle Services auflisten
sudo firewall-cmd --get-services

# Rich Rules
sudo firewall-cmd --add-rich-rule='rule family="ipv4" source address="192.168.1.0/24" service name="ssh" accept' --permanent

# Interface einer Zone zuweisen
sudo firewall-cmd --zone=trusted --change-interface=tailscale0 --permanent
```

### nftables (Low-Level)

```bash
sudo pacman -S nftables

# Aktive Regeln
sudo nft list ruleset

# Basis-Config: /etc/nftables.conf
table inet filter {
  chain input {
    type filter hook input priority 0; policy drop;
    ct state established,related accept
    iif "lo" accept
    tcp dport 22 accept
    icmp type echo-request accept
    counter drop
  }
  chain forward {
    type filter hook forward priority 0; policy drop;
  }
  chain output {
    type filter hook output priority 0; policy accept;
  }
}

sudo systemctl enable --now nftables
sudo nft -f /etc/nftables.conf
```

---

## 5. DNS-Konfiguration

```bash
# systemd-resolved (empfohlen)
sudo systemctl enable --now systemd-resolved
sudo ln -sf /run/systemd/resolve/stub-resolv.conf /etc/resolv.conf

# DNS prüfen
resolvectl status
resolvectl query archlinux.org

# DNS-over-TLS aktivieren
# /etc/systemd/resolved.conf
[Resolve]
DNS=1.1.1.1#cloudflare-dns.com 9.9.9.9#dns.quad9.net
FallbackDNS=8.8.8.8
DNSOverTLS=yes
DNSSEC=allow-downgrade

sudo systemctl restart systemd-resolved

# DNS-Cache leeren
resolvectl flush-caches
resolvectl statistics

# /etc/hosts für lokale Einträge
127.0.0.1  localhost
::1        localhost
192.168.1.100  meinserver.local
```

---

## 6. VPN

### WireGuard

```bash
sudo pacman -S wireguard-tools

# Schlüssel generieren
wg genkey | tee privatekey | wg pubkey > publickey

# Config: /etc/wireguard/wg0.conf
[Interface]
PrivateKey = <private-key>
Address = 10.0.0.2/24
DNS = 1.1.1.1

[Peer]
PublicKey = <server-public-key>
Endpoint = vpn.example.com:51820
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 25

# Starten
sudo wg-quick up wg0
sudo systemctl enable --now wg-quick@wg0

# Status
sudo wg show
```

### Tailscale

```bash
sudo pacman -S tailscale
sudo systemctl enable --now tailscaled

# Anmelden
sudo tailscale up

# Status
tailscale status
tailscale ip

# Exit-Node nutzen
sudo tailscale up --exit-node=<node-ip>

# Als Exit-Node fungieren
sudo tailscale up --advertise-exit-node
# + ip-forwarding:
echo 'net.ipv4.ip_forward=1' | sudo tee /etc/sysctl.d/99-tailscale.conf
echo 'net.ipv6.conf.all.forwarding=1' | sudo tee -a /etc/sysctl.d/99-tailscale.conf
sudo sysctl --system

# Subnetz advertisen
sudo tailscale up --advertise-routes=192.168.1.0/24
```

### OpenVPN

```bash
sudo pacman -S openvpn
sudo openvpn --config /etc/openvpn/client/myvpn.conf
sudo systemctl enable --now openvpn-client@myvpn
```

---

## 7. Bluetooth

```bash
sudo pacman -S bluez bluez-utils
sudo systemctl enable --now bluetooth.service

# Interaktiv
bluetoothctl
[bluetooth]# power on
[bluetooth]# agent on
[bluetooth]# default-agent
[bluetooth]# scan on
# Warten bis Gerät erscheint...
[bluetooth]# pair <MAC>
[bluetooth]# connect <MAC>
[bluetooth]# trust <MAC>

# Auto-Connect aktivieren
# /etc/bluetooth/main.conf
[General]
AutoEnable=true
FastConnectable=true

[Policy]
AutoEnable=true

# Bluetooth-Audio: PipeWire übernimmt automatisch (siehe desktop-and-audio.md)

# Troubleshooting
sudo dmesg | grep -i bluetooth
journalctl -u bluetooth.service -b
rfkill list
rfkill unblock bluetooth
```

---

## 8. Netzwerk-Diagnose

```bash
# Verbindungstest
ping -c 4 archlinux.org
ping -c 4 1.1.1.1          # DNS-unabhängig

# DNS testen
dig archlinux.org
nslookup archlinux.org
host archlinux.org

# Routen
ip route show
traceroute archlinux.org
mtr archlinux.org           # Kombiniert ping + traceroute

# Interfaces
ip addr show
ip link show

# Offene Ports
ss -tulnp
sudo ss -tulnp              # mit PID

# Bandbreite messen
sudo pacman -S iperf3
iperf3 -s                   # Server
iperf3 -c <server-ip>       # Client

# Pakete mitschneiden
sudo tcpdump -i enp0s3 -n port 80
sudo pacman -S wireshark-qt  # GUI

# ARP-Tabelle
ip neigh show

# Netzwerk-Interfaces neu starten
sudo nmcli networking off && sudo nmcli networking on
```

---

## 9. Bridge / VLAN / Bonding

```bash
# Bridge (für VMs)
sudo nmcli connection add type bridge ifname br0
sudo nmcli connection add type bridge-slave ifname enp0s3 master br0
sudo nmcli connection up br0

# VLAN
sudo nmcli connection add type vlan ifname vlan100 dev enp0s3 id 100

# Bonding (Link-Aggregation)
sudo nmcli connection add type bond ifname bond0 bond.options "mode=802.3ad,miimon=100"
sudo nmcli connection add type ethernet slave-type bond master bond0 ifname enp0s3
sudo nmcli connection add type ethernet slave-type bond master bond0 ifname enp0s4
```
