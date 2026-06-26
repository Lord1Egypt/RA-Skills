# Security Threat Indicators & Sources

This reference provides key indicators for identifying phishing, scams, and vulnerabilities, along with reliable sources for security research.

## Phishing Indicators

- **URL Discrepancies**: Slight misspellings (e.g., `g00gle.com` instead of `google.com`), unusual top-level domains (TLDs), or excessive subdomains.
- **Urgent or Threatening Language**: Phrases like "Account suspended," "Immediate action required," or "Legal action will be taken."
- **Requests for Sensitive Information**: Asking for passwords, PINs, social security numbers, or credit card details via email or a suspicious link.
- **Generic Greetings**: Using "Dear Customer" or "Dear User" instead of the user's actual name.
- **Mismatched Sender Address**: The sender's email address does not match the official domain of the organization they claim to represent.

## Scam Indicators

- **Too Good to Be True**: Promises of high returns with little to no risk, or winning a lottery/contest the user never entered.
- **Pressure Tactics**: Demanding immediate payment via untraceable methods like gift cards, wire transfers, or cryptocurrency.
- **Lack of Transparency**: No clear physical address, contact information, or official documentation for a business or investment opportunity.

## Vulnerability Sources (CVEs)

- **NVD (National Vulnerability Database)**: [https://nvd.nist.gov/](https://nvd.nist.gov/)
- **CVE MITRE**: [https://cve.mitre.org/](https://cve.mitre.org/)
- **GitHub Advisory Database**: [https://github.com/advisories](https://github.com/advisories)
- **Snyk Vulnerability DB**: [https://snyk.io/vuln/](https://snyk.io/vuln/)

## Analysis Workflow

1.  Identify the target for analysis (URL, file, message).
2.  Cross-reference with known threat indicators.
3.  Use browser tools to search for recent reports or vulnerabilities associated with the target.
4.  Compile a risk assessment report for the user.
