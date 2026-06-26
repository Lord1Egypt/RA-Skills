## Description: <br>
Guides agents through planning AI films, short dramas, cinematic sequences, and storyboard-driven video scenes with cross-shot continuity and film-language control. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hakityc](https://clawhub.ai/user/hakityc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and agents use this skill to turn shortform video ideas into continuity-aware preproduction assets, shot cards, review gates, bridge-frame choices, and chained shot prompts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Repository-specific paths and optional uv run aivideo commands may read project files or write a continuity ledger in the wrong AI-video project. <br>
Mitigation: Confirm the target project path and command arguments before using repository-specific workflow steps. <br>
Risk: AI video shot prompts can drift from locked identity, scene, prop, camera, or edit-continuity facts. <br>
Mitigation: Use the master-scene, shot-delta, bridge-frame, and final-clip gates before approving chained clips. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/hakityc/chain-referenced-shortform-video) <br>
- [Film Language For Chain-Referenced Shortform](references/film-language.md) <br>
- [Repo Mapping For Chain-Referenced Shortform](references/repo-mapping.md) <br>
- [Review Rubric For Chain-Referenced Shortform](references/review-rubric.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration, shell commands] <br>
**Output Format:** [Markdown guidance with structured shot cards, continuity ledgers, review rubrics, and optional shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No hidden execution; repository-specific commands should be reviewed before use.] <br>

## Skill Version(s): <br>
0.2.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
