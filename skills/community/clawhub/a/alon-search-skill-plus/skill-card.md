## Description: <br>
Search agent skills across trusted directories, ClawHub, and GitHub adaptation candidates with explicit ranking and safety filters. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alondotsh](https://clawhub.ai/user/alondotsh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to find existing agent skills before building one from scratch. It produces ranked, source-labeled recommendations and separates ready-to-use skills from GitHub repositories that may need adaptation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recommendations from ClawHub, aggregators, or GitHub repositories may point to third-party skills or install commands that have not been independently verified. <br>
Mitigation: Treat recommendations as leads and review any suggested skill, repository, npx command, or npm install before running it. <br>
Risk: Search results can overstate readiness if ordinary GitHub repositories are treated like packaged skills. <br>
Mitigation: Keep ready-to-use skills separate from adaptable repositories and verify standard skill packaging before presenting an item as installable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/alondotsh/alon-search-skill-plus) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown ranked shortlist with source labels, safety notes, and install or adaptation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes search keywords used, quality signals such as stars and recency when available, and separate sections for lower-trust or adaptable results.] <br>

## Skill Version(s): <br>
0.1.4 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
