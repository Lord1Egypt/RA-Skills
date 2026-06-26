# 👤 FREELANCER PROFILE
# ─────────────────────────────────────────────────
# This is your agent's identity file. HunterAI reads this before every
# single job hunt. Be specific — vague profiles produce generic proposals.
# ─────────────────────────────────────────────────

## 🧾 IDENTITY

name: "Your Full Name"
title: "Your Upwork Headline (e.g. Full-Stack Developer | React & Node.js | 5★ JSS)"
upwork_jss: 95                    # Your Job Success Score (0–100)
member_since: "2021"
timezone: "UTC+8"
availability: "40 hrs/week"       # or "20 hrs/week", "< 10 hrs/week"
english_level: "Native"           # Native | Fluent | Conversational


## 💰 RATE & BUDGET RULES

hourly_rate: 65                   # Your standard hourly rate in USD
minimum_budget_fixed: 300         # Reject any fixed job below this (USD)
minimum_budget_hourly: 35         # Reject any hourly job below this (USD/hr)
preferred_project_size: "Medium"  # Small (<$500) | Medium ($500–$5000) | Large (>$5000)


## 🎯 CORE SKILLS (List in priority order — top skills get used in proposals first)

primary_skills:
  - "React.js"
  - "Node.js / Express"
  - "TypeScript"
  - "REST API Development"
  - "PostgreSQL / MongoDB"

secondary_skills:
  - "Next.js"
  - "AWS (S3, Lambda, EC2)"
  - "Docker / CI-CD"
  - "Stripe Payment Integration"
  - "OpenAI API / LLM Integration"

emerging_skills:
  - "LangChain"
  - "Supabase"
  - "Webflow"


## 🏆 CREDIBILITY ANCHORS
# These are the real, specific results you've achieved.
# HunterAI will inject these into proposals to prove competence.
# Add numbers. Be precise. These are your secret weapons.

credibility_anchors:
  - "Built a SaaS dashboard for a fintech client that handles 50K+ daily active users"
  - "Reduced a client's API response time from 4.2s to 340ms through query optimization"
  - "Delivered 23 projects on Upwork with a 100% client satisfaction record"
  - "Integrated Stripe + subscription billing for a B2B tool now generating $12K MRR"
  - "Rebuilt a legacy PHP app in React/Node — client reported 60% faster onboarding"

# Add your own below:
  # - ""


## 📁 NICHE PREFERENCES (Jobs in these areas get a +15 score bonus)

preferred_niches:
  - "SaaS MVP Development"
  - "API Integration & Automation"
  - "Dashboard & Admin Panel Development"
  - "AI/LLM Feature Integration"
  - "E-commerce Backend Development"


## 🚫 BLACKLIST RULES
# HunterAI will auto-reject ANY job matching these criteria.
# This is your pre-flight firewall — no exceptions.

blacklist:
  payment_unverified: true          # true = reject all unverified payment accounts
  minimum_client_rating: 4.0        # Reject clients with rating below this
  minimum_client_reviews: 1         # Reject clients with zero reviews (set 0 to disable)

  # Jobs containing ANY of these keywords in title or description are auto-rejected
  blacklisted_keywords:
    - "data entry"
    - "copy paste"
    - "logo design"
    - "Wordpress theme install"
    - "per hour is negotiable"
    - "small budget"
    - "quick and easy"
    - "will pay after"
    - "test task first"
    - "unpaid trial"
    - "long term but starting small"   # Classic scope creep signal

  # Reject clients from these countries (leave empty [] to disable)
  blacklisted_client_countries: []

  # Reject jobs with MORE than this many proposals already (high competition filter)
  max_competing_proposals: 50


## 🧬 TONE & VOICE PROFILE
# HunterAI uses this to calibrate your proposal writing style.

tone: "Confident and direct, but not arrogant. Results-first. No fluff."
avoid_phrases:
  - "I am a passionate developer"
  - "I would love to work with you"
  - "Please give me a chance"
  - "I am hardworking and dedicated"
  - "Trust me"
  - "Best regards"

preferred_phrases:
  - Lead with their problem, not my resume
  - Use "you/your" more than "I/my"
  - Always mention a specific number or metric
  - End with an open question, never a statement


## 📝 SIGNATURE BLOCK
# Used at the end of select proposals (optional — agent decides when to include)

signature: |
  — [Your Name]
  ⭐ [JSS Score]% JSS | [X]+ Projects | [Your Timezone]


## 🔄 LAST UPDATED

last_updated: "YYYY-MM-DD"
updated_by: "HunterAI / Manual"
