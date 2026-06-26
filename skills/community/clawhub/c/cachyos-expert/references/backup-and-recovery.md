# Backup & Recovery — CachyOS

## Inhaltsverzeichnis
1. Snapper (BTRFS Snapshots)
2. btrbk
3. Timeshift
4. Borg Backup
5. rsync
6. BTRFS Send/Receive
7. Disaster Recovery Checkliste

---

## 1. Snapper (empfohlen für CachyOS BTRFS)

```bash
sudo pacman -S snapper snap-pac snapper-gui

# Config für Root erstellen
sudo snapper -c root create-config /

# Config für Home
sudo snapper -c home create-config /home

# Config anzeigen/bearbeiten
sudo snapper -c root get-config
sudo snapper -c root set-config "TIMELINE_CREATE=yes"
sudo snapper -c root set-config "TIMELINE_CLEANUP=yes"
sudo snapper -c root set-config "TIMELINE_LIMIT_HOURLY=5"
sudo snapper -c root set-config "TIMELINE_LIMIT_DAILY=7"
sudo snapper -c root set-config "TIMELINE_LIMIT_WEEKLY=4"
sudo snapper -c root set-config "TIMELINE_LIMIT_MONTHLY=6"
sudo snapper -c root set-config "TIMELINE_LIMIT_YEARLY=2"

# Timer aktivieren
sudo systemctl enable --now snapper-timeline.timer
sudo systemctl enable --now snapper-cleanup.timer

# Manueller Snapshot
sudo snapper -c root create -d "Vor Kernel-Update"
sudo snapper -c root create -t pre -d "Pre-Update"
# ... Update durchführen ...
sudo snapper -c root create -t post --pre-number <N> -d "Post-Update"

# Snapshots auflisten
sudo snapper -c root list

# Diff zwischen Snapshots
sudo snapper -c root diff <N1>..<N2>
sudo snapper -c root status <N1>..<N2>

# Rollback (einzelne Dateien)
sudo snapper -c root undochange <N1>..<N2>

# Komplett-Rollback
# 1. Booten in Snapshot (GRUB + grub-btrfs)
sudo pacman -S grub-btrfs
sudo systemctl enable --now grub-btrfsd
# 2. Oder manuell via chroot

# Snapshot löschen
sudo snapper -c root delete <N>

# snap-pac: Automatische Snapshots bei pacman-Transaktionen
# Wird automatisch via pacman-Hook ausgeführt
```

---

## 2. btrbk (BTRFS Backup-Tool)

```bash
paru -S btrbk

# Config: /etc/btrbk/btrbk.conf
snapshot_preserve_min   2d
snapshot_preserve       14d

target_preserve_min     no
target_preserve         20d 10w *m

snapshot_dir            _snapshots

volume /
  subvolume @
    snapshot_name  root
  subvolume @home
    snapshot_name  home

# Optional: Remote-Backup
target ssh://backup-server/mnt/backups

# Ausführen
sudo btrbk run
sudo btrbk snapshot     # Nur Snapshots
sudo btrbk resume       # Unterbrochenes fortsetzen

# Status
sudo btrbk list all

# Timer: /etc/systemd/system/btrbk.timer
[Unit]
Description=btrbk backup timer
[Timer]
OnCalendar=hourly
Persistent=true
[Install]
WantedBy=timers.target

sudo systemctl enable --now btrbk.timer
```

---

## 3. Timeshift (GUI-basiert)

```bash
sudo pacman -S timeshift

# GUI starten
sudo timeshift-gtk

# CLI
sudo timeshift --create --comments "Vor Update"
sudo timeshift --list
sudo timeshift --restore --snapshot '<snapshot-name>'
sudo timeshift --delete --snapshot '<snapshot-name>'

# Auto-Snapshots: Boot, Hourly, Daily, Weekly, Monthly
# Config: /etc/timeshift/timeshift.json
```

---

## 4. Borg Backup (Dedup + Verschlüsselung)

