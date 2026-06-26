## Description: <br>
Conducts structured web research by searching, fetching, following up, deduplicating, and synthesizing information into cited reports with source quality scoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[indigas](https://clawhub.ai/user/indigas) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and research-focused agents use this skill to turn a research question or batch of questions into cited Markdown, JSON, or HTML reports with source scoring, limitations, and follow-up questions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Research queries and generated reports may include sensitive topics and can be sent to external web services or persisted locally. <br>
Mitigation: Avoid sensitive topics unless that exposure is acceptable, and review or delete saved reports when they are no longer needed. <br>
Risk: Synthesized findings may be outdated, incomplete, or misleading if sources are weak or conflicting. <br>
Mitigation: Cross-check major claims against multiple sources, review source quality scores and limitations, and independently verify important conclusions before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/indigas/claw-web-research) <br>
- [Search Strategies](artifact/references/search-strategies.md) <br>
- [Synthesis Framework](artifact/references/synthesis-framework.md) <br>
- [Report Template](artifact/references/report_template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown, JSON, or HTML research reports with citations; inline shell commands for running the pipeline.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports may be saved under workspace/research/ and may include source quality scores, limitations, and citations.] <br>

## Skill Version(s): <br>
2.1.0 (source: server evidence release.version, artifact SKILL.md, scripts/research.py) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
