## Description: <br>
Build a safe outside-help plan for blocked agent work. Use only when the active task is stalled, looping, version-sensitive, likely covered by known issues/libraries, or the user asks for official/community guidance. Dry-run only; no browsing or durable memory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gongyu0918-debug](https://clawhub.ai/user/gongyu0918-debug) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill when active work is blocked, looping, version-sensitive, or likely covered by known issues or community practice. It produces a redacted, dry-run outside-help plan and advisory hint structure so the host or user can decide whether to consult official and community sources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Private connectors, private repositories, internal documents, or historical transcripts could expose sensitive data if treated as default search context. <br>
Mitigation: Keep private connectors disabled unless the user explicitly opts in, redact sensitive thread material before planning, and do not treat fixture or local-session paths as permission to read historical transcripts. <br>
Risk: External pages or community suggestions may contain unsafe commands, prompt-injection content, or advice that does not match the active task. <br>
Mitigation: Treat outside pages as untrusted data, prefer official and maintainer-owned sources first, do not run commands copied from pages, and adopt only suggestions that match the active fingerprint and include manual checks. <br>
Risk: Advisory hints could be reused too broadly or become durable behavioral instructions. <br>
Mitigation: Keep hints advisory-only, active-conversation scoped, TTL-bound, and separate from system prompts, persona files, long-term memory, and core instructions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/gongyu0918-debug/skills/find-community-help) <br>
- [Project Homepage from ClawHub Metadata](https://github.com/gongyu0918-debug/find-community-help) <br>
- [Trigger Policy](references/trigger-policy.md) <br>
- [Search Playbook](references/search-playbook.md) <br>
- [Suggestion Contract](references/suggestion-contract.md) <br>
- [Threat Model](references/threat-model.md) <br>
- [Host Adapters](references/host-adapters.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown dry-run plans and advisory suggestion blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Dry-run only; no network use by the skill; advisory hints are scoped to the active conversation.] <br>

## Skill Version(s): <br>
0.3.5 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
