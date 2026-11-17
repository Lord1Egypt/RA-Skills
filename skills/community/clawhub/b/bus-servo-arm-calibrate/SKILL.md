---
name: bus-servo-arm-calibrate
description: Calibrate a multi-DOF bus-servo robotic arm (Hiwonder-style, I2C/servo channels, no position readback) when you cannot read servo angles back and must confirm by eye. Provides the channel-to-joint mapping, the lift-hold-confirm interactive tuning loop, a place-and-home placement test, per-slot parameter storage, and diagnosis of the classic "second grab" failure (open claw fingers snagging the object on lift). Use when calibrating grasp/place coordinates for a table-top arm that picks objects from slots and places them on a tray.
license: MIT
metadata:
  version: 1.0.0
  author: dicky
---

# Bus-Servo Arm Calibration (no readback)

You are calibrating a small 6-DOF table-top arm (e.g. Hiwonder ArmPi) driven by
bus servos over I2C. Each servo is a **channel** (1-6) set with a function like
`set_servo(ch, angle)` where angle is 0-240. Critical constraint: **there is no
position readback** (the serial read path is dead), so you cannot ask "where is
the arm now?" — you judge grasp success by eye.

This skill is the methodology for turning an uncalibrated arm into one that
reliably picks from N slots and places on a tray.

## 1. Map channels to joints FIRST

Before any tuning, write down the channel-to-joint map and, crucially, the
**direction** of each joint (does a higher angle value raise or lower it?).
This is the #1 source of wasted calibration time: assuming the wrong direction.

A typical 6-DOF map (verify on your hardware):

| ch | joint        | direction note                                       |
|----|--------------|-------------------------------------------------------|
| 1  | gripper      | high = open, low = close (e.g. 105 open, 50 close)   |
| 2  | (varies)     | often unused or wrist roll                           |
| 3  | wrist tilt   | higher = tilt one way                                 |
| 4  | shoulder/upper arm | **higher value = claw DOWN; lower = UP** (the trap) |
| 5  | elbow/lower arm reach | higher = extend forward; low (30) = retract |
| 6  | base rotation | sets which column/slot the arm faces                |

**The shoulder (ch4) direction is the classic trap.** People read "lower the
claw to grab" and try a small ch4 value; on these arms a *small* ch4 lifts the
claw away from the table. To descend the claw, you *increase* ch4 (toward 180);
to lift, you *decrease* it (toward 60 or lower). Get this wrong and every grasp
is "too high / jams into the table" and you will blame the wrong parameter.

Write the direction into a comment in your constants file so you never re-derive it:

```
# ch4: higher = DOWN (descend). ch4=180 near table, ch4=60 lifted safe.
```

## 2. Define a safe lift height and a partial-grip open

Calibrate two globals before touching slots:

- `CH4_LIFT` — a shoulder angle high enough to clear all objects and the tray
  rim (e.g. 60). The arm lifts to this after every grasp. Too low = claw still
  in the object's way; too high = collision with the arm's own frame.
- `CH_OPEN` — gripper open angle wide enough to release cleanly but not so wide
  it stresses the servo (e.g. 105). Use a *wider* open (e.g. 120) at release if
  the open fingers snag the object on lift (see section 5).

## 3. The lift-hold-confirm tuning loop

Calibrate one slot at a time with an interactive tool that stops at the lift so
you can look. Sequence per attempt:

1. **Open gripper**, rotate base (ch6) to the slot column, extend elbow (ch5) to
   the slot's reach, tilt wrist (ch3), then **descend shoulder (ch4)** to the
   grab height. (Descend last, so you don't crash down mid-reach.)
2. **Close gripper** (ch1 = close), then **lift to `CH4_LIFT` only** — and STOP.
3. Human confirms by eye: did the gripper actually hold the object?
   - `y` -> it's held: go to the placement test (section 4).
   - `n` -> empty: open, descend back to grab height, adjust, retry.
   - `j` -> jog mode: nudge ch6/ch5/ch4/ch3 live by 2 deg (5 if uppercase),
     then auto re-grasp with the new params. This is how you converge.
   - `r` -> re-grasp with current params. `p` -> print params. `q` -> quit.
4. **Never touch ch1 (gripper) during the lift.** The object can slip; you only
   move the shoulder. This isolates "did the grip hold" from "did lifting drop it."

Why stop at the lift: with no readback, the *only* reliable signal is a human
looking at the held object at a known safe height. Running grasp+place in one go
hides whether the failure was the grab or the place.

## 4. Place-and-home test (placement calibration)

Once a slot grasps reliably, calibrate placement separately:

1. Rotate base to the **place angle** (a fixed ch6, or per-slot `ch6p`).
2. Tilt wrist up a few degrees (ch3 + 8) so the object clears the tray rim on
   the way in.
3. Extend elbow to a **place reach** (`ch5p`), descend shoulder to a **place
   height** (`ch4p` — note: NOT the grab height; usually a bit higher so the
   object releases onto the tray, not jams through it).
4. **Open gripper** to release.
5. Lift, retract, center base, home.

Store per-slot: `ch6, ch5, ch4, ch3` (grasp pose), `ch5p` (place reach),
`ch4p` (place height), `ch_open`. A `SLOTS = {1: dict(...), 2: dict(...), ...}`
structure lets the production path look up a slot by id.

## 5. Diagnose the "second grab" (object lifted then dropped)

Symptom: the object *is* released and lands on the tray, but on the lift the
claw drags it back up and it falls — looks like a "second grab." This is **not**
the gripper closing. The real cause: after release, the **open fingers are still
encircling the object neck/mouth**, and lifting straight up (shoulder up)
mechanically snags the object with the open fingers.

Do not chase gripper-close logic — it is not closing. Fixes, in order of cost:

1. **Open wider at release** (`ch_open` 105 -> 120) so the fingers clear the
   object cap/mouth before any lift. Cheapest; one parameter.
2. **Retract horizontally before lifting**: pull the elbow back (reduce ch5 a
   little) so the claw moves *off* the object, *then* lift the shoulder. The
   fingers no longer encircle the object during the vertical lift.
3. **Tilt the wrist more** at release (ch3 + 15) so the fingers lift clear of
   the mouth.

Diagnose which with three questions: (a) Did the object land on the tray? (b)
Does the drag happen *before* returning home, right after release? (c) Where
does the object end up — on the tray, or carried home? "On the tray, dragged up
then dropped, before home" = open-finger snag -> fix 1 or 2.

## 6. Front row vs back row (reach)

If slots are in two rows (far / near the arm), the near row needs *less* elbow
extension (smaller ch5) — using the far row's larger ch5 for the near row
overextends and the claw overshoots the slot. Keep per-row ch5 bands, don't
copy far-row reach into near-row slots.

## 7. Finalize

When a slot grasps and places cleanly: write its params into the SLOTS dict
(constants file), bump `CH4_LIFT` / `CH_OPEN` only if you re-derived a global,
and re-run the full slot to confirm. Store everything in code, not in your head
— the next calibration session will not remember.
