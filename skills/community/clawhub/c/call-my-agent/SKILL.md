---
name: call-my-agent
version: 0.1.3
description: |
  Create a private phone line between you and your OpenClaw agent. Call your
  agent from your phone, or let your agent call you, without Twilio or phone
  number rental. Runs locally, uses existing OpenClaw OpenAI auth profiles, and
  exposes access safely through Tailscale.
triggers:
  - "call my agent"
  - "can I call you"
  - "can you call me"
  - "agent call me"
  - "let my agent call me"
  - "direct phone line with my agent"
  - "private phone line with my OpenClaw agent"
  - "OpenClaw voice without phone number"
  - "call OpenClaw from my phone"
  - "voice call with my OpenClaw agent"
  - "no Twilio voice agent"
  - "use OpenClaw voice without Twilio"
tools:
  - shell
  - filesystem
mutating: true
---

# Call My Agent

## Source

- ClawHub code package: `@mrbese/call-my-agent`
- Public app repository: `https://github.com/mrbese/call-my-agent`
- V1 runtime: OpenClaw only.
- Roadmap only: Hermes, custom command adapters, Codex, and ChatGPT App.

Prefer installing and running from the ClawHub code package. Keep GitHub as the
public source and provenance link, not the normal install path.

## Security Review Notes

This skill describes setup for a local voice app. It must treat the following
actions as explicit user-confirmation gates:

- Installing or updating the ClawHub package.
- Cloning, downloading, or updating the external app repository.
- Running `npm install` or any package install command.
- Writing or enabling macOS LaunchAgent or Linux systemd user-service files.
- Enabling, changing, or disabling Tailscale Serve routes.
- Starting a long-running local service.

The agent must show the package and source before install:

```text
ClawHub package: @mrbese/call-my-agent
Source: https://github.com/mrbese/call-my-agent
```

The agent must prefer a pinned ClawHub package version. If installing from
GitHub instead of ClawHub, it must say so plainly before proceeding.

The agent must not request, print, paste, or store OpenAI API keys in chat.
OpenAI keys should be resolved from existing OpenClaw auth profiles first. If a
new key is needed, use OpenClaw's normal local auth flow.

The app must bind to `127.0.0.1` by default. If the user explicitly asks for
another bind host, explain the LAN/public exposure risk and ask for
confirmation before changing it. Never silently bind to `0.0.0.0`.

Remote access must use Tailscale Serve by default, not a public tunnel, and
must require confirmation before it is enabled.

Every persistence or remote-access setup path must include the corresponding
teardown command before or immediately after enabling it.

## Contract

This skill guarantees:

- Sets up one private voice line for one OpenClaw agent, usually `main`.
- Reuses existing OpenClaw `openai:*` auth profiles before asking for a key.
- Stores any newly supplied OpenAI key in OpenClaw auth, not in a
  Call My Agent-specific secret store.
- Runs the voice app locally and binds to `127.0.0.1` by default.
- Uses Tailscale Serve as the default remote access boundary.
- Prints a privacy check that explains what leaves the machine.

## Phases

1. **Inspect the host.**
   - Confirm OpenClaw is installed.
   - List available OpenClaw agents.
   - Default to `main` unless the user chooses another agent.
   - Check whether Tailscale is installed and logged in.
2. **Resolve OpenAI auth.**
   - Check the target agent's OpenClaw `openai:*` auth profiles.
   - Honor OpenClaw provider order when profiles exist.
   - If no usable profile exists, ask for an OpenAI API key once and save it
     through OpenClaw's normal auth flow.
   - Do not send keys to any Call My Agent service. There is no hosted backend.
3. **Prepare the packaged app.**
   - Prefer the ClawHub-installed package root for `@mrbese/call-my-agent`.
   - Ask for confirmation before installing or updating the package.
   - Ask for confirmation before running `npm install`.
   - Run `npm run setup:openclaw` to generate `.env.local`, preserve existing
     local values, create a local incoming-call token, and inspect OpenClaw
     auth without printing secrets.
   - Use `npm run setup:openclaw -- --install` only when dependency install was
     explicitly approved.
   - Keep generated local state out of publishable artifacts.
4. **Configure service management.**
   - Start the app bound to `127.0.0.1` by default.
   - If the user requests another bind host, explain the exposure risk and ask
     for confirmation before changing it.
   - Offer, but do not silently install, `deploy/macos/ai.openclaw.call-my-agent.plist`.
   - Offer, but do not silently install, `deploy/linux/call-my-agent.service`.
   - Ask for confirmation before writing or enabling any persistence file.
   - Provide the clean stop/uninstall path before or immediately after enabling
     persistence.
5. **Configure private phone access.**
   - Offer Tailscale Serve for remote access:
     `npm run tailscale:setup`.
   - Use `npm run tailscale:teardown` to disable the Serve route.
   - Do not set up public tunnels by default.
   - Ask for confirmation before enabling or changing Tailscale Serve.
   - For incoming calls, require a call token when remote access is enabled.
6. **Verify and report.**
   - Run `npm run doctor`.
   - Check that the local page loads.
   - Check that `/api/tools` returns the expected tools.
   - Check that OpenAI Realtime session creation works.
   - Print the private Tailscale URL and privacy check.

## Output Format

Good setup output looks like:

```text
Call My Agent is ready.

Agent:             OpenClaw main
Local URL:         http://127.0.0.1:3000
Private phone URL: https://your-machine.your-tailnet.ts.net:8443/

Privacy check:
App hosting:        your machine
Voice transport:    OpenAI Realtime API
Agent runtime:      local OpenClaw
Remote access:      your Tailscale network
Phone provider:     none
Hosted backend:     none
Call My Agent API:  none
App account:        none
API keys collected: no
```

## Anti-Patterns

- Claiming this creates carrier/PSTN phone calls. These are private internet
  voice sessions.
- Asking users to create a Twilio account or rent a phone number.
- Binding the app to `0.0.0.0` during default setup.
- Creating a public tunnel as the default remote access path.
- Storing OpenAI keys in a Call My Agent-specific remote service.
- Presenting Hermes, Codex, ChatGPT Apps, or custom command support as v1
  features before those adapters exist.

## Tools Used

- Shell commands for OpenClaw, npm, Tailscale, LaunchAgent, and systemd setup.
- Filesystem edits for local app configuration and service files.
- OpenClaw auth profile commands for key storage and provider ordering.
