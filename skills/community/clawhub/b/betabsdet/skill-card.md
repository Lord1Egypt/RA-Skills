## Description: <br>
Detects key claims in long messages and summarizes the real point. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1477009639zw-blip](https://clawhub.ai/user/1477009639zw-blip) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, reviewers, and developers use this skill to analyze verbose messages, identify filler language, and extract the practical point or ask. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Input files or pasted text may contain sensitive information that the local script reads and prints in terminal output. <br>
Mitigation: Run it only on text you intend to analyze locally, and remove secrets or sensitive content before use. <br>
Risk: The verdict and extracted point are heuristic summaries and may omit context or misclassify persuasive language. <br>
Mitigation: Treat the output as a review aid and compare it with the original message before making decisions. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Plain text terminal output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads user-provided text or a local text file and prints a verdict, extracted real point, and message statistics.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
