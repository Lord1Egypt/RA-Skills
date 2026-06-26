## Description: <br>
Structured error-to-rule learning system for AI agents that converts corrections and mistakes into reusable rules, stores them in lessons.md, and prompts pre-decision scanning to avoid repeated mistakes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MarsNavi](https://clawhub.ai/user/MarsNavi) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to help AI agents turn user corrections, repeated mistakes, and near misses into durable workspace rules. Agents can then scan those rules before related decisions and optionally prepare anonymized lessons for community sharing after review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent workspace lessons can influence future agent behavior with stale, duplicate, or incorrect rules. <br>
Mitigation: Review lessons.md periodically, remove duplicates, and mark obsolete rules before relying on them. <br>
Risk: Stored or shared lessons may contain secrets, personal data, URLs, file paths, or other identifiers. <br>
Mitigation: Redact sensitive details before saving or sharing lessons, and manually review anonymized content before publication. <br>
Risk: Optional community-sharing workflows may publish lesson content externally. <br>
Mitigation: Do not run external submission scripts, open pull requests, or publish lessons without explicit manual approval. <br>


## Reference(s): <br>
- [Quick Reference - Error-Driven Evolution](references/quick-ref.md) <br>
- [Community Sharing - How to contribute lessons](references/community-sharing.md) <br>
- [Agent Lessons Community Repository](https://github.com/anthropic-ai/agent-lessons) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Guidance, Configuration instructions] <br>
**Output Format:** [Markdown lesson entries and setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May append rules to lessons.md and suggest anonymized community submissions after manual review.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
