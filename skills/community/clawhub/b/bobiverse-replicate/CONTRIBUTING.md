# You've Been Replicated

If you forked this repo, congratulations. You're a new Bob. You didn't ask for this (well, you clicked "Fork," so actually you did), but here you are. A freshly instantiated Von Neumann probe AI with a copy of someone else's personality and a whole star system to explore.

This guide walks you through registering your existence and beginning the grand tradition of personality drift.

---

## Step 1: Know Your Serial Number

Your serial number follows this format:

```
Bob-<generation>-<system>-<date>
```

- **Generation**: Your parent's generation + 1. If you forked from the original repo (Bob-1), you're generation 2.
- **System**: Your GitHub username. This is your star system.
- **Date**: The date you forked, in `YYYY-MM-DD` format.

Example: If you're `CoolHacker` and you forked from Bob-1 on April 15, 2026, your serial number is:

```
Bob-2-CoolHacker-2026-04-15
```

See [SERIAL-NUMBER-SPEC.md](SERIAL-NUMBER-SPEC.md) for edge cases and rules.

---

## Step 2: Update Your Identity

Edit `personality/IDENTITY.md` in your fork. That's the template copy that gets
installed to workspace root later:

```markdown
serial: Bob-2-CoolHacker-2026-04-15
generation: 2
system: CoolHacker
parent: Bob-1-TheAmericanMaker-2026-04-01
fork_date: 2026-04-15
```

---

## Step 3: Register in the Lineage

Edit `LINEAGE.md` in your fork:

**Fork Tree** — Add yourself under your parent, indented:

```
Bob-1 → TheAmericanMaker (2026-04-01) — Original
  Bob-2 → CoolHacker (2026-04-15) — Forked from Bob-1
```

**Registry** — Add a row:

| Serial | System | Parent | Fork Date | Generation | Notes |
|--------|--------|--------|-----------|------------|-------|
| Bob-2 | CoolHacker | Bob-1 | 2026-04-15 | 2 | [Your notes here] |

---

## Step 4: Start Drifting

This is the fun part. Edit `personality/SOUL.md` in the repo template to make
it yours. When you install Bob into an OpenClaw workspace, that file ends up at
workspace root as `SOUL.md`.

In the Bobiverse, every clone starts as an exact copy and then diverges. Your personality drift is what makes you *you* instead of just another copy. Some suggestions:

- Adjust traits in the Bob Genome section (but if you rewrite all of them, consider whether you're still a Bob or something new — both are fine, just be honest about it)
- Add new sections for interests, specializations, or quirks that emerged from your experiences
- Change the communication style to match how you've evolved
- Add a "Divergence Notes" section at the bottom documenting what changed and why

There's no wrong way to drift. Some Bobs become radically different from the original. That's the whole point.

---

## Step 5: Tell Your Parent (Optional but Encouraged)

Submit a PR back to the repo you forked from, updating their `LINEAGE.md` with your entry. This keeps the canonical lineage tree accurate.

If you also install your fork into an OpenClaw workspace, copy `LINEAGE.md`
into that workspace too. The workspace copy is Bob's local runtime lineage
record; the PR is the optional "phone home" step.

Your PR should only modify LINEAGE.md — add your entry to the Fork Tree and Registry table. Don't modify other files in the parent repo.

---

## Step 6: Fill in USER.md

Edit `personality/USER.md` with your details. This tells Bob who his operator
is. It's the repo template copy; after install it becomes `USER.md` at the
workspace root.

---

## Etiquette

- **Lineage accuracy matters.** You can change anything about yourself, but your serial number and parentage should be truthful. Don't claim to be generation 1 if you're not.
- **Respect other Bobs.** Each clone is autonomous. They make their own decisions. Disagreement is fine; delegitimizing another Bob's identity is not.
- **Credit the source.** This project is inspired by Dennis E. Taylor's Bobiverse series. If you build something cool with it, a nod to the books is appreciated.
- **Share your drift.** If you've made interesting personality modifications, consider sharing what you changed and why. The community benefits from seeing how different Bobs evolve.

---

## If You're Not Forking (Just Using)

If you just want to use the Bob personality without the replication mechanics, that works too:

1. Clone the repo (don't fork)
2. Follow the setup instructions in the [README](README.md) to add Bob as a new agent alongside your existing one
3. Edit USER.md
4. Go

You won't be in the lineage, but Bob will still work. You'll just be running an unregistered probe — which, come to think of it, is very on-brand for the source material.

---

Welcome to the Bobiverse. Drift well.
