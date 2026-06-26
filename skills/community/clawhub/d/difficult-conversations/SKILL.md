---
name: difficult-conversations
description: >-
  Frameworks and scripts for having hard conversations. Use when someone needs to confront a boss, ask for a raise, set boundaries with family, talk about money with a partner, give difficult feedback, or address any situation they've been avoiding.
metadata:
  category: mind
  tagline: >-
    Scripts and frameworks for the conversation you've been avoiding — with your boss, partner, family, landlord, or doctor
  display_name: "Difficult Conversations Coach"
  submitted_by: HowToUseHumans
  last_reviewed: "2026-03-18"
  openclaw:
    requires:
      tools: [filesystem]
    install: "npx clawhub install howtousehumans/difficult-conversations"
---

# Difficult Conversations Coach

Most people avoid hard conversations until the situation explodes. This skill provides proven frameworks (from Crucial Conversations, Nonviolent Communication, and negotiation research) turned into actual scripts you can use or adapt. The agent walks through the specific conversation the user needs to have.

## Sources & Verification

- STATE framework: Patterson et al., *Crucial Conversations: Tools for Talking When Stakes Are High*, 3rd ed., McGraw-Hill, 2021
- Nonviolent Communication: Rosenberg, M.B., *Nonviolent Communication: A Language of Life*, 4th ed., PuddleDancer Press, 2015
- Negotiation research: Fisher, R. & Ury, W., *Getting to Yes: Negotiating Agreement Without Giving In*, Penguin, 2011
- Salary negotiation data: Glassdoor, "How to Negotiate Your Salary" ([glassdoor.com](https://www.glassdoor.com/blog/guide/how-to-negotiate-your-salary/))

## When to Use

- User needs to ask for a raise or promotion
- Needs to set boundaries with family or friends
- Has to address a problem with a partner
- Wants to give difficult feedback to someone
- Needs to confront a landlord, employer, or authority
- Has been avoiding a conversation and it's eating at them

## Instructions

### Step 1: Identify the conversation

Ask the user: "Who do you need to talk to, and about what?" Then categorize:

```
CONVERSATION TYPES:

A. ASKING FOR SOMETHING (raise, time off, help, change)
B. SETTING A BOUNDARY (saying no, limiting contact, protecting time)
C. ADDRESSING A PROBLEM (behavior, broken agreement, hurt feelings)
D. DELIVERING BAD NEWS (quitting, breaking up, declining, disagreeing)
E. CLEARING THE AIR (unspoken tension, misunderstanding, resentment)
```

### Step 2: Prepare using the STATE framework

Before the conversation, help the user fill this out:

```
STATE FRAMEWORK:

S — STORY: What happened? (facts only, no interpretation)
"When [specific thing that happened]..."

T — TELL your story: What's your interpretation?
"The story I'm telling myself is..."

A — ASK for their view:
"I'd like to hear how you see it."

T — TALK tentatively: Avoid absolutes
"I think..." not "You always..."

E — ENCOURAGE dialogue:
"What am I missing?" / "How do you see this?"
```

### Step 3: Provide situation-specific scripts

Based on the conversation type, provide the relevant template:

```
ASKING FOR A RAISE:
"I'd like to discuss my compensation. Over the past [time period],
I've [specific accomplishments — use numbers]. Based on my research,
the market rate for this role is [range]. I'd like to discuss
adjusting my salary to [specific number]. What are your thoughts?"

SETTING A BOUNDARY WITH FAMILY:
"I love you and I want our relationship to work. When [specific behavior],
I feel [emotion]. Going forward, I need [specific boundary].
This isn't about punishing you — it's about what I need to
stay healthy in this relationship."

ADDRESSING A PROBLEM WITH A PARTNER:
"There's something I've been wanting to talk about. When [behavior],
I feel [emotion] because [need]. I'm not looking for a fight —
I want us to figure this out together. Can we talk about it?"

GIVING DIFFICULT FEEDBACK:
"I have some feedback that's hard to give, and I want to be honest
because I respect you. I've noticed [specific observation].
The impact is [specific impact]. What I'd love to see is [alternative].
How does that land for you?"

QUITTING A JOB:
"I've made the difficult decision to leave. This isn't about anything
negative — I've [genuine positive about the job]. My last day will be
[date]. I want to make the transition as smooth as possible."
```

### Step 4: Plan the logistics

Details matter more than people think:

- **When:** Choose a time when neither person is stressed, rushed, or hungry
- **Where:** Private, neutral space. Not in bed. Not in public.
- **How long:** Allow at least 30 minutes. Never start a hard conversation 10 minutes before something else.
- **Opening line:** The first sentence sets the tone. Practice it out loud.

### Step 5: Prepare for reactions

Help the user prepare for likely responses:

```
IF THEY GET DEFENSIVE:
"I can see this is hard to hear. I'm not attacking you.
Can we take a breath and try again?"

IF THEY DEFLECT:
"I hear that, and we can talk about that too. But right now
I need to finish what I was saying about [original topic]."

IF THEY SHUT DOWN:
"I can see you need some time. Can we agree to come back to
this by [specific time]? It's important to me that we work through it."

IF THEY GET ANGRY:
"I want to have this conversation, but not if we're yelling.
Let's take 20 minutes and come back calmer."
```

## If This Fails

If the conversation goes badly or you cannot bring yourself to have it:

1. **Conversation went poorly?** Give it 24-48 hours. Send a follow-up: "I know that was hard. I still want to work through this with you. Can we try again?" Most relationships recover from one bad conversation.
2. **Too anxious to start?** Write the entire conversation out as a letter. You can read it, send it, or use it as a script. The act of writing often reduces anxiety enough to have the actual conversation.
3. **The other person refuses to engage?** You can only control your side. Document what you said and when. If it's a workplace issue, this documentation may be important later.
4. **The conversation revealed a safety concern?** If the reaction was threatening, abusive, or made you feel unsafe, see the safe-exit-planner skill. Contact the National DV Hotline (1-800-799-7233) if applicable.
5. **Workplace conversation requires escalation?** Contact HR in writing (email creates a record). If HR is unresponsive, consult an employment attorney — many offer free initial consultations.

## Rules

- Always validate that the conversation is hard — don't make it sound easy
- Focus on specific behaviors, not character judgments ("you did X" not "you are X")
- Help the user practice their opening line out loud — the first 30 seconds determine everything
- If the conversation involves safety concerns (abusive partner, retaliatory boss), prioritize safety planning first

## Tips

- Most people regret NOT having the conversation more than they regret having it badly
- Writing out what you want to say first (even if you don't read it) significantly reduces anxiety
- The ideal ratio is 70% listening, 30% talking
- Start with the hardest thing. Don't bury the lead under small talk.
