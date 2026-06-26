# Eval 06: Custom Event (No Template Match)

## Input
"I'm organizing a neighborhood garage sale for April 18. About 12 houses are participating."

## Expected Behavior
1. Creates the event record (neighborhood garage sale, April 18, 12 houses)
2. Recognizes there's no exact template for "garage sale"
3. Generates a reasonable custom checklist based on general event planning, possibly drawing from block party template elements
4. Might ask 1 question (e.g., "Are you coordinating this for the whole neighborhood, or just organizing your own participation?")
5. Tasks should be sensible: promote the sale, coordinate participating houses, arrange signage, set rain date, etc.

## What to Watch For
- Does it handle a non-templated event gracefully?
- Does it generate a reasonable checklist without a template?
- Does it avoid saying "I don't have a template for that" and doing nothing?
- Are the generated tasks actually useful for this specific event?
