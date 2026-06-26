## Description: <br>
ChangeBrief compares previous and current knowledge snapshots to surface important additions, changed claims, stale conclusions, decision-driving conflicts, and the top changes worth immediate action. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harrylabsj](https://clawhub.ai/user/harrylabsj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, managers, and operators use ChangeBrief to compare before-and-after document snapshots and quickly understand what materially changed, which prior conclusions are stale, and what needs attention now. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Change summaries can be wrong or incomplete if the supplied snapshots are stale, partial, or ambiguous. <br>
Mitigation: Review the generated brief against the original before and after documents before using it for decisions. <br>
Risk: Inputs may contain sensitive workplace, customer, roadmap, or policy information. <br>
Mitigation: Run the skill only on authorized materials and avoid including secrets or unnecessary personal data in snapshots. <br>
Risk: Workplace restructuring and employment-rights outputs are general guidance, not legal or HR advice. <br>
Mitigation: Verify facts and consult qualified HR, legal, or employee-support resources before acting on employment-related conclusions. <br>


## Reference(s): <br>
- [Change Signals](references/change-signals.md) <br>
- [ChangeBrief ClawHub Page](https://clawhub.ai/harrylabsj/skills/changebrief) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, guidance] <br>
**Output Format:** [Markdown or JSON change analysis] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local document-delta summaries from supplied before and after text or files.] <br>

## Skill Version(s): <br>
1.1.2 (source: SKILL.md frontmatter, package.json, clawhub.json, CHANGELOG, server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
