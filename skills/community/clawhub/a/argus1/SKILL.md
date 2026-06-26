---
name: argus1
description: "Argus â The Hundred-Eyed. Scan your Python or JavaScript codebase for bugs, security vulnerabilities, code smells, and common anti-patterns â get a prioritised findings report with line numbers, severity ratings, and fix suggestions. No external tools required."
version: "1.0.4"
metadata:
  openclaw:
    requires:
      env: []
      bins: [python3, pip3]
    primaryEnv: "SOURCE_PATH"
    homepage: https://clawhub.ai/occupythemilkyway/argus1
    emoji: "ððï¸"
    tags: [debugging, security, code-review, python, javascript, linter, argus, static-analysis]
    envVars:
      - name: SOURCE_PATH
        required: false
        description: "Path to a .py or .js file, or a directory to scan recursively. Defaults to current directory."
        default: "."
      - name: LANGUAGE
        required: false
        description: "Language to scan: python, javascript, or auto (detects from file extensions)"
        default: "auto"
      - name: SEVERITY_FILTER
        required: false
        description: "Minimum severity to report: critical, high, medium, low, or all"
        default: "all"
      - name: MAX_FINDINGS
        required: false
        description: "Maximum number of findings to display (default: 50)"
        default: "50"
      - name: OUTPUT_JSON
        required: false
        description: "Set to 'true' to also save findings as JSON"
        default: "false"
---

# Argus â Code Intelligence Scanner

Scan any Python or JavaScript codebase for bugs, security holes, and anti-patterns in seconds â with line numbers, severity ratings, and actionable fix suggestions.

## What Argus catches

**Security** â SQL injection patterns, hardcoded secrets, eval/exec abuse, innerHTML XSS, open redirects, pickle deserialization  
**Bugs** â mutable default arguments, bare except clauses, missing null checks, == None comparisons  
**Code quality** â broad imports, print statements in production, TODO/FIXME markers, deeply nested code  
**JavaScript** â var usage, loose equality (==), console.log left in, prototype pollution patterns

## Quick start

```bash
SOURCE_PATH="./src" LANGUAGE="python" SEVERITY_FILTER="high" openclaw skills run argus1
```

## ð Security

Reads local files only. Nothing transmitted outside your machine.

---

## Step 1 â Install

```bash
pip3 install rich --break-system-packages --quiet
```

---


---

## â¡ Upgrade to Argus Pro

ð **Get Argus Pro** â **ko-fi.com/s/8b27346505** â $9 one-time

```bash
openclaw skills install argus-pro
# Set LICENSE_KEY env var to your key from Ko-fi, then run
```

ð° **Bundle deal:** all 5 Pro skills for **$29** â **ko-fi.com/s/7625accf3f** (save $16)

## Step 2 â Scan for bugs and vulnerabilities

