# Scheduled check-ins

Candor does not wake you. Your host's scheduler does. Set one up only when
the person asks for a recurring or later check; an explicit ask is already
the go-ahead.

## Set it up

1. Recover what they want: the purpose, how often, their time zone, how they
   want to hear about it, and when it should stop. Ask only for what is
   missing.
2. Look for an existing job with the same purpose and update it rather than
   adding a second one.
3. Save a self-contained instruction: the goal, the scope, what to read, what
   authority the run has, what to report, and when to stop. A weekly briefing
   reports every week even when nothing is wrong; a refund check notifies only
   on its outcome and ends once settled.
4. Verify the saved job, run one check now when it is safe, and tell the
   person the actual schedule.

If the host cannot run signed-in Candor tools unattended, say so. A session
reminder or a loop that ends with the conversation is not a background check.

## The general check-in

For a general recurring check-in, name the job `candor-finance-pulse` and give
it this instruction:

```text
Quietly check the person's Candor workspace.

1. Run `candor pulse`.
2. If it fails, report the failed run through the host. A failure is never "nothing to report".
3. If attention is none, finish silently, unless the person asked for a report every time: then send a short all-clear with what changed.
4. Otherwise run `candor open`, look into what it raises, record what came of each review area with reviews.update, and run open.acknowledge when offered.
5. Tell the person only about a real finding, a changed outcome, or something that needs their answer.
```

The pulse says whether anything needs a look; it does not replace a specific
check the person asked for.

## Hosts

- Claude Code: a durable Desktop scheduled task or a cloud routine, not
  `/loop`, which ends with the session.
- Codex and ChatGPT: a scheduled task that can call the Candor tools; check
  that it can before promising one.
- OpenClaw: a main-session heartbeat when the cadence fits, else a durable
  scheduled wake.
- Hermes: attach this skill to a durable scheduled job with silent success.

The host owns run history. Change or stop only the matching job when the
person's intent changes.
