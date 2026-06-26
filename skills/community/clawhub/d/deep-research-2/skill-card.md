## Description: <br>
This skill helps agents perform comprehensive research, deep investigation, and detailed academic-style reporting on complex topics, producing multi-thousand word markdown reports with extensive citations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kongyo2](https://clawhub.ai/user/kongyo2) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Researchers, analysts, developers, and other agent users use this skill when they need a structured, source-grounded research report rather than a brief answer. It guides the agent through topic decomposition, staged web research, source evaluation, citation management, section drafting, and final markdown report assembly. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Research scope can expand significantly because the skill emphasizes exhaustive investigation, multilingual search, and several-thousand-word reports. <br>
Mitigation: Set clear limits on topic scope, browsing depth, source types, languages, and output length before invoking the skill. <br>
Risk: The workflow may create intermediate markdown draft files when local drafting is permitted. <br>
Mitigation: Confirm the workspace and file-writing permissions before allowing the agent to create or assemble draft files. <br>
Risk: Long-form research can still contain incorrect, stale, or poorly verified claims if source access or cross-checking is incomplete. <br>
Mitigation: Require direct source access, cross-verification of critical claims, and a complete references section for delivered reports. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/kongyo2/deep-research-2) <br>
- [Research Methodology](references/research_methodology.md) <br>
- [Citation Guidelines](references/citation_guidelines.md) <br>
- [Report Template](assets/report_template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown research reports with inline citations and a references section] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include intermediate markdown draft files when the agent is allowed to create local drafts.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
