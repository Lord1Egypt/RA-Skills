# ant CLI recipes

Use these when the user explicitly wants Anthropic's native CLI instead of the Python helper.

## Install and verify

```bash
ant --version
```

## Agents

### Create

```bash
ant beta:agents create \
  --name "Coding Assistant" \
  --model '{id: claude-sonnet-4-6}' \
  --system "You are a helpful coding agent." \
  --tool '{type: agent_toolset_20260401}'
```

### Update

```bash
ant beta:agents update \
  --agent-id "$AGENT_ID" \
  --version "$AGENT_VERSION" \
  --system "You are a helpful coding agent. Always write tests."
```

### Versions

```bash
ant beta:agents:versions list --agent-id "$AGENT_ID"
```

### Archive

```bash
ant beta:agents archive --agent-id "$AGENT_ID"
```

## Environments

### Create

```bash
ant beta:environments create \
  --name "python-dev" \
  --config '{type: cloud, networking: {type: unrestricted}}'
```

### List and retrieve

```bash
ant beta:environments list
ant beta:environments retrieve --environment-id "$ENVIRONMENT_ID"
```

### Archive and delete

```bash
ant beta:environments archive --environment-id "$ENVIRONMENT_ID"
ant beta:environments delete --environment-id "$ENVIRONMENT_ID"
```

## Sessions

### Create

```bash
ant beta:sessions create \
  --agent "$AGENT_ID" \
  --environment "$ENVIRONMENT_ID"
```

### Retrieve and list

```bash
ant beta:sessions retrieve --session-id "$SESSION_ID"
ant beta:sessions list
```

### Archive and delete

```bash
ant beta:sessions archive --session-id "$SESSION_ID"
ant beta:sessions delete --session-id "$SESSION_ID"
```

## Events

### Send a user message

```bash
ant beta:sessions:events send \
  --session-id "$SESSION_ID" \
<<'YAML'
events:
  - type: user.message
    content:
      - type: text
        text: Summarize the repo README
YAML
```

### Stream

```bash
ant beta:sessions stream --session-id "$SESSION_ID"
```

### List history

```bash
ant beta:sessions:events list --session-id "$SESSION_ID"
```

## When ant is the better fit

Use ant when:

- the user wants vendor-native commands
- you want copy-paste CLI docs
- you are manually debugging payloads or API behavior

Use the Python helper when:

- you want safer repeatable patterns
- you want SDK fallback behavior
- you want consistent automation and test coverage
