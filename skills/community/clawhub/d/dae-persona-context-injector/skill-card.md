## Description: <br>
Build a reusable persona profile for AI agents before planning, writing, coding, research, or advisory work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sirsws](https://clawhub.ai/user/sirsws) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run a structured elicitation dialogue that produces a reusable PersonaProfile for downstream AI agents. It is intended for situations where agents need operator context before planning, coding, writing, research, or advisory work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated PersonaProfiles may contain sensitive personal context if users provide private details. <br>
Mitigation: Review and redact profile text or JSON before sharing it with another agent, service, repository, or public demo. <br>
Risk: A downstream agent may overuse incomplete or stale profile assumptions. <br>
Mitigation: Preserve evidence, confidence, and status markers, and update the profile when important user context changes. <br>
Risk: The elicitation flow may ask about topics a user does not want to disclose. <br>
Mitigation: Allow sensitive questions to be skipped and mark withheld or insufficient data explicitly rather than guessing. <br>


## Reference(s): <br>
- [DaE Skill Prompt](references/DaE_Skill_Prompt_en.md) <br>
- [DaE v2 Acceptance Criteria](references/DaE_v2_acceptance_criteria_en.md) <br>
- [Public Repository](https://github.com/sirsws/dae-persona-context-injector) <br>
- [Benchmark Write-up](https://github.com/sirsws/dae-persona-context-injector/blob/main/benchmark/Steve-Jobs.md) <br>
- [Benchmark Profile](https://github.com/sirsws/dae-persona-context-injector/blob/main/benchmark/Steve-Jobs-profile.md) <br>
- [Research Paper](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5961054) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Guidance] <br>
**Output Format:** [Human-readable profile brief and long-form PersonaProfile; JSON only when explicitly requested.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Major judgments include evidence, confidence, and status markers such as Confirmed, Inferred, UserWithheld, or Insufficient.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
