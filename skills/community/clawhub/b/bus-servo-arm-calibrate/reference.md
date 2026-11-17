# bus-servo-arm-calibrate — Worked Example

A concrete transcript calibrating one near-row slot, showing the ch4 direction
trap and the "second grab" diagnosis. Names are illustrative.

## Setup

- 6-DOF arm, bus servos, no readback. Channels: ch1 gripper, ch3 wrist,
  ch4 shoulder (higher=DOWN), ch5 elbow reach, ch6 base.
- Two rows of slots. Near row (slots 4/5/6) needs less elbow reach than far
  row (slots 1/2/3).
- Globals: `CH_OPEN=105`, `CH_CLOSE=50`, `CH4_LIFT=60`, place base `PLACE_CH6=38`.

## Step 1 — map channels and directions

Written into the constants file so it is never re-derived:

```
# ch1 gripper: 105 open / 50 close
# ch4 shoulder: higher=DOWN (180 near table), lower=UP (60 lift)
# ch5 elbow: higher=extend, 30=retract
# ch6 base: sets slot column
```

## Step 2 — calibrate slot 5 (near, middle column)

Start from the far-row middle params and reduce ch5 for the near row.

Run the interactive lift-hold tool:

```
python3 tune_grasp.py 5
# -> grasp -> lift to CH4_LIFT=60 -> STOP -> confirm by eye
```

First attempt: claw too high, misses the bottle. Jog ch4 UP (descend) — but
remember higher ch4 = DOWN. To descend, *increase* ch4:

```
# in jog mode: R (uppercase = 5 deg) increases ch4 -> claw descends
#   ch4 158 -> 163 -> 168 ... until claw is at the bottle body
#   S (lowercase = 2 deg) decreases ch5 -> less reach for near row
#       ch5 150 -> 148 -> ... -> 145
```

Converged grasp pose for slot 5:

```
ch6=92  ch5=145  ch4=180  ch3=75
```

Confirm `y` -> the bottle is held at the lift height.

## Step 3 — place-and-home test

Place params: wrist up `ch3+8=83`, place reach `ch5p=185`, place height
`ch4p=160` (not the 180 grab height — a bit higher so the bottle releases onto
the tray, not through it).

```
python3 tune_grasp.py 5 --ch4p 160
```

## Step 4 — diagnose the "second grab"

After release the bottle lands on the tray, but the claw drags it up on lift
and it drops back. Looks like a second grab. Three diagnostic questions:

1. Did the object land on the tray? -> YES (so release worked).
2. Does the drag happen before returning home, right after release? -> YES.
3. Where does it end up? -> on the tray (carried up then dropped back).

Conclusion: NOT a gripper close. The open fingers (ch1=105) still encircle the
bottle neck; lifting the shoulder straight up snags it. Fix #1 (cheapest):
open wider at release so fingers clear the cap:

```
sed -i '64s/CH_OPEN/120/' tune_grasp.py   # release open 105 -> 120
sed -n '64p' tune_grasp.py
python3 tune_grasp.py 5 --ch4p 160
```

If 120 still snags, go to 130. If still snagging, fix #2: retract horizontally
before lifting (reduce ch5 a little, then shoulder up) so the claw moves off
the bottle first.

## Step 5 — store the slot

Once slot 5 grasps and places cleanly, write its params into the SLOTS dict:

```
5: dict(name='near-mid', ch6=92, ch5=145, ch4=180, ch3=75, ch5_place=185)
```

and the production place path uses `s.get('ch4p', s['ch4']-20)` for the place
height so per-slot overrides win over the default.
