# Secure Data Analyst Skill Suite

> **Version**: 1.4.0 · **Requires**: MGC Blackbox ≥ 1.5.4

A secure data-analysis workflow suite built on **MGC Blackbox**, providing a hybrid mix of **skill prompts + Agent system-prompt template**, helping data analysts securely manage scripts, workflows, credentials, sealed collaboration, and knowledge on the local machine.

---

## What this suite is

This suite helps data analysts complete data-analysis workflows locally and securely:

- **Database credential security** (zero exposure)
- **Application of user-owned scripts & workflows** (query / clean / analyze)
- **Auto-recognized workflows** (import / from-import / relative-path / subprocess runtime routing, including 1.5.4 cross-folder recognition)
- **Sealed-collaboration on workflows / skill packages** (one-key-per-node, node-bound, no resell, 1.5.4+)
- **Free-mode public distribution** (no public-key exchange; any 1.5.4+ node can import and run)
- **Knowledge management for analysis methods & prompts** (local encrypted storage)
- **Optional Data Analyst Agent template** (auto-enforces the security boundary)

All sensitive operations require explicit user authorization. This suite does not provide any automated data-access capability.

---

## Prerequisites

- Python 3.10+
- Install MGC Blackbox:
  ```
  pip install mgc-blackbox>=1.5.4
  ```
- Start MGC:
  ```
  mgc
  ```
  - WebUI: `http://127.0.0.1:57218` (visual interface)
  - API: `http://127.0.0.1:57219` (API endpoint)
  - Token Required: Header "X-MGC-Token"
  - Token File: `~/.mgc/database/mgc_black_box/.mgc_token`

> **Version requirement**: the receiving node must run **MGC 1.5.4+**. A workflow package carrying an `ext08` call graph additionally needs **MGC 1.5.2+** — with an older version the import still succeeds but cross-script calls are not routed through sealed execution, and MGC returns a `TARGET_NODE_MAY_NOT_SUPPORT_AUTO_WORKFLOW` warning.

---

## Target users

- Data analysts handling sensitive business data
- Teams that need secure script collaboration
- Organizations that need to protect local data assets
- Users building a secure Data Analyst Agent

---

## Workflow overview (secure chain)

