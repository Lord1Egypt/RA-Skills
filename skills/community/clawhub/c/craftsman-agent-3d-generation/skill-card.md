## Description:

Turns prompts or reference images into LEGO or Minecraft 3D assembly build plans through the Craftsman Agent API using OneKey Gateway or a local server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ai-hub-admin](https://clawhub.ai/user/ai-hub-admin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to generate LEGO or Minecraft build plans, part inventories, assembly-step image URLs, and client calls for the Craftsman Agent endpoints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses API credentials and may send prompts or reference image URLs to an external Craftsman Agent endpoint.

Mitigation: Use a scoped throwaway API key, avoid private prompts or reference URLs, and review requests before running the scripts.

Risk: The installation guidance includes unpinned npm and Python dependency installs.

Mitigation: Pin and review dependency versions before deployment in managed or commercial environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ai-hub-admin/skills/craftsman-agent-3d-generation)
- [Craftsman Agent API endpoint](https://agent.deepnlp.org/agent)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [API responses can include image URLs, inventory lists, inventory visuals, and ordered assembly-step image URLs.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
