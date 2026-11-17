## Description: <br>
Data Analysis Litiao Free helps an agent structure basic data-analysis work by clarifying the decision goal, checking statistical rigor, selecting basic methods such as hypothesis tests or descriptive statistics, and formatting conclusions with uncertainty. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and external agent users use this skill to guide lightweight data-analysis workflows, including decision framing, data inventory, sample-size and control-group checks, method selection, and concise result reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill declares broad local read, write, and command-execution style tools. <br>
Mitigation: Use it only on data intended for analysis and review any proposed command or file-writing action before allowing it. <br>
Risk: Basic statistical guidance can be over-applied when sample sizes are small, controls are unfair, or effect sizes are ignored. <br>
Mitigation: Require the agent to report sample-size limits, control-group comparability, effect size, and uncertainty before relying on conclusions. <br>
Risk: The free skill description excludes advanced checks such as multiple-comparison correction, full analysis-trap detection, cohort analysis, and anomaly detection. <br>
Mitigation: Treat outputs as lightweight analysis guidance and escalate to deeper review for high-impact or methodologically complex decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/data-analysis-litiao-free) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with optional shell command snippets and structured analysis notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include statistical checks, limitations, and review prompts for data-analysis conclusions.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