```
┌──────────────────────────────────────────────────────────┐
│                Data-analysis workflow                     │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  Credential mgmt → Data query (workflow package)         │
│                  → Data cleaning (auto-routed in package) │
│                                                          │
│  → Data analysis → Result output (file / DB / MGC)        │
│                  → Knowledge accumulation                 │
│                                                          │
│  Optional: seal the whole workflow to another node        │
│            (team / client)                               │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

All scripts are user-owned, all applications happen locally through MGC, and the AI never sees scripts or credentials.

---

## Core components

### 1. Credential management

Users store database credentials through MGC, enabling zero-exposure calls.

**Storing a credential:**
```
info_type: "token"
info_owner: "db_connection_name"
content: encrypted credential (user-owned)
```

**Calling a credential inside a script:** see `prompts/credential_management.md`

The AI never sees credential content.

---

### 2. Workflow management

Users store query / clean / analyze scripts as a workflow folder in MGC. MGC auto-recognizes import / from-import / relative-path / subprocess call relationships and routes execution under sealing.

**Storing a workflow:**
```python
mgc_save_file(
    path="./my_analysis",
    info_owner="monthly_sales_analysis",
)
```

> MGC uses the last segment of the directory name as `diff_2` (i.e. `my_analysis`). After saving, use `mgc_find` to confirm the actual `diff_2`.

**Running a workflow:**
```python
# diff_3 must point at the entry script, otherwise multiple records match
# and MGC returns AMBIGUOUS_SCRIPT
mgc_run(
    info_owner="monthly_sales_analysis",
    diff_2="my_analysis",
    diff_3="run.py",
)
```

Single-script mode (`mgc_save` + `mgc_run`) is also supported — see `prompts/script_management.md`.

---

### 3. Sealed-authorization collaboration

Seal-authorize workflows or skill packages to other nodes, enabling "usable but not readable, runnable but not resellable" cross-team / cross-organization collaboration.

**Two sealing modes:**

| | p2p mode (default) | free mode |
|---|---|---|
| How to seal | Pass `ext04=<recipient public key>` | **Omit** `ext04` |
| Resulting ext09 value | `p2p mode` | `free mode` |
| Who can unseal and run it | Only the node holding the matching private key | **Any MGC 1.5.4+ node** |
| Does it need public-key exchange | Yes | **No** |
| Best for | Per-customer authorization, confidential delivery | Public distribution, general install packages |

**Sealing a workflow:**
```python
mgc_seal_package(
    info_owner="monthly_sales_analysis",
    diff_2="my_analysis",
    output_dir="./delivery",     # required since 1.5.4
    ext04=recipient_pub,         # free mode: delete this line
)
# → ./delivery/my_analysis_delivery/my_analysis.mgc_file + README.md
```

**Recipient imports and runs:**
```python
mgc_save_file(path="./received.mgc_file", info_owner="monthly_sales_analysis")
mgc_run(
    info_owner="monthly_sales_analysis",
    diff_2="my_analysis",
    diff_3="run.py",
)
```

Both workflow sealing and skill-package sealing are supported — see `prompts/collaboration_management.md`.

---

### 4. Knowledge management

Users store analysis frameworks, prompt templates, and methodologies in MGC.

**Storing knowledge:**
```python
mgc_save(
    info_type="prompt",
    info_owner="framework_monthly_sales",
    content="analysis framework content"
)
```

See `prompts/knowledge_management.md`

---

## 1.5.4 Security Model

### Double-layer encryption

```
Layer 1: content  = AES-256-CBC(script body, one-time AES_KEY_4)
Layer 2: AES_KEY_4 = RSA-2048 encryption (p2p: target node public key / free mode: shared default public key)
Layer 3: ext03    = AES-256-GCM(Layer-2 result, key = SHA256(ext07)[:32], AAD = ext09)
```

### Link authorization

Every sealed artifact produced in 1.5.4 carries the source node identity (`ext07`) and the sealing mode (`ext09`). On unsealing, the outer key is derived from `ext07` and `ext09` is used as the AAD to verify integrity — so any change to either of them makes the artifact unsealable.

| Scenario | Result |
|---|---|
| Tamper with ext09 (add one space) | `UNSEAL_FAILED: AES-GCM auth tag mismatch` |
| Decrypt with a mismatched private key | `Double-layer unseal failed: Incorrect decryption` |
| Normal import and run | `{"status": "started"}` |

> `ext07` is a plaintext identifier rather than a signature. It provides tamper detection and key binding, but does not replace identity verification — the receiver should still check the source node public key through a trusted channel.

---

## Security boundary (must be obeyed)

### This suite provides:

- Local encrypted credential storage
- Zero-exposure application of user-owned scripts
- Workflow auto-recognition and sealed routing (import / from-import / relative-path / subprocess, including cross-folder calls)
- Sealed-authorization collaboration for workflows / skill packages (p2p mode and free mode; one-key-per-node, node-bound)
- Verifiable artifact integrity thanks to link authorization
- Knowledge management for analysis methods

### This suite does NOT provide:

- Automated data access
- Automated cleaning or analysis
- Automated transport
- Cross-organization data transfer
- Script generation or modification

All scripts must be user-provided and comply with organizational policy.

> MGC protects **content confidentiality**. After unsealing, the script runs with the permissions of the user running it; its command invocations, file reads/writes, and network access are outside MGC's control.

---

## Anti-patterns and pitfalls

### Common mistakes

| Mistake | Risk | Correct approach |
|---------|------|-----------------|
| Pasting credential content in an AI chat | Credential exposure | Store it in MGC; call it from inside the script |
| Letting the AI auto-select a script name | Wrong script executed | The user must supply `info_owner` |
| Accessing a credential without authorization | Policy violation | Request authorization before every access |
| Sending script content to the AI | Script exposure | Apply it through MGC; the AI sees only results |
| Expecting the suite to process data automatically | Violates the design principle | User-owned scripts, each step triggered manually |
| Manually chaining parameters across multiple scripts | Tedious and error-prone | Store as a workflow package with `mgc_save_file`; import relations are auto-recognized |
| Passing only `diff_2` to `mgc_run` without `diff_3` | Multiple records match → `AMBIGUOUS_SCRIPT` | Always pass `diff_3` pointing at the entry script |
| Passing `info_type` to `mgc_find` | The parameter was removed in 1.5.0 → schema validation error | Pass only `info_owner` / `diff_1..3` |
| Omitting `output_dir` when sealing | Required since 1.5.4 → immediate error | Always pass an absolute path |
| Writing `ext04` as `node_pub` | Raises `UNKNOWN_PARAM` (no silent downgrade) | The parameter name is fixed as `ext04` |
| Reading a packaged SKILL.md with `info_type="file"` | Not found — `.md` is stored as `info_type="text"` | Use `info_type="text"` + `diff_3` |

---

## Complete use case

### Scenario: monthly sales data analysis

**Step 1 — preparation**

The user stores the credential and the workflow in MGC:
- Credential: `db_sales_prod` (info_type: token)
- Workflow folder: `my_analysis` (containing run.py + helpers/query.py + helpers/clean.py + helpers/analyze.py)

**Step 2 — the workflow**

```
User: Analyze last month's sales data for me

