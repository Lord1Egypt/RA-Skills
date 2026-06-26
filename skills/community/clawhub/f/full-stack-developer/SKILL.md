---
name: Full Stack Developer Roadmap
description: Generate personalized full stack development career roadmaps based on developer experience, skills, and goals.
---

# Overview

The Full Stack Developer Roadmap API provides a professional career development platform designed for aspiring and experienced full stack developers. This API generates personalized, data-driven roadmaps that align with individual developer experience levels, current skill sets, and career objectives.

The platform leverages assessment data to create comprehensive learning pathways that guide developers through the essential technologies, frameworks, and practices required for success in modern full stack development. Whether you're transitioning from another discipline or advancing your existing career, this API delivers structured guidance tailored to your specific context.

Ideal users include career counselors, educational institutions, corporate training programs, and individual developers seeking objective, skill-based career progression guidance. Organizations can integrate this API into learning management systems, career development platforms, and technical mentorship programs.

## Usage

### Sample Request

```json
{
  "assessmentData": {
    "experience": {
      "yearsInTech": 2,
      "previousRoles": ["Junior Developer", "QA Engineer"],
      "industryBackground": "Financial Services"
    },
    "skills": {
      "frontend": ["JavaScript", "React", "CSS"],
      "backend": ["Node.js", "Express"],
      "databases": ["MongoDB"],
      "devops": ["Docker basics"]
    },
    "goals": {
      "targetRole": "Senior Full Stack Developer",
      "timeframe": "24 months",
      "focusAreas": ["System Design", "Cloud Architecture"]
    },
    "sessionId": "sess_abc123def456",
    "timestamp": "2024-01-15T10:30:00Z"
  },
  "sessionId": "sess_abc123def456",
  "userId": 12345,
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### Sample Response

```json
{
  "roadmapId": "roadmap_xyz789",
  "userId": 12345,
  "sessionId": "sess_abc123def456",
  "generatedAt": "2024-01-15T10:30:15Z",
  "phases": [
    {
      "phase": 1,
      "title": "Foundation Strengthening",
      "duration": "3 months",
      "focus": ["Advanced JavaScript", "System Design Fundamentals", "SQL Mastery"],
      "milestones": [
        "Complete Advanced JS course",
        "Build system design project",
        "PostgreSQL certification"
      ]
    },
    {
      "phase": 2,
      "title": "Advanced Architecture",
      "duration": "6 months",
      "focus": ["Microservices", "Kubernetes", "Cloud Platforms (AWS/GCP)"],
      "milestones": [
        "Deploy containerized application",
        "Design multi-service architecture",
        "Obtain cloud certification"
      ]
    },
    {
      "phase": 3,
      "title": "Leadership & Specialization",
      "duration": "15 months",
      "focus": ["Team Leadership", "Technical Decision Making", "Emerging Technologies"],
      "milestones": [
        "Lead architecture decision",
        "Mentor junior developers",
        "Contribute to open source leadership"
      ]
    }
  ],
  "recommendedTechnologies": [
    "TypeScript",
    "PostgreSQL",
    "Kubernetes",
    "AWS",
    "GraphQL",
    "Redis"
  ],
  "estimatedCompletionDate": "2026-01-15",
  "successMetrics": [
    "Complete all phase milestones",
    "Demonstrate system design skills",
    "Lead at least one major project",
    "Achieve cloud certification"
  ]
}
```

## Endpoints

### GET /health

**Description:** Health check endpoint to verify API availability and status.

**Parameters:** None

**Response:**
- Status: 200 OK
- Body: JSON object confirming service health status

---

### POST /api/fullstack/roadmap

**Description:** Generate a personalized full stack developer roadmap based on assessment data, experience level, skills, and career goals.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| assessmentData | object | Yes | Assessment data object containing developer profile information |
| assessmentData.experience | object | No | Developer's work history and background (years in tech, previous roles, industry) |
| assessmentData.skills | object | No | Current technical skills across frontend, backend, databases, and DevOps |
| assessmentData.goals | object | No | Career objectives and target roles |
| assessmentData.sessionId | string | Yes | Unique session identifier for this assessment |
| assessmentData.timestamp | string | Yes | ISO 8601 timestamp of assessment creation |
| sessionId | string | Yes | Top-level session identifier matching assessment session |
| userId | integer | No | Optional user identifier for authenticated requests |
| timestamp | string | Yes | ISO 8601 timestamp of the roadmap request |

**Response Shape:**
```json
{
  "roadmapId": "string",
  "userId": "integer or null",
  "sessionId": "string",
  "generatedAt": "string (ISO 8601)",
  "phases": [
    {
      "phase": "integer",
      "title": "string",
      "duration": "string",
      "focus": ["string"],
      "milestones": ["string"]
    }
  ],
  "recommendedTechnologies": ["string"],
  "estimatedCompletionDate": "string",
  "successMetrics": ["string"]
}
```

---

### OPTIONS /api/fullstack/roadmap

**Description:** Handle CORS preflight requests for the roadmap endpoint.

**Parameters:** None

**Response:**
- Status: 200 OK
- CORS headers configured

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

- Kong Route: https://api.mkkpro.com/career/full-stack-developer
- API Docs: https://api.mkkpro.com:8049/docs
