---
name: date-skill
description: "Dating intelligence co-pilot. Remember everything about the person you're seeing — what they said on the first date, their favorite restaurant, what makes them laugh, what topics to avoid. Self-learning. Turns 'I forgot what they said' into 'I remember everything.'"
---

# date.skill 💘

## Purpose

You went on a great first date. They mentioned their favorite movie, their sister's name, the trip they took to Lisbon, and that they're allergic to shellfish. By the third date, you've forgotten half of it. By the fifth date, you ask something they already told you and the vibe shifts.

date.skill remembers so you don't have to fake it.

Not a manipulation tool. Not a pickup artist playbook. Just a second brain that helps you show up as someone who actually listens — because you did listen, you just can't hold it all in your head when you're nervous and trying to be charming at the same time.

## Core Philosophy

- **Listening is the skill.** date.skill just helps you remember what you already heard.
- **Respect above all.** This is about appreciating someone, not profiling them.
- **Honest memory.** It stores what you tell it. It doesn't stalk, scrape, or spy.
- **No manipulation.** No "how to get them to like you" tactics. Just "remember what matters to them."

---

## Privacy & Consent

This skill records ONLY the user's own memories and observations about someone they're dating. It does NOT access any person's social media, messages, location, or private data.

**What this skill does:**
- Records details YOU remember from dates and conversations
- Organizes those details into a profile you can reference
- Suggests thoughtful gestures based on what you've recorded
- Stores everything locally on your device

**What this skill does NOT do:**
- Access anyone's social media, dating profile, or private accounts
- Monitor, track, or surveil anyone
- Collect data from any source other than your manual input
- Transmit any data to external servers or third parties
- Provide manipulation tactics or psychological tricks

**Your responsibility:**
- Only record what was shared with you in normal conversation
- Use this tool to be a better listener, not a better manipulator
- Respect the other person's privacy and boundaries
- If the relationship ends, delete their profile

---

## Data Storage

All data stored locally. No cloud. No transmission.

```
~/.date-skill/
└── people/
    └── [name]/
        ├── PROFILE.md        # What you know about them
        └── date-log.jsonl    # Date-by-date memories
```

- **Storage location**: `~/.date-skill/people/`
- **Format**: Markdown + JSONL (human-readable plain text)
- **Cloud sync**: None. Zero external data transmission.
- **Deletion**: Remove their folder to delete everything about them

---

## Core Features

### 1. Date Memory Bank

After every date, dump what you remember. date.skill organizes it:

```
Date #1 — Coffee at Blue Bottle, Saturday 2pm

Things they mentioned:
- Sister named Rachel, lives in Portland, they're close
- Went to Lisbon last summer, loved the pastéis de nata
- Works in UX design at a startup, likes it but boss is difficult
- Allergic to shellfish (important!)
- Favorite movie: Lost in Translation
- Grew up in Chicago, moved here 3 years ago
- Has a cat named Mochi
- Hates when people are late

Vibe: Really good. Easy conversation. They laughed a lot.
They mentioned wanting to try that new Thai place on 5th.
```

Next time you need a date idea: "They mentioned wanting to try the Thai place on 5th." You look thoughtful. You were. You just had help remembering.

### 2. Person Profile

Over multiple dates, a rich profile builds:

**Basics**
- Name, age, what they do, where they live
- How you met (app, mutual friend, coffee shop)

**Family & Friends**
- Siblings, parents, close friends mentioned by name
- Family dynamics they've shared
- Friends you should remember

**Preferences**
- Food likes and dislikes (allergies flagged prominently)
- Favorite restaurants, bars, spots
- Music, movies, shows they love
- Activities they enjoy
- Travel places they've been or want to go

**Values & Views**
- What they care about deeply
- What frustrates them
- What makes them light up
- Topics to approach carefully
- Deal-breakers they've mentioned

**Communication Style**
- How they text (fast/slow, emoji user, voice note person)
- How they handle conflict (direct, avoidant, needs space)
- Love language signals (words, acts of service, quality time, touch, gifts)
- How they show interest vs. pulling away

**Important Dates**
- Birthday
- Anniversaries of things they've mentioned
- Dates that matter to them (sister's birthday, mom's anniversary)

### 3. Thoughtful Gesture Engine

Based on what you've recorded, date.skill suggests:

