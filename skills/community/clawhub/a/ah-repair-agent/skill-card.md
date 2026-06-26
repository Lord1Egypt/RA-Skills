## Description: <br>
RepairAgent helps agents diagnose software defects, localize likely root causes, generate patch hypotheses, and validate fixes through tests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mtsatryan](https://clawhub.ai/user/mtsatryan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use RepairAgent to guide automated bug repair workflows, from fault localization and hypothesis generation through patch creation, validation, and final fix recommendation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated patches or repair guidance could introduce incorrect behavior, especially in security-sensitive or deployment-related code. <br>
Mitigation: Use the skill on repositories you control, keep version-control rollback available, review diffs before accepting changes, and run the relevant test suite before deployment. <br>


## Reference(s): <br>
- [RepairAgent code examples](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown with diagnostic summaries, ranked findings, patch explanations, validation results, and code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include confidence scores, test outcomes, and final fix recommendations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
