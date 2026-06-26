# Systemd, Journald & Diagnose — CachyOS

## Inhaltsverzeichnis
1. Systemd-Grundlagen
2. Service-Management
3. Eigene Units & Timer
4. Journald & Logging
5. Boot-Analyse
6. Systemd-Netzwerk (resolved, timesyncd)
7. Tmpfiles & Sysusers
8. Diagnose-Befehlsreferenz
9. Hardware-Info
10. Monitoring-Tools

---

## 1. Systemd-Grundlagen

```bash
# System-Status
systemctl status
systemctl is-system-running    # running, degraded, maintenance

# Fehlgeschlagene Units
systemctl --failed
systemctl reset-failed         # Failed-Status zurücksetzen

# Alle Units eines Typs
systemctl list-units --type=service
systemctl list-units --type=timer
systemctl list-units --type=mount
systemctl list-units --type=target

# Unit-Dateien (installierte)
systemctl list-unit-files
systemctl list-unit-files --state=enabled

# Default-Target
systemctl get-default
sudo systemctl set-default graphical.target    # Desktop
sudo systemctl set-default multi-user.target   # Server/TTY

# Targets
systemctl isolate multi-user.target    # Wechsel ohne Reboot
systemctl isolate rescue.target        # Rescue-Modus
systemctl isolate emergency.target     # Emergency
```

---

## 2. Service-Management

```bash
# Starten/Stoppen
sudo systemctl start <service>
sudo systemctl stop <service>
sudo systemctl restart <service>
sudo systemctl reload <service>         # Config neu laden (wenn unterstützt)
sudo systemctl reload-or-restart <service>

# Aktivieren/Deaktivieren (Autostart)
sudo systemctl enable <service>
sudo systemctl disable <service>
sudo systemctl enable --now <service>   # Enable + Start

# Maskieren (komplett blockieren)
sudo systemctl mask <service>
sudo systemctl unmask <service>

# Status & Details
systemctl status <service>
systemctl show <service>                # Alle Properties
systemctl cat <service>                 # Unit-Datei anzeigen
systemctl show -p MainPID <service>
systemctl show -p MemoryCurrent <service>

# Dependencies
systemctl list-dependencies <service>
systemctl list-dependencies --reverse <service>   # Wer braucht mich?

# Daemon Reload (nach Unit-Datei-Änderung)
sudo systemctl daemon-reload

# User-Services (ohne root)
systemctl --user start <service>
systemctl --user enable <service>
systemctl --user status <service>
loginctl enable-linger $(whoami)        # User-Services ohne Login
```

---

## 3. Eigene Units & Timer

### Service-Unit

```ini
# /etc/systemd/system/mein-backup.service
[Unit]
Description=Mein Backup-Skript
After=network-online.target
Wants=network-online.target

[Service]
Type=oneshot
ExecStart=/usr/local/bin/backup.sh
User=root
Nice=19
IOSchedulingClass=idle

# Ressourcen-Limits
MemoryMax=2G
CPUQuota=50%

# Sicherheit
ProtectSystem=strict
ProtectHome=read-only
PrivateTmp=true
NoNewPrivileges=true

[Install]
WantedBy=multi-user.target
```

### Timer-Unit (Ersatz für Cron)

```ini
# /etc/systemd/system/mein-backup.timer
[Unit]
Description=Backup Timer

[Timer]
OnCalendar=*-*-* 02:00:00       # Täglich um 02:00
# OnCalendar=Mon *-*-* 03:00:00 # Montags 03:00
# OnCalendar=hourly              # Stündlich
# OnBootSec=5min                 # 5min nach Boot
# OnUnitActiveSec=1h             # Alle Stunde nach letztem Lauf
Persistent=true                  # Verpasste Läufe nachholen
RandomizedDelaySec=300           # Bis zu 5min zufällige Verzögerung

[Install]
WantedBy=timers.target
```

