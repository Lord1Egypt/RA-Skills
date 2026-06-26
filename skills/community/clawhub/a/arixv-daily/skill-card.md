## Description: <br>
Fetches daily arXiv papers for configured categories, helps summarize each paper, and prepares scheduled digest pushes for the user. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hislocked](https://clawhub.ai/user/hislocked) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to configure arXiv categories, fetch recent papers on a schedule, generate Markdown digests, and route those digests to a chosen channel. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper script can modify the host Python environment by installing missing dependencies. <br>
Mitigation: Review the scripts first, run the skill in a virtual environment or container, and preinstall dependencies yourself. <br>
Risk: Scheduled push configuration can store chat-routing details such as channel, account, and chat_id values. <br>
Mitigation: Avoid enabling scheduled pushes until you know where those values are stored and how to remove them. <br>


## Reference(s): <br>
- [ClawHub arxiv-daily listing](https://clawhub.ai/hislocked/arixv-daily) <br>
- [arXiv](https://arxiv.org/) <br>
- [arXiv recent category listing](https://arxiv.org/list/cs.CV/recent) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries with configuration text and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local category data files and scheduled push guidance based on user-provided arXiv category and channel settings.] <br>

## Skill Version(s): <br>
0.9.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
