---
name: breach-check
description: "Check if your email, phone or password has been in data breaches. Full security response workflow."
metadata:
  category: Security/Privacy
  priority: P0
  languages: zh-CN, en
---

# Breach Check

Check if email, phone, or password has appeared in known data breaches. Uses k-anonymity and privacy-preserving lookup, never sends raw credentials.

## Workflow

1. **Hash input** — SHA-256 hash of email/phone. For passwords, use SHA-1 prefix (k-anonymity model, first 5 chars only sent).
2. **Query breach DB** — call Have I Been Pwned API v3 (or equivalent) with hash prefix. Respect rate limits (1.5s delay between calls).
3. **Results** — return only: breached (yes/no), breach name, data types exposed (email, password, phone, address, etc.).
   - Never return raw password or plaintext credential.
4. **Severity triage**:
   - 🔴 **High** — password exposed
   - 🟡 **Medium** — phone / address / ID number exposed
   - 🟢 **Low** — email-only breach
5. **Action plan** — per breach:
   - 🔴 → change password immediately, enable 2FA, check for account takeover
   - 🟡 → monitor for phishing, update linked account recovery info
   - 🟢 → review spam filter, update email alias if heavy spam
6. **Password check** — SHA-1 k-anonymity: send first 5 hex chars to Pwned Passwords API. Return count of occurrences.
7. **Report** — personal security report with:
   - breach timeline
   - severity summary
   - actionable todo list (prioritized)
8. **Optional** — set reminder for periodic re-check (cron / scheduling).

## Sample Prompt

```
breach-check check --email user@example.com --phone 13900000000
breach-check password --check "my-p@ssw0rd"
breach-check monitor --email user@example.com --interval monthly
breach-check report --email user@example.com --format json
```
