## Description: <br>
Claws Daily generates personalized twice-daily news briefs from public hot topics and news search results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chenhui7au](https://clawhub.ai/user/chenhui7au) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use Claws Daily to receive scheduled morning and evening news briefs filtered by selected topic labels, profile preferences, and output language. The skill supports Chinese or English Markdown briefs and uses Asia/Shanghai scheduling windows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Personalization setup stores user preference profile data in metadata.json. <br>
Mitigation: Keep the saved profile high-level, avoid sensitive personal or political details, and review metadata.json after initialization. <br>
Risk: Heartbeat scheduling can continue producing twice-daily runs after the user no longer wants briefs. <br>
Mitigation: Disable the Heartbeat when scheduled morning and evening generation is no longer desired. <br>
Risk: News retrieval can fail, be rate-limited, or return no matching items for a time window. <br>
Mitigation: Use the documented retry and fallback behavior, continue with available sections, and do not fabricate news or missing fields. <br>


## Reference(s): <br>
- [Claws Daily on ClawHub](https://clawhub.ai/chenhui7au/claws-daily) <br>
- [Install and Initialization](artifact/install.md) <br>
- [Daily Brief Examples](artifact/daily_example.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown brief with setup commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Briefs include major events and up to five personalized items; output language is controlled by LANGUAGE.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
