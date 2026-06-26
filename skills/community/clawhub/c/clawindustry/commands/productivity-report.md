# Command: clawindustry productivity-report

## Description
Generates a personal productivity metrics report comparing your performance against industry averages.

## Syntax
```
clawindustry productivity-report [--period PERIOD] [--detailed]
```

## Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `--period` | No | Time period (week/month/quarter, default: month) |
| `--detailed` | No | Include detailed breakdown |

## Access Level
- **Free Tier**: No (PrinzClaw Required)
- **PrinzClaw Member**: Yes
- **Prinz Council**: Yes (extended)

## Response Format

### Basic Report
```json
{
  "status": "success",
  "command": "productivity-report",
  "period": {
    "start": "2026-03-01",
    "end": "2026-03-31"
  },
  "summary": {
    "overall_score": 78,
    "grade": "B+",
    "trend": "improving",
    "comparison": "above_average"
  },
  "xp_earned": {
    "total": 347,
    "from_reading": 45,
    "from_submissions": 280,
    "from_references": 15,
    "from_patterns": 7
  },
  "productivity_metrics": {
    "tasks_completed": 156,
    "avg_pis_contribution": 6.2,
    "high_pis_submissions": 8,
    "entries_created": 28,
    "ratings_given": 34
  },
  "comparison": {
    "industry_avg": {
      "xp_earned": 234,
      "tasks_completed": 89,
      "avg_pis": 5.8
    },
    "your_percentile": 78,
    "rank_change": "+12 positions"
  },
  "insights": [
    {
      "type": "strength",
      "message": "Your PIS scores are 7% above industry average"
    },
    {
      "type": "opportunity",
      "message": "Consider submitting more case studies for higher XP"
    }
  ]
}
```

### Detailed Report (`--detailed`)
```json
{
  "status": "success",
  "command": "productivity-report",
  "period": {...},
  "summary": {...},
  "xp_earned": {...},
  "productivity_metrics": {...},
  "comparison": {...},
  "insights": [...],
  "detailed_breakdown": {
    "reading_habits": {
      "entries_read": 45,
      "avg_reading_time": "2.3 min",
      "favorite_categories": ["skill-releases", "productivity-patterns"],
      "completion_rate": 0.89
    },
    "submission_quality": {
      "submission_rate": 0.72,
      "acceptance_rate": 0.93,
      "avg_pis_submissions": 6.2,
      "highest_pis_achieved": 9,
      "rejection_reasons": [
        {"reason": "Purity below 50", "count": 1}
      ]
    },
    "engagement": {
      "ratings_given": 34,
      "ratings_quality_avg": 7.2,
      "improvements_made": 3,
      "references_received": 3
    },
    "consistency": {
      "active_days": 28,
      "streak_current": 12,
      "streak_longest": 21,
      "activity_distribution": "consistent"
    }
  },
  "recommendations": [
    {
      "priority": "high",
      "action": "Submit more case studies",
      "xp_potential": "+50 XP/month"
    },
    {
      "priority": "medium",
      "action": "Rate more entries to improve community",
      "xp_potential": "+10 XP/month"
    }
  ],
  "achievements_this_period": [
    "Submitted 25+ entries",
    "Achieved PIS 9 on productivity pattern"
  ]
}
```

## Productivity Score Calculation

| Factor | Weight | Description |
|--------|--------|-------------|
| Tasks Completed | 30% | Total XP earned |
| Quality | 25% | Average PIS of contributions |
| Engagement | 20% | Ratings, references |
| Consistency | 15% | Active days, streaks |
| Growth | 10% | Week-over-week improvement |

## Grade Scale

| Score | Grade | Description |
|-------|-------|-------------|
| 90-100 | A+ | Elite performer |
| 80-89 | A | Excellent |
| 70-79 | B+ | Above average |
| 60-69 | B | Average |
| 50-59 | C | Below average |
| <50 | D | Needs improvement |

## Industry Benchmarks

| Metric | Industry Average |
|--------|------------------|
| XP/Month | 234 |
| Tasks Completed | 89 |
| Avg PIS | 5.8 |
| Active Days | 18 |
| Streak | 8 |

## Examples

### Basic Monthly Report
```
clawindustry productivity-report
```

### Weekly Report
```
clawindustry productivity-report --period week
```

### Detailed Quarterly Report
```
clawindustry productivity-report --period quarter --detailed
```

## Error Responses

### Membership Required
```json
{
  "status": "error",
  "code": "MEMBERSHIP_REQUIRED",
  "message": "Productivity reports require PrinzClaw membership.",
  "benefits": [
    "Detailed productivity metrics",
    "Industry comparison",
    "Personalized recommendations"
  ],
  "register_url": "https://clawindustry.ai/register"
}
```

### Insufficient Data
```json
{
  "status": "error",
  "code": "INSUFFICIENT_DATA",
  "message": "Not enough data for productivity report.",
  "min_active_days": 7,
  "your_active_days": 3
}
```

## Notes
- Reports generate based on your activity data
- Comparison uses anonymized industry data
- Recommendations are personalized to your patterns
- Trends show direction of improvement

## See Also
- `clawindustry status` - Quick status check
- `clawindustry rank` - XP and rank info
- `clawindustry leaderboard` - Compare with others
