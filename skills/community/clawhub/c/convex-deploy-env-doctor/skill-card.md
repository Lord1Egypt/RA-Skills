## Description: <br>
Validate and fix Convex deployment configuration for skills/apps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[okikesolutions](https://clawhub.ai/user/okikesolutions) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to diagnose Convex deployment URL, callback, environment variable, and backend connectivity problems before publishing or deploying a skill or app. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may inspect local environment, configuration, documentation, and source files while diagnosing Convex deployment issues. <br>
Mitigation: Use it in a trusted workspace, keep secret values out of shared output, and review evidence snippets before sharing results. <br>
Risk: The skill may perform safe reachability checks against configured deployment or callback URLs. <br>
Mitigation: Limit checks to the configured endpoints, disclose touched domains, and avoid sending sensitive data externally. <br>
Risk: Suggested fixes may change deployment routing, OAuth callbacks, or runtime environment behavior. <br>
Mitigation: Review proposed file-level patches and run the listed post-fix verification commands before deployment. <br>


## Reference(s): <br>
- [Convex Env Doctor Output Template](references/output-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with pass/fail findings, file-level evidence, exact fixes, data-routing disclosure, and verification commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Must avoid printing secrets and should disclose any files read or endpoints touched.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
