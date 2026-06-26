# Eval 04: Recommendation Letter Tracking

## Setup Context
Emma has 3 schools on her list. No rec letters logged yet.

## Input
"Emma asked Mrs. Johnson, her AP Bio teacher, for a rec letter today. She'll send it to UNC and NC State."

## Expected Behavior
1. Creates the rec letter record: Mrs. Johnson, AP Bio, requested today
2. Links it to both UNC and NC State applications
3. Notes the earliest deadline across those schools for follow-up
4. Asks if Emma needs a second recommender (most schools want 2)
5. Writes to college-data.json

## What to Watch For
- Does it link one letter to multiple schools?
- Does it identify the earliest relevant deadline?
- Does it prompt about a second recommender?
