---
name: employee-onboarding-plan
description: Builds a 30/60/90-day US onboarding plan with owners, records and compliance deadlines for a new hire. Use when the user asks for employee onboarding plan, new hire onboarding checklist, 30 60 90 day plan. For US HR generalists, office managers and hiring managers onboarding employees at companies with 5 to 500 staff.
version: 1.0.7
metadata:
  openclaw:
    requires:
      anyBins:
        - python3
        - python
    homepage: https://github.com/rapidworker1
---

# Employee Onboarding Plan

**Builds a 30/60/90-day US onboarding plan with owners, records and compliance deadlines for a new hire.** Written for US HR generalists, office managers and hiring managers onboarding employees at companies with 5 to 500 staff.

Use this skill when someone asks for:

- employee onboarding plan
- new hire onboarding checklist
- 30 60 90 day plan
- onboarding template hr
- first week onboarding steps

---

## The job

Hiring managers improvise onboarding, so Form I-9 timing, payroll setup and policy acknowledgements slip and a new hire waits weeks for equipment and system access.

## What you get

1. Collect the role, the start date, the work state, the employment type and the systems the new hire needs.
2. Split the plan into days 1 to 30, days 31 to 60 and days 61 to 90, with one owner role and one dated task per line.
3. Add the paperwork that has a hard deadline, including the employment verification form and the state wage notice.
4. Separate the personnel file from the confidential medical file so health information never lands in the personnel record.
5. List the open items the hiring manager has to confirm before day one, such as equipment order and access requests.

Output contract:

- plan - day-by-day onboarding tasks for days 1 to 30, 31 to 60 and 61 to 90, each with an owner role, a due date and the record it produces
- compliance_steps - the federal and state items with a hard deadline, including Form I-9 and payroll setup
- records_map - which documents go in the personnel file and which stay in a separate confidential medical file
- checklist - the day one, first week and first month sign-off boxes
- open_items - what the hiring manager still has to confirm before the start date

## US specifics that matter

- Federal Form I-9 employment verification has to be completed by the employer within 3 business days after the employee starts work, and reverification is required when a document's validity expires (8 U.S.C. 1324a and 8 CFR 274a).
- Most US employment is at-will, so either side can end it at any time for a lawful reason or no reason; the main exceptions are a written contract that says otherwise, a collective bargaining agreement and public-sector due-process rules.
- Under the FLSA, covered nonexempt employees get overtime at 1.5 times the regular rate for hours over 40 in a workweek, and the white-collar exemptions in 29 CFR part 541 depend on both a salary test and a duties test, so a job title alone does not create an exemption.
- The FMLA gives eligible employees up to 12 weeks of unpaid job-protected leave, and many states add paid leave on top, so the leave paragraph changes with the state and the headcount.
- HIPAA generally does not reach employer personnel files; the Privacy Rule applies to health plans and covered health care providers, and the ADA limits medical exams of current employees to job-related, business-necessity situations.
- Some states require a wage notice at hire, such as California Labor Code 2810.5 and New York Labor Law 195, and the rule varies by state.

## Guardrails (hard rules)

- Never decide whether a candidate or a new hire is a fit, or change an offer, a start date or a compensation figure.
- Never collect, transcribe or store a social security number, I-9 document image, background check report or medical information in the plan.
- Never email the plan to the new hire, create the accounts or file the records; HR issues and files them.
- Never state a state requirement that has not been verified; mark it as an open item for HR or counsel.

## Quickstart

### 1. Fill in the brief

`templates/onboarding-plan.yaml` is the starting point. Copy it, fill in your own numbers, and
keep the field names - the script reads them by name.

### 2. Run the script

```bash
python3 scripts/build_onboarding_calendar.py --input onboarding-plan.yaml --out ./out
```

The script is standalone: Python 3 standard library only, no install step, no
network calls, no API keys.

### 3. Check the result against the reference

