#!/usr/bin/env python3
"""
Construction Law Skill — Interactive Wizard

Guided prompts for common contract administration tasks. Picks the right
sub-script, asks the right questions, and generates ready-to-use output.

Usage:
    python3 wizard.py
    python3 construction_law.py wizard
"""
import os
import sys
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

WIZARD_TASKS = [
    ("matter_intake",    "🏗️ Matter intake — structured issue triage (RECOMMENDED)"),
    ("notice_calendar",   "Generate a notice/obligations calendar"),
    ("claim_letter",      "Draft a claim letter (notice/EOT/disruption/VO/interim)"),
    ("sop_timeline",      "Singapore SOP Act payment timeline"),
    ("compare_fidic",     "Compare FIDIC contract forms side-by-side"),
    ("obligations_reg",   "Generate obligations register for a party"),
    ("excel_register",    "Excel workbook (obligations + notices combined)"),
    ("delay_analysis",    "Delay analysis & EOT entitlement"),
    ("quit",              "Exit wizard"),
]

FORMS_LONG = {
    "fidic-red":    "FIDIC Red Book 2017 (Construction, Employer-designed)",
    "fidic-yellow": "FIDIC Yellow Book 2017 (Plant & Design-Build)",
    "psscoc":       "PSSCOC (SG Public Sector Standard, Construction Works)",
    "sia":          "SIA Conditions (9th Ed.) — SG Private Sector",
    "nec4":         "NEC4 ECC",
}

CLAIM_TYPES = [
    ("notice-of-claim",    "Initial notice of claim (preserves time-bar)"),
    ("eot-application",    "Extension of Time application"),
    ("disruption-claim",   "Disruption / loss of productivity (NEW v2.1)"),
    ("loss-and-expense",   "Comprehensive Loss & Expense claim (NEW v2.2.1)"),
    ("variation-claim",    "Variation Order claim"),
    ("interim-claim",      "Interim payment application"),
    ("final-account",      "Final Account / Final Statement (NEW v2.2.1)"),
]

# ---------- prompt helpers ----------
def prompt(label, default=None, choices=None, allow_blank=False):
    """Prompt the user for input with optional default + validation."""
    while True:
        suffix = ""
        if choices:
            suffix = f" [{'/'.join(choices)}]"
        if default is not None:
            suffix += f" (default: {default})"
        try:
            raw = input(f"  {label}{suffix}: ").strip()
        except EOFError:
            print()
            return default if default is not None else ""
        if not raw:
            if default is not None:
                return default
            if allow_blank:
                return ""
            print("  ! Please enter a value.")
            continue
        if choices and raw not in choices:
            # Allow case-insensitive match
            lower_choices = [c.lower() for c in choices]
            if raw.lower() in lower_choices:
                return choices[lower_choices.index(raw.lower())]
            print(f"  ! Must be one of: {', '.join(choices)}")
            continue
        return raw

def prompt_date(label, default=None):
    while True:
        raw = prompt(label, default=default)
        try:
            datetime.strptime(raw, "%Y-%m-%d")
            return raw
        except ValueError:
            print("  ! Date must be YYYY-MM-DD")

def prompt_int(label, default=None, min_val=None, max_val=None):
    while True:
        raw = prompt(label, default=str(default) if default is not None else None)
        try:
            n = int(raw)
            if min_val is not None and n < min_val:
                print(f"  ! Must be >= {min_val}")
                continue
            if max_val is not None and n > max_val:
                print(f"  ! Must be <= {max_val}")
                continue
            return n
        except ValueError:
            print("  ! Must be a whole number")

def show_menu(title, items):
    print(f"\n{title}")
    for i, (_, label) in enumerate(items, 1):
        print(f"  {i}. {label}")
    while True:
        try:
            raw = input(f"\nChoice [1-{len(items)}]: ").strip()
        except EOFError:
            print()
            sys.exit(0)
        try:
            n = int(raw)
            if 1 <= n <= len(items):
                return items[n - 1][0]
        except ValueError:
            pass
        print(f"  ! Enter a number between 1 and {len(items)}")

def show_form_menu():
    items = [(k, f"{k:14s} — {v}") for k, v in FORMS_LONG.items()]
    return show_menu("Pick contract form:", items)

def show_claim_menu():
    items = [(k, f"{k:18s} — {v}") for k, v in CLAIM_TYPES]
    return show_menu("Pick claim type:", items)

# ---------- script runner ----------
def run_script(script_name, argv):
    """Import a sibling module by filename and call its main() with the given argv."""
    if SCRIPT_DIR not in sys.path:
        sys.path.insert(0, SCRIPT_DIR)
    module_name = script_name[:-3] if script_name.endswith(".py") else script_name
    saved_argv = sys.argv
    sys.argv = [script_name] + argv
    try:
        mod = __import__(module_name)
        if hasattr(mod, "main"):
            try:
                mod.main()
            except SystemExit as e:
                # Sub-scripts may sys.exit(0) on success — that's fine
                if e.code not in (0, None):
                    return False
        return True
    except Exception as e:
        print(f"\n[ERROR] Sub-script failed: {e}", file=sys.stderr)
        return False
    finally:
        sys.argv = saved_argv

