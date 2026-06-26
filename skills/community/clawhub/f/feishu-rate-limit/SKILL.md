---
name: feishu-rate-limit
description: "Feishu/Lark API rate limit handling strategy. Automatically activates during Feishu API calls to implement smart interval control and 429 error handling. Essential for batch operations, document writes, and bitable operations."
version: "1.0.0"
---

# Feishu Rate Limit Skill

Intelligent rate limit handling for Feishu/Lark API. Avoid 429 errors and ensure batch operations complete successfully.

## Quick Reference

| Situation | Action |
|-----------|--------|
| API call fails with 429 | Parse Retry-After, wait, retry (max 3 times) |
| Batch write operations | Split into batches of 10, 1s interval per item |
| Document API calls | Use 2-3s interval (stricter limits) |
| High call frequency | Increase interval dynamically |
| Rate limit reached | Wait 10s, then gradually reduce interval |

## Trigger Conditions

Activate this skill when:

- All Feishu API calls (`feishu_doc`, `feishu_bitable_*`, `feishu_drive`, `feishu_wiki`, etc.)
- Encountering 429 (rate limit) errors
- Batch operations on Feishu data
- Large data writes/queries to Feishu
- User mentions "Feishu API", "Lark API", "429", "rate limit", "飞书限流"

## Feishu API Limits

### Custom App Limits

| Limit Type | Quota | Description |
|-----------|-------|-------------|
| Per minute | 100 calls/min/app | App-level minute limit |
| Per day | 10,000 calls/day/app | App-level daily limit |
| Per minute (per user) | 5 calls/min/user/app | User-level limit |

### Document API Special Limits

| API Type | Special Limit |
|----------|---------------|
| Document writes | Stricter, recommend 2-3s interval |
| Bitable batch write | ≤100 per batch, ≥1s interval |
| File uploads | Large files need longer intervals |

**Official Docs**: https://open.feishu.cn/document/platform-notices/platform-updates-/custom-app-api-call-limit

## Call Strategy

### Basic Interval Rules

```
Initial interval: 1 second
Minimum interval: 1 second
Maximum interval: 10 seconds
Warning threshold: 50 calls/minute
```

### Sliding Window Strategy

```python
class FeishuRateLimiter:
    """Feishu API Rate Limiter"""
    
    def __init__(self):
        self.base_interval = 1.0      # Base interval 1s
        self.current_interval = 1.0   # Current interval
        self.max_interval = 10.0      # Max interval
        self.recent_calls = []        # Recent call records
        self.window_size = 60         # Stats window 60s
        self.max_retries = 3          # Max retries
    
    def before_call(self):
        """Wait before call"""
        time.sleep(self.current_interval)
        self.recent_calls.append(time.time())
        self._adjust_interval()
    
    def _adjust_interval(self):
        """Dynamically adjust interval based on recent call frequency"""
        now = time.time()
        # Count calls in last 60s
        recent = [t for t in self.recent_calls if now - t < self.window_size]
        self.recent_calls = recent
        call_count = len(recent)
        
        # Adjust interval based on frequency
        if call_count > 50:  # Near limit (100/min)
            self.current_interval = min(self.current_interval * 1.5, self.max_interval)
        elif call_count > 30:
            self.current_interval = min(self.current_interval * 1.2, self.max_interval)
        elif call_count < 10 and self.current_interval > self.base_interval:
            # Reduce interval when calls are infrequent
            self.current_interval = max(self.current_interval * 0.9, self.base_interval)
    
    def on_rate_limit(self, retry_after=None):
        """Called when 429 error occurs"""
        if retry_after:
            wait_time = retry_after
        else:
            wait_time = self.current_interval * 2
        
        self.current_interval = min(wait_time, self.max_interval)
        time.sleep(self.current_interval)
    
    def on_success(self):
        """Gradually restore normal interval after success"""
        if self.current_interval > self.base_interval:
            self.current_interval = max(self.current_interval * 0.8, self.base_interval)
```

### Retry Strategy

```
When 429 error occurs:
1. Parse Retry-After header (if present)
2. Wait specified time OR current_interval × 2
3. Retry (max 3 times)
4. If still fails, log error and notify user
```

## Implementation Guide

### 1. Batch Operation Processing

```markdown
❌ Wrong approach:
Write 100 records at once

✅ Correct approach:
for batch in chunks(records, 10):
    for record in batch:
        feishu_bitable_create_record(record)
        sleep(1)  # 1s per record
    sleep(5)  # Extra 5s between batches
```

### 2. Prefer Batch APIs

