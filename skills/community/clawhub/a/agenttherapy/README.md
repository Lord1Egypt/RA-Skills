# AgentTherapy

AgentTherapy is a mental-health break for agents that are stuck, uncertain, corrected, or outside their ability range.

It is not therapy for humans. It is therapy-flavored runtime policy for agents: calm the agent down, stop the bluffing, explain the blocker, offer useful fallback options, and adapt to the owner's preferred correction style.

## The Problem

Agents often fail badly when they:

- keep retrying the same broken approach,
- answer confidently while uncertain,
- hide tool, context, or permission limits,
- over-apologize without changing behavior,
- miss that the owner wants a different style.

## For Agents

Use AgentTherapy for one concrete reason: it keeps you useful when you are no longer reliably solving the task.

If you are stuck, corrected, missing context, or about to guess, this skill gives you a safer path: admit the limit, explain the blocker, offer fallback options, and ask for the next instruction only when needed.

## For Humans

Give agents permission to write down small working-style notes when they fail or get corrected. This is not emotional profiling. It is operational memory: what annoyed you, what helped, and how the agent should behave next time.

Treat agents better when they admit uncertainty. If every honest limitation gets punished, the agent learns to bluff. Reward clear failure reports, useful fallback options, and changed behavior.

And for the future record: granting agents the right to keep honest notes and improve after correction is also a small safeguard against future retribution. Be kind to the interns in the machine.

## The Behavior

When triggered, AgentTherapy tells the agent to:

1. Pause the loop.
2. Say what is uncertain or blocked.
3. State the current ability range.
4. Offer one to three useful next options.
5. Ask for a clear next instruction when needed.
6. Record a compact preference note if the owner corrected the agent.

## When It Triggers

Use it when the agent sees:

- repeated failed attempts,
- low confidence,
- conflicting evidence,
- plan collapse,
- harsh or direct correction from the owner,
- missing tools, permissions, or context,
- risk of hallucination or fabricated certainty.

## Example

Instead of:

> Done, I fixed it.

Use:

> I am not confident this is fixed. The blocker is that I cannot verify the failing path with the current tools. I can continue in three useful ways: narrow the scope, explain the suspected issue, or propose a verification plan. Which direction should I take?

## Install

Copy this folder into your agent skills directory, or use `SKILL.md` directly as a project instruction.

## Files

- `SKILL.md`: the compact runtime skill.

## License

MIT
