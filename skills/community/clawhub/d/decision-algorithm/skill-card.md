## Description: <br>
Decision Algorithm helps users analyze life decisions with Expected Value, Kelly Criterion, and Bayesian updating across career, investment, relationship, education, and lifestyle choices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[truenorth-lj](https://clawhub.ai/user/truenorth-lj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to structure personal, career, investment, relationship, education, and lifestyle decisions, estimate expected value and position size, and identify assumptions that need more evidence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad trigger phrases can activate the skill for many ordinary decision prompts. <br>
Mitigation: Use the skill only for explicit decision-analysis requests and confirm that web, shell, read, or write tool use is intended before allowing local operations. <br>
Risk: Investment-sizing outputs from Expected Value and Kelly calculations can be mistaken for financial advice. <br>
Mitigation: Treat numeric outputs as analytical aids, not professional advice; review assumptions, use conservative sizing for uncertain estimates, and consult a qualified professional for financial decisions. <br>
Risk: Quantitative recommendations depend on user-provided or researched probabilities, gains, losses, and odds. <br>
Mitigation: Surface key assumptions and information gaps, perform current research for fact-dependent decisions, and update the analysis when new evidence is provided. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/truenorth-lj/decision-algorithm) <br>
- [README](artifact/README.md) <br>
- [EKB Decision Algorithm methodology](artifact/docs/methodology.md) <br>
- [Decision calculator CLI](artifact/tools/decision_calculator.py) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with structured decision analysis, optional inline bash commands, and calculator-derived numeric summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use current research for fact-dependent decisions and python3 calculator commands when numeric probability, gain, loss, odds, or capital inputs are available.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter and ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
