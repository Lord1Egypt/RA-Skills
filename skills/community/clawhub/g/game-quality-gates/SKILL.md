---
name: game-quality-gates
description: Game development quality gates and mandatory checks. Activate when building, reviewing, debugging, or deploying any game project (H5/Canvas/WebGL/Phaser/Three.js/2D/3D). Covers state cleanup, lifecycle management, input handling, audio, persistence, networking, anti-cheat, and performance. Use as pre-deploy checklist or when diagnosing game-specific bugs (state leaks, phantom timers, buff conflicts, memory growth, touch issues).
---

# Game Quality Gates

Mandatory quality standards for all game projects. Based on 70+ real bugs and industry best practices.

## Core Principle

> Bugs come from **cross-state interactions**, not individual features.
> Each feature works alone; they break in combination.

## 12 Universal Rules (all games)

### 1. Single Cleanup Entry Point 🔄
All exit paths (death/level-complete/quit/pause/scene-switch) call ONE cleanup method with options.

```js
cleanupGameState(opts) {
  // Fixed order: sub-objects → buffs+timers → UI → projectiles → (optional) enemies/controls/events
}
// Every exit: resetBall(), levelComplete(), gameOver(), onShutdown() → calls this
```

**New feature = add one line here. Never scatter cleanup across exits.**

### 2. Respect Active Buffs ⚡
Any code modifying attributes (speed/attack/size/defense) must check for active temporary effects first.

```js
// ❌ speed = Math.max(speed, BASE_SPEED);  // ignores slow buff
// ✅ speed = Math.max(speed, this._currentBaseSpeed);  // buff-aware baseline
```

### 3. Cache Before Destroy 📦
Extract all needed data before `destroy()`/`dispose()`/`remove()`.

```js
const { x, y } = obj; const color = obj.getData('color');
obj.destroy();
spawnParticles(x, y, color);
```

### 4. Timers Follow Lifecycle ⏰
Track all `setTimeout`/`setInterval`/`delayedCall`/`rAF`. Cancel in cleanup.

```js
this.activeTimers.push(this.time.delayedCall(10000, cb));
// In cleanup: this.activeTimers.forEach(t => t.remove(false));
```

### 5. Frame-Rate Independent Logic 🖥️
Multiply all time-dependent logic by delta. Never assume 60fps.

```js
// ✅ player.x += speed * (delta / 1000);
```
- Phaser `update(time, delta)`: delta in ms, divide by 1000
- Three.js `clock.getDelta()`: returns seconds
- Physics: prefer fixed timestep (accumulate delta, step every 16.67ms)

### 6. Scene Transition = Full Cleanup 🚪
On scene/level switch, clean: event listeners, timers, rAF, audio nodes, object pools, WebGL resources (geometry/material/texture dispose), global state, pending fetch/XHR.

Verify: Chrome DevTools → Memory → heap snapshots before/after transition.

### 7. Audio Lifecycle 🔊
- iOS: AudioContext must `resume()` inside a user interaction event
- `visibilitychange` → pause all audio when hidden, resume when visible
- WeChat WebView: `WeixinJSBridge.invoke('getNetworkType')` before autoplay
- Pool short sound effects; manage background music separately

### 8. Input Safety 👆
- Purchase/consume actions: mutex lock + visual disable
- Attack/fire: cooldown timer
- State toggles (pause/resume): state machine guard
- See **Phaser reference** for multi-touch pointer ID tracking

### 9. Save State Persistence 💾
- Include `version` field for migration when game updates
- Only persist meaningful state (not particles/temp animations)
- Auto-save on: level end, manual save, `visibilitychange` (hidden)
- localStorage limit 5MB; use IndexedDB for larger saves
- WeChat: use `wx.setStorage` (not localStorage)

### 10. Network Fault Tolerance 🌐
All network calls (leaderboard/share/ads/sync): 5s timeout + local cache fallback + no blocking game flow on failure.

### 11. Asset Loading Strategy 📦
Three tiers: critical (startup, <2s) → level assets (loading screen) → deferred (background lazy load).
Fatal error only for critical failures; degrade gracefully for non-critical.

Compression: GLB+Draco, WebP images, MP3+OGG dual audio, sprite atlases.

### 12. Anti-Cheat Baseline 🛡️
Client is untrusted. Server validates:
- One-time raid tokens (bind user+timestamp, single use)
- Play duration sanity check (can't finish 30 levels in 3 seconds)
- Score range validation
- See `references/anti-cheat.md` for implementation patterns

---

## Engine-Specific Rules

For Phaser-specific rules (pointer ID tracking, physics group cleanup, OVERLAP_BIAS, time vs physics pause):
→ Read `references/phaser.md`

For Three.js-specific rules (dispose trio, GLB compression pipeline, animation state machine, prune pitfalls):
→ Read `references/threejs.md`

---

## Pre-Deploy Checklist

Run this checklist before every deployment:

### 🔴 Universal (all games)
- [ ] New objects cleaned in `cleanupGameState()`?
- [ ] New timers cancelled in cleanup?
- [ ] Attribute changes respect active buffs?
- [ ] Data cached before destroy?
- [ ] Movement/animation uses delta time?
- [ ] No memory leaks across scene transitions? (DevTools verify)
- [ ] Audio pauses on background/lock?
- [ ] Purchase/consume has duplicate-click prevention?
- [ ] Save has version number + migration?
- [ ] Network calls have timeout + fallback?
- [ ] Asset load failure has graceful degradation?
- [ ] Critical operations (spend/settle) server-validated?

### 🟡 Mobile Extra
- [ ] Multi-touch: each finger tracked independently?
- [ ] iOS AudioContext resumed after first interaction?
- [ ] WeChat WebView compatible (no advanced CSS like backdrop-filter)?
- [ ] Virtual joystick/buttons don't overlap game area?
- [ ] Orientation change handled?

### 🔵 Engine-specific
→ See `references/phaser.md` or `references/threejs.md` for engine checklists.
