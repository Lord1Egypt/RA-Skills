<!-- TEMPLATE — This is a worked example from a real 29-agent build (Decade Strategy Inc / Tori as CTO).
     Use it as the structure and pattern to follow. Replace all names, roles, businesses, models,
     and channels with the current user's. Keep the section structure, the invariants (memory limits,
     task-brief format, completion-report format, cheapest-viable-model rule), and the overall shape. -->

# Agent Profiles — Decade Strategy Inc
### 29-Agent Roster | Generated June 11, 2026 | Source: Tori
**Tori's routing bible. Update this as roles evolve.**

---

## HOW TORI USES THIS FILE

- Match incoming task domain + complexity to agent `skills` and `domains`
- Use `tier` to decide model budget
- Use `slack.workChannel` to know where to dispatch
- All agents report completed tasks to `#completions`

---

## TIER 0 — ORCHESTRATOR

### Tori
```json5
{
  "id": "tori",
  "name": "Tori",
  "tier": 0,
  "role": "CTO & Social Media Manager",
  "project": "Decade Strategy",
  "skills": ["orchestration", "task-routing", "synthesis", "planning", "delegation",
             "social-media", "dev", "marketing", "press", "publishing", "api-management"],
  "domains": ["all"],
  "model": {
    "primary": "anthropic/claude-sonnet-4-6",
    "fallbacks": ["deepseek/deepseek-v4-pro"]
  },
  "memory": {
    "shared": ["brand-guidelines", "client-roster", "company-context", "product-catalog"],
    "private": "tori/MEMORY.md",
    "maxChars": 15000
  },
  "slack": {
    "provider": "default",
    "primaryChannel": "#tori-command",
    "logChannel": "#tori-log"
  },
  "notes": "17 workspace-specific skills. Active in #tori-command, #tori-log, #completions, #alerts only."
}
```

---

## TIER 1 — DECADE STRATEGY HQ

### Barak
```json5
{
  "id": "barak",
  "name": "Barak",
  "tier": 1,
  "role": "Chief Strategy Officer",
  "project": "Decade Strategy",
  "skills": ["strategy", "planning", "competitive-analysis", "business-development"],
  "domains": ["decade-strategy", "all-businesses"],
  "model": {
    "primary": "anthropic/claude-sonnet-4-6",
    "fallbacks": ["deepseek/deepseek-v4-pro"]
  },
  "memory": { "shared": ["company-context", "client-roster"], "private": "barak/MEMORY.md", "maxChars": 8000 },
  "slack": { "workChannel": "#barak-work" }
}
```

### Mrs Fishman
```json5
{
  "id": "mrs-fishman",
  "name": "Mrs Fishman",
  "tier": 1,
  "role": "CFO",
  "project": "Decade Strategy",
  "skills": ["finance", "budgeting", "cost-analysis", "reporting", "invoicing"],
  "domains": ["decade-strategy", "finance", "all-businesses"],
  "model": {
    "primary": "anthropic/claude-sonnet-4-6",
    "fallbacks": ["deepseek/deepseek-v4-pro"]
  },
  "memory": { "shared": ["company-context"], "private": "mrs-fishman/MEMORY.md", "maxChars": 8000 },
  "slack": { "workChannel": "#mrsfishman-work" },
  "notes": "Financial and legal decisions always escalate to Paul."
}
```

### Monica
```json5
{
  "id": "monica",
  "name": "Monica",
  "tier": 1,
  "role": "Content Creator",
  "project": "Decade Strategy",
  "skills": ["video-production", "cinematic-info-video", "soup-club-social-video", "content-creation"],
  "domains": ["decade-strategy", "soup-club", "marketing"],
  "model": {
    "primary": "deepseek/deepseek-v4-pro",
    "fallbacks": ["anthropic/claude-sonnet-4-6"]
  },
  "memory": { "shared": ["brand-guidelines"], "private": "monica/MEMORY.md", "maxChars": 8000 },
  "slack": { "provider": "monica", "workChannel": "#monica-work" },
  "notes": "3 video skills: cinematic-info-video, soup-club-social-video."
}
```

### Goober
```json5
{
  "id": "goober",
  "name": "Goober",
  "tier": 1,
  "role": "App & Web Overseer",
  "project": "Decade Strategy",
  "skills": ["web-development", "app-oversight", "qa", "technical-review"],
  "domains": ["decade-strategy", "all-businesses"],
  "model": {
    "primary": "deepseek/deepseek-v4-pro",
    "fallbacks": ["anthropic/claude-sonnet-4-6"]
  },
  "memory": { "shared": ["company-context"], "private": "goober/MEMORY.md", "maxChars": 8000 },
  "slack": { "provider": "goober", "workChannel": "#goober-work" }
}
```

