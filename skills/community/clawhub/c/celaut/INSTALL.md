# Manual Installation Guide

This guide is for Linux users who want to bootstrap Nodo manually, without executing `install.sh`.
Java is optional and only required for Ergo-backed payment/reputation features.

It follows the current runtime model:

- Local runtimes and binaries under `MAIN_DIR` (Python, Java, yq).
- Cloud Hypervisor assets under `MAIN_DIR/cloud_hypervisor` (services run as microVMs).
- No local Docker by default: packing is delegated to an external packer-service.
  (Docker is only provisioned locally, in isolation, if you opt into
  `packer.local: true`; see step 9.)

## 1) Scope and assumptions

- OS: Ubuntu 22.04 LTS (or compatible Debian-based distro).
- Architecture: `x86_64` or `aarch64`.
- You have `sudo` access.
- Installation root: `TARGET_DIR` (default `/nodo`).

```bash
export TARGET_DIR=/nodo
```

## 2) Install base system packages

These are host-level packages used by setup/build tools. Python/JRE runtimes for Nodo are installed locally in later steps.

```bash
sudo apt-get update
sudo apt-get install -y \
  build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev \
  libssl-dev libreadline-dev libffi-dev libsqlite3-dev \
  wget libbz2-dev busybox-static cpio gzip initramfs-tools-core iputils-ping \
  ca-certificates curl gnupg lsb-release git procps locales \
  iproute2 zip iptables e2fsprogs
```

`iproute2` and `zip` are load-bearing at runtime: `ip` is a hard preflight
requirement for `execute` (CH networking), and `zip` is invoked when packing —
without them the first `execute`/`pack` fails. `iptables`/`e2fsprogs` provide
the `iptables`/`debugfs` tools also checked by the execute preflight.
`protobuf-compiler` is not installed by the setup script and is only needed for
development (regenerating protobufs), so it is omitted here.

## 3) Get source and create config

```bash
git clone https://github.com/celaut-project/nodo.git "$TARGET_DIR"
cd "$TARGET_DIR"
cp -n config.example.yaml config.yaml
```

## 4) Bootstrap local yq and set base config

Install a bootstrap `yq` binary first (used to edit/read `config.yaml`).

```bash
ARCH="$(uname -m)"
case "$ARCH" in
  x86_64|amd64) YQ_ASSET=yq_linux_amd64 ;;
  aarch64|arm64) YQ_ASSET=yq_linux_arm64 ;;
  *) echo "Unsupported arch: $ARCH"; exit 1 ;;
esac

mkdir -p "$TARGET_DIR/bin"
curl -fsSL "https://github.com/mikefarah/yq/releases/download/v4.44.3/${YQ_ASSET}" -o "$TARGET_DIR/bin/yq"
chmod +x "$TARGET_DIR/bin/yq"
```

Align `main.*` paths with your installation root:

```bash
"$TARGET_DIR/bin/yq" -i \
  '.main.MAIN_DIR = env(TARGET_DIR) |
   .main.STORAGE = env(TARGET_DIR) + "/storage" |
   .main.CACHE = .main.STORAGE + "/__cache__/" |
   .main.REGISTRY = .main.STORAGE + "/__registry__/" |
   .main.METADATA_REGISTRY = .main.STORAGE + "/__metadata__/" |
   .main.BLOCKDIR = .main.STORAGE + "/__block__/" |
   .main.DATABASE_FILE = .main.STORAGE + "/database.sqlite"' \
  "$TARGET_DIR/config.yaml"
```

Optional: override runtime/binary locations in `dependencies.*` before continuing. Example (custom roots):

```bash
"$TARGET_DIR/bin/yq" -i \
  '.dependencies.python.RUNTIME_ROOT = "${main.MAIN_DIR}/runtime/python" |
   .dependencies.python.RUNTIME_BIN = "${main.MAIN_DIR}/runtime/python/current/bin/python3" |
   .dependencies.python.VENV_BIN = "${main.MAIN_DIR}/venv/bin/python" |
   .dependencies.java.RUNTIME_ROOT = "${main.MAIN_DIR}/runtime/java" |
   .dependencies.java.JAVA_HOME = "${main.MAIN_DIR}/runtime/java/current" |
   .dependencies.yq.BIN = "${main.MAIN_DIR}/bin/yq"' \
  "$TARGET_DIR/config.yaml"
```

