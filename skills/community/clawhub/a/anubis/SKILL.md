---
name: anubis
description: "Anubis Standard -- Career Application Engine. Full resume rewrite + cover letter tailored to a specific job. ATS-optimised. Saved to files."
version: "1.0.0"
metadata:
  openclaw:
    requires:
      env: [JOB_DESCRIPTION, RESUME_PATH, LICENSE_KEY]
      bins: [python3, pip3]
    primaryEnv: JOB_DESCRIPTION
    emoji: "🐺📋"
    homepage: https://clawhub.ai/occupythemilkyway/anubis
    tags: [resume, career, job, cover-letter, ats, keywords, standard, anubis]
    envVars:
      - name: LICENSE_KEY
        required: true
        description: "Your Anubis Standard license key. Get one at: ko-fi.com/occupythemilkyway"
      - name: JOB_DESCRIPTION
        required: true
        description: "The full job description text"
      - name: RESUME_PATH
        required: true
        description: "Path to your current resume file (.txt, .md, or .pdf text)"
      - name: YOUR_NAME
        required: false
        description: "Your name for the cover letter"
        default: ""
      - name: COVER_TONE
        required: false
        description: "Cover letter tone: professional | conversational | executive (default: professional)"
        default: "professional"
      - name: OUTPUT_DIR
        required: false
        description: "Where to save outputs (default: ./anubis_output)"
        default: "./anubis_output"
---

# Anubis Standard -- Career Application Engine

Full resume rewrite tailored to a job description. ATS-optimised. Complete cover letter. All saved to files ready to submit.

---

## Step 1 -- Install

```bash
pip3 install rich --break-system-packages --quiet
```

---

## Step 2 -- Validate and load documents

```python
import os, sys, re
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.rule import Rule
from rich import box

console = Console()

LICENSE_KEY = os.environ.get("LICENSE_KEY", "").strip()
if not LICENSE_KEY or not LICENSE_KEY.startswith("ANUBIS-STD-"):
    console.print(Panel(
        "[red bold]Anubis Standard requires a license key.[/red bold]\n\n"
        "Get your key at: [bold cyan]ko-fi.com/occupythemilkyway[/bold cyan]\n\n"
        "Or use the free version: [dim]openclaw skills install anubis-lite[/dim]",
        title="License Required",
        border_style="red"
    ))
    sys.exit(1)

JD          = os.environ.get("JOB_DESCRIPTION", "").strip()
RESUME_PATH = os.environ.get("RESUME_PATH", "").strip()
YOUR_NAME   = os.environ.get("YOUR_NAME", "").strip()
COVER_TONE  = os.environ.get("COVER_TONE", "professional").lower().strip()
OUTPUT_DIR  = os.environ.get("OUTPUT_DIR", "./anubis_output").strip()

if not JD:
    console.print(Panel("[red]JOB_DESCRIPTION is required.[/red]", title="Error", border_style="red"))
    sys.exit(1)
if not RESUME_PATH or not os.path.exists(RESUME_PATH):
    console.print(Panel(f"[red]RESUME_PATH not found: {RESUME_PATH}[/red]", title="Error", border_style="red"))
    sys.exit(1)

os.makedirs(OUTPUT_DIR, exist_ok=True)

with open(RESUME_PATH, encoding="utf-8", errors="replace") as fh:
    resume_text = fh.read()

# ATS keyword extraction
TECH_KW = ["python","javascript","typescript","react","node","sql","aws","azure","gcp","docker",
           "kubernetes","machine learning","ai","data","api","rest","agile","scrum","product",
           "management","leadership","analytics","excel","tableau","salesforce","java","go"]
SOFT_KW = ["communication","collaboration","problem-solving","leadership","analytical",
           "strategic","cross-functional","stakeholder","detail-oriented"]

jd_lower = JD.lower()
ats_tech = [k for k in TECH_KW if k in jd_lower]
ats_soft = [k for k in SOFT_KW if k in jd_lower]
exp_match = re.findall(r"(\d+)\+?\s*years?", JD, re.IGNORECASE)
exp_req   = exp_match[0] + "+ years" if exp_match else "Not specified"
role_line = JD.split("\n")[0].strip()[:80]

console.print()
console.print(Panel.fit(
    f"[bold magenta]🐺 Anubis Standard -- Career Application Engine[/bold magenta]\n"
    f"Role:   [cyan]{role_line}[/cyan]\n"
    f"Exp:    [white]{exp_req}[/white]\n"
    f"Tone:   [white]{COVER_TONE}[/white]\n"
    f"Output: [green]{OUTPUT_DIR}/[/green]",
    border_style="magenta"
))

tbl = Table(title="ATS Analysis", box=box.SIMPLE, border_style="magenta")
tbl.add_column("Category", style="dim", width=20)
tbl.add_column("Keywords", style="cyan")
tbl.add_row("Technical", ", ".join(ats_tech) or "None detected")
tbl.add_row("Soft skills", ", ".join(ats_soft) or "None detected")
console.print(tbl)

console.print(Rule("[magenta]Loading documents...[/magenta]"))
print(f"\n=== CURRENT RESUME ===\n{resume_text}\n=== END RESUME ===")
print(f"\n=== JOB DESCRIPTION ===\n{JD}\n=== END JD ===")
```

---

## Step 3 -- Generate tailored application

Based on the resume and job description above, generate two complete documents:

**Document 1: TAILORED_RESUME.md**
Rewrite the candidate's resume to be perfectly tailored for this job:
- Reorder and rewrite ALL bullet points using action verbs from the JD
- Add/emphasize every ATS keyword found in the JD that legitimately applies
- Rewrite the summary/objective to match the role exactly
- Restructure sections if needed for this role type
- Preserve all true facts -- only reframe, never fabricate
- Format cleanly in markdown

**Document 2: COVER_LETTER.md**
Write a complete cover letter in the {COVER_TONE} tone:
- Opening: specific hook referencing something about the company or role
- Body paragraph 1: your strongest alignment with their top 2-3 requirements
- Body paragraph 2: a specific achievement that proves you can do the job
- Body paragraph 3: why THIS company specifically (research the company from JD clues)
- Closing: confident call to action
- Sign off with {YOUR_NAME} or "[Your Name]" if not provided

Both documents must be submission-ready. No placeholders unless genuinely unknown.

---

## Step 4 -- Save and confirm

```python
import os
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box
console = Console()

date_str    = datetime.now().strftime("%Y%m%d")
resume_out  = os.path.join(OUTPUT_DIR, f"tailored_resume_{date_str}.md")
letter_out  = os.path.join(OUTPUT_DIR, f"cover_letter_{date_str}.md")

tbl = Table(title="Anubis -- Application Package Ready", box=box.SIMPLE, border_style="green")
tbl.add_column("File", style="cyan")
tbl.add_column("Description", style="dim")
tbl.add_row(resume_out, "ATS-optimised tailored resume")
tbl.add_row(letter_out, f"Cover letter ({COVER_TONE} tone)")
console.print()
console.print(tbl)
console.print(Panel(
    "[bold green]Application package complete.[/bold green]\n\n"
    "Upgrade to [magenta]Anubis Pro ($9)[/magenta] for interview Q&As, follow-up email templates, and application tracking.\n"
    "-> [cyan]ko-fi.com/occupythemilkyway[/cyan]",
    border_style="green"
))
```

Save both files to OUTPUT_DIR using your file writing tool, then display the confirmation.
