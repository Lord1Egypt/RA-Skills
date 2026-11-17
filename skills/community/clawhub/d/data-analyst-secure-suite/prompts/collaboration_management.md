# Workflow & Skill Package Sealed Collaboration (Collaboration Management)

This document guides data analysts on how to securely seal and deliver workflows or skill packages to other nodes in **MGC Blackbox ≥ 1.5.4**, enabling "usable but unreadable, runnable but unresellable" cross-team / cross-organization collaboration.

All sensitive operations must be explicitly authorized by the user before proceeding.

---

# 1. Why Sealed Collaboration Is Needed

Common collaboration pain points in data analysis workflows:

| Scenario | Pain Point | MGC Solution |
|----------|-----------|--------------|
| Data team delivers analysis workflow to business team | Don't want business team to see source code or modify logic | After workflow sealing, recipient can only run, never read |
| External analyst delivers analysis package to customer | Customer resells source to peers after delivery | AES key bound to customer node, cannot re-seal |
| Cross-department sharing of analysis methodology | Worry about core algorithm leakage | Seal the entire workflow at once, core algorithms locked inside scripts |
| Delivering to multiple customers | Each customer needs independent authorization | One key per customer, each customer has independent key |
| Publishing a solution to an unspecified audience | Key exchange is inconvenient | **Free mode** sealing — no key exchange needed, importable and runnable as is (1.5.4+) |

> **Core principle**: Delivery equals authorization. After sealing, the recipient can only run — cannot read, modify, or resell.

---

# 2. Workflow Sealing vs Skill Package Sealing

MGC supports two sealed collaboration modes:

