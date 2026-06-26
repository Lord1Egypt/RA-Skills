# Anti-Cheat Patterns for Web Games

Web game clients run in the browser — fully inspectable, modifiable, and replayable. **Never trust client-submitted data.**

---

## Pattern 1: One-Time Raid Token

The most important pattern. Links the "start game" and "submit score" APIs so you can't skip payment/deduction.

```
Client                          Server
  |-- POST /api/start-game ------>|
  |<-- { raidToken: "abc123" } ---|  (bind: userId + timestamp + gameId)
  |                                |
  |  ... player plays game ...     |
  |                                |
  |-- POST /api/submit-score ---->|  { raidToken: "abc123", score: 500 }
  |                                |  Server validates:
  |                                |  1. Token exists & unused
  |                                |  2. Time elapsed is reasonable
  |                                |  3. Score within plausible range
  |                                |  4. Mark token as used
  |<-- { success: true } ---------|
```

**Key:** Without a valid raid token, the submit endpoint rejects. Attacker can't skip start-game (which does deduction) and go straight to submit-score (which grants rewards).

---

## Pattern 2: Duration Sanity Check

```js
// Server-side
app.post('/api/submit-score', (req, res) => {
  const token = getToken(req.body.raidToken);
  const elapsed = Date.now() - token.startedAt;
  
  // Can't finish level 5+ in under 30 seconds
  if (token.level >= 5 && elapsed < 30000) {
    return res.status(400).json({ error: 'suspicious' });
  }
  
  // Max reasonable score-per-second
  const maxScorePerSec = 50;
  if (req.body.score / (elapsed / 1000) > maxScorePerSec) {
    return res.status(400).json({ error: 'suspicious' });
  }
});
```

---

## Pattern 3: Operation Sequence Enforcement

For games with virtual currency (coins, gems, tickets):

```
❌ Vulnerable:
   Client: POST /api/grant-reward { item: "sword" }
   → Attacker calls this directly, skipping payment

✅ Secure:
   Client: POST /api/purchase { itemId: "sword" }
   → Server deducts currency AND grants item atomically
   → Single endpoint, no way to split the operation
```

**Rule:** Never have separate "deduct" and "grant" endpoints. Make it one atomic operation server-side.

---

## Protection Tiers

| Tier | Measures | Cost | Use when |
|------|----------|------|----------|
| 🟢 Basic | Score range + duration check | 30 min | All games |
| 🟡 Medium | + Raid tokens + sequence validation | 2-3 hours | Games with currency/rewards |
| 🔴 Advanced | + Server simulation + behavior ML | Days | Competitive/monetized games |

**For small H5 games:** 🟡 Medium is the sweet spot. Blocks casual cheaters without massive engineering investment.

---

## Common Attack Vectors

| Attack | Defense |
|--------|---------|
| `fetch('/api/submit', {score: 999999})` | Score range + duration check |
| Skip start, call submit directly | Raid token required |
| Replay old token | Token single-use + expiry |
| Modify JS to change score var | Server doesn't trust client score calculation |
| Call grant-reward without payment | Atomic purchase endpoint |
| Slow-roll (play at 0.1x speed) | Max duration cap |
