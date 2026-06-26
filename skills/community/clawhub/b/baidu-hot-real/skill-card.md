## Description: <br>
Baidu Hot Real fetches real-time Baidu hot-search rankings directly from top.baidu.com/board. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iph0n3](https://clawhub.ai/user/iph0n3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to retrieve current public Baidu hot-search rankings for Chinese search-trend context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs local Python or Bash and makes outbound requests to Baidu. <br>
Mitigation: Install only when outbound access to top.baidu.com is acceptable, and review future updates for any expansion beyond the Baidu hot-search fetch workflow. <br>
Risk: The Baidu page format or rate limits can change, which may cause incomplete or failed ranking output. <br>
Mitigation: Keep request frequency modest and review parser behavior when results look empty, malformed, or outdated. <br>


## Reference(s): <br>
- [Baidu Hot Search Board](https://top.baidu.com/board) <br>
- [Baidu Hot Search Realtime Board](https://top.baidu.com/board?tab=realtime) <br>
- [ClawHub Skill Page: Baidu Hot Real](https://clawhub.ai/iph0n3/baidu-hot-real) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Plain text ranking output with optional Markdown command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fetches up to 50 public ranking items; network access to top.baidu.com is required.] <br>

## Skill Version(s): <br>
1.3.0 (source: SKILL.md frontmatter, package.json, evidence.json release) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
