## Description: <br>
Paper Assistant helps agents fetch, filter, and recommend recent Agent model algorithm and reinforcement learning papers for review or downstream posting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luahan77m](https://clawhub.ai/user/luahan77m) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and teams running paper feeds use this skill to collect recent OpenReview and arXiv candidates, select one high-value Agent algorithm or reinforcement learning paper, and prepare a concise recommendation for deeper review or scheduled delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs local Python scripts that contact public OpenReview and arXiv endpoints and update a local pushed-paper history. <br>
Mitigation: Run it in an expected workspace/network context and review data/pushed.json changes before using the result in automated posting. <br>
Risk: Paper selection can be incomplete or misclassified because it depends on public API results and LLM screening criteria. <br>
Mitigation: Keep a human review step before deeper analysis, scheduled posting, or group-chat delivery. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/luahan77m/arxiv-paper-assistant) <br>
- [OpenReview notes search API](https://api2.openreview.net/notes/search) <br>
- [arXiv API query endpoint](https://export.arxiv.org/api/query) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown recommendation with paper metadata; supporting scripts can emit JSON candidate lists.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Maintains data/pushed.json to avoid repeated paper recommendations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
