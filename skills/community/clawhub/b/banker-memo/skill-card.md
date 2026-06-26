## Description: <br>
Generate an investment-banker-grade research memo (analysis.md + slides-outline.md + data-provenance.md) from CN raw-data/ snapshots. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jackdark425](https://clawhub.ai/user/jackdark425) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to turn prepared CN company raw-data snapshots into a banker-grade research memo, slide outline, and data-provenance file. It is intended for A-share, H-share, or non-listed Chinese companies with the required raw-data inputs already populated. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated valuation ranges, credit terms, peer estimates, and investment conclusions may be incorrect or unsuitable for decision-making. <br>
Mitigation: Have a qualified human verify all estimates, source traces, valuation assumptions, credit recommendations, and final conclusions before relying on the output. <br>
Risk: Using the workflow on missing, untrusted, or mismatched raw-data inputs can produce incomplete or misleading memo content. <br>
Mitigation: Run it only on the intended prepared raw-data directory, review the generated prompt and selected paths, and validate outputs with the referenced strict audit gates. <br>
Risk: The skill is CN-focused and may not fit US-listed firms or quick fact-sheet workflows. <br>
Mitigation: Use the skill only for A-share, H-share, or non-listed Chinese company research cases that need the full banker memo workflow. <br>


## Reference(s): <br>
- [Banker Prompt Template](artifact/references/banker_prompt_template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown files with prompt text and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces analysis.md, slides-outline.md, and data-provenance.md with strict source tracing expectations.] <br>

## Skill Version(s): <br>
0.9.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
