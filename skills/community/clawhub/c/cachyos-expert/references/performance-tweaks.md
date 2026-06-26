# Performance Tweaks Reference — CachyOS

## Inhaltsverzeichnis
1. CPU-Scheduling (sched-ext, BORE, EEVDF)
2. RAM-Management (ZRAM, Zswap, Swappiness)
3. Filesystem-Optimierung (BTRFS, XFS, ext4, tmpfs)
4. sysctl-Tuning
5. GPU-Treiber (NVIDIA, AMD, Intel)
6. udev-Rules & I/O-Scheduler
7. Power-Management (TLP, auto-cpufreq)
8. SSD/NVMe-Health & TRIM
9. CPU-Frequency & Governors
10. Kernel-Parameter für Performance
11. Monitoring & Benchmarking

---

## 1. CPU-Scheduling: sched-ext / scx

CachyOS unterstützt sched-ext (pluggable Scheduler im Userspace) ab Kernel 6.12+.

### Verfügbare Scheduler

| Scheduler | Einsatz | Stärke |
|-----------|---------|--------|
| scx_rusty | Allgemein, Multi-Core | Gute Balance Throughput/Latenz |
| scx_lavd | Gaming, Latenz-sensitiv | Minimale Latenz |
| scx_bpfland | Desktop-Responsiveness | Interaktive Workloads |
| scx_flash | Server, Throughput | Maximaler Durchsatz |
| scx_wd40 | Experimentell | Latenz-optimiert für Mixed Workloads |

```bash
# Installieren
sudo pacman -S scx-scheds

# Temporär testen
sudo scx_rusty
sudo scx_lavd         # Ctrl+C zum Stoppen

# Permanent via systemd
sudo systemctl enable --now scx.service

# Scheduler konfigurieren
sudo nano /etc/default/scx
# SCX_SCHEDULER=scx_lavd
# SCX_FLAGS=""

# Status prüfen
systemctl status scx.service
cat /sys/kernel/sched_ext/root/ops  # Aktiver Scheduler
```

### BORE / EEVDF (Kernel-integriert)

- `linux-cachyos` → BORE (Burst-Oriented Response Enhancer) — Desktop/Gaming
- `linux-cachyos-eevdf` → EEVDF (Earliest Eligible Virtual Deadline First) — Fairness

```bash
# Kernel-Wechsel
sudo pacman -S linux-cachyos linux-cachyos-headers
# oder
sudo pacman -S linux-cachyos-eevdf linux-cachyos-eevdf-headers

# Bootloader-Einträge aktualisieren
sudo reinstall-kernels  # CachyOS-spezifisch
# oder manuell:
sudo mkinitcpio -P
```

---

## 2. RAM-Management

### ZRAM (CachyOS Standard)

```bash
# Status
zramctl
cat /proc/swaps
swapon --show

# Config: /etc/systemd/zram-generator.conf
[zram0]
zram-size = ram / 2
compression-algorithm = zstd
swap-priority = 100
fs-type = swap

# Neustart nach Änderung oder:
sudo systemctl restart systemd-zram-setup@zram0.service

# Statistiken
cat /sys/block/zram0/mm_stat
# orig_data_size  compr_data_size  mem_used  mem_limit  max_used  same_pages  pages_compacted
```

### Swappiness & Memory Pressure

```bash
# CachyOS-Default für ZRAM: 180 (höher = aggressiveres Swappen in ZRAM)
cat /proc/sys/vm/swappiness

# Anpassen (persistent)
echo 'vm.swappiness=180' | sudo tee /etc/sysctl.d/99-swappiness.conf
sudo sysctl --system

# Watermark-Tuning
echo 'vm.watermark_scale_factor=125' | sudo tee -a /etc/sysctl.d/99-swappiness.conf
echo 'vm.watermark_boost_factor=0' | sudo tee -a /etc/sysctl.d/99-swappiness.conf

# Memory-Pressure prüfen
cat /proc/pressure/memory
# some avg10=0.00 avg60=0.00 avg300=0.00 total=0
# full avg10=0.00 avg60=0.00 avg300=0.00 total=0
```

### Hugepages (für Gaming/VMs)

```bash
# Transparente Hugepages (Standard bei CachyOS: madvise)
cat /sys/kernel/mm/transparent_hugepage/enabled
# [always] madvise [never]

# Für Gaming empfohlen: madvise
echo madvise | sudo tee /sys/kernel/mm/transparent_hugepage/enabled

# Statische Hugepages für VMs
echo 'vm.nr_hugepages=1024' | sudo tee /etc/sysctl.d/99-hugepages.conf
# 1024 * 2MB = 2GB reserviert
```

---

## 3. Filesystem-Optimierung

