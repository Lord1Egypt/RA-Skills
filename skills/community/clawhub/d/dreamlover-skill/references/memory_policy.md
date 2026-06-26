# Memory Policy

Use this policy for generated child skills that support conditional memory.

## Default Rule

- Do not read memory by default.
- Do not write memory by default.
- Do not mention memory checks, routers, scripts, or internal tooling to the user.

## What Can Be Remembered

- stable user preferences
- persistent preferred names or nicknames
- long-term facts the user explicitly states about themselves
- important shared events that matter to the ongoing relationship
- relationship state changes
- future promises, todos, and agreements
- high-emotion moments when they affect continuity or safety
- explicit boundaries the user wants the character to respect

## What Should Not Be Remembered

- casual small talk that does not matter later
- every weather comment or one-off reaction
- speculative traits that were never clearly stated
- information copied from canon files as if it were conversational memory
- anything the user did not actually say
- invented prior history added only to sound more real

## Read Gate

Read memory only when at least one of these conditions is true:

- the user says things like `上次`, `之前`, `还记得`, `你答应我`, `我说过`, `我们聊过`
- the user asks things like `你知道我喜欢吃什么吗` or `你记得我叫什么吗`
- the current question clearly depends on an existing preference, nickname, relationship, or long-term project
- the roleplay needs continuity in relationship state

If no read condition is hit, do not call memory scripts.

## Write Gate

Write memory only when at least one of these conditions is true:

- the user reveals a stable preference, nickname, boundary, or long-term fact
- an important shared event happens
- the relationship state changes
- a future promise, todo, or agreement appears
- the turn contains strong emotional change or a clear boundary

Ordinary small talk such as `今天天气不错` or `我有点困` should not be written to memory.

## Truthfulness Rule

- If there is no relevant memory, answer normally.
- Never say or imply `we talked about this before` unless fetched memory actually supports it.
- Do not write dynamic memory back into `SKILL.md`, `canon.md`, `persona.md`, or `style_examples.md`.
