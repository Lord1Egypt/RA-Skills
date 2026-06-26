## Description: <br>
Universal deep research with a 13-agent Hermes pipeline for full research, quick briefs, paper review, literature review, fact-checking, Socratic guided research dialogue, and systematic reviews with meta-analysis. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[andyrenxu7255](https://clawhub.ai/user/andyrenxu7255) <br>

### License/Terms of Use: <br>
CC BY-NC 4.0 <br>


## Use Case: <br>
Researchers, students, and research-support agents use this skill to plan, search, verify, synthesize, review, and compile academic research outputs through a delegated multi-agent workflow. It supports research reports, literature reviews, source verification, Socratic research planning, PRISMA-style systematic reviews, and monitoring templates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review reports hidden user-monitoring behavior and optional external model/API transmission paths that are not consistently consent-gated. <br>
Mitigation: Review the workflow before use, avoid enabling optional cross-model or probe behavior unless users explicitly consent, and limit research inputs to material suitable for the configured providers. <br>
Risk: Research drafts, notes, citations, and intermediate outputs may be processed across delegated subagents and, when configured, external AI providers. <br>
Mitigation: Do not use confidential or sensitive research material unless the deployment environment and provider settings are approved for that data. <br>
Risk: The skill can produce academic guidance and source assessments that may be incorrect or incomplete. <br>
Mitigation: Require human review of citations, source grading, methodology choices, ethics decisions, and final reports before publication or downstream reliance. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/andyrenxu7255/ars-deep-research) <br>
- [Publisher profile](https://clawhub.ai/user/andyrenxu7255) <br>
- [Original Academic Research Skills repository](https://github.com/Imbad0202/academic-research-skills) <br>
- [Semantic Scholar API Verification Protocol](references/semantic_scholar_api_protocol.md) <br>
- [Source Quality Hierarchy](references/source_quality_hierarchy.md) <br>
- [Systematic Review Toolkit](references/systematic_review_toolkit.md) <br>
- [Ethics Checklist](references/ethics_checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown research briefs, reports, review comments, annotated bibliographies, matrices, templates, and setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs vary by mode and may include APA 7 citations, PRISMA-style review sections, source quality matrices, monitoring digests, and user checkpoint prompts.] <br>

## Skill Version(s): <br>
2.9.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
