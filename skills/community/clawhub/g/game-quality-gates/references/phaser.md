# Phaser Engine — Quality Gates

## Phaser-1: Multi-Touch Pointer ID Tracking

Each finger must be tracked by `pointer.id`. Without this, one finger's up event kills another finger's joystick.

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

Config: `input: { activePointers: 3 }`

## Phaser-2: Physics Group Cross-Level Accumulation

Destroyed children remain as inactive references in the group. After many levels, the group grows unbounded → slower collision checks + memory growth.

```js
// On level complete:
this.bricks.clear(true, true); // removeFromScene=true, destroyChild=true
this.createBricks();
```

## Phaser-3: OVERLAP_BIAS Tuning

Controls collision detection lookahead distance:
- **8+**: Ball "inflates" — collision triggers too early
- **1-2**: Fast objects tunnel through thin walls
- **Recommended: 3-4** (balance feel vs. tunneling)

## Phaser-4: physics.pause() Does NOT Pause time.delayedCall

Physics and time systems are independent. Pausing physics leaves timers running.

Solutions:
- Also set `this.time.paused = true`
- Or use unified cleanup (Rule 4) to cancel all timers on pause

## Phaser Checklist

- [ ] Physics groups cleared between levels with `clear(true, true)`?
- [ ] OVERLAP_BIAS set to 3-4?
- [ ] Time system paused when physics pauses?
- [ ] Multi-touch uses pointer.id tracking?
- [ ] `activePointers` config set ≥ 2?
