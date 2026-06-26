# ClawSaver Integration Checklist

Print this and check off as you go.

---

## Pre-Integration

- [ ] Read `QUICKSTART.md` (5 min)
- [ ] Read `SUMMARY.md` for overview (5 min)
- [ ] Review this checklist (2 min)

**Time: 12 minutes**

---

## Setup

- [ ] Run `npm test` in clawsaver directory
  ```bash
  cd /home/lumadmin/.openclaw/workspace/skills/clawsaver
  npm test
  ```
  Expected: 10 passing tests ✅

- [ ] Run `npm run demo`
  ```bash
  npm run demo
  ```
  Expected: 5 scenarios, mostly passing ✅

- [ ] Copy `SessionDebouncer.js` to your project
- [ ] Review `example-integration.js` (reference template)

**Time: 5 minutes**

---

## Integration

- [ ] Import SessionDebouncer in your session handler
  ```javascript
  import SessionDebouncer from './SessionDebouncer.js';
  ```

- [ ] Create a Map for debouncers
  ```javascript
  const debouncers = new Map();
  ```

- [ ] Implement `getOrCreateDebouncer(sessionKey)`
  (See `example-integration.js` lines 13–26)

- [ ] Update `handleUserMessage()` to call `debouncer.enqueue()`
  (See `example-integration.js` lines 30–36)

- [ ] Implement `processModelCall()` handler
  (See `example-integration.js` lines 41–62)

- [ ] Implement `mergeMessages()` function
  (See `example-integration.js` lines 68–73)

**Time: 20 minutes**

---

## Testing (Staging)

- [ ] Deploy to staging environment
- [ ] Send 2–3 related messages from same session
- [ ] Check logs for: `"Batching: 2 messages, saved 1 call(s)"`
- [ ] Verify responses come back normally
- [ ] Test multiple sessions simultaneously
- [ ] Check memory usage (should be low, <5 MB)

**Time: 15 minutes**

---

## Monitoring (1–2 days)

- [ ] Add logging for metrics (see `example-integration.js` lines 96–112)
- [ ] Collect data: batches, messages, saved calls
- [ ] Calculate cost savings: `(savedCalls / totalMessages) * 100`

**Expected:** >15% cost reduction for typical users

- [ ] Record user feedback (latency, performance)

**Target:** No complaints or <5% "slow" reports

---

## Tuning (if needed)

- [ ] Is cost savings low (<15%)?
  - [ ] Increase `debounceMs` to 1500–2000
  - [ ] Increase `maxMessages` to 8–10
  
- [ ] Are users complaining about latency?
  - [ ] Reduce `debounceMs` to 300–500
  - [ ] OR add "Send now" button calling `forceFlush()`

- [ ] Re-measure metrics after tuning
- [ ] Verify improvements

**Time: 1–2 hours (over 1–2 days)**

---

## Production Rollout

### Phase 1: Canary (10% traffic, 1 day)
- [ ] Enable for 10% of new sessions
- [ ] Monitor error rates, latency, cost
- [ ] Confirm no regressions
- [ ] Check user feedback

### Phase 2: Expand (50% traffic, 1 day)
- [ ] Enable for 50% of new sessions
- [ ] Continue monitoring
- [ ] Gather more metrics

### Phase 3: Full (100% traffic)
- [ ] Enable for all new sessions
- [ ] Monitor continuously
- [ ] Tune if needed

**Time: 2–3 days**

---

## Documentation

- [ ] Update your runbooks with ClawSaver config
- [ ] Document tuning parameters you chose
- [ ] Record baseline metrics (cost before/after)
- [ ] Add alerting for cost anomalies

**Time: 30 minutes**

---

## Post-Launch Optimization (Optional)

- [ ] Analyze per-user message patterns
- [ ] Consider adaptive debounce based on patterns
- [ ] Add message intent classification
- [ ] Implement Redis backend for multi-server setup

**Time: 1–2 weeks (if pursuing)**

---

## Success Criteria

- [ ] Tests pass (10/10)
- [ ] Demo runs successfully
- [ ] Integration complete in 1–2 hours
- [ ] Staging shows >15% cost savings
- [ ] Users report acceptable latency
- [ ] Production rollout smooth
- [ ] Ongoing monitoring in place

---

## Quick Reference

| File | Purpose |
|------|---------|
| `SessionDebouncer.js` | Core class — copy to your project |
| `example-integration.js` | Integration template — use as reference |
| `README.md` | Full docs + tuning guide |
| `QUICKSTART.md` | 5-min setup |
| `INTEGRATION.md` | Integration details + troubleshooting |
| `test/SessionDebouncer.test.js` | Tests — run to verify |
| `demo.js` | Demo — see batching in action |

---

## Contact / Support

If you get stuck:

1. Check `INTEGRATION.md` "Troubleshooting" section
2. Review `example-integration.js` for reference
3. Run tests with `npm test` to isolate issues
4. Check `README.md` FAQ

---

## Estimated Timeline

| Phase | Duration | What |
|-------|----------|------|
| Pre-work | 12 min | Reading |
| Setup | 5 min | Tests & copy files |
| Integration | 20 min | Wiring into handler |
| Testing | 15 min | Staging verification |
| Monitoring | 1–2 days | Collect real data |
| Tuning | 1–2 hours | Optimize parameters |
| Rollout | 2–3 days | Phased production launch |
| **Total** | **~3 days** | **Full production setup** |

---

**Start with QUICKSTART.md. Good luck! 🚀**
