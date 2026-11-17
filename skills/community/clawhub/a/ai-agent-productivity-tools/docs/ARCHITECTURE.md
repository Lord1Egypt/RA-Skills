# Architecture — pa-pack

## Design Principles

1. **Modularity:** No component depends on another. They share only a context format.
2. **Transparency:** Every output includes reasoning. Nothing happens opaquely.
3. **Human-in-the-loop:** The human approves before any external action (send, schedule, delete).
4. **Minimal state:** Components are stateless where possible. Persistent state lives outside the skill.

## Context Format

All components accept a `context` object:

```json
{
  "user": {
    "name": "Anton",
    "timezone": "America/Chicago",
    "working_hours": "09:00-18:00",
    "preferences": {
      "email_tone": "concise",
      "calendar_buffer_minutes": 15
    }
  },
  "session": {
    "id": "sess_abc123",
    "previous_actions": []
  }
}
```

## Component Interaction

```
Incoming Message
      |
      v
   Triager
   (scores, suggests action)
      |
      +---> Reply Now --------> Drafter -----> Human Review -----> Send
      +---> Reply Later -------> Queue
      +---> Delegate -----------> Handoff
      +---> Ignore
```

## Extending the Pack

1. Create a new prompt file in `scripts/prompts/`
2. Add a command to `skill.json`
3. Document in `docs/`
4. Open a PR with a test case