```bash
# Aktivieren
sudo systemctl daemon-reload
sudo systemctl enable --now mein-backup.timer

# Timer auflisten
systemctl list-timers --all

# Timer manuell triggern
sudo systemctl start mein-backup.service

# Nächsten Lauf prüfen
systemctl status mein-backup.timer
```

### Path-Unit (Datei-Trigger)

```ini
# /etc/systemd/system/mein-watcher.path
[Unit]
Description=Überwache Verzeichnis

[Path]
PathModified=/var/data/incoming
Unit=mein-processor.service

[Install]
WantedBy=multi-user.target
```

---

## 4. Journald & Logging

```bash
# Logs des aktuellen Boots
journalctl -b
journalctl -b -p err           # Nur Fehler
journalctl -b -p warning       # Warnungen+

# Vorheriger Boot
journalctl -b -1
journalctl --list-boots         # Alle Boots

# Nach Unit filtern
journalctl -u NetworkManager
journalctl -u docker.service -f    # Follow (live)

# User-Services
journalctl --user -u pipewire

# Zeitraum
journalctl --since "2025-01-01 10:00" --until "2025-01-01 12:00"
journalctl --since "1 hour ago"
journalctl --since today

# Nach PID/UID
journalctl _PID=1234
journalctl _UID=1000

# Kernel-Logs
journalctl -k
journalctl -k -p err

# Ausgabe-Formate
journalctl -o short-precise     # Timestamps
journalctl -o json-pretty       # JSON
journalctl -o verbose           # Alle Felder

# Speicherplatz
journalctl --disk-usage

# Logs rotieren/bereinigen
sudo journalctl --vacuum-time=2weeks
sudo journalctl --vacuum-size=500M

# Persistente Logs aktivieren
sudo mkdir -p /var/log/journal
sudo systemd-tmpfiles --create --prefix /var/log/journal

# Config: /etc/systemd/journald.conf
[Journal]
Storage=persistent
SystemMaxUse=1G
SystemMaxFileSize=100M
MaxRetentionSec=1month
Compress=yes
```

---

## 5. Boot-Analyse

```bash
# Boot-Zeit
systemd-analyze

# Langsame Services identifizieren
systemd-analyze blame

# Kritischer Pfad
systemd-analyze critical-chain

# SVG-Grafik des Boot-Prozesses
systemd-analyze plot > boot.svg
xdg-open boot.svg

# Einzelne Unit analysieren
systemd-analyze verify <unit>
systemd-analyze security <service>   # Sicherheits-Score
```

---

## 6. Systemd-Netzwerk (resolved, timesyncd)

```bash
# DNS (systemd-resolved)
resolvectl status
resolvectl query archlinux.org
resolvectl flush-caches
resolvectl statistics

# NTP (systemd-timesyncd)
timedatectl status
timedatectl timesync-status
# Config: /etc/systemd/timesyncd.conf
[Time]
NTP=0.de.pool.ntp.org 1.de.pool.ntp.org
FallbackNTP=0.pool.ntp.org
```

---

## 7. Tmpfiles & Sysusers

```bash
# Temporäre Dateien/Verzeichnisse verwalten
# /etc/tmpfiles.d/mein-app.conf
d /var/lib/mein-app 0755 myuser mygroup -
f /var/log/mein-app.log 0644 myuser mygroup -
L /etc/mein-app/config.yml - - - - /opt/mein-app/default-config.yml

# Anwenden
sudo systemd-tmpfiles --create

# System-User erstellen
# /etc/sysusers.d/mein-app.conf
u mein-app - "Mein App Service User"
sudo systemd-sysusers
```

---

## 8. Diagnose-Befehlsreferenz

### Logs & Fehler

```bash
journalctl -b -p err                    # Boot-Fehler
journalctl -b -p warning                # + Warnungen
dmesg --level=err,warn                   # Kernel-Fehler
dmesg -T                                 # Mit Zeitstempel
systemctl --failed                       # Fehlgeschlagene Services
coredumpctl list                         # Core-Dumps
coredumpctl info <PID>                   # Core-Dump Details
```

