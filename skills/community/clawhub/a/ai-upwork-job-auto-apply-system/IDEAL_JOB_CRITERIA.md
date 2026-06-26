# 🎯 IDEAL JOB CRITERIA — Targeting & Scoring Rubric
# ─────────────────────────────────────────────────────────────────────────────
# HunterAI uses this file to score every job 0–100 before bidding.
# Customize these values to match your freelancing goals.
# ─────────────────────────────────────────────────────────────────────────────

## 🔍 SEARCH TARGETING

primary_keywords:
  - "React developer"
  - "Node.js API"
  - "full stack developer"
  - "SaaS MVP"
  - "web app development"
  - "REST API"
  - "Next.js"
  - "LLM integration"
  - "OpenAI API"

secondary_keywords:
  - "TypeScript"
  - "PostgreSQL"
  - "Stripe integration"
  - "backend developer"
  - "frontend React"

job_categories:
  - "Web Development"
  - "API & Backend Development"
  - "Software Development"

excluded_categories:
  - "Data Entry"
  - "Graphic Design"
  - "Translation"
  - "SEO"


## 📊 SCORING RUBRIC (Total: 100 Points)

### Budget Match (25 pts)
budget_scoring:
  - range: "> $5,000 or > $75/hr"
    points: 25
    label: "Premium"
  - range: "$1,000–$5,000 or $50–$75/hr"
    points: 20
    label: "Strong"
  - range: "$500–$999 or $35–$50/hr"
    points: 12
    label: "Acceptable"
  - range: "Below minimum"
    points: 0
    label: "Auto-Reject"

### Skill Alignment (25 pts)
skill_scoring:
  - match: "4+ primary skills required"
    points: 25
  - match: "2–3 primary skills required"
    points: 18
  - match: "1 primary + secondary skills"
    points: 10
  - match: "Secondary skills only"
    points: 5

### Client Quality (20 pts)
client_scoring:
  - rating: "4.8–5.0"
    points: 20
  - rating: "4.5–4.79"
    points: 15
  - rating: "4.0–4.49"
    points: 8
  - rating: "< 4.0"
    points: 0
    action: "Auto-Reject"

### Competition Level (15 pts)
# Fewer competing proposals = more points
competition_scoring:
  - proposals: "0–5 (Low)"
    points: 15
  - proposals: "6–15 (Medium)"
    points: 10
  - proposals: "16–30"
    points: 5
  - proposals: "> 30 (High)"
    points: 2

### Niche Fit (15 pts)
niche_scoring:
  - fit: "Exact preferred niche match"
    points: 15
  - fit: "Adjacent to preferred niche"
    points: 8
  - fit: "General web development"
    points: 3


## 🏆 BIDDING THRESHOLD

minimum_score_to_bid: 55    # Jobs scoring below this are skipped (not blacklisted)
priority_threshold: 80      # Jobs above this get your highest-quality vault hook

## 📅 JOB AGE FILTER

max_job_age_hours: 48       # Skip jobs posted more than 48 hours ago
prefer_posted_within_hours: 12  # Bonus indicator for fresher posts


## 💡 SPECIAL SIGNALS (Qualitative flags to increase priority)

boost_signals:
  - "long term"             # +5 implicit score bonus
  - "ongoing"               # +5 implicit score bonus
  - "looking for expert"    # +3 implicit score bonus
  - "had bad experience"    # +8 (pain is fresh — high response probability)
  - "urgent"                # +5 (they want to decide fast)
  - "technical co-founder"  # +10 (highest LTV potential)

risk_signals:
  - "milestone upon completion"    # Flag but don't reject
  - "will pay bonus for quality"   # Often not paid — note in log
  - "spec work"                    # Flag as risk
