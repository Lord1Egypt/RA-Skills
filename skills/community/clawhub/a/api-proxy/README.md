# API Gateway

Smart proxy for external API calls with retry logic, caching, circuit breaker, and rate limiting.

## Features

- **HTTP Proxy** — Make API calls with automatic retry and timeout handling
- **Circuit Breaker** — Automatic failure detection and cooldown (opens after 5 failures)
- **Response Caching** — Cache API responses to reduce repeated calls
- **Rate Limiting** — Per-provider rate limit tracking
- **Fallback Providers** — Configure fallback providers for redundancy
- **API Key Management** — Store, list, and remove API keys with masked output
- **Request Logging** — Track request history for debugging

## Installation

```bash
# The skill is auto-loaded by OpenClaw via the skill registry.
# For standalone use:
const AG = require('./api-gateway.js');
```

## Commands

```
--call <provider> <endpoint> [body]       Make API call with retry/caching
--call --dry-run <provider> <endpoint>    Preview call without executing
--keys                                     List configured API keys (masked)
--keys add <provider> <key>               Add API key
--keys remove <provider>                  Remove API key
--cache                                    Show cache status
--cache --clear                            Clear cache
--rate <provider>                          Check rate limit status
--fallback <provider> <fallback>           Set fallback provider
--status                                   Gateway status overview
```

## API

### `makeRequest(url, method, headers, body, timeout)`
Make an HTTP request with automatic retry and timeout.

```javascript
const result = await AG.makeRequest('https://api.openai.com/v1/models', 'GET', {}, null, 30000);
```

### `maskKey(key)`
Mask a sensitive key for display (`sk-a****fgh`).

### Circuit Breaker
```javascript
AG.getCircuitState('openai');     // Current state (CLOSED/OPEN/HALF-OPEN)
AG.recordFailure('openai');       // Record a failure
AG.recordSuccess('openai');       // Record a success (resets counter)
AG.getCircuitStatus();            // All circuit states
AG.resetCircuit('openai');        // Reset circuit breaker
```

### Key Management
```javascript
AG.addKey('openai', 'sk-...');    // Add API key
AG.removeKey('openai');           // Remove API key
AG.listKeys();                    // List all keys (masked)
```

### Cache
```javascript
AG.showCache();                   // Show cached responses
AG.clearCache();                  // Clear all cached responses
```

### Fallback
```javascript
AG.setFallback('openai', 'anthropic');  // Set fallback provider
AG.listFallbacks();                     // List all fallback providers
```

### Status
```javascript
AG.showStatus();                  // Full gateway status
```

## Security

- API keys masked by default in console output
- Circuit breaker prevents rapid retry cascades
- Backoff strategy: 1s → 2s → 4s → 8s → 16s (exponential)
- Max 5 retries per request
- Cache expires after configurable TTL

## Testing

```bash
node tests/run-self-tests.js
```

### Test Coverage

| Suite | Tests | Status |
|---|---|---|
| Self-tests (isolated) | 20 | ✅ Passing |
