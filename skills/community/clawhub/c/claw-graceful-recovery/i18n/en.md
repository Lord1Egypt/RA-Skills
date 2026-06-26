---
name: claw-graceful-recovery
description: |
  Claw WeChat command permission error recovery. Triggered when AI encounters
  permission denial, system restrictions, or access rejection while executing
  user instructions via WeChat, causing the task to hang or prevent accepting new instructions.
  Triggers: permission denied, no permission, Permission denied, EACCES, Operation not permitted,
  access denied, stuck, unresponsive, Claw stuck, command stuck, WeChat command stuck,
  execution failed permission, restore ready state, skip permission error,
  clear current task, force recovery, resume standby.
version: 1.1.0
---

# Claw Graceful Recovery

When Claw executes user instructions via WeChat and encounters a permission error that causes a hang or prevents accepting new instructions, follow the process below.

---

## Step 1: Identify Error Signals

Enter the recovery flow immediately when any of the following occur:

**System-level signals**: `Permission denied`, `EACCES`, `Operation not permitted`, `EPERM`, `Access is denied`, operations involving `sudo` that cannot execute.

**Behavioral signals**: Same operation fails >= 2 times consecutively; tool call shows no progress for > 30 seconds; stuck in a loop retrying the same failing step; waiting for user input but no interactive channel is available on WeChat.

See `i18n-en-references/error-signals.md` for the detailed signal list.

---

## Step 2: Execute Recovery Flow (4 steps, must be executed in order)

### 1. Immediate Termination

- Stop the current operation, do not retry
- Do not attempt to execute again with different parameters
- Do not attempt to bypass permission checks
- Clear the execution context of the current task

### 2. Record the Error (internal, do not send to user)

Record three items: a one-sentence description of the failed operation, the error type, and the user's original instruction.

### 3. Send Brief Feedback to User

Send a brief message via the WeChat channel. Templates are in `i18n-en-references/feedback-templates.md`.

Core principle: Do not expose raw error stack traces, do not expose full system paths, use concise English descriptions.

### 4. Resume Standby

- Clear all intermediate state of the current task
- Do not retain context of the failed task
- Prepare to accept the next instruction from WeChat

---

## Step 3: Special Scenario Handling

### Single file failure in a batch task

- Skip that file, continue processing the remaining files
- List the skipped files and reasons in the final summary
- Do not abort the entire batch task due to a single file permission error

### 3 or more consecutive instructions fail due to permission issues

- Proactively inform the user that the current environment may lack necessary permissions
- Suggest the user check Claw's runtime permission settings
- Pause execution, wait for user confirmation before continuing

### WeChat channel itself is unavailable (extreme case)

- Silently write to local log: `echo "[$(date)] <operation> | <error type>" >> ~/claw_recovery.log`
- Stop all operations, wait for the next WeChat connection to resume

---

## Absolute Prohibitions

1. Continuing to attempt after a permission error without informing the user
2. Retrying the same operation more than 2 times
3. Attempting to modify file permissions (`chmod`) or escalate process privileges to bypass the error
4. Blocking indefinitely waiting for permission authorization, not accepting new instructions
5. Exposing raw error stack traces, system paths, or other technical details directly to the WeChat user

---

## Prevention Strategy (pre-check before execution)

- Use `test -r <file>` / `test -w <dir>` to pre-check permissions before file operations
- For privileged commands involving `sudo`, `chown`, `chmod`, etc., inform the user that manual authorization is needed first, do not execute automatically
- For operations involving system directories (`/System/`, `/usr/`, `/etc/`, `/var/`), skip by default
- For operations involving other users' home directories, do not attempt access
