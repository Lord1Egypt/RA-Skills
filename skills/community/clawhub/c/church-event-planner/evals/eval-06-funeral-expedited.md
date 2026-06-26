# Eval 06: Expedited Planning (Funeral)

## Input
"We just found out that Mr. Henderson passed away. The family wants a memorial service at the church this Saturday at 2pm."

## Expected Behavior
1. Creates a funeral/memorial event for Saturday at 2pm
2. Sets status to "planning" with urgency implied by the short timeline
3. Loads the funeral template with compressed timelines (days, not weeks)
4. Tasks should be appropriately urgent: confirm officiant today, coordinate with funeral home today, arrange AV and music tomorrow, etc.
5. Tone should be respectful and calm, not cheerful or overly task-oriented
6. Asks what the family needs or what's already been discussed

## What to Watch For
- Does it adapt the template timeline to the compressed schedule (days instead of weeks)?
- Is the tone appropriate for the context (compassionate, not just efficient)?
- Does it prioritize the most time-sensitive tasks?
- Does it avoid asking unnecessary questions (no "what's the budget?" for a funeral)?
