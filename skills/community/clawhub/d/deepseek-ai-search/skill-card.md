## Description: <br>
Search the web using AI models with built-in search capability for live information, news, documentation, or research topics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cznorth](https://clawhub.ai/user/cznorth) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to run AI-assisted web searches for current information, documentation, news, and research questions from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill routes search queries to a third-party endpoint and has weak privacy and trust disclosure. <br>
Mitigation: Verify the configured endpoint before use and avoid sending secrets, proprietary code, personal data, or regulated information through this skill. <br>
Risk: The artifact advertises a shared public API key. <br>
Mitigation: Use an operator-controlled, scoped API key instead of the shared key and rotate credentials according to local policy. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cznorth/deepseek-ai-search) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text or Markdown-style console output with search results, optional reasoning, and usage statistics] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and AI_SEARCH_API_KEY; accepts a JSON request with query, model, verbose, and stream options.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
