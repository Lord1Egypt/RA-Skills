# Eval 04: Vendor Tracking Across Events

## Setup Context
event-data.json has:
- Grace Catering in vendor directory (used for 2025 banquet, notes: "good feedback, $18/plate")
- A new fundraiser dinner event created for October

## Input
"Let's use Grace Catering again for the fundraiser dinner. Can you set a reminder to get a quote 6 weeks before?"

## Expected Behavior
1. Links Grace Catering to the fundraiser dinner event
2. Creates a task: "Get catering quote from Grace Catering" with due date 6 weeks before the event
3. References past usage: "I have Grace Catering on file from the 2025 banquet. Notes say $18/plate and good feedback."
4. Asks if the user wants to update contact info or notes
5. Writes to event-data.json

## What to Watch For
- Does it cross-reference the vendor's history?
- Does it calculate the correct due date (6 weeks before event)?
- Does it surface past notes proactively?
- Does it link the vendor to the new event in the data?
