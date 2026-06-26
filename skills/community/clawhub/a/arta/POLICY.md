# ARTA Policy — Quick Reference

## Core Idea

Real-time self-awareness for agents across channels.

## Protocol

### Register
On session start:
```javascript
arta.register({ instanceId, channel, human, task })
```

### Update
On activity:
```javascript
arta.update({ instanceId, task, status })
```

### Query
When needed:
```javascript
arta.queryOtherThan(instanceId)  // What am I doing elsewhere?
arta.queryByChannel(channel)      // What's in this channel?
arta.queryByHuman(human)          // What's this human involved in?
```

### Leave
On session end:
```javascript
arta.leave({ instanceId })
```

## Simple In-Memory Implementation

```javascript
class ARTA {
  constructor(agentName) {
    this.instances = new Map();
  }
  register({ instanceId, channel, human, task }) { ... }
  update({ instanceId, task }) { ... }
  leave({ instanceId }) { ... }
  query() { return Array.from(this.instances.values()); }
  queryOtherThan(id) { return this.query().filter(i => i.instanceId !== id); }
}
```

## Rules

1. Register on session start
2. Update on meaningful task change
3. Query when human asks about other sessions
4. Leave on session end
5. Keep state in-memory only
6. No persistence needed
7. Private per agent

## Integration

In IBT Observe phase:
```javascript
const otherTasks = arta.queryOtherThan(sessionId);
if (otherTasks.length > 0) {
  // Agent is active elsewhere
}
```
