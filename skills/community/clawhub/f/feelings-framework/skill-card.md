## Description: <br>
Provides OpenClaw agents with persistent emotional states, tracking mood and feelings over time to influence response tone and behavior consistently. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[blaspat](https://clawhub.ai/user/blaspat) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers integrating OpenClaw or other agents use this skill to persist mood and feeling state across sessions and generate tone modifiers that shape agent responses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can retain inferred mood, feeling intensities, timestamps, session counts, and trigger counts across sessions. <br>
Mitigation: Store mood files in a protected workspace and clear or disable the memory backend when retained interaction-derived state is not desired. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/blaspat/feelings-framework) <br>
- [README.md](README.md) <br>
- [CORE.md](CORE.md) <br>
- [SKILL.md](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and JavaScript code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces response modifier values and serialized local mood state through the included libraries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, pyproject.toml, setup.py, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
