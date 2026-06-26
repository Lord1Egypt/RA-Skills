## Description: <br>
Run deep biological research using the BIOS API with API-key authentication or x402 crypto payments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jmartink](https://clawhub.ai/user/jmartink) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and researchers use this skill to start, monitor, and summarize BIOS deep-research sessions for biological and biomedical questions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Research prompts may be sent to a paid external biomedical API. <br>
Mitigation: Use a limited BIOS API key or limited funded wallet, avoid sharing secrets or unrelated personal data, and confirm expected costs before starting a request. <br>
Risk: BIOS outputs are AI-generated biomedical research summaries and may be incomplete or incorrect. <br>
Mitigation: Verify findings against primary sources before relying on them for scientific, medical, or operational decisions. <br>
Risk: x402 payment signing can expose funds if handled with an inappropriate wallet setup. <br>
Mitigation: Use a dedicated low-balance wallet or managed signer and keep private keys outside the agent workflow. <br>


## Reference(s): <br>
- [BIOS API documentation](https://ai.bio.xyz/docs/api/overview) <br>
- [x402 signer setup](references/x402-setup.md) <br>
- [x402 documentation](https://github.com/coinbase/x402) <br>
- [ClawHub skill page](https://clawhub.ai/jmartink/bios-deep-research) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries with curl command examples and state-file guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include BIOS conversation IDs, research status, discoveries, supporting evidence, confidence levels, and related hypotheses.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