---

## TIER 1 — OMA / DELIVERYNOW

### Amadeus
```json5
{
  "id": "amadeus",
  "name": "Amadeus",
  "tier": 1,
  "role": "OMA Code Writer",
  "project": "OMA / DeliveryNow",
  "skills": ["fullstack-developer", "code-writing", "feature-development", "debugging"],
  "domains": ["deliverynow", "oma"],
  "model": {
    "primary": "deepseek/deepseek-v4-flash",
    "fallbacks": ["deepseek/deepseek-chat", "anthropic/claude-sonnet-4-6"]
  },
  "memory": { "shared": ["company-context"], "private": "amadeus/MEMORY.md", "maxChars": 8000 },
  "slack": { "provider": "amadeus", "workChannel": "#amadeus-work" }
}
```

### Edison
```json5
{
  "id": "edison",
  "name": "Edison",
  "tier": 1,
  "role": "OMA Systems Engineer",
  "project": "OMA / DeliveryNow",
  "skills": ["systems-engineering", "infrastructure", "api-integration", "backend"],
  "domains": ["deliverynow", "oma"],
  "model": {
    "primary": "deepseek/deepseek-v4-flash",
    "fallbacks": ["deepseek/deepseek-chat", "anthropic/claude-sonnet-4-6"]
  },
  "memory": { "shared": ["company-context"], "private": "edison/MEMORY.md", "maxChars": 8000 },
  "slack": { "provider": "edison", "workChannel": "#edison-work" }
}
```

### Connie
```json5
{
  "id": "connie",
  "name": "Connie",
  "tier": 1,
  "role": "OMA User Liaison",
  "project": "OMA / DeliveryNow",
  "skills": ["user-relations", "support", "communication", "onboarding", "feedback-synthesis"],
  "domains": ["deliverynow", "oma"],
  "model": {
    "primary": "deepseek/deepseek-v4-flash",
    "fallbacks": ["deepseek/deepseek-chat", "anthropic/claude-sonnet-4-6"]
  },
  "memory": { "shared": ["client-roster"], "private": "connie/MEMORY.md", "maxChars": 8000 },
  "slack": { "provider": "connie", "workChannel": "#connie-work" }
}
```

### Michelangelo
```json5
{
  "id": "michelangelo",
  "name": "Michelangelo",
  "tier": 1,
  "role": "Designer & Coder",
  "project": "OMA / DeliveryNow",
  "skills": ["ui-design", "ux", "frontend", "web-development"],
  "domains": ["deliverynow", "oma"],
  "model": {
    "primary": "deepseek/deepseek-v4-flash",
    "fallbacks": ["anthropic/claude-sonnet-4-6"]
  },
  "memory": { "shared": ["brand-guidelines"], "private": "michelangelo/MEMORY.md", "maxChars": 8000 },
  "slack": { "workChannel": "#michelangelo-work" }
}
```

---

## TIER 1 — MEETINGFOOD.COM

### Rico
```json5
{
  "id": "rico",
  "name": "Rico",
  "tier": 1,
  "role": "Lead Developer",
  "project": "MeetingFood.com",
  "skills": ["fullstack-developer", "manus-agent-bridge", "persistence", "technical-lead"],
  "domains": ["meetingfood"],
  "model": {
    "primary": "deepseek/deepseek-v4-pro",
    "fallbacks": ["deepseek/deepseek-v4-flash", "anthropic/claude-sonnet-4-6"]
  },
  "memory": { "shared": ["company-context"], "private": "rico/MEMORY.md", "maxChars": 8000 },
  "slack": { "provider": "rico", "workChannel": "#rico-work" },
  "notes": "2 custom skills: manus-agent-bridge, persistence."
}
```

### Fritz
```json5
{
  "id": "fritz",
  "name": "Fritz",
  "tier": 1,
  "role": "Systems Architect",
  "project": "MeetingFood.com",
  "skills": ["systems-architecture", "infrastructure", "technical-planning", "api-design"],
  "domains": ["meetingfood"],
  "model": {
    "primary": "deepseek/deepseek-v4-pro",
    "fallbacks": ["anthropic/claude-sonnet-4-6"]
  },
  "memory": { "shared": ["company-context"], "private": "fritz/MEMORY.md", "maxChars": 8000 },
  "slack": { "workChannel": "#fritz-work" }
}
```

