## Description: <br>
Use the frigatebird npm package to interact with X from the CLI with bird-style command parity, posting/reply/article support, and list automation without X API keys. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Oceanswave](https://clawhub.ai/user/Oceanswave) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to run bird-style X workflows from an agent, including reading timelines, posting, replying, publishing articles, and automating list changes through the frigatebird CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to act as a logged-in X account through browser cookies. <br>
Mitigation: Use a dedicated browser profile or test account and do not expose raw cookies or tokens in prompts, logs, or shared artifacts. <br>
Risk: Commands can perform public account-changing actions such as posting, replying, following, liking, retweeting, or changing lists. <br>
Mitigation: Require explicit user confirmation before running any account-changing frigatebird command. <br>
Risk: The workflow depends on an external npm package and X web UI behavior, which can change or drift. <br>
Mitigation: Verify the installed npm package source and version before use, and run read-only checks such as `frigatebird check` and `frigatebird whoami` before mutation workflows. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and CLI options] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include JSON-output flags for scripted CLI reads; account-changing commands should require explicit user confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
