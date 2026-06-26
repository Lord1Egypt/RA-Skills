## Description: <br>
Use this skill when the user provides AF2, ESMFold, AF3, Boltz-1, SASA, or MD results and needs a Gate 1-4 audit with a Go/Hold/Kill decision. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[barrett-cryptoDNA](https://clawhub.ai/user/barrett-cryptoDNA) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers and developers use this skill to review user-provided structural prediction, epitope exposure, and molecular dynamics evidence for nanoparticle vaccine design gates and decide Go, Hold, or Kill. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Most audit instructions are in Chinese, which may lead to reviewer misunderstanding if the workflow team cannot read them directly. <br>
Mitigation: Use reviewers who can read the instructions or translate and verify the Gate 1-4 criteria before relying on audit decisions. <br>
Risk: The skill evaluates user-provided modeling results and can produce incorrect Go/Hold/Kill guidance if the supplied evidence is incomplete or unreliable. <br>
Mitigation: Confirm required logs, checkpoints, repeats, exposure metrics, and dynamics summaries before acting on the decision. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [markdown, guidance] <br>
**Output Format:** [Markdown structured as an audit summary with Gate 1-4 findings, failure modes, a Go/Hold/Kill decision, and data gaps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only output based on user-provided modeling and simulation results] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
