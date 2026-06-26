---
name: garmin-health-report
description: Generate comprehensive daily health reports from Garmin Connect data with professional running analysis (Heart Rate Zones, TRIMP, Jack Daniels VDOT).
version: 2.0.0
metadata:
  openclaw:
    requires:
      bins:
        - python3
      python: ">=3.8"
    install:
      - kind: pip
        packages:
          - garth>=0.4.0
    emoji: "🏃‍♂️"
    homepage: https://github.com/yourusername/garmin-health-report
---

# Garmin Health Report

Generate professional daily health reports from Garmin Connect data with advanced running analysis.

**Features:**
- **Sleep Analysis**: Duration, stages (deep/light/REM), scores, and 7-dimension quality ratings
- **Heart Rate Monitoring**: Resting HR with recovery status
- **Activity Tracking**: Steps, distance, floors, goal completion
- **Professional Running Metrics**:
  - Heart Rate Zones (Zone 1-5 distribution)
  - TRIMP (Training Impulse) load calculation
  - Jack Daniels VDOT estimation with training paces
  - Personalized recovery and training advice
- **7-Day Trend Analysis**: Activity patterns and consistency tracking
- **Personalized Recommendations**: Sleep tips, step goals, training insights

**Regional Support**: Works with both Garmin.com (international) and Garmin.cn (China region) accounts.

## Quick Start

### 1. Install Dependencies

This skill requires Python 3.8 or higher and `garth` library:

```bash
# Install garth (Garmin Connect authentication library)
pip3 install garth

# Verify installation
python3 -c "import garth; print('garth installed successfully')"
```

### 2. Authenticate with Garmin Connect

First time setup requires authentication with Garmin Connect:

```bash
# Navigate to skill directory
cd ~/.agents/skills/garmin-health-report

# Run authentication script
python3 authenticate.py
```

Follow prompts to enter your Garmin Connect username and password. Tokens will be securely stored in `~/.garmin-health-report/tokens.json`.

**For China Region Users (garmin.cn):**

Create a config file before authenticating:

```bash
mkdir -p ~/.garmin-health-report
cat > ~/.garmin-health-report/config.json << 'EOF'
{
  "is_cn": true,
  "log_level": "INFO"
}
EOF
```

Then run `python3 authenticate.py`.

### 3. Generate Health Report

Generate a report for today or any specific date:

```bash
# Today's report
python3 health_daily_report.py

# Specific date
python3 health_daily_report.py 2025-01-15

# Save to file
python3 health_daily_report.py > ~/health_report_$(date +%Y-%m-%d).txt
```

### 4. (Optional) Automate with Cron

To automatically generate daily health reports, add to your crontab:

```bash
crontab -e

# Add this line for daily report at 23:00
0 23 * * * /usr/bin/python3 /path/to/health_daily_report.py >> /path/to/health_report.log 2>&1
```

## Usage Examples

```bash
# Generate today's report
python3 health_daily_report.py

# Generate report for a specific date
python3 health_daily_report.py 2026-03-01

# Check authentication status
python3 authenticate.py

# Logout and remove saved tokens
python3 authenticate.py
# Then choose 'y' when prompted to logout
```

## Understanding the Metrics

### Heart Rate Zones

| Zone | Intensity | Purpose | % HRR |
|-------|-----------|----------|---------|
| 1 | Recovery | Warm-up, recovery | <50% |
| 2 | Aerobic Base | Build foundation | 50-60% |
| 3 | Aerobic Endurance | Improve endurance | 60-70% |
| 4 | Lactate Threshold | Raise threshold | 70-80% |
| 5 | VO2Max | Maximal intensity | >80% |

### TRIMP (Training Impulse)

A measure of training load combining duration and intensity:

- **<100**: Light load - recovery days
- **100-200**: Moderate load - daily training
- **200-300**: High load - needs recovery
- **>300**: Very high load - recommend rest

### VDOT (VDot O₂max)

Estimate of running aerobic capacity (based on Jack Daniels' Running Formula). Higher VDOT = faster race pace potential.

VDOT is used to calculate optimal training paces:
- **E (Easy)**: Recovery and base building
- **M (Marathon)**: Marathon race pace
- **T (Threshold)**: Tempo/lactate threshold
- **I (Interval)**: Speed intervals
- **R (Repetition)**: Repetitions/sprints

## Output Format

The report generates a beautifully formatted text output:

```
📅 2026-03-01 健康日报
============================================================

😴 睡眠质量
总睡眠：7.7 小时
└─ 深睡：1.4h (18%) | 浅睡：4.5h (58%) | REM：1.9h (24%)

睡眠评分：82 (良好)

💓 心率监测
静息心率：57 bpm 💙

👟 活动量
今日步数：13620 步
步数目标：10000 步
完成度：136.2%
...

💪 运动数据分析（专业版）
... (detailed HR zones, TRIMP, VDOT analysis)

💡 J.A.R.V.I.S.有话说
... (personalized insights)

📈 长期趋势（过去7天）
... (7-day pattern analysis)

============================================================
💪 今天运动量很充足！继续保持！

✨ 明天加油！💪
```

## Configuration

Edit the configuration section at the top of `health_daily_report.py`:

```python
# Health history file (for 7-day trend analysis)
HISTORY_FILE = os.path.expanduser("~/.garmin_health_report/history.json")

# User profile (optional, for more accurate HR zone calculations)
USER_RESTING_HR = None  # e.g., 53
USER_AGE = None        # e.g., 25
```

Setting `USER_RESTING_HR` and `USER_AGE` improves accuracy of:
- Heart rate zone calculations
- TRIMP (Training Impulse) estimation
- Recovery status assessment

If not set, defaults will be used (Age: 30, Resting HR: 60).

## Troubleshooting

### Error: garth not installed

```
ModuleNotFoundError: No module named 'garth'
```

**Solution:** Install garth:
```bash
pip3 install garth
```

### Error: Not authenticated

```
Error: Not authenticated.
Run 'python3 authenticate.py' first.
```

**Solution:** Run `python3 authenticate.py` to authenticate with Garmin Connect.

### China Region Issues

```bash
# Verify config
cat ~/.garmin-health-report/config.json
# Should show: {"is_cn": true, ...}

# Clear tokens and re-authenticate
rm ~/.garmin-health-report/tokens.json
python3 authenticate.py
```

## Privacy & Data

- All data is retrieved from your personal Garmin Connect account
- Tokens are stored locally in `~/.garmin-health-report/tokens.json`
- No data is sent to third-party servers beyond Garmin's API
- Health history is stored locally in `~/.garmin_health_report/history.json`
- Token files have restricted permissions (600: owner read/write only)

## Differences from Original (garmer-based Version)

This version uses `garth` directly instead of `garmer`:

✅ **Simpler dependency** - Only requires `garth` (a single library)
✅ **Same features** - All original functionality preserved:
  - Sleep analysis
  - Heart rate monitoring
  - Steps tracking
  - Activity analysis
  - Professional running metrics (HR Zones, TRIMP, VDOT)
  - 7-day trend analysis
  - Personalized recommendations

**Why the change?**
- Removes complex dependency chain (garmer → garth)
- Uses the underlying Garmin Connect library directly
- Easier to install (`pip3 install garth` vs dealing with garmer's issues)
- Better error handling and debugging

## License

MIT License - See LICENSE file for details.

## Credits

- Uses [garth](https://github.com/matin/garth) library for Garmin Connect API access
- Jack Daniels VDOT formulas based on "Daniels' Running Formula"
- TRIMP calculation using Banister's equation