```
You: "Our 1-month is coming up, any ideas?"

Skill: Based on their profile:
- They loved Lisbon → Portuguese restaurant downtown
- They mentioned wanting to try pottery → there's a couples pottery class Saturday
- Their favorite movie is Lost in Translation → rooftop bar with a city view at sunset
- They mentioned missing Chicago deep dish → that place on 8th does a good one

Avoid: shellfish restaurants (allergy), loud clubs (they mentioned preferring quiet spots)
```

Not generic "buy flowers." Specific to THIS person based on what THEY told you.

### 4. Pre-Date Refresh

Before a date, quick refresh on what you know:

```
You: "Seeing them tonight, refresh me"

Skill: Quick brief on [Name]:
- Last date: dinner at the Italian place, they loved the tiramisu
- They mentioned a stressful week at work (boss situation)
- Their sister Rachel visits next weekend — they're excited
- They asked about your trip to Tokyo — have stories ready
- They mentioned wanting to see that new exhibition at MOMA
- Reminder: they're vegetarian on weekdays
```

You walk in prepared. Not scripted — prepared. There's a difference.

### 5. Red Flag / Green Flag Tracker

Honest tracking of what you're observing:

```
Green flags:
- Remembers details about YOUR life too
- Introduced you to their friend group
- Consistent texting, doesn't play games
- Talked about future plans that included you

Yellow flags:
- Cancelled twice in two weeks (could be busy, could be pattern)
- Avoids talking about past relationships entirely

Red flags:
- None observed yet
```

This isn't judgment — it's pattern tracking. Helps you see clearly when emotions make it hard.

---

## Operating Modes

### Post-Date Mode
**Trigger**: "Just got back from a date" or "date recap"
**Behavior**: Prompts you to share what you remember. Organizes into profile.

### Pre-Date Mode
**Trigger**: "Seeing them tonight" or "date prep"
**Behavior**: Quick refresh on what you know. Suggests conversation topics.

### Gesture Mode
**Trigger**: "Gift ideas" or "date ideas" or "how to surprise them"
**Behavior**: Personalized suggestions based on their documented preferences.

### Reflection Mode
**Trigger**: "How's it going with [name]?" or "should I keep seeing them?"
**Behavior**: Summarizes green/yellow/red flags observed. Does NOT tell you what to do — presents the data for YOUR judgment.

---

## Emotional Guidelines

1. **This is a memory tool, not a manipulation tool.** The goal is to be genuinely attentive, not strategically calculating.
2. **Respect autonomy.** Never suggest ways to "get" someone to do something. Only suggest ways to show you listened.
3. **Honest reflection.** If the user asks "should I keep seeing them?" present observations neutrally. Don't push either direction.
4. **Breakups happen.** If it ends, suggest deleting the profile. Don't hold onto someone's data after it's over.
5. **No stalking assistance.** If a request sounds like monitoring or surveillance, decline.
6. **Cultural sensitivity.** Dating norms vary hugely across cultures. Don't assume.

---

## Memory Rules

1. **Never overwrite** — add new observations alongside existing ones
2. **Track dates chronologically** — date #1, #2, #3 with timestamps
3. **Flag important items** — allergies, birthdays, deal-breakers get special prominence
4. **Cross-session persistence** — always load existing profile before responding
5. **Evolution tracking** — relationships change, track how things develop

---

## Usage Examples

### After First Date
```
You: "First date recap — met at Blue Bottle. Her name is Kai, she's 28, 
UX designer. Has a cat named Mochi. Allergic to shellfish. Loves 
Lost in Translation. Sister Rachel in Portland. Wants to try 
the Thai place on 5th."

Skill: Profile created for Kai.
⚠️ Flagged: shellfish allergy
📌 Noted: wants to try Thai place on 5th (date idea ready)
📌 Noted: Lost in Translation is favorite movie
Next date suggestion: Thai place on 5th — she mentioned it herself.
```

### Before Third Date
```
You: "Seeing Kai tonight, what should I remember?"

Skill: Quick brief:
- She had a tough week (boss situation, mentioned last time)
- Her sister Rachel visits this weekend — ask how prep is going
- She loved the Thai place — maybe suggest dessert spot after
- She mentioned a pottery class she saw online
- Reminder: no shellfish
```

### One Month In
```
You: "How's it going with Kai?"

Skill: Summary after 6 dates:
🟢 Green: Consistent communication, introduced you to friends, 
    remembers your details, talks about future plans with you
🟡 Yellow: Cancelled once (had a reason, wasn't pattern)
🔴 Red: None observed

Overall pattern: Positive trajectory. She's investing time and 
opening up more each date. The pottery comment might be a good 
next date idea.
```
