# Code Review Integration - Codex & Claude Code

## Auto-Review After Every Coding Event

Add these instructions to make reviews automatic.

---

## For Codex CLI (~/.codex/instructions.md)

Add this block:

```markdown
## Mandatory Post-Coding Review

After completing ANY coding task, before reporting done:

### Step 1: Jeff Dean Architecture Review
Review your changes through Jeff Dean's lens:
- Does the design make architectural sense?
- Is code in the right place (here vs library)?
- Is it clear enough for someone unfamiliar to maintain?
- Are functions small, focused, well-documented?
- Does it integrate cleanly with existing systems?

### Step 2: Self-Correct
Fix any issues identified before proceeding.

### Step 3: For UI/UX Changes, Add Luke W Review
Also check:
- Mobile-first responsive?
- Progressive disclosure (complexity hidden)?
- Obvious CTAs and next actions?
- Minimal cognitive load?
- Clear visual hierarchy?
- Happy path is frictionless?

### Step 4: Report Completion
Only after review passes, report the task complete.
```

---

## For Claude Code (CLAUDE.md or project instructions)

Add this block:

```markdown
## Post-Coding Review Protocol (MANDATORY)

**After EVERY code change, before marking complete:**

### 1. Channel Jeff Dean
Ask yourself:
- "Would Jeff Dean approve this architecture?"
- "Is this code clear, maintainable, and well-integrated?"
- "Could a junior dev understand and debug this?"

Review checklist:
- [ ] Logic is in the right place
- [ ] Functions are small and focused
- [ ] Code is documented where needed
- [ ] Integrates cleanly with existing code
- [ ] No unnecessary complexity

### 2. For UI Changes - Channel Luke W + Ryan Singer
Additional checks:
- [ ] Mobile-first design
- [ ] Complexity progressively disclosed
- [ ] Next actions are obvious
- [ ] Cognitive load minimized
- [ ] Clear visual hierarchy
- [ ] Happy path is frictionless

### 3. Self-Correct Before Reporting
Fix any issues found. Don't report completion until review passes.

### 4. Brief Review Note
When reporting completion, include a one-liner:
"✅ Jeff Dean review passed: [what you verified]"
```

---

## For All Agents (AGENTS.md addition)

Add to `~/clawd/AGENTS.md`:

```markdown
## Code Review Standard

ALL agents must run post-coding reviews:

1. **After any code change**: Jeff Dean architecture review
2. **After any UI change**: + Luke W / Ryan Singer UX review  
3. **Self-correct** before reporting complete
4. **Note in completion**: "✅ Review passed"

This is non-negotiable. Ship quality, not speed.
```

---

## Quick Reference Card

### Jeff Dean (Code/Architecture)
| Principle | Check |
|-----------|-------|
| Design | Does architecture make sense? |
| Placement | Is code in the right place? |
| Clarity | Would others understand it? |
| Functions | Small, focused, documented? |
| Integration | Clean fit with existing code? |

### Luke W + Ryan Singer (UX)
| Principle | Check |
|-----------|-------|
| Mobile First | Responsive design? |
| Progressive Disclosure | Complexity hidden? |
| Obvious Actions | Clear CTAs? |
| Cognitive Load | Minimal? |
| Visual Hierarchy | Eye guided? |
| JTBD | Happy path frictionless? |

---

## Example Completion Messages

Good:
```
✅ Added user auth flow. Jeff Dean review: Logic properly abstracted to auth/ module, 
small focused functions, clear error handling. Ready for PR.
```

```
✅ Built settings modal. Jeff Dean: Clean component structure. Luke W: Progressive 
disclosure for advanced settings, obvious save/cancel CTAs. Mobile responsive.
```

Bad:
```
Done with the feature.
```
(Missing review confirmation)
