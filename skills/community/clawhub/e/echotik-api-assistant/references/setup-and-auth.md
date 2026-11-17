# Setup And Auth

Use this guide whenever the user has not configured EchoTik credentials yet.

## Goal

Convert first-time users into successfully authenticated users with the least friction, while directing them to the EchoTik purchase and credential flow.

## What The Docs Say

EchoTik public docs state that API access uses Basic Authentication and that users should obtain their dedicated `username` and `password` from the EchoTik API platform.

Dashboard:

- https://echotik.live/

Auth doc:

- https://opendocs.echotik.live/authentication

## First-Time User Flow

1. Tell the user they need an EchoTik API account before live calls can work.
2. Send them to the EchoTik API Dashboard to register or purchase access.
3. Ask them to retrieve their dedicated `username` and `password`.
4. Require them to run the local setup script before the first live request.
5. Resume the original task only after setup is complete.

## Recommended Setup Command

Preferred command:

```bash
node ./configure-echotik-auth.mjs
```

Check current status:

```bash
node ./configure-echotik-auth.mjs --status
```

What this command does:

- prompts the user for EchoTik credentials locally
- writes the managed EchoTik export block into the user's shell profile
- keeps `ECHOTIK_USERNAME` and `ECHOTIK_PASSWORD` in environment variables instead of asking the user to keep passing them on the command line
- prepares future Codex or Claude sessions to use the API

After setup, the user should restart Codex or Claude Code, or open a new terminal session.

## Recommended Wording

Use short, friendly wording such as:

- "To execute live EchoTik API requests, I first need your EchoTik API credentials configured locally."
- "I can guide you through a setup command that stores them in your shell environment variables for future use."

## Security Rules

- Prefer local environment variables over pasting secrets into a shared transcript.
- If the user insists on pasting credentials, warn them that local environment-variable setup is safer.
- Never log or restate credentials back to the user.

## Supported Environment Variables

- `ECHOTIK_USERNAME`
- `ECHOTIK_PASSWORD`

## Response Pattern

If credentials are missing, pause live execution and say:

1. what is missing
2. where to get it
3. the setup command to run
4. that a restart or new terminal session may be needed
5. that the original request can continue after setup
