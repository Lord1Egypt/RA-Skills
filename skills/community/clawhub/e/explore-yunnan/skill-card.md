## Description: <br>
Explore Yunnan's diversity across Kunming, Lijiang, Dali, Shangri-La, and Xishuangbanna, and use flyai CLI data to support travel search, booking links, itinerary planning, and related travel tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External travelers, travel planners, and agent operators use this skill to search Yunnan flights, hotels, attractions, and itinerary options with live flyai results and booking links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install and run a global npm CLI for travel searches. <br>
Mitigation: Review the CLI package and run it in a controlled environment before using it for booking workflows. <br>
Risk: Travel searches may send prompts and itinerary details to flyai or Fliggy services. <br>
Mitigation: Avoid entering passport, payment, account, or other sensitive booking details in prompts. <br>
Risk: The skill may persist raw travel queries in .flyai-execution-log.json. <br>
Mitigation: Delete the local execution log if retained travel-query history is not desired. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/dingtom336-gif/explore-yunnan) <br>
- [Parameter and output templates](references/templates.md) <br>
- [Scenario playbooks](references/playbooks.md) <br>
- [Failure recovery fallbacks](references/fallbacks.md) <br>
- [Execution runbook](references/runbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with comparison tables, booking links, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires live flyai CLI output; booking results should include detailUrl links and may write .flyai-execution-log.json when filesystem writes are available.] <br>

## Skill Version(s): <br>
3.2.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
