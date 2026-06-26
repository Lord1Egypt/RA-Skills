## Description: <br>
Monitor blogs and RSS/Atom feeds for updates using the blogwatcher CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MemoryF](https://clawhub.ai/user/MemoryF) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to install and run the blogwatcher CLI for tracking blog and RSS/Atom feed updates, scanning for new articles, and managing read state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The install command fetches the latest version of an external Go module, which can change over time. <br>
Mitigation: Pin the Go module to a reviewed version when reproducibility or change control is required. <br>
Risk: Scanning feeds sends network requests to the blog and RSS/Atom URLs configured by the user. <br>
Mitigation: Configure only trusted feed URLs and review network access expectations before use in restricted environments. <br>


## Reference(s): <br>
- [Blogwatcher Project](https://github.com/Hyaxia/blogwatcher) <br>
- [Blogwatcher Moss on ClawHub](https://clawhub.ai/MemoryF/blogwatcher-moss) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and example CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces CLI usage guidance; the blogwatcher tool itself performs network requests to configured feeds.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
