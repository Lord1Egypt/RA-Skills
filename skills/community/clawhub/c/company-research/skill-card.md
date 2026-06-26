## Description: <br>
企业背景调查工具（智访通）面向电信客户经理，通过百度、360、搜狗微信和头条等公共搜索引擎搜集企业公开信息，并生成企业概况、近期动态、互联网信息和商机雷达报告。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[szsip239](https://clawhub.ai/user/szsip239) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Telecom account managers use this skill to research a named company from public Chinese web sources and turn the findings into a concise account-planning report. The report highlights company background, recent developments, internet context, and telecom-related opportunity signals. <br>

### Deployment Geography for Use: <br>
China, with stated focus on Suzhou and Suzhou Industrial Park. <br>

## Known Risks and Mitigations: <br>
Risk: Company names, search terms, and pasted business context may be sent to public search engines during research. <br>
Mitigation: Use only public or approved inputs, and do not paste confidential annual reports, non-public financials, internal prospect lists, or other sensitive material. <br>
Risk: Public web search results can be stale, incomplete, or confused with similarly named companies. <br>
Mitigation: Review the generated report before use, verify important facts against trusted public sources, and preserve the skill's rules against fabrication and entity confusion. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/szsip239/company-research) <br>
- [agent-browser dependency](https://github.com/vercel-labs/agent-browser) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown report with concise bullet sections and inline shell commands when setup guidance is needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a Chinese-language company research report; omits empty sections when evidence is not found.] <br>

## Skill Version(s): <br>
1.1.3 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
