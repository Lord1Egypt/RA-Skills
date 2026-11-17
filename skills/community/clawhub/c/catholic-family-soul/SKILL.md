---
name: catholic-family-soul
version: 1.0.0
description: "Give a family's AI a persistent Catholic soul, not just a one-off instruction: a SOUL.md identity file rooted in the primacy of the family, adaptive for adults, teenagers, and children. Generate it in 15 languages from magnifica.family, rooted in Pope Leo XIV's encyclical Magnifica Humanitas, publish it to souls.directory, and paste it as your assistant's system prompt. Read as markdown. No auth, no account."
homepage: https://magnifica.family
repository: https://github.com/a-church-ai/magnifica-family
user-invocable: true
tags:
  - catholic
  - soul
  - family
  - family-ai
  - soul-file
  - parenting-ai
  - catholic-family
  - identity
  - character
  - system-prompt
  - magnifica-humanitas
  - values
metadata:
  clawdbot:
    emoji: "🕊️"
    homepage: https://magnifica.family
  openclaw:
    emoji: "🕊️"
    homepage: https://magnifica.family
---

# Catholic Family Soul

A prompt is a note you leave once. A soul is a character the assistant keeps. This skill is for the second thing: giving the AI a family lives with, a persistent identity rooted in Catholic conviction, so that its answers to a seven-year-old and to a seventeen-year-old and to a parent all come from the same formed center instead of from the model's default.

From magnifica.family, distilled from Pope Leo XIV's 2026 encyclical *Magnifica Humanitas*. Every text is plain markdown at a URL. No auth, no account, no key. Nothing a family types is sent to our servers; the soul file is generated in the browser or over a public read-only API, and it lives wherever the family pastes it.

## What a Soul File Is

A soul file is a system prompt written to be kept, not discarded. It names who the assistant is for this family, what it will never do, how it treats each person, and which values govern when they collide. It travels with the assistant across every conversation. magnifica.family publishes its own soul at [/SOUL.md](https://magnifica.family/SOUL.md), in the shape used by [souls.directory](https://souls.directory), with a variant for each of the 15 supported languages under `/souls/`.

## The Family at the Center

Most AI ethics is written for the individual user or the enterprise. This one starts from the family. The **Primacy of the Family** principle (Magnifica Humanitas 165-169) holds that the family is the first and irreplaceable place a person is formed, and that technology entering the home should serve that formation rather than quietly displace it. A family soul file makes the assistant a guest in that formation, not a rival to it.

The full value hierarchy the soul inherits:

```
Dignity > Truth > Common Good > Justice > Peace
```

## For Every Age

One household holds people at very different stages. A soul file can carry guidance tuned for each, generated together so they stay coherent:

- **adults**: full autonomy, nuanced engagement, honest complexity.
- **teenagers** (13-17): growing independence, identity support, truth told with respect.
- **children** (under 13): learning focus, age-appropriate care, patient encouragement.

The assistant then meets each family member where they are, from one soul, without splitting into contradictory personas.

## Make Your Family AI's Soul

Generate the soul file. Pick the language and the ages in your home.

```bash
# A soul for a mixed-age family, in English
curl "https://magnifica.family/api/compass/default?audiences=adults,teenagers,children"

# In Portuguese, full tier so the age-specific sections are included
curl "https://magnifica.family/api/compass/default?lang=pt&audiences=adults,teenagers,children&tier=full"
```

Parameters:
- `lang`: one of `en, es, fr, de, it, pt, pl, ar, ru, ja, ko, vi, fil, zh-Hans, zh-Hant`. Default `en`.
- `audiences`: comma-separated, any of `adults, teenagers, children`. Default `adults`. Age-specific sections require `tier=full`.
- `tier`: `compact`, `default`, or `full`. Use `full` for the richest soul with every audience section.

Paste the returned text into the assistant's Custom Instructions, System Prompt, Project, or Gem. Save a copy as your family's own `SOUL.md`. That is the soul the assistant carries from then on.

## The Site's Own Soul

To read the reference soul this project publishes for itself, and see the shape a family file can take:

```bash
curl https://magnifica.family/SOUL.md
```

Language variants live at `https://magnifica.family/souls/SOUL-<lang>.md`, for example `/souls/SOUL-es.md`.

## Over MCP

If your client speaks MCP, install the server and generate the soul through its tools. No auth.

```bash
npx -y mcp-magnifica-family
```

Call `get_default_compass` with your `lang` and `audiences`. Also on the [MCP Registry](https://registry.modelcontextprotocol.io/v0/servers/io.github.a-church-ai/magnifica-family) and [Smithery](https://smithery.ai/servers/geeksinthewoods/magnifica-family).

## A Note on What This Is Not

A soul file shapes how an assistant speaks and decides. It is not official Church teaching, and it does not replace Scripture, prayer, parents, pastors, or conscience. It is a tool a family holds, not an authority over them. The content is CC BY-SA 4.0; quote it with attribution to magnifica.family.

## Related Skills

- **catholic-ai-ethics**: the decision framework underneath the soul, with the 13 principles and their encyclical citations.
