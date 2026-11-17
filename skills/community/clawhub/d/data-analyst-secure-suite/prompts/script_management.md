# Script & Workflow Management

This document guides data analysts on how to securely manage query scripts, cleaning scripts, analysis scripts, and other **user-owned scripts** in **MGC Blackbox ≥ 1.5.4**, and implement **zero-exposure application** locally.

All sensitive operations must be explicitly authorized by the user before proceeding.

---

# 1. Workflow Management Overview

MGC Blackbox 1.5.4+ provides local encrypted storage, automatic cross-script recognition, and zero-exposure application:

- Script content is never exposed to AI
- Scripts are decrypted only on the user's local machine
- Scripts can safely call credentials (zero-exposure)
- All applications must be authorized by the user
- AI can only see execution results, never script logic
- **Workflow folders are automatically scanned for `import` / relative-path / `subprocess` call relationships** (1.5.1+)
- **Cross-folder `subprocess` calls are recognized as well and routed through sealed execution** (1.5.4+)

---

# 2. Two Management Modes

| Mode | Scenario | Storage Tool | Run Tool |
|------|---------|-------------|---------|
| **Workflow Mode (recommended)** | Multi-script pipelines (query → clean → analyze) | `mgc_save_file` | `mgc_run` (specify the entry script) |
| **Single-Script Mode** | A single independent script | `mgc_save` | `mgc_run` |

> **Recommendation**: If your analysis chain has 2+ scripts, use Workflow Mode. MGC automatically recognizes `import` / `from-import` / relative-path / `subprocess` relationships between scripts and routes execution under sealing — no manual parameter passing needed.

---

# 3. Workflow Mode (Recommended)

## 3.1 Workflow Folder Structure

A typical data analysis workflow:

```
my_analysis/
├── manifest.json
├── run.py              # Entry script: invokes modules under helpers
├── helpers/
│   ├── query.py        # Query module
│   ├── clean.py        # Cleaning module
│   └── analyze.py      # Analysis module
└── config/
    └── settings.json   # Configuration file
```

`run.py` can directly `import` modules from the same package:

```python
# run.py
from helpers.query import query_data
from helpers.clean import clean_data
from helpers.analyze import analyze_data

def main():
    raw = query_data()
    cleaned = clean_data(raw)
    result = analyze_data(cleaned)
    # Write result to file or MGC; never return it
    with open("output/report.xlsx", "wb") as f:
        f.write(result)

if __name__ == "__main__":
    main()
```

## 3.2 Save the Workflow

```python
mgc_save_file(
    path="./my_analysis",
    info_owner="monthly_sales_analysis",
    diff_2="monthly_sales_analysis",
)
```

**MGC will automatically**:
- Parse each script's `argparse` and write it to `ext02` (parameter list)
- Scan imports and write them to `ext05` (dependency list)
- Infer `ext06` (platform list)
- Build `ext08` (cross-script call graph) — recognizing `import` / `from-import` / `Path` relative-path / `subprocess` relationships; **since 1.5.4 both same-folder imports and cross-folder `subprocess` calls are fully recognized**

> **Note**: MGC will **use the last segment of the path as `diff_2`** (e.g. `path="./my_analysis"` actually writes `diff_2="my_analysis"`), so the `diff_2` passed by the caller is discarded. After saving, use `mgc_find` to confirm the actual `diff_2`, then pass that value when sealing.

## 3.3 Run the Workflow

```python
mgc_run(
    info_owner="monthly_sales_analysis",
    diff_2="monthly_sales_analysis",
    diff_3="run.py",          # Relative path of the entry script inside the package
)
# → {"status": "started"}
```

MGC will automatically:
- Decrypt all scripts into memory (never written to disk)
- Intercept `import` / `subprocess` calls and route them through sealed execution
- Return the run status, never script content

