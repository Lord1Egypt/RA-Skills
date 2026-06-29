## Description: <br>
FarmDash Trail Marshal helps agents plan guarded DeFi workflows by listing recipes, building quality gates, recording session workflow runs, and reporting status without executing wallet or trading actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[parmasanandgarlic](https://clawhub.ai/user/parmasanandgarlic) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to coordinate DeFi workflow recipes, check installed companion skills, and keep state-changing actions behind separate confirmation gates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: DeFi workflow plans can lead to financial loss if stale quotes, market movement, or incomplete companion-skill coverage are ignored. <br>
Mitigation: Verify each quote and required companion skill before confirmation, and keep execution in separately reviewed skills with their own confirmation gates. <br>
Risk: Session workflow records and optional tokens may expose paid or session-tracking features when configured. <br>
Mitigation: Provide FARMDASH_API_KEY or session tokens only when intentionally using those features, and do not provide wallet secrets or signing material. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/parmasanandgarlic/skills/farmdash-trail-marshal) <br>
- [FarmDash agents homepage](https://www.farmdash.one/agents) <br>
- [FarmDash API schema](https://www.farmdash.one/agents/openapi.yaml) <br>
- [FarmDash MCP server config](https://www.farmdash.one/.well-known/mcp.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown guidance with structured workflow metadata and status records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Plans are advisory orchestration outputs; state-changing execution remains delegated to separately installed skills.] <br>

## Skill Version(s): <br>
0.1.7 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
