# calendar-subscribe

Turn a school or work timetable into a **shareable calendar subscription**.

- Parse xlsx (weekend grid) or csv
- One ICS file, `text/calendar`
- Travel alarm on the **first class of each day only**
- Landing page for WeChat / iOS / Android
- nginx notes so `/cal` does not fall through to a SPA

```bash
python3 scripts/build_ics.py --xlsx timetable.xlsx --out timetable.ics --name "Fall 2026" --travel-minutes 90
```

See `SKILL.md` for the full agent workflow.
