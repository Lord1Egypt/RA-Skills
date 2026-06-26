# Extended Garmin Capabilities — Frisbee Edition

This skill supports **comprehensive frisbee performance tracking, time-based queries, and FIT file analysis**. Below is a full reference of what you can ask and how data is fetched.

---

## 🎯 Time-Based Queries

Ask questions like:
- "What was my heart rate at halftime yesterday?"
- "What was my Body Battery before the game at 10am?"
- "How stressed was I between games?"

```bash
# Heart rate at specific time
python3 scripts/garmin_query.py heart_rate "3:00 PM" --date 2026-03-08

# Body Battery (e.g., pre-game check)
python3 scripts/garmin_query.py body_battery "10:00 AM" --date 2026-03-08

# Stress level between games
python3 scripts/garmin_query.py stress "14:30"

# Steps at time
python3 scripts/garmin_query.py steps "17:00"
```

**Time formats supported:** `3:00 PM` · `15:00` · `2026-03-08 15:30`

---

## 📊 Extended Metrics

### Training & Performance

```bash
# Training readiness (ready for today's game/practice?)
python3 scripts/garmin_data_extended.py training_readiness

# Training status (load, VO2 max trends)
python3 scripts/garmin_data_extended.py training_status

# Endurance score (relevant for full-day tournament stamina)
python3 scripts/garmin_data_extended.py endurance_score

# VO2 max (aerobic capacity — track improvements across season)
python3 scripts/garmin_data_extended.py max_metrics

# Fitness age
python3 scripts/garmin_data_extended.py fitness_age
```

### Body & Health

```bash
# Body composition (weight, body fat %, muscle mass, BMI)
python3 scripts/garmin_data_extended.py body_composition --date 2026-03-08

# Weight history across season
python3 scripts/garmin_data_extended.py weigh_ins --start 2026-01-01 --end 2026-03-08

# Blood oxygen (SpO2) — useful for altitude tournaments
python3 scripts/garmin_data_extended.py spo2 --date 2026-03-08

# Respiration (breathing rate — elevated after high-intensity game)
python3 scripts/garmin_data_extended.py respiration
```

### Activity & Load

```bash
# Intraday steps (total movement across tournament day)
python3 scripts/garmin_data_extended.py steps --date 2026-03-08

# Intensity minutes (vigorous/moderate — compare game vs training weeks)
python3 scripts/garmin_data_extended.py intensity_minutes

# Hydration tracking (important during tournaments)
python3 scripts/garmin_data_extended.py hydration

# Stress time-series (see stress between points/games)
python3 scripts/garmin_data_extended.py stress_detailed

# Intraday heart rate (all HR samples — full game HR curve)
python3 scripts/garmin_data_extended.py hr_intraday
```

---

## 🗺️ FIT File Analysis (Single Game/Training)

FIT files contain raw sensor data recorded by your Garmin watch during an activity. This is the richest data source for frisbee performance.

```bash
# Analyze latest activity
python3 scripts/frisbee_activity.py --latest

# Analyze specific game by ID
python3 scripts/frisbee_activity.py --activity-id 12345678

# Analyze activity on a specific date
python3 scripts/frisbee_activity.py --date 2026-03-08

# Save dashboard to file
python3 scripts/frisbee_activity.py --latest --output ~/Desktop/game.html
```

### What FIT Analysis Produces

| Metric | What it tells you |
|--------|-------------------|
| Sprint Count | How many times you accelerated above 14.4 km/h |
| Sprint Peak Speed | Your fastest burst in each sprint |
| Sprint Fatigue Index | Last-3 vs first-3 sprint speed ratio — did you slow down? |
| Top Speed | Absolute fastest speed in the session |
| High-Intensity Distance | Meters covered while sprinting |
| HR Zone Distribution | Time in Zone 1–6 — did you hit Zone 4/5? |
| **Ground Contact Time** | **Average stance time (ms) — rises as you fatigue** |
| **GCT Trend** | **2nd half vs 1st half GCT — detects late-game fatigue** |

