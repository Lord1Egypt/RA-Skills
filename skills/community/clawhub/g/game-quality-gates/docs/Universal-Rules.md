# The 12 Universal Rules

These rules apply to **every game project**, regardless of engine, genre, or platform.

---

## Rule 1: Single Cleanup Entry Point 🔄

**Problem:** Cleanup logic scattered across 4+ exit paths. Add a feature, forget to clean it in one path = bug.

**Solution:** One `cleanupGameState(opts)` method. All exits call it with different options.

```js
cleanupGameState(opts) {
  // Fixed order:
  // 1. Sub-objects (bullets, pets, extra balls) + their colliders
  // 2. Buff/debuff effects + associated timers
  // 3. UI components (timer bars, floating text)
  // 4. Projectiles in flight
  // 5. (optional) Enemies/bricks        → opts.clearEnemies
  // 6. (optional) UI controls (joystick) → opts.clearUI
  // 7. (optional) Event listeners        → opts.unbindEvents
}
```

**Golden rule:** New feature = add ONE line in cleanup. Never scatter.

---

## Rule 2: Respect Active Buffs ⚡

**Problem:** Code modifies speed/attack/size without checking if a temporary effect is active. Buff gets silently overwritten.

**Solution:** Always use the current baseline (which may already be modified by buffs), not the raw base value.

**Applies to:** Any game with temporary effects — powerups, debuffs, equipment, auras, potions.

---

## Rule 3: Cache Before Destroy 📦

**Problem:** `obj.destroy()` then `obj.x` — property may be nulled/garbage after destroy.

**Solution:** Save everything you need BEFORE calling destroy.

```js
const { x, y } = obj;
const color = obj.getData('color');
obj.destroy();
spawnParticles(x, y, color); // Safe: using cached values
```

---

## Rule 4: Timers Follow Lifecycle ⏰

**Problem:** `setTimeout`/`delayedCall` keeps running after game over, scene switch, or object destruction.

**Solution:** Track all timers. Cancel them in cleanup.

**Also applies to:** `requestAnimationFrame`, Web Audio scheduled nodes, CSS animation callbacks.

---

## Rule 5: Frame-Rate Independent Logic 🖥️

**Problem:** `player.x += 5` per frame. At 30fps = half speed. At 120fps = double speed.

**Solution:** `player.x += speed * (delta / 1000)` — same real-world speed regardless of frame rate.

**Engine specifics:**
| Engine | Delta source | Unit |
|--------|-------------|------|
| Phaser | `update(time, delta)` | milliseconds |
| Three.js | `clock.getDelta()` | seconds |
| Raw Canvas | `timestamp - lastTimestamp` | milliseconds |

---

## Rule 6: Scene Transition = Full Cleanup 🚪

**Problem:** Switch levels → event listeners, timers, audio, WebGL resources leak into the new scene.

**Cleanup checklist:**
- ☐ `removeEventListener` / `.off()` for all registered events
- ☐ Cancel all `setTimeout` / `setInterval` / `rAF`
- ☐ Stop audio, release AudioContext nodes
- ☐ Empty object pools
- ☐ Dispose WebGL resources (Three.js: geometry + material + texture)
- ☐ Reset globals/singletons
- ☐ Abort pending `fetch`/`XHR`

**Verify:** Chrome DevTools → Memory → Heap snapshots before/after transition.

---

## Rule 7: Audio Lifecycle 🔊

**Key constraints:**
- **iOS Safari:** AudioContext must `.resume()` inside a user gesture event
- **Background tab:** `visibilitychange` → pause all audio when `document.hidden`
- **WeChat WebView:** Must call `WeixinJSBridge.invoke('getNetworkType')` before autoplay works
- **Best practice:** Pool short SFX; manage BGM track separately

---

## Rule 8: Input Safety 👆

| Scenario | Protection |
|----------|-----------|
| Purchase/consume | Mutex lock + visual disable |
| Attack/fire | Cooldown timer |
| Pause/resume | State machine guard |
| Multi-touch | Per-finger pointer ID tracking |

**Never let a double-click trigger double-spend.**

---

## Rule 9: Save State Persistence 💾

**Must-haves:**
- `version` field in save data (for migration when game updates)
- Only persist meaningful state (not particles, temp animations)
- Auto-save triggers: level end, manual save, `visibilitychange` hidden
- localStorage cap: 5MB. Larger saves → IndexedDB
- WeChat: `wx.setStorage` (not localStorage)

---

## Rule 10: Network Fault Tolerance 🌐

**Every network call needs:**
1. Timeout (5-10 seconds)
2. Local cache fallback
3. Never block game flow on failure

Leaderboard down? Show cached scores. Share failed? Skip it. Ad didn't load? Continue game.

---

## Rule 11: Asset Loading Strategy 📦

**Three tiers:**

| Tier | What | When |
|------|------|------|
| Critical | UI sprites, core sounds | Startup (<2s) |
| Level | Tilemap, character anims | Loading screen |
| Deferred | Future levels, boss models | Background lazy load |

**On failure:** Critical → fatal error screen. Non-critical → warn + degrade gracefully.

**Compression targets:** GLB+Draco, WebP images, sprite atlases, MP3+OGG dual audio.

---

## Rule 12: Anti-Cheat Baseline 🛡️

**Client is untrusted.** Server must validate:
- Raid token exists and is unused
- Play duration is plausible
- Score is within reasonable range

See [Anti-Cheat Patterns](Anti-Cheat-Patterns) for implementation details.
