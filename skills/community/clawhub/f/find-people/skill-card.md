## Description: <br>
Find People (x402) helps agents run paid OSINT research on individuals, including professional backgrounds, career timelines, credential checks, due diligence, competitive intelligence, and investor research. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TzannetosGiannis](https://clawhub.ai/user/TzannetosGiannis) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to research public information about individuals for background research, due diligence, hiring, partnerships, investment, competitive analysis, or journalism. Each lookup requires a paid x402 request. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Paid people-search requests can return sensitive or unverified personal data. <br>
Mitigation: Confirm each lookup has a legitimate purpose, review results before relying on them, and do not use the tool for stalking, doxxing, discrimination, or decisions based solely on unverified data. <br>
Risk: The workflow uses a raw wallet private key with external code fetched at runtime. <br>
Mitigation: Use a dedicated low-balance wallet, avoid project-local plaintext key files, and inspect the external package before running paid lookups. <br>
Risk: Each query can trigger a paid x402 request. <br>
Mitigation: Confirm user consent and payment intent before running the script, and avoid unattended or repeated lookups. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/TzannetosGiannis/find-people) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and terminal output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a person query and an x402 wallet private key; paid lookups cost $0.15 USDC per request on Base.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
