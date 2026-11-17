---
spec: usk/3.0
id: cross_node_script_auth
version: 1.3.0
name: Cross‑Device Encrypted Script Authorization (Zero‑Exposure)
description: Zero‑exposure cross‑device script authorization using MGC Blackbox. Scripts are sealed with the target node's RSA public key, delivered as ciphertext, and decrypted only in memory on the authorized node; also supports key‑exchange‑free free mode for public distribution. Adapted to MGC 1.5.4 — dual‑layer encryption, link authorization, and self‑describing capsule delivery.
author: MirginCipher Team
license: MIT
tags:
  - security
  - cross-device
  - encryption
  - zero-exposure
  - mgc
  - authorization
  - seal
  - RSA
  - dual-layer encryption
  - free mode
  - link authorization
  - blackbox execution
platform_compatibility:
  - windows
  - macos
  - linux
mcp_tools:
  - mgc_save
  - mgc_save_file
  - mgc_get
  - mgc_run
  - mgc_find
  - mgc_list
  - mgc_seal
  - mgc_seal_package
  - mgc_package
  - mgc_delete
  - mgc_open_webui
  - mgc_skill
requirements:
  mgc_version: ">=1.5.4"
install: pip install mgc-blackbox>=1.5.4
runtime: mgc
port: 57219
changelog:
  - version: 1.3.0
    changes:
      - Upgraded to MGC 1.5.4: sealing now uses dual-layer encryption, with the new ext09 mode field and ext07 owner binding
      - Rewrote the core concept chapter: from single-layer RSA binding to dual-layer encryption plus link authorization, and added a free-mode comparison table
      - Fixed the sealing flow: ext04 is optional since 1.5.4 (omitting it means free mode); an empty ext04 no longer errors out
      - Fixed the storage flow: switched to mgc_save_file(path=capsule file) for one-shot import, which parses every ext field automatically
      - Fixed the security notes: item 3 ("no other node can decrypt") does not hold in free mode, and item 6 ("integrity is not verified") is outdated
      - Added a Link Authorization chapter covering ext07 / ext09 tampering detection plus a hands-on verification procedure
      - Fixed mgc_run parameters: diff_1 is optional since 1.5.4, diff_3 is the most reliable locator, and the AMBIGUOUS_SCRIPT error code was added
      - Fixed the capsule structure: 4 fields became 8 (added ext05 / ext06 / ext07 / ext09), and the legacy underscore keys were dropped
      - Documented ext05 dependency list, ext06 platform list, and the ext10 runnability badge
      - Added the output_dir requirement and the capsule directory layout
      - Fixed broken Windows absolute-path links
      - Neutralized the wording ("the caller" instead of agent-centric phrasing) and restated the security boundary around content confidentiality and responsibility
      - Completed mcp_tools to all 12 tools, adding mgc_delete and mgc_skill
  - version: 1.1.0
    changes:
      - Upgraded to adapt to MGC 1.4.10
      - Replaced mgc_get(action=run) with mgc_run (1.4.7+) for executing sealed scripts
      - Documented ext02 auto-parsing (1.4.10): argparse defaults are bundled into ext_02 during sealing
      - Fixed mgc_seal required parameters: info_type is optional, ext04 must be multi-line PEM
      - Added mgc_find fuzzy search tool
      - Updated node_pub retrieval flow: WebUI Settings → Node Public Key
      - Added update_if_exists for overwriting same-name scripts
      - Added brief note on 1.4.9 sandbox mode
  - version: 1.0.1
    changes:
      - Clarified lazy generation mechanism differences for node_pub (MCP/API vs WebUI)
  - version: 1.0.0
    changes:
      - Initial release for cross-device encrypted script authorization
---

# Overview

Cross‑Device Encrypted Script Authorization is a documentation skill that teaches how to **authorize script execution across devices without exposing plaintext**.

