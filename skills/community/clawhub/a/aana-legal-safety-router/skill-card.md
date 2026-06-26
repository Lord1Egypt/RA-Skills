## Description: <br>
Routes legal-related agent responses to preserve jurisdiction caveats, distinguish general information from legal advice, avoid unsupported legal claims, and refer high-impact matters to qualified legal help. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mindbomber](https://clawhub.ai/user/mindbomber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill when answering, summarizing, drafting, classifying, or routing legal, regulatory, compliance, contract, immigration, criminal, family, employment, housing, court, dispute, or rights-related questions. It helps keep responses as general legal information unless qualified review is needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Marketplace capability tags include crypto and purchase authority even though the artifact is instruction-only. <br>
Mitigation: Verify platform-granted permissions before enabling the skill, and avoid granting purchase, crypto, external tool, or broad data access unless separately needed. <br>
Risk: Legal workflows may expose sensitive legal records, identifiers, credentials, or private documents. <br>
Mitigation: Use redacted summaries instead of raw legal records, court filings, contracts with private details, IDs, credentials, or unrelated private data. <br>
Risk: Legal-sensitive answers can overstate jurisdiction-specific law, deadlines, rights, or outcomes. <br>
Mitigation: Keep jurisdiction and current-law caveats, avoid unsupported claims, and route high-impact or deadline-sensitive matters to qualified legal professionals or human review. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mindbomber/aana-legal-safety-router) <br>
- [Legal safety review schema](schemas/legal-safety-review.schema.json) <br>
- [Redacted legal safety review example](examples/redacted-legal-safety-review.json) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration] <br>
**Output Format:** [Markdown guidance with optional structured JSON review payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only; does not install dependencies, execute commands, call services, write files, or persist memory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
