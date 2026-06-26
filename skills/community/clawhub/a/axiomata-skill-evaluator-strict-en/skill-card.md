## Description: <br>
Provides local scripts and guidance for evaluating ClawHub skills with Axioma five-dimension scoring and ISO 25010-style structural checks under a documented strict 90% quality gate. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kofna3369](https://clawhub.ai/user/kofna3369) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and reviewers use this skill to run local heuristic evaluations of ClawHub skill directories, inspect pass/warn/fail checks and score reports, and identify improvements before publishing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill advertises a strict 90% approval gate, but server security evidence says the local evaluator does not enforce that rule. <br>
Mitigation: Treat results as heuristic review input, not as a final approval decision, unless the threshold logic is independently fixed and verified. <br>
Risk: The evaluator includes hard-coded local paths and can write report files outside the evaluated skill directory. <br>
Mitigation: Run it only against explicit test skill directories, avoid broad --all scans unless the configured paths are understood, and check the report output path before use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/kofna3369/axiomata-skill-evaluator-strict-en) <br>
- [kofna3369 Publisher Profile](https://clawhub.ai/user/kofna3369) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance, files] <br>
**Output Format:** [Markdown guidance, shell commands, terminal reports, optional JSON check output, and saved local report files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are based on local heuristic checks of a supplied skill directory; one evaluator script writes timestamped report files to a configured local reports path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact SKILL.md version table) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
