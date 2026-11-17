# Diet Plateau Decoder

**Week 3, the scale is flat — is your diet broken, or is it lying to you?**

Most 2–3 week "plateaus" are masks: fat is still leaving, but 1–2 kg of
water (sodium, new-training repair edema, menstrual phase, glycogen refill,
cortisol) is sitting on top of it. Cutting calories into a mask is the
classic self-inflicted wound — deprivation stacks on a phantom problem, and
the rebound follows.

This tool separates the three cases statistically:

| Verdict | Test that triggers it |
|---|---|
| **NOT A PLATEAU** | smoothed 14-day trend still negative; raw flatness is inside the noise band |
| **TRUE PLATEAU** | smoothed trend flat ≥14 days with no water flags to explain it |
| **LOG BROKEN** | flat trend + known weekend overshoot — the arithmetic, not the metabolism |
| **GAINING** | smoothed trend positive — surplus creep or a big flag |

```
Input:  14 daily weights + expected loss rate + context flags
Output: trend vs expected (kg/wk), noise band, trend/noise ratio,
        water budget from flags, verdict, per-verdict action plan
```

## The physics it encodes

- 7700 kcal ≈ 1 kg fat → expected rate from your deficit
- Water masks by cause and magnitude (sodium +0.3–1.2 kg, new training
  +0.5–2 kg for 2 weeks, luteal +0.5–2 kg, refeed glycogen 3:1 water…)
- Weekend arithmetic: −500×5 + 400×2 ≈ half the intended deficit, silently
- True-plateau differential in order of likelihood: intake creep → TDEE
  shrink → NEAT collapse → weekends → adaptation → recomposition → medical

## Quick start

```bash
# classic mask: new training program, scale flat 2 weeks
python3 scripts/plateau_decoder.py \
  --weights 82.1,81.8,82.4,81.6,81.9,81.4,81.7,81.5,81.6,81.3,81.4,81.2,81.3,81.1 \
  --expected-loss 0.5 --flag new-training

# lb units, suspected weekend leak
python3 scripts/plateau_decoder.py --weights "180,179.5,..." --expected-loss 1 \
  --unit lb --flag weekend-overshoot
```

## Who needs this

- Anyone mid-weight-loss-journey staring at a flat scale (i.e., most of the
  ~half of adults trying to lose weight at any time)
- Coaches triaging client stalls before touching their calories
- Post-holiday "did I ruin it?" triage (same water physics in reverse)

Not for eating-disorder contexts — deliberate coarse statistics, and
obsessive daily trend-watching is harmful there.

## What's inside

- `SKILL.md` — verdict logic, physics tables, per-verdict action plans, pitfalls
- `references/plateau-science.md` — mechanisms, magnitudes, differential
  diagnosis, measurement protocol, evidence notes
- `scripts/plateau_decoder.py` — stdlib-only CLI with JSON mode

Stdlib Python only. Not medical advice.

## License

MIT © Denis Voronin
