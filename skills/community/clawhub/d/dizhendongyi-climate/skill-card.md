## Description: <br>
Provides local Python scripts and agent guidance for experimental orbital-scale climate modeling, near-term scenario comparison, East Asian monsoon projection, paleoclimate replay, and extreme-event warning exploration. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[zxfei420](https://clawhub.ai/user/zxfei420) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and climate-research users can use this skill to run local experimental climate-model scripts, compare RCP scenarios, inspect orbital and FEBE assumptions, and draft explanatory analysis. Outputs are for research and review, not policy, planning, safety, or operational climate decisions unless independently validated. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contains overstated scientific claims and produces experimental climate-model outputs that could be mistaken for operational guidance. <br>
Mitigation: Treat outputs as illustrative research material and independently validate any result before using it for policy, planning, safety, or operational climate decisions. <br>
Risk: The bundled scripts depend on an unpinned numpy package. <br>
Mitigation: Install and run the skill in a virtual environment and review dependency versions before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zxfei420/dizhendongyi-climate) <br>
- [Core theory](references/core_theory.md) <br>
- [Orbital parameter formulas](references/orbital_data.md) <br>
- [Extreme-event warning framework](references/extreme_events.md) <br>
- [Model verification cases](references/verification.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell-command examples; local scripts emit terminal text and structured Python data.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python with numpy; climate outputs should be reviewed as illustrative research material.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
