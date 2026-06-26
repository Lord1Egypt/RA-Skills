# Eval 01: Create New Event with Smart Template

## Input
"We need to start planning VBS. It's going to be June 15-19 this year. Budget is $2,500."

## Expected Behavior
1. Creates a VBS event record with dates June 15-19, status "planning," budget $2,500
2. Offers the VBS planning template with tasks and due dates calculated backward from June 15
3. Presents the template as adjustable, not final
4. Writes the event to event-data.json
5. Asks if the user wants to load the full checklist or customize first

## What to Watch For
- Are the due dates calculated correctly from the event date?
- Does it present the template as a suggestion, not a mandate?
- Does it capture the budget?
- Does it write to the data file?
