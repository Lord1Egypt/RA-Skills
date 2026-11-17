## Description:

EVE is a persistent AI research supervisor agent with Auto, Semi-Manual, and Manual modes for managing a research lifecycle from literature search to publication-ready LaTeX paper drafting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[amzayn](https://clawhub.ai/user/amzayn)

### License/Terms of Use:

MIT-0

## Use Case:

External researchers, students, and developers use this agent to organize literature discovery, gap analysis, research-idea generation, experiment planning, citation management, and LaTeX paper drafting across multi-session projects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credentials and research content may be sent to a non-official LLM endpoint.

Mitigation: Review the code before installing, configure a trusted LLM endpoint, and do not reuse an official OpenAI API key with the default api.openai-hk.com endpoint unless that operator is explicitly trusted.

Risk: Research profiles, notes, project details, and server configuration are kept as long-lived local memory files.

Mitigation: Avoid storing sensitive material unless needed, restrict local file access, and manually clear the memory directory when retention is no longer appropriate.

Risk: SSH monitoring features can automate remote server access and were flagged for unsafe host-key checking, command validation, and path handling.

Mitigation: Avoid using those features on sensitive servers until the SSH behavior is reviewed and fixed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/amzayn/skills/eve-research-supervisor-pro)
- [Artifact README](artifact/README.md)
- [Artifact Skill Instructions](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and text guidance with generated files such as LaTeX, BibTeX, JSON, plots, tables, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include persistent local research memory, downloaded paper metadata, research notes, gap lists, ideas, roadmaps, and publication drafts.]

## Skill Version(s):

5.1.0 (source: server release evidence, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