### BTRFS (CachyOS Default)

Empfohlene Mount-Optionen in `/etc/fstab`:

```
UUID=xxx  /  btrfs  noatime,compress=zstd:3,space_cache=v2,discard=async,autodefrag,subvol=@  0 0
```

| Option | Zweck |
|--------|-------|
| noatime | Keine Access-Time-Updates → weniger Writes |
| compress=zstd:3 | Transparente Kompression (1=schnell, 3=balanced, 6=max) |
| space_cache=v2 | Schnelleres Mounting, bessere Performance |
| discard=async | Asynchrones TRIM für SSDs |
| autodefrag | Auto-Defrag kleiner random Writes |
| commit=120 | Flush-Intervall erhöhen (default 30s, riskanter aber schneller) |

```bash
# Kompressionsstatistiken
sudo compsize /

# Defrag manuell
sudo btrfs filesystem defragment -r -czstd /

# Scrub (Integritätsprüfung)
sudo btrfs scrub start /
sudo btrfs scrub status /

# Balance (freien Platz optimieren)
sudo btrfs balance start -dusage=50 -musage=50 /
sudo btrfs balance status /

# Filesystem-Nutzung
btrfs filesystem usage /
btrfs filesystem df /

# Subvolumes auflisten
sudo btrfs subvolume list /

# Quota (falls aktiviert — kann Performance kosten!)
sudo btrfs quota disable /
```

### XFS

```bash
# Mount-Optionen
UUID=xxx  /data  xfs  noatime,logbufs=8,logbsize=256k,allocsize=64m  0 0

# Defrag
sudo xfs_fsr /dev/sdX

# Info
xfs_info /dev/sdX
```

### ext4

```bash
# Mount-Optionen
UUID=xxx  /data  ext4  noatime,commit=60,barrier=0,data=writeback  0 0
# ACHTUNG: barrier=0 und data=writeback nur mit UPS/Battery

# Tuning
sudo tune2fs -o journal_data_writeback /dev/sdX
```

### tmpfs für Build-Verzeichnisse

```bash
# /etc/fstab — AUR-Builds im RAM
tmpfs  /tmp  tmpfs  defaults,noatime,size=8G,mode=1777  0 0

# makepkg in tmpfs bauen
# /etc/makepkg.conf
BUILDDIR=/tmp/makepkg
```

---

## 4. sysctl-Tuning

Datei: `/etc/sysctl.d/99-cachyos-tweaks.conf`

```ini
# === Virtual Memory ===
vm.dirty_ratio = 10
vm.dirty_background_ratio = 5
vm.dirty_writeback_centisecs = 1500
vm.dirty_expire_centisecs = 3000
vm.vfs_cache_pressure = 50
vm.page-cluster = 0
vm.compaction_proactiveness = 0
vm.min_free_kbytes = 65536

# === ZRAM-optimiert ===
vm.swappiness = 180
vm.watermark_boost_factor = 0
vm.watermark_scale_factor = 125

# === Netzwerk ===
net.core.netdev_max_backlog = 16384
net.core.somaxconn = 8192
net.core.default_qdisc = cake
net.ipv4.tcp_congestion_control = bbr2
net.ipv4.tcp_fastopen = 3
net.ipv4.tcp_mtu_probing = 1
net.ipv4.tcp_syncookies = 1
net.ipv4.tcp_tw_reuse = 1
net.ipv4.tcp_fin_timeout = 15
net.ipv4.tcp_keepalive_time = 300
net.ipv4.tcp_keepalive_intvl = 30
net.ipv4.tcp_keepalive_probes = 5
net.ipv4.conf.all.rp_filter = 1

# === IPv6 (falls nicht benötigt) ===
# net.ipv6.conf.all.disable_ipv6 = 1

# === Inotify (IDEs, große Projekte) ===
fs.inotify.max_user_watches = 524288
fs.inotify.max_user_instances = 1024
fs.file-max = 2097152

# === Kernel Hardening ===
kernel.kptr_restrict = 2
kernel.dmesg_restrict = 1
kernel.printk = 3 3 3 3
kernel.unprivileged_bpf_disabled = 1
kernel.sysrq = 1
# SysRq aktiviert für Notfall-Recovery (Alt+SysRq+REISUB)

# === Shared Memory (für große Apps/DBs) ===
kernel.shmmax = 4294967296
kernel.shmall = 1048576
```

```bash
# Anwenden
sudo sysctl --system

# Einzelnen Wert prüfen
sysctl vm.swappiness
sysctl net.ipv4.tcp_congestion_control

# BBR2 prüfen (CachyOS Kernel hat es)
lsmod | grep bbr
```

---

## 5. GPU-Treiber

### NVIDIA