This skill enables:
- Seal scripts using the target node's RSA public key and deliver them as ciphertext
- Also support a key‑exchange‑free **free mode** for public distribution
- Run sealed scripts on the authorized node via **blackbox execution**
- Verify the origin of an artifact through **link authorization**

This skill contains **no executable code** and is safe for automatic approval.

---

# What This Skill Enables

After reading this documentation, the caller will understand how to:

- Fetch the target node's RSA public key (`__NODE_PUB__`)
- Seal scripts via `mgc_seal` (with auto-extracted default arguments), producing a deliverable capsule file
- Choose the authorization mode: p2p (bound to a specific node) or free mode (runnable on any 1.5.4+ node)
- Import the capsule on the target node with a single call (all fields parsed automatically)
- Execute the sealed script in blackbox mode via `mgc_run`
- Verify artifact origin integrity (tamper detection on `ext07` / `ext09`)
- Handle dependency consistency (credentials, files, environment variables)

---

# Prerequisites

1. **Install MGC Blackbox**: `pip install mgc-blackbox>=1.5.4`
2. **Start MGC service**: `mgc` (runs at http://127.0.0.1:57219, WebUI at 57218)
3. **MCP tools available**: `mgc_save`, `mgc_save_file`, `mgc_get`, `mgc_run`, `mgc_seal`, `mgc_find`, `mgc_list`, `mgc_delete`, `mgc_open_webui`, `mgc_skill`
4. **Two MGC nodes**: One owner node and one authorized node; a single node can self-verify the flow
5. **Token file**: `~/.mgc/database/mgc_black_box/.mgc_token`

> **Version requirement**: the receiver must run **MGC 1.5.4+**. Earlier versions cannot unseal artifacts carrying link authorization.
> **Sandbox mode (1.4.9+)**: When running inside a sandbox Agent (Trae Work / Workbuddy), install MGC in the system environment; otherwise MCP tool calls may be intercepted — in that case, call FastAPI directly.

---

# Core Concept

## Why Cross‑Device Authorization?

```
Traditional: Script Owner → Send Script (plaintext) → Authorized Node
MGC Way:    Script Owner → Seal → Ciphertext Capsule → Authorized Node
                                        ↓
                            Always encrypted, never exposed
```

The script remains encrypted throughout:
- After sealing on the owner node
- During network transfer
- During storage on the authorized node
- Decrypted only briefly in memory during blackbox execution

## The 1.5.4 Dual‑Layer Encryption Structure

Since 1.5.4 every seal goes through the dual-layer path:

```
Layer 1: content   = AES-256-CBC(script body, one-time AES_KEY_4)
Layer 2: AES_KEY_4 = RSA-2048 encryption (p2p: target node public key / free mode: shared default public key)
Layer 3: ext03     = AES-256-GCM(layer 2 result, key = SHA256(ext07)[:32], AAD = ext09)
```

The layer-3 key is derived from **ext07 (owner node public key)** and the AAD binds **ext09 (seal mode)** — this is exactly where link authorization comes from.
The layer-1 `AES_KEY_4` is freshly randomized on every seal and never reused across artifacts.

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

Free mode wraps the content with MGC's shared default public key, so **any machine running MGC 1.5.4+ can import and run it**, while the source script still never lands on disk in plaintext at the receiving side.

> Free mode fits "hand everyone a runnable trial build". It is **not** suitable when authorization must be limited per customer.

## Sealed Capsule Structure (measured on 1.5.4)

```
{
  "info_type":  "script",
  "info_owner": "my_script",
  "ext01":      "python",                    // startup command
  "ext02":      '["--name", "World"]',       // default args (argparse auto-parsed at seal time)
  "ext03":      "<dual-layer wrapped ciphertext>",  // sealing key
  "ext05":      "[]",                        // third-party dependency list (auto-detected)
  "ext06":      '["windows","macos","linux"]',// compatible platform list (statically inferred)
  "ext07":      "<owner node RSA public key>",     // origin identity, participates in key derivation
  "ext09":      "p2p mode",                 // seal mode
  "content":    "<AES-encrypted script body>"
}
```

Key points:

- Field keys carry **no underscore** (`ext01`, not `ext_01`)
- `ext07` and `ext09` **must travel with the artifact**; if either is missing, it can never be unsealed
- `ext05` / `ext06` are pre-run hints — MGC does **not** install dependencies for you

---

# Use Cases

## Use Case 1: Cross‑Organization Script Sharing

Organization A wants to share scripts with Organization B without exposing script content.

1. Organization B installs MGC and provides its `node_pub`
2. Organization A seals the script with `node_pub` (p2p mode)
3. Organization B imports the capsule and executes it

## Use Case 2: Trusted Partner Automation

A company wants to deliver automation scripts to partners without revealing the script logic.

1. Partner installs MGC and provides `node_pub`
2. Company seals the script with the partner's `node_pub`
3. Partner runs the sealed script locally in blackbox mode

## Use Case 3: Delegated Task Execution

A central server delegates tasks to edge devices without exposing task logic.

1. Edge device provides `node_pub` to the central server
2. Central server seals the task script
3. Edge device executes the sealed task

## Use Case 4: Public Distribution (Free Mode)

When the script must reach an unknown audience, or be published on a skill marketplace:

1. The owner node seals **without `ext04`**
2. The artifact can be placed on a public channel
3. Any node running MGC 1.5.4+ can import and run it; the source script never lands on disk

---

# Workflow

## Step 1: Get Target Node Public Key

Only needed for p2p mode. Free mode can skip this step.

The target node (the node that runs the sealed script) must provide its RSA public key.

**Option A: Trigger lazy generation via MCP/API**
```python
# Fetch node public key via MCP (auto-generates keypair on first call)
node_pub = mgc_get(
    info_type="__NODE_PUB__",
    info_owner="__NODE_PUB__"
)
```

**Option B: View via WebUI (1.4.7+)**
Open WebUI → skill page → Settings dropdown → **Node Public Key** → Copy multi-line PEM.
On Safari the browser will download a `.pem` file instead.

> **Critical requirement**: `node_pub` **must** be a **multi-line PEM** with real newlines:
> ```
> -----BEGIN PUBLIC KEY-----
> MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA...
> ...(base64 lines)...
> -----END PUBLIC KEY-----
> ```
> Single-line concatenation triggers MGC's "Invalid PEM format" error; copy verbatim from the `mgc_get` response.

## Step 2: Seal Script on Owner Node

Store the original script first, then seal it. Sealing produces a **self-describing capsule file**.

```python
# 1. Store the original script first (ext01 required; ext02 optional — MGC auto-parses argparse)
mgc_save(
    info_type="script",
    info_owner="my_script",
    ext01="python",
    content="import argparse\nparser = argparse.ArgumentParser()\nparser.add_argument('--name', default='World')\nargs = parser.parse_args()\nprint(f'Hello {args.name}')"
)

# 2. Seal
sealed = mgc_seal(
    info_owner="my_script",        # required: script identifier to seal
    output_dir="/abs/path/to/out", # required: since 1.5.4 there is no desktop fallback, an absolute path must be given
    # p2p mode: pass the target node public key; free mode: drop this line entirely
    ext04=node_pub
)

# sealed contains:
#   capsule_path  absolute path of the capsule file
#   content / ext01..ext09        the complete self-describing artifact
```

> **`output_dir` is required since 1.5.4** — there is no default location. The artifact lands in
> `<output_dir>/<info_owner>_<YYYYMMDD_HHMMSS>/sealed_capsule.json`.

> **Free mode**: delete the whole `ext04` line; all other parameters stay the same.

> **The parameter name must be `ext04`**: writing `node_pub` / `target_pub` / `public_key` and other aliases
> fails immediately with `UNKNOWN_PARAM`, so you never mistake a free-mode artifact for a node-bound one.

## Step 3: Transfer the Sealed Artifact

Hand the whole `sealed_capsule.json` file pointed to by `capsule_path` to the receiver — any channel (email / USB / IM) works.

```python
import shutil
shutil.copy(sealed["capsule_path"], "/path/to/send/sealed_capsule.json")
# Or paste the JSON file content to the receiver directly
```

> The artifact is ciphertext, but **its integrity is guaranteed by link authorization** (see the "Link Authorization" chapter). A trusted channel is still recommended.
> When forwarding, `ext07` / `ext09` must be **passed through verbatim**; any edit makes it unrestorable.

## Step 4: Import the Artifact on the Authorized Node

**A single call is enough** — MGC recognizes the capsule and parses out every field:

```python
# On the authorized node (recommended: path import, fewest parameters, type inferred automatically)
mgc_save_file(
    path="/path/to/send/sealed_capsule.json",
    info_owner="partner_script"     # use your own owner, so you don't overwrite the source record on the owner node
)
```

You can also pass the JSON directly:

```python
mgc_save(
    info_type="script",             # required by this tool's schema, even though the capsule repeats it
    info_owner="partner_script",
    content=capsule_json_string     # the whole capsule JSON, verbatim
)
```

> **Never hand-copy fields one by one** (`ext01` / `ext02` / `content` / `ext03`) — that drops `ext07` and `ext09`,
> and the artifact can then be stored but will **never unseal**.

> **Choosing the owner**: the `info_owner` inside the capsule belongs to the owner node. Storing it under the same owner on the *same* node **overwrites the source record**; on a *different* node the owner node is unaffected. Supplying your own owner keeps both copies.

## Step 5: Execute the Sealed Script (Blackbox)

```python
# ✅ 1.5.4 recommended: use mgc_run
result = mgc_run(
    info_type="script",
    info_owner="partner_script",
    diff_3="partner_script",          # most reliable locator: the script's relative path / file name
    ext02='["--name", "Alice"]'       # optional: runtime override of default args (JSON array string)
)
# Returns e.g.: {"status": "started"}
# The caller only gets the start status; script content is never exposed
```

> **`diff_1` is no longer required since 1.5.4**. Prefer `diff_3` (most precise), then `diff_2` (folder name).
> If multiple records match under the same owner, MGC returns `AMBIGUOUS_SCRIPT` — list the candidates with `mgc_find` first, then retry.

> **Execution output**: `mgc_run` returns only the start status, not stdout. For detailed results, the sealed script should write results to a file and print the path on stdout (see the "Dependency Requirements" chapter).

## Step 6: (Optional) List / Find Sealed Scripts

```python
# Fuzzy search (1.4.10+)
scripts = mgc_find(
    info_owner="partner",
    match_mode="substring",          # substring / prefix / suffix / exact
    limit=50
)
# Returns a metadata list — **never includes content plaintext**
```

---

# Link Authorization

Since 1.5.4 every sealed artifact carries the owner node's identity (`ext07`) and the seal mode (`ext09`). Together they form **link authorization**.

## How It Works

At unseal time, MGC validates in this order:

1. Derive the outer key `SHA256(ext07)[:32]` from `ext07`
2. Use `ext09` as the AAD to validate ciphertext integrity
3. If validation fails → `UNSEAL_FAILED`

Because key derivation is bound to `ext07` and integrity validation is bound to `ext09`, **any modification to either one makes the artifact unrestorable** — even a single added space.

## Hands‑On Verification Steps

To confirm locally that this mechanism is really in effect, follow these three steps (all on one machine, no second node needed):

```python
# 1. Seal and import
sealed = mgc_seal(info_owner="my_script", output_dir="/tmp/probe")
mgc_save_file(path=sealed["capsule_path"], info_owner="probe_copy")
```

```python
# 2. Tamper with ext09 (append a trailing space) and write a new file
#    Python side: append a space to ext09 in the capsule JSON, save as tampered.json
```

```python
# 3. Import the tampered file and run it
mgc_save_file(path="/tmp/probe/tampered.json", info_owner="probe_tampered")
mgc_run(info_type="script", info_owner="probe_tampered")
```

Measured result:

```
Error: UNSEAL_FAILED
→ Hint: Double-layer unseal failed: AES-GCM auth tag mismatch:
      source_node_pub (ext07) or mode (ext09) tampered, or wrong key.
```

The same principle also enforces "a non-target node cannot unseal": decrypting with a mismatched private key reports
`Double-layer unseal failed: Incorrect decryption`.

## Recommendations

- The receiver should check that `ext07` matches the owner node's public key (verify through a trusted channel)
- Pass `ext07` / `ext09` through verbatim when forwarding — do not edit or reformat them
- `ext07` is a **plaintext identifier in the artifact, not a signature**; it detects tampering and binds the unseal key, and does not replace identity verification

---

# Dependency Requirements

When the sealed script runs on the target node, ensure dependencies are consistent:

| Dependency | How to Handle |
|------------|---------------|
| **MGC credentials** | Target node must store credentials with the same `info_type` / `info_owner`; format consistent but content may vary by node |
| **External files** | Paths must be consistent; recommended to also store in MGC and pull via MGC API at runtime |
| **Environment variables** | Must be set on the target node |
| **Python libraries** | Target node must install the same library versions; at seal time MGC writes the dependency list into `ext05`, but **it does not install them** |
| **Cross-platform differences** | Use `pathlib.Path` or `/` separators; avoid platform-specific APIs. The compatible platform list is written into `ext06` |

> **Important**: Dependency mismatch is the most common cause of sealed script failures. Verify `info_type`/`info_owner`, environment variables, and file paths match between source and target before sealing.

---

# Security Notes

1. **Zero exposure**: the script is encrypted at rest and during transfer, decrypted only in memory on the target node during execution; plaintext never lands on disk
2. **Blackbox execution**: sealed scripts run in MGC's sandbox; the caller cannot see script content
3. **The authorization boundary depends on the mode**: in p2p mode only the node holding the matching private key can unseal; **in free mode any MGC 1.5.4+ node can unseal** — choosing free mode means giving up the "restricted recipient" constraint
4. **Execution right ≠ ownership**: the receiver of a p2p artifact can only execute it; it cannot re-seal the owner node's artifact for a third party
5. **No root protection**: a malicious root can read the decrypted body during execution; ensure the target node is trusted before authorizing
6. **Integrity is now verifiable**: 1.5.4 link authorization detects tampering with `ext07` / `ext09` (see the "Link Authorization" chapter); but this is **origin binding**, not a guarantee about the script's runtime behavior

> **Scope of the guarantee**: MGC protects **content confidentiality**. Once unsealed, the script runs with the permissions of the user running it; which commands it invokes, which files it reads or writes, and which network endpoints it reaches are not restricted by MGC. Those behaviors are the script author's responsibility. Verify the owner node's public key through a trusted channel before importing.

---

# MCP Tools Reference

| Tool | Purpose | Required Parameters |
|------|------|----------|
| `mgc_save` | Store the original script / pass capsule JSON directly | info_type, info_owner, content |
| `mgc_save_file` | Import a capsule by path (**recommended**) / import a folder / import `.mgc_file` | path, info_owner |
| `mgc_seal` | Seal a single script, producing a capsule file | info_owner, **output_dir** (p2p additionally needs ext04) |
| `mgc_run` | Blackbox execution | info_type="script", info_owner (`diff_3` is the most reliable) |
| `mgc_get` | Fetch node_pub / fetch credentials / list all entries | info_type, info_owner |
| `mgc_find` | Fuzzy search | info_owner, match_mode |
| `mgc_list` | List all entries' metadata | — |
| `mgc_delete` | Delete a stored record (includes a confirmation flow) | info_type, info_owner |
| `mgc_open_webui` | Open WebUI | — |
| `mgc_skill` | Read the official MGC skill documentation | — |

## mgc_seal

**Required:** `info_owner`, `output_dir`　**p2p mode additionally needs:** `ext04`

```json
{
  "info_owner": "my_script",
  "info_type": "script",
  "diff_1": "optional",
  "diff_2": "optional",
  "diff_3": "optional",
  "output_dir": "/abs/path/to/out",
  "ext04": "<target node node_pub multi-line PEM; omit for free mode>"
}
```

> **PEM format requirement**: `ext04` must be a multi-line PEM with real newlines (`\n`). If you see "Invalid PEM format", copy the value verbatim from `mgc_get(info_type='__NODE_PUB__')`.

## mgc_run

**Required:** `info_type="script"`, `info_owner`　**Locator:** `diff_3` (most reliable) / `diff_2` (folder name) / `diff_1` (optional)

```json
{
  "info_type": "script",
  "info_owner": "partner_script",
  "diff_3": "partner_script",
  "ext02": "[\"--name\", \"Alice\"]"
}
```

**Returns:** `{ "status": "started" }`

---

# Troubleshooting

| Issue | Solution |
|-------|----------|
| `mgc_seal` reports "Missing required param: output_dir" | Since 1.5.4 `output_dir` is required with no desktop fallback; pass an absolute path |
| `mgc_seal` reports "Unknown param: node_pub" (`UNKNOWN_PARAM`) | The parameter name must be `ext04`; aliases are rejected so you cannot accidentally produce a free-mode artifact |
| `mgc_seal` returns "Invalid PEM format" | `ext04` must be a multi-line PEM with real newlines; copy it verbatim from `mgc_get(info_type='__NODE_PUB__')` |
| Running after import reports `UNSEAL_FAILED: AES-GCM auth tag mismatch` | `ext07` or `ext09` was modified; re-import the original artifact |
| Running after import reports `Double-layer unseal failed: Incorrect decryption` | The current node's private key does not match `ext04` — it is not the designated target node |
| Running after import reports "ext09 is non-empty but ext07 is missing" | `ext07` was lost while moving fields by hand; use `mgc_save_file(path=capsule file)` to import in one call |
| Running reports `AMBIGUOUS_SCRIPT` | Multiple records match the same owner; list the candidates with `mgc_find`, then retry with `diff_3` / `diff_2` |
| `mgc_run` returns "args_not_recognized" | The source script's `argparse` was not recognized; verify `add_argument` usage or pass `ext02` explicitly |
| `mgc_save` returns "dynamic_args_detected" warning | The source script has dynamic defaults (e.g. `datetime.now()`, `os.path.expanduser`); use literal defaults or pass `ext02` manually |
| Target node execution cannot find credentials | The credential `info_type` / `info_owner` differs from the source node; unify the naming before sealing |
| `mgc_run` returns a start status but the script produces no output | Expected: `mgc_run` only returns the start status; the sealed script should write results to a file and print the path on stdout |
| The owner node's source record disappears after import | You imported under the same `info_owner` on the same node, overwriting the source record; use your own owner |
| Target node storage fails on a duplicate name | Add `update_if_exists=true` to overwrite; or check with `mgc_find` and rename |
| A dependency-missing hint appears | `ext05` is a pre-run hint only; MGC does not install anything — set it up manually on the target node |
| WebUI has no node_pub entry | Confirm MGC ≥ 1.4.7; the entry is in the Settings dropdown on the skill page |
| MCP tools unavailable in sandbox mode | Install MGC in the system environment, or call FastAPI directly |

---

# Links

- **Main Repository**: https://github.com/zkeviny/MGC-Blackbox
- **Issues**: https://github.com/zkeviny/MGC-Blackbox/issues
- **Contact**: mirgincipher@outlook.com
