## Description: <br>
Build next-session A-share game plans from market structure, overnight macro shocks, policy timing, and watchlist leadership. Use when the user asks what A-shares may do tomorrow, which sectors may repair first, how to read the open, or wants a reusable pre-open discretionary decision workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huangrichao2020](https://clawhub.ai/user/huangrichao2020) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and market-focused agents use this skill to prepare next-session A-share decision notes, pre-open checklists, sector repair scenarios, and watchlist overlays from live market data, public news, and configured desk references. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an Eastmoney API key and makes live finance-data requests. <br>
Mitigation: Store the key only in the documented local runtime file, review endpoint access before use, and verify live facts before acting on a market note. <br>
Risk: Generated market plans can be stale or misleading if public endpoints throttle, change, or return incomplete data. <br>
Mitigation: Run the bundled source benchmark, prefer official primary sources for policy or macro claims, and treat outputs as decision support rather than financial advice. <br>
Risk: Optional background polling can continue writing reports and state under the user's home directory. <br>
Mitigation: Enable launchd or loop mode only intentionally, monitor the state directory, and use the provided uninstall flow when continuous polling is no longer needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/huangrichao2020/a-share-decision-desk) <br>
- [Project Homepage](https://github.com/huangrichao2020/uwillberich) <br>
- [Methodology](references/methodology.md) <br>
- [Data Sources](references/data-sources.md) <br>
- [Message Iterator](references/message-iterator.md) <br>
- [Opening Window Template](references/opening-window-template.md) <br>
- [Cross-Cycle Watchlist](references/cross-cycle-watchlist.md) <br>
- [Event Regime Watchlists](references/event-regime-watchlists.md) <br>
- [Eastmoney MX Application](https://ai.eastmoney.com/mxClaw) <br>
- [Eastmoney MX Official Site](https://ai.eastmoney.com/nlink/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown desk notes with optional shell commands, configuration steps, JSONL event records, SQLite state, and generated report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may depend on live finance endpoints, local watchlists, an EM_API_KEY, and optional background polling state.] <br>

## Skill Version(s): <br>
0.1.12 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
