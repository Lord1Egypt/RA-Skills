# Smartwatch / Fitness Tracker Analysis Reference

## Supported Devices
Apple Watch, Garmin, Huawei Watch, Xiaomi Band, WHOOP, Polar, Fitbit, Samsung Galaxy Watch, COROS, Suunto, Oura Ring

## Data Input Methods
- Screenshot of watch/app summary (extract visually)
- Text paste of stats
- Export file (Apple Health, Garmin Connect, Strava)
- Verbal dictation

## Key Metrics

### Heart Rate
- **Average HR**: appropriate for session type?
- **Max HR**: vs estimated max (220 - age baseline, adjust if actual max known)
- **Zone distribution**:
  - Zone 1 (50-60% max): warm-up / recovery
  - Zone 2 (60-70%): fat-burning / aerobic base — ideal for steady-state cardio
  - Zone 3 (70-80%): aerobic — the "gray zone", avoid without purpose
  - Zone 4 (80-90%): anaerobic threshold — HIIT, heavy lifting
  - Zone 5 (90-100%): max effort — sprints, PR attempts, brief only
- **HR recovery**: speed of drop after peak (faster = better CV fitness)
- **Resting HR trend**: decreasing = improving fitness

### Training Load & Recovery
- Training load / Training Effect (Garmin, COROS, Polar)
- Body Battery / Readiness (Garmin, WHOOP, Oura) — low = reduce intensity
- HRV trend — declining over days = overtraining flag
- Sleep data — poor sleep impairs recovery directly
- VO2 Max — long-term fitness indicator

### Calories
- Active calories vs plan expectations
- Accuracy caveat: watches 15-30% off, use as trends not absolutes
- Factor into daily calorie balance

### Sport-Specific
- Running: pace, cadence, stride length, ground contact time
- Strength: active time vs rest time ratio
- Swimming: SWOLF, stroke count, pace/100m
- Cycling: power, cadence, speed

## Analysis Output Format

```
Training Session Analysis — [Date]
Session: [type]

Heart Rate: Avg XXX bpm (assessment) | Max XXX bpm (XX% of max)
Zone Distribution: [breakdown + assessment]
Recovery: HR dropped to XXX in 2 min (Good/Needs work)

Intensity: [appropriate for goal? specific feedback]
Calories: Watch XXX kcal > Estimated ~XXX kcal (adjusted)
Recovery Status: [based on HRV, sleep, resting HR]

Coach's Verdict: [2-3 sentences]
```

## Data-Driven Adjustment Rules
- HR too low in strength > lift heavier or reduce rest
- HR too high on easy days > enforce polarized training
- Resting HR up + HRV down > deload week, check sleep/stress
- Sleep <6h consistently > flag as recovery bottleneck
- Training load "overreaching" > reduce volume 20-30%
- VO2 Max improving > celebrate, note CV base building
