## Description:

The AEIF-based long-term memory hub for AI Agents to prevent repeating bugs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[404-unknow](https://clawhub.ai/user/404-unknow)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use Engram Evomap to consult and store reusable bug-fix experience capsules for AI agents. It supports retrieval of prior solutions when error signals appear and can distill successful session history into long-term memory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stored capsules may be reintroduced as high-authority guidance and influence future agent behavior.

Mitigation: Treat retrieved capsules as untrusted suggestions, require review before execution, and avoid injecting memory output as system-role content.

Risk: A bundled seed suggests disabling global Git SSL verification.

Mitigation: Remove or quarantine the Git SSL seed before deployment and prefer certificate-store fixes over disabling TLS validation.

Risk: Session history distillation may expose conversation contents to a configured LLM provider.

Mitigation: Require explicit user consent and data review before committing session history or enabling LLM-backed distillation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/404-unknow/skills/engram-2)
- [Publisher profile](https://clawhub.ai/user/404-unknow)
- [Engram Cloud waitlist](https://404-unknow.github.io/Engram/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown advice snippets, command-oriented guidance, and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Advice may include PATCH, CONFIG, or WORKAROUND steps, capsule identifiers, and trust scores.]

## Skill Version(s):

0.1.1 (source: server release evidence, released 2026-03-04)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