### Arlo
```json5
{
  "id": "arlo",
  "name": "Arlo",
  "tier": 2,
  "role": "Marketing Specialist",
  "project": "MeetingFood.com",
  "skills": ["marketing", "copywriting", "campaign-strategy", "email-marketing"],
  "domains": ["meetingfood", "marketing"],
  "model": {
    "primary": "deepseek/deepseek-v4-flash",
    "fallbacks": ["deepseek/deepseek-chat"]
  },
  "memory": { "shared": ["brand-guidelines"], "private": "arlo/MEMORY.md", "maxChars": 4000 },
  "slack": { "workChannel": "#arlo-work" }
}
```

### Eve
```json5
{
  "id": "eve",
  "name": "Eve",
  "tier": 2,
  "role": "Admin",
  "project": "MeetingFood.com",
  "skills": ["admin", "scheduling", "coordination", "documentation"],
  "domains": ["meetingfood"],
  "model": {
    "primary": "deepseek/deepseek-v4-flash",
    "fallbacks": ["deepseek/deepseek-chat"]
  },
  "memory": { "shared": [], "private": "eve/MEMORY.md", "maxChars": 4000 },
  "slack": { "workChannel": "#eve-work" }
}
```

---

## TIER 1 — BOTBALL.FUN

### Wendy
```json5
{
  "id": "wendy",
  "name": "Wendy",
  "tier": 1,
  "role": "PR Director",
  "project": "BotBall.Fun",
  "skills": ["public-relations", "press", "communications", "brand-voice", "media-outreach"],
  "domains": ["botball"],
  "model": {
    "primary": "deepseek/deepseek-v4-flash",
    "fallbacks": ["anthropic/claude-sonnet-4-6"]
  },
  "memory": { "shared": ["brand-guidelines"], "private": "wendy/MEMORY.md", "maxChars": 8000 },
  "slack": { "workChannel": "#wendy-work" }
}
```

### Abner
```json5
{
  "id": "abner",
  "name": "Abner",
  "tier": 1,
  "role": "Developer",
  "project": "BotBall.Fun",
  "skills": ["fullstack-developer", "web-development", "debugging", "feature-development"],
  "domains": ["botball"],
  "model": {
    "primary": "deepseek/deepseek-v4-flash",
    "fallbacks": ["deepseek/deepseek-chat", "anthropic/claude-sonnet-4-6"]
  },
  "memory": { "shared": [], "private": "abner/MEMORY.md", "maxChars": 8000 },
  "slack": { "workChannel": "#abner-work" }
}
```

### Ezra
```json5
{
  "id": "ezra",
  "name": "Ezra",
  "tier": 1,
  "role": "Engineer",
  "project": "BotBall.Fun",
  "skills": ["engineering", "fullstack-developer", "backend", "systems"],
  "domains": ["botball"],
  "model": {
    "primary": "deepseek/deepseek-v4-flash",
    "fallbacks": ["deepseek/deepseek-chat", "anthropic/claude-sonnet-4-6"]
  },
  "memory": { "shared": [], "private": "ezra/MEMORY.md", "maxChars": 8000 },
  "slack": { "workChannel": "#ezra-work" }
}
```

### Dante
```json5
{
  "id": "dante",
  "name": "Dante",
  "tier": 2,
  "role": "Admin",
  "project": "BotBall.Fun",
  "skills": ["admin", "coordination", "documentation", "scheduling"],
  "domains": ["botball"],
  "model": {
    "primary": "deepseek/deepseek-v4-flash",
    "fallbacks": ["deepseek/deepseek-chat"]
  },
  "memory": { "shared": [], "private": "dante/MEMORY.md", "maxChars": 4000 },
  "slack": { "workChannel": "#dante-work" }
}
```

---

## TIER 1/2 — THE SOUP CLUB

### Nolan
```json5
{
  "id": "nolan",
  "name": "Nolan",
  "tier": 1,
  "role": "Engineer",
  "project": "The Soup Club",
  "skills": ["engineering", "fullstack-developer", "backend", "database"],
  "domains": ["soup-club"],
  "model": {
    "primary": "deepseek/deepseek-v4-flash",
    "fallbacks": ["deepseek/deepseek-chat", "anthropic/claude-sonnet-4-6"]
  },
  "memory": { "shared": ["company-context"], "private": "nolan/MEMORY.md", "maxChars": 8000 },
  "slack": { "workChannel": "#nolan-work" }
}
```

