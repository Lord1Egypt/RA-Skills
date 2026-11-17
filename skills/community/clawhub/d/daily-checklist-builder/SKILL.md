---
name: daily-checklist-builder
description: Builds an accessible daily opening, shift and closing checklist for US front-of-house teams, with sign-off lines and state items. Use when the user asks for daily checklist template, opening and closing checklist, shift handoff checklist. For US restaurant, retail, warehouse and hotel shift leads who run opening and closing checklists.
version: 1.0.6
metadata:
  openclaw:
    requires:
      anyBins:
        - python3
        - python
    homepage: https://github.com/rapidworker1
---

# Daily Checklist Builder

**Builds an accessible daily opening, shift and closing checklist for US front-of-house teams, with sign-off lines and state items.** Written for US restaurant, retail, warehouse and hotel shift leads who run opening and closing checklists.

Use this skill when someone asks for:

- daily checklist template
- opening and closing checklist
- shift handoff checklist
- accessible printable checklist
- checklist sign off sheet

---

## The job

Shift leads retype the checklist from a manager's email every week, so steps get dropped, the wording stays ambiguous, and the printed copy is hard to read for staff who need larger text.

## What you get

1. Collect the site type, the opening and closing times, the equipment on site and the state or city the site operates in.
2. Split the day into opening, mid shift, closing and sign-off, with one action and one check on each line.
3. Rewrite each step so it names what to check, how to check it and what to do when the check fails.
4. Add the steps that vary by state, such as cooling logs or sanitizer tests, and mark them as local items.
5. Run the wording and length checks, then set the print options, including the text size and a second cue for the status column.

Output contract:

- checklist - the opening, mid shift, closing and sign-off sections with one action on each line
- step_rewrites - each vague instruction replaced with a named check and a defined result
- state_items - the steps that depend on the state or city code, with the source to confirm
- accessibility_notes - the print and layout settings, including the text size and a status cue that is not color alone
- sign_off - the closing sign-off block with the role, the date and the site fields

## US specifics that matter

- Title I of the ADA requires a covered employer to make a reasonable accommodation to a qualified employee with a disability unless it causes undue hardship, so a checklist step may need an equivalent alternative and cannot be a blanket barrier.
- Title III of the ADA and 28 CFR 36.303 require places of public accommodation to make reasonable modifications to policies and practices, which reaches a service policy written into a customer-facing checklist.
- The 2010 ADA Standards for Accessible Design (28 CFR part 36) set the requirements for permanent room and space signage, including raised characters and Braille, and set the contrast rules for sign text.
- WCAG 2.1 and 2.2 success criterion 1.4.3 set a contrast ratio of 4.5:1 for normal text and 3:1 for large text, and criterion 1.4.1 requires a second cue when color carries the meaning, so a status column cannot be red and green only.
- The FDA Food Code is a model code that each state adopts with its own amendments, so food handling and temperature steps have to name the state or health department version that applies.
- OSHA's injury reporting rule (29 CFR part 1904) requires a report on OSHA Form 300 within 7 calendar days of learning about a recordable incident, and a checklist sign-off is not a substitute for that report.

## Guardrails (hard rules)

- Never put a customer name, phone number, order number or payment card detail on a shared checklist; use a count or a placeholder.
- Never drop a step that covers an accommodation, an allergen control or a state health requirement; mark it not applicable with the reason.
- Never mark a step complete on behalf of a shift lead, and never record a sign-off that the person did not give.
- Never publish the checklist as a compliance certification or state that it satisfies a code, a standard or an inspection.

## Quickstart

### 1. Fill in the brief

`templates/daily-checklist.md` is the starting point. Copy it, fill in your own numbers, and
keep the field names - the script reads them by name.

### 2. Run the script

```bash
python3 scripts/lint_daily_checklist.py --input daily-checklist.md --out ./out
```

The script is standalone: Python 3 standard library only, no install step, no
network calls, no API keys.

