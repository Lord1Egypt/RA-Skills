## Description: <br>
Guides users through Bayesian reasoning with multi-turn dialogue, posterior probability and Bayes factor calculations, sensitivity analysis, and ASCII result visualizations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[erelief](https://clawhub.ai/user/erelief) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers can use this skill to structure hypotheses and evidence, convert probability estimates, calculate Bayesian updates, compare Bayes factors, and optionally save JSON results for later analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Saved Bayesian analysis files may contain sensitive hypotheses or evidence if the user chooses to write results to disk. <br>
Mitigation: Confirm the filename and folder before saving, and avoid shared or synced directories for sensitive analyses. <br>


## Reference(s): <br>
- [Bayesian Analysis Result Schema](references/data_schema.md) <br>
- [ClawHub skill page](https://clawhub.ai/erelief/bayesian-reasoning) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, text, markdown, shell commands, JSON] <br>
**Output Format:** [Conversational Markdown with shell command examples, parsed JSON results, and optional saved JSON analysis files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a local Python calculator for probability math and can save Bayesian analysis state when the user chooses.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
