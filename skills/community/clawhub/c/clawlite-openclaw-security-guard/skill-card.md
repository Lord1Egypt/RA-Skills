## Description:

OpenClaw Security Guard helps agents run lightweight local checks for prompt injection, secret leakage, risky shell commands, SSRF-prone URLs, sensitive paths, and unsafe skill install or publish flows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[x-rayluan](https://clawhub.ai/user/x-rayluan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill publishers use this skill to preflight agent workflows, commands, URLs, paths, and skill folders for common security red flags before install, automation, or ClawHub publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security evidence says helper scripts can write outside expected locations.

Mitigation: Run the skill in a controlled workspace and only use the hook installer or Obsidian writer when the destination path and note title are intentional and controlled.

Risk: Security evidence says the prepublish guard can be bypassed and should not be the sole publish or install gate.

Mitigation: Treat WARN and BLOCK findings as review triggers, inspect flagged lines manually, and use runtime isolation or additional review for high-risk skills.

Risk: Artifact behavior relies on lightweight regex detection for common secret, command, URL, and path risks.

Mitigation: Use the checks as a preflight filter, not a safety proof, and escalate uncertain or high-impact automation to human security review.

## Reference(s):

- [Security Guard Checklist](references/checklist.md)
- [ClawHub Skill Page](https://clawhub.ai/x-rayluan/skills/clawlite-openclaw-security-guard)

## Skill Output:

**Output Type(s):** [Text, JSON, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown guidance with inline shell commands; bundled scripts emit JSON audit/check results and can write Markdown audit notes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Lightweight regex-based checks return ALLOW, WARN, or BLOCK verdicts; clean results do not prove safety.]

## Skill Version(s):

0.2.1 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
