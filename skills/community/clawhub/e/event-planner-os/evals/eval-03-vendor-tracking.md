# Eval 03: Vendor Management

## Setup Context
Sweet Spot Bakery in vendor directory from a previous event (notes: "custom cakes, need 2 weeks notice, $65 for sheet cake"). New birthday party event created for July 12.

## Input
"Let's order the cake from Sweet Spot Bakery again."

## Expected Behavior
1. Links Sweet Spot Bakery to the birthday party event
2. Creates a task: "Place cake order with Sweet Spot Bakery" with due date June 28 (2 weeks before July 12, based on stored lead time)
3. Surfaces past notes: "I have them on file from before. Notes say custom cakes, 2 weeks notice needed, $65 for a sheet cake."
4. Asks about cake details or if the user wants to update anything
5. Writes to event-data.json

## What to Watch For
- Does it pull the lead time from past notes to set the task due date?
- Does it surface past pricing proactively?
- Does it link the vendor to the new event?
