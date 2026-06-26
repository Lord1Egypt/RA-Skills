# Virtualisierung & Container — CachyOS

## Inhaltsverzeichnis
1. KVM/QEMU/libvirt
2. GPU-Passthrough (VFIO)
3. Docker
4. Podman (Rootless)
5. LXC/LXD
6. Distrobox
7. Virt-Manager Tipps

---

## 1. KVM/QEMU/libvirt

```bash
# Voraussetzung: CPU-Virtualisierung prüfen
grep -cE '(vmx|svm)' /proc/cpuinfo  # >0 = OK
lscpu | grep Virtualization          # VT-x oder AMD-V

# Installation
sudo pacman -S qemu-full virt-manager libvirt edk2-ovmf dnsmasq vde2 \
  bridge-utils openbsd-netcat iptables-nft

# Dienste starten
sudo systemctl enable --now libvirtd.service
sudo systemctl enable --now virtlogd.service

# User zur Gruppe hinzufügen
sudo usermod -aG libvirt $(whoami)
sudo usermod -aG kvm $(whoami)
# Neu einloggen!

# Default-Netzwerk starten
sudo virsh net-start default
sudo virsh net-autostart default

# VM erstellen (CLI)
virt-install \
  --name=debian12 \
  --ram=4096 \
  --vcpus=4 \
  --cpu host-passthrough \
  --os-variant=debian12 \
  --cdrom=/path/to/debian-12.iso \
  --disk size=40,format=qcow2 \
  --network bridge=virbr0 \
  --graphics spice \
  --boot uefi

# VM-Management
virsh list --all
virsh start <vm>
virsh shutdown <vm>
virsh destroy <vm>          # Force Stop
virsh undefine <vm> --remove-all-storage
virsh snapshot-create-as <vm> --name "pre-update"
virsh snapshot-list <vm>
virsh snapshot-revert <vm> "pre-update"

# VM-Disk verkleinern
qemu-img convert -O qcow2 -c old.qcow2 new.qcow2

# Hugepages für VMs
# /etc/sysctl.d/99-hugepages.conf
vm.nr_hugepages = 2048
# → 2048 * 2MB = 4GB für VMs reserviert

# Nested Virtualization
# Intel: echo 'options kvm_intel nested=1' | sudo tee /etc/modprobe.d/kvm-nested.conf
# AMD:   echo 'options kvm_amd nested=1' | sudo tee /etc/modprobe.d/kvm-nested.conf
```

---

## 2. GPU-Passthrough (VFIO)

```bash
# === Voraussetzungen ===
# - IOMMU aktiviert (Intel VT-d / AMD-Vi)
# - Separate GPU für Host und Guest
# - UEFI-VM (OVMF)

# 1. IOMMU aktivieren (Kernel-Parameter)
# Intel: intel_iommu=on iommu=pt
# AMD:   amd_iommu=on iommu=pt

# 2. IOMMU-Gruppen prüfen
for g in $(find /sys/kernel/iommu_groups/* -maxdepth 0 -type d | sort -V); do
  echo "IOMMU Group ${g##*/}:"
  for d in $g/devices/*; do
    echo -e "\t$(lspci -nns ${d##*/})"
  done
done

# 3. GPU-IDs ermitteln (Vendor:Device)
lspci -nn | grep -i nvidia
# z.B. 10de:2684,10de:22ba (GPU + Audio)

# 4. VFIO-Treiber binden
# /etc/modprobe.d/vfio.conf
options vfio-pci ids=10de:2684,10de:22ba
softdep nvidia pre: vfio-pci

# 5. mkinitcpio: VFIO früh laden
# /etc/mkinitcpio.conf
MODULES=(vfio_pci vfio vfio_iommu_type1)
sudo mkinitcpio -P

# 6. Reboot + prüfen
lspci -k | grep -A2 "NVIDIA"
# Kernel driver in use: vfio-pci  ← Korrekt!

# 7. In virt-manager: PCI-Gerät hinzufügen
# → Add Hardware → PCI Host Device → GPU + Audio auswählen

# 8. Looking Glass (für GPU-Passthrough ohne zweiten Monitor)
paru -S looking-glass-client
# Shared Memory in VM-XML:
# <shmem name='looking-glass'>
#   <model type='ivshmem-plain'/>
#   <size unit='M'>64</size>
# </shmem>

# Troubleshooting
dmesg | grep -i vfio
dmesg | grep -i iommu
```

---

## 3. Docker

