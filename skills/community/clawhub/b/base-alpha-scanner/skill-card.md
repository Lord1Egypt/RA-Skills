## Description: <br>
Base Alpha Scanner helps agents scan Base-chain tokens, narratives, holder distribution, and market signals to generate high-conviction crypto alert candidates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[a4205586](https://clawhub.ai/user/a4205586) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and crypto analysts use this skill to run Base-chain market scans, investigate token addresses and holder concentration, monitor Clanker, Bankr.fun, and VIRTUAL Protocol narratives, and prepare alert candidates from public market data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill queries third-party crypto market-data sites and may rely on external availability, rate limits, or browser-session access. <br>
Mitigation: Validate token addresses before use, expect public endpoint failures, avoid logged-in browser sessions unless needed, and protect any Basescan API key. <br>
Risk: Generated alert candidates can be incorrect, incomplete, stale, or financially risky if treated as trading instructions. <br>
Mitigation: Verify trading signals independently before acting and use the skill output as research support, not as standalone financial advice. <br>
Risk: Some sources such as GMGN and Bankr.fun may require browser fallback or manual review, which can leave gaps in automated scans. <br>
Mitigation: Cross-check results across documented sources and treat missing or inaccessible data as an uncertainty to disclose in the alert. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/a4205586/base-alpha-scanner) <br>
- [Alert Rules & Filtering Logic](references/alert-rules.md) <br>
- [Base Alpha Scanner API & Endpoint Reference](references/api-endpoints.md) <br>
- [DexScreener API](https://api.dexscreener.com) <br>
- [Basescan API](https://api.basescan.org/api) <br>
- [VIRTUAL Protocol API](https://api.virtuals.io/api/virtuals) <br>
- [Clanker Token API](https://www.clanker.world/api/tokens?sort=desc&page=1&limit=30) <br>
- [Warpcast Bankr Channel](https://warpcast.com/~/channel/bankr) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Shell commands, Markdown, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and terminal-style scanner summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May query public third-party crypto market-data endpoints; BASESCAN_API_KEY is optional for higher rate limits.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