```markdown
Priority:
1. Batch APIs (create_records, batch_update)
2. Single API + smart interval
3. Concurrent requests (reads only, use cautiously)
```

### 3. Smart Caching Strategy

```markdown
For frequently queried data:
- User info: Cache 24 hours
- Field definitions: Cache 1 hour
- Document structure: Cache 30 minutes
- Department list: Cache 2 hours
```

## Error Handling Flow

```
┌─────────────────┐
│   API Call      │
└────────┬────────┘
         ▼
┌─────────────────┐
│   Check Response│
└────────┬────────┘
         ▼
    ┌────┴────┐
    │ 429?    │
    └────┬────┘
         │
    ┌────┴────────────────────────────┐
    │ Yes                             │ No
    ▼                                 ▼
┌─────────────────┐          ┌─────────────────┐
│ Check Retry-After│          │   Continue      │
└────────┬────────┘          └─────────────────┘
         ▼
┌─────────────────┐
│  Wait specified │
│  OR interval×2  │
└────────┬────────┘
         ▼
┌─────────────────┐
│  Retries < 3?   │
└────────┬────────┘
         │
    ┌────┴────┐
    │ Yes     │ No
    ▼         ▼
┌─────────┐  ┌─────────────────┐
│ Retry   │  │ Log error, notify│
└─────────┘  └─────────────────┘
```

## Configuration Parameters

```yaml
feishu_rate_limit:
  enabled: true
  base_interval_ms: 1000      # Base interval 1s
  max_interval_ms: 10000      # Max interval 10s
  max_retries: 3              # Max retries
  window_size_sec: 60         # Stats window 60s
  warning_threshold: 50       # Warning threshold (calls/min)
  batch_size: 10              # Batch size
  batch_delay_ms: 5000        # Delay between batches
```

## Common Scenarios

### Scenario 1: Batch Create Bitable Records

```markdown
Task: Create 200 records

Strategy:
1. Split: 10 records per batch
2. Batch interval: 5 seconds
3. Record interval: 1 second
4. Estimated time: ~40 seconds

Implementation:
batch_1: 10 records → wait 5s
batch_2: 10 records → wait 5s
...
batch_20: 10 records → Done
```

### Scenario 2: Document Batch Write

```markdown
Task: Write 50 paragraphs to document

Strategy:
1. Paragraph interval: 2-3s (Document API stricter)
2. Every 10 paragraphs: Extra 10s wait
3. Estimated time: ~3-4 minutes

Notes:
- Document API limits are stricter
- Double wait time on 429
```

### Scenario 3: Mixed Operations

```markdown
Task: Read 100 records + update 50 records

Strategy:
1. Read operations: Can be concurrent
2. Update operations: Serial + 1s interval
3. Mixed: Wait after read before update

Recommendation:
- Batch read first (cacheable)
- Split updates into batches
```

## Best Practices

| Practice | Description |
|----------|-------------|
| **Estimate call volume** | Calculate API calls before batch operations |
| **Batch execution** | Split large operations into multiple runs |
| **Off-peak calls** | Avoid peak hours (9-10am, 2-3pm) for intensive calls |
| **Monitor usage** | Check Feishu backend API usage stats periodically |
| **Graceful degradation** | Log progress on limit, continue later |
| **Log records** | Track call count and duration for optimization |
| **Archive errors** | Log 429 errors to `.learnings/ERRORS.md` |

## Troubleshooting

### Problem: Frequent 429 Errors

**Analysis**:
- Call frequency too high
- No interval control implemented
- Batch operations not split

**Solution**:
1. Increase base interval to 2 seconds
2. Reduce batch size
3. Implement sliding window monitoring

### Problem: Operation Timeout

**Analysis**:
- Wait time too long
- Too many retries

**Solution**:
1. Adjust max_interval parameter
2. Reduce single operation data volume
3. Use async processing

## Integration with Other Skills

| Skill | Integration |
|-------|-------------|
| `problem-solving` | Trigger fix workflow on errors |
| `feishu-doc` | Apply rate limit to document operations |
| `feishu-archive` | Apply rate limit to archive operations |
| `self-improving-agent` | Log rate limit events to learning journal |

## Related Resources

- 📖 [Feishu API Limits Documentation](https://open.feishu.cn/document/platform-notices/platform-updates-/custom-app-api-call-limit)
- 📖 [OpenClaw Feishu Solution](https://xx0a.com/blog/openclaw-feishu)
- 📖 [Feishu Developer Community](https://open.feishu.cn/community)
- 📖 [OpenClaw Documentation](https://docs.openclaw.ai)

---

**Version**: 1.0.0  
**License**: MIT