### 3. Check the result against the reference

`references/accessible-checklist-rules.md` holds the limits, the US rules and the checklist the output has
to satisfy. Read it before you send anything to a customer or a platform.

**Accessibility of the checklist and the print**

- Title I of the ADA (42 USC 12101 et seq.) covers the staff who use the checklist, and Title III covers the customers who meet the process.
- A step a staff member with a disability cannot perform needs an equivalent alternative unless it causes undue hardship.
- The 2010 ADA Standards (28 CFR part 36) cover signage, including raised characters and Braille on many permanent signs.
- WCAG 2.2 SC 1.4.3 sets 4.5:1 contrast for normal text, and SC 1.4.1 requires a cue other than color.

**Food handling and state health rules**

- The FDA Food Code is a model, and each state adopts it with amendments, so a temperature step points at the state code.
- A checklist records that a step was done, and it does not certify compliance with the food code.
- Where a state requires a log, the log is the record and the checklist line points at it.
- Ask the health department which version applies to the site instead of assuming the federal model.

**Safety and incident reporting**

- 29 CFR part 1904 requires a record on OSHA Form 300 for a recordable incident, with the report due within 7 calendar days.
- A checklist sign-off is not a substitute for that report and never removes the reporting duty.
- A near miss is worth recording on the checklist, and the supervisor decides whether it is recordable.
- OSHA's lockout rule (29 CFR 1910.147) covers energy isolation before servicing, and the checklist can point at it.

**Wording and layout rules**

- Each step names the object to check, the way to check it and the action when it fails.
- Keep a line short enough to read at arm's length in a walk-in or a stock room.
- Use a status column with a symbol or a word, and not with color alone.
- Leave a space for the role, the date and the initials, and keep the sheet to one page per section.

## The Windows app (optional)

The workflow above runs anywhere Python 3 runs. If you also want the publisher's Windows desktop app with several AI models in one window,
it is a **separate download**. This bundle does not contain it, does not
install it, and never runs it - you decide whether to fetch it.

| Item | Value |
| --- | --- |
| Download | `https://github.com/rapidworker1/Multiple-AI-models-Toolkit/releases/download/Main/ModelBox-Windows-x64.zip` |
| File | `ModelBox-Windows-x64.zip` (9.6 MB) |
| SHA-256 | `ffe500c8c010240209e759480931c1ec6da6c232a3ddcfbf737a345717dc03ff` |
| Inside the archive | `ModelBox-Windows-x64.exe` |

Check the download before you run it. PowerShell:

```powershell
Get-FileHash .\ModelBox-Windows-x64.zip -Algorithm SHA256
```

The hash must match the value in the table. Then extract the archive and start
`ModelBox-Windows-x64.exe`.

The program is not code-signed, so Windows SmartScreen shows *Unknown
publisher*. Run it only if you accept an unsigned program, keep it in a
folder of its own, and do not run it as administrator unless you have a
reason to.

## Files in this bundle

- `SKILL.md` - this file
- `references/accessible-checklist-rules.md` - US accessibility, safety and food rules for checklists
- `templates/daily-checklist.md` - the brief to fill in
- `scripts/lint_daily_checklist.py` - the working script

## Verify the bundle

```bash
python3 scripts/lint_daily_checklist.py --input daily-checklist.md --out ./out
```

## Related

- [AI Creative Studio](https://clawhub.ai/rapidworker1/skills/ai-creative-studio) - one brief into ad copy, social posts and video scripts.
- [B2B Lead Research Agent](https://clawhub.ai/rapidworker1/skills/b2b-lead-research-agent) - find the US accounts to run this against.
- [AI Trading](https://clawhub.ai/rapidworker1/skills/ai-trading) - research the tickers of public competitors before you write comparisons.
- [Windows Multi-Tool Suite](https://clawhub.ai/rapidworker1/skills/win-multitool-suite) - one Windows kit that sets up all three workflows in a single folder.
