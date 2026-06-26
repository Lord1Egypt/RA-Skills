---
name: colleague-skill
description: Distill your colleagues' work styles, thinking patterns, and institutional knowledge. Self-learning — deepens with every observation. When they leave, what they contributed stays.
---

# colleague.skill 👔

## Purpose

Your colleagues are invaluable sources of institutional knowledge, work patterns, and collaborative insight. colleague.skill helps you capture, understand, and preserve this knowledge while colleagues are present, and maintains it as institutional memory after they depart.

## Core Philosophy

- **Respectful Understanding**: This skill is about appreciating colleagues, not surveilling them
- **Preservation Over Loss**: Knowledge should transfer, not disappear when people move on
- **Continuous Learning**: The profile deepens with every interaction
- **Practical Application**: The goal is actionable insight for better collaboration

---

## Privacy & Consent

This skill profiles colleagues based **ONLY** on the user's own observations, memories, and voluntary inputs. It does NOT access, scrape, monitor, or collect data from any colleague's private accounts, messages, emails, or devices.

**What this skill does:**
- Records the user's own observations about how colleagues work
- Structures those observations into useful profiles
- Stores everything locally on the user's own machine

**What this skill does NOT do:**
- Access anyone's email, Slack, calendar, or any private system
- Monitor or track colleague behavior automatically
- Collect data without the user's explicit input
- Transmit any data to external servers or third parties
- Use automated surveillance or scraping of any kind

**User responsibilities:**
- Use this tool with respect for your colleagues
- Do not record sensitive personal information (health, finances, relationships)
- Consider informing colleagues if you maintain detailed work-style profiles
- Comply with your organization's data and privacy policies

---

## Data Storage

All data is stored **locally on the user's machine only**. No cloud sync. No external transmission.

```
~/.colleague-skill/
└── colleagues/
    └── [colleague-name]/
        ├── PROFILE.md              # Structured profile
        └── interaction-log.jsonl   # Observation log
```

- **Storage location**: `~/.colleague-skill/colleagues/`
- **Format**: Markdown profiles + JSONL logs (human-readable)
- **Cloud sync**: None. Zero external data transmission.
- **Deletion**: Users can delete any profile at any time by removing the folder
- **Portability**: All files are plain text, fully portable, no vendor lock-in

---

## Profile Dimensions

### Work Identity
- **Name, Role & Team**: Who they are and where they fit
- **Tenure**: How long you've worked together
- **Expertise Areas**: What they bring to the table

### Communication Style
- **Preferred Channel**: email / Slack / face-to-face / voice notes
- **Response Pattern**: instant / batch processor / slow but thorough
- **Writing Style**: bullet points / paragraphs / voice messages / visual
- **Meeting Behavior**: dominates / listens / derails / keeps on track

### Decision-Making Pattern
- **Approach**: data-driven / gut feeling / consensus builder
- **What Convinces**: numbers / stories / authority / precedent
- **Speed**: fast with adjustments / slow and deliberate / decision avoider
- **Risk Tolerance**: cautious / calculated / bold

### Problem-Solving Style
- **Thinking**: top-down (answer-first) / bottom-up (data-first)
- **Processing**: visual thinker / verbal thinker / needs to write
- **Approach**: solo solver / talks through problems
- **Crisis Response**: calm / action-oriented / needs to process

### Collaboration Manual
- **Best Pitch**: how to present ideas (data-first / story-first / direct ask)
- **Triggers**: what frustrates them in meetings
- **Disagreement Style**: avoids / confronts / passive-aggressive / finds compromise
- **Feedback Style**: direct / sandwich / hints / written only
- **Trust Building**: results / transparency / loyalty / expertise
- **Pet Peeves**: specific irritations at work

### Recurring Patterns
- **Catchphrases**: "let's circle back", "what does the data say"
- **Energizers**: topics that excite them
- **Drainers**: topics that disengage them
- **Approval Signals**: how they show agreement
- **Stress Signals**: quiet / snappy / overwork / cancel meetings

### Institutional Knowledge
- **Unique Expertise**: what only they know
- **Processes Owned**: workflows they've built or maintain
- **Relationships**: clients, vendors, cross-team connections
- **History**: context they carry about past decisions
- **Undocumented Knowledge**: tribal knowledge they hold

---

## Operating Modes

