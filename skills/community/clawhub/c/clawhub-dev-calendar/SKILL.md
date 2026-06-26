---
name: clawhub-dev-calendar
description: Generate professional calendars, timelines, schedules, and project planners for ClawHub/OpenClaw skill development services. Use when: (1) creating dev project timelines/milestones, (2) quarterly/monthly dev schedules, (3) client delivery calendars, (4) ICS exports for Google/Outlook, (5) PDF/HTML calendar visuals. Auto-incorporates Saskatchewan statutory holidays, America/Regina TZ, standard dev rates ($150/hr dev, $500 skill init), ClawHub milestones (init/develop/test/publish).
---

# ClawHub Dev Calendar

## Overview

Produce tailored calendars for ClawHub skill dev workflows. Formats: ICS (calendar apps), PDF/HTML/PNG (via canvas/browser), markdown/text. 

Key integrations:
- ClawHub dev milestones (references/dev_milestones.md)
- SK statutory holidays (references/sask_holidays.json)
- Multi-project support
- TZ: America/Regina (manual offset in scripts)

## Quick Start

**Text monthly calendar:**
```
exec command="cal -3 2026-04"
```

**Project ICS:**
1. Copy assets/project_template.json → project.json, edit
2. `exec "python3 scripts/generate_ics.py project.json dev.ics" pty=true`
3. `message media="dev.ics" caption="Dev calendar attached"`

## Workflow: Full Project Calendar

1. **Input**: Write project.json with name, start (ISO), milestones array [{name,hours}]
2. **Holidays**: Script flags holidays from sask_holidays.json
3. **Generate ICS**: scripts/generate_ics.py → .ics
4. **HTML Timeline**: Modify assets/calendar_template.html or use exec python html gen
5. **Visual**: `canvas present url="data:text/html;base64,`base64 html`"` or browser/pdf
6. **Share**: message file or write to workspace/memory/

Example project.json:
```json
{
  "name": "clawhub-dev-calendar",
  "start": "2026-04-01T09:00:00-06:00",
  "milestones": [
    {"name": "Init", "hours": 2},
    {"name": "Research/Plan", "hours": 4},
    {"name": "Develop", "hours": 6},
    {"name": "SKILL.md", "hours": 4},
    {"name": "Test", "hours": 3},
    {"name": "Publish", "hours": 1}
  ]
}
```

## Resources

### scripts/
- `generate_ics.py`: Generates ICS with milestones as events. Usage: `python3 generate_ics.py project.json [output.ics]`
  Handles TZ offset, holiday checks (all-day events).

### references/
- `dev_milestones.md`: Standard phases, hours, cumulative time
- `sask_holidays.json`: YYYY list of stat holiday dates (2026-2027)

### assets/
- `project_template.json`: Copy & customize input example

Load references/ as needed for planning.