# ---------- task handlers ----------
def task_notice_calendar():
    print("\n>> Notice / Obligations Calendar")
    form = show_form_menu()
    fmt = prompt("Output format", default="md", choices=["md", "csv"])
    out = prompt("Output file path (blank = print to screen)", allow_blank=True)
    args = ["--form", form, "--format", fmt]
    if out:
        args += ["--output", out]
    return run_script("notice_calendar.py", args)

def task_claim_letter():
    print("\n>> Claim Letter Generator")
    ctype = show_claim_menu()
    form = show_form_menu()
    out = prompt("Output file path (blank = print to screen)", allow_blank=True)
    args = ["--form", form, "--type", ctype]
    if out:
        args += ["--output", out]
    return run_script("claims_template.py", args)

def task_sop_timeline():
    print("\n>> Singapore SOP Act Timeline")
    cdate = prompt_date("Payment claim date (YYYY-MM-DD)")
    rperiod = prompt_int("Response period in days", default=21, min_val=1, max_val=60)
    fmt = prompt("Output format", default="md", choices=["md", "csv"])
    out = prompt("Output file path (blank = print to screen)", allow_blank=True)
    args = ["--claim-date", cdate, "--response-period", str(rperiod), "--format", fmt]
    if out:
        args += ["--output", out]
    return run_script("sop_calculator.py", args)

def task_compare_fidic():
    print("\n>> FIDIC Comparator")
    print("\nAvailable FIDIC forms: red, yellow, silver, emerald")
    forms = prompt("Forms (comma-separated, e.g. red,yellow)", default="red,yellow")
    topic = prompt("Topic", default="all",
                   choices=["overview", "risk", "claims", "disputes", "payment", "termination", "all"])
    fmt = prompt("Output format", default="md", choices=["md", "csv"])
    out = prompt("Output file path (blank = print to screen)", allow_blank=True)
    args = ["--forms", forms, "--topic", topic, "--format", fmt]
    if out:
        args += ["--output", out]
    return run_script("fidic_comparator.py", args)

def task_obligations_reg():
    print("\n>> Obligations Register")
    form = show_form_menu()
    party = prompt("Party", default="both", choices=["contractor", "employer", "both"])
    fmt = prompt("Output format", default="md", choices=["md", "csv"])
    out = prompt("Output file path (blank = print to screen)", allow_blank=True)
    args = ["--form", form, "--party", party, "--format", fmt]
    if out:
        args += ["--output", out]
    return run_script("obligations_register.py", args)

def task_excel_register():
    print("\n>> Excel Register (combined obligations + notices)")
    form = show_form_menu()
    rtype = prompt("Type", default="both", choices=["obligations", "notices", "both"])
    out = prompt("Output Excel file (e.g. register.xlsx)", default="register.xlsx")
    commencement = prompt("Commencement date (YYYY-MM-DD, blank to skip)", allow_blank=True)
    args = ["--form", form, "--type", rtype, "--output", out]
    if commencement:
        args += ["--commencement", commencement]
    return run_script("excel_register.py", args)

def task_delay_analysis():
    print("\n>> Delay Analysis")
    bstart = prompt_date("Baseline start (YYYY-MM-DD)")
    bend = prompt_date("Baseline completion (YYYY-MM-DD)")
    print("\nAdd delay events (one at a time). Format: description|start|end|responsibility[|critical]")
    print("Example: Late site access|2026-05-15|2026-06-15|Employer|true")
    print("Press Enter on blank line when done.\n")
    events = []
    while True:
        e = input(f"  Event #{len(events)+1} (blank to finish): ").strip()
        if not e:
            break
        events.append(e)
    fmt = prompt("Output format", default="md", choices=["md", "csv", "json"])
    out = prompt("Output file path (blank = print to screen)", allow_blank=True)
    args = ["--baseline-start", bstart, "--baseline-end", bend, "--format", fmt]
    for e in events:
        args += ["--add", e]
    if out:
        args += ["--output", out]
    return run_script("delay_calculator.py", args)

TASK_DISPATCH = {
    "matter_intake":    lambda: run_script("intake.py", []),
    "notice_calendar":  task_notice_calendar,
    "claim_letter":     task_claim_letter,
    "sop_timeline":     task_sop_timeline,
    "compare_fidic":    task_compare_fidic,
    "obligations_reg":  task_obligations_reg,
    "excel_register":   task_excel_register,
    "delay_analysis":   task_delay_analysis,
}

# ---------- main loop ----------
def main():
    print("=" * 60)
    print("  Construction Law Skill — Interactive Wizard (v2.8.1)")
    print("=" * 60)
    print("\nGuided prompts for common contract administration tasks.")
    print("Press Ctrl+C at any time to exit.\n")
    while True:
        try:
            task = show_menu("What would you like to do?", WIZARD_TASKS)
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            return
        if task == "quit":
            print("\nGoodbye!")
            return
        try:
            ok = TASK_DISPATCH[task]()
        except KeyboardInterrupt:
            print("\n\n[Cancelled]")
            continue
        print("\n" + ("-" * 60))
        if ok:
            print("✅ Done.")
        else:
            print("❌ Task failed. See errors above.")
        again = input("\nAnother task? [Y/n]: ").strip().lower()
        if again in ("n", "no", "q", "quit"):
            print("\nGoodbye!")
            return

if __name__ == "__main__":
    main()
