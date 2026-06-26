## Description: <br>
Daily AI intelligence briefing workflow for finding the hottest global and China-region artificial intelligence news, product launches, model releases, research, funding, policy updates, and industry moves, then sending a concise Chinese briefing to the user's Codex workbench. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liangdd](https://clawhub.ai/user/liangdd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to collect recent global and China-region AI news, rank the strongest items, and prepare a concise Chinese-language briefing for a Codex workbench. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Using the optional --insecure collector flag can allow tampered feed content on an untrusted network. <br>
Mitigation: Use the default collector command with TLS verification enabled; reserve --insecure only for temporary local certificate troubleshooting and disclose when it was used. <br>
Risk: Single-source or conflicting AI news can lead to uncertain briefing claims. <br>
Mitigation: Prefer primary sources, use reputable secondary reporting for confirmation, and label uncertain facts as pending confirmation. <br>


## Reference(s): <br>
- [AI Hot News Source Policy](references/source_policy.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/liangdd/ai-hot-news-workbench) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Chinese Markdown briefing with source links and publication times, optionally supported by JSON candidate output from the bundled collector.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Selects 6-10 ranked briefing items and includes at least 2 credible China-region items when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
