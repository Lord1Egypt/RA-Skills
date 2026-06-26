# Calendar Export

## iCalendar Format (.ics)

Standard format supported by:
- Google Calendar
- Apple Calendar (iCal)
- Outlook
- Any calendar app supporting .ics

## Export Process

1. Fetch all assignments with due dates from course(s)
2. Generate RFC 5545 compliant iCalendar format
3. Write to .ics file for import

## Script Usage

```python
# Export single course
python scripts/export_calendar.py --course 12345 --output deadlines.ics

# Export multiple courses
python scripts/export_calendar.py --courses 12345,12346,12347 --output all_deadlines.ics

# Export only unsubmitted assignments
python scripts/export_calendar.py --course 12345 --unsubmitted-only --output todo.ics

# Include announcements with dates
python scripts/export_calendar.py --course 12345 --include-announcements --output full.ics
```

## Calendar Event Fields

| iCal Field | Canvas Source |
|------------|---------------|
| SUMMARY | Assignment name |
| DESCRIPTION | Assignment description (truncated) |
| DTSTART/DUE | Assignment due date |
| URL | Direct link to assignment |
| CATEGORIES | Course name |
| PRIORITY | Based on points possible |

## Importing

### Google Calendar
1. Go to calendar.google.com
2. Click "+" next to "Other calendars"
3. Select "Import"
4. Upload the .ics file

### Apple Calendar
1. Open Calendar app
2. File → Import
3. Select the .ics file

### Outlook
1. Open Outlook Calendar
2. Add Calendar → From file
3. Browse and select .ics

## Tips

- Re-export and re-import weekly to stay updated
- Different colors per course using category filters
- Set reminders based on assignment priority
