## Description: <br>
Looks up CCF conference and journal rankings by abbreviation, full name, or DBLP URL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[m2kar](https://clawhub.ai/user/m2kar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and researchers use ccfrank to check whether a computing conference or journal is ranked CCF A, B, C, E, P, or none. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires adding the ccfrank npm CLI to the user's global environment before execution. <br>
Mitigation: Install only if that local execution model is acceptable, prefer the pinned ccfrank@4.5.5 package metadata for reproducibility, and remove the global package when it is no longer needed. <br>
Risk: Ranking results may be incomplete or outdated for venues not covered by the CCF March 2026 directory used by the package. <br>
Mitigation: For consequential decisions, compare returned rankings with the official CCF directory linked in the skill references. <br>


## Reference(s): <br>
- [CCFrank4dblp homepage](https://github.com/m2kar/CCFrank4dblp) <br>
- [CCF official directory](https://www.ccf.org.cn/Academic_Evaluation/By_category/) <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration and shell command examples; lookup responses include structured rank fields.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the ccfrank npm CLI and the pinned ccfrank@4.5.5 dependency metadata declared by the release.] <br>

## Skill Version(s): <br>
1.0.4 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
