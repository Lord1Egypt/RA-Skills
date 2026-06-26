## Description: <br>
Maintains an argument ledger and premise consistency report for drafted sections so an agent can check narrative linkage, closed section-level argument loops, and stable definitions before merge. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[WILLOSCAR](https://clawhub.ai/user/WILLOSCAR) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and writing agents use this skill during prose drafting to check whether research-paper sections have explicit paragraph roles, stable premises, and actionable revision tasks. It is most relevant after draft sections exist and before those sections are merged into a final document. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release bundles broad research workflow pipelines and runner code in addition to the advertised argument checker. <br>
Mitigation: Install it only when the broader pipeline bundle is desired, not when a narrow argument-checking prompt is enough. <br>
Risk: Running the bundled pipeline helpers can create or update workspace output files. <br>
Mitigation: Run it in a version-controlled workspace and review generated files and diffs before accepting changes. <br>
Risk: Automatic routing or shell-backed pipeline execution may make workspace-wide changes. <br>
Mitigation: Avoid enabling those execution paths unless the operator understands the pipeline contract and expected output changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/WILLOSCAR/argument-selfloop) <br>
- [WILLOSCAR publisher profile](https://clawhub.ai/user/WILLOSCAR) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, JSON, Files, Shell commands] <br>
**Output Format:** [Markdown reports, JSONL ledger records, and local file outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces intermediate argument-check artifacts such as ARGUMENT_SELFLOOP_TODO.md, SECTION_ARGUMENT_SUMMARIES.jsonl, and ARGUMENT_SKELETON.md; these artifacts are not intended to be inserted into the final draft.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata; bundled skill frontmatter reports 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
