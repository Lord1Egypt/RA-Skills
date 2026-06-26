---
name: apple-health-csv
description: >-
  Query Apple Health data exported as CSV files from iOS apps like Simple Health Export or
  Health Auto Export. Supports 30+ health metrics including heart rate, steps, sleep analysis,
  blood oxygen, workouts, body measurements, and more. Fully local — no cloud services,
  no API keys, no third-party data sharing. Use when users ask about their health data,
  fitness trends, sleep patterns, or want a daily health summary.
---

# Apple Health CSV Skill

Query Apple Health data from CSV exports. Works with any iOS app that exports HealthKit data
as CSV (Simple Health Export, Health Auto Export, etc.).

## Setup

1. Export health data from your iPhone using an app like **Simple Health Export** (free)
2. Transfer the CSV files to your Mac (via AirDrop, iCloud, or USB)
3. Place them in the skill data directory:

```bash
# Default location (auto-detected)
~/.openclaw/workspace-butler/health-data/

# Or specify a custom path
export HEALTH_DATA_DIR="/path/to/your/csv/files"
```

## Usage

```bash
# List available health metrics
python3 scripts/health_query.py list

# Get a comprehensive daily health summary
python3 scripts/health_query.py summary

# Query a specific metric (last 7 days by default)
python3 scripts/health_query.py query HeartRate
python3 scripts/health_query.py query StepCount --days 14
python3 scripts/health_query.py query SleepAnalysis --days 7
python3 scripts/health_query.py query OxygenSaturation --days 30

# JSON output for programmatic use
python3 scripts/health_query.py query HeartRate --days 7 --json
python3 scripts/health_query.py summary --json
```

## Supported Metrics

| Category | Metrics |
|----------|---------|
| **Heart** | HeartRate, RestingHeartRate, WalkingHeartRateAverage, HeartRateVariabilitySDNN |
| **Activity** | StepCount, ActiveEnergyBurned, BasalEnergyBurned, AppleExerciseTime, AppleStandTime, FlightsClimbed |
| **Distance** | DistanceWalkingRunning, DistanceCycling, DistanceSwimming |
| **Vitals** | OxygenSaturation, RespiratoryRate, BodyTemperature |
| **Sleep** | SleepAnalysis (with stage breakdown: REM/Core/Deep/Awake) |
| **Body** | BodyMass, BodyFatPercentage, BodyMassIndex, Height, LeanBodyMass |
| **Walking** | WalkingSpeed, WalkingStepLength, WalkingAsymmetryPercentage, WalkingDoubleSupportPercentage |
| **Audio** | EnvironmentalAudioExposure, HeadphoneAudioExposure |
| **Performance** | VO2Max, SixMinuteWalkTestDistance, AppleWalkingSteadiness |
| **Other** | DietaryWater, AppleSleepingWristTemperature |

## Tips for Agents

1. Start with `summary` to get a quick overview of today's health
2. Use `--json` flag when you need structured data for analysis
3. Sleep data is grouped by night (cross-midnight sessions handled correctly)
4. Blood oxygen values are auto-converted from 0-1 decimal to percentage
5. Cumulative metrics (steps, calories, exercise time) show daily totals
6. Rate metrics (heart rate, SpO2) show daily averages with min/max range
