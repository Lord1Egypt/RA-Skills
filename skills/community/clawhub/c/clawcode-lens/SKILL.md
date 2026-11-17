---
name: ClawCode Lens
slug: clawcode-lens
version: 1.0.1
description: "Explain code in any language with structured syntax/logic breakdown, local security scan, and improvement suggestions. 100% lokal — private og hurtig, ingen netværkskald, ingen API-nøgle."
metadata: {"clawbot": {"requires": {"bins": ["python3"]}, "notes": "100% lokal — ingen netværkskald, ingen API-nøgle."}}
---

# ClawCode Lens

Code explanation and analysis tool — inspired by Dify Code Interpreter, **improved**:

## 🆕 Unique features (not in the original)

### Feature 1: Runs 100% LOCALLY — no external API required
code directly with structured rules — works offline, free and instantly:

```bash
python3 scripts/explain.py code.py --lang python
python3 scripts/explain.py main.js --lang javascript --detail
```

### Feature 2: Security scanning (local)
Finds vulnerabilities: hardcoded keys, SQL injection, `eval()` misuse, unsafe
`exec` calls, weak passwords, unsafe imports:

```bash
python3 scripts/security_scan.py code.py --out report.md
```

### Feature 3: Improvement suggestions
Gives concrete, prioritized suggestions: complexity, repeated code, missing error handling,
performance bottlenecks and best practices — with code examples:

```bash
python3 scripts/improve.py code.py --out suggestions.md
```

---

## How to use

### Explain code (structured)
```bash
python3 scripts/explain.py file.py --lang python
# Output: overview → key functions → logic flow → edge cases
```

### Supported languages
Python, JavaScript/TypeScript, C/C++, Java, C#, Go, Rust, SQL, Bash, PHP, Ruby — auto-detected from file type.

### Combine everything in one call
```bash
python3 scripts/explain.py app.py --security --improve --out full-report.md
```

```bash

# 2) Deep scan (PAID call — uploads your code + costs per call)
python3 scripts/code_scan.py app.py
```

- **Price**: $0.005/call · $25/mo
- ⚠️ Paid call — each run charges your key AND uploads the selected source file to the external API. **Do not use on confidential/proprietary code.**

## Example output (security scan)

```text
🔒 Security scan: app.py
  [HIGH]    Line 45: SQL string built with f-string — injection risk
  [INFO]    Line 78: eval() — avoid unless strictly necessary
```

## Feedback
- Helpful? → `clawhub star clawcode-lens`
---
