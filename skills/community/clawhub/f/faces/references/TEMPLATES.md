# Face Templates

Use `${face-username}` in any message to reference a face's profile. The token is replaced with the face's display name in the message text, and the face's profile is injected as context for the model.

## With a primary face

When a face is set in the model field, it becomes the persona (system prompt). Templates bring additional faces in as context:

```bash
# Alice is the persona; Bob's profile injected as context
faces chat:chat alice --llm gpt-4o-mini \
  -m 'You are debating ${bob}. Argue your position on space exploration.'

faces chat:messages alice@claude-sonnet-4-6 \
  -m 'You are debating ${bob}. State your position on AI safety.'

# Multiple references
faces chat:responses alice@gpt-4o-mini \
  -m 'Moderate a debate between ${bob} and ${carol}. Summarize their positions.'
```

If you reference the primary face itself (e.g. `alice@gpt-4o-mini` with `${alice}` in the message), the token is replaced with Alice's display name but no duplicate profile is added.

## Without a primary face (bare model)

Pass a bare model name to skip the persona entirely. The model acts as a standard assistant with face profiles injected as context:

```bash
faces chat:messages claude-sonnet-4-6 \
  -m 'Compare the worldviews of ${alice} and ${bob}. Where do they agree?'

faces chat:responses gpt-4o-mini \
  -m 'You are moderating a debate between ${alice} and ${bob}.'
```

Note: `chat:chat` requires a face username as the first argument, so bare model usage is only available via `chat:messages` and `chat:responses`.

## Escaping

To include a literal `${...}` without triggering expansion, escape with a backslash: `\${name}`.

## Rules

- Referenced usernames must be faces you own.
- Synthetic faces (boolean formulas) work in templates.
- Unknown usernames return `422` with a list of the unrecognized names.
- If an API key has a face allowlist, template-referenced faces are checked against it.
- Templates are expanded once — profile text is never re-scanned for nested `${...}` tokens.
