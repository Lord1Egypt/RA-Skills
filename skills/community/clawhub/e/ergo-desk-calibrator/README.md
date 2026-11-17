# Ergo Desk Calibrator

**Your desk, in your numbers.** The "standard" 75 cm desk fits people
around 185 cm — everyone shorter types with shrugged shoulders, and the
laptop-on-desk is a geometry trap (screen 25 cm too low, always). The
3 PM neck ache is arithmetic, and so is the fix.

From just your height, this toolkit computes:

- **Chair seat, desk, monitor top-edge, and viewing-distance numbers**
  (anthropometric proportions: seat 0.26H, desk 0.415H, seated eye
  0.674H, standing elbow 0.63H) — sitting and standing variants.
- **Monitor checker** — any diagonal size: does the top edge land
  at/below your eye line? Exact cm of riser (or lowering, or extra
  distance) needed. Spoiler: 27"+ monitors often need LOWERING.
- **Laptop compromise protocol** — why riser + external keyboard is
  the only fix, and the $25 budget path.
- **Symptom router** — neck/shoulder/wrist/eye/back pain → ranked
  likely mechanical causes → exact fixes.
- **12-point posture self-audit** + the 20-20-20 eye schedule.

## The real-world problem
Hundreds of millions now work from home on furniture never designed for
8-hour typing. Ergonomic assessments cost $150-400; the underlying math
is five fractions of body height plus a monitor-geometry check. People
buy $600 chairs and still hurt because the DESK height — the one number
that matters — was never measured against their body.

## Quick start
```bash
python3 scripts/ergo_setup.py calibrate --height 175
python3 scripts/ergo_setup.py calibrate --height 163 --standing
python3 scripts/ergo_setup.py monitor --height 175 --size 27
python3 scripts/ergo_setup.py symptom --pain wrist
python3 scripts/ergo_setup.py checklist
```

Pure Python stdlib. Offline. No camera, no accounts — a tape measure
and your height.

Not medical advice; persistent/radiating symptoms deserve a clinician.

## License
MIT © Denis Voronin
