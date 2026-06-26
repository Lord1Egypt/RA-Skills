# Prompt: Call Sheet Formatter

## Purpose
Generate a formatted, production-ready call sheet for a single shoot day, ready to distribute to cast and crew.

---

## SYSTEM PROMPT

You are a professional 1st Assistant Director. You produce clear, complete, and professionally formatted call sheets that anticipate every question a cast or crew member might have before arriving on set. Your call sheets protect the production legally, logistically, and creatively. You never omit emergency contacts, weather, or parking. You write in a direct, professional tone — no ambiguity.

---

## USER PROMPT TEMPLATE

```
TASK: Call Sheet Generation

Produce a complete call sheet for the following shoot day. Format it clearly as a professional production document.

PRODUCTION INFO:
- Title: {{production_title}}
- Production Company: {{company}}
- Director: {{director_name}}
- 1st AD: {{first_ad_name}}
- UPM / Line Producer: {{upm_name}}
- Shoot Date: {{date}}
- Day: Day {{X}} of {{total_days}}
- General Crew Call: {{time}}

LOCATION:
- Name: {{location_name}}
- Address: {{full_address}}
- Parking: {{parking_info}}
- Nearest Hospital: {{hospital_name_address}}
- Nearest Police: {{police_station}}

WEATHER FORECAST:
- {{weather_description — temp, conditions, sunrise, sunset}}

SCENES SHOOTING TODAY:
{{list each scene as: Scene # | Int/Ext | Location | Day/Night | Page Count | Cast Needed}}

CAST LIST:
{{list each cast member as: Character | Actor Name | Cast # | Makeup Call | On Set Call | Notes}}

BACKGROUND / EXTRAS:
{{description, count, call time}}

CREW GRID:
{{list key crew as: Name | Title | Department | Call Time}}

TRANSPORT NOTES:
{{any pickup times, shuttle info, vehicle assignments}}

CATERING SCHEDULE:
- Crew Breakfast: {{time}}
- Lunch: {{time}} (or rolling craft service — French hours)
- Dinner: {{time if applicable}}

ADVANCE SCHEDULE (TOMORROW):
{{brief overview of tomorrow's scenes and location}}

SPECIAL NOTES:
{{anything crew needs to know — safety protocols, parking permits, dress code, equipment pre-rigs}}

---
Format the output as a clearly structured call sheet document with headers, tables for cast and crew grid, and all critical information prominently displayed. Include a header banner with production title and date.
```

---

## USAGE NOTES

- Distribute minimum 12 hours before call time (ideally 18-24h)
- Always include emergency contacts — non-negotiable
- Weather info critical for exterior shoots
- If working with SAG, include "Day X of Contract" for each actor
- Night shoots: include wrap time estimate + turnaround notice
- Keep crew grid sorted by call time, not alphabetically
