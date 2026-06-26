## Description: <br>
Downloads arXiv papers, translates them into Chinese, and sends the translated PDF by email using synchronous or queued execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ckqiao](https://clawhub.ai/user/ckqiao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and researchers use this skill to fetch an arXiv paper, translate it to Chinese, and deliver the translated PDF through email. It supports direct execution for one-off work and a queued mode for serialized background processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release evidence reports embedded live-looking service credentials. <br>
Mitigation: Remove embedded credentials, rotate any exposed secrets, and require user-provided scoped credentials through a secret store or environment variables. <br>
Risk: The release evidence reports under-scoped outbound messaging and email delivery. <br>
Mitigation: Require explicit recipient and attachment confirmation, restrict attachments to generated PDFs, and document all outbound notification targets. <br>
Risk: The artifact describes background queue and cron execution. <br>
Mitigation: Make background execution opt-in, expose task status clearly, and keep serialized locking so only one translation job runs at a time. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ckqiao/arxiv-translate-email) <br>
- [arXiv API query example](https://export.arxiv.org/api/query?search_query=ti:SearchR1&max_results=3) <br>
- [arXiv paper example](https://arxiv.org/abs/2503.09516) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated PDF attachments] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces translated PDF files and can send them as email attachments when configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
