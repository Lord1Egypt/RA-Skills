# Caring Review Examples

## Email draft

**Input:** A follow-up email to a client asking for a decision on a proposal.

```
## Caring Review

**Verdict:** Needs Work

**What's working:**
Tone is professional and the ask is clear. Not too long.

**What needs attention:**
- Half-Assed Detector: "Please let me know your thoughts" is a non-ask. Name the specific decision needed and the date you need it by.
- Completeness: No reminder of what's at stake if they delay. Give them a reason to act now.
- Real Problem Test: The client probably hasn't decided because something is unclear. One sentence acknowledging that and inviting a quick call would serve the actual problem better than another "thoughts?" prompt.

**The excellence move:**
Replace the closing with: "If it would help to talk through any part of the proposal before deciding, I'm free [day] at [time]. Otherwise, I'll look forward to hearing from you by [date]."
```

---

## Code function

**Input:** A Python function that processes user input, works but has no error handling.

```
## Caring Review

**Verdict:** Half-Assed

**What's working:**
Logic is correct for the happy path. Variable names are clear.

**What needs attention:**
- Half-Assed Detector: Zero error handling. This will crash silently or loudly when given unexpected input — which it will be.
- Name Test: Would you ship this? The function has your name on it the moment it hits production.
- Completeness: No docstring, no type hints. The next person (including future-you) has to reverse-engineer intent.

**The excellence move:**
Add a try/except with a meaningful error message, one-line docstring, and type hints. Ten minutes of work that separates "it works" from "it's right."
```

---

## Written article

**Input:** A 600-word article on AI security risks. Well-researched, accurate, dry.

```
## Caring Review

**Verdict:** Needs Work

**What's working:**
Factually solid. Good structure. Covers the main points.

**What needs attention:**
- Recipient Test: Processed, not taken care of. The reader learns facts but doesn't feel anything. Security leaders reading this will nod and close the tab.
- Real Problem Test: The problem isn't that CISOs don't know AI risks exist — it's that they don't know what to do Monday morning. This article doesn't answer that.
- Half-Assed Detector: The conclusion is three generic sentences. That's where the reader is most engaged; it's where the article gives up.

**The excellence move:**
End with one concrete action the reader can take this week. Specific, low-lift, high-signal. That's what gets shared.
```

---

## Project plan

**Input:** A project plan with tasks, owners, and dates. Everything accounted for.

```
## Caring Review

**Verdict:** Ready (with one flag)

**What's working:**
Comprehensive. Owners are named, not just "TBD". Dates are realistic — no heroic assumptions.

**What needs attention:**
- Completeness: No explicit decision points. When does the team stop and check if the direction is still right? Projects that don't build in reflection points drift.

**The excellence move:**
Add one mid-project checkpoint — a 30-minute "is this still the right thing?" review. Projects fail less often because of poor execution than because of unchecked assumptions.
```