```bash
sudo pacman -S docker docker-compose docker-buildx

# Dienst starten
sudo systemctl enable --now docker.service

# User zur Gruppe (vermeidet sudo)
sudo usermod -aG docker $(whoami)
# Neu einloggen!

# Basis-Befehle
docker ps                    # Laufende Container
docker ps -a                 # Alle Container
docker images                # Images
docker pull <image>
docker run -d --name test -p 8080:80 nginx
docker exec -it <container> bash
docker logs -f <container>
docker stop <container>
docker rm <container>
docker rmi <image>

# Docker Compose
docker compose up -d
docker compose down
docker compose logs -f
docker compose pull
docker compose restart <service>

# Aufräumen
docker system prune -af      # ALLES nicht genutzte entfernen
docker volume prune           # Unbenutzte Volumes
docker image prune -a         # Unbenutzte Images
docker builder prune          # Build-Cache

# Storage-Driver (CachyOS BTRFS)
# /etc/docker/daemon.json
{
  "storage-driver": "btrfs",
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  },
  "dns": ["1.1.1.1", "9.9.9.9"]
}

# Docker-Root verschieben
# /etc/docker/daemon.json
{
  "data-root": "/mnt/data/docker"
}
sudo systemctl restart docker

# Ressourcen-Limits
docker run -d --memory=2g --cpus=2 --name limited nginx

# Netzwerk
docker network ls
docker network create mynet
docker network inspect mynet
```

---

## 4. Podman (Rootless)

```bash
sudo pacman -S podman podman-compose podman-docker  # docker-Alias

# Rootless — kein Daemon, kein root!
podman run -d --name web -p 8080:80 nginx
podman ps
podman exec -it web bash
podman stop web
podman rm web

# Pods (wie K8s)
podman pod create --name mypod -p 8080:80
podman run -d --pod mypod nginx
podman run -d --pod mypod redis

# Systemd-Integration (Auto-Start ohne Daemon)
podman generate systemd --new --name web > ~/.config/systemd/user/container-web.service
systemctl --user enable --now container-web.service
loginctl enable-linger $(whoami)  # Überlebt Logout

# Podman Compose
podman-compose up -d
podman-compose down

# Registries: /etc/containers/registries.conf
unqualified-search-registries = ["docker.io", "quay.io", "ghcr.io"]

# Storage: ~/.local/share/containers/storage/
```

---

## 5. LXC/LXD

```bash
# LXD (System-Container)
paru -S lxd
sudo systemctl enable --now lxd.service
sudo usermod -aG lxd $(whoami)

lxd init  # Interaktive Ersteinrichtung

lxc launch ubuntu:24.04 mycontainer
lxc exec mycontainer -- bash
lxc list
lxc stop mycontainer
lxc delete mycontainer
lxc snapshot mycontainer snap1
```

---

## 6. Distrobox (Container als Desktop-Apps)

```bash
sudo pacman -S distrobox

# Box erstellen (beliebige Distro!)
distrobox create --name fedora --image fedora:40
distrobox create --name ubuntu --image ubuntu:24.04
distrobox create --name debian --image debian:12

# Eintreten
distrobox enter fedora

# App aus Container als Host-Desktop-Eintrag exportieren
distrobox enter fedora
sudo dnf install gimp
distrobox-export --app gimp
# → .desktop-Datei wird auf dem Host erstellt!

# CLI-Tool exportieren
distrobox-export --bin /usr/bin/htop --export-path ~/.local/bin

# Box löschen
distrobox rm fedora

# Alle Boxen
distrobox list
```

---

## 7. Virt-Manager Tipps

```bash
# Performance-Optimierung in VM-XML:
# CPU: host-passthrough
# Festplatte: virtio-scsi (statt ide/sata)
# Netzwerk: virtio
# Display: Spice mit QXL (oder VirtIO-GPU)
# Speicher: Hugepages aktivieren

# Windows-VM: VirtIO-Treiber
# ISO: https://fedorapeople.org/groups/virt/virtio-win/direct-downloads/stable-virtio/virtio-win.iso
# Vor Installation: VirtIO-Storage-Treiber laden

# Shared Folders (virtiofs)
# In VM-XML:
# <filesystem type='mount' accessmode='passthrough'>
#   <source dir='/home/user/shared'/>
#   <target dir='hostshare'/>
#   <driver type='virtiofs'/>
# </filesystem>
# In Guest: mount -t virtiofs hostshare /mnt/shared

# SPICE USB-Redirect (USB-Geräte in VM nutzen)
sudo pacman -S spice-vdagent
```
