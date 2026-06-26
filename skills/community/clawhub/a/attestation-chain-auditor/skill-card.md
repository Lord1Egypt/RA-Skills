## Description: <br>
Helps validate the completeness and integrity of trust attestation chains in AI agent ecosystems, identifying broken links, expired credentials, and missing vouching relationships that make verified trust claims unverifiable. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andyxinweiminicloud](https://clawhub.ai/user/andyxinweiminicloud) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, security reviewers, and marketplace operators use this skill to audit trust attestation chains for completeness, expiry, circular vouching relationships, authority legitimacy, revocation propagation, and overall chain strength. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may lead an agent to inspect private attestation documents or internal trust metadata. <br>
Mitigation: Only provide private attestation documents or internal trust metadata when they are intended for the audit. <br>
Risk: The skill declares curl and python3 as available binaries, so later agent-proposed commands could fetch or process external data. <br>
Mitigation: Review any curl or python commands before execution. <br>
Risk: Attestation chain audits can be incomplete when chain metadata is opaque or unpublished. <br>
Mitigation: Treat missing chain metadata as an explicit limitation and avoid reconstructing unavailable links from unrelated provenance. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/andyxinweiminicloud/attestation-chain-auditor) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/andyxinweiminicloud) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Guidance] <br>
**Output Format:** [Markdown attestation chain audit report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include chain visualization, link-by-link validity assessment, circular dependency findings, authority legitimacy assessment, revocation results, chain strength rating, and recommended actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
