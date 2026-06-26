## Description: <br>
Dependency Autopsy helps agents examine dependency trees for maintenance activity, maintainer health, bloat, replacement difficulty, version drift, license concerns, and dependency depth. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jcools1977](https://clawhub.ai/user/jcools1977) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering teams use this skill before adding dependencies, during dependency health checks, before security or compliance reviews, and when investigating bundle size or dependency risk. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may produce incomplete or incorrect dependency health, license, or security conclusions. <br>
Mitigation: Independently verify license and security conclusions before making production dependency decisions. <br>
Risk: Using the skill may lead an agent to inspect dependency files and source imports in a repository. <br>
Mitigation: Use it only in repositories where that review is acceptable and avoid exposing sensitive private code unnecessarily. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jcools1977/dependency-autopsy) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Guidance] <br>
**Output Format:** [Markdown dependency health report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No API calls or executable code; report quality depends on available manifests, lockfiles, source imports, and registry or project metadata.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
