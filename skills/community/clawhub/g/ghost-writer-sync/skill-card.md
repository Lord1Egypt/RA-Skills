## Description:

Pulls published blog posts from Substack and Ghost into an Obsidian or Logseq vault for AI-assisted repurposing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liverock](https://clawhub.ai/user/liverock)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators and developers use this skill to configure an agent to fetch published Substack or Ghost posts, convert them to Markdown, and place them in an Obsidian or Logseq vault for repurposing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Ghost Admin credentials may be exposed or over-scoped when stored in configuration or displayed in logs.

Mitigation: Use a dedicated, revocable Ghost integration key, keep configuration out of shared or synced folders, and avoid displaying configuration where logs are captured.

Risk: Untrusted blog sources can introduce misleading or unsafe content into the local vault for downstream AI repurposing.

Mitigation: Configure only trusted HTTPS sources and review synced Markdown before using it in downstream AI workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liverock/skills/ghost-writer-sync)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, files]

**Output Format:** [Markdown files with Obsidian YAML frontmatter or Logseq properties, plus Markdown command output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes posts under a Ghost-Writer directory in the configured vault; Ghost sources require an API key.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