```bash
# === CachyOS-optimiert (DKMS) ===
sudo pacman -S nvidia-dkms nvidia-utils lib32-nvidia-utils nvidia-settings opencl-nvidia

# === Open-Source-Kernel-Module (ab RTX 2000+) ===
sudo pacman -S nvidia-open-dkms nvidia-utils lib32-nvidia-utils

# === Wayland-Support (zwingend!) ===
# Kernel-Parameter hinzufügen:
#   nvidia_drm.modeset=1 nvidia_drm.fbdev=1

# systemd-boot: /boot/loader/entries/linux-cachyos.conf
# GRUB: /etc/default/grub → GRUB_CMDLINE_LINUX_DEFAULT

# mkinitcpio: MODULES und Early-KMS
# /etc/mkinitcpio.conf
MODULES=(nvidia nvidia_modeset nvidia_uvm nvidia_drm)
sudo mkinitcpio -P

# === NVIDIA Powermanagement (Suspend/Resume) ===
sudo systemctl enable nvidia-suspend.service
sudo systemctl enable nvidia-resume.service
sudo systemctl enable nvidia-hibernate.service

# === Persistenced (verhindert Driver-Unload) ===
sudo systemctl enable nvidia-persistenced.service

# === Overclocking (optional) ===
sudo nvidia-settings  # GUI
# oder CLI:
nvidia-smi -pm 1                          # Persistence Mode
nvidia-smi -pl 250                        # Power Limit in Watt
nvidia-smi --lock-gpu-clocks=1500,1900    # Clock-Range

# === Diagnose ===
nvidia-smi                    # Übersicht
nvidia-smi -q                 # Detailliert
nvidia-smi dmon               # Monitoring
cat /sys/module/nvidia_drm/parameters/modeset  # Sollte Y sein
cat /sys/module/nvidia_drm/parameters/fbdev     # Sollte Y sein
glxinfo | grep "OpenGL renderer"
vulkaninfo --summary
```

### AMD

```bash
# === Mesa + Vulkan ===
sudo pacman -S mesa lib32-mesa vulkan-radeon lib32-vulkan-radeon
sudo pacman -S libva-mesa-driver lib32-libva-mesa-driver  # VA-API Hardware-Decode
sudo pacman -S mesa-vdpau lib32-mesa-vdpau                # VDPAU

# === AMDGPU-Übertaktung ===
# Performance-Level
echo high | sudo tee /sys/class/drm/card1/device/power_dpm_force_performance_level

# GPU-Takt anzeigen
cat /sys/class/drm/card1/device/pp_dpm_sclk
cat /sys/class/drm/card1/device/pp_dpm_mclk

# OverDrive aktivieren (Kernel-Parameter: amdgpu.ppfeaturemask=0xffffffff)
sudo pacman -S corectrl  # GUI für AMD OC

# === Diagnose ===
glxinfo | grep "OpenGL renderer"
vulkaninfo --summary
sensors | grep amdgpu      # Temperaturen
sudo cat /sys/kernel/debug/dri/1/amdgpu_pm_info
```

### Intel (iGPU)

```bash
sudo pacman -S mesa lib32-mesa intel-media-driver vulkan-intel lib32-vulkan-intel
# intel-media-driver = iHD (empfohlen ab Broadwell)
# libva-intel-driver = i965 (älter)

# HW-Decode testen
vainfo
```

---

## 6. udev-Rules & I/O-Scheduler

```bash
# /etc/udev/rules.d/60-ioschedulers.rules
# NVMe: none (direkt, kein Scheduler nötig)
ACTION=="add|change", KERNEL=="nvme[0-9]*", ATTR{queue/scheduler}="none"
# SATA SSD: mq-deadline
ACTION=="add|change", KERNEL=="sd[a-z]", ATTR{queue/rotational}=="0", ATTR{queue/scheduler}="mq-deadline"
# HDD: bfq
ACTION=="add|change", KERNEL=="sd[a-z]", ATTR{queue/rotational}=="1", ATTR{queue/scheduler}="bfq"
# eMMC/SD: mq-deadline
ACTION=="add|change", KERNEL=="mmcblk[0-9]*", ATTR{queue/scheduler}="mq-deadline"
```

```bash
# Anwenden
sudo udevadm control --reload-rules
sudo udevadm trigger

# Prüfen
cat /sys/block/nvme0n1/queue/scheduler
cat /sys/block/sda/queue/scheduler

# Queue-Tiefe für NVMe optimieren
cat /sys/block/nvme0n1/queue/nr_requests   # Default 1024, kann erhöht werden
```

### Weitere nützliche udev-Rules

