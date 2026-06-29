## Description: <br>
古人诗词大师 helps agents answer classical Chinese poetry questions, generate poems in selected traditional styles, analyze form and imagery, explain allusions, compare poets, and produce interactive poetry knowledge graphs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bettermen](https://clawhub.ai/user/bettermen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to support classical Chinese poetry education, creative drafting, literary analysis, allusion lookup, and relationship visualization across poets, dynasties, schools, and themes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may activate on broad poetry-related terms. <br>
Mitigation: Confirm the user's intent before routing ambiguous general poetry requests into classical Chinese poetry workflows. <br>
Risk: Generated graph HTML loads D3 from d3js.org when viewed. <br>
Mitigation: Review the generated HTML before sharing or opening it in restricted environments, and account for the external D3 dependency. <br>


## Reference(s): <br>
- [Poet Data](references/poets.json) <br>
- [Classical Chinese Poetry Forms](references/forms.md) <br>
- [Poetry Allusions Reference](references/allusions.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/bettermen/ancient-poetry-master) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown, JSON analysis output, and generated HTML graph files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Graph output is an HTML file that loads D3 from d3js.org when viewed.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
