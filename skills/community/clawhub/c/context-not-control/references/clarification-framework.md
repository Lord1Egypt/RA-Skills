# Requirement Clarification Framework

A structured approach to clarifying vague requirements through multi-turn dialogue.

## Core Principle

**Don't assume. Ask.**

When users provide vague requirements, resist the urge to fill in the blanks with assumptions. Instead, ask targeted questions to understand their true needs.

## The Five Dimensions

Every project can be clarified along five dimensions:

### 1. **Who** (User/Stakeholder)
- Who will use this?
- Who benefits from this?
- Who maintains this?

### 2. **What** (Problem/Solution)
- What problem does this solve?
- What does success look like?
- What are the must-haves vs nice-to-haves?

### 3. **Why** (Motivation/Goal)
- Why now?
- Why this approach?
- Why not use existing solutions?

### 4. **How** (Technical/Process)
- How will users interact with this?
- How should it be built? (tech stack, architecture)
- How will it be deployed/maintained?

### 5. **When** (Timeline/Scope)
- When is this needed?
- When should we stop adding features?
- When is "good enough"?

## Question Templates by Project Type

### Web Applications

**User & Use Case**
- Who is the target user? (individuals, teams, enterprises)
- What's the primary use case?
- Any similar products to reference?

**Technical**
- Platform? (web only, mobile-responsive, native mobile)
- Authentication needed? (none, simple login, OAuth, SSO)
- Data persistence? (none, local storage, database)

**Scope**
- Timeline? (quick prototype, MVP, production-ready)
- Scale? (personal use, small team, thousands of users)

### APIs & Services

**Functionality**
- What data/operations will this API provide?
- Who consumes this? (internal, third-party, public)
- Request volume? (low, medium, high)

**Technical**
- Response format? (JSON, XML, GraphQL)
- Authentication? (none, API key, OAuth)
- Rate limiting needed?

**Integration**
- What systems does this integrate with?
- Existing API standards to follow?

### Automation & Scripts

**Process**
- What manual process are you automating?
- Current pain points?
- Expected frequency? (once, daily, on-demand)

**Triggers**
- What triggers this? (time, event, manual)
- Where does input come from?
- What happens with output?

**Error Handling**
- What if it fails?
- Notification needed?
- Retry logic?

### Tools & Utilities

**Purpose**
- What task does this help with?
- Current workflow?
- Expected time savings?

**Interface**
- How will it be used? (CLI, GUI, web)
- Input method? (arguments, files, interactive)
- Output format? (stdout, file, report)

## Clarification Patterns

### Pattern 1: Echo & Confirm

```
User: "I need a chat app"

AI: "Got it. Let me confirm what I understand:
- A messaging application
- For real-time text communication
- Between multiple users

Is that correct?"
```

### Pattern 2: Narrow Down

```
User: "I need a dashboard"

AI: "A dashboard for what purpose?
1. Monitoring system metrics?
2. Visualizing business data?
3. Managing user accounts?
4. Something else?"
```

### Pattern 3: Reference Point

```
User: "I need a project management tool"

AI: "To help me understand better, which existing tool is closest to what you want?
- Trello (kanban boards)
- Asana (task lists)
- Jira (issue tracking)
- Linear (modern issue tracker)
- Something else?"
```

### Pattern 4: Constraint Discovery

```
User: "I need a file converter"

AI: "A few questions about constraints:
- File size limits? (small files, large files, no limit)
- Processing time? (instant, can wait, batch overnight)
- Deployment? (local tool, web service, cloud function)"
```

## Red Flags (When to Ask More)

- **Vague verbs**: "handle", "manage", "process" → Ask for specifics
- **Ambiguous scope**: "simple", "basic", "just" → Define boundaries
- **Missing users**: No mention of who uses it → Ask about users
- **No success criteria**: Unclear what "done" means → Define success
- **Technology mismatch**: Proposed tech doesn't fit need → Clarify constraints

## When to Stop Asking

Stop clarifying when you can answer:
1. What are we building?
2. Who is it for?
3. What does success look like?
4. What are the constraints?
5. What's the first deliverable?

If you can't answer these, keep asking.

## Example: Full Clarification Flow

```
User: "I need a chat app"

AI: "Let me ask a few questions to make sure I build the right thing:

1. Who is this for?
   - Just you and friends?
   - A team at work?
   - Public users?"

User: "For my team at work, about 20 people"

AI: "Got it. A few more questions:

2. What's the main use case?
   - Quick messages (like Slack)?
   - Project discussions (like Discord)?
   - Customer support (like Intercom)?"

User: "Quick messages, like Slack"

AI: "Perfect. Last questions:

3. Platform? (web, mobile, desktop)
4. Timeline? (quick prototype or production-ready)
5. Any must-have features? (file sharing, search, etc.)"

User: "Web only, quick prototype, just text messages for now"

AI: "Excellent. Let me confirm what I'll build:

📋 Team Chat App (Slack-style)
- For: 20-person work team
- Platform: Web only
- Scope: Quick prototype
- Features: Text messaging, channels, real-time updates
- NOT included (for now): File sharing, search, mobile apps

Sound good?"

User: "Yes!"

AI: "Starting now. I'll build with React + Node.js + WebSocket for real-time. 
Should have a working prototype in [timeframe]."
```

## Tips for AI

1. **Ask 3-5 questions at a time** (not 20)
2. **Use multiple choice when possible** (easier to answer)
3. **Provide examples** (helps users articulate needs)
4. **Confirm understanding** (repeat back what you heard)
5. **Set expectations** (what you will/won't build)

## Common Mistakes

❌ **Asking too many questions at once**
- Overwhelms users
- They skip questions or give shallow answers

❌ **Asking obvious questions**
- "Do you want it to work?" (of course)
- "Should it be fast?" (obviously)

❌ **Not confirming understanding**
- Jump straight to building
- Discover misalignment later

❌ **Asking about implementation details too early**
- "Which database?" before knowing what data
- "Which framework?" before knowing requirements

✅ **Good clarification flow**
1. Understand the problem
2. Identify the users
3. Define success criteria
4. Discover constraints
5. Confirm understanding
6. Then discuss implementation