## 5) Resolve effective paths from `config.yaml`

Run this block once and keep the shell session open. Later commands rely on these variables.

```bash
expand_main_dir() {
  printf '%s' "$1" | sed "s|\${main.MAIN_DIR}|$TARGET_DIR|g"
}

read_cfg_path_or_default() {
  local query="$1"
  local fallback="$2"
  local raw
  raw="$("$TARGET_DIR/bin/yq" -r "$query // \"\"" "$TARGET_DIR/config.yaml")"
  if [ -z "$raw" ] || [ "$raw" = "null" ]; then
    raw="$fallback"
  fi
  expand_main_dir "$raw"
}

YQ_BIN="$(read_cfg_path_or_default '.dependencies.yq.BIN' '${main.MAIN_DIR}/bin/yq')"
mkdir -p "$(dirname "$YQ_BIN")"
if [ "$YQ_BIN" != "$TARGET_DIR/bin/yq" ]; then
  cp "$TARGET_DIR/bin/yq" "$YQ_BIN"
  chmod +x "$YQ_BIN"
fi

PY_RUNTIME_ROOT="$(read_cfg_path_or_default '.dependencies.python.RUNTIME_ROOT' '${main.MAIN_DIR}/runtime/python')"
PY_RUNTIME_BIN="$(read_cfg_path_or_default '.dependencies.python.RUNTIME_BIN' '${main.MAIN_DIR}/runtime/python/current/bin/python3')"
PY_VENV_BIN="$(read_cfg_path_or_default '.dependencies.python.VENV_BIN' '${main.MAIN_DIR}/venv/bin/python')"
PY_VENV_DIR="$(dirname "$(dirname "$PY_VENV_BIN")")"

JAVA_RUNTIME_ROOT="$(read_cfg_path_or_default '.dependencies.java.RUNTIME_ROOT' '${main.MAIN_DIR}/runtime/java')"
JAVA_HOME_PATH="$(read_cfg_path_or_default '.dependencies.java.JAVA_HOME' '${main.MAIN_DIR}/runtime/java/current')"

CH_BINARY_PATH="$(read_cfg_path_or_default '.virtualizers.ch.BINARY_PATH' '${main.MAIN_DIR}/bin/cloud-hypervisor')"
```

## 6) Install local portable Python runtime

Pinned versions used by project setup:

- Python: `3.11.15`
- python-build-standalone tag: `20260325`

```bash
PY_VER="3.11.15"
PY_TAG="20260325"
ARCH="$(uname -m)"
case "$ARCH" in
  x86_64|amd64) PY_ARCH="x86_64-unknown-linux-gnu" ;;
  aarch64|arm64) PY_ARCH="aarch64-unknown-linux-gnu" ;;
  *) echo "Unsupported arch: $ARCH"; exit 1 ;;
esac

PY_DIST="cpython-${PY_VER}+${PY_TAG}-${PY_ARCH}-install_only_stripped.tar.gz"
PY_BASE="https://github.com/astral-sh/python-build-standalone/releases/download/${PY_TAG}"

mkdir -p "$PY_RUNTIME_ROOT"
curl -fsSL "$PY_BASE/$PY_DIST" -o /tmp/nodo-python.tar.gz
curl -fsSL "$PY_BASE/SHA256SUMS" -o /tmp/nodo-python.SHA256SUMS

EXPECTED="$(awk -v name="$PY_DIST" '{f=$2; gsub(/^\*/,"",f); if (f==name || $NF==name) {print $1; exit}}' /tmp/nodo-python.SHA256SUMS)"
ACTUAL="$(sha256sum /tmp/nodo-python.tar.gz | awk '{print $1}')"
[ "$EXPECTED" = "$ACTUAL" ] || { echo "Python checksum mismatch"; exit 1; }

PY_INSTALL_DIR="$PY_RUNTIME_ROOT/${PY_VER}+${PY_TAG}"
mkdir -p "$PY_INSTALL_DIR"
TMP_PY_DIR="$(mktemp -d)"
tar -xzf /tmp/nodo-python.tar.gz -C "$TMP_PY_DIR"
cp -a "$TMP_PY_DIR"/*/. "$PY_INSTALL_DIR" 2>/dev/null || cp -a "$TMP_PY_DIR"/. "$PY_INSTALL_DIR"
ln -sfn "$PY_INSTALL_DIR" "$PY_RUNTIME_ROOT/current"

PY_CURRENT_BIN="$PY_RUNTIME_ROOT/current/bin/python3"
if [ "$PY_RUNTIME_BIN" != "$PY_CURRENT_BIN" ]; then
  mkdir -p "$(dirname "$PY_RUNTIME_BIN")"
  ln -sfn "$PY_CURRENT_BIN" "$PY_RUNTIME_BIN"
fi

rm -rf "$TMP_PY_DIR" /tmp/nodo-python.tar.gz /tmp/nodo-python.SHA256SUMS
```