| Dimension | Workflow Sealing | Skill Package Sealing |
|-----------|------------------|------------------------|
| **Sealing Target** | Analysis script folder (run.py + helpers/) | Complete skill package with SKILL.md |
| **Sealing Tool** | `mgc_seal_package` | `mgc_seal_package` |
| **Recipient Usage** | `mgc_run` directly invokes the entry script | AI reads SKILL.md instructions and calls the corresponding scripts |
| **Use Case** | Deliver a "one-click run" analysis tool to a business team | Deliver a complete "AI-understandable usage guide" package to a client |
| **SKILL.md Included?** | Not required | Required (the recipient AI's usage manual) |
| **Recipient AI Visibility** | Sees only run status | Can read SKILL.md (plaintext), but cannot see script source code |

> **Selection guidance**:
> - If the recipient only needs to "execute your analysis", use **Workflow Sealing**
> - If the recipient needs AI to autonomously call different scripts per your package, use **Skill Package Sealing**

---

# 3. Two Sealing Modes (new in 1.5.4)

As of 1.5.4, the sealing mode is determined by **whether `ext04` is passed**:

| | p2p mode (node-bound) | free mode |
|---|---|---|
| How to seal | Pass `ext04=<target node multi-line PEM>` | **Omit** `ext04` |
| Resulting `ext09` value | `p2p mode` | `free mode` |
| Who can unseal and run it | Only the node holding the matching private key | **Any MGC 1.5.4+ node** |
| Must public keys be exchanged first? | Yes | No |
| Source visibility | Not readable | Not readable (decrypted in memory at execution time only) |
| Anti-resale strength | Strong (key bound to the node) | Weak (anyone can import and run it) |
| Best for | Commercial delivery, customer isolation | General distribution, open-source solutions, internal sharing |

**How to choose**:
- The deliverable contains commercial algorithms and must not be resold → **p2p mode**
- The deliverable is a general methodology and the recipient does not need to be restricted → **free mode**, which removes the key-exchange step entirely

---

# 4. Link Authorization (new in 1.5.4)

As of 1.5.4, a sealed package is bound to its source node:

- The outer key of the sealed artifact is derived from `ext07` (source node public key)
- `ext09` (sealing mode) participates in the authentication-tag (AAD) computation
- **Any modification to a sealed artifact** (even adding a single space after `ext09`) makes unsealing fail and returns `UNSEAL_FAILED`

**This means**:
- The recipient cannot modify the package content and redistribute it
- Tampering in transit is exposed immediately instead of taking effect silently
- Free mode has the same property (it simply no longer restricts *who* can run it)

---

# 5. End-to-End Collaboration Flow

## 5.1 Complete Flow (p2p mode)

```
Author Node                                         Recipient Node (Client / Team)
───────────                                        ──────────────────────

1. Save workflow / skill package
   mgc_save_file(path="./my_workflow",
                 info_owner="my_workflow")
   → MGC auto-recognizes import / subprocess relationships

2. Recipient fetches their own public key            mgc_get(info_type="__NODE_PUB__",
   (Public key is not secret; any channel OK)         info_owner="__NODE_PUB__")
                                                    → Send PEM public key to author

3. Seal with recipient's public key
   mgc_seal_package(
       info_owner="my_workflow",
       diff_2="my_workflow",
       ext04=recipient_PEM_pubkey,
       output_dir="./delivery",          # REQUIRED since 1.5.4
   )
   → Generates ./delivery/my_workflow_delivery/
       ├── my_workflow.mgc_file
       └── README.md

4. Deliver by any channel                            5. Import sealed package
   (email / USB / IM / cloud drive)                     mgc_save_file(
                                                      path="./received.mgc_file",
                                                      info_owner="my_workflow",
                                                   )
                                                   → Record identity comes from the
                                                     manifest inside the package

                                                   6. Run
                                                      mgc_run(info_owner="my_workflow",
                                                             diff_2="my_workflow",
                                                             diff_3="run.py")
                                                      → Sealed execution, no plaintext on disk
```

## 5.2 Complete Flow (free mode)

```
Author Node                                              Recipient Node
───────────                                             ─────────

1. Save workflow
   mgc_save_file(path="./my_workflow",
                 info_owner="my_workflow")

2. Seal directly (omit ext04 — no key exchange at all)
   mgc_seal_package(
       info_owner="my_workflow",
       diff_2="my_workflow",
       output_dir="./delivery",
   )
   → ext09 = "free mode"

3. Deliver the .mgc_file                                  4. Import
   (email / USB / IM / cloud drive)                          mgc_save_file(
                                                               path="./received.mgc_file",
                                                               info_owner="my_workflow",
                                                            )
                                                          5. Run
                                                             mgc_run(info_owner="my_workflow",
                                                                    diff_2="my_workflow",
                                                                    diff_3="run.py")
```

## 5.3 Security Features

- **AES-256 encryption**: Each script file encrypted independently
- **RSA-2048 key exchange** (p2p mode): the AES key is encrypted with the recipient's node public key, only the recipient can decrypt it
- **Node binding** (p2p mode): the key is bound to the target node, so the recipient cannot re-seal it for a third party
- **Link authorization**: a modified package can no longer be unsealed or run
- **No cloud**: all encryption / decryption / execution happens locally, MGC connects to no cloud
- **Any delivery channel**: encrypted packages can be sent via email, USB, IM, or cloud drive — even if intercepted, they cannot be decrypted

---

# 6. Workflow Sealing Walkthrough

## 6.1 Prepare the Workflow Folder

```
my_analysis/
├── manifest.json
├── run.py              # Entry script
├── helpers/
│   ├── query.py        # Query module
│   ├── clean.py        # Cleaning module
│   └── analyze.py      # Analysis module
└── config/
    └── settings.json
```

## 6.2 Save to MGC

```python
mgc_save_file(
    path="./my_analysis",
    info_owner="monthly_sales_analysis",
    diff_2="monthly_sales_analysis",
)
# MGC auto-recognizes import / subprocess call relationships
```

> **Note**: MGC uses the **last segment of the directory name** as the actual `diff_2` (the `diff_2` you pass is discarded), so use `mgc_find` to confirm it after saving and before sealing.

## 6.3 Seal to Target Node (p2p mode)

```python
# Target node's public key (the recipient fetches it via mgc_get and sends it to you)
recipient_pub = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA...
-----END PUBLIC KEY-----"""

mgc_seal_package(
    info_owner="monthly_sales_analysis",
    diff_2="monthly_sales_analysis",
    ext04=recipient_pub,
    output_dir="./delivery",        # REQUIRED since 1.5.4
)
# → Generates ./delivery/monthly_sales_analysis_delivery/
#      ├── monthly_sales_analysis.mgc_file
#      └── README.md
```

> **Notes**:
> - `ext04` MUST contain real newline characters `\n`. Do NOT pass the PEM as a single concatenated line
> - `output_dir` is **required** as of **1.5.4** (breaking change) — there is no default desktop-directory fallback any more
> - **Do not seal with your own node_pub**: that overwrites the local source record and is not reversible
> - Aliases of `ext04` (`node_pub` / `target_pub` / `public_key` / `pem`, etc.) are compatibility spellings only; **always use `ext04`**

## 6.4 Seal for an Unspecified Audience (free mode)

```python
mgc_seal_package(
    info_owner="monthly_sales_analysis",
    diff_2="monthly_sales_analysis",
    output_dir="./delivery",        # Omitting ext04 means free mode
)
# → ext09 = "free mode"; any MGC 1.5.4+ node can import and run it
```

## 6.5 Recipient Imports and Runs

```python
# Recipient imports the sealed package
# info_owner is required; the record identity comes from the manifest inside the
# package, and the caller's value is only checked for presence
mgc_save_file(
    path="./received.mgc_file",
    info_owner="monthly_sales_analysis",
)

# Recipient runs it (sealed execution, no plaintext on disk)
mgc_run(
    info_owner="monthly_sales_analysis",
    diff_2="monthly_sales_analysis",
    diff_3="run.py",
)
# → {"status": "started"}
```

> **Important**: `diff_3` locates the entry script by its relative path inside the package — it is the only reliable way to avoid `AMBIGUOUS_SCRIPT` (more than one record matched).
>
> **Receiver version requirement**: as of 1.5.4, **both p2p and free-mode sealed packages require the receiver to run MGC ≥ 1.5.4**; older versions fail the link-authorization check and cannot unseal the package.

---

# 7. Skill Package Sealing Walkthrough

The difference between a skill package and a workflow: it includes `SKILL.md` as the recipient AI's usage manual.

## 7.1 Prepare Skill Package Folder

```
my_skill_package/
├── manifest.json
├── SKILL.md             # ← Required for skill packages; recipient AI's usage manual (plaintext)
├── run_query.py          # Query script
├── run_clean.py          # Cleaning script
├── run_analyze.py        # Analysis script
└── helpers/
    ├── db_connect.py
    └── stats.py
```

## 7.2 Role of SKILL.md

`SKILL.md` is **plaintext** — the recipient AI needs to read it to understand:
- Which scripts are available
- Which script to call in which scenario
- What parameters to pass
- In what order

> **Key rule**: `SKILL.md` describes "how to use"; core algorithms live in scripts. Recipient AI can read SKILL.md but cannot read script source.
>
> **Non-script files** inside the package (`SKILL.md` / `config.json` / `manifest.json`) are stored in plaintext and can be read directly with `mgc_get`; **script files** are stored encrypted and decrypted in memory by `mgc_run`.

## 7.3 Save and Seal

```python
# Save the skill package
mgc_save_file(
    path="./my_skill_package",
    info_owner="sales_analysis_suite",
    diff_2="sales_analysis_suite",
)

# Seal to target node (p2p mode)
mgc_seal_package(
    info_owner="sales_analysis_suite",
    diff_2="sales_analysis_suite",
    ext04=recipient_pub,
    output_dir="./delivery",        # REQUIRED since 1.5.4
)
# → Generates .mgc_file encrypted package
```

## 7.4 Recipient Imports and Uses

```python
# Recipient imports
mgc_save_file(
    path="./received.mgc_file",
    info_owner="sales_analysis_suite",
)

# Recipient AI reads SKILL.md (plaintext, learns how to use it)
# Note: a .md file is stored with info_type "text", not "file"
mgc_get(
    info_type="text",
    info_owner="sales_analysis_suite",
    diff_2="sales_analysis_suite",
    diff_3="SKILL.md",
)

# Recipient AI follows SKILL.md instructions to invoke the corresponding scripts
mgc_run(
    info_owner="sales_analysis_suite",
    diff_2="sales_analysis_suite",
    diff_3="run_query.py",
)
```

> **Note**: after a `.mgc_file` is imported, MGC asks you to save the `README.md` generated alongside the package into the recipient's skill manager, so the package can be recognized later and invoked per its instructions.

---

# 8. Independent Authorization per Customer

Each customer needs to be sealed independently — one key binds to one node:

```python
# Seal for customer A
mgc_seal_package(
    info_owner="monthly_sales_analysis",
    diff_2="monthly_sales_analysis",
    ext04=client_a_pub,
    output_dir="./delivery_a",
)
# → Generates .mgc_file for customer A

# Seal for customer B (same workflow, different key)
mgc_seal_package(
    info_owner="monthly_sales_analysis",
    diff_2="monthly_sales_analysis",
    ext04=client_b_pub,
    output_dir="./delivery_b",
)
# → Generates .mgc_file for customer B
```

**Security features**:
- Customer A's package cannot run on Customer B's machine (key mismatch)
- Customer A cannot re-seal their package to Customer C (the AES key is bound to A's node)
- Each customer's sealed package is independent, no cross-impact

> If node binding is not required and you simply want multiple parties to be able to use it, seal once in **free mode** (omit `ext04`) instead of producing one package per customer.

---

# 9. Authorization Template (AI Must Ask)

### Before sealing a workflow:

```
Workflow Name: monthly_sales_analysis
Sealing Mode: p2p mode (node-bound)
Target Node Public Key: {first 16 chars of node_pub}...
Operation: Seal Workflow
Authorization Required: YES

Do you authorize sealing this workflow? Reply "yes" to proceed, or "no" to cancel.
```

### Before sealing a skill package:

```
Skill Package Name: sales_analysis_suite
Sealing Mode: free mode (any 1.5.4+ node can run it)
Output Directory: ./delivery
Operation: Seal Skill Package
Authorization Required: YES

Do you authorize sealing this skill package? Reply "yes" to proceed, or "no" to cancel.
```

---

# 10. Best Practices

### ✔ 1. Put Core Algorithms in Scripts, Not in SKILL.md
SKILL.md is plaintext; the recipient can read it. The algorithm is your "product" — it must be locked inside scripts.

### ✔ 2. SKILL.md Only Describes Routing
Specify "which scenario calls which script, with what parameters"; do not write business logic details.

### ✔ 3. Seal Independently for Each Customer
Do not try to deliver one p2p sealed package to multiple customers — each customer's key binds to their own node.

### ✔ 4. Write Results to Specified Files
After a sealed package runs, MGC will not return plaintext. Workflow output must explicitly target a file path, or be written to a database or MGC itself.

### ✔ 5. Delivery Channel Is Unrestricted
Encrypted packages can be sent via email, USB, IM, or cloud drive. Even if intercepted, without the corresponding node's private key they cannot be decrypted.

### ✔ 6. Always Pass `output_dir` When Sealing
Since 1.5.4, `output_dir` is required for `mgc_seal_package` / `mgc_package`.

### ✔ 7. Never Seal With Your Own node_pub
Sealing locally overwrites the local source record, and once the plaintext script is replaced by ciphertext the change is not reversible.

---

# 11. FAQ

| Issue | Solution |
|-------|----------|
| Sealing failed | Check whether `ext04` is a multi-line PEM public key (preserving `\n`) |
| Sealing reports a parameter error | `output_dir` is required as of 1.5.4 |
| Recipient run fails | Check whether the dependencies in `ext05` are installed on the recipient side |
| Recipient import fails | Ensure all scripts are within the same `mgc_save_file` package |
| Platform incompatible | Check whether `ext06` contains the recipient's OS |
| Customer says "it doesn't work on another machine" | This is by design in p2p mode — node binding prevents resale; switch to free mode for general distribution |
| Recipient cannot unseal the package | The receiver's MGC version must be ≥ 1.5.4 (link authorization requirement) |
| Unsealing returns `UNSEAL_FAILED` | The sealed package content was modified — it must be sealed again |
| `AMBIGUOUS_SCRIPT` returned | Several script records in the package matched; use `mgc_find` to look up `diff_3`, then specify it precisely |
| Import overwrote the source record | `mgc_save_file` must use your own `info_owner`, not the source node's |

---

# 12. Summary

This sealed collaboration document provides:

- Workflow sealing (`mgc_seal_package`) and skill package sealing
- End-to-end authorized collaboration flow (node_pub → seal → import → run)
- Multi-customer independent authorization (one key per seal, one node per key)
- p2p / free sealing modes and link authorization (1.5.4)
- IP protection: "usable but unreadable, runnable but unresellable"

This is the core capability of secure data analyst collaboration workflows.
