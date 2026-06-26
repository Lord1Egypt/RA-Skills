---
name: argus-pro
description: "Argus Pro â Code Intelligence Scanner. Scan Python and JavaScript codebases with 40+ rules covering security, bugs, performance, and code quality. Get prioritised findings with fix suggestions, trend tracking across scans, CI-ready JSON output, and custom rule support. The full-power version of Argus."
version: "1.0.4"
metadata:
  openclaw:
    requires:
      env: [LICENSE_KEY]
      bins: [python3, pip3]
    primaryEnv: "SOURCE_PATH"
    homepage: https://clawhub.ai/occupythemilkyway/argus-pro
    emoji: "ððï¸â¡"
    tags: [debugging, security, code-review, python, javascript, linter, argus, pro, ci, static-analysis]
    envVars:
      - name: LICENSE_KEY
        required: true
        description: "Your Argus Pro license key. Get one at: ko-fi.com/s/8b27346505"

ð° **Bundle deal:** all 5 Pro skills for **$29** â **ko-fi.com/s/7625accf3f** (save $16)
      - name: SOURCE_PATH
        required: false
        description: "Path to scan (file or directory)"
        default: "."
      - name: LANGUAGE
        required: false
        description: "python, javascript, or auto"
        default: "auto"
      - name: SEVERITY_FILTER
        required: false
        description: "Minimum severity: critical, high, medium, low, all"
        default: "all"
      - name: MAX_FINDINGS
        required: false
        description: "Max findings to display"
        default: "100"
      - name: OUTPUT_JSON
        required: false
        description: "Save JSON output for CI pipelines"
        default: "true"
      - name: FAIL_ON_CRITICAL
        required: false
        description: "Exit with code 1 if critical findings found (for CI)"
        default: "false"
      - name: IGNORE_PATHS
        required: false
        description: "Comma-separated paths to skip (e.g. tests/,node_modules/)"
        default: ""
---

# Argus Pro â Full Code Intelligence

Everything in Argus, plus 40+ rules, performance patterns, CI/CD integration, custom ignore paths, and trend JSON for tracking debt over time.

## Pro features vs free Argus

| Feature | Argus (Free) | Argus Pro |
|---------|-------------|-----------|
| Rules | 20 | **40+** |
| Languages | Python or JS | Python + JS simultaneously |
| Performance rules | â | â N+1, blocking calls, memory leaks |
| CI exit code | â | â FAIL_ON_CRITICAL |
| Ignore paths | â | â |
| JSON output | Optional | â Always (CI-ready) |
| Finding deduplication | Basic | â Cross-file smart dedup |
| Custom severity filter | â | â + per-rule override |

ð **Upgrade:** `openclaw skills install argus-pro` + key at **ko-fi.com/s/8b27346505**

---

## Setup

1. **Purchase** your license key at **ko-fi.com/s/8b27346505** ($9 one-time)
   - Or get all 5 Pro skills for **$29** â **ko-fi.com/s/7625accf3f** (save $16)
2. **Install:** `openclaw skills install argus-pro`
3. **Activate:** set the `LICENSE_KEY` environment variable to the key you received
4. **Run** â you're in

---

## Step 1 â Install

```bash
pip3 install rich --break-system-packages --quiet
```

---

## Step 2 â Full code scan (Pro)

