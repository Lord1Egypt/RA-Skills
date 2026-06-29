## Description: <br>
Bayesian Reasoning helps agents apply priors, likelihood ratios, and posterior updates to probabilistic decisions while avoiding base-rate neglect, prosecutor's fallacy, and correlated-evidence errors. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deciqai](https://clawhub.ai/user/deciqai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers use this skill to structure probabilistic decisions, interpret uncertain evidence, and produce a clear Bayesian update for high-stakes domains such as medical screening, security alerts, fraud flags, hiring signals, and A/B tests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may activate too broadly on the word "update" outside a probabilistic reasoning task. <br>
Mitigation: Confirm the user is making an uncertain decision with evidence before applying the Bayesian workflow. <br>
Risk: Outputs may be mistaken for professional medical, legal, security, or hiring advice. <br>
Mitigation: Use the output as reasoning support, state uncertainty clearly, and defer consequential decisions to qualified reviewers or domain experts. <br>


## Reference(s): <br>
- [Sources - bayesian-reasoning](references/sources.md) <br>
- [Sally Clark Case (1999)](examples/sally-clark-1999.md) <br>
- [Royal Statistical Society letter on statistical evidence](https://web.archive.org/web/20120925034735/http://www.rss.org.uk/uploadedfiles/documentlibrary/744.pdf) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown coaching prompts and a structured Bayesian Update template] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May ask one question at a time in Coach mode and pause for user input.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