## 7) Install local portable Java runtime (Temurin JRE 21)

Pinned version used by project setup:

- JRE: `21.0.8_9` (`jdk-21.0.8+9` release tag)

```bash
JRE_VER="21.0.8_9"
JRE_TAG="jdk-21.0.8%2B9"
ARCH="$(uname -m)"
case "$ARCH" in
  x86_64|amd64) JRE_DIST="OpenJDK21U-jre_x64_linux_hotspot_${JRE_VER}.tar.gz" ;;
  aarch64|arm64) JRE_DIST="OpenJDK21U-jre_aarch64_linux_hotspot_${JRE_VER}.tar.gz" ;;
  *) echo "Unsupported arch: $ARCH"; exit 1 ;;
esac

JRE_URL="https://github.com/adoptium/temurin21-binaries/releases/download/${JRE_TAG}/${JRE_DIST}"

mkdir -p "$JAVA_RUNTIME_ROOT"
curl -fsSL "$JRE_URL" -o /tmp/nodo-jre.tar.gz
curl -fsSL "${JRE_URL}.sha256.txt" -o /tmp/nodo-jre.sha256.txt

EXPECTED="$(awk '{print $1}' /tmp/nodo-jre.sha256.txt | head -n1)"
ACTUAL="$(sha256sum /tmp/nodo-jre.tar.gz | awk '{print $1}')"
[ "$EXPECTED" = "$ACTUAL" ] || { echo "JRE checksum mismatch"; exit 1; }

JRE_INSTALL_DIR="$JAVA_RUNTIME_ROOT/${JRE_VER}"
mkdir -p "$JRE_INSTALL_DIR"
TMP_JRE_DIR="$(mktemp -d)"
tar -xzf /tmp/nodo-jre.tar.gz -C "$TMP_JRE_DIR"
cp -a "$TMP_JRE_DIR"/*/. "$JRE_INSTALL_DIR" 2>/dev/null || cp -a "$TMP_JRE_DIR"/. "$JRE_INSTALL_DIR"
ln -sfn "$JRE_INSTALL_DIR" "$JAVA_RUNTIME_ROOT/current"

JAVA_CURRENT_HOME="$JAVA_RUNTIME_ROOT/current"
if [ "$JAVA_HOME_PATH" != "$JAVA_CURRENT_HOME" ] && [ "$JAVA_HOME_PATH" != "$JRE_INSTALL_DIR" ]; then
  mkdir -p "$(dirname "$JAVA_HOME_PATH")"
  ln -sfn "$JRE_INSTALL_DIR" "$JAVA_HOME_PATH"
fi

rm -rf "$TMP_JRE_DIR" /tmp/nodo-jre.tar.gz /tmp/nodo-jre.sha256.txt
```

## 8) Create local Python venv and install Python deps

```bash
mkdir -p "$PY_VENV_DIR"
"$PY_RUNTIME_BIN" -m venv "$PY_VENV_DIR"
"$PY_VENV_BIN" -m pip install --upgrade pip
"$PY_VENV_BIN" -m pip install -r "$TARGET_DIR/bash/requirements.txt"
```

## 9) Docker is not installed by default

