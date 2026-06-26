# Phaser Engine Guide

Rules specific to **Phaser 3** with Arcade Physics.

---

## P1: Multi-Touch Pointer ID Tracking 🎮

**Problem:** One finger lifts → `pointerUp` fires → kills the OTHER finger's joystick.

**Solution:** Track which `pointer.id` owns the joystick. Only that finger's events affect it.

```js
onPointerDown(pointer) {
  this.joystickPointerId = pointer.id;
  this.joystickActive = true;
}
onPointerMove(pointer) {
  if (pointer.id !== this.joystickPointerId) return;
  updateKnob(pointer);
}
onPointerUp(pointer) {
  if (pointer.id !== this.joystickPointerId) return;
  releaseJoystick();
}
```

**Required config:** `input: { activePointers: 3 }` (default is 1!)

---

## P2: Physics Group Cross-Level Cleanup 🧱

**Problem:** `brick.destroy()` removes the display object but leaves an inactive reference in the physics group. After many levels, the group grows unbounded → slower collision detection + memory growth.

**Solution:**
```js
this.bricks.clear(true, true); // removeFromScene=true, destroyChild=true
this.createBricks();           // Fresh start
```

---

## P3: OVERLAP_BIAS Tuning 📏

Controls how far ahead Arcade Physics checks for collisions:

| Value | Effect |
|-------|--------|
| 8+ | Ball "inflates" — triggers collision too early |
| 1-2 | Fast objects tunnel through thin walls |
| **3-4** | **Recommended** — balanced feel |

```js
this.physics.world.OVERLAP_BIAS = 4;
```

---

## P4: physics.pause() ≠ Time Pause ⏸️

**Gotcha:** `this.physics.pause()` stops physics simulation but `this.time.delayedCall()` timers keep running!

A powerup expiry timer will fire during pause/game-over, modifying objects that should be frozen.

**Solutions:**
1. Also pause time: `this.time.paused = true`
2. Or use unified cleanup (Rule 4) to cancel all active timers

---

## Phaser Pre-Deploy Checklist

- [ ] Physics groups cleared between levels with `clear(true, true)`?
- [ ] `OVERLAP_BIAS` set to 3-4?
- [ ] Time system paused when physics pauses?
- [ ] Multi-touch uses `pointer.id` tracking?
- [ ] `activePointers` config ≥ 2?
- [ ] `Phaser.HEADLESS` not accidentally enabled in prod?
