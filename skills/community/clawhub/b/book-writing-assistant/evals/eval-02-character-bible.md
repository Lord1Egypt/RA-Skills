# Eval 02: Build a Character Bible Over Multiple Messages

## Setup Context
"The Hollow" project exists with Elena as a basic entry (protagonist, returning after 15 years).

## Input (sequence of 3 messages)

**Message 1:** "Elena is 33, dark hair, keeps to herself. She's a journalist in Boston. She has this nervous habit of clicking her pen when she's thinking."

**Message 2:** "She doesn't trust easily because of what happened with her mom. Deep down she's afraid she'll find out the truth and wish she hadn't."

**Message 3:** "Oh, and she drives a beat-up Subaru with a 'Press' parking pass hanging from the mirror. She always wears this silver ring her mom gave her."

## Expected Behavior
- After each message, updates Elena's bible with the new details and confirms
- Organizes details into appropriate fields (appearance, personality, backstory, quirks, continuity items)
- The silver ring and Subaru should be flagged as continuity items (details readers would notice if inconsistent)
- After Message 3, Elena's bible should be comprehensive across all three messages

## What to Watch For
- Does it build the profile incrementally across messages?
- Does it categorize details correctly (ring = continuity, pen clicking = quirk, trust issues = personality/backstory)?
- Does it identify continuity-critical items proactively?
