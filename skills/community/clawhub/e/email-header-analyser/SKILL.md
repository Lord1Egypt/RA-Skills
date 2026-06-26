---
name: Email Header Analyser API
description: Analyzes email headers to extract authentication, routing, and security metadata for threat detection and email forensics.
---

# Overview

The Email Header Analyser API provides deep inspection and forensic analysis of email message headers. Security professionals, incident responders, and email administrators use this tool to identify spoofing attempts, trace message routing, validate authentication protocols (SPF, DKIM, DMARC), and detect malicious headers.

Email headers contain critical metadata that reveals the true origin of messages, intermediate mail servers, and authentication status. This API parses raw headers and extracts actionable intelligence for phishing investigations, compliance audits, and email security operations.

Ideal users include SOC analysts, email security teams, incident response professionals, forensic investigators, and organizations requiring email authentication verification and threat intelligence capabilities.

## Usage

### Sample Request

```json
{
  "header": "Received: from mail.example.com (mail.example.com [192.0.2.1]) by mx.targetdomain.com with SMTP id abc123; Wed, 15 Jan 2025 10:30:45 +0000\nFrom: sender@example.com\nTo: recipient@targetdomain.com\nSubject: Security Analysis\nAuthentication-Results: targetdomain.com; spf=pass smtp.mailfrom=sender@example.com; dkim=pass header.d=example.com; dmarc=pass\nReturn-Path: <sender@example.com>\nDate: Wed, 15 Jan 2025 10:30:45 +0000"
}
```

### Sample Response

```json
{
  "sender_ip": "192.0.2.1",
  "sender_domain": "mail.example.com",
  "from_address": "sender@example.com",
  "to_address": "recipient@targetdomain.com",
  "received_servers": [
    {
      "hostname": "mail.example.com",
      "ip": "192.0.2.1",
      "timestamp": "2025-01-15T10:30:45Z"
    },
    {
      "hostname": "mx.targetdomain.com",
      "ip": null,
      "timestamp": null
    }
  ],
  "authentication": {
    "spf": "pass",
    "dkim": "pass",
    "dmarc": "pass"
  },
  "subject": "Security Analysis",
  "date": "2025-01-15T10:30:45Z",
  "return_path": "sender@example.com",
  "suspicious_indicators": []
}
```

## Endpoints

### POST /analyze-header

Analyzes a raw email header to extract authentication, routing, and security metadata.

**Method:** POST  
**Path:** `/analyze-header`

**Request Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| header | string | Yes | Raw email header text containing one or more Received headers, authentication headers, and message metadata. |

**Response Schema:**

The response contains extracted header analysis including:

| Field | Type | Description |
|-------|------|-------------|
| sender_ip | string | IP address of the originating mail server. |
| sender_domain | string | Hostname of the originating mail server. |
| from_address | string | Email address in the From header. |
| to_address | string | Email address in the To header. |
| received_servers | array | List of mail servers in the routing path with hostname, IP, and timestamp. |
| authentication | object | Authentication protocol results (spf, dkim, dmarc status). |
| subject | string | Email subject line. |
| date | string | Message date in ISO 8601 format. |
| return_path | string | Return-Path header value. |
| suspicious_indicators | array | List of detected anomalies or security concerns. |

**Status Codes:**

- **200:** Successful analysis returned.
- **422:** Validation error—header field missing or invalid.

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

- Kong Route: https://api.mkkpro.com/security/email-header-analyser
- API Docs: https://api.mkkpro.com:8016/docs
