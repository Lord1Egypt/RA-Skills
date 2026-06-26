## Description: <br>
Analyzes Vue, React, and Angular front-end code to infer trading-domain business requirements, extract business rules, and produce reusable knowledge artifacts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[joshphe](https://clawhub.ai/user/joshphe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect trading-oriented front-end codebases, reverse-engineer functional requirements, compare implementation with requirements, and generate JSON or Markdown analysis artifacts for review and knowledge management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local caching and optional knowledge-base storage can persist code-derived analysis. <br>
Mitigation: Install only for repositories where local persistence is acceptable, review configured storage paths, and use --no-cache for sensitive one-off analysis. <br>
Risk: Optional LLM-backed analysis may send code-derived data outside the local environment if enabled in the future. <br>
Mitigation: Do not enable LLM_API_KEY or related optional dependencies until the data flow and provider terms have been reviewed. <br>
Risk: The optional setup script can modify skill files. <br>
Mitigation: Review setup scripts before running them and execute them only when those file changes are intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/joshphe/code-to-requirement-analyser) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, JSON, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown reports, JSON analysis results, and command-line guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local cache entries and optional knowledge-base files under configured local paths.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata); artifact frontmatter reports 2.1.0 <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
