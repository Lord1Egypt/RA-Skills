---
name: Cloud Compliance Checker
description: Validates cloud infrastructure configurations against industry compliance standards and regulatory frameworks.
---

# Overview

The Cloud Compliance Checker is a powerful API for auditing cloud infrastructure against multiple compliance standards and regulatory requirements. It enables security teams, cloud architects, and compliance officers to systematically verify that their cloud deployments meet required security postures and compliance benchmarks.

This tool supports major cloud providers and compliance frameworks, allowing organizations to perform automated compliance validation on their cloud configurations. Whether you're preparing for a security audit, maintaining continuous compliance, or validating infrastructure-as-code deployments, this API provides rapid, standardized compliance assessment against recognized standards.

Ideal users include DevSecOps teams automating compliance checks in CI/CD pipelines, cloud security engineers validating multi-cloud deployments, compliance auditors performing infrastructure reviews, and organizations managing regulatory obligations across diverse cloud environments.

## Usage

**Example Request:**

```json
{
  "provider": "aws",
  "standard": "cis",
  "config": "{\"region\": \"us-east-1\", \"scan_type\": \"full\"}"
}
```

**Example Response:**

```json
{
  "compliance_status": "passed",
  "provider": "aws",
  "standard": "cis",
  "checks_performed": 156,
  "checks_passed": 154,
  "checks_failed": 2,
  "compliance_percentage": 98.7,
  "failed_checks": [
    {
      "check_id": "CIS-1.2",
      "title": "Ensure MFA is enabled for all IAM users",
      "severity": "high",
      "resource": "iam-user-admin"
    },
    {
      "check_id": "CIS-2.1",
      "title": "Ensure CloudTrail is enabled on all regions",
      "severity": "medium",
      "resource": "eu-west-1"
    }
  ],
  "timestamp": "2024-01-15T10:30:00Z",
  "scan_duration_seconds": 42
}
```

## Endpoints

### POST /check-compliance

Performs a comprehensive compliance audit against specified cloud provider and compliance standard.

**Method:** `POST`

**Path:** `/check-compliance`

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `provider` | string | Yes | Cloud provider identifier (e.g., `aws`, `azure`, `gcp`, `kubernetes`) |
| `standard` | string | Yes | Compliance framework or standard (e.g., `cis`, `pci-dss`, `hipaa`, `sox`, `nist`, `iso27001`) |
| `config` | string | No | JSON string containing provider-specific configuration options. Default: `"{}"`. Supports parameters like region, scan_type, resource_filters, etc. |

**Response (200 - Success):**

Returns a JSON object containing:
- `compliance_status`: Overall status (passed/failed/warning)
- `provider`: The cloud provider checked
- `standard`: The compliance standard used
- `checks_performed`: Total number of compliance checks executed
- `checks_passed`: Number of passing checks
- `checks_failed`: Number of failing checks
- `compliance_percentage`: Percentage of checks passed
- `failed_checks`: Array of failed checks with check_id, title, severity, and resource
- `timestamp`: UTC timestamp of the scan
- `scan_duration_seconds`: Time taken to complete the audit

**Response (422 - Validation Error):**

Returns validation error details when required parameters are missing or invalid.

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

- **Kong Route:** https://api.mkkpro.com/compliance/cloud-compliance
- **API Docs:** https://api.mkkpro.com:8019/docs
