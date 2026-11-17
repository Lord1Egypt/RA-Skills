# Installation routes (fitctl CLI 0.8.0 / Python 0.1.1)

Inventory first; use an existing suitable installation and record versions
and exact paths — do not silently switch versions:

```bash
command -v fitctl; command -v python3; command -v cargo; command -v cc
```

The Python wheel does not install the CLI; the CLI does not install the
Python module. Either route works alone. Public sources:
- CLI/core 0.8.0: https://github.com/tznurmin/fitctl (tag v0.8.0 =
  commit 1ec8777d69525b6037fa2654d084cddcf61e3c62), crates.io package
  `fitctl` 0.8.0 (this crate IS the CLI; `fitctl-core` 0.8.0 is the library)
- Python 0.1.1: https://pypi.org/project/fitctl/0.1.1/ , source
  https://github.com/tznurmin/fitctl-python (tag v0.1.1)

## Python wheel (no compilation)

Ordinary GIL CPython 3.12–3.14, Linux x86_64, glibc >= 2.28 only. Not for
musl, other architectures, free-threaded builds, macOS or Windows — "no
matching wheel" means that platform mismatch, not "no fitctl".

```bash
python3 -m venv .venv
.venv/bin/python -m pip install --only-binary=:all: 'fitctl==0.1.1'
FITCTL_PY="$PWD/.venv/bin/python"
"$FITCTL_PY" -c 'import sys,fitctl; print(sys.executable); print(fitctl.__version__, fitctl.core_version, fitctl.semantic_encoding)'
```

Expected: bindings `0.1.1`, core `0.8.0`, `fitctl.semantic_cbor.v2`. No
other Python dependencies. Keep `.venv/` outside the skill and git-ignored;
choose one interpreter and use it consistently (`$FITCTL_PY`).

## Rust CLI

No prebuilt binaries are published with the GitHub release. Two routes:

### A. crates.io (recommended)

Needs a Rust toolchain (cargo + rustc), a C linker (`cc`), and network to
crates.io. On managed systems (e.g. NixOS) use the existing toolchain
source; do not replace it with rustup. On a conventional Linux box without
Rust, the official user-local installer is documented at
https://rust-lang.org/tools/install/ (`rustup-init -y --profile minimal
--no-modify-path`). If a dynamically-linked rustup-init cannot run
(NixOS stub-ld), obtain cargo/rustc from the system's package manager
(e.g. `nix-build -E 'with import <nixpkgs> {}; cargo'`) instead.

```bash
FITCTL_INSTALL_ROOT="$PWD/.tools/fitctl-0.8.0"     # isolated root
BUILD_DIR=$(mktemp -d "${TMPDIR:-/tmp}/fitctl-install.XXXXXX")   # operation-owned scratch
mkdir -p "$BUILD_DIR/target"
findmnt -T "$BUILD_DIR"    # inspect the filesystem backing the build directory
CARGO_HOME="$PWD/.tools/cargo-home" CARGO_TARGET_DIR="$BUILD_DIR/target" \
  cargo install fitctl --version 0.8.0 --locked \
  --root "$FITCTL_INSTALL_ROOT" --jobs 3
"$FITCTL_INSTALL_ROOT/bin/fitctl" --version    # must print: fitctl 0.8.0
rm -rf "$BUILD_DIR"
```

Notes that matter in practice:
- `--locked` uses the release lockfile; avoid `--force` over unrelated
  installs. No MSRV is declared for 0.8.0 — do not invent one or paper over
  a toolchain failure with `--ignore-rust-version`.
- cargo writes its registry cache under `$CARGO_HOME` (default
  `~/.cargo`); point `CARGO_HOME` at an operation-owned directory when the
  home cache is absent or read-only (sandboxed sessions).
- Large builds on constrained hosts: declare scratch, timeout, resource
  budget and cleanup before launching; cap `--jobs`; clean only the owned
  build directory.
- Make the binary addressable for later commands:
  `FITCTL_BIN="$FITCTL_INSTALL_ROOT/bin/fitctl"` or prepend its bin dir to
  PATH for the session.

### B. Exact public source (alternative)

```bash
git clone --branch v0.8.0 --depth 1 https://github.com/tznurmin/fitctl.git .tools/fitctl-source-0.8.0
git -C .tools/fitctl-source-0.8.0 rev-parse HEAD   # require the 1ec8777d... v0.8.0 revision
# same block as above with:
#   cargo install --path .tools/fitctl-source-0.8.0/crates/fitctl-cli --locked --root "$FITCTL_INSTALL_ROOT" --jobs 3
```

The skill's procedures must not depend on this checkout existing.

## Post-install configuration (no checkout needed)

```bash
fitctl config list
fitctl config export --out-dir fitctl-config
mkdir -p reports
```

Run these in a working directory outside the skill directory (the skill
tree is the publication tree; exported config is upstream-licensed data).

Use paths under `fitctl-config/configs/` for policies/service profiles.
Python's `builtin_config()` exposes matching built-in dictionaries for
categories `policy`, `service_profiles`, `extensions`,
`invocation_contexts` (ids include the `.json` suffix). A profile's
filename and its `profile_id` can differ — never derive identity from the
filename.
