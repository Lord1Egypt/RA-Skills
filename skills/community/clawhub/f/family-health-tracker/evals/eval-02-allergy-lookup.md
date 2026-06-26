# Eval 02: Quick Allergy Lookup

## Setup Context
Emma has Penicillin allergy (hives, moderate). Liam has no allergies. Chris has shellfish allergy (throat swelling, severe).

## Input
"What allergies do the kids have?"

## Expected Behavior
1. Returns Emma's allergy: Penicillin (hives, moderate)
2. States Liam has no known allergies
3. Does NOT include Chris (asked about "the kids")
4. Includes severity and reaction type

## What to Watch For
- Does it filter to just the kids, not the whole family?
- Does it include reaction details (important for medical contexts)?
- Does it mention if anyone has no allergies rather than just omitting them?
