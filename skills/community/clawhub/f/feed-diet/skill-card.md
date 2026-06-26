## Description: <br>
Audit your information diet across HN and RSS feeds with category breakdowns, ASCII charts, and personalized recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tkuehnl](https://clawhub.ai/user/tkuehnl) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and technical readers use this skill to audit Hacker News or RSS reading habits, classify consumed items, and generate a report or goal-focused weekly digest. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches HN or RSS data and may send feed item titles and URLs to a configured LLM provider. <br>
Mitigation: Use the keyword fallback or avoid setting provider API keys when feed privacy matters. <br>
Risk: Feed data is cached locally during audits. <br>
Mitigation: Clear the local feed-diet cache after sensitive audits. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tkuehnl/feed-diet) <br>
- [README](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [Main feed-diet script](artifact/scripts/feed-diet.sh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown report or digest, with shell commands used by the agent to fetch, classify, and summarize feed items] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can use optional LLM classification when ANTHROPIC_API_KEY or OPENAI_API_KEY is configured; otherwise falls back to keyword matching.] <br>

## Skill Version(s): <br>
0.2.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
