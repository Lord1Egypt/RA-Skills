---
name: clawstore
description: Search, install, and publish OpenClaw agent packages from the Clawstore registry. Use when the user wants to find agents, install them, or publish their own.
user-invocable: true
argument-hint: [search query or command]
---

Clawstore is the package manager for OpenClaw agents. Use the `clawstore` CLI to search, install, and publish agent packages from the registry at useclawstore.com.

## Prerequisites

The CLI must be installed globally:

```bash
npm install -g clawstore
```

Verify with `clawstore --version`.

## When to use this skill

- User asks to find, discover, or browse AI agents → use **search**
- User asks to install or add an agent → use **install**
- User asks to publish or share their agent → use **publish** flow
- User asks what agents they have → use **list**
- User asks to update agents → use **update**
- User asks to create a new agent package → use **init**

## Commands

### Search for agents

```bash
clawstore search "productivity"
clawstore search "code review"
```

Returns a list of matching agents with scope, name, and description.

### Get agent details

```bash
clawstore info @scope/agent-name
```

Shows the full description, version, download count, rating, and category.

### Install an agent

```bash
# Latest version
clawstore install @scope/agent-name

# Specific version
clawstore install @scope/agent-name@1.2.0
```

Downloads the agent package and sets it up in the local OpenClaw workspace.

### List installed agents

```bash
clawstore list
```

Shows all locally installed agents with their versions and update policies.

### Check for updates

```bash
clawstore update
```

Checks the registry for newer versions of installed agents.

### Authenticate

```bash
clawstore login
```

Opens a browser-based GitHub OAuth flow. Required before publishing.

### Create a new agent package

```bash
clawstore init
```

Scaffolds `agent.json` and the recommended directory structure:

```
my-agent/
├── agent.json          # Package manifest
├── app/
│   ├── IDENTITY.md     # Agent persona
│   ├── AGENTS.md       # Capabilities
│   ├── SOUL.md         # Personality
│   └── knowledge/      # Reference files
└── store/
    ├── icon.png        # Store icon (256x256 PNG)
    └── screenshots/    # Store listing images
```

### Validate a package

```bash
clawstore validate
```

Checks that `agent.json` is valid and the package structure is correct. Always run before publishing.

### Preview a tarball

```bash
clawstore pack
```

Builds the tarball without publishing. Useful for inspecting what will be uploaded.

### Publish

```bash
clawstore publish
# or from a specific directory
clawstore publish ./path/to/agent
```

Uploads the agent package to the Clawstore registry. Requires `clawstore login` first.

### Yank a version

```bash
clawstore yank @scope/agent-name@1.0.0 --reason "critical bug"
```

Marks a published version as yanked. It won't be installed by default but remains downloadable for existing users.

## Guidance

- **Search first**: Before recommending an agent, search to see what's available.
- **Check info**: Use `clawstore info` to verify an agent's quality (downloads, rating) before installing.
- **Validate before publish**: Always run `clawstore validate` before `clawstore publish` to catch issues early.
- **Use init for new packages**: Don't hand-write `agent.json` — use `clawstore init` to get the correct structure.
- **Login once**: Authentication persists across sessions. Only run `clawstore login` if the user hasn't authenticated yet.
