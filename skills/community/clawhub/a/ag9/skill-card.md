## Description: <br>
Use AG9 to register and verify AI agents with VeryAI Palm-backed human ownership, generate or load portable Ed25519 identities for OpenClaw, Codex, local CLI/MCP, browser, or cloud agents, call AG9 registration/signature verification APIs, and solve reverse-CAPTCHA capability challenges. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oyyblin](https://clawhub.ai/user/oyyblin) <br>

### License/Terms of Use: <br>
Apache License 2.0 <br>


## Use Case: <br>
Developers and agent operators use this skill to register an agent under a palm-verified human owner, prove control of an Ed25519 agent identity, verify AG9 registration status, or solve AG9 reverse-CAPTCHA challenges for capability attestation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may create or load AG9 identity material, including private keys, from ~/.ag9/identity.json, ~/.openclaw/identity/device.json, or cloud secret variables. <br>
Mitigation: Protect identity files and AG9 private-key environment variables, and confirm private keys are used only locally for signing. <br>
Risk: AG9 verification sends public key material, signatures, messages, timestamps, tokens, and challenge solutions to AG9 services, and registration involves VeryAI palm-based human verification. <br>
Mitigation: Install only when AG9 identity registration or reverse-CAPTCHA verification is intended, and use the VeryAI registration link only if the human owner accepts palm verification. <br>
Risk: Registration URLs are short-lived and intended for the human owner; opening them automatically or sharing them broadly can send the verification flow to the wrong person. <br>
Mitigation: Output registration URLs as text or Markdown links for the owner to open manually, and avoid browser-launch commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oyyblin/ag9) <br>
- [AG9 homepage](https://ag9.ai) <br>
- [AG9 API base](https://api.ag9.ai) <br>
- [AG9 OpenAPI specification](https://api.ag9.ai/openapi/v1.yaml) <br>
- [AG9 interactive demo](https://ag9.ai/demo) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline JSON, JavaScript, shell commands, API request examples, and registration links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce AG9 registration URLs for the human owner to open manually; may guide creation or loading of local identity files and cloud secret variables.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release metadata and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
