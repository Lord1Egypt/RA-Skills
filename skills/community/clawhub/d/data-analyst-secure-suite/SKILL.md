---
spec: usk/3.0
id: data-analyst-secure-suite
version: 1.4.0
name: Secure Data Analyst Skill Suite
description: A secure data analysis workflow suite based on MGC Blackbox 1.5.4+, providing credential protection, zero-exposure script & workflow application, workflow / skill-package sealed-authorization collaboration, and knowledge management. Supports 1.5.4 double-layer encryption with link authorization, free-mode sealing, and cross-folder workflow auto-recognition. Includes a Data Analyst Agent system prompt template.
author: MirginCipher Team
license: MIT
tags:
  - security
  - data analysis
  - mgc
  - zero-exposure
  - local sandbox
  - credential management
  - workflow management
  - sealed collaboration
  - knowledge management
  - agent template
  - fuzzy search
  - auto-recognized workflow
  - sealed cross-script
  - double-layer encryption
  - link authorization
  - free mode
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
files:
  skill: SKILL.md
  readme: README.md
  agent_template: agent_system_prompt.md
  prompts:
    - prompts/credential_management.md
    - prompts/script_management.md
    - prompts/collaboration_management.md
    - prompts/knowledge_management.md
changelog:
  - version: 1.4.0
    changes:
      - Upgraded for MGC 1.5.4: the sealing chain now uses double-layer encryption, with new ext07 source binding and ext09 sealing-mode fields.
      - Added free mode: omit ext04 to seal, suitable for publicly distributed analysis workflows and skill packages.
      - Added the "link authorization" chapter: ext07 / ext09 tamper-detection mechanism with a hands-on verification procedure.
      - Fixed factual error: mgc_run must carry diff_3 for workflows, otherwise AMBIGUOUS_SCRIPT is raised.
      - Fixed factual error: output_dir is required for mgc_seal_package and mgc_package since 1.5.4.
      - Fixed factual error: mgc_find no longer accepts info_type since 1.5.0.
      - Fixed factual error: reading SKILL.md inside a workflow package requires info_type="text", not "file".
      - Fixed factual error: the record identity after importing a .mgc_file comes from the package manifest, not from the caller's info_owner.
      - Documented the cross-folder workflow auto-recognition capability added in 1.5.4.
      - Documented receiver version requirements: sealed packages need MGC 1.5.4+, ext08 auto-workflows need MGC 1.5.2+.
      - Added the two new tools mgc_delete and mgc_skill; the MCP tool list is now complete at 12.
      - Frontmatter upgraded to the usk/3.0 spec: requirements.mgc_version, block-list tags, full mcp_tools.
      - manifest now carries the spec / requirements / files fields.
      - Unified the version statement across all documents to MGC Blackbox 1.5.4+.
      - Fixed the chapter-numbering gap (six) in the knowledge management document and the duplicated README title.
  - version: 1.3.0
    changes:
      - Upgraded for MGC 1.5.2+: added mgc_save_file (workflow folder storage), mgc_seal_package (workflow sealing), mgc_package (plaintext packaging).
      - Script management refactor: upgraded from single-script to workflow-folder mode, with import / from-import / relative-path / subprocess auto-recognition.
      - Credential management: unified info_type from 'credential' to 'token' to align with skill_spec.
      - Added prompts/collaboration_management.md: dedicated workflow / skill-package sealed-authorization guide.
      - Agent template: workflow examples upgraded from 5-step manual chain to find → save_file → run pattern.
      - Added sealed-collaboration chapter (mgc_seal_package one-click seal of an entire workflow).
      - Added recognizable cross-script patterns table (from-import / import / Path / subprocess).
      - MCP tools list expanded to 10 (added mgc_save_file, mgc_seal_package, mgc_package).
  - version: 1.2.0
    changes:
      - Synced with MGC Blackbox 1.4.10: added mgc_find (fuzzy search) and mgc_run (preferred over mgc_get action=run).
      - Script management: replaced mgc_get(action='run') with dedicated mgc_run tool.
      - Script management: added mgc_find workflow for locating scripts by name.
      - Script sealing: clarified ext04 must be a multi-line PEM public key.
      - Credential management: added mgc_find workflow.
      - Knowledge management: added mgc_find workflow.
      - Agent system prompt: documented the find -> get/run workflow pattern.
  - version: 1.1.1
    changes:
      - Optimized documentation structure per review report
      - Added 'Anti-patterns and pitfalls' chapter
      - Added 'Complete use cases' chapter
      - Unified prompt file-name references
  - version: 1.1.0
    changes:
      - Consolidated prompts into three core modules: credential, script, knowledge management
      - Added agent_system_prompt.md as a Data Analyst Agent system-prompt template
      - Strengthened document structure and clarified each module's scenario and invocation
  - version: 1.0.0
    changes:
      - Initial release
