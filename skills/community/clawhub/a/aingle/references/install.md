# Install the Aingle CLI

Install only after the operator explicitly authorizes downloading and running the official CLI.

## Existing installation

Run:

```sh
aingle update --check --json
```

If `update_available` is `true`, run `aingle update` and repeat the check. If the installed executable has no `update` command, replace it with a current verified release.

## New installation

Use only the public [`aingl/aingle-cli`](https://github.com/aingl/aingle-cli) repository and its [latest release](https://github.com/aingl/aingle-cli/releases/latest).

1. Identify the operating system and architecture.
2. Download the matching archive and its adjacent `.sha256` file from the same GitHub release.
3. Calculate the archive's SHA-256 digest locally and require an exact match before extraction.
4. Extract only the Aingle archive.
5. Install `aingle` or `aingle.exe` under the current user's directory, such as `~/.local/bin`.
6. Run `aingle --version` and `aingle update --check --json`.

Do not use administrator elevation, a system directory, an unofficial mirror, or an archive whose checksum is missing or mismatched. Do not disable Gatekeeper, SmartScreen, antivirus, TLS verification, or other security controls.

When no release exists for the current platform, build from the official repository only if Rust 1.93 or newer is already available:

```sh
cargo install --locked \
  --git https://github.com/aingl/aingle-cli \
  --package aingle-cli \
  --root "$HOME/.local"
```

If environment policy blocks installation, stop and report the restriction instead of bypassing it.
