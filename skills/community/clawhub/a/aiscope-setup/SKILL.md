---
name: aiscope-setup
description: Install AIScope and its agent skills, verify the executable, and run a first noninteractive instruction audit. Use for initial setup or a missing AIScope command.
---

# Set up AIScope

Check `aiscope --version` before installing. AIScope is a native Rust CLI; running a released binary does not require Rust, Python, Node.js, an account, or an API key.

Use the current release at https://github.com/Jayanth-MKV/aiscope/releases/latest. Match the OS and CPU: Windows x86_64, macOS x86_64/ARM64, or Linux x86_64/ARM64 with glibc. Download the archive and its `.sha256` file from the same release, compare SHA-256 before extracting, then place the executable in a user-writable directory on PATH. Do not silently install an incompatible architecture or assume Linux musl support.

With Node.js 22+, use `npm install --global aiscope-cli@0.1.2` or `npx --yes aiscope-cli@0.1.2 --version`. The first run downloads a checksum-verified binary; later scans are offline. With Python, use `uv tool install aiscope-cli==0.1.2` or `pip install aiscope-cli==0.1.2`; platform wheels bundle the executable and need no Rust or Node.js. Prefer an existing package manager and avoid global installation unless the user requests it.

If Cargo is available, the alternative is `cargo install aiscope --version 0.1.2 --locked`. A source build requires Rust and a platform linker; consult the repository's installation guide if it fails. Do not replace the user's Rust toolchain to resolve a build failure without agreement.

For standalone skills, use the published repository with the skills CLI:

```sh
npx --yes skills add Jayanth-MKV/aiscope --skill aiscope-setup aiscope --agent codex --copy --yes
```

Replace `codex` with the current agent's identifier. Default to project scope; use `--global` only if the user requests it. If Node.js is unavailable, copy just the two skill directories from the repository's `skills/` folder to the current agent's supported skills directory. Do not overwrite an existing skill without checking it. A plugin already supplies both skills, so skip a duplicate standalone installation.

Verify with `aiscope --version`, then run `aiscope --specific --json .` from the target project. Parse stdout as JSON and confirm its `root` matches the intended directory. Do not launch the TUI or watch mode during setup. Explain scan coverage and any returned conflicts; leave instruction files unchanged unless changes were requested. User-wide instructions require the explicit `--user` opt-in.

Use the exact npm/PyPI package name `aiscope-cli`. The unrelated npm package named `aiscope` is not this tool.
