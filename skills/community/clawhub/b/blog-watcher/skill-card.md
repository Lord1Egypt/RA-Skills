## Description: <br>
Monitors blogs and websites for updates using RSS feeds and webpage change detection, with diff comparison, update summaries, and exclusion rules described in the release evidence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[534422530](https://clawhub.ai/user/534422530) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure an agent to watch RSS feeds or webpages and summarize detected blog or site updates. It is useful for tracking public content changes from user-specified sources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks the agent to fetch RSS feeds or webpages, which may include private, localhost, intranet, or otherwise sensitive URLs if a user adds them. <br>
Mitigation: Only add public or explicitly approved URLs, and avoid private or sensitive endpoints unless the agent is allowed to request and parse them from the current environment. <br>
Risk: Website and RSS content is external input and may be incorrect, stale, or intentionally misleading. <br>
Mitigation: Review detected updates and summaries before acting on them or forwarding them to other workflows. <br>


## Reference(s): <br>
- [Blog Watcher on ClawHub](https://clawhub.ai/534422530/blog-watcher) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown with Python and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces update summaries and example code for checking RSS feeds or webpage changes from user-provided URLs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter says 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
