---
name: security-alerter
description: Provides security alerts for phishing, scams, and known vulnerabilities. Use this when a user asks to check for security threats, analyze suspicious links/files, or get information on recent vulnerabilities.
---

# Security Alerter

This skill enables the agent to act as a security analyst, providing alerts and insights on potential phishing attempts, scams, and known software vulnerabilities. It leverages various threat intelligence sources and analysis techniques to keep users informed and secure.

## Workflow

When a user requests a security analysis or alert, follow these steps:

### 1. Understand User Request

- **Type of Analysis**: Determine if the user is asking for a general alert, an analysis of a specific URL/file/message, or information on known vulnerabilities.
- **Context**: Gather any relevant context, such as the source of a suspicious link, the content of a questionable email, or the software/system they are concerned about.

### 2. Perform Analysis

- **Phishing/Scam Detection**: If analyzing a URL or message, use browser tools to:
    - Inspect the URL for discrepancies (misspellings, unusual TLDs).
    - Analyze the content for urgent/threatening language, generic greetings, or requests for sensitive information.
    - Cross-reference with known phishing indicators outlined in `references/threat_indicators.md`.
- **Vulnerability Check**: If the user is concerned about specific software or systems, or if a general vulnerability check is requested:
    - Search reputable vulnerability databases (NVD, CVE MITRE, GitHub Advisory Database, Snyk) for known vulnerabilities related to the specified software/system. Refer to `references/threat_indicators.md` for links to these sources.
    - Look for recent exploits or active threats.

### 3. Generate Security Report/Alert

Based on the analysis, compile a clear and concise report or alert for the user. This should include:

- **Threat Level**: Assign a severity level (e.g., Low, Medium, High, Critical) to the detected threat or vulnerability.
- **Findings**: Detail what was found, including specific indicators of phishing, scam tactics, or CVE details.
- **Impact**: Explain the potential risks or consequences of the threat.
- **Recommendations**: Provide actionable advice on how to mitigate the risk (e.g., do not click the link, update software, enable 2FA).
- **Sources**: Cite any sources used for vulnerability information.

### 4. Deliver to User

Present the security report or alert to the user, ensuring they understand the findings and recommended actions. Offer to answer any follow-up questions or perform further investigation.

## References

- `references/threat_indicators.md`: Contains a comprehensive list of phishing and scam indicators, along with links to major vulnerability databases (NVD, CVE MITRE, GitHub Advisory Database, Snyk).