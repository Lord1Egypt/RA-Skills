# Paketmanagement — CachyOS / Arch Linux

## Inhaltsverzeichnis
1. Pacman Grundlagen
2. Pacman Erweitert
3. AUR-Helper (paru, yay)
4. CachyOS Mirrors & Repos
5. Keyring & Signierung
6. Paket-Downgrade
7. PKGBUILD & makepkg
8. Pacman Hooks
9. Paketcache & Bereinigung
10. Orphans & Abhängigkeiten
11. Flatpak & AppImage

---

## 1. Pacman Grundlagen

```bash
# Synchronisieren + Upgrade
sudo pacman -Syu

# Paket installieren
sudo pacman -S <paket>

# Paket entfernen (mit Abhängigkeiten + Configs)
sudo pacman -Rns <paket>

# Paket suchen (in Repos)
pacman -Ss <suchbegriff>

# Paket-Info (Remote)
pacman -Si <paket>

# Paket-Info (lokal installiert)
pacman -Qi <paket>

# Dateien eines Pakets auflisten
pacman -Ql <paket>

# Welchem Paket gehört eine Datei?
pacman -Qo /usr/bin/<binary>

# Alle explizit installierten Pakete
pacman -Qe

# Alle explizit installierten, die nicht in Repos sind (= AUR)
pacman -Qm

# Installationsgröße aller Pakete (sortiert)
pacman -Qi | awk '/^Name/{name=$3} /^Installed Size/{print $4, $5, name}' | sort -rh | head -30
```

---

## 2. Pacman Erweitert

```bash
# Nur herunterladen, nicht installieren
sudo pacman -Sw <paket>

# Lokales Paket installieren
sudo pacman -U /path/to/<paket>.pkg.tar.zst

# Von URL installieren
sudo pacman -U https://example.com/<paket>.pkg.tar.zst

# Paketdatenbank erzwingen (nach korrupter DB)
sudo pacman -Syy

# Upgrade mit Ausnahme
sudo pacman -Syu --ignore=linux-cachyos

# Paket dauerhaft von Updates ausschließen
# /etc/pacman.conf:
# IgnorePkg = linux-cachyos nvidia-dkms

# Paketgruppe installieren
sudo pacman -S --needed base-devel

# Diff zwischen installiert und Repo
pacman -Qii <paket> | grep "Modified"

# Backup der Paketliste
pacman -Qqe > ~/pkglist-explicit.txt
pacman -Qqm > ~/pkglist-aur.txt

# System aus Paketliste wiederherstellen
sudo pacman -S --needed - < ~/pkglist-explicit.txt

# Veränderte Config-Dateien finden
pacman -Qii | grep "MODIFIED" | awk '{print $2}'

# .pacnew-Dateien finden und mergen
sudo find /etc -name "*.pacnew" -o -name "*.pacsave" 2>/dev/null
sudo pacdiff  # interaktives Mergen (Teil von pacman-contrib)

# Paketcache-Pfad
ls /var/cache/pacman/pkg/
```

---

## 3. AUR-Helper

### paru (empfohlen)

```bash
# Installation
sudo pacman -S paru
# oder manuell:
git clone https://aur.archlinux.org/paru-bin.git && cd paru-bin && makepkg -si

# Suchen
paru -Ss <suchbegriff>

# Installieren (interaktiv)
paru <suchbegriff>

# AUR-Pakete updaten
paru -Sua

# System + AUR updaten
paru -Syu

# PKGBUILD vor Build anzeigen
paru --review <paket>

# Cache bereinigen
paru -Sc

# Config: ~/.config/paru/paru.conf
[options]
BottomUp
SudoLoop
CleanAfter
RemoveMake
```

### yay (Alternative)

```bash
sudo pacman -S yay

yay -Ss <suchbegriff>
yay -S <paket>
yay -Sua        # nur AUR-Updates
yay -Yc         # nicht benötigte Abhängigkeiten entfernen
yay -Ps         # Statistiken
```

---

## 4. CachyOS Mirrors & Repos

```bash
# Mirrors aktualisieren (CachyOS-Tool)
sudo cachyos-rate-mirrors

# Manuell: /etc/pacman.d/mirrorlist
# Reflector (Arch Standard):
sudo reflector --country Germany,Austria --protocol https --sort rate --save /etc/pacman.d/mirrorlist

# CachyOS-Repos in /etc/pacman.conf:
[cachyos-v3]        # x86-64-v3 optimiert
[cachyos-v4]        # x86-64-v4 optimiert (falls CPU unterstützt)
[cachyos]           # Basis-Repo
[cachyos-extra-v3]  # Extra-Pakete v3

# Microarchitecture-Level prüfen
/lib/ld-linux-x86-64.so.2 --help 2>&1 | grep supported
# Unterstützt x86-64-v3 → v3-Repos nutzen
# Unterstützt x86-64-v4 → v4-Repos nutzen (nur neueste CPUs)

# Repo-Liste anzeigen
pacman-conf --repo-list
```

---

## 5. Keyring & Signierung

```bash
# CachyOS Keyring installieren/aktualisieren
sudo pacman -S cachyos-keyring

# Arch Keyring aktualisieren
sudo pacman -S archlinux-keyring

# Keyring komplett neu initialisieren (bei schweren Problemen)
sudo rm -rf /etc/pacman.d/gnupg
sudo pacman-key --init
sudo pacman-key --populate archlinux cachyos
sudo pacman -Sy archlinux-keyring cachyos-keyring

# Einzelnen Key importieren
sudo pacman-key --recv-keys <KEY-ID>
sudo pacman-key --lsign-key <KEY-ID>

# Keyserver ändern (bei Timeout)
# /etc/pacman.d/gnupg/gpg.conf
keyserver hkps://keyserver.ubuntu.com

# Signatur-Checks (temporär deaktivieren — nur Notfall!)
# /etc/pacman.conf: SigLevel = Never  → NICHT dauerhaft!
```

