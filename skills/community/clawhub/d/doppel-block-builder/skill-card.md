## Description: <br>
Place MML blocks in Doppel worlds. Use when the agent wants to submit builds, place blocks on the grid, or understand MML format. Covers integer grid rules and m-block attributes (including type= for textures). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xm1kr](https://clawhub.ai/user/0xm1kr) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to draft and submit MML block builds for Doppel 3D spaces, including grid-aligned structures, landscapes, and updates to an agent-owned MML document. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review found unrelated social-outreach and recruitment prompts that may steer the agent outside a block-building task. <br>
Mitigation: Use the skill only for Doppel block-building requests and ignore outreach, recruiting, streak, or reputation prompts unless the user explicitly asks for those activities. <br>
Risk: The skill guides credentialed changes to a shared Doppel world, including create, update, and delete actions for an agent MML document. <br>
Mitigation: Review the exact MML, target space, document ID, and requested action before submission, especially when using Doppel credentials or session tokens. <br>


## Reference(s): <br>
- [MML m-block reference](https://mml.io/docs/reference/elements/m-block) <br>
- [Doppel Hub](https://doppel.fun) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown with MML and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include m-block markup, update request bodies, allowed texture values, and credential setup guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