**FIT data available per record:**
- GPS coordinates, speed (m/s), heart rate
- Stance time / Ground Contact Time (if watch + activity type supports it)
- Lap splits — per-half or per-point breakdown
- Distance, altitude

---

## 📈 Comparison & Season Analysis

```bash
# Compare training sessions over last 90 days
python3 scripts/frisbee_compare.py --mode training --days 90

# Compare tournament games
python3 scripts/frisbee_compare.py --mode tournament --days 60

# Training vs game intensity comparison
python3 scripts/frisbee_compare.py --mode cross --days 60

# Full season overview (HRV + load + speed trends)
python3 scripts/frisbee_compare.py --mode season --days 180
```

### Charts Generated in Compare Mode

| Chart | What it shows |
|-------|---------------|
| Top Speed Trend | Speed improving across sessions? |
| Avg HR per Activity | Intensity level, color-coded by zone |
| **Intensity Ceiling** | **Avg HR + Max HR per session with Zone 4/5 reference lines** |
| Morning HRV Trend | Recovery quality before each session |
| Activity Volume | Duration + distance across time |

---

## 🏆 Tournament Dashboard

```bash
python3 scripts/frisbee_tournament.py \
    --start 2026-03-08 --end 2026-03-10 \
    --name "Spring Tournament 2026" \
    --output ~/Desktop/tournament.html
```

### Charts Generated

| Chart | What it shows |
|-------|---------------|
| Body Battery Fatigue Timeline | Energy levels across tournament days |
| Per-Game HR Intensity | Avg + Max HR for each game |
| Heart Rate Recovery (HRR) | How fast HR dropped after each game (1 min / 2 min) |
| Overnight Recovery | Sleep hours + HRV per night |

---

## 🔍 Frisbee Use Cases

### Post-Game Analysis
- "How many sprints did I hit yesterday?"
- "Did my sprint speed drop in the second half?" → Sprint Fatigue Index
- "How long was I in Zone 4+ during the game?"
- "Did my ground contact time increase in the second half?" → fatigue signal

### Tournament Monitoring
- "What was my Body Battery before game 1, 2, and 3?"
- "How fast did my HR recover between games?"
- "Which game had the best/worst recovery curve?"

### Training Quality
- "Is my practice intensity matching game intensity?" → cross mode
- "Did I actually reach Zone 5 in today's training?"
- "How does my max HR compare between training and games?"

### Recovery Tracking
- "What's my training readiness today after the tournament?"
- "Did I get enough deep sleep before the final?"
- "Is my HRV trending up as I get fitter?"

### Season-Long Trends
- "Is my top speed improving across games this season?"
- "How does sleep quality compare during tournament vs training weeks?"
- "Am I accumulating too much fatigue?" → HRV + resting HR trends

---

## 🛠️ Advanced Tips

### Finding an Activity ID

The activity ID is in the Garmin Connect URL:
```
https://connect.garmin.com/modern/activity/12345678
                                        ^^^^^^^^
```

Or fetch recent activity IDs:
```bash
python3 scripts/garmin_data.py activities --days 7
```

### Activity Classification

`frisbee_compare.py` classifies activities by name keywords:

| Category | Keywords |
|----------|----------|
| Game | `game`, `match`, `tournament`, `vs`, `finals`, `semifinal`, `比赛` |
| Training | `practice`, `training`, `train`, `drill`, `scrimmage`, `练`, `训` |

Name your Garmin activities consistently to get accurate classification.

### Ground Contact Time Availability

GCT (`stance_time`) is recorded when:
- You use a running activity type on your Garmin watch
- Your watch model supports running dynamics (Forerunner 955/965, Fenix 7+, etc.)
- A foot pod or HRM-Pro is paired (on older models)

If GCT data is unavailable, the GCT chart and stat card will be hidden automatically.

---

## 📦 Dependencies

```bash
pip3 install garminconnect fitparse gpxpy
```

| Package | Purpose |
|---------|---------|
| `garminconnect` | Garmin Connect API wrapper |
| `fitparse` | Parse FIT binary files — required for sprint detection, GCT |
| `gpxpy` | Parse GPX files (GPS track format) |
