## Description: <br>
Queries aviation regulations, manuals, and publications through Deepsky's open search API for ICAO, FAA/14 CFR, EASA, CASA, and related operational rule lookups. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deepskyai](https://clawhub.ai/user/deepskyai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Aviation-focused agents use this skill to search regulatory and operational documentation, return cited excerpts, and help users compare rule references across supported jurisdictions. It is intended for regulation lookup support, not for live aviation data such as weather, NOTAM feeds, charts, or flight plans. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User aviation-regulation questions are sent to Deepsky's public API. <br>
Mitigation: Avoid including private operational details, personal data, or confidential legal or compliance context in search queries. <br>
Risk: Aviation regulatory answers can affect safety-critical decisions. <br>
Mitigation: Verify returned excerpts and citations against official regulator sources before using them for operational, legal, or compliance decisions. <br>


## Reference(s): <br>
- [Aviation Regulations Search](https://clawhub.ai/deepskyai/aviation-regulations) <br>
- [Deepsky API Search](https://www.deepskyai.com/api/v1/search) <br>
- [Deepsky Agent Manifest](https://www.deepskyai.com/llms.txt) <br>
- [Deepsky OpenAPI Schema](https://www.deepskyai.com/.well-known/openapi.json) <br>
- [Query Tips](references/query-tips.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown responses with cited regulatory excerpts; optional JSON from the helper script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search results should include jurisdiction, rule reference, excerpt, and Deepsky source URL; match count is limited to 1-20.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
