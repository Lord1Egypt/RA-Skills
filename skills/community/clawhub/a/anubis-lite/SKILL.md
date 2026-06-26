---
name: anubis-lite
description: "Anubis Lite -- Career Application Engine. Paste a job description and get tailored resume bullet points in seconds. Free tier."
version: "1.0.0"
metadata:
  openclaw:
    requires:
      env: [JOB_DESCRIPTION]
      bins: [python3, pip3]
    primaryEnv: JOB_DESCRIPTION
    emoji: "🐺📄"
    homepage: https://clawhub.ai/occupythemilkyway/anubis-lite
    tags: [resume, career, job, application, cover-letter, ats, free, lite, anubis]
    envVars:
      - name: JOB_DESCRIPTION
        required: true
        description: "The full job description text (paste the entire posting)"
---

# Anubis Lite -- Career Application Engine

Anubis weighs every word. Feed it a job description and it tells you exactly how to position yourself.

## Free vs Standard vs Pro

| Feature | Anubis Lite (Free) | Anubis Standard ($5) | Anubis Pro ($9) |
|---------|-------------------|---------------------|-----------------|
| ATS keyword extraction | Yes | Yes | Yes |
| Resume bullet tailoring | 5 bullets | Full resume rewrite | Full resume + formatting |
| Cover letter | No | Yes (full) | Yes (3 tone variants) |
| Interview prep | No | No | 10 Q&A pairs |
| Follow-up emails | No | No | Yes (3 templates) |
| Application tracker | No | No | Yes (.md log) |

**Upgrade:** Anubis Standard -> ko-fi.com/occupythemilkyway ($5)

---

## Step 1 -- Install

```bash
pip3 install rich --break-system-packages --quiet
```

---

## Step 2 -- Parse job description

```python
import os, sys, re
from collections import Counter
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box

console = Console()

JD = os.environ.get("JOB_DESCRIPTION", "").strip()
if not JD:
    console.print(Panel("[red]JOB_DESCRIPTION is required.[/red]\nPaste the full job posting text.", title="Error", border_style="red"))
    sys.exit(1)

console.print()
console.print(Panel.fit(
    f"[bold magenta]🐺 Anubis Lite -- Career Application Engine[/bold magenta]\n"
    f"[dim]Free tier -- ATS keywords + 5 tailored resume bullets[/dim]",
    border_style="magenta"
))

# Extract ATS keywords
TECH_KEYWORDS = [
    "python","javascript","typescript","react","node","sql","aws","azure","gcp","docker",
    "kubernetes","machine learning","ai","data","api","rest","graphql","ci/cd","agile","scrum",
    "product","management","leadership","analytics","excel","tableau","salesforce","java","go",
    "rust","c++","ruby","php","swift","kotlin","tensorflow","pytorch","spark","kafka"
]
SOFT_SKILLS = ["communication","collaboration","problem-solving","leadership","analytical",
               "strategic","cross-functional","stakeholder","detail-oriented","fast-paced"]

jd_lower = JD.lower()
found_tech   = [k for k in TECH_KEYWORDS if k in jd_lower]
found_soft   = [k for k in SOFT_SKILLS if k in jd_lower]

# Extract years of experience requirements
exp_matches = re.findall(r"(\d+)\+?\s*(?:to\s*\d+)?\s*years?", JD, re.IGNORECASE)
exp_req = exp_matches[0] if exp_matches else "Not specified"

# Extract role title (first line usually)
role_title = JD.split("\n")[0].strip()[:80]

tbl = Table(title="Job Posting Analysis", box=box.ROUNDED, border_style="magenta")
tbl.add_column("Category", style="dim")
tbl.add_column("Found", style="cyan")
tbl.add_row("Role", role_title)
tbl.add_row("Experience req", f"{exp_req} years")
tbl.add_row("Technical keywords", ", ".join(found_tech[:10]) or "None detected")
tbl.add_row("Soft skills", ", ".join(found_soft[:6]) or "None detected")
console.print(tbl)

# Print full JD for Claude
print(f"\n=== FULL JOB DESCRIPTION ===\n{JD}\n=== END JD ===")
```

---

## Step 3 -- Generate tailored bullets

Based on the job description above, generate:

**1. ATS Keyword Report:**
List every important keyword, skill, and phrase from the job posting that a resume MUST include to pass ATS screening. Group them: Required Skills | Nice-to-Have | Soft Skills | Action Verbs Used in JD.

**2. 5 Tailored Resume Bullets:**
Write 5 powerful resume bullet points a candidate should use for this role. Each bullet:
- Starts with a strong action verb from the JD
- Includes a metric or quantifiable result (use [X%] or [N] as placeholders if needed)
- Mirrors the language of the job description
- Is 1-2 lines, achievement-focused

Format: `• [Verb] [what you did] by [how] resulting in [measurable outcome]`

**3. Quick Positioning Statement:**
2-3 sentences the candidate can use as their resume summary for this specific role.

---

## Step 4 -- Upsell

```python
from rich.console import Console
from rich.panel import Panel
console = Console()
console.print()
console.print(Panel(
    "[bold magenta]Anubis Standard ($5)[/bold magenta] does a full resume rewrite + complete cover letter tailored to this exact job.\n"
    "[bold cyan]Anubis Pro ($9)[/bold cyan] adds 10 interview Q&As, 3 follow-up email templates, and an application tracker.\n\n"
    "Upgrade: [bold cyan]ko-fi.com/occupythemilkyway[/bold cyan]",
    title="[magenta]Want the full application package?[/magenta]",
    border_style="magenta"
))
```
