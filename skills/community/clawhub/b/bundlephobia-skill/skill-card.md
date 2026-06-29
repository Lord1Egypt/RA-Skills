## Description: <br>
Analyze JavaScript and npm package size using Bundlephobia plus related package and bundle-size checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nick2bad4u](https://clawhub.ai/user/nick2bad4u) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to evaluate npm package, publish, and built-artifact size with Bundlephobia and local package checks, then identify concrete reductions such as narrower imports, dependency swaps, publish-file trimming, or size gates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Documented helper commands may not work because the referenced helper script and check-selection reference are absent from the artifact. <br>
Mitigation: Verify that required helper files are present before relying on helper commands; otherwise use direct Bundlephobia API checks and local npm or artifact-size commands. <br>
Risk: Running npm pack or audit-style local checks in an untrusted repository may execute or inspect project-controlled package metadata and files. <br>
Mitigation: Run local package checks only in repositories the operator trusts and review results before acting on generated recommendations. <br>
Risk: Bundlephobia package results estimate complete-package browser transfer cost and may not represent a user's actual application bundle. <br>
Mitigation: Treat Bundlephobia results as screening data and confirm production impact with project-specific bundler statistics or source-map analysis. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nick2bad4u/skills/bundlephobia-skill) <br>
- [Server-resolved GitHub repository](https://github.com/Nick2bad4u/Bundlephobia-Skill) <br>
- [Bundlephobia package API](https://bundlephobia.com/api/size?package=<name[@version]>) <br>
- [Bundlephobia package pages](https://bundlephobia.com/package/<package>) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with package-size measurements, command examples, and prioritized recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include minified, gzip, dependency-count, npm pack, artifact-size, threshold, and failed-package details when checks are run.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
