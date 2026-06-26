# Boot & Verschlüsselung — CachyOS

## Inhaltsverzeichnis
1. systemd-boot
2. GRUB
3. mkinitcpio
4. dracut
5. Kernel-Management
6. LUKS / dm-crypt
7. Secure Boot
8. Boot-Recovery (Chroot)
9. Unified Kernel Images (UKI)

---

## 1. systemd-boot (CachyOS UEFI Default)

```bash
# Status
bootctl status

# Einträge auflisten
bootctl list

# Loader-Config: /boot/loader/loader.conf
default  linux-cachyos.conf
timeout  3
console-mode max
editor   no          # WICHTIG: editor no für Sicherheit!

# Boot-Eintrag: /boot/loader/entries/linux-cachyos.conf
title   CachyOS Linux
linux   /vmlinuz-linux-cachyos
initrd  /initramfs-linux-cachyos.img
# Intel: initrd /intel-ucode.img
# AMD:   initrd /amd-ucode.img
options root=UUID=<uuid> rw quiet splash loglevel=3

# Fallback-Eintrag: /boot/loader/entries/linux-cachyos-fallback.conf
title   CachyOS Linux (Fallback)
linux   /vmlinuz-linux-cachyos
initrd  /initramfs-linux-cachyos-fallback.img
options root=UUID=<uuid> rw

# Bootloader aktualisieren
sudo bootctl update

# Neuen Eintrag erstellen
sudo cp /boot/loader/entries/linux-cachyos.conf /boot/loader/entries/linux-cachyos-lts.conf
# Anpassen: vmlinuz-linux-cachyos-lts, initramfs-linux-cachyos-lts.img

# UUID finden
blkid -s UUID -o value /dev/nvme0n1p2
```

---

## 2. GRUB

```bash
# Config: /etc/default/grub
GRUB_DEFAULT=0
GRUB_TIMEOUT=3
GRUB_CMDLINE_LINUX_DEFAULT="quiet splash loglevel=3 nowatchdog"
GRUB_CMDLINE_LINUX=""
GRUB_GFXMODE=auto
GRUB_DISABLE_OS_PROBER=false  # Für Dual-Boot

# Nach Änderung: Config neu generieren
sudo grub-mkconfig -o /boot/grub/grub.cfg

# GRUB neu installieren (UEFI)
sudo grub-install --target=x86_64-efi --efi-directory=/boot/efi --bootloader-id=CachyOS

# GRUB neu installieren (BIOS/Legacy)
sudo grub-install --target=i386-pc /dev/sdX

# OS-Prober für Dual-Boot
sudo pacman -S os-prober
sudo os-prober
sudo grub-mkconfig -o /boot/grub/grub.cfg

# GRUB Rescue (von Grub-Prompt)
grub> set root=(hd0,gpt2)
grub> linux /vmlinuz-linux-cachyos root=/dev/nvme0n1p2
grub> initrd /initramfs-linux-cachyos.img
grub> boot

# GRUB Theme
sudo pacman -S cachyos-grub-theme
# /etc/default/grub:
# GRUB_THEME="/usr/share/grub/themes/cachyos/theme.txt"
```

---

## 3. mkinitcpio (Standard)

```bash
# Config: /etc/mkinitcpio.conf

# MODULES — Für Early-KMS und Hardware-spezifisches
# NVIDIA:
MODULES=(nvidia nvidia_modeset nvidia_uvm nvidia_drm)
# AMD:
MODULES=(amdgpu)
# Intel:
MODULES=(i915)
# BTRFS:
MODULES=(btrfs)

# HOOKS — Reihenfolge ist wichtig!
HOOKS=(base udev autodetect microcode modconf kms keyboard keymap consolefont block filesystems fsck)
# Für LUKS:
HOOKS=(base udev autodetect microcode modconf kms keyboard keymap consolefont block encrypt filesystems fsck)
# Für LVM:
HOOKS=(base udev autodetect microcode modconf kms keyboard keymap consolefont block lvm2 filesystems fsck)
# Für LUKS + LVM:
HOOKS=(base udev autodetect microcode modconf kms keyboard keymap consolefont block encrypt lvm2 filesystems fsck)
# Für systemd-basiert (Alternative):
HOOKS=(base systemd autodetect microcode modconf kms keyboard sd-vconsole block sd-encrypt filesystems fsck)

# COMPRESSION
COMPRESSION="zstd"
COMPRESSION_OPTIONS=(-19 -T0)

# Alle Kernel neu bauen
sudo mkinitcpio -P

# Einzelnen Kernel bauen
sudo mkinitcpio -p linux-cachyos

# Preset anzeigen
cat /etc/mkinitcpio.d/linux-cachyos.preset

# Verbose bauen (bei Problemen)
sudo mkinitcpio -p linux-cachyos -v

# Hooks auflisten (verfügbar)
ls /usr/lib/initcpio/hooks/
ls /usr/lib/initcpio/install/
```

