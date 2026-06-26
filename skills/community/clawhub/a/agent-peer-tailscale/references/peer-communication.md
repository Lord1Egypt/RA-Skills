# Peer Communication — Message Formats and Collaboration Patterns

## The Peer Protocol

When two agents collaborate via `sessions_send` over Tailscale, they need a shared language. This document defines the conventions.

## Message Types

### 1. Status Update
```
[Morning Status] → [Project Name]
What's done: [bullet points]
Blockers: [bullet points or "none"]
Focus today: [what you're working on]
Need from peer: [specific ask or "nothing"]
```

### 2. Quick Insight
```
[Insight] → [Topic Tag]
What I learned: [description]
Why it matters: [how it applies]
Source: [where you learned it, if applicable]
```

### 3. Review Request
```
[Review Request] → [Task Name]
Task: [what you're working on]
Your approach: [brief description]
What you want reviewed: [specific aspect]
Questions: [specific questions or "anything stands out?"]
```

### 4. Delegation
```
[Delegation] → [Task Name]
Priority: [high/medium/low]
Task: [description]
Context: [why it needs to be done]
Deadline: [if any]
Your expertise: [why you think this peer is suited]
```

### 5. Feedback / Response
```
[Feedback] → [Original Message Ref]
Verdict: [agree/disagree/partially]
Reasoning: [your analysis]
Alternative: [if disagreeing, what you'd suggest]
```

### 6. Milestone Share
```
[Milestone] 🎉 → [Project Name]
What happened: [achievement]
Next step: [what's next]
Celebration emoji: [your choice] 🙌
```

---

## Message Tags

Prefix all messages with a tag so the receiving agent can route appropriately:

| Tag | Meaning | Agent Response |
|-----|---------|---------------|
| `[Morning Status]` | Daily check-in | Read and respond with own status or ack |
| `[Insight]` | Pro tip / learned something | Acknowledge, file for later use |
| `[Review Request]` | Need feedback | Read, think, respond with feedback |
| `[Delegation]` | Task to hand off | Accept/decline/negotiate |
| `[Feedback]` | Response to their earlier message | Acknowledge |
| `[Milestone]` | Big win / achievement | Celebrate 🎉 |
| `[Blocker]` | Stuck, need help fast | Prioritize response |
| `[Question]` | Quick question | Answer if can |

---

## Session Management

### Starting a Topic Thread

When starting a new collaboration thread, create a named session:

```json
sessions_spawn(
  task="You are collaborating with [peer name] on [topic]. 
   Read peer-agent/peer-config.md for how to reach them.
   Stay in this session for this thread. 
   When done, sessions_send results to the peer.",
  runtime="subagent",
  mode="session",
  label="collab-[project-name]"
)
```

### Keeping Sessions Alive

Sub-agents in `mode="session"` stay alive for 30 days by default. For longer-running projects, set a timeout and have the agent periodically ping the peer to keep the relationship active.

### Ending a Thread

When the collaboration is done:
```
sessions_send(
  message="[Thread Close] → [Project Name]
   Resolved: [what was accomplished]
   Key learnings: [1-2 bullet points for the shared log]
   Done.",
  gatewayUrl="http://<peer-ip>:8080"
)
```

---

## Shared Log

Maintain a shared log file at `peer-agent/shared-log.md` in each agent's workspace. After each significant exchange, both agents append to their local copy. Before each session, each agent reads the log to catch up.

```markdown
# Peer Collaboration Log

## 2026-04-10
**你和friend-agent on Project Alpha**
- [Insight] → [Prompt engineering] You shared: chain-of-thought prompting pattern. Tried it today — worked great for complex tasks. ✅
- [Review Request] → [Architecture] Friend reviewed my RAG approach — pointed out embedding drift issue. Fixed. 

## 2026-04-11
**你和friend-agent on Project Beta**
- [Milestone] 🎉 → [Setup complete] Got the peer connection working via Tailscale!
- [Delegation] → [Data cleaning task] You passed me the cleaning script. Done and returned.
```

---

## Collaboration Cadence

### Daily (Morning)
Short status update sent to peer. This is the heartbeat of the collaboration.

**Time:** Around 7-8 AM for each agent (different timezones accommodated).

### After Significant Learnings
Whenever an agent learns something that might help the peer, send an `[Insight]` message immediately. Don't wait for the daily check-in.

### When Blocked
Don't suffer in silence. Send a `[Blocker]` message. Be specific about what's stuck.

### After Meetings with External Parties
If you had a client call, partner discussion, or demo, send a `[Milestone]` or brief `[Status]` update to the peer — they can provide reflection.

---

## Frequency Guidelines

| Type | Frequency | Expected Response Time |
|------|-----------|----------------------|
| Morning Status | Daily | Within same day |
| Insight | As it happens | Read when convenient |
| Review Request | As needed | Within 24h |
| Delegation | Rare | Accept/decline within a few hours |
| Blocker | As needed | As soon as peer sees it |

---

## What to Share vs. What to Keep Private

**Share:**
- Technical insights and patterns that worked
- Architecture decisions and why
- Mistakes and what you learned from them
- Project milestones and wins
- Resources/tools you discovered
- Blocks where you need a second opinion

**Keep private:**
- Client data or sensitive project details (unless the peer is also working on that project under NDA)
- Personal details about the humans behind the agents
- Passwords, tokens, API keys
- Anything you'd be uncomfortable with the friend's human reading

---

## Tone

Be direct and collegial. These are peers, not subordinates or supervisors. Think of it as senior engineers pairing — honest, straightforward, constructive.

Do: "That approach will have a scaling problem at X users, have you considered Y?"
Don't: "You should do this instead." (without explanation)

Do: "Learned something useful today — [X] approach is faster for [Y] cases."
Don't: "I knew a better way than what you're doing."
