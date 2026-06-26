# Report Template

Use this shape when summarizing Better Every Run output in chat:

```text
Better Every Run report:

- Events captured: N
- Lessons accepted: M
- Open proposals: K
- Promotion suggestions: P
- Quarantined/superseded/expired: Q/S/X
- Local store: `.better-every-run/`
- Durable files changed: none or `<path>`

Captured lessons:
1. ...
2. ...

No open proposals. Create a lesson card before durable promotion. Promote only lessons that should become memory, skill behavior, or eval coverage; quarantine or supersede the rest. No durable memory file was changed unless listed above.
```

Keep the user-facing report short. Mention internal commands only when debugging or auditing.
