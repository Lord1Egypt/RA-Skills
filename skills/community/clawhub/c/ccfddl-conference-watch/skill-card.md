## Description: <br>
Fetches and filters academic conference deadline data from CCFDDL for CCF conference, CFP, ranking, and venue-selection questions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fengwm64](https://clawhub.ai/user/fengwm64) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Students, researchers, and academic authors use this skill to find upcoming CCFDDL conference deadlines, filter by venue, category, and ranking, and receive sortable Markdown summaries from public CCFDDL data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may activate on broad academic deadline or submission wording. <br>
Mitigation: Use clear conference-specific prompts or specify the desired venue, category, or CCF rank. <br>
Risk: Conference results can be incomplete if CCFDDL data is unavailable, stale, or filtered too narrowly. <br>
Mitigation: Use current CCFDDL data, report when data cannot be fetched, and avoid fabricating missing conference details. <br>


## Reference(s): <br>
- [CCFDDL](https://ccfddl.com) <br>
- [CCFDDL Conference Deadline RSS Feed](https://ccfddl.com/conference/deadlines_zh.xml) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Guidance] <br>
**Output Format:** [Markdown table with concise summary text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses CCFDDL-sourced public deadline data and preserves UTC-12/AoE time labels when present.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