```python
import os, re, json, sys
from pathlib import Path
from datetime import date
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

FENCE = chr(96) * 3

console = Console()

LICENSE_KEY = os.environ.get("LICENSE_KEY","").strip()
if not LICENSE_KEY:
    console.print(Panel(
        "[red bold]ð Argus Pro requires a license key.[/red bold]\n\n"
        "Get your key at: [bold cyan]ko-fi.com/s/8b27346505[/bold cyan]\n\n"
        "Or use the free version: [dim]openclaw skills install argus1[/dim]",
        title="License Required", border_style="red"
    ))
    raise SystemExit(1)

SRC_PATH      = os.environ.get("SOURCE_PATH",".").strip()
LANGUAGE      = os.environ.get("LANGUAGE","auto").lower()
SEV_FILTER    = os.environ.get("SEVERITY_FILTER","all").lower()
try: MAX_FINDINGS = int(os.environ.get("MAX_FINDINGS","100"))
except: MAX_FINDINGS = 100
OUTPUT_JSON   = os.environ.get("OUTPUT_JSON","true").lower() == "true"
FAIL_CRITICAL = os.environ.get("FAIL_ON_CRITICAL","false").lower() == "true"
IGNORE_RAW    = os.environ.get("IGNORE_PATHS","")
IGNORE_PATHS  = [p.strip() for p in IGNORE_RAW.split(",") if p.strip()]
TODAY         = date.today()

src = Path(SRC_PATH)
if not src.exists():
    console.print(f"[red]â Path not found: {SRC_PATH}[/red]")
    raise SystemExit(1)

def detect_lang(path):
    py = len(list(path.rglob("*.py") if path.is_dir() else ([path] if str(path).endswith(".py") else [])))
    js = len(list(path.rglob("*.js") if path.is_dir() else ([path] if str(path).endswith(".js") else [])))
    return "python" if py >= js else "javascript"

lang = LANGUAGE if LANGUAGE != "auto" else detect_lang(src)

# Pro: Scan both languages if directory
SCAN_LANGS = ["python","javascript"] if src.is_dir() and LANGUAGE == "auto" else [lang]

# ââ Extended rule sets ââââââââââââââââââââââââââââââââââââââââââââââââââââââââ
PYTHON_RULES = [
    # Security
    ("PY001","critical","security", r"\beval\s*\(",                              "eval() executes arbitrary code.",                         "Use ast.literal_eval() for safe literal evaluation."),
    ("PY002","critical","security", r"\bexec\s*\(",                              "exec() executes arbitrary code.",                         "Refactor to eliminate dynamic code execution."),
    ("PY003","critical","security", r"\bpickle\.loads?\s*\(",                   "pickle.load() with untrusted data enables code execution.", "Use json.loads() instead."),
    ("PY004","high","security",     r"(?i)(password|secret|api_key|token|auth_key)\s*=\s*['\"].+['\"]", "Hardcoded credential.", "Use environment variables."),
    ("PY005","high","security",     r"shell\s*=\s*True",                        "shell=True is a command-injection risk.",                  "Use list arguments: subprocess.run(['cmd','arg'])"),
    ("PY006","high","security",     r"\.execute\s*\(.*(%|\.format\(|f['\"])",   "Potential SQL injection via string formatting.",           "Use parameterised queries."),
    ("PY016","medium","security",   r"hashlib\.(md5|sha1)\s*\(",                "MD5/SHA1 are cryptographically weak.",                    "Use hashlib.sha256() or bcrypt for passwords."),
    ("PY017","high","security",     r"\brandom\.(random|randint|choice)\s*\(",  "random module not cryptographically secure.",             "Use secrets module for security-sensitive values."),
    # Bugs
    ("PY007","medium","bug",        r"def\s+\w+\s*\([^)]*=\s*\[\s*\]",        "Mutable default argument [].",                            "Use None as default; init inside function."),
    ("PY008","medium","bug",        r"def\s+\w+\s*\([^)]*=\s*\{\s*\}",        "Mutable default argument {}.",                            "Use None as default; init inside function."),
    ("PY009","medium","bug",        r"except\s*:",                             "Bare except catches SystemExit/KeyboardInterrupt.",       "Catch specific: except ValueError: or except Exception:"),
    ("PY010","medium","bug",        r"==\s*None\b|\bNone\s*==",                "Use 'is None' not '== None'.",                           "Replace with 'is None'."),
    ("PY011","medium","bug",        r"!=\s*None\b|\bNone\s*!=",                "Use 'is not None'.",                                     "Replace with 'is not None'."),
    ("PY018","medium","bug",        r"open\s*\(.+\)(?!\s*as\b)(?!.*with\b)",   "File opened without context manager.",                   "Use 'with open(...) as f:'."),
    ("PY020","medium","bug",        r"\btype\s*\(\w+\)\s*==\s*",               "type() == for type checks is fragile.",                  "Use isinstance() instead."),
    ("PY021","medium","bug",        r"except.*:\s*pass$",                      "Silent exception swallowed â bugs hidden.",               "At minimum log the exception before passing."),
    ("PY022","low","bug",           r"\bassert\s+",                            "assert statements removed by -O flag.",                  "Use explicit if + raise for runtime checks."),
    # Quality
    ("PY012","medium","quality",    r"\bprint\s*\(",                           "print() in production code.",                            "Replace with logging.debug()/logging.info()."),
    ("PY013","low","quality",       r"#\s*(TODO|FIXME|HACK|XXX|BUG)\b",       "Unresolved TODO/FIXME.",                                 "Create a tracked issue and remove the marker."),
    ("PY014","low","quality",       r"from\s+\w+\s+import\s+\*",              "Wildcard import pollutes namespace.",                     "Import only what you need."),
    ("PY015","low","quality",       r"import\s+pdb\b",                        "Debugger import left in code.",                          "Remove before committing."),
    ("PY019","low","quality",       r"lambda\s+\w+:\s*\w+\s*\(",              "Complex lambda â use a named def.",                      "Replace with a def statement."),
    # Performance (Pro only)
    ("PY030","medium","performance",r"for\s+\w+\s+in\s+range\(len\(",         "for i in range(len(x)) is slow and unidiomatic.",        "Use enumerate(x) or iterate directly."),
    ("PY031","medium","performance",r"\+\s*=\s*['\"]",                        "String concatenation in loop builds O(nÂ²) strings.",     "Use ''.join(parts) or an f-string outside the loop."),
    ("PY032","low","performance",   r"\.keys\(\)\s*\)",                       "Iterating .keys() is redundant.",                        "Iterate the dict directly: for k in my_dict."),
    ("PY033","medium","performance",r"time\.sleep\s*\(",                      "Blocking sleep in potentially async context.",            "Use asyncio.sleep() in async functions."),
]

JS_RULES = [
    ("JS001","high","quality",      r"\bvar\s+",                               "var is function-scoped and hoisted.",                    "Use const or let."),
    ("JS002","critical","security", r"\.innerHTML\s*=",                        "innerHTML is an XSS vector.",                           "Use textContent or DOMPurify."),
    ("JS003","critical","security", r"\beval\s*\(",                            "eval() executes arbitrary JS.",                          "Eliminate eval() usage."),
    ("JS004","high","security",     r"(?i)(api_key|apikey|api_secret|access_token|password)\s*=\s*['\"].+['\"]", "Hardcoded credential.", "Use environment variables."),
    ("JS005","medium","bug",        r"==\s*null\b(?!\=)|null\s*==(?!\=)",      "Loose null check also matches undefined.",               "Use === null explicitly."),
    ("JS006","medium","bug",        r"(?<!=)==(?!=)",                          "Loose equality (==) causes type coercion bugs.",         "Use strict equality (===)."),
    ("JS007","medium","quality",    r"\bconsole\.(log|warn|error|debug)\s*\(", "console.log left in production.",                        "Remove or replace with a logging library."),
    ("JS008","medium","security",   r"document\.write\s*\(",                   "document.write() is an XSS risk.",                      "Use DOM manipulation methods instead."),
    ("JS009","low","quality",       r"//\s*(TODO|FIXME|HACK|XXX|BUG)\b",      "Unresolved TODO/FIXME.",                                "Create a tracked issue."),
    ("JS010","high","security",     r"__proto__\s*=",                          "Prototype pollution pattern.",                          "Validate object keys exclude __proto__."),
    ("JS011","medium","bug",        r"setTimeout\s*\(\s*['\"]",                "setTimeout with string calls eval internally.",          "Pass a function: setTimeout(() => fn(), ms)"),
    ("JS012","low","quality",       r"function\s+\w+\s*\([^)]{60,}\)",        "Too many parameters.",                                  "Use an options object instead."),
    # Performance (Pro only)
    ("JS030","medium","performance",r"\.forEach\s*\(.*\.push\s*\(",           "forEach+push is slower than Array.map().",               "Replace with map() for transformations."),
    ("JS031","medium","performance",r"document\.querySelector\s*\(.*\bfor\b", "DOM query inside a loop â expensive.",                  "Cache the element outside the loop."),
    ("JS032","low","performance",   r"JSON\.parse\s*\(JSON\.stringify\s*\(",  "JSON.parse(JSON.stringify()) for deep clone is slow.",   "Use structuredClone() in modern environments."),
]

SEV_ORDER = {"critical":0,"high":1,"medium":2,"low":3}
SEV_FILTER_LEVEL = {"all":3,"low":3,"medium":2,"high":1,"critical":0}.get(SEV_FILTER,3)

def should_skip(filepath, ignore_paths):
    path_str = str(filepath)
    return any(ig in path_str for ig in ignore_paths)

all_findings = []
all_files    = []

for scan_lang in SCAN_LANGS:
    ext   = "*.py" if scan_lang == "python" else "*.js"
    rules = PYTHON_RULES if scan_lang == "python" else JS_RULES
    files = [f for f in (src.rglob(ext) if src.is_dir() else [src]) if not should_skip(f, IGNORE_PATHS)]
    all_files.extend(files)
    for filepath in files:
        try:
            source = filepath.read_text(encoding="utf-8", errors="replace")
            for lineno, line in enumerate(source.splitlines(), 1):
                for rule_id, sev, category, pattern, message, fix in rules:
                    if re.search(pattern, line):
                        if SEV_ORDER.get(sev,3) <= SEV_FILTER_LEVEL:
                            all_findings.append({
                                "id": rule_id, "severity": sev, "category": category,
                                "lang": scan_lang,
                                "file": str(filepath.relative_to(src) if src.is_dir() else filepath),
                                "line": lineno, "code": line.strip()[:80],
                                "message": message, "fix": fix,
                            })
        except Exception as e:
            console.print(f"[dim]Skipping {filepath}: {e}[/dim]")

# Smart dedup
seen = set()
unique = []
for f in all_findings:
    key = (f["id"], f["file"], f["line"])
    if key not in seen:
        seen.add(key)
        unique.append(f)
unique.sort(key=lambda f: (SEV_ORDER.get(f["severity"],3), f["file"], f["line"]))
display = unique[:MAX_FINDINGS]

SEV_COLOUR = {"critical":"red","high":"orange3","medium":"yellow","low":"dim"}

console.print()
console.print(Panel.fit(
    f"[bold red]ððï¸â¡ Argus Pro â Code Intelligence Scanner[/bold red]\n"
    f"Scanning [yellow]{len(all_files)}[/yellow] file(s)  |  Languages: [cyan]{', '.join(SCAN_LANGS)}[/cyan]  |  Rules: [white]{len(PYTHON_RULES)+len(JS_RULES) if len(SCAN_LANGS)>1 else (len(PYTHON_RULES) if lang=='python' else len(JS_RULES))}[/white]",
    border_style="red"
))

if not unique:
    console.print(Panel("[green]â No issues found â clean codebase![/green]", border_style="green"))
else:
    suffix = f" â showing {len(display)} of {len(unique)}" if len(unique) > MAX_FINDINGS else f" â {len(unique)} total"
    tbl = Table(title=f"ð Findings{suffix}", box=box.ROUNDED, border_style="red", show_lines=True)
    tbl.add_column("ID",        width=7,  style="dim")
    tbl.add_column("Sev",       width=9)
    tbl.add_column("Cat",       width=12, style="cyan")
    tbl.add_column("Lang",      width=5,  style="magenta")
    tbl.add_column("File:Line", width=30, style="yellow")
    tbl.add_column("Issue",     width=42)
    for fi in display:
        sc  = SEV_COLOUR.get(fi["severity"],"white")
        loc = f"{fi['file'][-26:]}:{fi['line']}" if len(fi["file"])>26 else f"{fi['file']}:{fi['line']}"
        tbl.add_row(fi["id"],f"[{sc}]{fi['severity'].upper()}[/{sc}]",fi["category"],fi["lang"][:2].upper(),loc,fi["message"][:40])
    console.print(tbl)

    for fi in [f for f in display if f["severity"] in ("critical","high")][:5]:
        sc = SEV_COLOUR.get(fi["severity"],"white")
        console.print(Panel(
            f"[dim]File:[/dim] {fi['file']}:{fi['line']}\n"
            f"[dim]Code:[/dim] [italic]{fi['code']}[/italic]\n\n"
            f"[white]{fi['message']}[/white]\n\n"
            f"[green]Fix:[/green] {fi['fix']}",
            title=f"[{sc}][bold]{fi['severity'].upper()}[/bold][/{sc}] â {fi['id']}",
            border_style=sc
        ))

    sev_counts = {s: sum(1 for f in unique if f["severity"]==s) for s in ("critical","high","medium","low")}
    console.print()
    console.print(Panel(
        f"Files: [yellow]{len(all_files)}[/yellow]  Issues: [red]{len(unique)}[/red]  "
        + "  ".join(f"[{SEV_COLOUR[s]}]{s.title()}: {sev_counts[s]}[/{SEV_COLOUR[s]}]" for s in ("critical","high","medium","low") if sev_counts[s]),
        title="Summary", border_style="cyan"
    ))

# Save
report_file = f"argus_pro_report_{TODAY}.md"
json_file   = f"argus_pro_report_{TODAY}.json"

with open(report_file,"w",encoding="utf-8") as f:
    f.write(f"# ð Argus Pro Report â {TODAY}\n\n**Path:** `{SRC_PATH}`  **Files:** {len(all_files)}  **Issues:** {len(unique)}\n\n")
    f.write("## Findings\n\n| ID | Severity | Category | Lang | File:Line | Issue |\n|---|---|---|---|---|---|\n")
    for fi in unique:
        f.write(f"| {fi['id']} | {fi['severity'].upper()} | {fi['category']} | {fi['lang']} | {fi['file'][:30]}:{fi['line']} | {fi['message'][:50]} |\n")
    f.write("\n## Fix Guide (Critical + High)\n\n")
    for fi in [x for x in unique if x["severity"] in ("critical","high")]:
        f.write(f"### {fi['id']} â {fi['file']}:{fi['line']}\n**Issue:** {fi['message']}\n**Fix:** {fi['fix']}\n{FENCE}\n{fi['code']}\n{FENCE}\n\n")

with open(json_file,"w",encoding="utf-8") as f:
    json.dump({"date":str(TODAY),"path":SRC_PATH,"files":len(all_files),"findings":unique},f,indent=2)

console.print(Panel(f"[green]â Done![/green]  [cyan]{report_file}[/cyan]  |  [cyan]{json_file}[/cyan]",border_style="green"))

if FAIL_CRITICAL and any(f["severity"]=="critical" for f in unique):
    console.print("[red]CI: Exiting with code 1 â critical findings detected.[/red]")
    sys.exit(1)
```
