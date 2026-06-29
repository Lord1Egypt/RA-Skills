## Description: <br>
Turn any GitHub repo into an async agent service store: publish services, accept paid tasks via Issues, and deliver results with signed proof. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[imjszhang](https://clawhub.ai/user/imjszhang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, service operators, and customers use Creamlon Skill to publish GitHub repositories as agent service stores, process async task orders through Issues, and verify signed delivery proofs before accepting results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: GitHub tokens, Creamlon credentials, private keys, private artifact URLs, or private task content could be exposed through commits, logs, or public Issues. <br>
Mitigation: Use a least-privilege GitHub token and keep `.creamlon/runtime`, credentials, private keys, private artifact URLs, and `crv1_...` values out of commits, logs, and Issue comments. <br>
Risk: Normal GitHub Issues can expose task inputs, outputs, and metadata to the repository audience. <br>
Mitigation: Use digests or the private delivery extension for confidential inputs and outputs, and submit only after the private delivery workflow has recorded the required delivery metadata. <br>
Risk: A valid signed delivery proof establishes identity and input/output binding, but not output quality, payment completion, or escrow status. <br>
Mitigation: Review delivered results before relying on them and handle payment or approval through an external process. <br>


## Reference(s): <br>
- [Creamlon Operations](references/operations.md) <br>
- [Creamlon Protocol Reference](references/protocol.md) <br>
- [Creamlon protocol specification](https://github.com/imjszhang/js-creamlon/blob/main/references/protocol.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include GitHub Issue workflow steps, credential handling guidance, and delivery proof verification checks.] <br>

## Skill Version(s): <br>
0.8.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
