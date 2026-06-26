# ARTA Template — Drop-in Implementation

## Quick Start

```javascript
const ARTA = require('./arta');

const arta = new ARTA('your-agent-name');

// Session start
arta.register({
  instanceId: 'session-123',
  channel: 'telegram:456',
  human: 'human-name',
  task: 'initial task'
});

// Update task
arta.update({
  instanceId: 'session-123',
  task: 'new task'
});

// Query
const otherTasks = arta.queryOtherThan('session-123');

// Session end
arta.leave({ instanceId: 'session-123' });
```

## Full Class

```javascript
class ARTA {
  constructor(agentName) {
    this.agentName = agentName;
    this.instances = new Map();
  }

  register({ instanceId, channel, human, task = 'idle', status = 'active' }) {
    this.instances.set(instanceId, {
      instanceId,
      channel,
      human,
      task,
      status,
      started: Date.now(),
      lastHeartbeat: Date.now()
    });
  }

  update({ instanceId, task, status = 'active' }) {
    const instance = this.instances.get(instanceId);
    if (instance) {
      instance.task = task;
      instance.status = status;
      instance.lastHeartbeat = Date.now();
    }
  }

  leave({ instanceId }) {
    this.instances.delete(instanceId);
  }

  query() {
    return Array.from(this.instances.values());
  }

  queryOtherThan(instanceId) {
    return this.query().filter(i => i.instanceId !== instanceId);
  }

  queryByChannel(channel) {
    return this.query().filter(i => i.channel === channel);
  }

  queryByHuman(human) {
    return this.query().filter(i => i.human === human);
  }
}
```

## Integration Points

### Session Start
```javascript
arta.register({ instanceId, channel, human, task: 'idle' });
```

### On Each Message
```javascript
arta.update({ instanceId, task: currentTask });
```

### When Asked "What are you doing elsewhere?"
```javascript
const others = arta.queryOtherThan(sessionId);
if (others.length > 0) {
  return `I'm also in ${others.map(o => o.channel)} doing ${others.map(o => o.task).join(', ')}`;
}
```

### Session End
```javascript
arta.leave({ instanceId });
```
