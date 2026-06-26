## Description: <br>
Pre-ingestion verification for epistemic quality in RAG systems, producing Clarity-Gated Documents and validating Source of Truth files before knowledge-base use. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[frmoretto](https://clawhub.ai/user/frmoretto) <br>

### License/Terms of Use: <br>
CC-BY-4.0 <br>


## Use Case: <br>
Developers, documentation owners, and RAG system operators use this skill to review documents for unclear claims, missing uncertainty markers, temporal inconsistencies, and human verification needs before ingestion. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill checks whether claims are clearly qualified, but it does not independently prove that the claims are true. <br>
Mitigation: Complete and review the HITL verification record before treating generated CGD output as ready for RAG ingestion. <br>
Risk: Generated CGD or HITL outputs may be added to a knowledge base without sufficient review. <br>
Mitigation: Review generated outputs before ingestion and use explicit invocations for document review workflows. <br>
Risk: Bundled helper scripts operate on local files supplied by the user. <br>
Mitigation: Run the helper scripts only on files intentionally selected for Clarity Gate analysis. <br>


## Reference(s): <br>
- [Clarity Gate release page](https://clawhub.ai/frmoretto/clarity-gate) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [claim_id.py](artifact/scripts/claim_id.py) <br>
- [document_hash.py](artifact/scripts/document_hash.py) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, text, shell commands, guidance] <br>
**Output Format:** [Markdown reports, CGD markdown files, validation findings, HITL review tables, and helper-script command output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce .cgd.md documents with Clarity Gate frontmatter, document hashes, HITL claims, and end markers.] <br>

## Skill Version(s): <br>
2.1.3 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
