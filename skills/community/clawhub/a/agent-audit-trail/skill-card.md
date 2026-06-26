## Description: <br>
Append-only, hash-chained audit log for AI agents that records actions, tool calls, decisions, and external writes with provenance, timestamps, and sha256 chain integrity for EU AI Act Article 12 event recording. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[roosch269](https://clawhub.ai/user/roosch269) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and compliance engineers use this skill to configure append-only NDJSON audit logging for AI agent activity, including tool calls, decisions, credential access, payments, and external writes. It supports traceability, tamper detection, and event-recording workflows for high-risk AI system compliance review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audit entries may contain sensitive operational metadata, personal data, credential locations, or payment details if users log more than is necessary. <br>
Mitigation: Decide log location, access controls, retention, and redaction rules before installation; avoid raw secrets, tokens, passwords, unnecessary personal data, and overly detailed credential locations. <br>
Risk: Future remote log shipping could introduce additional security and compliance exposure. <br>
Mitigation: Treat remote shipping as a separate security and compliance decision with dedicated review before enabling it. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with JSON, Python, and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local append-only NDJSON audit log guidance with hash-chain verification examples.] <br>

## Skill Version(s): <br>
2.1.0 (source: frontmatter, release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
