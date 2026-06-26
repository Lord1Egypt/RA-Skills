## Description: <br>
Analyzes Android project Git changes to find resource files such as drawables, layouts, strings, and colors that may no longer be used, then checks whether those resources are still referenced elsewhere in the project. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[opoojkk](https://clawhub.ai/user/opoojkk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Android developers and engineers use this skill to review staged, unstaged, or recent Git changes and identify resource files that may be safe to remove after manual confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Text-based resource analysis can misclassify resources as unused when references are dynamic, reflective, generated, or located across modules. <br>
Mitigation: Treat results as a review checklist, inspect each suggested file, consider dynamic and cross-module references, and build/test before deleting resources. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/opoojkk/android-unused-resource-cleanup) <br>
- [Publisher profile](https://clawhub.ai/user/opoojkk) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown-style terminal report with suggested shell delete commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports candidate removable resources, resources to keep, referenced file paths, and manual verification guidance.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
