## Description: <br>
Redacts sensitive fields from medical records or other documents through the EasyLink masking API, including submission, polling, custom masking fields, and masked-file result handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sycamore792](https://clawhub.ai/user/sycamore792) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operational users use this skill to submit medical records or documents to EasyLink for sensitive-field masking, poll asynchronous tasks, and retrieve normalized masked-file results. <br>

### Deployment Geography for Use: <br>
Global, subject to EasyLink CN platform availability and applicable data-processing requirements. <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive medical or personal documents are sent to an external EasyLink service. <br>
Mitigation: Use only when authorized, confirm the endpoint, region, retention model, and API-key handling, and avoid regulated records unless third-party processing is approved. <br>
Risk: The skill requires an EasyLink API key. <br>
Mitigation: Store the key in EASYLINK_API_KEY or a managed secret store, and avoid exposing it in shared logs, prompts, or saved outputs. <br>


## Reference(s): <br>
- [EasyLink EasyDoc Mask API Reference](references/easydoc-mask-api.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/sycamore792/easydoc-mask) <br>
- [EasyLink Platform](https://platform.easylink-ai.com) <br>
- [EasyLink EasyDoc Mask Endpoint](https://api.easylink-ai.com/v1/easydoc/mask) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash and Python command examples plus normalized JSON result envelopes.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires EASYLINK_API_KEY; uploads supported document files up to 100 MB and may return masked-file download URLs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
