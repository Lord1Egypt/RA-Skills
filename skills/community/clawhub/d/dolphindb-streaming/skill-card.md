## Description: <br>
提供基于 DolphinDB 的金融场景流式计算能力，支持实时行情、因子计算、风控及订单簿等实时数据流处理。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ugpoor](https://clawhub.ai/user/ugpoor) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and quantitative engineering teams use this skill to design DolphinDB streaming workflows for real-time market data processing, factor calculation, order book processing, and risk monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Examples repeatedly use weak sample DolphinDB admin credentials. <br>
Mitigation: Replace sample admin/123456 credentials with a least-privileged DolphinDB account before use. <br>
Risk: The artifact includes an automated trading execution pipeline example without clear user controls. <br>
Mitigation: Keep execution-related examples disabled or paper-trading until approvals, limits, monitoring, and rollback procedures are in place. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ugpoor/dolphindb-streaming) <br>
- [DolphinDB website](https://www.dolphindb.cn/) <br>
- [DolphinDB documentation center](https://docs.dolphindb.cn/zh/) <br>
- [Streaming data tutorial](https://docs.dolphindb.cn/zh/stream/str_intro.html) <br>
- [Streaming financial factor implementation](https://docs.dolphindb.cn/zh/tutorials/str_comp_fin_quant_2.html) <br>
- [Real-time high-frequency factors](https://docs.dolphindb.cn/zh/tutorials/hf_factor_streaming_2.html) <br>
- [Order book engine](https://docs.dolphindb.cn/zh/tutorials/orderBookSnapshotEngine.html) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with Python, DolphinDB, and bash code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces implementation guidance for agent-assisted DolphinDB streaming workflows; examples require environment setup and credential review before execution.] <br>

## Skill Version(s): <br>
1.4.0 (source: server release metadata, released 2026-04-02) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