### Prozesse & Ressourcen

```bash
ps aux --sort=-%mem | head -20           # Top RAM
ps aux --sort=-%cpu | head -20           # Top CPU
pidof <prozessname>
pgrep -la <pattern>
kill -TERM <PID>
kill -9 <PID>                            # Force Kill
pkill -f <pattern>

# Offene Dateien
lsof -p <PID>
lsof -i :8080                           # Wer nutzt Port 8080?
fuser -v /dev/sda1                       # Wer nutzt Partition?

# File-Descriptors
ls -la /proc/<PID>/fd/ | wc -l
cat /proc/sys/fs/file-nr                 # System-weit
```

### Speicher & Disk

```bash
free -h                                  # RAM
df -hT                                   # Disk (mit Filesystem-Typ)
du -sh /var/* | sort -rh | head -20      # Größte Verzeichnisse
ncdu /                                   # Interaktiv
lsblk -f                                 # Block-Devices mit FS + UUID
findmnt                                  # Mount-Baum
mount | column -t                        # Mounts
cat /proc/mounts                         # Kernel-Sicht

# Inode-Nutzung
df -ih

# Gelöschte aber offene Dateien (Speicher nicht freigegeben)
sudo lsof +L1
```

### Kernel & Module

```bash
uname -a                                 # Kernel-Version
uname -r                                 # Nur Version
cat /proc/version
lsmod                                    # Geladene Module
modinfo <modul>                          # Modul-Info
cat /proc/cmdline                        # Kernel-Cmdline
zcat /proc/config.gz | grep <CONFIG>     # Kernel-Config
sysctl -a                                # Alle sysctl-Werte
```

---

## 9. Hardware-Info

```bash
# Übersicht
inxi -Fxz                               # Komplett (installieren: sudo pacman -S inxi)
hostnamectl                              # Hostname + OS

# CPU
lscpu
cat /proc/cpuinfo | head -30
cpupower frequency-info

# RAM
free -h
sudo dmidecode -t memory
cat /proc/meminfo

# PCI-Geräte (GPU, NIC, etc.)
lspci -v
lspci -k                                # Mit Kernel-Treiber
lspci -nn | grep -i vga

# USB
lsusb
lsusb -t                                # Baum

# Disk
lsblk -o NAME,SIZE,FSTYPE,MOUNTPOINT,UUID,MODEL
sudo smartctl -a /dev/nvme0n1
sudo hdparm -I /dev/sda

# Sensoren (Temperatur)
sudo pacman -S lm_sensors
sudo sensors-detect                      # Einmalig
sensors

# BIOS/UEFI
sudo dmidecode -t bios
sudo dmidecode -t system
sudo efibootmgr -v                      # EFI-Einträge

# ACPI
acpi -V                                  # Battery, Thermal
```

---

## 10. Monitoring-Tools

```bash
# TUI-Monitore
btop                      # Alles-in-einem (CPU, RAM, Disk, Net, Procs)
htop                      # Prozess-Monitor (klassisch)
sudo nvtop                # GPU-Monitor (NVIDIA + AMD)
sudo intel_gpu_top        # Intel GPU
iotop -oP                 # I/O pro Prozess
nethogs                   # Netzwerk pro Prozess
iftop                     # Netzwerk pro Verbindung
sudo powertop             # Power-Verbrauch (Laptop)

# Installieren
sudo pacman -S btop htop nvtop iotop nethogs iftop powertop

# Echtzeit-Kernel-Stats
vmstat 1                  # VM-Statistiken (1s Intervall)
iostat -xz 1              # I/O-Statistiken
mpstat -P ALL 1           # CPU pro Core
sar -n DEV 1              # Netzwerk
# (sysstat-Paket: sudo pacman -S sysstat)

# Systemd-Ressourcen
systemd-cgtop             # Cgroup-basierte Top-Ansicht
```
