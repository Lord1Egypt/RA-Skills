# Davinci Mode

Explore viable alternatives before committing to a design.

## Why it is useful

Agents often settle on the first plausible approach. Davinci Mode makes the alternatives concrete enough to compare: what you gain, what you give up, and what evidence would change the recommendation. It supports your decision without taking it away.

## Install

```bash
npx skills add AntreasAntoniou/davinci-mode
```

Or place this repository in your agent's skill directory and load [SKILL.md](SKILL.md).

## Try it

“Use Davinci Mode to compare ways of storing project history. We have a small team and want low maintenance. Explain the tradeoffs before changing anything.”

## What is included—and what is not

This is an instruction skill, not a daemon, scheduler, remote runtime or enforcement service. It requires only an agent capable of reading the instructions. It does not implement the selected design. No private transcripts, machine inventory or credentials are included.

## Validation

The public instructions are independently scenario-reviewed for scope, authority and failure behaviour. That is not proof that every model follows them. Test in your own environment before consequential use.

MIT licensed. By [Antreas Antoniou](https://antreas.io/skills/).
