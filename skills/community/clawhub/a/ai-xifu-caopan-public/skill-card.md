## Description:

Generates structured educational finance and market-analysis trading-plan reports for stocks, futures, funds, and market risk signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xgs-520](https://clawhub.ai/user/xgs-520)

### License/Terms of Use:

MIT-0

## Use Case:

Finance-focused users can ask an agent to prepare educational market-analysis and trading-plan reports for stocks, futures, funds, and related economic context. Outputs rely on public or user-configured market data and should be treated as unverified educational material, not financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated trading plans may be mistaken for financial advice or may rely on stale financial defaults.

Mitigation: Treat every generated plan as educational material, independently verify data and assumptions, and consult qualified financial professionals before making trading decisions.

Risk: Subprocess-based market-data calls can expose environment secrets to another skill.

Mitigation: Review and limit subprocess environments before installation, and avoid running the skill where valuable credentials are available.

Risk: The skill can write generated reports and local watchlist or tracking files.

Mitigation: Require explicit user confirmation for saves, sends, watchlist updates, and tracking behavior; run the skill only in workspaces where these writes are expected.

Risk: Unsafe filename handling or automatic write behavior could create unexpected files.

Mitigation: Review filename containment and output paths before deployment, and keep automatic file persistence disabled unless the user confirms it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xgs-520/skills/ai-xifu-caopan-public)
- [README](artifact/README.md)
- [Skill documentation](artifact/SKILL.md)
- [Usage instructions](artifact/instructions.md)
- [Tushare](https://tushare.pro)
- [Guosen Securities](https://www.guosen.com.cn)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance and generated .docx trading-plan report files, with helper scripts returning text or JSON status.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs require user verification of market data, API credentials, and any file save, send, or watchlist update.]

## Skill Version(s):

5.3.7 (source: server release metadata, package.json, skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
