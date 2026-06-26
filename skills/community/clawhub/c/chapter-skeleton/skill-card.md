## Description: <br>
Builds a retrieval-informed chapter-level outline skeleton from taxonomy or scope hints before detailed subsection decomposition. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[WILLOSCAR](https://clawhub.ai/user/WILLOSCAR) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and writing agents use this skill to stabilize chapter-level intent for literature-survey or paper-writing workspaces before mapping H3 or subsection structure. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bundled pipeline and report-generation artifacts may steer broader workflows if an OpenClaw environment indexes them. <br>
Mitigation: Review package contents before installing, and limit activation to the chapter-skeleton helper unless the broader pipelines are intentionally enabled. <br>
Risk: The helper writes outline/chapter_skeleton.yml from taxonomy and scope hints, which may influence later outline and drafting stages. <br>
Mitigation: Run it only in the intended workspace and review the generated YAML before using it to drive subsection planning or writing. <br>


## Reference(s): <br>
- [Chapter Skeleton overview](artifact/references/overview.md) <br>
- [ClawHub release page](https://clawhub.ai/WILLOSCAR/chapter-skeleton) <br>


## Skill Output: <br>
**Output Type(s):** [configuration, text] <br>
**Output Format:** [YAML file at outline/chapter_skeleton.yml] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [One record per core chapter with id, title, rationale, seed_topics, and target_h3_count; existing non-placeholder output is preserved.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter declares 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
