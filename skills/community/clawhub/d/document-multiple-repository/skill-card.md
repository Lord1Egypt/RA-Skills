## Description: <br>
Generates consolidated technical documentation for software systems made up of multiple local repositories, including frontend, backend, microservices, infrastructure, docs, and wikis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dannyxyz22](https://clawhub.ai/user/dannyxyz22) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering teams use this skill to analyze locally cloned multi-repository systems and generate consolidated architecture, repository map, deployment, process, README, API, code structure, and wiki summary documentation. It is intended for documentation generation without executing code or modifying the original repositories. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads the repository tree selected by the user and generated documentation may include credentials, private configuration, internal infrastructure, or wiki and business-process content. <br>
Mitigation: Point ROOT_PATH only at approved projects, write to a controlled OUTPUT_PATH, and review generated documentation before committing or sharing it. <br>
Risk: Generated documentation can be incomplete or misleading if repository structure, manifests, routes, or wiki content are stale or ambiguous. <br>
Mitigation: Have project maintainers review the generated Markdown against the source repositories before relying on it for onboarding, architecture, deployment, or process decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dannyxyz22/document-multiple-repository) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, files, guidance] <br>
**Output Format:** [Markdown documentation files organized by system and repository] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes generated documentation to OUTPUT_PATH and does not modify the source repositories.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and server release metadata; artifact changelog lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
