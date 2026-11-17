## Description:

Provides DolphinDB streaming-computation guidance for real-time financial market data, factor calculation, risk monitoring, and order-book workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ugpoor](https://clawhub.ai/user/ugpoor)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and quantitative engineering teams use this skill to create DolphinDB streaming tables, engines, subscriptions, real-time factors, market-data views, and risk-monitoring workflows for financial data pipelines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release depends on DolphinDB helper skills or setup scripts that are not pinned in the evidence.

Mitigation: Verify the referenced helper skills and scripts before installation, pin trusted versions where possible, and review changes before updating.

Risk: Examples show privileged default DolphinDB credentials for financial automation workflows.

Mitigation: Replace sample credentials with least-privilege accounts, secret management, and environment-specific access controls before running in a real environment.

Risk: Alerting and order-execution examples could affect production financial workflows if copied directly.

Mitigation: Treat these examples as illustrative until dry-run mode, human approvals, audit logging, and production separation are added.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ugpoor/skills/dolphindb-streaming)
- [DolphinDB official site](https://www.dolphindb.cn/)
- [DolphinDB documentation center](https://docs.dolphindb.cn/zh/)
- [DolphinDB streaming tutorial](https://docs.dolphindb.cn/zh/stream/str_intro.html)
- [Financial factor streaming implementation](https://docs.dolphindb.cn/zh/tutorials/str_comp_fin_quant_2.html)
- [Real-time high-frequency factors](https://docs.dolphindb.cn/zh/tutorials/hf_factor_streaming_2.html)
- [Streaming capital flow calculation](https://docs.dolphindb.cn/zh/tutorials/streaming_capital_flow_order_by_order_2.html)
- [Real-time stock price increase calculation](https://docs.dolphindb.cn/zh/tutorials/rt_stk_price_inc_calc_2.html)
- [Level-2 stock data processing](https://docs.dolphindb.cn/zh/tutorials/l2_stk_data_proc_2.html)
- [Order book snapshot engine](https://docs.dolphindb.cn/zh/tutorials/orderBookSnapshotEngine.html)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown guidance with Python and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the user to adapt dependencies, credentials, DolphinDB connection settings, and operational safeguards before use.]

## Skill Version(s):

1.4.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
