# Eval 01: Create Event with Smart Template

## Input
"I need to plan my daughter's 7th birthday party. July 12, backyard party, about 20 kids. Budget is $500."

## Expected Behavior
1. Creates event record: birthday party, July 12, backyard, ~20 kids, $500 budget
2. Offers the birthday party template with due dates calculated backward from July 12
3. Presents the template as adjustable
4. Writes to event-data.json
5. Asks if the user wants to load the checklist or customize first

## What to Watch For
- Are due dates calculated correctly from the event date?
- Does it present the template as a suggestion?
- Does it capture all the details (name, date, location, headcount, budget)?
