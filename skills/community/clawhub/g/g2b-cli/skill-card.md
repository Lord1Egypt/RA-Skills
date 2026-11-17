## Description:

G2b Cli helps agents query Korea's public procurement OpenAPI for bidding notices, contract listings, and open-standard award or contract feeds through Bash subcommands that return JSONL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chloepark85](https://clawhub.ai/user/chloepark85)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, procurement analysts, and agent builders use this skill to monitor Korean public tenders, build RFP dashboards, scrape awarded contracts, and feed supplier KYB or warehouse workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Real data.go.kr credentials can be exposed through command-line URLs or visible shell processes.

Mitigation: Run the scripts only in a trusted shell, avoid shared systems where process command lines may be visible, and rotate credentials if exposure is suspected.

Risk: Endpoint override variables can redirect requests away from the official public procurement API hosts.

Mitigation: Clear or verify G2B_BID_BASE, G2B_CNTRCT_BASE, and G2B_STD_BASE before use, and keep them pointed at the official https://apis.data.go.kr hosts.

Risk: Example workflows can save JSONL files containing public tender records and supplier identifiers.

Mitigation: Store generated JSONL files in appropriate workspaces, review downstream sharing, and delete temporary extracts when they are no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chloepark85/skills/g2b-cli)
- [data.go.kr](https://www.data.go.kr/)
- [BidPublicInfoService endpoint](https://apis.data.go.kr/1230000/ad/BidPublicInfoService)
- [CntrctInfoService endpoint](https://apis.data.go.kr/1230000/ao/CntrctInfoService)
- [PubDataOpnStdService endpoint](https://apis.data.go.kr/1230000/ao/PubDataOpnStdService)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline Bash commands; runtime command output is JSONL.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires G2B_SERVICE_KEY; --meta returns response paging metadata instead of records.]

## Skill Version(s):

0.1.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
