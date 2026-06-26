# Security and Secrets Management

## Overview
This document outlines security best practices for using the Facebook Graph API skill in production environments.

## 1. Secret Storage
- Never store `FB_APP_SECRET` or `FB_ACCESS_TOKEN` in source control.
- Use environment variables, a secrets manager (e.g., HashiCorp Vault, AWS Secrets Manager), or OpenClaw's built-in secret resolution.
- Rotate secrets regularly and after any suspected exposure.

## 2. Principle of Least Privilege
- Request only the permissions your workflow needs.
- Use `pages_manage_posts` instead of broader publish permissions when possible.
- Review and revoke unused tokens periodically.

## 3. Webhook Security
If using webhooks:
- Verify the `X-Hub-Signature-256` header using your app secret.
- Reject requests with invalid signatures.
- Validate the `entry` and `time` fields to prevent replay attacks.

## 4. Rate Limiting and Retries
- Implement exponential backoff on 429 responses.
- Respect the `x-app-usage` and `x-page-usage` headers to stay within rate limits.
- Batch requests where possible to reduce API calls.

## 5. Logging and Monitoring
- Do not log full tokens, app secrets, or personally identifiable information (PII).
- Log only minimal identifiers (e.g., post ID, comment ID) for debugging.
- Set up alerts for unusual activity (e.g., sudden spikes in posts or deletions).

## 6. Incident Response
If a token or secret is compromised:
1. Revoke the token immediately via Facebook Developer Dashboard.
2. Generate a new Page access token.
3. Rotate the App Secret if it may have been exposed.
4. Review recent API calls for unauthorized actions.
5. Notify affected stakeholders per your security policy.

## 7. Compliance
- Ensure your usage complies with Facebook's Platform Policy.
- Store user data according to applicable regulations (GDPR, CCPA, etc.).
- Provide a mechanism for users to request data deletion if required.
