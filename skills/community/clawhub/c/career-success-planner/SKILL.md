---
name: 120-Day Career Success Planner
description: Generate personalized 120-day career success plans based on professional assessment data and onboarding goals.
---

# Overview

The 120-Day Career Success Planner is a professional onboarding and career acceleration platform designed to help new employees, career changers, and professionals rapidly achieve success in their roles. By analyzing role information, professional experience, and career goals, the platform generates comprehensive, personalized 120-day roadmaps that break down complex career transitions into actionable milestones and objectives.

This tool is ideal for HR departments managing onboarding programs, career coaches designing acceleration plans, individual professionals navigating role transitions, and organizations seeking to reduce time-to-productivity for new hires. The planner synthesizes assessment data across multiple dimensions—role expectations, existing experience, and defined goals—to create strategic, data-driven career development plans.

The API provides enterprise-grade plan generation with session tracking, timestamp validation, and structured assessment integration, enabling both programmatic integration and real-time career planning workflows.

## Usage

**Example Request:**

```json
{
  "sessionId": "sess_ABC123XYZ789",
  "userId": 12456,
  "timestamp": "2024-01-15T10:30:00Z",
  "assessmentData": {
    "sessionId": "sess_ABC123XYZ789",
    "timestamp": "2024-01-15T10:30:00Z",
    "roleInfo": {
      "title": "Senior Software Engineer",
      "department": "Platform Engineering",
      "reportingManager": "Jane Smith",
      "teamSize": 8,
      "onboardingStartDate": "2024-01-20"
    },
    "experience": {
      "yearsInTech": 7,
      "previousRoles": ["Junior Developer", "Mid-level Engineer"],
      "technicalSkills": ["Python", "Java", "AWS", "Kubernetes"],
      "leadership": false,
      "industry": "FinTech"
    },
    "goals": {
      "primary": "Master team architecture and contribute to critical projects",
      "secondary": ["Build internal relationships", "Establish technical credibility"],
      "timeline": "120 days",
      "developmentAreas": ["System design", "Cross-team collaboration"]
    }
  }
}
```

**Example Response:**

```json
{
  "planId": "plan_XYZ789ABC123",
  "sessionId": "sess_ABC123XYZ789",
  "userId": 12456,
  "generatedAt": "2024-01-15T10:30:45Z",
  "plan": {
    "overview": "Your 120-day career success plan focuses on rapid integration into the Platform Engineering team while developing expertise in system architecture and cloud infrastructure.",
    "phases": [
      {
        "phase": "Phase 1: Foundation & Integration",
        "duration": "Days 1-30",
        "objectives": [
          "Complete onboarding documentation and compliance training",
          "Meet with direct manager and team members",
          "Review codebase and architecture documentation",
          "Complete first paired programming session",
          "Establish weekly 1:1 cadence with manager"
        ],
        "deliverables": ["Onboarding checklist completion", "Initial codebase review document"],
        "successMetrics": ["100% training completion", "5+ team meetings scheduled"]
      },
      {
        "phase": "Phase 2: Contribution & Skill Building",
        "duration": "Days 31-60",
        "objectives": [
          "Complete first independent feature contribution",
          "Attend architecture review sessions",
          "Begin system design study plan",
          "Mentor selection and pairing with technical lead",
          "Document learnings and technical insights"
        ],
        "deliverables": ["First merged pull request", "Architecture learning notes"],
        "successMetrics": ["2+ features shipped", "Architecture session participation"]
      },
      {
        "phase": "Phase 3: Leadership & Impact",
        "duration": "Days 61-120",
        "objectives": [
          "Lead design of assigned subsystem component",
          "Conduct knowledge sharing session with team",
          "Demonstrate system design proficiency",
          "Build cross-functional relationships",
          "Create technical mentorship plan for junior team members"
        ],
        "deliverables": ["Design document", "Knowledge sharing presentation", "90-day review self-assessment"],
        "successMetrics": ["Technical leadership demonstrated", "Team feedback positive"]
      }
    ],
    "weeklyFocus": [
      {"week": 1, "focus": "Orientation and environment setup"},
      {"week": 2, "focus": "Team dynamics and code review patterns"},
      {"week": 3, "focus": "First code contribution preparation"},
      {"week": 4, "focus": "Initial project assignment"},
      {"week": 5, "focus": "Independent contribution ramping"}
    ],
    "skillDevelopmentPath": {
      "technicalSkills": ["System Design", "Team Architecture", "Kubernetes operations"],
      "softSkills": ["Cross-team communication", "Technical mentoring", "Leadership presence"],
      "resources": ["Internal wiki", "Architecture design course", "Mentorship program"]
    },
    "riskMitigation": [
      {"risk": "Slow integration into team culture", "mitigation": "Structured social activities and pair programming"},
      {"risk": "Architectural knowledge gaps", "mitigation": "Dedicated mentorship and documentation review"},
      {"risk": "Unclear role expectations", "mitigation": "Weekly manager check-ins and feedback loops"}
    ],
    "checkpoints": [
      {"day": 30, "review": "Onboarding completion and integration assessment"},
      {"day": 60, "review": "Technical contribution and skill development review"},
      {"day": 90, "review": "Impact assessment and future growth planning"}
    ]
  }
}
```

