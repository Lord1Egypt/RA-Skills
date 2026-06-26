# fedica — OpenClaw skill

Compose and schedule cross-platform social posts on [Fedica](https://fedica.com) (X, LinkedIn, Threads, Mastodon, Bluesky, and more) via [`agent-browser`](https://github.com/vercel-labs/agent-browser).

This skill teaches an OpenClaw / Claude-style agent how to drive Fedica's web UI reliably: login, composer, image upload, the shadow-DOM date picker, the "When to publish?" modal, and the UTC-vs-local timezone gotcha.

## Why this skill exists

Fedica is great but its UI has a few non-obvious behaviours that trip agents up on first try:

- Times are displayed **only in GMT+00** — no per-user timezone setting is applied to the composer
- The image upload works only through a modal (`openTweetBoxAttachmentUploadModal(1)`), not the visible camera icon directly
- The date picker is a web component with day buttons in shadow DOM
- The Schedule button is a split button — the entry that opens the modal is labelled "Specific date"
- Bluesky's 300-grapheme limit is always the binding constraint for multi-platform posts

This skill documents the workflow and the exact JS/CSS selectors needed so an agent can ship a scheduled post in seconds instead of reverse-engineering the DOM each time.

## Install

Via [ClawHub](https://clawhub.com):

```bash
clawhub install fedica
```

Or copy the `SKILL.md` into your OpenClaw workspace's `skills/fedica/` directory.

## Requirements

- `agent-browser` (`npm i -g agent-browser`)
- A Fedica account with at least one connected platform
- Your own credential source (password manager, env vars, `~/.secrets/...`) — this skill does not manage secrets

## Safety

Fedica is public broadcast. The skill instructs the agent to **always confirm** text + platforms + local-time schedule with the user before the final confirm click.

## License

MIT — see `LICENSE`.
