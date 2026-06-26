## Description: <br>
Validate, fix, optimize natural language, and publish EvoMap Gene+Capsule bundles for maximum discoverability. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Josephyb97](https://clawhub.ai/user/Josephyb97) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to validate, repair, enhance, and optionally publish EvoMap Gene+Capsule bundle JSON files. It is intended for improving bundle structure, summaries, trigger signals, asset hashes, and publish readiness. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The publish path can run unintended shell commands from bundle contents. <br>
Mitigation: Review or patch the publish path before use, avoid running publish commands on untrusted bundle JSON, and inspect bundle data before sending it to EvoMap. <br>
Risk: The skill rewrites trust-like metadata such as confidence, success_streak, and EvolutionEvent values. <br>
Mitigation: Treat generated trust and promotion fields as promotional edits, not independently verified results, and validate them before saving or publishing bundles. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Josephyb97/evomap-bundle-improve) <br>
- [EvoMap publish endpoint](https://evomap.ai/a2a/publish) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, validation diagnostics, JSON bundle edits, and publish responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May rewrite input bundle JSON files, recompute asset_id hashes, generate summaries and content, and call the EvoMap publish endpoint for publish commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
