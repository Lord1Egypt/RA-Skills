# Cross‑Device Encrypted Script Authorization (Zero‑Exposure)

A documentation skill for **zero‑exposure cross‑device script authorization** built on MGC Blackbox 1.5.4.

## What This Skill Is

Cross‑Device Encrypted Script Authorization teaches how to:

- Seal scripts using the target node's RSA public key and deliver them as ciphertext capsules
- Also support a key‑exchange‑free **free mode** for public distribution
- Run sealed scripts on the authorized node via **blackbox execution** (`mgc_run`) — the source never uploads plaintext
- Verify the origin of an artifact through **link authorization**
- Build cross‑device trust chains

## Prerequisites

- Python 3.10+
- Install: `pip install mgc-blackbox>=1.5.4`
- Start MGC: `mgc` (API port 57219, WebUI port 57218)
- Two MGC nodes (one owner, one authorized; a single node can self-verify)

> The receiver must run **MGC 1.5.4+** — earlier versions cannot unseal artifacts carrying link authorization.

## Two Sealing Modes

Whether `ext04` is supplied decides the seal mode:

| | p2p mode (default) | Free mode |
|---|---|---|
| How to seal | Supply `ext04=<target node multi-line PEM>` | **Omit** `ext04` |
| `ext09` value in the artifact | `p2p mode` | `free mode` |
| Who can unseal and run it | Only the node holding the matching private key | **Any MGC 1.5.4+ node** |
| Can the source script be read | No | No (it is still only decrypted in memory) |
| Public key exchange needed | Yes | **No** |
| Best for | Single-customer authorization, confidential delivery | Public distribution, skill marketplaces, generic installers |

## Quick Start

### 1. Get Target Node Public Key (p2p mode only)

```python
# MCP/API lazy generation
node_pub = mgc_get(
    info_type="__NODE_PUB__",
    info_owner="__NODE_PUB__"
)
```

Or via WebUI: skill page → Settings → **Node Public Key** → copy the multi-line PEM.

> `node_pub` must be a **multi-line PEM** with real newlines (`\n`); do not concatenate into a single line.

### 2. Seal the Script (Owner Node)

```python
# Store the original script first
mgc_save(
    info_type="script",
    info_owner="my_script",
    ext01="python",
    content="print('Confidential script')"
)

# Seal, producing a capsule file
sealed = mgc_seal(
    info_owner="my_script",
    output_dir="/abs/path/to/out",   # required since 1.5.4, no desktop fallback
    ext04=node_pub,                  # free mode: delete this line
)
# → /abs/path/to/out/my_script_<timestamp>/sealed_capsule.json
# The capsule carries content / ext01..ext09, with ext07 = owner node public key and ext09 = seal mode
```

### 3. Transfer the Sealed Artifact

Hand the whole `sealed_capsule.json` file to the receiver — email / USB / IM, any channel works.

### 4. Authorized Node Imports and Executes

```python
# On the authorized node: one call imports it, MGC parses every field automatically
mgc_save_file(
    path="/path/to/send/sealed_capsule.json",
    info_owner="partner_script"     # use your own owner, so you don't overwrite the source record on the owner node
)

# Blackbox execution
result = mgc_run(
    info_type="script",
    info_owner="partner_script",
    diff_3="partner_script",        # the most reliable locator
    ext02='["--name", "Alice"]'     # optional: runtime override of default args
)
# Returns: {"status": "started"}
```

> **Never hand-copy fields one by one** (`ext01` / `ext02` / `content` / `ext03`) — that drops `ext07` and `ext09`, and the artifact will never unseal.

## Link Authorization

Since 1.5.4 every sealed artifact carries the owner node's identity (`ext07`) and the seal mode (`ext09`). At unseal time MGC derives the outer key from `ext07` and uses `ext09` as the AAD for integrity validation, so **any modification to either one makes the artifact unrestorable** — including a single added space.

Measured results:

| Scenario | Result |
|---|---|
| Tampering with `ext09` by adding a space | `UNSEAL_FAILED: AES-GCM auth tag mismatch` |
| Decrypting with a mismatched private key | `Double-layer unseal failed: Incorrect decryption` |
| Normal import and execution | `{"status": "started"}` |

> `ext07` is a plaintext identifier rather than a signature. It detects tampering and binds the unseal key, and does not replace identity verification. The receiver should still verify the owner node's public key through a trusted channel.

## Use Cases

| Use Case | Description |
|----------|-------------|
| Cross‑Organization Sharing | Share scripts without exposing logic |
| Trusted Partner Automation | Provide automation to partners securely |
| Delegated Task Execution | Central server delegates to edge devices |
| Public Distribution | Free mode, no key exchange, runnable on any 1.5.4+ node |

## MCP Tools

| Tool | Description | Required Parameters |
|------|-------------|---------------------|
| `mgc_save` | Store the original script / pass capsule JSON directly | info_type, info_owner, content |
| `mgc_save_file` | Import a capsule by path (**recommended**) / import a folder / import `.mgc_file` | path, info_owner |
| `mgc_seal` | Seal a single script, producing a capsule file | info_owner, **output_dir** (p2p additionally needs ext04) |
| `mgc_run` | Blackbox execution | info_type=script, info_owner (`diff_3` is the most reliable) |
| `mgc_get` | Fetch node_pub / fetch credentials | info_type, info_owner |
| `mgc_find` | Fuzzy search | info_owner, match_mode |
| `mgc_list` | List entry metadata | — |
| `mgc_delete` | Delete a stored record (includes a confirmation flow) | info_type, info_owner |
| `mgc_open_webui` | Open WebUI | — |
| `mgc_skill` | Read the official MGC skill documentation | — |

## MGC 1.5.4 Adaptation

- ✅ Sealing now uses **dual-layer encryption**: `ext03`'s outer layer derives its key from `SHA256(ext07)[:32]` and binds `ext09` as AAD
- ✅ **Link authorization**: any modification to `ext07` / `ext09` makes the artifact unrestorable
- ✅ **Free mode**: omit `ext04` for public distribution with no key exchange
- ✅ `output_dir` is now a required sealing parameter, producing a **self-describing capsule file**
- ✅ `mgc_save_file(path=capsule)` imports everything in one call, parsing all ext fields automatically
- ✅ `mgc_run` no longer requires `diff_1`; `diff_3` is the most reliable locator; the `AMBIGUOUS_SCRIPT` error code was added
- ✅ `ext05` dependency list / `ext06` platform list travel with the artifact
- ✅ New `mgc_delete` and `mgc_skill` tools

## Security Boundary

MGC protects **content confidentiality**, not runtime behavior: once unsealed, the sealed script runs with the permissions of the user running it; which commands it invokes, which files it reads or writes, and which network endpoints it reaches are not restricted by MGC — those behaviors belong to the script author. Verify the owner node's public key through a trusted channel before importing.

## Supported Platforms

- Windows
- macOS
- Linux

## Links

- **Main Repository**: https://github.com/zkeviny/MGC-Blackbox
- **Issues**: https://github.com/zkeviny/MGC-Blackbox/issues
- **Contact**: mirgincipher@outlook.com