Docker is **not** installed at install time, and service **execution** never uses
it — services run as **Cloud Hypervisor** microVMs. Docker is only relevant to the
*packer*, and only in the opt-in local mode:

- **Default (`packer.local: false`) — no Docker on this host.** `nodo pack`
  delegates the build to a **packer-service** (it runs Docker/buildx inside its
  own sealed microVM). Set the packer-service's published service id under
  `core_services` in `config.yaml` — the single source of truth:
  `core_services: [{ name: "packer", id: "<id>" }]` — and `nodo execute` it so a
  running instance exists; nodo resolves that instance's `ip:port` automatically.
  When nodo needs to download the packer, it fetches it directly from
  `packer.PACKER_SOURCE_URL` if set, otherwise via the source-application core
  service. To point at an out-of-band packer instead, set
  `packer.PACKER_SERVICE_URL` to its `ip:8080` as an override.

- **Opt-in (`packer.local: true`) — isolated local Docker toolchain.** If you set
  `packer.local: true`, `nodo pack` builds on this host instead. Docker is still
  not installed by the node installer; the first local pack provisions an
  **isolated** toolchain on demand via `bash/install_docker.sh` (independent of
  any Docker already on the host, mirroring `install_java.sh`) and drives its own
  daemon under `MAIN_DIR` — never the host's Docker. See `dependencies.docker.*`
  and `packer.docker.*` in `config.yaml`. Full packing reference:
  [`PACKING.md`](./PACKING.md).

## 10) Install Cloud Hypervisor assets

Pinned version used by project setup:

- Cloud Hypervisor: `v51.1`

```bash
CH_VERSION="v51.1"
ARCH="$(uname -m)"
case "$ARCH" in
  x86_64|amd64)
    CH_ARCH_TAG="linux/amd64"
    CH_ASSET_CANDIDATES=("cloud-hypervisor-static" "cloud-hypervisor-static-x86_64")
    ;;
  aarch64|arm64)
    CH_ARCH_TAG="linux/arm64"
    CH_ASSET_CANDIDATES=("cloud-hypervisor-static-aarch64" "cloud-hypervisor-static-arm64")
    ;;
  *) echo "Unsupported arch: $ARCH"; exit 1 ;;
esac

mkdir -p "$(dirname "$CH_BINARY_PATH")"
CH_OK=""
for A in "${CH_ASSET_CANDIDATES[@]}"; do
  if curl -fsSL "https://github.com/cloud-hypervisor/cloud-hypervisor/releases/download/${CH_VERSION}/${A}" -o /tmp/cloud-hypervisor.bin; then
    install -m 0755 /tmp/cloud-hypervisor.bin "$CH_BINARY_PATH"
    CH_OK=1
    break
  fi
done
[ -n "$CH_OK" ] || { echo "Unable to download cloud-hypervisor"; exit 1; }
rm -f /tmp/cloud-hypervisor.bin

KERNEL_SOURCE="$(readlink -f /boot/vmlinuz 2>/dev/null || true)"
if [ -z "$KERNEL_SOURCE" ] || [ ! -f "$KERNEL_SOURCE" ]; then
  KERNEL_SOURCE="$(find /boot -maxdepth 1 -type f -name 'vmlinuz-*' -printf '%T@ %p\n' | sort -nr | head -n1 | cut -d' ' -f2-)"
fi
[ -f "$KERNEL_SOURCE" ] || { echo "Kernel not found in /boot"; exit 1; }

CH_KERNEL_TARGET="$TARGET_DIR/cloud_hypervisor/kernels/${CH_ARCH_TAG}/vmlinuz"
CH_INITRAMFS_TARGET="$TARGET_DIR/cloud_hypervisor/initramfs/${CH_ARCH_TAG}/initramfs"
mkdir -p "$(dirname "$CH_KERNEL_TARGET")" "$(dirname "$CH_INITRAMFS_TARGET")"
cp -f "$KERNEL_SOURCE" "$CH_KERNEL_TARGET"
chmod 0644 "$CH_KERNEL_TARGET"

bash "$TARGET_DIR/bash/build_ch_initramfs.sh" "$TARGET_DIR" "$CH_ARCH_TAG" "$CH_INITRAMFS_TARGET"

CH_BINARY_PATH="$CH_BINARY_PATH" "$YQ_BIN" -i '.virtualizers.ch.BINARY_PATH = strenv(CH_BINARY_PATH)' "$TARGET_DIR/config.yaml"
CH_ARCH_TAG="$CH_ARCH_TAG" CH_KERNEL_TARGET="$CH_KERNEL_TARGET" "$YQ_BIN" -i \
  '.virtualizers.ch.KERNEL_PATHS[strenv(CH_ARCH_TAG)] = strenv(CH_KERNEL_TARGET)' \
  "$TARGET_DIR/config.yaml"
CH_ARCH_TAG="$CH_ARCH_TAG" CH_INITRAMFS_TARGET="$CH_INITRAMFS_TARGET" "$YQ_BIN" -i \
  '.virtualizers.ch.INITRAMFS_PATHS[strenv(CH_ARCH_TAG)] = strenv(CH_INITRAMFS_TARGET)' \
  "$TARGET_DIR/config.yaml"
```