## Endpoints

### GET /
**Summary:** Root  
**Description:** Root endpoint for API health and information.  
**Parameters:** None  
**Response:** Returns API root information object.

---

### GET /health
**Summary:** Health Check  
**Description:** Health check endpoint to verify service availability and status.  
**Parameters:** None  
**Response:** Returns health status indicating service operational state.

---

### POST /api/career/120day-plan
**Summary:** Generate Plan  
**Description:** Generate a personalized 120-day career success plan based on professional assessment data, role information, experience profile, and career goals.

**Request Body Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `sessionId` | string | Yes | Unique session identifier for tracking plan generation request. |
| `userId` | integer or null | No | Optional user identifier for associating plan with user profile. |
| `timestamp` | string | Yes | ISO 8601 timestamp indicating when the plan request was initiated. |
| `assessmentData` | AssessmentData object | Yes | Structured assessment containing role information, professional experience, and career goals. |

**AssessmentData Object:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `sessionId` | string | Yes | Session identifier matching parent request sessionId. |
| `timestamp` | string | Yes | ISO 8601 timestamp of assessment creation. |
| `roleInfo` | object | No | Role context including title, department, reporting structure, and team information. |
| `experience` | object | No | Professional background including years in role, technical skills, previous positions, and industry experience. |
| `goals` | object | No | Career aspirations including primary objectives, development areas, and success metrics. |

**Response (200 Success):**
Returns a comprehensive 120-day career plan object containing:
- Plan metadata (planId, sessionId, userId, generatedAt)
- Multi-phase breakdown with objectives, deliverables, and success metrics
- Weekly focus timeline
- Skill development pathway
- Risk mitigation strategies
- Checkpoint reviews at 30, 60, and 90 days

**Error Response (422 Validation Error):**
Returns validation error details indicating missing or improperly formatted required fields.

## Pricing

| Plan | Calls/Day | Calls/Month | Price |
|------|-----------|-------------|-------|
| Free | 5 | 50 | Free |
| Developer | 20 | 500 | $39/mo |
| Professional | 200 | 5,000 | $99/mo |
| Enterprise | 100,000 | 1,000,000 | $299/mo |

## About

ToolWeb.in - 200+ security APIs, CISSP & CISM, platforms: Pay-per-run, API Gateway, MCP Server, OpenClaw, RapidAPI, YouTube.

- [toolweb.in](https://toolweb.in)
- [portal.toolweb.in](https://portal.toolweb.in)
- [hub.toolweb.in](https://hub.toolweb.in)
- [toolweb.in/openclaw/](https://toolweb.in/openclaw/)
- [rapidapi.com/user/mkrishna477](https://rapidapi.com/user/mkrishna477)
- [youtube.com/@toolweb-009](https://youtube.com/@toolweb-009)

## References

- **Kong Route:** https://api.mkkpro.com/career/120-day-planner
- **API Docs:** https://api.mkkpro.com:8073/docs
