## Description: <br>
arxiv-daily helps agents fetch daily arXiv papers for subscribed categories, organize summaries, and schedule delivery to a configured chat destination. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hislocked](https://clawhub.ai/user/hislocked) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and research-oriented users use this skill to set up recurring arXiv category fetches, save paper metadata and abstracts, generate concise markdown summaries, and send scheduled updates to a configured chat destination. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recurring runs can write local configuration and paper data files, and the setup script may install Python dependencies. <br>
Mitigation: Confirm the arXiv categories, timer schedule, output paths, and dependency installation approach before enabling recurring runs; use a virtual environment or preinstall dependencies when appropriate. <br>
Risk: Scheduled paper summaries can be sent to the wrong chat destination if the push configuration is incorrect. <br>
Mitigation: Verify the channel, account, and chat_id before enabling daily delivery, and test with a limited category first. <br>


## Reference(s): <br>
- [arXiv](https://arxiv.org/) <br>
- [arXiv recent category listing](https://arxiv.org/list/cs.CV/recent) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries, configuration snippets, and shell command guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fetches arXiv pages over HTTPS and can create local preference and paper data files under references/ and data/.] <br>

## Skill Version(s): <br>
0.9.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
