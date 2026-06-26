# Practical Recipes

## Minimal sequence
1. List agents
2. Create chat
3. Send message to agent-scoped console chat endpoint
4. Read SSE answer

## Example request flow

### List agents
```bash
curl -s http://COPAW_HOST:PORT/api/agents
```

### Create chat
```bash
curl -s -X POST http://127.0.0.1:8088/api/chats \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "neuromant-api-test",
    "session_id": "neuromant-api-session",
    "user_id": "neuromant",
    "channel": "console",
    "meta": {}
  }'
```

### Send message
```bash
curl -sN -X POST http://127.0.0.1:8088/api/agents/default/console/chat \
  -H 'Content-Type: application/json' \
  -d '{
    "channel": "console",
    "user_id": "neuromant",
    "session_id": "neuromant-api-session",
    "input": [
      {
        "role": "user",
        "content": [
          {"type": "text", "text": "Привет. Ответь одной короткой фразой: ты жив?"}
        ]
      }
    ]
  }'
```

## Example skill folder layout

### Minimal skill
```text
copaw-api-chat/
├── SKILL.md
└── references/
    ├── overview-auth-scoping.md
    ├── chats-console-sse.md
    ├── agents-models-skills-tools.md
    ├── workspace-mcp-cron.md
    └── practical-recipes.md
```

### Project-local knowledge next to skill
```text
project/
├── .agents/
│   └── skills/
│       └── copaw-api-chat/
│           ├── SKILL.md
│           └── references/
└── notes/
```

### Split between quick routing and deeper refs
```text
copaw-api-chat/
├── SKILL.md          # short router
└── references/       # detailed API notes
```

## Confirmed practical test
A direct local API test succeeded with this sequence:
- list agents → `default`
- create chat
- send message in that session context
- receive text answer from CoPaw
rames return the assistant response