---

# Overview

**Secure Data Analyst Skill Suite** is a documentation skill suite built on **MGC Blackbox 1.5.4+** that helps data analysts securely manage, on the local machine:

- Sensitive credentials
- User-owned scripts and workflows
- Workflow / skill-package sealed-authorization collaboration
- Analysis frameworks and knowledge

This suite uses a **hybrid design**:

- **Skill prompts (under `prompts/`)**: four core capabilities — credential management, workflow management, sealed-collaboration, knowledge management
- **Agent system-prompt template (`agent_system_prompt.md`)**: builds a Data Analyst Agent that obeys strict security boundaries

All sensitive operations require explicit user authorization. This suite provides no automated data-access capability.

---

# Scenarios

This suite is suitable for:

- In-house enterprise data analysis
- Scenarios requiring sensitive-data protection
- Secure sharing of scripts / workflows in team collaboration
- Safe use of vendor scripts
- Building a secure Data Analyst Agent
- Building a knowledge accumulation system (can pair with a Self-Improving Agent)

---

# Prerequisites

1. Install MGC Blackbox (≥ 1.5.4):
   ```
   pip install mgc-blackbox>=1.5.4
   ```
2. Start the MGC service:
   ```
   mgc
   ```
   WebUI: `http://127.0.0.1:57218`　API: `http://127.0.0.1:57219`
3. Available MCP tools (12):
   `mgc_save`, `mgc_save_file`, `mgc_get`, `mgc_run`, `mgc_find`, `mgc_list`, `mgc_seal`, `mgc_seal_package`, `mgc_package`, `mgc_delete`, `mgc_open_webui`, `mgc_skill`
4. Token file: `~/.mgc/database/mgc_black_box/.mgc_token`

> **Version requirement**: the receiving node must run **MGC 1.5.4+**. Earlier versions cannot unseal a sealed package that carries link authorization, and will fail with a link-authorization error.
> **Workflow auto-recognition**: a workflow package carrying an `ext08` call graph requires the receiver to run **MGC 1.5.2+**. Older versions can still import the package, but cross-script calls will not be routed through sealed execution, and MGC returns a `TARGET_NODE_MAY_NOT_SUPPORT_AUTO_WORKFLOW` warning.
> **Sandbox mode (1.4.9+)**: when running inside a sandbox agent (Trae Work / WorkBuddy), install MGC into the system environment — otherwise MCP tool calls may be blocked. In that case, call the FastAPI directly.

---

# Core capabilities

## 1. Credential management (`credential_management.md`)

Securely manage sensitive credentials such as database keys and API tokens.

### Scenarios
- Need to connect to databases or external services
- Scripts need safe access to credentials
- Team members share database/service **access rights** (not the data itself)
- Team members share **analysis methods and scripts** across the team and outside (via workflow sealed authorization)

### What it provides
- Local encrypted storage
- AI never sees credential content
- Scripts can call credentials with zero exposure
- All accesses require user authorization

### How the agent uses it
After user authorization, the agent reads credentials but never sees plaintext.

---

## 2. Workflow management (`script_management.md`)

Manage user-owned query / clean / analyze scripts — both single-script and workflow-folder modes.

### Scenarios
- User wants to apply their own scripts or workflows
- Scripts need safe access to credentials
- Multi-script workflows need auto-recognition of import / subprocess call relationships (1.5.1+, including 1.5.4 cross-folder recognition)
- Workflows need cross-team collaboration (sealed)
- Need to build a complete data-analysis chain (query → clean → analyze)

### What it provides
- Single-script encrypted storage (`mgc_save`)
- Workflow-folder encrypted storage with auto-recognition of import / subprocess (`mgc_save_file`)
- AI never sees script content
- Scripts call credentials with zero exposure
- Supports single-script sealing (`mgc_seal`) and workflow sealing (`mgc_seal_package`)
- All applications require user authorization

### How the agent uses it
After user authorization, the agent runs scripts or workflows through MGC. In workflow mode, MGC auto-recognizes the import chain — no manual parameter chaining needed.

---

## 3. Sealed-authorization collaboration (`collaboration_management.md`)

Seal-authorize workflows and skill packages to other nodes, enabling "usable but not readable, runnable but not resellable" cross-team / cross-organization collaboration.

### Scenarios
- Data team seals an analysis workflow to a business team (run only, no source access)
- Vendor analyst seals an analysis solution to a client
- Cross-department sharing of analysis methodologies while protecting core logic
- Independent license per client
- Public distribution of a general-purpose analysis workflow (free mode)

