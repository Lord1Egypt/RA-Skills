## Description: <br>
flomo-add sends a single user-provided memo to a Flomo webhook using a Python requests script that reads the webhook URL from .flomo.config. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[giraffe-tree](https://clawhub.ai/user/giraffe-tree) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and Flomo users use this skill to add quick notes, temporary ideas, or automated single memos from an agent workflow. The skill is intended when the user has already provided memo content and a configured Flomo webhook URL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Flomo webhook URL and memo text are sensitive and may be exposed if shared, logged, or printed. <br>
Mitigation: Keep .flomo.config private, avoid sharing terminal output that includes webhook data, and review memo content before sending. <br>
Risk: Using --url can override the configured webhook and send memo content to an unintended endpoint. <br>
Mitigation: Use --url only intentionally and verify the full webhook URL before execution. <br>
Risk: --dry-run prints the full webhook URL and memo body to the terminal. <br>
Mitigation: Use dry-run only in trusted terminals and avoid preserving or sharing logs that contain the printed request. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/giraffe-tree/flomo-add) <br>
- [Publisher profile](https://clawhub.ai/user/giraffe-tree) <br>
- [Flomo](https://flomoapp.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May execute an HTTP POST to the configured Flomo webhook when used outside dry-run mode.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
