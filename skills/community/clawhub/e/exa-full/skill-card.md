## Description: <br>
Exa AI search + Research API supports web and code search, content extraction, and asynchronous multi-step research tasks with optional structured output schemas. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[XieShaocong33Ethan](https://clawhub.ai/user/XieShaocong33Ethan) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to query Exa for web results, code and documentation context, URL contents, and asynchronous research results. It is useful when an agent needs current external information, page extraction, or structured research output through Exa's API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an Exa API key and sends user-directed search queries, URLs, research instructions, and selected schema files to Exa. <br>
Mitigation: Use a dedicated Exa API key, monitor quota usage, and run the skill only for data that is acceptable to send to Exa. <br>
Risk: SCHEMA_FILE contents are uploaded as outputSchema for Exa research tasks. <br>
Mitigation: Do not point SCHEMA_FILE at secrets, credentials, key files, certificates, .env files, or confidential documents; use a dedicated JSON schema file. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/XieShaocong33Ethan/exa-full) <br>
- [Publisher Profile](https://clawhub.ai/user/XieShaocong33Ethan) <br>
- [Exa Homepage](https://exa.ai) <br>
- [Exa Documentation](https://docs.exa.ai/) <br>
- [Exa Subpage Crawling Reference](https://docs.exa.ai/reference/crawling-subpages) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with bash command examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, and EXA_API_KEY; optional environment variables tune search, content extraction, and research polling.] <br>

## Skill Version(s): <br>
1.2.1 (source: evidence release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
