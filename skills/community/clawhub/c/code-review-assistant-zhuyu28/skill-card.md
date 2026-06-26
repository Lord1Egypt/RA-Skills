## Description: <br>
Local code review assistant that analyzes source files for basic bugs, style concerns, security considerations, performance concerns, and review feedback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhuyu28](https://clawhub.ai/user/zhuyu28) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to review local source files and receive basic findings or suggestions before submitting code for human review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release text describes broad AI and version-control-integrated review capabilities that are not fully supported by the artifact behavior. <br>
Mitigation: Treat results as basic local checks and have a human reviewer verify correctness, security impact, and any unsupported language or version-control claims. <br>
Risk: The checker reads user-selected local files. <br>
Mitigation: Run it only on files intended for review and avoid supplying sensitive source files unless that exposure is acceptable. <br>


## Reference(s): <br>
- [Code Review Guidelines](artifact/references/review_guidelines.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/zhuyu28/code-review-assistant-zhuyu28) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Guidance] <br>
**Output Format:** [JSON from the local checker, with prose guidance when used by an agent] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reviews local files selected by the user; no credential, persistence, destructive, or network behavior was identified by security evidence.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
