## Description: <br>
Use when the user wants to run, design, or interpret caliper evals, write an `.eval.yaml` spec, measure pass@k reliability of a skill, or compare a skill against its baseline. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[edonadei](https://clawhub.ai/user/edonadei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to create, validate, run, and interpret Caliper evaluation specs for agent skills. It helps compare skill behavior against baselines and measure pass@k reliability across supported agent and judge backends. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Eval specs can run setup, cleanup, assertions, and agent backends that execute commands or create files. <br>
Mitigation: Review each .eval.yaml before running it, use trusted specs, and run evaluations in an isolated workspace when possible. <br>
Risk: Selected backends may use local CLI subscriptions or explicit API billing. <br>
Mitigation: Confirm the skill and judge backends before running evaluations, and choose API backends only when API billing is intended. <br>
Risk: Saved Caliper results and transcripts may include prompts, outputs, or local context from an evaluation run. <br>
Mitigation: Review .caliper/results content before sharing or committing it, and gitignore results when only the eval spec should be retained. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/edonadei/skills/evaluate-skill) <br>
- [Caliper Reference](REFERENCE.md) <br>
- [Evaluate Skill Eval Spec](evaluate-skill.eval.yaml) <br>
- [Simple Eval Example](references/examples/simple.eval.yaml) <br>
- [Bundled Eval Examples](references/evals/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with YAML, Python, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update .eval.yaml files and summarize Caliper validation, run, list, and report results.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
