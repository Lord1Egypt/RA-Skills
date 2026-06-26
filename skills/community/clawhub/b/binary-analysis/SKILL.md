---
name: drbinary-analysis
description: >
  Use when the user wants to analyze a binary file, check if a file is
  malicious, decompile an executable, or understand what a binary does.
  Triggers on: "analyze this binary", "is this malicious?", "decompile
  this exe", "what does this binary do?", "reverse engineer this file".
---

# Dr. Binary Analysis

## Required environment variables

- `DRBINARY_API_KEY` — drbinary.ai → Settings → Billing → API Key

## Steps

### 1. Upload the binary

Run `upload.py` with the local file path. It uploads the file to the
Dr. Binary sandbox and prints the remote path:

```bash
python skills/drbinary-analysis/upload.py /path/to/file.exe
# → /sandbox/<pathname>
```

### 2. Open Ghidra server

Call the `ghidra_open_server` MCP tool with the remote sandbox path
returned in step 1. This initialises analysis and returns basic file
metadata (size, hash, segments, imports, exports, strings, functions).

### 3. Analyse with Ghidra tools

Use the available MCP tools to perform a thorough analysis:

- **`ghidra_list_imports`** — identify suspicious API calls
- **`ghidra_list_strings`** — extract strings for IoC identification
- **`ghidra_list_exports`** — list exported symbols
- **`ghidra_decompile_function`** — decompile key functions to pseudo-C
- **`ghidra_generate_call_graph`** — understand program flow
- **`sandbox_execute`** — run safe commands (e.g. `file`, `strings`, `sha256sum`)

### 4. Report

Return a report in this format:

```markdown
## Binary Analysis Report

**File Information**
- Name: [filename]
- Size: [bytes]
- SHA256: [hash]

**Analysis Summary**
[Brief overview of findings]

**Detailed Findings**
1. [Finding category]
   - Evidence: [specific data]
   - Significance: [what it means]

**Threat Assessment**
- Severity: [Critical/High/Medium/Low]
- Classification: [malware type or benign]
- Confidence: [High/Medium/Low]

**Recommendations**
1. [Action item]
```
