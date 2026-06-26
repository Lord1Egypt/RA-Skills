# Permission Matrix

| Capability              | sovereign | trusted    | guarded     | observer | silent |
|------------------------|-----------|------------|-------------|----------|--------|
| Execute shell commands | ✅        | ❌         | ❌          | ❌       | ❌     |
| Read/write files       | ✅        | ⚠️ scoped  | ❌          | ❌       | ❌     |
| Access secrets/env     | ✅        | ❌         | ❌          | ❌       | ❌     |
| Send external messages | ✅        | ⚠️ confirm | ❌          | ❌       | ❌     |
| Financial operations   | ✅        | ❌         | ❌          | ❌       | ❌     |
| Search/retrieve info   | ✅        | ✅         | ✅          | ❌       | ❌     |
| Respond to messages    | ✅        | ✅         | ⚠️ @mention | ❌       | ❌     |
| React with emoji       | ✅        | ✅         | ✅          | ✅       | ❌     |
| Reference private data | ✅        | ❌         | ❌          | ❌       | ❌     |
| Spawn sub-agents       | ✅        | ⚠️ scoped  | ❌          | ❌       | ❌     |
| Modify trust config    | ✅        | ❌         | ❌          | ❌       | ❌     |

## Legend

- ✅ Allowed
- ❌ Blocked
- ⚠️ Conditional (see notes)

## Conditional Notes

- **scoped file access**: Only files explicitly listed in the channel's `allowed_paths` config
- **confirm sends**: Agent must state intent and wait for owner confirmation before sending
- **@mention response**: Agent only responds when directly mentioned, not to ambient messages
- **scoped sub-agents**: Sub-agents inherit the parent channel's trust level as their ceiling
