## Description: <br>
Car Scraper collects used and new vehicle listings from Dasouche, Dongchedi, and Autohome, then exports the data in OpenClaw-compatible JSON, JSONL, or CSV formats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jackiezhao-eng](https://clawhub.ai/user/jackiezhao-eng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data teams use this skill to collect car listing, pricing, vehicle detail, and dealer information from supported automotive sites and normalize it for OpenClaw ingestion or market analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill collects data from target sites and includes anti-bot evasion behavior. <br>
Mitigation: Use it only with authorization to collect from the target sites, keep page counts low, and disable proxy rotation unless clearly permitted. <br>
Risk: The collected vehicle records may include VIN and dealer contact fields. <br>
Mitigation: Remove, redact, or restrict VIN and dealer phone fields unless they are necessary, lawfully handled, and covered by the intended use. <br>
Risk: The security review verdict is suspicious because privacy and authorization guardrails are not clearly defined. <br>
Mitigation: Require human review of target-site permissions, data retention, and downstream sharing before deployment. <br>


## Reference(s): <br>
- [Car Scraper on ClawHub](https://clawhub.ai/jackiezhao-eng/car-scraper) <br>
- [Publisher profile](https://clawhub.ai/user/jackiezhao-eng) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Code, Shell commands, Configuration, Data files, Guidance] <br>
**Output Format:** [Markdown usage guidance plus JSON, JSONL, and CSV data exports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Exports normalized VehicleInfo records with source URL, title, vehicle metadata, images, VIN when present, dealer fields, and timestamps.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
