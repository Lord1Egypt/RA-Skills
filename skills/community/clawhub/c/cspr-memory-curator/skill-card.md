## Description: <br>
Updates CSPR preference memory from accumulated feedback and recent newspaper outcomes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[happywalkers](https://clawhub.ai/user/happywalkers) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
CSPR users and their agents use this skill after feedback or several runs to maintain a conservative preference profile for topics, source preferences, and disliked patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Preference profile updates can affect future news selection, source visibility, and topic weighting. <br>
Mitigation: Review generated profile updates before applying them, especially changes involving hidden sources, disliked patterns, or long-term topic preferences. <br>
Risk: Overfitting to a single feedback action could make preferences too narrow. <br>
Mitigation: Keep updates conservative and base durable preference changes on accumulated feedback rather than one reaction. <br>


## Reference(s): <br>
- [CSPR Memory Curator on ClawHub](https://clawhub.ai/happywalkers/skills/cspr-memory-curator) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell command examples and YAML profile update instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a complete updated CSPR preference profile for review before applying with prefmem.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
