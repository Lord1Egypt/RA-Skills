## Description: <br>
CoVerify helps agents and developers extract commitment kernels from text, compare transformations with Jaccard scoring, detect ghost-token leakage, and run model-swap consistency checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SunrisesIllNeverSee](https://clawhub.ai/user/SunrisesIllNeverSee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and agent operators use Coverify to check whether obligation-bearing language survived rewriting, compression, or cross-model processing. The skill is most useful for advisory drift analysis and local verification reports, not as standalone proof of governance compliance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can write local audit and model-swap report files that may contain prompt or signal text. <br>
Mitigation: Avoid running highly sensitive prompts unless local retention is acceptable, and review or clear the OpenClaw/MOSES state directories according to local policy. <br>
Risk: The artifact makes strong claims about proof, cryptographic scoring, and governance-grade meaning preservation, while evidence.security characterizes the classifications as advisory. <br>
Mitigation: Treat results as heuristic drift analysis and require human review or independent validation before using them for compliance or governance decisions. <br>


## Reference(s): <br>
- [Coverify on ClawHub](https://clawhub.ai/SunrisesIllNeverSee/coverify) <br>
- [Falsifiability Protocol](references/falsifiability.md) <br>
- [Ghost Token Specification](references/ghost-token-spec.md) <br>
- [Commitment Conservation DOI](https://zenodo.org/records/18792459) <br>
- [MOSES Website](https://mos2es.io) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON/text reports from local Python scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local audit and model-swap report files under OpenClaw/MOSES state directories when the scripts are run.] <br>

## Skill Version(s): <br>
0.4.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
