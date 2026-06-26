## Description: <br>
Pulls published blog posts from Substack and Ghost into an Obsidian or Logseq vault for AI-assisted repurposing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liverock](https://clawhub.ai/user/liverock) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Writers, developers, and content operators use this skill to sync published Substack or Ghost posts into local Obsidian or Logseq Markdown vaults so an agent can summarize, remix, or plan follow-up content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Ghost support stores a powerful API key in a local JSON config. <br>
Mitigation: Use a dedicated or least-privileged Ghost key when possible, keep the config file private, avoid printing config in captured logs, and test against a backed-up or dedicated vault before syncing important notes. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands, Configuration] <br>
**Output Format:** [Markdown files with Obsidian YAML frontmatter or Logseq properties, plus markdown command output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes synced posts under a Ghost-Writer folder in the configured local vault and stores source settings in a local JSON config.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