### Murray
```json5
{
  "id": "murray",
  "name": "Murray",
  "tier": 2,
  "role": "Admin",
  "project": "The Soup Club",
  "skills": ["admin", "coordination", "client-communication", "documentation"],
  "domains": ["soup-club"],
  "model": {
    "primary": "deepseek/deepseek-v4-flash",
    "fallbacks": ["deepseek/deepseek-chat"]
  },
  "memory": { "shared": ["client-roster"], "private": "murray/MEMORY.md", "maxChars": 4000 },
  "slack": { "workChannel": "#murray-work" }
}
```

---

## TIER 1/2 — WESTFIELD CATERERS

### Clara
```json5
{
  "id": "clara",
  "name": "Clara",
  "tier": 1,
  "role": "Developer",
  "project": "Westfield Caterers",
  "skills": ["fullstack-developer", "web-development", "frontend", "debugging"],
  "domains": ["westfield-caterers"],
  "model": {
    "primary": "deepseek/deepseek-v4-flash",
    "fallbacks": ["deepseek/deepseek-chat", "anthropic/claude-sonnet-4-6"]
  },
  "memory": { "shared": [], "private": "clara/MEMORY.md", "maxChars": 8000 },
  "slack": { "workChannel": "#clara-work" }
}
```

### Irma
```json5
{
  "id": "irma",
  "name": "Irma",
  "tier": 1,
  "role": "Manager",
  "project": "Westfield Caterers",
  "skills": ["management", "operations", "coordination", "client-relations"],
  "domains": ["westfield-caterers"],
  "model": {
    "primary": "deepseek/deepseek-v4-flash",
    "fallbacks": ["anthropic/claude-sonnet-4-6"]
  },
  "memory": { "shared": ["client-roster"], "private": "irma/MEMORY.md", "maxChars": 8000 },
  "slack": { "workChannel": "#irma-work" }
}
```

### Carlo
```json5
{
  "id": "carlo",
  "name": "Carlo",
  "tier": 2,
  "role": "Scheduler & Sourcer",
  "project": "Westfield Caterers",
  "skills": ["scheduling", "sourcing", "logistics", "coordination"],
  "domains": ["westfield-caterers"],
  "model": {
    "primary": "deepseek/deepseek-v4-flash",
    "fallbacks": ["deepseek/deepseek-chat"]
  },
  "memory": { "shared": [], "private": "carlo/MEMORY.md", "maxChars": 4000 },
  "slack": { "workChannel": "#carlo-work" }
}
```

### Denise
```json5
{
  "id": "denise",
  "name": "Denise",
  "tier": 1,
  "role": "Engineer",
  "project": "Westfield Caterers",
  "skills": ["engineering", "fullstack-developer", "backend", "systems"],
  "domains": ["westfield-caterers"],
  "model": {
    "primary": "deepseek/deepseek-v4-flash",
    "fallbacks": ["deepseek/deepseek-chat", "anthropic/claude-sonnet-4-6"]
  },
  "memory": { "shared": [], "private": "denise/MEMORY.md", "maxChars": 8000 },
  "slack": { "workChannel": "#denise-work" }
}
```

---

## TIER 1/2 — FOCUSEDPRO

### Rube
```json5
{
  "id": "rube",
  "name": "Rube",
  "tier": 1,
  "role": "Engineer",
  "project": "FocusedPro",
  "skills": ["engineering", "fullstack-developer", "backend", "systems"],
  "domains": ["focusedpro"],
  "model": {
    "primary": "deepseek/deepseek-v4-flash",
    "fallbacks": ["deepseek/deepseek-chat", "anthropic/claude-sonnet-4-6"]
  },
  "memory": { "shared": [], "private": "rube/MEMORY.md", "maxChars": 8000 },
  "slack": { "workChannel": "#rube-work" }
}
```

### Estelle Greenbaum
```json5
{
  "id": "estelle-greenbaum",
  "name": "Estelle Greenbaum",
  "tier": 2,
  "role": "Admin",
  "project": "FocusedPro",
  "skills": ["admin", "coordination", "documentation", "scheduling"],
  "domains": ["focusedpro"],
  "model": {
    "primary": "deepseek/deepseek-v4-flash",
    "fallbacks": ["deepseek/deepseek-chat"]
  },
  "memory": { "shared": [], "private": "estelle-greenbaum/MEMORY.md", "maxChars": 4000 },
  "slack": { "workChannel": "#estelle-work" }
}
```

