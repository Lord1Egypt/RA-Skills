# Short-Term Memory (Working Memory)

## Design
- Stores recent context, active conversation turns, current task state
- TTL-based expiry (default 1 hour)
- Priority-weighted: important items survive longer
- Max items cap prevents unbounded growth

## Redis Production Config

```python
import redis
import json

class RedisShortTerm:
    def __init__(self, agent_id: str, ttl: int = 3600):
        self.r = redis.Redis(decode_responses=True)
        self.prefix = f"agent:{agent_id}:stm"
        self.ttl = ttl

    def add(self, key: str, value: dict, priority: float = 1.0):
        entry = {"value": value, "priority": priority, "ts": time.time()}
        self.r.zadd(f"{self.prefix}:items", {json.dumps(entry): priority})
        self.r.expire(f"{self.prefix}:items", self.ttl)

    def recall(self, limit: int = 10) -> list:
        items = self.r.zrevrange(f"{self.prefix}:items", 0, limit - 1)
        return [json.loads(i) for i in items]
```

## When to Promote to Long-Term
- Item accessed 3+ times within TTL
- Item tagged as "important" by agent
- Item matches consolidation pattern