### What it provides
- Workflow sealing (`mgc_seal_package`): seal the entire workflow in one call; the script portion is double-layer encrypted
- Skill-package sealing: seal a complete skill package (with SKILL.md); receiving AI can read the instructions but cannot see source code
- Node binding (p2p mode): the key is bound to the target node's RSA public key, so the package cannot be re-sealed for a third party
- Free mode (free mode): omit `ext04` — no public-key exchange needed, and any 1.5.4+ node can import and run it
- Link authorization: the sealed package binds the source node and the sealing mode; tampering with `ext07` / `ext09` makes it unsealable
- One-key-per-node: each client receives an independent key
- No cloud: all encryption / decryption / execution happens locally

### How the agent uses it
After user authorization, the agent performs the sealing operation. The sealed package is delivered by the user manually — the agent does not participate in transport.

---

## 4. Knowledge management (`knowledge_management.md`)

Manage knowledge assets: analysis frameworks, prompt templates, methodologies, business rules, and more.

### Scenarios
- Build standardized analysis frameworks
- Reuse prompt templates
- Share analysis methods across the team
- Build a knowledge accumulation system
- Pair with a Self-Improving Agent for automatic knowledge capture

### What it provides
- Encrypted storage of knowledge content
- Agent reads knowledge with explicit user authorization
- Knowledge sealed collaboration supported
- Used to build analysis-report structure

### How the agent uses it
After user authorization, the agent reads knowledge and uses it to guide analysis structure or generate prompts.

---

# 1.5.4 Sealing Security Model

## Double-layer encryption structure

Since 1.5.4 every sealing goes through the double-layer chain:

```
Layer 1: content  = AES-256-CBC(script body, one-time AES_KEY_4)
Layer 2: AES_KEY_4 = RSA-2048 encryption (p2p: target node public key / free mode: shared default public key)
Layer 3: ext03    = AES-256-GCM(Layer-2 result, key = SHA256(ext07)[:32], AAD = ext09)
```

The Layer-3 key is derived from `ext07` (source node public key), and `ext09` (sealing mode) is bound as the AAD — this is where link authorization comes from.

## Two sealing modes

Whether `ext04` is passed determines the sealing mode:

| | p2p mode (default) | free mode |
|---|---|---|
| How to seal | Pass `ext04=<target node multi-line PEM>` | **Omit** `ext04` |
| Resulting ext09 value | `p2p mode` | `free mode` |
| Who can unseal and run it | Only the node holding the matching private key | **Any MGC 1.5.4+ node** |
| Is the source script readable | No | No (decrypted in memory only) |
| Does it need public-key exchange | Yes | **No** |
| Best for | Per-customer authorization, confidential delivery | Public distribution, skill marketplaces, general install packages |

> Free mode suits "give the general-purpose analysis tool to everyone". It is **not** suitable when authorization must be differentiated per customer.
> The parameter name must be `ext04`. Writing it as `node_pub` / `target_pub` / `public_key` etc. immediately raises `UNKNOWN_PARAM` — there is no silent downgrade.

## Link authorization

Every sealed artifact produced in 1.5.4 carries the source node identity (`ext07`) and the sealing mode (`ext09`). On unsealing, MGC validates them in order:

1. Derive the outer key `SHA256(ext07)[:32]` from `ext07`
2. Use `ext09` as the AAD to verify ciphertext integrity
3. On failure → `UNSEAL_FAILED`

Therefore **any change to `ext07` or `ext09` (even adding a single space) makes the artifact unsealable**.

### Hands-on verification

The following steps can be completed on a single machine, no second node required. **Verifying with a single-script capsule is the most direct route** — the capsule is a self-describing JSON file, so fields are easy to edit:

```python
# 1. Seal a single script to produce a self-describing capsule
sealed = mgc_seal(
    info_owner="my_script",
    output_dir="/tmp/probe",
)
# → /tmp/probe/my_script_<YYYYMMDD_HHMMSS>/sealed_capsule.json
```

```python
# 2. Tamper with ext09: add a trailing space to the ext09 value in the capsule JSON, save as tampered.json
```

```python
# 3. Import the tampered artifact and run it
mgc_save_file(path="/tmp/probe/tampered.json", info_owner="probe_tampered")
mgc_run(info_owner="probe_tampered", diff_3="my_script")
```

Observed result:

```
Error: UNSEAL_FAILED
→ Hint: Double-layer unseal failed: AES-GCM auth tag mismatch:
        source_node_pub (ext07) or mode (ext09) tampered, or wrong key.
```

For a workflow package (`.mgc_file`), `ext09` lives in the record inside the package's `MGCFILE.json` — a zip entry, so the same tamper test requires unzipping, editing, and re-packing. The mechanism is identical; only the carrier differs.

Decrypting with a mismatched private key yields `Double-layer unseal failed: Incorrect decryption` — this is exactly the node-binding effect of p2p mode.

