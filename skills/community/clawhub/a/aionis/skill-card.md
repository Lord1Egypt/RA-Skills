## Description:

Connect OpenClaw to Aionis using write/context/policy/feedback memory loop APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cognary](https://clawhub.ai/user/cognary)

### License/Terms of Use:


## Use Case:

Developers and agents use Aionis to connect OpenClaw workflows to an Aionis memory service for long-term memory writes, contextual retrieval, policy-based tool routing, and feedback loops.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic bootstrap can start a persistent local Docker service from a container image.

Mitigation: Install only when the Aionis container source is trusted, prefer digest-pinned images, review or disable automatic bootstrap, and stop or remove the container and volume when no longer needed.

Risk: Runtime credential files can contain local API keys or tokens.

Mitigation: Protect `.runtime` files with restrictive permissions, avoid sourcing untrusted environment files, and never print full secrets in responses.

Risk: Memory workflows can retain sensitive or overly broad tool output.

Mitigation: Keep scope fixed per project, store concise summaries instead of raw dumps, and set bounded limits for recall and context assembly.

## Reference(s):

- [Aionis OpenClaw integration documentation](https://doc.aionisos.com/public/en/integrations/04-openclaw)
- [Aionis ClawHub skill page](https://clawhub.ai/cognary/skills/aionis)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code]

**Output Format:** [Markdown guidance with bash commands and JSON request templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses should include relevant request, commit, decision, run, base URL, and scope identifiers when present.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata and user-provided changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
