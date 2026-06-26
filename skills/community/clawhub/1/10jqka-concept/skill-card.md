## Description: <br>
Queries Tonghuashun/iWencai stock concept data for A-share stocks by scraping public F10 pages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liweijie0709-cmyk](https://clawhub.ai/user/liweijie0709-cmyk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and market-analysis agents use this skill to look up A-share stock concept boards, concept constituents, and concept-board market data from public Tonghuashun/iWencai pages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running the scripts contacts Tonghuashun and iWencai-related public sites, which may disclose queried stock symbols to those services. <br>
Mitigation: Avoid using the skill for private trading research when query privacy matters, and review the contacted endpoints before use. <br>
Risk: Batch queries may keep stock concept results in a local OpenClaw cache for about 24 hours. <br>
Mitigation: Disable caching for sensitive workflows or remove the local cache file after use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liweijie0709-cmyk/10jqka-concept) <br>
- [Tonghuashun F10](https://basic.10jqka.com.cn/) <br>
- [Tonghuashun concept boards](https://q.10jqka.com.cn/gn/) <br>
- [iWencai](https://www.iwencai.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with Python and shell examples; included scripts emit JSON and console text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No API key is required. Runtime output depends on public page availability, GBK decoding, and the current page structure.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