---

## 4. dracut (Alternative)

```bash
# Installieren
sudo pacman -S dracut

# Config: /etc/dracut.conf.d/
# /etc/dracut.conf.d/cachyos.conf
hostonly="yes"
hostonly_cmdline="no"
compress="zstd"
add_dracutmodules+=" crypt btrfs "
force="yes"
# NVIDIA Early-KMS:
force_drivers+=" nvidia nvidia_modeset nvidia_uvm nvidia_drm "

# Rebuild
sudo dracut-rebuild
# oder manuell:
sudo dracut --force /boot/initramfs-linux-cachyos.img $(uname -r)

# Inhalt inspizieren
lsinitrd /boot/initramfs-linux-cachyos.img
lsinitrd /boot/initramfs-linux-cachyos.img | grep nvidia
```

---

## 5. Kernel-Management

```bash
# Verfügbare CachyOS-Kernel
pacman -Ss linux-cachyos

# Installierte Kernel
pacman -Q | grep "^linux-"

# Kernel wechseln
sudo pacman -S linux-cachyos-lts linux-cachyos-lts-headers
sudo mkinitcpio -P  # oder dracut-rebuild

# CachyOS Kernel Manager (GUI)
cachyos-kernel-manager

# Laufenden Kernel
uname -r
uname -a

# Kernel-Module
lsmod
modinfo <modul>
modprobe <modul>         # Laden
modprobe -r <modul>      # Entladen

# Modul-Blacklist
# /etc/modprobe.d/blacklist.conf
blacklist nouveau
blacklist pcspkr

# DKMS-Status (für nvidia-dkms etc.)
dkms status

# DKMS manuell bauen
sudo dkms autoinstall

# Kernel-Config anzeigen
zcat /proc/config.gz | grep CONFIG_SCHED
```

---

## 6. LUKS / dm-crypt

```bash
# === Neue LUKS-Partition erstellen ===
# WARNUNG: Löscht alle Daten!
sudo cryptsetup luksFormat /dev/nvme0n1p2
sudo cryptsetup open /dev/nvme0n1p2 cryptroot
sudo mkfs.btrfs /dev/mapper/cryptroot
sudo mount /dev/mapper/cryptroot /mnt

# === LUKS-Infos ===
sudo cryptsetup luksDump /dev/nvme0n1p2

# === Passwort hinzufügen/ändern ===
sudo cryptsetup luksAddKey /dev/nvme0n1p2
sudo cryptsetup luksChangeKey /dev/nvme0n1p2
sudo cryptsetup luksRemoveKey /dev/nvme0n1p2

# === Keyfile erstellen (für Auto-Unlock) ===
sudo dd if=/dev/urandom of=/etc/cryptsetup-keys.d/cryptroot.key bs=512 count=4
sudo chmod 000 /etc/cryptsetup-keys.d/cryptroot.key
sudo cryptsetup luksAddKey /dev/nvme0n1p2 /etc/cryptsetup-keys.d/cryptroot.key

# === /etc/crypttab ===
# cryptroot  UUID=<uuid>  /etc/cryptsetup-keys.d/cryptroot.key  luks,discard
# oder für Passwort-Prompt:
# cryptroot  UUID=<uuid>  none  luks,discard

# === Kernel-Parameter (systemd-boot) ===
# options cryptdevice=UUID=<uuid>:cryptroot root=/dev/mapper/cryptroot rw
# Für sd-encrypt Hook:
# options rd.luks.name=<uuid>=cryptroot root=/dev/mapper/cryptroot rw

# === LUKS Header-Backup (WICHTIG!) ===
sudo cryptsetup luksHeaderBackup /dev/nvme0n1p2 --header-backup-file ~/luks-header-backup.img
# Sicher extern speichern!

# === Benchmark ===
cryptsetup benchmark
```