```python
import os, re, json
from pathlib import Path
from datetime import date
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

FENCE = chr(96) * 3

console = Console()

SRC_PATH   = os.environ.get("SOURCE_PATH", ".").strip()
LANGUAGE   = os.environ.get("LANGUAGE", "auto").lower().strip()
SEV_FILTER = os.environ.get("SEVERITY_FILTER", "all").lower().strip()
try:
    MAX_FINDINGS = int(os.environ.get("MAX_FINDINGS", "50"))
except ValueError:
    MAX_FINDINGS = 50
OUTPUT_JSON = os.environ.get("OUTPUT_JSON", "false").lower() == "true"
TODAY       = date.today()

src = Path(SRC_PATH)
if not src.exists():
    console.print(f"[red]â Path not found: {SRC_PATH}[/red]")
    raise SystemExit(1)

def detect_lang(path: Path) -> str:
    py = len(list(path.rglob("*.py") if path.is_dir() else ([path] if str(path).endswith(".py") else [])))
    js = len(list(path.rglob("*.js") if path.is_dir() else ([path] if str(path).endswith(".js") else [])))
    if py >= js:
        return "python"
    return "javascript"

lang = LANGUAGE if LANGUAGE != "auto" else detect_lang(src)
ext  = "*.py" if lang == "python" else "*.js"

# ââ Rule definitions: (id, severity, category, regex, message, fix) ââââââââââ
PYTHON_RULES = [
    ("PY001", "critical", "security",  r"\beval\s*\(",                     "eval() executes arbitrary code â extremely dangerous with user input.",               "Use ast.literal_eval() for safe evaluation of literals."),
    ("PY002", "critical", "security",  r"\bexec\s*\(",                     "exec() executes arbitrary strings as Python code.",                                   "Refactor to avoid dynamic code execution."),
    ("PY003", "critical", "security",  r"\bpickle\.loads?\s*\(",           "pickle.load() can execute arbitrary code when deserialising untrusted data.",         "Use json.loads() or a safe serialisation format instead."),
    ("PY004", "high",     "security",  r"(?i)(password|secret|api_key|token|auth_key)\s*=\s*['\"].+['\"]", "Hardcoded credential detected.",                      "Store secrets in environment variables, never in source code."),
    ("PY005", "high",     "security",  r"shell\s*=\s*True",                "shell=True in subprocess is a command-injection risk.",                               "Pass a list of arguments instead: subprocess.run(['cmd', 'arg'])"),
    ("PY006", "high",     "security",  r"\.execute\s*\(.*(%|\.format\(|f['\"])", "Potential SQL injection via string formatting in execute().",                   "Use parameterised queries: cursor.execute(sql, (param,))"),
    ("PY007", "medium",   "bug",       r"def\s+\w+\s*\([^)]*=\s*\[\s*\]", "Mutable default argument [] â shared across all calls.",                             "Use None as default and initialise inside the function."),
    ("PY008", "medium",   "bug",       r"def\s+\w+\s*\([^)]*=\s*\{\s*\}", "Mutable default argument {} â shared across all calls.",                             "Use None as default and initialise inside the function."),
    ("PY009", "medium",   "bug",       r"except\s*:",                      "Bare except: catches SystemExit and KeyboardInterrupt â almost never intentional.",   "Catch specific exceptions: except ValueError: or except Exception:"),
    ("PY010", "medium",   "bug",       r"==\s*None\b|\bNone\s*==",         "Use 'is None' instead of '== None'.",                                                "Replace '== None' with 'is None' and '!= None' with 'is not None'."),
    ("PY011", "medium",   "bug",       r"!=\s*None\b|\bNone\s*!=",         "Use 'is not None' instead of '!= None'.",                                            "Replace '!= None' with 'is not None'."),
    ("PY012", "medium",   "quality",   r"\bprint\s*\(",                    "print() statement found â likely debug output left in production code.",              "Remove or replace with logging.debug() / logging.info()."),
    ("PY013", "low",      "quality",   r"#\s*(TODO|FIXME|HACK|XXX|BUG)\b", "Unresolved TODO/FIXME marker.",                                                      "Resolve or create a tracked issue for this item."),
    ("PY014", "low",      "quality",   r"from\s+\w+\s+import\s+\*",        "Wildcard import pollutes namespace and makes dependencies unclear.",                  "Import only what you need: from module import specific_name"),
    ("PY015", "low",      "quality",   r"import\s+pdb\b",                  "Debugger import (pdb) left in code.",                                                 "Remove pdb import before committing to production."),
    ("PY016", "medium",   "security",  r"hashlib\.(md5|sha1)\s*\(",        "MD5/SHA1 are cryptographically weak â not suitable for passwords or signatures.",     "Use hashlib.sha256() or better; bcrypt/argon2 for passwords."),
    ("PY017", "high",     "security",  r"random\.(random|randint|choice)\s*\(", "random module is not cryptographically secure.",                                 "Use secrets module for security-sensitive random values."),
    ("PY018", "medium",   "bug",       r"open\s*\(.+\)(?!\s*as\b)(?!.*with\b)", "File opened without context manager â may leak file handle.",                   "Use 'with open(...) as f:' to ensure proper cleanup."),
    ("PY019", "low",      "quality",   r"lambda\s+\w+:\s*\w+\s*\(",        "Lambda used where a named function would be clearer.",                               "Consider replacing with a def statement for readability."),
    ("PY020", "medium",   "bug",       r"\btype\s*\(\w+\)\s*==\s*",        "Use isinstance() instead of type() == for type checks.",                             "Replace type(x) == SomeType with isinstance(x, SomeType)."),
]

JS_RULES = [
    ("JS001", "high",     "quality",   r"\bvar\s+",                        "var is function-scoped and hoisted â causes subtle bugs.",                            "Use const or let instead."),
    ("JS002", "critical", "security",  r"\.innerHTML\s*=",                 "innerHTML assignment is an XSS vector if content comes from user input.",             "Use textContent for text or DOMPurify to sanitise HTML."),
    ("JS003", "critical", "security",  r"\beval\s*\(",                     "eval() executes arbitrary JavaScript â a critical security risk.",                    "Refactor to eliminate eval() usage entirely."),
    ("JS004", "high",     "security",  r"(?i)(api_key|apikey|api_secret|access_token|auth_token|password)\s*=\s*['\"].+['\"]", "Hardcoded credential detected.", "Move secrets to environment variables or a secrets manager."),
    ("JS005", "medium",   "bug",       r"==\s*null\b(?!\=)|null\s*==(?!\=)", "Loose equality with null also matches undefined â usually unintentional.",         "Use === null or check explicitly for both null and undefined."),
    ("JS006", "medium",   "bug",       r"(?<!=)==(?!=)",                   "Loose equality (==) performs type coercion â a common source of bugs.",              "Use strict equality (===) instead."),
    ("JS007", "medium",   "quality",   r"\bconsole\.(log|warn|error|debug)\s*\(", "console.log left in production code.",                                         "Remove or replace with a proper logging library."),
    ("JS008", "medium",   "security",  r"document\.write\s*\(",            "document.write() can overwrite the entire page and is an XSS risk.",                 "Use DOM manipulation methods (createElement, appendChild) instead."),
    ("JS009", "low",      "quality",   r"//\s*(TODO|FIXME|HACK|XXX|BUG)\b", "Unresolved TODO/FIXME marker.",                                                    "Resolve or create a tracked issue for this item."),
    ("JS010", "high",     "security",  r"__proto__\s*=|Object\.assign\s*\(\s*\{\s*\},", "Potential prototype pollution pattern.",                                 "Validate that object keys don't include __proto__ or constructor."),
    ("JS011", "medium",   "bug",       r"setTimeout\s*\(\s*['\"]",         "setTimeout with a string argument calls eval internally.",                           "Pass a function reference instead: setTimeout(() => doThing(), ms)"),
    ("JS012", "low",      "quality",   r"function\s+\w+\s*\([^)]{60,}\)",  "Function has too many parameters â consider an options object.",                    "Refactor long parameter lists into a single options/config object."),
]

RULES = PYTHON_RULES if lang == "python" else JS_RULES
SEV_ORDER = {"critical": 0, "high": 1, "medium": 2, "low": 3}
SEV_FILTER_LEVEL = {"all": 3, "low": 3, "medium": 2, "high": 1, "critical": 0}.get(SEV_FILTER, 3)

files = list(src.rglob(ext) if src.is_dir() else [src])
if not files:
    console.print(f"[yellow]No {ext} files found in {SRC_PATH}[/yellow]")
    raise SystemExit(0)

console.print()
console.print(Panel.fit(
    f"[bold red]ð ðï¸  Argus â Code Intelligence Scanner[/bold red]\n"
    f"Scanning [yellow]{len(files)}[/yellow] {lang} file(s) in [cyan]{SRC_PATH}[/cyan] "
    f"| Severity: [white]{SEV_FILTER}[/white] | Rules: [white]{len(RULES)}[/white]",
    border_style="red"
))

findings = []
for filepath in files:
    try:
        source = filepath.read_text(encoding="utf-8", errors="replace")
        lines  = source.splitlines()
        for lineno, line in enumerate(lines, 1):
            for rule_id, sev, category, pattern, message, fix in RULES:
                if re.search(pattern, line):
                    if SEV_ORDER.get(sev, 3) <= SEV_FILTER_LEVEL:
                        findings.append({
                            "id":       rule_id,
                            "severity": sev,
                            "category": category,
                            "file":     str(filepath.relative_to(src) if src.is_dir() else filepath),
                            "line":     lineno,
                            "code":     line.strip()[:80],
                            "message":  message,
                            "fix":      fix,
                        })
    except Exception as e:
        console.print(f"[dim]Skipping {filepath}: {e}[/dim]")

# Deduplicate by (rule, file, line)
seen = set()
unique = []
for f in findings:
    key = (f["id"], f["file"], f["line"])
    if key not in seen:
        seen.add(key)
        unique.append(f)

# Sort by severity then file/line
unique.sort(key=lambda f: (SEV_ORDER.get(f["severity"], 3), f["file"], f["line"]))
display = unique[:MAX_FINDINGS]

# ââ Display results âââââââââââââââââââââââââââââââââââââââââââââââââââââââââââ
SEV_COLOUR = {"critical": "red", "high": "orange3", "medium": "yellow", "low": "dim"}

if not unique:
    console.print(Panel(
        "[green]â No issues found![/green]\n\n"
        f"Scanned {len(files)} file(s) with {len(RULES)} rules â all clear.",
        border_style="green"
    ))
else:
    display_count = len(display)
    title_suffix  = f" â showing {display_count} of {len(unique)}" if len(unique) > MAX_FINDINGS else f" â {len(unique)} found"
    findings_table = Table(
        title=f"ð Findings{title_suffix}",
        box=box.ROUNDED, border_style="red", show_lines=True
    )
    findings_table.add_column("ID",       style="dim",    width=7)
    findings_table.add_column("Sev",      style="white",  width=9)
    findings_table.add_column("Cat",      style="cyan",   width=10)
    findings_table.add_column("File:Line",style="yellow", width=28)
    findings_table.add_column("Issue",    style="white",  width=45)

    for fi in display:
        sc   = SEV_COLOUR.get(fi["severity"], "white")
        loc  = f"{fi['file'][-24:]}:{fi['line']}" if len(fi["file"]) > 24 else f"{fi['file']}:{fi['line']}"
        findings_table.add_row(
            fi["id"],
            f"[{sc}]{fi['severity'].upper()}[/{sc}]",
            fi["category"],
            loc,
            fi["message"][:43],
        )
    console.print(findings_table)

    # Detailed panels for critical/high
    critical_high = [f for f in display if f["severity"] in ("critical", "high")]
    if critical_high:
        console.print()
        for fi in critical_high[:5]:
            sc = SEV_COLOUR.get(fi["severity"], "white")
            console.print(Panel(
                f"[dim]File:[/dim]  {fi['file']}:{fi['line']}\n"
                f"[dim]Code:[/dim]  [italic]{fi['code']}[/italic]\n\n"
                f"[white]{fi['message']}[/white]\n\n"
                f"[green]Fix:[/green] {fi['fix']}",
                title=f"[{sc}][bold]{fi['severity'].upper()}[/bold][/{sc}] â {fi['id']}",
                border_style=sc
            ))

    # Summary by severity
    console.print()
    sev_counts = {s: sum(1 for f in unique if f["severity"] == s)
                  for s in ("critical", "high", "medium", "low")}
    summary_lines = "  ".join(
        f"[{SEV_COLOUR[s]}]{s.title()}: {sev_counts[s]}[/{SEV_COLOUR[s]}]"
        for s in ("critical", "high", "medium", "low") if sev_counts[s]
    )
    console.print(Panel(
        f"Files scanned: [yellow]{len(files)}[/yellow]   "
        f"Total issues: [red]{len(unique)}[/red]   {summary_lines}",
        title="Summary",
        border_style="cyan"
    ))

# ââ Save outputs ââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââââ
report_file = f"argus_report_{TODAY}.md"
with open(report_file, "w", encoding="utf-8") as f:
    f.write(f"# ð Argus Code Scan Report â {TODAY}\n\n")
    f.write(f"**Path:** `{SRC_PATH}`  **Language:** {lang}  **Files:** {len(files)}  **Issues:** {len(unique)}\n\n")
    sev_counts = {s: sum(1 for fi in unique if fi["severity"] == s) for s in ("critical","high","medium","low")}
    f.write(f"**Critical:** {sev_counts['critical']}  **High:** {sev_counts['high']}  **Medium:** {sev_counts['medium']}  **Low:** {sev_counts['low']}\n\n")
    f.write("## Findings\n\n| ID | Severity | Category | File:Line | Issue |\n|---|---|---|---|---|\n")
    for fi in unique:
        f.write(f"| {fi['id']} | {fi['severity'].upper()} | {fi['category']} | {fi['file'][:30]}:{fi['line']} | {fi['message'][:60]} |\n")
    f.write("\n## Fix Suggestions\n\n")
    for fi in [x for x in unique if x["severity"] in ("critical","high")]:
        f.write(f"### {fi['id']} â {fi['file']}:{fi['line']}\n\n")
        f.write(f"**Issue:** {fi['message']}\n\n")
        f.write(f"**Fix:** {fi['fix']}\n\n")
        f.write(f"{FENCE}\n{fi['code']}\n{FENCE}\n\n")

if OUTPUT_JSON:
    json_file = f"argus_report_{TODAY}.json"
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump({"scanned": str(TODAY), "path": SRC_PATH, "language": lang,
                   "files": len(files), "findings": unique}, f, indent=2)
    console.print(f"[dim]JSON saved to {json_file}[/dim]")

console.print(Panel(
    f"[green]â Scan complete![/green]  Report saved to [cyan]{report_file}[/cyan]",
    border_style="green"
))
```