```bash
sudo pacman -S borg

# Repository erstellen
borg init --encryption=repokey /mnt/backup/borg-repo
# oder remote:
borg init --encryption=repokey ssh://user@server/path/to/repo

# Backup erstellen
borg create --stats --progress \
  /mnt/backup/borg-repo::{hostname}-{now:%Y-%m-%d_%H:%M} \
  /home /etc \
  --exclude '/home/*/.cache' \
  --exclude '/home/*/Downloads' \
  --exclude '/home/*/.local/share/Trash'

# Archive auflisten
borg list /mnt/backup/borg-repo

# Archiv-Inhalt
borg list /mnt/backup/borg-repo::archiv-name

# Wiederherstellen
cd /tmp/restore
borg extract /mnt/backup/borg-repo::archiv-name

# Einzelne Datei
borg extract /mnt/backup/borg-repo::archiv-name home/user/wichtig.txt

# Prune (alte Backups löschen)
borg prune --keep-daily=7 --keep-weekly=4 --keep-monthly=6 /mnt/backup/borg-repo

# Compact (Speicher freigeben nach Prune)
borg compact /mnt/backup/borg-repo

# Integrität prüfen
borg check /mnt/backup/borg-repo

# Repo-Info
borg info /mnt/backup/borg-repo

# Passphrase exportieren (SICHER AUFBEWAHREN!)
borg key export /mnt/backup/borg-repo ~/borg-key-backup.txt
```

### Borg Backup-Skript

```bash
#!/bin/bash
# /usr/local/bin/borg-backup.sh
set -euo pipefail

export BORG_REPO="/mnt/backup/borg-repo"
export BORG_PASSPHRASE="$(cat /root/.borg-passphrase)"

borg create --stats --compression zstd,6 \
  ::"{hostname}-{now:%Y-%m-%d_%H:%M}" \
  /home /etc /var/lib \
  --exclude '*.cache' \
  --exclude '/home/*/Downloads'

borg prune --keep-hourly=24 --keep-daily=7 --keep-weekly=4 --keep-monthly=12
borg compact

# Systemd-Timer dafür erstellen (siehe systemd-and-diagnostics.md)
```

---

## 5. rsync

```bash
# Einfache Synchronisation
rsync -avhP /source/ /destination/

# Mit Löschen (Mirror)
rsync -avhP --delete /source/ /destination/

# Remote
rsync -avhP -e ssh /source/ user@server:/destination/

# Trockenlauf
rsync -avhPn /source/ /destination/

# Exclude
rsync -avhP --exclude='.cache' --exclude='node_modules' /source/ /destination/

# Bandwidth-Limit
rsync -avhP --bwlimit=10000 /source/ /destination/  # 10 MB/s
```

---

## 6. BTRFS Send/Receive

```bash
# Snapshot erstellen (read-only für send!)
sudo btrfs subvolume snapshot -r / /snapshots/root-$(date +%F)

# Lokal kopieren
sudo btrfs send /snapshots/root-2025-01-01 | sudo btrfs receive /mnt/backup/

# Remote kopieren
sudo btrfs send /snapshots/root-2025-01-01 | ssh user@server sudo btrfs receive /mnt/backup/

# Inkrementell (schnell!)
sudo btrfs send -p /snapshots/root-2025-01-01 /snapshots/root-2025-01-02 | \
  sudo btrfs receive /mnt/backup/
```

---

## 7. Disaster Recovery Checkliste

1. **Vor jedem größeren Eingriff**: Snapper-Snapshot + Pacman-Log sichern
2. **Wöchentlich**: Borg-Backup auf externem Medium
3. **LUKS-Header**: Separat gesichert (`cryptsetup luksHeaderBackup`)
4. **Paketliste**: `pacman -Qqe > pkglist.txt`, `pacman -Qqm > aurlist.txt`
5. **Configs**: `/etc/` in Borg enthalten
6. **Bootloader**: `bootctl status` dokumentieren, Einträge sichern
7. **fstab**: Kopie extern aufbewahren
8. **Recovery-USB**: Aktuelles CachyOS Live-ISO bereithalten
