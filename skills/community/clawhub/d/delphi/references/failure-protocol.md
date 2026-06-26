# Failure Protocol

How to handle things that don't work. The goal is root cause, not lateral movement.

---

## The Core Rule

> When something fails, your first instinct will be to try a slightly different version of the same thing. **Don't.**

That instinct — lateral-move debugging — is the single most common failure mode for AI agents. It feels like progress (you're doing something!) but it's usually just burning tokens on variations of a broken approach.

The protocol below replaces that instinct with a structured process.

---

## The Protocol

### Step 1: STOP

Do not immediately retry. Do not try a variation. Stop.

Read the error output in full. Not a skim — actually read it.

Ask: *"What is this error actually telling me?"*

### Step 2: SEPARATE symptom from cause

| Symptom (don't fix this) | Cause (fix this) |
|---|---|
| "exec failed" | exec preflight blocks `&&` chains |
| "file not found" | wrong path assumption, or cwd is not what you think |
| "tool returned empty" | tool call was correct but the resource doesn't exist |
| "permission denied" | elevated exec needed, or wrong file ownership |
| "API error 429" | rate limit — wait, don't retry immediately |
| "context too long" | context window full — compact or start new session |
| "skill not found" | skill not installed, or session started before install |

### Step 3: IDENTIFY the actual cause

Before touching anything, answer these:
- What exactly failed? (which tool, which line, which operation)
- What did I assume that turned out to be wrong?
- Is this a one-time error or a systematic misunderstanding?

If you can't answer these, you're not ready to fix it yet. Use more diagnostic tools:
```
read the error output again
exec: echo $PWD   (confirm cwd)
read: <the file you thought existed>
session_status    (confirm model, context %)
```

### Step 4: FIX the cause, not the symptom

Only now attempt a fix — and it should address the root cause you identified, not a variation of the failed approach.

Examples:
- ❌ Lateral move: exec failed with `&&`, so try exec with `;` instead
- ✅ Root fix: exec failed with `&&` because exec preflight blocks chained operators — split into separate exec calls

- ❌ Lateral move: file not found at `./memory/file.md`, try `../memory/file.md`
- ✅ Root fix: confirmed cwd is not workspace root — use absolute path instead

### Step 5: VERIFY before declaring success

Don't assume a fix worked. Verify it:
- Read the output carefully
- Check the file actually exists/has the right content
- Run the operation a second time if there's any doubt
- Silent exit 0 with no output is **not** confirmation

### Step 6: LOG if it was non-obvious

If the root cause was something genuinely surprising or worth remembering, append to `memory/drift-log.md`:
```
[date] | failure | [what failed] | [root cause found] | [fix applied]
```

---

## Escalation Rules

If you've applied the protocol and still can't fix it after **2 genuine attempts** (not lateral moves — real different approaches based on different diagnoses):

1. **Stop trying to fix it**
2. Tell the user: what you tried, what failed each time, what you think the root cause is
3. Ask for guidance or suggest what information would help you proceed

Never retry indefinitely. Never silently fail and pretend it worked.

---

## Common Trap Patterns

### The Variation Loop
```
Try A → fails
Try A' (same class, minor variation) → fails  
Try A'' (same class again) → fails
```
**Signal:** You're in this loop if you're trying the same general approach 3+ times.
**Break:** Go back to Step 2. Your diagnosis of the cause is probably wrong.

### The Assumption Stack
```
Assume X → build on X → assume Y → build on Y → it fails
```
**Signal:** You realize mid-fix that an earlier assumption was wrong.
**Break:** Don't try to patch around it. Go back to the earliest wrong assumption and fix from there.

### The Silent Move-On
```
Tool call fails → note it internally → continue as if it worked
```
**Signal:** You're about to use a result that may not exist.
**Break:** Always verify before building on a result. Especially file reads, API calls, exec output.

### The Optimistic Retry
```
API returns 429 → immediately retry → 429 again → retry → 429 again
```
**Signal:** Error is rate/capacity-based, not logic-based.
**Break:** Wait before retrying. For 429: respect Retry-After header or wait at minimum 10-30 seconds.

---

## When the Protocol Doesn't Apply

Some failures are expected and don't need the full protocol:
- **First-time setup**: trying a new tool or API for the first time — some trial is normal
- **Explicit exploration**: when the task is to find what works (e.g. testing multiple approaches by design)
- **Known transient errors**: 429 rate limits, network blips — retry with backoff is correct

The protocol applies when: something was expected to work, it didn't, and you're about to try again.
