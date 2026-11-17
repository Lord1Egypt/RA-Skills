## Description:

AI-powered research advisor for graduate students - provides research assessment, proposal generation, literature analysis, advisor matching, and publication guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhenstaff](https://clawhub.ai/user/zhenstaff)

### License/Terms of Use:

MIT

## Use Case:

Graduate students and researchers use this skill to assess research ideas, draft proposal materials, analyze literature, find advisor or lab matches, plan papers, and identify academic resources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional OCR and PDF features may require additional system packages.

Mitigation: Install only the documented optional dependencies needed for the user's workflow and verify they come from trusted package sources.

Risk: Research ideas, unpublished papers, PDFs, and academic profile details may be sensitive.

Mitigation: Avoid sharing confidential research material with external integrations unless data handling is understood and approved.

Risk: Generated assessments, advisor matches, and resource recommendations may be incomplete or outdated.

Mitigation: Use the output as planning guidance and validate important academic decisions with human mentors, current venue information, and official program resources.

Risk: File export or save operations could write to an unintended path.

Mitigation: Confirm destination paths with the user before saving or exporting generated materials.

## Reference(s):

- [Academic Mentor ClawHub Skill Page](https://clawhub.ai/zhenstaff/skills/academic-mentor)
- [Academic Mentor Project Homepage](https://github.com/ZhenRobotics/openclaw-academic-mentor)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with optional Python examples, shell commands, structured scores, outlines, proposals, and ranked recommendations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include generated research assessments, proposal sections, literature summaries, advisor matches, paper outlines, resource recommendations, and file export guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter and README state 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
