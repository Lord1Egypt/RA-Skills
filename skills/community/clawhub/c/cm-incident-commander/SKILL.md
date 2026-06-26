---
name: incident-commander
description: Guide incident response with structured communication, timeline tracking, severity assessment, stakeholder updates, and post-incident review — a virtual incident commander for on-call teams.
metadata:
  tags: ["incident-response", "on-call", "sre", "communication", "ops"]
---

# Incident Commander

Guide teams through incident response with structured communication templates, timeline tracking, severity assessment, stakeholder updates, and post-incident review facilitation. Acts as a virtual incident commander to keep response organized and effective.

## Usage

```
"We have a production incident — help me manage it"
"Draft an incident communication for stakeholders"
"Create a timeline for the current incident"
"Help me run a post-incident review"
"Assess the severity of this outage"
```

## How It Works

### 1. Incident Declaration

When an incident is reported, establish structure:

**Severity assessment:**
- **SEV-1 (Critical)**: Complete service outage, data loss, security breach
  - Response: All-hands, exec notification, 15-min status updates
- **SEV-2 (High)**: Major feature degraded, significant user impact
  - Response: On-call team + leads, 30-min updates
- **SEV-3 (Medium)**: Minor feature degraded, workaround available
  - Response: On-call team, hourly updates
- **SEV-4 (Low)**: Cosmetic issue, minimal impact
  - Response: Normal ticket workflow

**Information gathering:**
- What's broken? (symptom description)
- When did it start? (first alert or user report)
- Who's affected? (users, regions, services)
- What changed recently? (deployments, config, infrastructure)
- What's the blast radius? (single service vs cascading)

### 2. Role Assignment

Establish incident roles:

- **Incident Commander (IC)**: Coordinates response, makes decisions
- **Technical Lead**: Drives investigation and fix
- **Communications Lead**: Handles stakeholder updates
- **Scribe**: Maintains timeline and documents actions

### 3. Communication Templates

**Initial notification:**
```
🔴 INCIDENT DECLARED — SEV-[1/2/3]

Impact: [what's broken, who's affected]
Started: [timestamp]
Status: Investigating
IC: [name]

Next update: [time]
War room: [link]
```

**Status update:**
```
🔄 INCIDENT UPDATE — SEV-[X] — [duration]

Status: [Investigating / Identified / Fixing / Monitoring]
Impact: [current impact description]
Root cause: [if identified]
Actions:
- [what's being done]
- [what's next]

Next update: [time]
```

**Resolution:**
```
✅ INCIDENT RESOLVED — SEV-[X] — Total duration: [time]

Root cause: [brief description]
Fix: [what was done]
Impact: [final impact assessment]
Monitoring: [what we're watching]

Post-incident review scheduled: [date]
```

### 4. Timeline Management

Maintain a precise incident timeline:

```
## Incident Timeline — INC-2026-0430

14:23 UTC — First alert: API latency >5s (PagerDuty)
14:25 UTC — On-call acknowledged, began investigation
14:28 UTC — Identified: database connection pool exhausted
14:30 UTC — IC declared SEV-2, notified engineering leads
14:32 UTC — Root cause: migration running without connection limit
14:35 UTC — Action: killed migration, restarted connection pools
14:38 UTC — API latency returning to normal
14:45 UTC — Confirmed: all services healthy
14:50 UTC — SEV-2 resolved, total duration: 27 minutes
```

### 5. Escalation Decisions

Guide escalation based on:
- Duration exceeding SLA thresholds
- Impact expanding to new services
- Investigation stalled (>30 min without progress)
- Customer-facing impact increasing
- Data integrity concerns emerging

### 6. Post-Incident Review

Facilitate blameless post-incident review:

**Template:**
```
## Post-Incident Review — INC-2026-0430

### Summary
[1-2 sentence description of what happened]

### Timeline
[Key events with timestamps]

### Root Cause
[Technical root cause]
[Contributing factors]

### Impact
- Duration: [time]
- Users affected: [count/percentage]
- Revenue impact: [if applicable]
- SLA impact: [remaining budget]

### What Went Well
- [Fast detection, good communication, etc.]

### What Could Be Improved
- [Gaps in monitoring, slow escalation, etc.]

### Action Items
- [ ] [Specific action] — Owner: [name] — Due: [date]
- [ ] [Specific action] — Owner: [name] — Due: [date]

### Lessons Learned
[Key takeaways for the team]
```

### 7. Runbook Suggestions

Based on incident type, suggest relevant runbooks:
- Database issues → connection pool reset, failover, backup restore
- Deployment issues → rollback steps, canary analysis
- Infrastructure → scaling, failover, DNS changes
- Security → containment, communication, forensics

## Output

Provides real-time incident management guidance tailored to severity and context.
