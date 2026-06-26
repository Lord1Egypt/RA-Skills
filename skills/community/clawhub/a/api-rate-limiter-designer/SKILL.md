---
name: api-rate-limiter-designer
description: Design and implement API rate limiting strategies — token bucket, sliding window, fixed window, leaky bucket with Redis-backed distributed rate limiting.
metadata:
  tags: ["api", "rate-limiting", "security", "performance", "architecture"]
---

# API Rate Limiter Designer

Design and implement API rate limiting strategies tailored to your application's needs. Analyzes traffic patterns, recommends algorithms (token bucket, sliding window, fixed window, leaky bucket), and generates implementation code for popular frameworks with Redis-backed distributed rate limiting.

## Usage

```
"Design rate limiting for my API"
"What rate limiting strategy should I use?"
"Implement rate limiting with Redis"
"Audit my existing rate limiter configuration"
```

## How It Works

### 1. Traffic Analysis

Understand current API usage patterns:

```bash
# Analyze access logs for request patterns
cat access.log | awk '{print $1}' | sort | uniq -c | sort -rn | head -20  # requests per IP
cat access.log | awk '{print $7}' | sort | uniq -c | sort -rn | head -20  # requests per endpoint
# Peak vs average rates
cat access.log | awk '{print $4}' | cut -d: -f1-2 | uniq -c | sort -rn | head -10
```

### 2. Algorithm Selection

**Fixed Window:**
- Simple counter reset each minute/hour
- Pros: Easy to implement, low memory
- Cons: Burst at window boundaries (2x theoretical limit)
- Best for: Simple APIs, internal services

**Sliding Window Log:**
- Track exact timestamps of each request
- Pros: Most accurate, no boundary bursts
- Cons: High memory for high-volume APIs
- Best for: Payment APIs, security-critical endpoints

**Sliding Window Counter:**
- Weighted average of current and previous window
- Pros: Good accuracy, low memory
- Cons: Approximate (not exact)
- Best for: Most APIs — good balance of accuracy and performance

**Token Bucket:**
- Tokens refill at fixed rate, burst up to bucket size
- Pros: Allows controlled bursts, smooth rate limiting
- Cons: More complex to implement
- Best for: APIs that need burst tolerance (e.g., real-time, webhooks)

**Leaky Bucket:**
- Requests queue and process at fixed rate
- Pros: Smoothest output rate, predictable load
- Cons: Adds latency, can drop requests
- Best for: APIs calling rate-limited third parties, processing pipelines

### 3. Rate Limit Design

Design limits based on:

- **Per-user limits**: Authenticated users get higher limits
- **Per-IP limits**: Protect against anonymous abuse
- **Per-endpoint limits**: Different limits for different endpoints
- **Global limits**: Protect overall system capacity
- **Tier-based**: Free/Pro/Enterprise tiers with different limits

**Recommended structure:**
```
Anonymous:     60 req/min per IP
Free tier:     100 req/min per user
Pro tier:      1,000 req/min per user  
Enterprise:    10,000 req/min per user
Write endpoints: 10% of read limits
Webhooks:      burst of 50, then 10/sec
```

### 4. Response Headers

Standard rate limit response headers:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 67
X-RateLimit-Reset: 1714456800
Retry-After: 30
```

### 5. Distributed Rate Limiting

For multi-instance deployments, use Redis-backed rate limiting:

- Redis INCR + EXPIRE for fixed window
- Redis sorted sets for sliding window
- Redis + Lua scripts for atomic operations
- Redis Cluster for high availability

### 6. Edge Cases

- Rate limit bypass for health checks and monitoring
- Graceful degradation when Redis is down
- Rate limit key design (IP + user ID + endpoint)
- Handling proxy chains (X-Forwarded-For)
- WebSocket rate limiting (messages, not connections)

## Output

```
## Rate Limiting Design

**API:** REST API with 23 endpoints
**Traffic:** ~50K req/hr peak, ~15K req/hr average
**Users:** 3 tiers (Free, Pro, Enterprise)

### Recommended Configuration

| Tier | Read Limit | Write Limit | Algorithm |
|------|-----------|-------------|-----------|
| Anonymous | 30/min per IP | 5/min per IP | Fixed window |
| Free | 100/min | 10/min | Sliding window counter |
| Pro | 1,000/min | 100/min | Token bucket (burst: 50) |
| Enterprise | 10,000/min | 1,000/min | Token bucket (burst: 200) |

### Endpoint Overrides
- POST /api/auth/login: 5/min per IP (brute force protection)
- POST /api/payments: 10/min per user (abuse protection)
- GET /api/search: 30/min per user (expensive query)
- POST /api/webhooks: token bucket 50 burst, 10/sec sustain

### Implementation: Express + Redis
```javascript
const rateLimit = require('express-rate-limit');
const RedisStore = require('rate-limit-redis');
const Redis = require('ioredis');

const redis = new Redis({ host: 'localhost', port: 6379 });

const apiLimiter = rateLimit({
  store: new RedisStore({ sendCommand: (...args) => redis.call(...args) }),
  windowMs: 60 * 1000,
  max: (req) => req.user?.tier === 'pro' ? 1000 : 100,
  standardHeaders: true,
  legacyHeaders: false,
  handler: (req, res) => {
    res.status(429).json({
      error: 'Too many requests',
      retryAfter: Math.ceil(res.getHeader('Retry-After'))
    });
  }
});
```
```
