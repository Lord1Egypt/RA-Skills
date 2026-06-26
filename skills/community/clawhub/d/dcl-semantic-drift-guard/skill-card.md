## Description: <br>
Use this skill to detect semantic hallucinations and context drift in LLM outputs by checking whether generated responses are grounded in supplied source documents or retrieved knowledge. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daririnch](https://clawhub.ai/user/daririnch) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, AI application teams, and governance reviewers use this skill to compare LLM outputs against authoritative documents or RAG-retrieved context before accepting, logging, or delivering the output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Source documents and knowledge-base queries may contain confidential or regulated content. <br>
Mitigation: Provide only sources and kb_endpoint URLs that are trusted for the intended workflow, and avoid submitting confidential material unless the deployment environment is approved for it. <br>
Risk: The artifact describes no-retention, compliance, and audit-chain behavior that is not independently proven by the server security evidence. <br>
Mitigation: Treat those claims as publisher-provided behavior statements and verify operational controls before relying on them for compliance or retention guarantees. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/daririnch/dcl-semantic-drift-guard) <br>
- [Publisher profile](https://clawhub.ai/user/daririnch) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown guidance with JSON input and output schemas] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a verdict-oriented audit record structure with drift items, confidence, source mode, strictness, policy, hash, timestamp, and audit chain identifier.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
