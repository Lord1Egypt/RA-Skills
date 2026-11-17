# ambition

> An OpenClaw skill that makes your agent *less obedient and more ambitious*.

Say **"ambition"** (or "be more ambitious," "elevate this," "go deeper," "go bigger") on whatever you're working on, and your agent stops doing exactly what you asked — and instead reads your actual context, figures out the *better* version of the task, and goes and builds that.

It's based on [Felix Rieseberg's "How to be more ambitious: A tutorial for humans with models"](https://felixrieseberg.com/how-to-be-more-ambitious-a-tutorial-for-humans-with-models/), distilled into something an agent can act on in the middle of real work.

## The idea

Models are "astounding in some directions, while inadequate in others." Most people under-use them — asking for the capital of France when they could be discovering a planet. The gap isn't capability; it's **ambition**. Felix breaks ambition into four flavors:

- **Altitude** — chase the goal *behind* the goal. Not "fix this crash" but "keep the app crash-free." Not "update the deck" but "redesign how decisions get made."
- **Depth** — do one thing so well an expert would learn from it. Raw data over summaries, real statistical instruments over hand-waved tables, unreasonable targets treated as obviously achievable.
- **Range** — pull in fields the task doesn't obviously need. Restate the noun as a verb and the useful disciplines appear. Then *do what each specialist does* — don't role-play one.
- **Speed** — same result, less time. (Usually not what "be ambitious" means.)

This skill teaches the agent to read the live context of what you're already doing, pick the axis that actually moves *this* task, rewrite it into a concrete harder objective, and then **execute the elevated version with an outside check** — not just describe it.

## Install

With [OpenClaw](https://openclaw.ai):

```bash
# From this git repo
openclaw skills install https://github.com/abhione/ambition-skill

# ...or clone and install locally
git clone https://github.com/abhione/ambition-skill
openclaw skills install ./ambition-skill
```

Install for every local agent with `--global`:

```bash
openclaw skills install https://github.com/abhione/ambition-skill --global
```

The skills watcher picks it up on the next agent turn. Verify with:

```bash
openclaw skills list | grep ambition
```

## Use

In the middle of any task, just say it:

> **ambition**

or

> be more ambitious with this
> elevate this
> go deeper on the churn analysis

The agent will tell you the jump it's making ("you asked for X; the version worth building is Y, because…") and — unless it meaningfully changes scope, spend, or does something external — just go do it.

## What's inside

- `SKILL.md` — the skill itself (prose, context-driven; no rigid step form)
- `LICENSE` — MIT

## Credit

Framework by [Felix Rieseberg](https://felixrieseberg.com/how-to-be-more-ambitious-a-tutorial-for-humans-with-models/). Packaged as an OpenClaw skill. Image in Felix's original post: Francisco Goya, *"Modo de volar" (A Way of Flying)*.

## License

MIT — see [LICENSE](./LICENSE).