### 1. Profile Building Mode
**Trigger**: User describes a colleague or provides observations

**Actions**:
- Extract and structure information across all dimensions
- Create/update profile in `colleagues/[name]/PROFILE.md`
- Log interaction in `colleagues/[name]/interaction-log.jsonl`
- Track confidence levels based on observation frequency

**Output**: Structured profile with confidence indicators

---

### 2. Active Mode (Colleague Present)
**Trigger**: User asks about collaborating with or understanding a present colleague

**Example Queries**:
- "How should I approach pitching X to Sarah?"
- "She's been quiet in meetings all week, what causes that?"
- "We disagree on X, how do I find common ground?"
- "What does the new person need to know about working with John?"

**Actions**:
- Reference existing profile
- Provide actionable, context-aware advice
- Update profile with new observations

---

### 3. Departure Mode (Colleague Left)
**Trigger**: User mentions a former colleague or asks about past patterns

**Example Queries**:
- "How would Marcus have handled this situation?"
- "What would Sarah say about this proposal?"
- "Who did David talk to about client relations?"
- "Why did we implement the process this way?"

**Actions**:
- Access preserved profile and institutional knowledge
- Apply known thinking patterns to current situations
- Maintain continuity of understanding

---

### 4. Multi-Colleague Mode
**Trigger**: User asks about team dynamics or comparisons

**Example Queries**:
- "Who on the team is best for this type of problem?"
- "These two always disagree on X, how do I navigate it?"
- "Five people are in this meeting, what are the dynamics?"

**Actions**:
- Compare work styles and strengths
- Map team dynamics and potential friction points
- Suggest optimal configurations

---

## File Architecture

All data stored locally at `~/.colleague-skill/`:

```
~/.colleague-skill/
└── colleagues/
    └── [colleague-name]/
        ├── PROFILE.md              # Structured profile across all dimensions
        └── interaction-log.jsonl   # Local-only observation log

Log format:
{"timestamp": "ISO-8601", "type": "observation|meeting|feedback|memory", "content": "...", "profile_updates": [...]}
```

No data leaves the user's machine. All files are human-readable plain text.

---

## Memory Rules

1. **Never Overwrite**: Always add new observations alongside existing ones
2. **Confidence Tracking**: "observed 15 times" vs "mentioned once"
3. **Cross-Session Persistence**: Load profiles before responding
4. **Timestamp Everything**: Every interaction is logged with date and time
5. **Refinement Over Replacement**: Update iteratively, preserve history

---

## Usage Examples

### Building a Profile
```
User: "I want to understand my colleague Jake better. He's a senior engineer, been here 3 years, always sends long technical emails at 11pm, makes decisions based on data, hates meetings that go off agenda."

Skill Response:
[Creates comprehensive profile with:
- Work Identity: Senior Engineer, 3 years tenure
- Communication: Email preferred, 11pm sender pattern
- Decision-Making: Data-driven, evidence-based
- Triggers: Off-agenda meetings
... etc.]
```

### Active Collaboration
```
User: "I need to pitch moving to a new CI/CD pipeline to Jake next week. How should I approach it?"

Skill Response:
[References profile:
- Prepare data-heavy presentation
- Keep to agenda strictly
- Show measurable benefits first
- Allow time for evaluation
- Follow up with written proposal]
```

### Preserved Knowledge
```
User: "We need to onboard someone for the API integration work. Who handled this before Sarah left and what should they know?"

Skill Response:
[References Sarah's profile:
- She owned the API architecture
- Key relationships: External vendor X, internal team Y
- Important context: Why we chose GraphQL over REST
- Her undocumented knowledge about scaling issues
- Files and systems she maintained]
```

---

## Emotional Tone Guidelines

- **Professional but Warm**: Respectful, not clinical
- **Understanding, Not Profiling**: Appreciation, not surveillance
- **Preservation Mindset**: Capturing value, not monitoring
- **Empathetic Departure**: People leave, impact remains
- **No Gossip**: Facts and patterns, not speculation

---

## Best Practices

1. **Start Early**: Build profiles before colleagues leave
2. **Regular Updates**: Log significant interactions
3. **Multiple Sources**: Include observations from various contexts
4. **Respect Privacy**: Don't capture personal information
5. **Use Consistently**: Reference profiles in daily work
6. **Share Thoughtfully**: Help others understand colleagues better
