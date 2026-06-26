## Description: <br>
G2b Cli helps agents query Korea Public Procurement Service OpenAPI endpoints for bidding notices, contract listings, and unified public procurement feeds. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chloepark85](https://clawhub.ai/user/chloepark85) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and procurement agents use this skill to monitor Korean public tenders, retrieve awarded-contract records, build tender dashboards, and prepare downstream supplier checks from public records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API keys or procurement records may be exposed through shared logs, stderr, JSONL outputs, or downstream KYB pipeline files. <br>
Mitigation: Keep G2B_SERVICE_KEY out of logs and avoid sharing outputs that contain API errors, business identifiers, or procurement records beyond the intended workflow. <br>
Risk: High-volume polling can exhaust data.go.kr quotas and interrupt tender-monitoring workflows. <br>
Mitigation: Use pagination and metadata checks, keep polling intervals reasonable, and request production-tier quota when sustained aggregation is required. <br>
Risk: Upstream procurement fields can vary by service surface and record type, which can break assumptions in downstream automations. <br>
Mitigation: Inspect representative JSONL rows before hard-coding field mappings, and prefer the unified standard feed when a stable schema is required. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/chloepark85/g2b-cli) <br>
- [data.go.kr](https://www.data.go.kr/) <br>
- [BidPublicInfoService API](https://apis.data.go.kr/1230000/ad/BidPublicInfoService) <br>
- [CntrctInfoService API](https://apis.data.go.kr/1230000/ao/CntrctInfoService) <br>
- [PubDataOpnStdService API](https://apis.data.go.kr/1230000/ao/PubDataOpnStdService) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, JSONL data, Guidance] <br>
**Output Format:** [Markdown guidance with bash examples; wrapper scripts emit JSONL records or single-line metadata JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, and a G2B_SERVICE_KEY for data.go.kr API access; API calls are read-only.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