> `ext07` is a plaintext identifier in the artifact, not a signature. It provides tamper detection and key binding; it does not replace identity verification. The receiver should still verify the source node public key through a trusted channel.

---

# Security boundary

## This suite provides

- Local encrypted credential storage
- Zero-exposure application of user-owned scripts
- Workflow auto-recognition and sealed routing (including cross-folder subprocess calls)
- Sealed-authorization collaboration for workflows / skill packages (p2p mode and free mode)
- Verifiable artifact integrity thanks to link authorization
- Knowledge encryption management

## This suite does NOT provide

- Automated data access
- Automated cleaning or analysis
- Automated transport
- Script generation or modification

All scripts must be user-provided and comply with organizational policy.

> **Scope of the guarantee**: MGC protects **content confidentiality**. After unsealing, the script runs with the permissions of the user running it; which commands it invokes, which files it reads or writes, and which network endpoints it reaches are all outside MGC's control — those behaviors are the script author's responsibility.

---

# File structure

```
data-analyst-secure-suite/
├── SKILL.md                    # main document (this file)
├── README.md                   # detailed usage guide
├── manifest.json               # skill metadata
├── agent_system_prompt.md      # Agent system-prompt template
└── prompts/
    ├── credential_management.md    # credential management
    ├── script_management.md        # workflow & script management
    ├── collaboration_management.md # sealed collaboration
    └── knowledge_management.md     # knowledge management
```

---

# Usage modes

## Mode 1 — Skill mode

The AI can read the four core prompts under `prompts/`:

| Document | When to use | Triggered by |
|----------|-------------|--------------|
| `credential_management.md` | Need to store or access credentials | user or agent |
| `script_management.md` | Need to store or run a script/workflow | user or agent |
| `collaboration_management.md` | Need to seal a workflow / skill package to another node | user or agent |
| `knowledge_management.md` | Need to store or read knowledge | user or agent |

The AI cites the matching document on user request and asks for authorization before every sensitive operation.

---

## Mode 2 — Agent template mode

Set `agent_system_prompt.md` as the system prompt for an AI Agent.

The agent will automatically enforce:

- Request user authorization before every sensitive operation
- Only apply scripts or workflows through MGC Blackbox
- Never view script content or credentials
- Never automate workflow execution
- Never auto-select a script name (`info_owner` must be supplied by the user)

After authorization, the agent may cite documents under `prompts/` as workflow guidance.

---

# MCP tools reference

| Tool | Description | Authorization required |
|------|-------------|------------------------|
| `mgc_save` | Store credentials, single scripts, prompts | yes |
| `mgc_save_file` | Store workflow folders (auto-recognize import / subprocess); import `.mgc_file` sealed packages | yes |
| `mgc_get` | Retrieve a value / fetch node_pub / read a file inside a package | yes |
| `mgc_run` | Run a script or workflow (black-box) | yes |
| `mgc_find` | Fuzzy-search entries by name (**does not accept info_type**) | optional |
| `mgc_list` | List stored entries | optional |
| `mgc_seal` | Seal a single script (produces a self-describing capsule file) | yes |
| `mgc_seal_package` | Seal an entire workflow folder (produces `.mgc_file` + README) | yes |
| `mgc_package` | Plaintext export of a folder (archive within the same trust zone) | yes |
| `mgc_delete` | Delete stored records (folder deletion requires a second user confirmation) | yes |
| `mgc_open_webui` | Open MGC WebUI | no |
| `mgc_skill` | Read the official MGC skill documentation | no |

---

# Security notes

1. **Zero exposure**: scripts and credentials execute locally; the AI receives only run status
2. **Encrypted storage**: all content encrypted at rest
3. **No plaintext leak**: the AI never sees script or credential content
4. **Auto-recognized workflows**: import / from-import / relative-path / subprocess call chains auto-routed; nothing lands on disk; 1.5.4 adds cross-folder subprocess call support
5. **Sealed workflows / skill packages**: entire workflow or skill package sealed to the target node in one call; node-bound; cannot be resold
6. **Free mode available**: omit `ext04` for free mode — any 1.5.4+ node can import and run it, and the source code remains unreadable
7. **Link authorization**: a sealed package whose `ext07` / `ext09` was tampered with cannot be unsealed, so artifact integrity is verifiable
8. **Deletion requires confirmation**: when `mgc_delete` removes folder-level records, the user must explicitly approve first — only then may the caller pass `confirm_folder_delete="true"`

---

# Contact

- Issues: https://github.com/zkeviny/MGC-Blackbox/issues
- Email: mirgincipher@outlook.com

---

> **Reminder**: This suite is for secure workflow management. All sensitive operations must have explicit user authorization. All scripts are user-owned; all execution happens locally through MGC Blackbox.

---
