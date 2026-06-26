## Description: <br>
Cn Json Tools helps agents format, compare, extract, minify, and validate JSON with Chinese-first user-facing output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freedompixels](https://clawhub.ai/user/freedompixels) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to inspect API responses, compare JSON configuration files, extract fields from nested JSON, compact JSON for configuration use, and validate JSON syntax. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is flagged as requiring sensitive credentials in server evidence, and the security guidance limits use to contexts where the associated maintenance workflows make sense. <br>
Mitigation: Install and run it only in trusted ClawHub/Convex maintainer contexts, and review moderation, deployment, or proof-publishing commands before use. <br>
Risk: Formatting, extraction, and diff commands can read local JSON files and print their contents or derived values to the terminal. <br>
Mitigation: Use the tool on trusted local files, avoid unnecessary processing of secrets or personal data, and redact sensitive values before sharing output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/freedompixels/cn-json-tools) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON or plain-text command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local Python standard-library JSON parsing; diff, format, extract, minify, and validate commands may print parsed JSON content to stdout.] <br>

## Skill Version(s): <br>
1.2.6 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
