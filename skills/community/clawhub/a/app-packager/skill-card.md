## Description: <br>
Automatically switches Git branches and runs app packaging workflows for Android, iOS, or combined builds with optional upload settings and completion reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Heigher](https://clawhub.ai/user/Heigher) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and release engineers use this skill to package mobile apps from a selected Git branch, choose platform and build type, optionally upload the build, and receive a result summary. It is intended for packaging workflows, not code merging, committing, unit testing, or code checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles upload credentials and its documented feedback can echo an API key into chat. <br>
Mitigation: Do not paste live Pgyer API keys into chat unless transcript exposure is acceptable; redact API keys from output before routine use. <br>
Risk: The skill changes Git branches and runs local packaging scripts on a fixed project path. <br>
Mitigation: Confirm the intended local project, branch, and working tree before execution, and inspect the packaging script before relying on the build result. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Heigher/app-packager) <br>
- [Publisher profile](https://clawhub.ai/user/Heigher) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and build result summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include generated package paths, elapsed time, branch status, error summaries, and optional upload links.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