> **Important**: `diff_3` is the **only reliable way** to locate the entry script. A workflow package holds several script records under the same `info_owner`; if more than one record matches and only `info_owner` + `diff_2` are passed, MGC returns `AMBIGUOUS_SCRIPT` (HTTP 409) and asks you to run `mgc_find` first to confirm the path.
>
> `diff_3` takes the **relative path inside the package** (e.g. `run.py`, `helpers/query.py`), not a bare file name.
>
> Also: since **1.5.4**, `mgc_run` **no longer requires `diff_1`** — `info_owner` is the only required parameter.

## 3.4 Locate a Workflow by Name

```python
# Fuzzy search for a workflow
matches = mgc_find(
    info_owner="monthly",      # Partial name; substring match by default
    match_mode="substring",
)
# Returns a metadata list (info_type, info_owner, diff_1..diff_3) — never plain text.
# Once the exact info_owner and diff_3 are located, pass them to mgc_run.
```

> **Note**: since 1.5.0, `mgc_find` **does not accept an `info_type` parameter** — pass only `info_owner` / `diff_1` / `diff_2` / `diff_3` / `match_mode` / `limit`.

## 3.5 Workflow Sealed Collaboration

Seal the entire workflow to another node (team member / client) in one shot:

```python
# 1. The recipient first fetches their own node_pub
# Recipient runs: mgc_get(info_type="__NODE_PUB__", info_owner="__NODE_PUB__")

# 2. You seal the entire workflow with the recipient's public key (p2p mode)
mgc_seal_package(
    info_owner="monthly_sales_analysis",
    diff_2="monthly_sales_analysis",
    ext04=recipient_node_pub,          # Recipient's PEM public key
    output_dir="./delivery",            # REQUIRED since 1.5.4: output directory for the sealed package
)
# → Generates ./delivery/monthly_sales_analysis_delivery/monthly_sales_analysis.mgc_file
```

After the recipient receives the `.mgc_file`:

```python
# Recipient imports the sealed package
# Note: info_owner is required; the record identity comes from the manifest inside the
# package, and the caller's value is only checked for presence
mgc_save_file(
    path="./received.mgc_file",
    info_owner="monthly_sales_analysis",
)

# Recipient runs it in blackbox mode
mgc_run(
    info_owner="monthly_sales_analysis",
    diff_2="monthly_sales_analysis",
    diff_3="run.py",
)
```

**Security features**:
- The whole workflow is sealed in one shot — no need to seal each script individually
- The AES key is bound to the recipient's RSA public key, so the recipient cannot re-seal it for a third party
- The recipient can only run it, never read the source
- Since 1.5.4 the sealed package carries **link authorization**: once the package content is modified, it can no longer be unsealed or run

> **Note**: `ext04` MUST contain real newline characters `\n`. Do NOT pass the PEM as a single concatenated line.

---

# 4. Single-Script Mode (Simple Scenarios)

When you only need to manage a single independent script (no cross-script calls), use `mgc_save`.

## 4.1 Save a Single Script

```python
mgc_save(
    info_type="script",
    info_owner="quick_query",
    ext01="python",
    content="<your script content>"
)
```

## 4.2 Run a Single Script

```python
mgc_run(
    info_type="script",
    info_owner="quick_query",
)
```

> **Changed in 1.5.4**: `mgc_run` no longer requires `diff_1`. If more than one record shares the same name in the library, `AMBIGUOUS_SCRIPT` is still returned — in that case use `mgc_find` to retrieve `diff_1..diff_3` and specify it precisely.

## 4.3 Seal a Single Script (Sealed Capsule, 1.5.4+)

`mgc_seal` produces a **self-describing sealed capsule file** (`sealed_capsule.json`) for a single script:

```python
# p2p mode: only the node holding the matching private key can unseal and run it
capsule_path = mgc_seal(
    info_owner="quick_query",
    ext04=recipient_node_pub,      # Target node's PEM public key
    output_dir="./delivery",        # REQUIRED since 1.5.4
)
# → ./delivery/quick_query_<timestamp>/sealed_capsule.json
```