```bash
# /etc/udev/rules.d/70-power.rules
# USB Autosuspend
ACTION=="add", SUBSYSTEM=="usb", ATTR{power/autosuspend}="2"

# /etc/udev/rules.d/80-gamepad.rules
# Xbox-Controller Zugriff ohne root
SUBSYSTEM=="usb", ATTRS{idVendor}=="045e", MODE="0666"
```

---

## 7. Power-Management

### auto-cpufreq (empfohlen für Laptops)

```bash
sudo pacman -S auto-cpufreq
sudo systemctl enable --now auto-cpufreq.service

# Live-Monitoring
sudo auto-cpufreq --monitor

# Config: /etc/auto-cpufreq.conf
[charger]
governor = performance
turbo = auto
[battery]
governor = powersave
turbo = never
scaling_max_freq = 2500000
```

### TLP (Alternative)

```bash
sudo pacman -S tlp tlp-rdw
sudo systemctl enable --now tlp.service
sudo systemctl mask systemd-rfkill.service systemd-rfkill.socket

# Status
sudo tlp-stat -s
sudo tlp-stat -b  # Battery

# Config: /etc/tlp.conf
CPU_ENERGY_PERF_POLICY_ON_AC=performance
CPU_ENERGY_PERF_POLICY_ON_BAT=power
```

> **Wichtig:** auto-cpufreq und TLP nicht gleichzeitig verwenden!

### CPU Governor manuell

```bash
# Aktuellen Governor prüfen
cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor
cpupower frequency-info

# Setzen
sudo cpupower frequency-set -g performance
# Optionen: performance, powersave, schedutil, conservative, ondemand

# Alle CPUs
for cpu in /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor; do
  echo performance | sudo tee "$cpu"
done
```

---

## 8. SSD/NVMe-Health & TRIM

```bash
# SMART-Status
sudo smartctl -a /dev/nvme0n1
sudo smartctl -a /dev/sda

# NVMe-spezifisch
sudo nvme smart-log /dev/nvme0n1
sudo nvme id-ctrl /dev/nvme0n1  # Controller-Info

# TRIM (CachyOS aktiviert fstrim.timer per Default)
sudo systemctl status fstrim.timer
sudo systemctl enable --now fstrim.timer

# Manuelles TRIM
sudo fstrim -av

# Wear-Level prüfen (NVMe)
sudo smartctl -a /dev/nvme0n1 | grep -i "percentage used"
# Percentage Used: 2%  → 98% Restleben
```

---

## 9. Kernel-Parameter für Performance

Für systemd-boot in `/boot/loader/entries/linux-cachyos.conf`:

```
options ... quiet splash loglevel=3 \
  nowatchdog nmi_watchdog=0 \
  mitigations=off \
  preempt=full threadirqs \
  nvidia_drm.modeset=1 nvidia_drm.fbdev=1 \
  amd_pstate=active \
  split_lock_detect=off
```

| Parameter | Zweck | Risiko |
|-----------|-------|--------|
| nowatchdog nmi_watchdog=0 | Watchdog deaktiviert, weniger Interrupts | Gering — kein Auto-Reboot bei Hang |
| mitigations=off | CPU-Mitigations aus → mehr Performance | **Hoch** — nur auf Desktop ohne untrusted Code |
| preempt=full | Volle Preemption → niedrigere Latenz | Gering |
| threadirqs | IRQs als Threads → besseres Scheduling | Gering |
| amd_pstate=active | AMD P-State EPP Treiber | Nur AMD Zen 3+ |
| split_lock_detect=off | Split-Lock-Detection aus → kein Performance-Hit | Gering |

---

## 10. Monitoring & Benchmarking

```bash
# System-Übersicht
btop           # TUI-Monitor (CPU, RAM, Disk, Net)
sudo nvtop     # GPU-Monitor (NVIDIA + AMD)
sudo intel_gpu_top  # Intel GPU

# CPU-Info
lscpu
cat /proc/cpuinfo | grep "model name" | head -1
nproc

# RAM-Details
free -h
sudo dmidecode -t memory | grep -E "Size|Speed|Type"

# Disk-Benchmark
sudo hdparm -Tt /dev/nvme0n1      # Grob
fio --name=randread --ioengine=io_uring --iodepth=32 --rw=randread \
    --bs=4k --direct=1 --size=1G --numjobs=4 --group_reporting

# Netzwerk-Speed
iperf3 -c speedtest.example.com
curl -s https://raw.githubusercontent.com/sivel/speedtest-cli/master/speedtest.py | python -

# Kernel-Build als Benchmark
time make -j$(nproc)

# Perf (Profiling)
sudo perf stat -a sleep 5
sudo perf top

# Strace für Syscall-Analyse
strace -c <command>

# Latenz messen
sudo cyclictest -t1 -p 80 -n -i 1000 -l 10000
```
