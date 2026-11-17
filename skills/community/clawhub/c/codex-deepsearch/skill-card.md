## Description:

Guides Codex through deep, source-backed research with local, web, and user-provided evidence separation, tool-limit disclosure, source and claim ledgers, review gates, privacy-safe repository handling, and optional worker delegation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shaoqing404](https://clawhub.ai/user/shaoqing404)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and research-focused agents use this skill to plan, conduct, review, and hand off evidence-heavy research that may become a specification, roadmap, product decision, PRD, or engineering input.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may guide an agent to read local project files, browse current sources, create research documents, or delegate work when permitted.

Mitigation: Apply the skill's stated privacy boundaries, require explicit authorization for private or ignored files, and keep the main agent responsible for final review and acceptance.

Risk: The inspected artifact references supporting files under references/ and templates/ that are not included in the artifact.

Mitigation: Review the missing referenced materials before relying on those detailed workflows, templates, or review gates.

Risk: Research outputs can contain stale, snippet-only, or insufficiently verified claims.

Mitigation: Use source and claim ledgers, label claim reliability, disclose tool limits, check counter-evidence, and surface unresolved gaps in the final status.

## Reference(s):

- [Server-resolved GitHub provenance](https://github.com/shaoqing404/codex-deepsearch/tree/main/plugins/codex-deepsearch/skills/codex-deepsearch)
- [ClawHub skill page](https://clawhub.ai/shaoqing404/skills/codex-deepsearch)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, ledgers, checkpoints, implementation guidance, and status labels]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include DONE, DONE_WITH_CONCERNS, NEEDS_CONTEXT, or BLOCKED status labels and explicit uncertainty notes.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