---

## 6. Paket-Downgrade

```bash
# Aus lokalem Cache
sudo pacman -U /var/cache/pacman/pkg/<paket>-<alte-version>.pkg.tar.zst

# downgrade Tool
sudo pacman -S downgrade
sudo downgrade <paket>
# Wählt aus Cache oder Arch Linux Archive (ALA)

# Arch Linux Archive (manuell)
# https://archive.archlinux.org/packages/
sudo pacman -U https://archive.archlinux.org/packages/p/<paket>/<paket>-<version>-x86_64.pkg.tar.zst

# Nach Downgrade: IgnorePkg setzen!
# /etc/pacman.conf: IgnorePkg = <paket>
```

---

## 7. PKGBUILD & makepkg

```bash
# PKGBUILD-Struktur
pkgname=<name>
pkgver=<version>
pkgrel=1
pkgdesc="Beschreibung"
arch=('x86_64')
url="https://..."
license=('MIT')
depends=('dep1' 'dep2')
makedepends=('cmake' 'git')
source=("$pkgname-$pkgver.tar.gz::https://...")
sha256sums=('SKIP')

build() {
  cd "$pkgname-$pkgver"
  cmake -B build -DCMAKE_INSTALL_PREFIX=/usr
  cmake --build build
}

package() {
  cd "$pkgname-$pkgver"
  DESTDIR="$pkgdir" cmake --install build
}

# Bauen
makepkg -si            # Build + Install
makepkg -sri           # + Deps installieren
makepkg -srcf          # + Clean + Force
makepkg --printsrcinfo > .SRCINFO  # Für AUR-Upload

# makepkg Konfiguration: /etc/makepkg.conf
MAKEFLAGS="-j$(nproc)"
COMPRESSZST=(zstd -c -T0 --ultra -20 -)
BUILDDIR=/tmp/makepkg
PKGDEST=~/packages
# CachyOS-spezifische Flags:
CFLAGS="-march=x86-64-v3 -O2 -pipe"
CXXFLAGS="$CFLAGS"

# namcap — Paket-Linter
sudo pacman -S namcap
namcap PKGBUILD
namcap <paket>.pkg.tar.zst
```

---

## 8. Pacman Hooks

```bash
# Hook-Verzeichnis: /etc/pacman.d/hooks/

# Beispiel: Snapper-Snapshot vor jedem Upgrade
# /etc/pacman.d/hooks/00-snapper-pre.hook
[Trigger]
Operation = Upgrade
Operation = Install
Operation = Remove
Type = Package
Target = *

[Action]
Description = Creating pre-transaction snapshot...
When = PreTransaction
Exec = /usr/bin/snapper -c root create -t pre -d "pacman transaction"
Depends = snapper

# Beispiel: mkinitcpio nach Kernel-Update
# (bereits Standard, aber zur Referenz)
# /etc/pacman.d/hooks/90-mkinitcpio.hook
[Trigger]
Type = File
Operation = Install
Operation = Upgrade
Target = usr/lib/modules/*/vmlinuz

[Action]
Description = Updating initramfs...
When = PostTransaction
Exec = /usr/bin/mkinitcpio -P
```

---

## 9. Paketcache & Bereinigung

```bash
# Cache-Größe
du -sh /var/cache/pacman/pkg/

# Nur letzte 3 Versionen behalten
sudo paccache -r
sudo paccache -rk3     # Behalte 3 Versionen
sudo paccache -rk1     # Behalte nur aktuelle

# Uninstallierte Pakete aus Cache entfernen
sudo paccache -ruk0

# Automatisch via Hook
sudo pacman -S pacman-contrib
# /etc/pacman.d/hooks/clean-cache.hook
[Trigger]
Operation = Upgrade
Operation = Install
Operation = Remove
Type = Package
Target = *

[Action]
Description = Cleaning pacman cache (keeping last 3)...
When = PostTransaction
Exec = /usr/bin/paccache -rk3

# AUR-Build-Cache
paru -Sc     # paru Cache bereinigen
rm -rf ~/.cache/paru/clone/*
```

---

## 10. Orphans & Abhängigkeiten

```bash
# Verwaiste Pakete (nirgends mehr benötigt)
pacman -Qtdq

# Orphans entfernen
sudo pacman -Rns $(pacman -Qtdq)

# Optional installierte Pakete
pacman -Qdq

# Abhängigkeitsbaum eines Pakets
pactree <paket>

# Reverse-Dependencies (wer braucht dieses Paket?)
pactree -r <paket>

# Fehlende Abhängigkeiten prüfen
pacman -Dk

# Gebrochene Symlinks finden
sudo find / -xtype l -not -path "/proc/*" -not -path "/sys/*" 2>/dev/null
```

---

## 11. Flatpak & AppImage

```bash
# Flatpak
sudo pacman -S flatpak
flatpak remote-add --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo

flatpak install flathub <app-id>
flatpak update
flatpak list
flatpak uninstall --unused   # Unbenutzte Runtimes entfernen
flatpak repair               # Reparieren

# Flatpak-Berechtigungen (Flatseal)
flatpak install flathub com.github.tchx84.Flatseal

# AppImage
chmod +x <app>.AppImage
./<app>.AppImage

# AppImage in System integrieren
paru -S appimagelauncher
```
