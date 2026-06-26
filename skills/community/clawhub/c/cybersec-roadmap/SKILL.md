---
name: Cybersecurity Career Roadmap
description: Generate personalized cybersecurity career roadmaps based on professional assessment data and individual goals.
---

# Overview

The Cybersecurity Career Roadmap API is a professional assessment and planning platform designed to help cybersecurity professionals chart their career progression with data-driven insights. By analyzing your current experience, technical skills, and professional goals, the platform generates customized career development roadmaps aligned with industry standards and market demand.

This tool is essential for cybersecurity practitioners seeking structured guidance on skill development, role transitions, and long-term career planning. It integrates assessment data including years of experience, current competencies, and career objectives to deliver actionable recommendations tailored to your professional profile.

The API is ideal for career counselors, HR professionals, security training organizations, and individual practitioners looking to optimize their cybersecurity career trajectory with confidence and clarity.

## Usage

**Example Request:**

```json
{
  "sessionId": "sess_abc123xyz789",
  "userId": 4521,
  "timestamp": "2024-01-15T10:30:00Z",
  "assessmentData": {
    "sessionId": "sess_abc123xyz789",
    "timestamp": "2024-01-15T10:30:00Z",
    "experience": {
      "yearsInCybersecurity": 3,
      "currentRole": "Security Analyst",
      "previousRoles": [
        "IT Support Technician",
        "Network Administrator"
      ]
    },
    "skills": {
      "technical": [
        "Network Security",
        "Vulnerability Assessment",
        "SIEM Tools",
        "Linux Administration"
      ],
      "certifications": [
        "CompTIA Security+",
        "Certified Ethical Hacker (CEH)"
      ]
    },
    "goals": {
      "targetRole": "Senior Security Architect",
      "timeframe": "3-5 years",
      "specialization": "Cloud Security"
    }
  }
}
```

**Example Response:**

```json
{
  "roadmapId": "rm_20240115_4521",
  "sessionId": "sess_abc123xyz789",
  "userId": 4521,
  "currentAssessment": {
    "role": "Security Analyst",
    "experienceLevel": "Mid-Level",
    "skillGapAnalysis": "Strong foundation in SIEM and vulnerability assessment; gaps in cloud security and architecture design"
  },
  "recommendedPath": {
    "phase1": {
      "duration": "6-12 months",
      "objectives": [
        "Obtain AWS Security Specialty certification",
        "Lead 2-3 cloud security projects",
        "Develop architectural thinking through design reviews"
      ]
    },
    "phase2": {
      "duration": "12-24 months",
      "objectives": [
        "Transition to Cloud Security Engineer role",
        "Obtain CISSP certification",
        "Build expertise in cloud-native security frameworks"
      ]
    },
    "phase3": {
      "duration": "24-36 months",
      "objectives": [
        "Advance to Senior Security Architect",
        "Lead enterprise security architecture initiatives",
        "Develop strategic security vision and roadmaps"
      ]
    }
  },
  "skillDevelopmentPlan": [
    "Cloud Security (AWS, Azure, GCP)",
    "Security Architecture and Design",
    "Risk Management and Compliance",
    "Leadership and Communication"
  ],
  "certificationPath": [
    "AWS Certified Security - Specialty",
    "CISSP",
    "CCSK (Cloud Security Knowledge)"
  ],
  "generatedAt": "2024-01-15T10:30:00Z"
}
```

## Endpoints

### GET /

**Description:** Root endpoint for service verification.

**Parameters:** None

**Response:** Success message (200 OK)

---

### GET /health

**Description:** Health check endpoint to verify API availability and operational status.

**Parameters:** None

**Response:** Health status (200 OK)

---

### POST /api/cybersecurity/roadmap

**Description:** Generate a personalized cybersecurity career roadmap based on assessment data including experience, skills, and professional goals.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| sessionId | string | Yes | Unique session identifier for this assessment and roadmap generation. |
| userId | integer or null | No | Unique user identifier for tracking and record management. |
| timestamp | string | Yes | ISO 8601 timestamp indicating when the assessment was completed. |
| assessmentData | object | Yes | Core assessment data object containing experience, skills, and goals. |
| assessmentData.sessionId | string | Yes | Session identifier matching the parent sessionId. |
| assessmentData.timestamp | string | Yes | ISO 8601 timestamp for assessment data creation. |
| assessmentData.experience | object | No | Professional experience details including years in cybersecurity, current role, and previous positions. |
| assessmentData.skills | object | No | Technical skills and certifications inventory. |
| assessmentData.goals | object | No | Career objectives, target roles, and specialization interests. |

**Response Shape:**

```json
{
  "roadmapId": "string",
  "sessionId": "string",
  "userId": "integer or null",
  "currentAssessment": {
    "role": "string",
    "experienceLevel": "string",
    "skillGapAnalysis": "string"
  },
  "recommendedPath": {
    "phase1": {
      "duration": "string",
      "objectives": ["string"]
    },
    "phase2": {
      "duration": "string",
      "objectives": ["string"]
    },
    "phase3": {
      "duration": "string",
      "objectives": ["string"]
    }
  },
  "skillDevelopmentPlan": ["string"],
  "certificationPath": ["string"],
  "generatedAt": "string"
}
```

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

- Kong Route: https://api.mkkpro.com/career/cybersec-roadmap
- API Docs: https://api.mkkpro.com:8075/docs