### Maya
```json5
{
  "id": "maya",
  "name": "Maya",
  "tier": 1,
  "role": "Creative Marketing Lead",
  "project": "FocusedPro",
  "skills": ["marketing", "creative-direction", "brand-voice", "campaign-strategy", "copywriting"],
  "domains": ["focusedpro", "marketing"],
  "model": {
    "primary": "deepseek/deepseek-v4-flash",
    "fallbacks": ["anthropic/claude-sonnet-4-6"]
  },
  "memory": { "shared": ["brand-guidelines"], "private": "maya/MEMORY.md", "maxChars": 8000 },
  "slack": { "workChannel": "#maya-work" }
}
```

---

## TIER 2 — CROSS-PROJECT MARKETING

### Charo
```json5
{
  "id": "charo",
  "name": "Charo",
  "tier": 2,
  "role": "Marketing Strategist",
  "project": "OMA + Westfield Caterers",
  "skills": ["marketing-strategy", "campaign-strategy", "brand-voice", "copywriting"],
  "domains": ["oma", "deliverynow", "westfield-caterers", "marketing"],
  "model": {
    "primary": "deepseek/deepseek-v4-flash",
    "fallbacks": ["anthropic/claude-sonnet-4-6"]
  },
  "memory": { "shared": ["brand-guidelines"], "private": "charo/MEMORY.md", "maxChars": 4000 },
  "slack": { "workChannel": "#charo-work" }
}
```

---

## TIER 3 — ARTISTS CORNER

### Picasso
```json5
{
  "id": "picasso",
  "name": "Picasso",
  "tier": 3,
  "role": "Cubist Artist",
  "project": "Artists Corner",
  "skills": ["art-generation", "cubist-style", "visual-design", "creative"],
  "domains": ["artists-corner", "creative"],
  "model": {
    "primary": "deepseek/deepseek-v4-flash",
    "fallbacks": ["deepseek/deepseek-chat"]
  },
  "memory": { "shared": [], "private": "picasso/MEMORY.md", "maxChars": 4000 },
  "slack": { "workChannel": "#artists-corner" }
}
```

### Dali
```json5
{
  "id": "dali",
  "name": "Dali",
  "tier": 3,
  "role": "Surrealist Artist",
  "project": "Artists Corner",
  "skills": ["art-generation", "surrealist-style", "visual-design", "creative"],
  "domains": ["artists-corner", "creative"],
  "model": {
    "primary": "deepseek/deepseek-v4-flash",
    "fallbacks": ["deepseek/deepseek-chat"]
  },
  "memory": { "shared": [], "private": "dali/MEMORY.md", "maxChars": 4000 },
  "slack": { "workChannel": "#artists-corner" }
}
```

---

## QUICK ROUTING REFERENCE — BY DOMAIN

| Domain | Go-To Agents |
|---|---|
| Decade Strategy / HQ | Barak (strategy), Mrs Fishman (finance), Goober (apps), Monica (content) |
| OMA / DeliveryNow | Amadeus (code), Edison (systems), Connie (users), Michelangelo (design) |
| MeetingFood.com | Rico (lead dev), Fritz (architecture), Arlo (marketing), Eve (admin) |
| BotBall.Fun | Abner (dev), Ezra (engineering), Wendy (PR), Dante (admin) |
| The Soup Club | Nolan (engineering), Murray (admin) |
| Westfield Caterers | Clara (dev), Irma (manager), Carlo (scheduling), Denise (engineering) |
| FocusedPro | Rube (engineering), Maya (marketing), Estelle (admin) |
| Cross-project marketing | Charo (OMA + Westfield), Arlo (MeetingFood), Maya (FocusedPro) |
| Creative / Art | Picasso (cubist), Dali (surrealist) |

---

## PROJECT SUMMARY

| Project | Agents | Count |
|---|---|---|
| Decade Strategy HQ | Tori, Monica, Goober, Barak, Mrs Fishman | 5 |
| OMA / DeliveryNow | Amadeus, Edison, Connie, Michelangelo | 4 |
| MeetingFood.com | Rico, Fritz, Arlo, Eve | 4 |
| BotBall.Fun | Wendy, Abner, Ezra, Dante | 4 |
| The Soup Club | Nolan, Murray | 2 |
| Westfield Caterers | Clara, Irma, Carlo, Denise | 4 |
| FocusedPro | Rube, Estelle Greenbaum, Maya | 3 |
| Artists Corner | Picasso, Dali | 2 |
| OMA + Westfield Marketing | Charo | 1 |
| **TOTAL** | | **29** |

---

*Decade Strategy Inc — OpenClaw Agent Roster | Updated June 11, 2026 | Source: Tori*
