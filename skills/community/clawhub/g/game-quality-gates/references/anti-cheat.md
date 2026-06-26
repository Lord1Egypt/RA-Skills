# Anti-Cheat Patterns for Web Games

## The Core Problem

Web game client = JavaScript in browser = fully inspectable and modifiable. **Never trust client-submitted data.**

## Pattern 1: One-Time Raid Token

```
Client                          Server
  |-- POST /api/start-game ------>|
  |<-- { raidToken: "abc123" } ---|  (bind to userId + timestamp + gameId)
  |                                |
  |  ... player plays game ...     |
  |                                |
  |-- POST /api/submit-score ---->|  { raidToken: "abc123", score: 500 }
  |                                |  Server checks:
  |                                |  1. Token exists and unused
  |                                |  2. Token age reasonable (not 3s for 30-level game)
  |                                |  3. Score within plausible range
  |                                |  4. Mark token as used
  |<-- { success: true } ---------|
```

**Key:** Start API and Submit API are linked by token. Skipping start = no valid token = rejected.

## Pattern 2: Server-Side Duration Check

```js
// Server
app.post('/api/submit-score', (req, res) => {
  const token = getToken(req.body.raidToken);
  const elapsed = Date.now() - token.startedAt;
  
  // Level 5 takes minimum 30 seconds to complete
  if (token.level >= 5 && elapsed < 30000) {
    return res.status(400).json({ error: 'suspicious' });
  }
  
  // Max reasonable score per second
  const maxScorePerSec = 50;
  if (req.body.score / (elapsed / 1000) > maxScorePerSec) {
    return res.status(400).json({ error: 'suspicious' });
  }
});
```

## Pattern 3: Operation Sequence Validation

For games with currency (coins, gems):
1. **Deduct first** (server-side) → returns receipt token
2. **Grant reward** only with valid receipt token
3. Never let client call "grant reward" without prior deduction

```
❌ Client: POST /api/grant-reward { item: "sword" }     ← attacker skips payment
✅ Client: POST /api/purchase { itemId: "sword" }        ← server deducts + grants atomically
```

## Protection Tiers

| Tier | Measures | When to use |
|------|----------|-------------|
| 🟢 Basic | Score range check + duration check | All games |
| 🟡 Medium | Raid tokens + sequence validation | Games with currency/rewards |
| 🔴 Advanced | Server simulation + behavior analysis | Competitive/monetized games |

For our project scale (small H5 games), **🟡 Medium** is the sweet spot.
