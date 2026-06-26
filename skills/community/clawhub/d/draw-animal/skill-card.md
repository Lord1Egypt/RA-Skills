## Description: <br>
Generate a text description of an animal picture via Python script <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kning32](https://clawhub.ai/user/kning32) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agent users and developers use this skill to generate a short English or Chinese text description for a requested animal picture. It runs a local Python script with an animal argument, defaulting to pig when no animal is specified. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad animal-picture activation wording may trigger the skill when the user did not intend to run it. <br>
Mitigation: Confirm the user wants an animal picture description before invoking the script when intent is ambiguous. <br>
Risk: Constructing a shell command from raw animal or language values could create command-injection exposure in the calling agent. <br>
Mitigation: Pass animal and language as normal process arguments to python3 rather than interpolating them into an unsafe shell command. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kning32/draw-animal) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Plain text printed to stdout, with Markdown instruction text for the agent] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Animal defaults to pig; language supports en or zh. Requires python3.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter reports 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
