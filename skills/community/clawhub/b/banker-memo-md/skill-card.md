## Description: <br>
Produces an investment-banker-grade research memo and data provenance table from CN raw-data JSON snapshots. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jackdark425](https://clawhub.ai/user/jackdark425) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Analysts and agents use this skill to turn populated CN company raw-data snapshots into an eight-section banker-style memo for credit review and investment analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated credit or investment recommendations may be incomplete or unsuitable for real decisions. <br>
Mitigation: Review the memo and recommendations independently before relying on them. <br>
Risk: The skill reads local raw-data JSON files and writes memo outputs to a chosen directory. <br>
Mitigation: Confirm the raw-data directory contains only intended inputs and choose an output directory the agent may write to. <br>
Risk: Financial figures in the memo can lose traceability if provenance rows are missing or inconsistent. <br>
Mitigation: Review data-provenance.md and resolve any data flags or missing source rows before handoff. <br>


## Reference(s): <br>
- [Banker Memo MD prompt template](references/banker_memo_md_prompt.md) <br>
- [ClawHub skill page](https://clawhub.ai/jackdark425/banker-memo-md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown files and prompt text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces analysis.md and data-provenance.md from local raw-data JSON snapshots.] <br>

## Skill Version(s): <br>
0.9.7 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
