---
name: argus-lite
description: "Argus Lite â Code Scanner (Free). Scan a single Python file for the top 10 most critical security and bug patterns. A free preview of what Argus Pro does for your full codebase."
version: "1.0.4"
metadata:
  openclaw:
    requires:
      env: []
      bins: [python3, pip3]
    primaryEnv: "SOURCE_PATH"
    homepage: https://clawhub.ai/occupythemilkyway/argus-lite
    emoji: "ð"
    tags: [debugging, security, code-review, python, free, lite, argus, linter]
    envVars:
      - name: SOURCE_PATH
        required: false
        description: "Path to a single Python file to scan (Lite: one file at a time)"
        default: "."
---

# Argus Lite â Free Code Scanner

Scan one Python file against the top 10 critical security and bug rules.

## Free vs Pro

| Feature | Argus Lite (Free) | Argus Pro |
|---------|------------------|-----------|
| Files | **1 file only** | Full directory recursion |
| Rules | **10 (critical/high)** | 40+ incl. performance |
| Languages | Python only | Python + JavaScript |
| JSON output | â | â CI-ready |
| CI exit codes | â | â FAIL_ON_CRITICAL |
| Ignore paths | â | â |
| Deduplication | Basic | Smart cross-file |

ð **Upgrade:** `openclaw skills install argus-pro` â key at **ko-fi.com/s/8b27346505**

ð° **Bundle deal:** all 5 Pro skills for **$29** â **ko-fi.com/s/7625accf3f** (save $16)

---

## Step 1 â Install

```bash
pip3 install rich --break-system-packages --quiet
```

---

## Step 2 â Quick security scan (Lite)

```python
import os, re
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

console = Console()

SRC_PATH = os.environ.get("SOURCE_PATH",".").strip()
src      = Path(SRC_PATH)

# Find a single Python file to scan
if src.is_dir():
    py_files = list(src.rglob("*.py"))
    if not py_files:
        console.print(f"[yellow]No .py files found in {SRC_PATH}[/yellow]")
        raise SystemExit(0)
    target = py_files[0]
    if len(py_files) > 1:
        console.print(f"[yellow]â¹ï¸  Lite scans 1 file at a time. Scanning: {target}\n   (Upgrade to Pro to scan all {len(py_files)} files)[/yellow]\n")
elif src.is_file():
    target = src
else:
    console.print(f"[red]â Not found: {SRC_PATH}[/red]")
    raise SystemExit(1)

# Top 10 critical/high rules only (Lite)
RULES = [
    ("PY001","critical","security", r"\beval\s*\(",                           "eval() executes arbitrary code â critical risk.",         "Use ast.literal_eval() for safe evaluation."),
    ("PY002","critical","security", r"\bexec\s*\(",                           "exec() executes arbitrary strings as Python code.",       "Refactor to eliminate dynamic execution."),
    ("PY003","critical","security", r"\bpickle\.loads?\s*\(",                 "pickle.load() with untrusted data â code execution.",     "Use json.loads() instead."),
    ("PY004","high","security",     r"(?i)(password|secret|api_key|token)\s*=\s*['\"].+['\"]","Hardcoded credential detected.",          "Move to environment variables."),
    ("PY005","high","security",     r"shell\s*=\s*True",                      "shell=True in subprocess â command injection risk.",      "Use list arguments: subprocess.run(['cmd','arg'])"),
    ("PY006","high","security",     r"\.execute\s*\(.*(%|\.format\(|f['\"])", "Potential SQL injection via string formatting.",          "Use parameterised queries: cursor.execute(sql,(val,))"),
    ("PY009","medium","bug",        r"except\s*:",                            "Bare except catches SystemExit and KeyboardInterrupt.",   "Use: except Exception: or catch specific types."),
    ("PY016","medium","security",   r"hashlib\.(md5|sha1)\s*\(",              "MD5/SHA1 are cryptographically broken.",                  "Use hashlib.sha256() or bcrypt for passwords."),
    ("PY007","medium","bug",        r"def\s+\w+\s*\([^)]*=\s*\[\s*\]",      "Mutable default argument [] â shared across all calls.",  "Use None as default; init list inside function."),
    ("PY017","high","security",     r"\brandom\.(random|randint|choice)\s*\(","random module is not cryptographically secure.",          "Use secrets module for security-sensitive values."),
]

console.print(Panel.fit(
    f"[bold red]ð Argus Lite â Quick Scan[/bold red]\n"
    f"File: [yellow]{target}[/yellow]\n"
    f"[dim]Lite: 1 file, 10 rules â upgrade to Pro for full codebase scanning[/dim]",
    border_style="red"
))

findings = []
try:
    source = target.read_text(encoding="utf-8", errors="replace")
    for lineno, line in enumerate(source.splitlines(), 1):
        for rule_id, sev, category, pattern, message, fix in RULES:
            if re.search(pattern, line):
                findings.append({"id":rule_id,"severity":sev,"category":category,
                                 "line":lineno,"code":line.strip()[:80],"message":message,"fix":fix})
except Exception as e:
    console.print(f"[red]Error reading file: {e}[/red]")
    raise SystemExit(1)

# Deduplicate
seen, unique = set(), []
for f in findings:
    key = (f["id"],f["line"])
    if key not in seen:
        seen.add(key)
        unique.append(f)

SEV_COLOUR = {"critical":"red","high":"orange3","medium":"yellow","low":"dim"}

if not unique:
    console.print(Panel(
        f"[green]â No issues in {RULES.__len__()} rule scan![/green]\n"
        f"[dim]Pro scans 40+ rules including performance patterns â upgrade for full coverage.[/dim]",
        border_style="green"
    ))
else:
    tbl = Table(title=f"ð {len(unique)} Finding(s) in {target.name}", box=box.ROUNDED, border_style="red")
    tbl.add_column("ID",      width=7,  style="dim")
    tbl.add_column("Sev",     width=9)
    tbl.add_column("Line",    width=6,  justify="right", style="yellow")
    tbl.add_column("Issue",   width=50)
    for fi in unique:
        sc = SEV_COLOUR.get(fi["severity"],"white")
        tbl.add_row(fi["id"],f"[{sc}]{fi['severity'].upper()}[/{sc}]",str(fi["line"]),fi["message"][:48])
    console.print(tbl)

    for fi in [f for f in unique if f["severity"] in ("critical","high")]:
        sc = SEV_COLOUR.get(fi["severity"],"white")
        console.print(Panel(
            f"[dim]Line {fi['line']}:[/dim] [italic]{fi['code']}[/italic]\n\n"
            f"[white]{fi['message']}[/white]\n\n"
            f"[green]Fix:[/green] {fi['fix']}",
            title=f"[{sc}]{fi['severity'].upper()}[/{sc}] â {fi['id']}",
            border_style=sc
        ))

console.print()
console.print(Panel(
    f"[bold yellow]ð Want more?[/bold yellow]\n\n"
    f"Argus Pro scans [bold]your entire codebase[/bold] with [bold]40+ rules[/bold] across Python and JavaScript â "
    f"including performance issues, memory leaks, and N+1 query patterns. "
    f"Plus CI-ready JSON output and FAIL_ON_CRITICAL exit codes.\n\n"
    f"[bold cyan]openclaw skills install argus-pro[/bold cyan]\n"
    f"Get your key â [bold]ko-fi.com/s/8b27346505[/bold]",
    title="Upgrade to Argus Pro",
    border_style="cyan"
))
```
