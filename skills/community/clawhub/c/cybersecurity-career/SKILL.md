---
name: Cybersecurity Career Guidance
description: Professional career assessment and roadmap platform for cybersecurity professionals seeking personalized guidance and skill development recommendations.
---

# Overview

Cybersecurity Career Guidance is a professional career assessment and roadmap platform designed to help cybersecurity professionals evaluate their current competencies, identify skill gaps, and chart a strategic career path. The platform combines experience evaluation, skills assessment, and interest mapping to deliver personalized career recommendations and development roadmaps.

This API enables organizations and individual practitioners to conduct comprehensive career assessments tailored to the cybersecurity domain. It captures critical data points including professional experience, technical skills, career interests, and professional goals to generate actionable insights and career progression strategies.

Ideal users include career development platforms, HR departments in security-focused organizations, cybersecurity training providers, and individual professionals seeking objective career guidance within the information security field.

## Usage

### Career Assessment Example

**Sample Request:**

```json
{
  "tier": "professional",
  "sessionId": "sess_abc123xyz789",
  "userId": 42,
  "assessmentData": {
    "sessionId": "sess_abc123xyz789",
    "timestamp": "2024-01-15T14:30:00Z",
    "experience": {
      "yearsInIT": 8,
      "yearsInSecurity": 4,
      "previousRoles": ["Network Administrator", "IT Support Specialist"]
    },
    "skills": {
      "technical": ["Network Security", "Threat Detection", "Incident Response"],
      "certifications": ["CompTIA Security+", "Certified Ethical Hacker"],
      "proficiency": "intermediate"
    },
    "interests": {
      "specialization": "Threat Intelligence",
      "preferredEnvironment": "Enterprise",
      "industryFocus": ["Finance", "Healthcare"]
    },
    "goals": {
      "shortTerm": "Obtain CISSP certification",
      "longTerm": "Security Manager role",
      "timeline": "24 months"
    }
  },
  "userInfo": {
    "name": "John Smith",
    "email": "john.smith@example.com",
    "company": "SecureCorpInc"
  }
}
```

**Sample Response:**

```json
{
  "assessmentId": "assess_def456ghi012",
  "sessionId": "sess_abc123xyz789",
  "timestamp": "2024-01-15T14:30:45Z",
  "careerProfile": {
    "currentLevel": "Mid-Level Security Professional",
    "experienceScore": 78,
    "skillsGapAnalysis": {
      "strengths": ["Network Security", "Incident Response"],
      "gapsToAddress": ["Cloud Security", "DevSecOps", "Security Architecture"],
      "developmentPriority": ["CISSP Domain Knowledge", "Cloud Platforms"]
    }
  },
  "recommendedRoadmap": {
    "nextSteps": [
      "Pursue advanced networking certifications",
      "Develop cloud security expertise (AWS/Azure)",
      "Lead incident response initiatives"
    ],
    "estimatedTimeline": "18-24 months",
    "recommendedCertifications": ["CISSP", "CCSK", "AWS Security Specialty"],
    "targetRoles": ["Senior Security Engineer", "Security Architect", "Security Manager"]
  },
  "actionItems": [
    {
      "priority": "High",
      "action": "Enroll in cloud security training",
      "timeline": "Next 3 months"
    },
    {
      "priority": "High",
      "action": "Obtain hands-on experience with SIEM platforms",
      "timeline": "Next 6 months"
    },
    {
      "priority": "Medium",
      "action": "Begin CISSP exam preparation",
      "timeline": "Next 12 months"
    }
  ]
}
```

## Endpoints

### GET /health

**Summary:** Health Check

**Description:** Verifies the availability and operational status of the Career Guidance API service.

**Method:** GET

**Path:** `/health`

**Parameters:** None

**Response:**
- **Status Code:** 200
- **Content-Type:** application/json
- **Body:** Health status object confirming service availability

---

### POST /api/career/assess

**Summary:** Career Assessment

**Description:** Performs a comprehensive cybersecurity career assessment using provided professional profile data, skills inventory, career interests, and goals to generate personalized career recommendations and development roadmaps.

**Method:** POST

**Path:** `/api/career/assess`

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| tier | string | Optional | Assessment tier level; defaults to "professional". Values: "professional", "enterprise", "advanced" |
| sessionId | string | Required | Unique session identifier for tracking the assessment |
| userId | integer | Optional | Unique user identifier for linking assessment to user profile |
| userInfo | object | Optional | User metadata including name, email, company, department |
| assessmentData | object | Required | Core assessment data object containing experience, skills, interests, and goals |
| assessmentData.sessionId | string | Required | Session identifier for correlation |
| assessmentData.timestamp | string | Required | ISO 8601 formatted timestamp of assessment |
| assessmentData.experience | object | Optional | Professional experience details including tenure, previous roles, domain history |
| assessmentData.skills | object | Optional | Technical skills inventory with proficiency levels and certifications |
| assessmentData.interests | object | Optional | Career interests including specialization preferences and industry focus |
| assessmentData.goals | object | Optional | Career objectives with short-term and long-term targets |

**Response:**
- **Status Code:** 200
- **Content-Type:** application/json
- **Body:** 
  - `assessmentId` (string): Unique assessment result identifier
  - `sessionId` (string): Session identifier
  - `timestamp` (string): Assessment completion timestamp
  - `careerProfile` (object): Current career level, experience score, skills gap analysis
  - `recommendedRoadmap` (object): Next steps, timeline, certification recommendations, target roles
  - `actionItems` (array): Prioritized list of recommended actions with timelines

**Error Responses:**
- **Status Code:** 422 - Validation Error
  - Returned when required fields are missing or malformed
  - Contains detailed validation error information

---

### OPTIONS /api/career/assess

**Summary:** Options Career Assess

**Description:** Handles CORS (Cross-Origin Resource Sharing) preflight requests for the career assessment endpoint.

**Method:** OPTIONS

**Path:** `/api/career/assess`

**Parameters:** None

**Response:**
- **Status Code:** 200
- **Content-Type:** application/json
- **Body:** CORS compliance response

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

- **Kong Route:** https://api.mkkpro.com/career/cybersecurity
- **API Docs:** https://api.mkkpro.com:8046/docs
