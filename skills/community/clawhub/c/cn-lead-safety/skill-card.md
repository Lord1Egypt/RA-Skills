## Description: <br>
Chinese-market client-intelligence safety layer for lead-discovery skills that enforces literal Chinese text, controlled term usage, source-tier ordering, inline citations for hard numbers, and no-fabrication handling for missing data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jackdark425](https://clawhub.ai/user/jackdark425) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill as a quality gate for Chinese-market lead-discovery markdown before downstream banker deliverables consume the intelligence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The verifier checks markdown citation coverage but does not fully validate Chinese typos, lexicon usage, source-tier ordering, or whether unavailable data was fabricated. <br>
Mitigation: Use the verifier as a citation gate and pair it with human review or downstream checks for terminology, source quality, and missing-data handling. <br>
Risk: Hard numbers can be misleading if they cite media-only or unavailable sources for financial intelligence. <br>
Mitigation: Run the verifier in strict mode when stronger traceability is required so hard numbers must cite an MCP-tool anchor or official filing source. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell command examples and a Python verification script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Verifies citation coverage for hard numbers in generated intelligence markdown; strict mode requires MCP-tool or official-filing anchors.] <br>

## Skill Version(s): <br>
0.8.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
