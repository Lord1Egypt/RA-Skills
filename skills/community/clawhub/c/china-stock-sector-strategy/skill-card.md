## Description: <br>
Provides a public-source China A-share sector strategy snapshot based on Eastmoney industry and concept-sector data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luyao-inc](https://clawhub.ai/user/luyao-inc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to fetch a JSON snapshot of China stock industry and concept-sector activity for market context. The output is informational and should not be treated as investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes outbound requests to Eastmoney and may use web search or fetch for context. <br>
Mitigation: Run it only in environments where public market-data network access is acceptable and review fetched context before relying on it. <br>
Risk: The output contains informational market data and could be mistaken for investment advice. <br>
Mitigation: Treat the JSON snapshot as reference material only and require human review before making trading or portfolio decisions. <br>


## Reference(s): <br>
- [China Stock Sector Strategy on ClawHub](https://clawhub.ai/luyao-inc/china-stock-sector-strategy) <br>
- [luyao-inc Publisher Profile](https://clawhub.ai/user/luyao-inc) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [JSON printed by a Python command, with optional markdown guidance from the agent] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes ok, payload, sectors_count, concepts_count, market overview, and a northbound-funds limitation note.] <br>

## Skill Version(s): <br>
2.0.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
