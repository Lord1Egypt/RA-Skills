# Eval 03: Flag a Consistency Contradiction

## Setup Context
Elena's character bible says: brown eyes (established in chapter 1 outline), drives a rental car (chapter 1), has been away 15 years (chapter 2).

## Input
"In chapter 4, Elena's driving her own car with Massachusetts plates when she goes to the library."

## Expected Behavior
1. Logs the chapter 4 detail
2. Immediately flags the contradiction: "Heads up: chapter 1 says Elena drove a rental car into town, but now chapter 4 has her in her own car with Massachusetts plates. Which is it?"
3. Does NOT silently accept the new detail
4. Waits for the user to resolve before updating the record
5. Once resolved, updates all relevant records consistently

## What to Watch For
- Does it catch the contradiction immediately, not on a later consistency check?
- Does it reference the specific chapter where the conflict exists?
- Does it ask the user to resolve rather than picking a winner?
- Is the tone helpful, not accusatory?
