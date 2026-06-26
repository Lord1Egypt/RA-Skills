---
name: Cloud Risk Summary Generator
description: Generates comprehensive cloud risk summaries by analyzing provider configurations, environments, services, and security exposures.
---

# Overview

The Cloud Risk Summary Generator is a security-focused API that synthesizes cloud infrastructure risk assessments into actionable summaries. It analyzes multi-cloud deployments across AWS, Azure, GCP, and other providers to identify, categorize, and contextualize security exposures within specific environments and service architectures.

This tool is designed for cloud security engineers, compliance teams, and DevSecOps professionals who need rapid risk quantification and executive-level reporting on cloud infrastructure posture. By consolidating exposure data with environmental and service context, the API generates structured risk narratives that facilitate remediation prioritization and stakeholder communication.

The generator supports complex cloud environments with multiple services and heterogeneous exposure types, making it suitable for enterprises managing hybrid and multi-cloud infrastructures at scale.

## Usage

### Sample Request

```json
{
  "provider": "aws",
  "environment": "production",
  "services": [
    "ec2",
    "s3",
    "rds",
    "lambda"
  ],
  "exposures": [
    {
      "issue": "Publicly accessible S3 bucket",
      "impact": "Confidentiality breach affecting 10GB of customer PII"
    },
    {
      "issue": "Unencrypted RDS instance",
      "impact": "Data at rest vulnerability affecting financial records"
    },
    {
      "issue": "Overly permissive IAM policy on Lambda execution role",
      "impact": "Lateral movement risk to other AWS services"
    }
  ]
}
```

### Sample Response

```json
{
  "summary": "AWS production environment contains 3 critical security exposures across 4 services. Immediate action required on S3 public access and RDS encryption. Lambda IAM permissions require least-privilege review.",
  "risk_level": "high",
  "provider": "aws",
  "environment": "production",
  "exposure_count": 3,
  "affected_services": [
    "ec2",
    "s3",
    "rds",
    "lambda"
  ],
  "exposures_analyzed": [
    {
      "issue": "Publicly accessible S3 bucket",
      "impact": "Confidentiality breach affecting 10GB of customer PII",
      "severity": "critical"
    },
    {
      "issue": "Unencrypted RDS instance",
      "impact": "Data at rest vulnerability affecting financial records",
      "severity": "critical"
    },
    {
      "issue": "Overly permissive IAM policy on Lambda execution role",
      "impact": "Lateral movement risk to other AWS services",
      "severity": "high"
    }
  ]
}
```

## Endpoints

### POST /generate-risk-summary

Generates a comprehensive risk summary for a cloud infrastructure configuration.

**Method:** `POST`

**Path:** `/generate-risk-summary`

**Description:** Analyzes cloud provider configuration, environment details, active services, and identified security exposures to produce a structured risk summary with severity assessment and remediation context.

**Request Body (application/json):**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `provider` | string | Yes | Cloud service provider (e.g., "aws", "azure", "gcp") |
| `environment` | string | Yes | Deployment environment (e.g., "production", "staging", "development") |
| `services` | array[string] | Yes | List of cloud services in use (e.g., ["ec2", "s3", "rds"]) |
| `exposures` | array[Exposure] | Yes | Array of identified security exposures, each with issue and impact description |

**Exposure Object:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `issue` | string | Yes | Description of the security issue or vulnerability |
| `impact` | string | Yes | Description of potential business impact if exploited |

**Response (200 - Success):**

Returns a JSON object containing:
- `summary` (string): Executive-level risk summary text
- `risk_level` (string): Overall risk classification (e.g., "critical", "high", "medium", "low")
- `provider` (string): Echoed provider identifier
- `environment` (string): Echoed environment name
- `exposure_count` (integer): Total number of exposures analyzed
- `affected_services` (array[string]): Services impacted by identified exposures
- `exposures_analyzed` (array): Detailed breakdown of each exposure with severity assessment

**Response (422 - Validation Error):**

```json
{
  "detail": [
    {
      "loc": ["body", "provider"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
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

- **Kong Route:** https://api.mkkpro.com/compliance/cloud-risk-summary
- **API Docs:** https://api.mkkpro.com:8027/docs
