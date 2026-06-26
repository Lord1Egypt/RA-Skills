## Description: <br>
Fetches yesterday's arXiv papers, ranks them by keyword relevance for configured research groups, and pushes selected results to Feishu/Lark via webhook. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ventaozzz](https://clawhub.ai/user/ventaozzz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and research teams use this skill to automate daily monitoring of arXiv papers for configured topics and deliver ranked paper recommendations to Feishu/Lark groups. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Configured group names, keywords, and selected paper titles or links are sent to the configured Feishu/Lark webhook. <br>
Mitigation: Use only approved webhook destinations and keep the webhook URL private. <br>
Risk: The optional scheduled cron command can run the skill automatically. <br>
Mitigation: Review the cron command and runtime path before enabling scheduled execution. <br>
Risk: Dependencies are declared with lower bounds rather than exact pins. <br>
Mitigation: Pin dependency versions in production environments. <br>
Risk: The HTTP fallback mode can use the plain-HTTP arXiv API endpoint. <br>
Mitigation: Prefer arxiv library mode when avoiding plain-HTTP fallback is required. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ventaozzz/arxiv-daily-pusher) <br>
- [README](artifact/README.md) <br>
- [Configuration example](artifact/config.example.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text Feishu/Lark messages with Markdown setup guidance and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Posts selected paper titles, publication dates, relevance scores, and links to the configured webhook.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