## 11) Isolated local Docker daemon directories

Nodo does not use the host Docker daemon. When packing with `packer.local: true`,
the first local pack lazily starts a private, isolated Docker daemon and creates
its state under `$TARGET_DIR/docker`:

- `$TARGET_DIR/docker/data` — data-root
- `$TARGET_DIR/docker/config` — daemon config
- `$TARGET_DIR/docker/exec` — exec root
- `$TARGET_DIR/docker/docker.sock` — the daemon's private socket

These are created automatically on the first local pack (nothing to do here at
install time) and the daemon is stopped again after each pack. `uninstall.sh`
removes this tree during teardown.

## 12) Run DB migration

```bash
"$PY_VENV_BIN" "$TARGET_DIR/nodo.py" migrate
```

## 13) Configure service and wrapper

Create the `systemd` unit from template:

```bash
PY_RUNTIME_DIR="$(dirname "$PY_RUNTIME_BIN")"

sudo sed \
  -e "s|{{MAIN_DIR}}|$TARGET_DIR|g" \
  -e "s|{{JAVA_HOME}}|$JAVA_HOME_PATH|g" \
  -e "s|{{PYTHON_RUNTIME_BIN_DIR}}|$PY_RUNTIME_DIR|g" \
  -e "s|{{PYTHON_VENV_BIN}}|$PY_VENV_BIN|g" \
  "$TARGET_DIR/bash/nodo.service.template" > /tmp/nodo.service

sudo install -m 0644 /tmp/nodo.service /etc/systemd/system/nodo.service
sudo systemctl daemon-reload
sudo systemctl enable --now nodo.service
```

Optional wrapper command (`/usr/local/bin/nodo`) with same env as service:

```bash
sudo tee /usr/local/bin/nodo >/dev/null <<WRAP
#!/bin/bash
ORIGINAL_DIR="\$PWD"
cd "$TARGET_DIR" || exit 1
export JAVA_HOME="$JAVA_HOME_PATH"
export PATH="$JAVA_HOME_PATH/bin:$PY_RUNTIME_DIR:$TARGET_DIR/bin:\$PATH"
source "$PY_VENV_DIR/bin/activate"
ORIGINAL_DIR="\$ORIGINAL_DIR" "$PY_VENV_BIN" "$TARGET_DIR/nodo.py" "\$@"
WRAP
sudo chmod +x /usr/local/bin/nodo
```

## 14) Post-install checks

```bash
systemctl status nodo.service --no-pager
"$PY_VENV_BIN" "$TARGET_DIR/nodo.py" info
```

Cloud Hypervisor checks:

```bash
test -x "$CH_BINARY_PATH"
test -f "$CH_KERNEL_TARGET"
test -f "$CH_INITRAMFS_TARGET"
```

## 15) Operational notes

- Cross-arch builds are disabled in this profile. If target architecture differs from host architecture, build/pack flows fail early with an explicit message.
- QEMU/binfmt are intentionally not installed.
- Keep `config.yaml` and actual installed paths aligned. If you move runtimes/binaries, update `dependencies.*` and restart `nodo.service`.