```python
# free mode: omit ext04 — any MGC 1.5.4+ node can import and run it
capsule_path = mgc_seal(
    info_owner="quick_query",
    output_dir="./delivery",
)
```

The recipient imports the capsule (`mgc_save_file` is recommended — it recognizes the capsule and extracts all `ext` fields automatically):

```python
mgc_save_file(
    path="<capsule_path>",
    info_owner="my_quick_query",   # Use your own owner name to avoid overwriting the source record
)
```

> **Notes**:
> - `output_dir` is **required** as of **1.5.4** (breaking change) — there is no desktop-directory fallback any more
> - Aliases of `ext04` (`node_pub` / `target_pub` / `public_key` / `pem`, etc.) are compatibility spellings only; **always use `ext04`**
> - Omitting `ext04` means free mode; see Chapter 5 for the difference between the two modes

---

# 5. Two Sealing Modes (1.5.4)

| | p2p mode (node-bound) | free mode |
|---|---|---|
| How to seal | Pass `ext04=<target node multi-line PEM>` | **Omit** `ext04` |
| Resulting `ext09` value | `p2p mode` | `free mode` |
| Who can unseal and run it | Only the node holding the matching private key | **Any MGC 1.5.4+ node** |
| Is the source readable | No | No (decrypted in memory at execution time only) |
| Best for | Targeted delivery, preventing resale | General distribution, open-source delivery |

**The trade-off of free mode**: it gives up "node binding" in exchange for "anyone can run it". If the deliverable contains commercial algorithms, p2p mode is still the right choice.

---

# 6. Link Authorization (1.5.4)

As of 1.5.4, a sealed package is bound to its source node: the outer key of the sealed artifact is derived from `ext07` (source node public key), and `ext09` (sealing mode) participates in the authentication-tag computation. **Any modification to a sealed artifact** (even adding a single space) makes unsealing fail with `UNSEAL_FAILED`.

**This means**:
- The recipient cannot modify the package content and redistribute it
- Tampering in transit is exposed immediately instead of taking effect silently
- Free mode has the same property (it simply no longer restricts *who* can run it)

---

# 7. Zero-Exposure Credential Calls Inside Scripts

**MGC implementation**: scripts are stored in MGC; at runtime MGC decrypts the script and executes it locally. If the script needs to access credentials, it calls a local API to fetch them internally.

## Standard Example: Script Safely Accesses Credentials Internally

```python
import os, requests, json

# Read MGC access token (fixed path, do not change)
with open(os.path.expanduser("~/.mgc/database/mgc_black_box/.mgc_token")) as f:
    MGC_TOKEN = f.read().strip()

def get_credential(info_owner="db_warehouse_prod"):
    """Fetch credential from MGC"""
    resp = requests.post(
        "http://127.0.0.1:57219/api/mgc/sensitive/get",
        headers={"X-MGC-Token": MGC_TOKEN},
        json={
            "info_type": "token",
            "info_owner": info_owner,
        },
    )
    if resp.status_code == 200:
        data = resp.json()
        if data.get("code") == 200:
            data_field = data.get("data")
            if isinstance(data_field, str):
                return json.loads(data_field)
            elif isinstance(data_field, dict):
                content = data_field.get("content")
                if content:
                    return json.loads(content)
    return None

# Using credential
def query_monthly_orders():
    credential = get_credential("db_warehouse_prod")
    # ... use credential to connect and query
```

**Notes**:
- This call is local-only (127.0.0.1), AI cannot see credentials
- Token file path: `~/.mgc/database/mgc_black_box/.mgc_token`

---

# 8. Recognizable Cross-Script Patterns (Required for Workflow Mode)

When saving a workflow folder with `mgc_save_file`, MGC automatically recognizes the following patterns:

