---
name: Cloud Misconfiguration Scanner
description: Automated security scanner for identifying and reporting misconfigurations across cloud infrastructure providers.
---

# Overview

The Cloud Misconfiguration Scanner is a security-focused API that analyzes cloud infrastructure configurations to identify potential security risks, compliance violations, and operational misconfigurations. It connects to major cloud providers and performs comprehensive audits of your cloud environment without requiring direct infrastructure changes.

This tool is essential for security teams, DevOps engineers, and cloud architects who need continuous visibility into their cloud security posture. By automating configuration scanning, it reduces the time and effort required for manual security assessments while providing detailed, actionable remediation guidance. The scanner integrates seamlessly with multi-cloud environments and supports automated compliance reporting workflows.

Ideal users include organizations managing infrastructure across AWS, Azure, Google Cloud, or hybrid cloud environments; security and compliance teams performing regular audits; and enterprises implementing Infrastructure-as-Code (IaC) security practices.

## Usage

**Sample Request:**

```json
{
  "provider": "aws",
  "credentials": {
    "access_key_id": "AKIAIOSFODNN7EXAMPLE",
    "secret_access_key": "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
    "region": "us-east-1"
  }
}
```

**Sample Response:**

```json
{
  "scan_id": "scan_1234567890",
  "provider": "aws",
  "status": "completed",
  "timestamp": "2024-01-15T10:30:45Z",
  "findings": [
    {
      "id": "MISCFG-001",
      "severity": "high",
      "category": "access_control",
      "resource": "s3://my-bucket-prod",
      "issue": "S3 bucket has public read access enabled",
      "recommendation": "Update bucket policy to restrict public access",
      "compliance_impact": ["PCI-DSS", "HIPAA"]
    },
    {
      "id": "MISCFG-002",
      "severity": "medium",
      "category": "encryption",
      "resource": "rds-instance-main",
      "issue": "Database encryption at rest is disabled",
      "recommendation": "Enable RDS encryption and rotate master key",
      "compliance_impact": ["SOC2"]
    }
  ],
  "summary": {
    "total_resources_scanned": 247,
    "misconfiguration_count": 12,
    "high_severity": 2,
    "medium_severity": 5,
    "low_severity": 5
  }
}
```

## Endpoints

### POST /scan-cloud-config

Initiates a comprehensive security scan of cloud infrastructure configurations for the specified provider.

**Method:** `POST`

**Path:** `/scan-cloud-config`

**Description:** Scans cloud configurations and identifies security misconfigurations, compliance violations, and operational risks across the target environment.

**Request Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `provider` | string | Yes | Cloud provider identifier (e.g., `aws`, `azure`, `gcp`, `alibaba`) |
| `credentials` | object | Yes | Provider-specific authentication credentials including access keys, secret keys, tokens, or service account data required to authenticate and access cloud resources |

**Response Shape (HTTP 200):**

```json
{
  "scan_id": "string",
  "provider": "string",
  "status": "string",
  "timestamp": "string",
  "findings": [
    {
      "id": "string",
      "severity": "string",
      "category": "string",
      "resource": "string",
      "issue": "string",
      "recommendation": "string",
      "compliance_impact": ["string"]
    }
  ],
  "summary": {
    "total_resources_scanned": "integer",
    "misconfiguration_count": "integer",
    "high_severity": "integer",
    "medium_severity": "integer",
    "low_severity": "integer"
  }
}
```

**Error Response (HTTP 422 - Validation Error):**

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

- **Kong Route:** https://api.mkkpro.com/security/cloud-misconfig-scanner
- **API Docs:** https://api.mkkpro.com:8018/docs