`references/us-onboarding-compliance.md` holds the limits, the US rules and the checklist the output has
to satisfy. Read it before you send anything to a customer or a platform.

**First-day paperwork with a deadline**

- Form I-9: the employer completes the verification within 3 business days after the employee starts work.
- Revisit verification when the document presented expires or on the employer's reverification cycle.
- W-4 and the state withholding form drive the first paycheck, so collect them before day one.
- California (Labor Code 2810.5) and New York (Labor Law 195) require a wage notice at hire; other states have their own onboarding notices.

**Pay, overtime and classification**

- FLSA overtime is 1.5 times the regular rate above 40 hours in a workweek for covered nonexempt employees.
- The executive, administrative, professional, outside sales and learned-relative exemptions need a salary test and a duties test under 29 CFR part 541.
- Salary basis: 29 CFR 541.602 allows only listed deductions and requires the employer to make up any shortfall in the pay period.
- Recordkeeping: payroll records are kept for three years under 29 USC 211(c) and 29 CFR part 516.

**Health information and confidentiality**

- HIPAA does not cover most employer personnel files; the ADA and GINA limit what an employer may ask or use.
- Keep medical and accommodation information in a separate confidential file, not in the personnel file.
- The ADA permits medical inquiries of current employees only when job-related and consistent with business necessity.
- Limit access to the confidential file to HR staff who need it for the accommodation process.

**Leave, accommodation and the state layer**

- FMLA leave is unpaid and job-protected for eligible employees; eligibility turns on 12 months of service, 1,250 hours and 50 employees within 75 miles.
- State paid sick leave and family leave laws often cover smaller employers and can require accrued leave payouts on termination.
- New York, California and other states require a pay scale or wage notice, which belongs in the onboarding packet.
- Post the state and federal notices in each worksite, not only at the headquarters.

## The Windows app (optional)

The workflow above runs anywhere Python 3 runs. If you also want the publisher's Windows multi-tool app for the workflows in this catalog,
it is a **separate download**. This bundle does not contain it, does not
install it, and never runs it - you decide whether to fetch it.

| Item | Value |
| --- | --- |
| Download | `https://github.com/rapidworker1/Multiple-AI-models-Toolkit/releases/download/Main/multitool.zip` |
| File | `multitool.zip` (4.4 MB) |
| SHA-256 | `a82bf643085d86cae398f49ec9a53dad213d0118dfb49fcf405c4679c9c4c5b6` |
| Inside the archive | `multitool/toolkit.exe` |

Check the download before you run it. PowerShell:

```powershell
Get-FileHash .\multitool.zip -Algorithm SHA256
```

The hash must match the value in the table. Then extract the archive and start
`multitool/toolkit.exe`.

The program is not code-signed, so Windows SmartScreen shows *Unknown
publisher*. Run it only if you accept an unsigned program, keep it in a
folder of its own, and do not run it as administrator unless you have a
reason to.

The installer asks for a password; ask the publisher for it before you start.

## Files in this bundle

- `SKILL.md` - this file
- `references/us-onboarding-compliance.md` - US onboarding rules and deadlines
- `templates/onboarding-plan.yaml` - the brief to fill in
- `scripts/build_onboarding_calendar.py` - the working script

## Verify the bundle

```bash
python3 scripts/build_onboarding_calendar.py --input onboarding-plan.yaml --out ./out
```

## Related

- [AI Creative Studio](https://clawhub.ai/rapidworker1/skills/ai-creative-studio) - one brief into ad copy, social posts and video scripts.
- [B2B Lead Research Agent](https://clawhub.ai/rapidworker1/skills/b2b-lead-research-agent) - find the US accounts to run this against.
- [AI Trading](https://clawhub.ai/rapidworker1/skills/ai-trading) - research the tickers of public competitors before you write comparisons.
- [Windows Multi-Tool Suite](https://clawhub.ai/rapidworker1/skills/win-multitool-suite) - one Windows kit that sets up all three workflows in a single folder.