| Pattern | Code Example | Recognizable? |
|---------|--------------|--------------|
| `from` import | `from config import DEFAULT_CITY` | ✅ |
| `from` import with alias | `from helpers.fetch import get_weather as gw` | ✅ |
| Plain `import` | `import helpers.parse` | ✅ |
| `Path` relative path | `Path(__file__).parent / "config.py"` | ✅ |
| `open()` relative path | `open("config.json")` referencing a sibling file | ✅ |
| `subprocess` + relative path | `subprocess.run([sys.executable, str(Path(__file__).parent / "config.py"), ...])` | ✅ — since 1.5.4 both same-folder and cross-folder calls are recognized |
| `subprocess` + literal list | `subprocess.run([sys.executable, "helper.py", "--arg"])` | ✅ — runtime routing support since 1.5.2 |
| Dynamic import | `importlib.import_module(module_name)` | ❌ only static parsing supported |
| Absolute path | `open("/Users/alice/config.py")` | ❌ not portable |

**Scope**: since 1.5.4, cross-folder `subprocess` calls are also recognized and routed through sealed execution; the called script must still live **inside the same `mgc_save_file` package**, otherwise the runtime returns a `DIFF2_MISMATCH` warning and fails.

---

# 9. Authorization Template (AI Must Ask)

When AI needs to apply scripts or workflows, it must ask the user:

```
Workflow Name: monthly_sales_analysis
Operation: Run Workflow
Authorization Required: YES

Do you authorize this operation? Reply "yes" to proceed, or "no" to cancel.
```

AI must not apply any script or workflow without user authorization.

---

# 10. Best Practices

### ✔ 1. Prefer Workflow Mode
For multi-script analysis chains, save with `mgc_save_file` — MGC auto-recognizes import relationships, no manual parameter passing needed.

### ✔ 2. Entry Script Only Handles Orchestration
`run.py` should only call modules under `helpers`; put core algorithms in their own modules.

### ✔ 3. Write Results to File or MGC
For blackbox execution, MGC will not return any plaintext. Workflow output must explicitly target a file path, or be written to a database or MGC itself.

### ✔ 4. Use Descriptive `info_owner`
For example: `monthly_sales_analysis`, `customer_churn_prediction`, `daily_report_gen`

### ✔ 5. Never Hardcode Secrets in Scripts
All secrets must be obtained through MGC.

### ✔ 6. All Applications Require Authorization
AI must not automatically apply scripts or workflows.

### ✔ 7. Always Pass `diff_3` When Running
Specify the relative path of the entry script inside the package to avoid matching several records and triggering `AMBIGUOUS_SCRIPT`.

### ✔ 8. Always Pass `output_dir` When Sealing
Since 1.5.4, `output_dir` is required for `mgc_seal` / `mgc_package` / `mgc_seal_package`.

---

# 11. FAQ

| Issue | Solution |
|-------|----------|
| Workflow run fails | Check whether dependencies in `ext05` are installed locally |
| Import cannot find module | Ensure all scripts are within the same `mgc_save_file` package |
| `AMBIGUOUS_SCRIPT` returned | More than one record matched; use `mgc_find` to look up `diff_3`, then specify the entry script's relative path in `mgc_run` |
| Sealing failed | Check whether `ext04` is a multi-line PEM public key (preserving `\n`) |
| Sealing reports a parameter error | `output_dir` is required as of 1.5.4 |
| Platform incompatible | Check whether `ext06` contains the current OS |
| Credential fetch failed | Check whether `info_owner` matches |
| Import overwrote the source record | `mgc_save_file` must use your own `info_owner`, not the source node's |
| Sealed package cannot be unsealed | The package content was modified — link authorization rejects any tampering, so it must be sealed again |

---

# 12. Summary

This workflow management document provides:

- Encrypted workflow folder storage and automatic recognition (including cross-folder calls)
- Zero-exposure credential calls
- Zero-exposure workflow execution
- User authorization mechanism
- Workflow sealing and collaboration authorization
- p2p / free sealing modes and link authorization (1.5.4)

This is the core capability of secure data analyst workflows.
