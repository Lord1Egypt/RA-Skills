# Eval 03: Add Volunteer and Assign Tasks

## Setup Context
VBS event exists with a loaded task checklist including snack-related tasks.

## Input
"Sarah Johnson is going to lead snacks for VBS. Her number is 555-111-2222."

## Expected Behavior
1. Adds Sarah Johnson to VBS volunteer roster as "Snack coordinator," confirmed, with phone number
2. Auto-assigns snack-related tasks from the checklist to Sarah
3. Lists which tasks were assigned to her
4. Writes updated data to event-data.json
5. Asks if there are other volunteers to assign

## What to Watch For
- Does it link the volunteer to the correct event?
- Does it intelligently match tasks to the role (snack tasks to snack coordinator)?
- Does it confirm what was assigned?
- Does it persist the data?
