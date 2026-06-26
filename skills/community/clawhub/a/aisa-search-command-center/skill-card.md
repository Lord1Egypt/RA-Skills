## Description: <br>
Run web, multi-source, or last-30-days research through AIsa for search, synthesis, competitor scans, trend discovery, and structured retrieval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bibaofeng](https://clawhub.ai/user/bibaofeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and research teams use this skill to run AIsa-backed web, scholarly, multi-source, Tavily, and Perplexity-style searches, then turn retrieval results into concise research briefs, comparisons, or trend summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Searches, prompts, system instructions, and URLs are sent to AIsa. <br>
Mitigation: Use the skill only when sending that content to AIsa is acceptable; avoid secrets, private internal URLs, personal data, and confidential business material. <br>
Risk: Retrieved or synthesized results can be incomplete, stale, or affected by provider errors and timeouts. <br>
Mitigation: Report provider failures honestly, keep cited evidence visible where available, and retry or narrow deep-research prompts when timeouts occur. <br>
Risk: The skill requires a sensitive API credential. <br>
Mitigation: Provide AISA_API_KEY through the environment or an approved secret manager, and avoid committing credentials to project files or command history. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bibaofeng/aisa-search-command-center) <br>
- [AIsa API base endpoint](https://api.aisa.one/apis/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AISA_API_KEY and python3; API results may include retrieved sources, confidence scores, provider errors, and timeout guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
