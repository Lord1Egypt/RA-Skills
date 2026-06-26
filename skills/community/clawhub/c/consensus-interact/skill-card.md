## Description: <br>
Use the open-source @consensus-tools/consensus-tools engine to run multi-LLM policy-based decision workflows: post jobs, collect submissions, cast votes, and resolve outcomes with customizable consensus logic gates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaicianflone](https://clawhub.ai/user/kaicianflone) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and external agent operators use this skill to run consensus.tools workflows that post jobs, collect submissions, cast votes, resolve outcomes, and fetch final decisions from local-first or explicitly configured hosted boards. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Hosted or global board mode can transmit job inputs, submissions, votes, or results to a remote consensus.tools service. <br>
Mitigation: Use local mode for sensitive work unless the hosted service is explicitly trusted, and do not send secrets, private documents, or regulated data without reviewing privacy and retention terms. <br>
Risk: Mutating workflows can post jobs, create submissions, cast votes, or resolve outcomes when network side effects and optional tools are enabled. <br>
Mitigation: Keep network side effects disabled and require opt-in for optional mutating tools until the operator intentionally enables those actions for the deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kaicianflone/consensus-interact) <br>
- [consensus.tools API reference](references/api.md) <br>
- [consensus.tools jobs guide](JOBS.md) <br>
- [@consensus-tools/consensus-tools npm package](https://www.npmjs.com/package/@consensus-tools/consensus-tools) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference optional local or hosted consensus.tools workflows; hosted mutations require explicit configuration.] <br>

## Skill Version(s): <br>
1.0.9 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
