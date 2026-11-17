## Description:

Checks URLs shared from LINE, SMS, email, or chat for known scam, phishing, and suspicious-domain signals before a user clicks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phishguard-niki](https://clawhub.ai/user/phishguard-niki)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to evaluate suspicious links and receive advisory scam or phishing risk guidance before visiting a site or entering sensitive information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Risky links may be reported as safe because the security review found flaws in trust logic and setup flow.

Mitigation: Treat all results as advisory, verify suspicious links through additional sources, and avoid entering personal or payment information based only on a low-risk result.

Risk: Scans may be less reliable when GitHub-hosted blocklist data is unavailable.

Mitigation: Use the skill only where network and cache behavior are acceptable, and review uncertain results manually when blocklist data cannot be fetched.

Risk: The optional bulk download fetches remote shard data and can increase supply-chain exposure if downloaded data is not validated.

Mitigation: Avoid the optional bulk download unless the publisher validates shard filenames or pins and verifies the downloaded data.

Risk: Taiwan public-suffix domain handling requires extra caution according to the security guidance.

Mitigation: Apply manual review and independent checks before trusting results for Taiwan public-suffix domains.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/phishguard-niki/skills/anti-scam-guard)
- [Source code](https://github.com/phishguard-niki/Phishguard)
- [Issue tracker](https://github.com/phishguard-niki/Phishguard/issues)
- [Chrome Web Store extension](https://chromewebstore.google.com/detail/phishguard-scam-phishing-checker/odbipahjojmphhmjgicnafkhiikjandb)
- [LINE Bot](https://line.me/R/ti/p/@163hfjhz)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with URL risk results derived from checker JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results are advisory and should not be treated as proof that a link is safe.]

## Skill Version(s):

0.4.10 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
