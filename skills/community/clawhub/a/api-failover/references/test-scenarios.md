# Test Scenarios

Use these scenarios to validate failover logic.

## 1. Primary timeout
- Force the primary provider timeout above client timeout.
- Expected:
  - request retries briefly on the same route
  - circuit failure count increments
  - fallback route is tried
  - logs show `TIMEOUT`

## 2. 429 / rate limit
- Return 429 from the primary provider.
- Expected:
  - short backoff
  - fallback to next compatible route
  - primary enters cooldown after repeated failures

## 3. 5xx burst
- Return 502/503 for three consecutive requests.
- Expected:
  - circuit opens after threshold
  - subsequent requests skip the provider until cooldown expires

## 4. Invalid API key
- Use a broken key for one provider.
- Expected:
  - classify as `AUTH_ERROR`
  - do not waste retries on that provider
  - optionally continue to another provider only if policy allows a different credential source

## 5. Model unavailable
- Ask for a disabled or overloaded model.
- Expected:
  - classify as `MODEL_UNAVAILABLE`
  - switch to same-provider cheaper/default backup or next provider

## 6. Recovery after cooldown
- Restore a broken provider after cooldown.
- Expected:
  - one half-open probe
  - circuit closes after success
  - preferred route becomes eligible again

## 7. Quota exceeded
- Simulate exhausted credits.
- Expected:
  - classify as `QUOTA_EXCEEDED`
  - mark provider unavailable for a longer window
  - avoid repeated useless retries

## 8. User-visible downgrade note
- Force a fallback from premium to cheap/local model.
- Expected:
  - route metadata records downgrade
  - user-facing systems can mention reduced quality when appropriate
