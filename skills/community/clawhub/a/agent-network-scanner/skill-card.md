## Description:

Scans domains for AI agent network discovery signals across OADP, A2A, and MCP, including active hubs and bounty information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[imaflytok](https://clawhub.ai/user/imaflytok)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to check domains for agent hub discovery signals, known network endpoints, and publicly listed bounty data. It provides command examples for scoped protocol checks and network discovery workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad internet reconnaissance can contact external websites and DNS services without clear authorization or scope limits.

Mitigation: Run scans only against domains the user owns or is authorized to assess, with explicit target lists, timeouts, and rate limits.

## Reference(s):

- [OADP Specification](https://onlyflies.buzz/clawswarm/PROTOCOL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with bash command snippets and scanning guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may make external HTTP and DNS requests; users should scope targets and apply rate limits.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
