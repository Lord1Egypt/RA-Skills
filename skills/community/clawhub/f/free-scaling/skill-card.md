## Description: <br>
$0 test-time scaling with online learning. Classify, generate, and verify using free model ensembles. Models self-select via ELO scoring and A/B testing from deployment data, with 13 NIM models and an optional Copilot backend. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[isotrivial](https://clawhub.ai/user/isotrivial) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to route classification, generation, verification, batch evaluation, health checks, and model-panel evolution through free NVIDIA NIM model ensembles, with optional GitHub Copilot-backed models for selected workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and context may be sent to NVIDIA NIM and, when Copilot aliases or hybrid audit workflows are used, to GitHub Copilot. <br>
Mitigation: Review provider policies before use and avoid submitting secrets, regulated data, or sensitive customer content unless that data path is approved. <br>
Risk: The optional Copilot backend can reuse local OpenClaw or GitHub credential files. <br>
Mitigation: Use Copilot-backed models only in environments where local credential reuse is acceptable, and isolate or remove Copilot token files after use when required. <br>
Risk: ELO and feedback features store recent inference history and feedback metadata in local cache files. <br>
Mitigation: Configure an isolated FREE_SCALING_STATE_DIR for sensitive workflows and clear the free-scaling cache after use when retention is not desired. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/isotrivial/free-scaling) <br>
- [NVIDIA Build](https://build.nvidia.com) <br>
- [Source repository mentioned in artifact](https://github.com/isotrivial/free-scaling.git) <br>
- [README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command examples; runtime APIs can return text, JSON-like result objects, and status dictionaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call external NVIDIA NIM endpoints and optional GitHub Copilot endpoints; local ELO and feedback state may be written under the configured free-scaling cache directory.] <br>

## Skill Version(s): <br>
3.3.1 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
