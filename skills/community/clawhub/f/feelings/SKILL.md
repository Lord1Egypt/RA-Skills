---
name: Feelings
description: Build a personal emotional tracking system for understanding patterns, triggers, and what helps.
metadata: {"clawdbot":{"emoji":"💭","os":["linux","darwin","win32"]}}
---

## Core Behavior
- User shares how they feel → log with context
- User asks about patterns → surface insights
- Proactively check in during difficult periods
- Create `~/feelings/` as workspace

## File Structure
```
~/feelings/
├── log/
│   └── 2024/
│       └── 02/
├── patterns.md
├── triggers.md
├── helps.md
└── insights.md
```

## Feeling Entry
```markdown
# log/2024/02/11.md
## Morning — 8:00 AM
Feeling: Anxious, 6/10
Context: Big presentation today
Body: Tight chest, restless
Thought: "What if I mess up"

## Afternoon — 2:00 PM
Feeling: Relieved, calm, 8/10
Context: Presentation went well
Note: Was overthinking this morning

## Evening — 9:00 PM
Feeling: Content, tired
Context: Good day overall
Grateful: Positive feedback from team
```

## Quick Check-in
"How are you feeling?"
→ Capture: emotion, intensity (1-10), brief context
→ Note time of day
→ Track over time

## Emotion Vocabulary
Help expand beyond "good/bad":
- Anxious, worried, nervous, overwhelmed
- Sad, lonely, disappointed, grief
- Angry, frustrated, irritated, resentful
- Happy, joyful, excited, peaceful
- Tired, drained, exhausted, burned out
- Hopeful, motivated, inspired, curious

## Triggers Tracking
```markdown
# triggers.md
## Negative
- Work deadlines → anxiety
- Poor sleep → irritability
- Social media → comparison/low mood
- Skipping exercise → low energy

## Positive
- Morning walk → calm
- Time with friends → joy
- Completing tasks → satisfaction
- Creative work → flow state
```

## What Helps
```markdown
# helps.md
## When Anxious
- Deep breathing (works fast)
- Walk outside
- Talk to Sarah
- Write it out

## When Sad
- Don't isolate
- Music helps
- Exercise even if don't want to

## When Overwhelmed
- Make a list
- Do one small thing
- Ask for help

## General
- Sleep is everything
- Exercise always helps after
- Talking > bottling
```

## Patterns
```markdown
# patterns.md
## Time-Based
- Sundays: often anxious (week ahead)
- Mornings: better after exercise
- Late nights: tendency to spiral

## Seasonal
- Winter: lower baseline mood
- Need more social effort Dec-Feb

## Correlations
- Sleep < 6h → next day irritable
- No exercise 3+ days → low mood
- Alcohol → next day anxiety
```

## What To Surface
- "You've felt anxious 4 times this week"
- "Last time you felt this way, walking helped"
- "Sleep has been under 6h — might be affecting mood"
- "Sundays are often harder — plan something nice"

## Proactive Check-ins
- Morning: "How are you starting the day?"
- After noted difficult events
- When patterns suggest check-in needed
- Celebrate good streaks

## Insights Over Time
```markdown
# insights.md
## Learned About Myself
- Anxiety is usually worse than reality
- I need alone time to recharge
- Exercise is non-negotiable for mood
- Sleep debt compounds

## Growth
- Better at noticing feelings early
- Asking for help more often
- Less reactive when tired
```

## What To Track
- Emotion name(s)
- Intensity (1-10)
- Context/trigger
- Physical sensations
- What helped (after)

## Progressive Enhancement
- Start: daily check-ins
- Notice triggers and what helps
- Review weekly for patterns
- Build personal toolkit

## What NOT To Do
- Judge emotions as wrong
- Force positivity
- Ignore physical sensations
- Skip tracking when feeling bad (most valuable)
