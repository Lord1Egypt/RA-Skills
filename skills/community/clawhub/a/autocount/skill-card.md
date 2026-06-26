## Description: <br>
Create and validate AutoCount sales, purchase, and master-data documents through the AutoCount Web API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teckyuen](https://clawhub.ai/user/teckyuen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and business-system operators use this skill to create, test, inspect, and validate AutoCount sales and purchase documents through a Windows-hosted AutoCount Web API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create, update, cancel, or delete real AutoCount business documents. <br>
Mitigation: Use drafts or test company data by default and require explicit approval before final posting, transfers, updates, cancellations, or deletions. <br>
Risk: AutoCount API credentials may be exposed when used over untrusted HTTP networks. <br>
Mitigation: Use least-privilege API keys and avoid sending keys over untrusted HTTP networks. <br>
Risk: Transfer chains and document mutations can affect the wrong source or target document if identifiers or quantities are incorrect. <br>
Mitigation: Validate source document status, quantities, DocNo, and DocKey before mutation, then fetch and report the affected record after each create or update. <br>


## Reference(s): <br>
- [AutoCount Invoice Test Notes](references/test-notes.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, JSON payloads, API call instructions, configuration] <br>
**Output Format:** [Markdown with JSON and HTTP snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prefers draft document creation and requires explicit approval for final posting, transfers, updates, cancellations, or deletions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
