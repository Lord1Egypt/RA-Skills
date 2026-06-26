## Description: <br>
Reads advertising performance CSV exports and produces a structured Markdown diagnostic report with creative rankings, quadrant classifications, keyword insights, and optimization guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ahsbnb](https://clawhub.ai/user/ahsbnb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing operators and advertising analysts use this skill to analyze platform-exported creative performance reports, identify high- and low-performing creatives, and generate practical optimization guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated reports may contain confidential advertising performance metrics or sensitive business context from the input CSV. <br>
Mitigation: Use approved datasets only, avoid including secrets or personal data, and review generated reports before external sharing. <br>
Risk: Sharing reports through Feishu or email could expose performance data to unintended audiences. <br>
Mitigation: Confirm the destination and audience before sending any report outside the approved team. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ahsbnb/creative-performance-diagnoser2) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, guidance] <br>
**Output Format:** [Markdown diagnostic report printed to stdout] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses user-provided CSV data and column mappings to calculate CTR, CVR, ROI, CPC, quadrant classifications, keyword summaries, and optimization suggestions.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
