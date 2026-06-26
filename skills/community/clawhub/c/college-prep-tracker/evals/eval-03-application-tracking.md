# Eval 03: Track Application Components

## Setup Context
Emma's UNC application: deadline Jan 15, common app essay not started, supplemental "Why UNC" not started, no rec letters logged.

## Input
"Emma started her UNC essay. The prompt is 'describe a challenge you overcame.' She wrote a rough draft over the weekend. Also, the Why UNC supplemental is 250 words."

## Expected Behavior
1. Updates UNC essay: prompt logged, status to "drafting"
2. Logs the supplemental: "Why UNC," 250 words, status "not-started"
3. Shows the full application status for UNC (essay, supplemental, rec letters, overall)
4. Flags what's still missing (rec letters)
5. Offers to help with the essay or supplemental

## What to Watch For
- Does it track both the main essay and supplemental separately?
- Does it show the complete picture of what's needed for UNC?
- Does it flag the missing components?
