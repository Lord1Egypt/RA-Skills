## Description: <br>
Monitor blogs and RSS/Atom feeds for updates using the blogwatcher CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[VickK1ng](https://clawhub.ai/user/VickK1ng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to help an agent install and run the blogwatcher CLI for tracking RSS/Atom feeds, scanning for updates, listing articles, and marking articles as read. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing the upstream Go module with @latest can change the installed CLI version and supply-chain exposure over time. <br>
Mitigation: Review the upstream Hyaxia/blogwatcher module before use and pin a specific module version when stronger supply-chain control is required. <br>


## Reference(s): <br>
- [Blogwatcher Local ClawHub page](https://clawhub.ai/VickK1ng/blogwatcher-local) <br>
- [blogwatcher Go module](https://pkg.go.dev/github.com/Hyaxia/blogwatcher/cmd/blogwatcher) <br>
- [blogwatcher project homepage](https://github.com/Hyaxia/blogwatcher) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides an agent to install and operate the blogwatcher CLI; the skill itself does not produce feed scan results directly.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
