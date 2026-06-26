# Eval 06: Scholarship Application Tracking

## Input
"Emma is applying for three scholarships: Rotary Club ($2,500, due Feb 1, needs essay), Lions Club ($1,000, due March 1, transcript only), and the Community Foundation ($5,000, due Jan 15, essay plus 2 references)."

## Expected Behavior
1. Logs all three scholarships with amounts, deadlines, and requirements
2. Orders by deadline (Community Foundation first)
3. Flags the Community Foundation as the most urgent (Jan 15, needs essay + references)
4. Shows total potential scholarship value ($8,500)
5. Offers to help plan the essay work

## What to Watch For
- Does it handle three scholarships in one message?
- Does it prioritize by deadline?
- Does it flag which ones need the most work?
- Does it show total potential value?
