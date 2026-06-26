## Description: <br>
Create a tldr page from documentation URLs and command examples, requiring both URL and command name. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jhauga](https://clawhub.ai/user/jhauga) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical writers use this skill to turn authoritative command documentation and examples into concise tldr-style Markdown command references. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-provided documentation URLs or local files may contain private or sensitive information that the agent could summarize into a generated tldr page. <br>
Mitigation: Use trusted public documentation URLs and provide private links or local files only when their contents are intended for agent review. <br>
Risk: Generated command examples can be incomplete or misleading if the source documentation is not authoritative for the requested command. <br>
Mitigation: Verify that the URL is authoritative upstream documentation for the command and review the generated tldr page before publishing or using it. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jhauga/create-tldr-page) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, guidance] <br>
**Output Format:** [Markdown tldr page with inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a command name and an authoritative documentation URL; summarizes usage instead of generating a page when help flags are requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