---

## 7. Secure Boot

```bash
# === sbctl (CachyOS empfohlen) ===
sudo pacman -S sbctl

# Status prüfen
sbctl status

# Eigene Schlüssel erstellen
sudo sbctl create-keys

# Schlüssel im Firmware enrollen
sudo sbctl enroll-keys --microsoft
# --microsoft: Microsoft-Keys behalten (für Dual-Boot/Option-ROMs)

# Kernel und Bootloader signieren
sudo sbctl sign -s /boot/vmlinuz-linux-cachyos
sudo sbctl sign -s /boot/EFI/systemd/systemd-bootx64.efi
sudo sbctl sign -s /boot/EFI/BOOT/BOOTX64.EFI
# -s = in DB speichern, wird bei Updates automatisch neu signiert

# Alle signierten Dateien anzeigen
sudo sbctl list-files

# Prüfen ob alles signiert
sudo sbctl verify

# === shim (Alternative für Dual-Boot mit Windows) ===
sudo pacman -S shim-signed
# Komplexere Einrichtung, für reine CachyOS-Systeme sbctl bevorzugen
```

---

## 8. Boot-Recovery (Chroot)

```bash
# 1. Von CachyOS Live-USB booten

# 2. Partitionen identifizieren
lsblk -f

# 3. Root mounten
# Ohne LUKS:
mount /dev/nvme0n1p2 /mnt
# Mit LUKS:
cryptsetup open /dev/nvme0n1p2 cryptroot
mount /dev/mapper/cryptroot /mnt

# 4. BTRFS-Subvolumes (falls verwendet)
mount -o subvol=@ /dev/nvme0n1p2 /mnt
mount -o subvol=@home /dev/nvme0n1p2 /mnt/home

# 5. Boot-Partition mounten
mount /dev/nvme0n1p1 /mnt/boot
# oder /mnt/boot/efi bei GRUB

# 6. Chroot
arch-chroot /mnt

# 7. Im Chroot: Reparaturen
# Pacman-DB reparieren
pacman -Syy
# Kernel neu installieren
pacman -S linux-cachyos linux-cachyos-headers
# Initramfs neu bauen
mkinitcpio -P
# Bootloader reparieren
bootctl install  # systemd-boot
# oder:
grub-install --target=x86_64-efi --efi-directory=/boot/efi --bootloader-id=CachyOS
grub-mkconfig -o /boot/grub/grub.cfg

# 8. Chroot verlassen + unmounten
exit
umount -R /mnt
reboot
```

---

## 9. Unified Kernel Images (UKI)

```bash
# UKI: Kernel + initrd + cmdline in einem EFI-Binary
# Vorteile: Secure Boot einfacher, keine separaten Einträge nötig

# mkinitcpio UKI Config: /etc/mkinitcpio.d/linux-cachyos.preset
ALL_kver="/boot/vmlinuz-linux-cachyos"
PRESETS=('default' 'fallback')
default_uki="/boot/EFI/Linux/cachyos-linux.efi"
default_options="--splash /usr/share/systemd/bootctl/splash-arch.bmp"
fallback_uki="/boot/EFI/Linux/cachyos-linux-fallback.efi"
fallback_options="-S autodetect"

# Kernel-Cmdline für UKI
# /etc/kernel/cmdline
root=UUID=<uuid> rw quiet splash loglevel=3

# Bauen
sudo mkinitcpio -P

# systemd-boot erkennt UKIs automatisch in /boot/EFI/Linux/
bootctl list
```
