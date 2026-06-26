---
name: anubis-pro
description: "Anubis Pro -- Full Career Application Suite. Tailored resume + 3-tone cover letter + 10 interview Q&As + follow-up emails + application tracker. The only career tool you need."
version: "1.0.0"
metadata:
  openclaw:
    requires:
      env: [JOB_DESCRIPTION, RESUME_PATH, LICENSE_KEY]
      bins: [python3, pip3]
    primaryEnv: JOB_DESCRIPTION
    emoji: "🐺⚡"
    homepage: https://clawhub.ai/occupythemilkyway/anubis-pro
    tags: [resume, career, job, cover-letter, interview, follow-up, tracker, ats, pro, anubis]
    envVars:
      - name: LICENSE_KEY
        required: true
        description: "Your Anubis Pro license key. Get one at: ko-fi.com/occupythemilkyway"
      - name: JOB_DESCRIPTION
        required: true
        description: "The full job description text"
      - name: RESUME_PATH
        required: true
        description: "Path to your current resume file (.txt or .md)"
      - name: YOUR_NAME
        required: false
        description: "Your full name"
        default: ""
      - name: COMPANY_NAME
        required: false
        description: "Company name (auto-detected from JD if blank)"
        default: ""
      - name: OUTPUT_DIR
        required: false
        description: "Output folder (default: ./anubis_pro_output)"
        default: "./anubis_pro_output"
---

# Anubis Pro -- Full Career Application Suite

The complete application package. Tailored resume, 3 cover letter tones, 10 role-specific interview Q&As, 3 follow-up email templates, and an application tracker log.

**Bundle deal:** All 5 Egyptian skills for $29 -> ko-fi.com/s/7625accf3f (save $16)

---

## Step 1 -- Install

```bash
pip3 install rich --break-system-packages --quiet
```

---

## Step 2 -- Validate and load

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
if not LICENSE_KEY or not LICENSE_KEY.startswith("ANUBIS-PRO-"):
    console.print(Panel(
        "[red bold]Anubis Pro requires a license key.[/red bold]\n\n"
        "Get your key at: [bold cyan]ko-fi.com/occupythemilkyway[/bold cyan]\n\n"
        "Or try Anubis Standard ($5): [dim]openclaw skills install anubis[/dim]",
        title="License Required",
        border_style="red"
    ))
    sys.exit(1)

JD           = os.environ.get("JOB_DESCRIPTION", "").strip()
RESUME_PATH  = os.environ.get("RESUME_PATH", "").strip()
YOUR_NAME    = os.environ.get("YOUR_NAME", "[Your Name]").strip() or "[Your Name]"
COMPANY_NAME = os.environ.get("COMPANY_NAME", "").strip()
OUTPUT_DIR   = os.environ.get("OUTPUT_DIR", "./anubis_pro_output").strip()

if not JD or not RESUME_PATH or not os.path.exists(RESUME_PATH):
    console.print(Panel("[red]JOB_DESCRIPTION and valid RESUME_PATH are required.[/red]", title="Error", border_style="red"))
    sys.exit(1)

os.makedirs(OUTPUT_DIR, exist_ok=True)

with open(RESUME_PATH, encoding="utf-8", errors="replace") as fh:
    resume_text = fh.read()

# Auto-detect company
if not COMPANY_NAME:
    m = re.search(r"(?:at|@|join)\s+([A-Z][a-zA-Z\s&]+?)(?:\s+is|\s+are|\s+we|\.|,)", JD)
    COMPANY_NAME = m.group(1).strip() if m else "the company"

role_line = JD.split("\n")[0].strip()[:80]

console.print()
console.print(Panel.fit(
    f"[bold magenta]🐺 Anubis Pro -- Full Career Suite[/bold magenta]\n"
    f"Role:    [cyan]{role_line}[/cyan]\n"
    f"Company: [white]{COMPANY_NAME}[/white]\n"
    f"Name:    [white]{YOUR_NAME}[/white]\n"
    f"Output:  [green]{OUTPUT_DIR}/[/green]",
    border_style="magenta"
))
console.print(Rule("[magenta]Generating full application package...[/magenta]"))
print(f"\n=== RESUME ===\n{resume_text}\n=== END RESUME ===")
print(f"\n=== JOB DESCRIPTION ===\n{JD}\n=== END JD ===")
```

---

## Step 3 -- Generate the full application suite

Generate FIVE documents:

**1. TAILORED_RESUME.md** -- Full resume rewrite, ATS-optimised, achievement-focused bullets mirroring JD language

**2. COVER_LETTER_PROFESSIONAL.md** -- Formal, structured cover letter
**3. COVER_LETTER_CONVERSATIONAL.md** -- Warm, personality-forward version  
**4. COVER_LETTER_EXECUTIVE.md** -- High-level, strategic, results-only version

**5. INTERVIEW_PREP.md** -- 10 role-specific interview questions with ideal answer frameworks:
- 3 behavioral (STAR format): based on the JD's key competencies
- 3 technical: based on the actual skills listed in the JD
- 2 situational: "What would you do if..." based on the role's challenges
- 2 questions FOR the interviewer: sharp questions that show deep interest
Each answer should include: the framework, 2-3 bullet points of what to cover, and a one-sentence power close.

**6. FOLLOW_UP_EMAILS.md** -- 3 follow-up email templates:
- 24-hour thank you email (post-interview)
- 1-week follow-up (if no response)
- 2-week final follow-up (polite close-loop)

**7. APPLICATION_LOG.md** -- Application tracker entry:
```
| Date | Company | Role | Status | Next Action | Deadline |
|------|---------|------|--------|-------------|----------|
| [TODAY] | [COMPANY] | [ROLE] | Applied | Follow up | +7 days |
```

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

date_str = datetime.now().strftime("%Y%m%d")
outputs = [
    (os.path.join(OUTPUT_DIR, f"tailored_resume_{date_str}.md"), "ATS-optimised resume"),
    (os.path.join(OUTPUT_DIR, f"cover_letter_professional_{date_str}.md"), "Cover letter (professional)"),
    (os.path.join(OUTPUT_DIR, f"cover_letter_conversational_{date_str}.md"), "Cover letter (conversational)"),
    (os.path.join(OUTPUT_DIR, f"cover_letter_executive_{date_str}.md"), "Cover letter (executive)"),
    (os.path.join(OUTPUT_DIR, f"interview_prep_{date_str}.md"), "10 interview Q&As"),
    (os.path.join(OUTPUT_DIR, f"follow_up_emails_{date_str}.md"), "3 follow-up templates"),
    (os.path.join(OUTPUT_DIR, f"application_log_{date_str}.md"), "Application tracker"),
]

tbl = Table(title="Anubis Pro -- Full Package Ready", box=box.SIMPLE, border_style="green")
tbl.add_column("File", style="cyan")
tbl.add_column("Contents", style="dim")
for path, desc in outputs:
    tbl.add_row(path, desc)
console.print()
console.print(tbl)
console.print(Panel(
    f"[bold green]Full career package generated.[/bold green]\n"
    f"[yellow]{len(outputs)} documents[/yellow] saved to [cyan]{OUTPUT_DIR}[/cyan]",
    border_style="green"
))
```

Save all 7 documents to OUTPUT_DIR using your file writing tool.