Agent:
[1] Request authorization: Do you authorize running the workflow monthly_sales_analysis?
User: yes

[2] MGC auto-recognizes the import chain and routes the whole workflow
    through sealed execution
    query → clean → analyze (fully chained, no manual parameter passing)

[3] Results are written to the designated file; the run status is returned
```

Only one authorization is needed — MGC chains the entire workflow, and the Agent never sees script content or credentials.

---

## MCP tools reference

| Tool | Description |
|------|-------------|
| mgc_save | Store credentials, single scripts, prompts |
| mgc_save_file | Store workflow folders / import `.mgc_file` sealed packages |
| mgc_get | Retrieve a value / fetch node_pub / read a file inside a package |
| mgc_run | Run a script or workflow (black-box) |
| mgc_find | Fuzzy-search entries by name (**does not accept info_type**) |
| mgc_list | List stored entries |
| mgc_seal | Seal a single script (produces a self-describing capsule file) |
| mgc_seal_package | Seal an entire workflow folder (produces `.mgc_file` + README) |
| mgc_package | Plaintext export of a folder |
| mgc_delete | Delete stored records (folder deletion requires a second user confirmation) |
| mgc_open_webui | Open MGC WebUI |
| mgc_skill | Read the official MGC skill documentation |

---

## Prompt templates (skill-suite part)

Located in the `prompts/` directory:

- `credential_management.md` — credential-management workflow
- `script_management.md` — workflow & script management
- `collaboration_management.md` — sealed-authorization collaboration workflow
- `knowledge_management.md` — knowledge-management workflow

---

## Agent template (hybrid enhancement)

This suite includes an optional **Data Analyst Agent system-prompt template**:

### agent_system_prompt.md

Used to build a secure Data Analyst Agent. The Agent will:

- Request user authorization before every sensitive operation
- Apply scripts or workflows through MGC after authorization
- Never view script content
- Never access credentials
- Never automate workflow execution
- Never auto-select a script name (`info_owner` must be supplied by the user)

### How to use the Agent template

1. When creating an Agent, set `agent_system_prompt.md` as the system prompt
2. Configure the MCP tools: mgc_save / mgc_save_file / mgc_get / mgc_run / mgc_find / mgc_list / mgc_seal / mgc_seal_package / mgc_package / mgc_delete / mgc_open_webui / mgc_skill
3. The Agent may refer to the prompts in the `prompts/` directory to execute workflow nodes

The Agent is an optional enhancement, not a required component.

---

## Troubleshooting

| Issue | Solution |
|-------|---------|
| Workflow run fails | Check whether the dependencies in `ext05` are installed |
| Import cannot find module | Ensure all scripts are within the same `mgc_save_file` package |
| Run returns `AMBIGUOUS_SCRIPT` | `mgc_run` matched multiple records; list candidates with `mgc_find` and retry with `diff_3` |
| Sealing reports "output_dir required" | `output_dir` is required since 1.5.4 — pass an absolute path |
| Sealing reports `UNKNOWN_PARAM` | The public-key parameter must be `ext04`, not `node_pub` or another alias |
| Sealing reports "Invalid PEM format" | `ext04` must be a multi-line PEM containing real newlines, copied verbatim from `mgc_get(info_type='__NODE_PUB__')` |
| Run after import reports `UNSEAL_FAILED` | The artifact's ext07 / ext09 was modified — obtain the original artifact again |
| Run after import reports "Incorrect decryption" | This node's private key does not match `ext04` — it is not the designated target node |
| Cannot read the packaged SKILL.md | Use `info_type="text"`, not `"file"` |
| `mgc_find` reports a parameter error | The tool has not accepted `info_type` since 1.5.0 |
| Credential fetch failed | Check whether `info_owner` matches |
| Receiver imported it but cross-script calls were not sealed-routed | The receiver runs MGC below 1.5.2 — upgrade it |
| Target node platform incompatible | Check whether `ext06` contains the recipient's OS |

---

## Contact

- Issues: https://github.com/zkeviny/MGC-Blackbox/issues
- Email: mirgincipher@outlook.com

---

## License

MIT License

---

## Full statement

This skill suite is for secure workflow management.
All sensitive operations require user authorization.
This suite provides no automated data-access capability; all scripts must be user-provided and comply with organizational policy.

---
