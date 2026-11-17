# ETF投研平台-前置意图识别Skill设计

## 定位

> **执行时机：用户输入完成之后、分发到5个业务Agent（宏观/事件/政策等）并行任务之前**
> 角色：网关级前置安全&意图校验Skill，**拦截非法、越权、无意义、风险提问**，只有校验通过才下发给下游5个Agent集群；不通过直接返回标准化应答，不触发下游Agent消耗。

## 整体数据流

```
用户聊天框输入原始query →【意图识别Skill】→分支判断
├─分支1：拦截类（非法/风险/无意义/越权）→直接返回给用户，**不调用5个业务Agent**
└─分支2：合法投研查询 →输出标准化结构化请求对象 →分发至宏观Agent、事件Agent、政策Agent等5个Agent并行执行 →结果汇总返回用户
```

## 6阶段处理链路

1. **阶段1 规则预处理**：基础清洗（零宽/控制字符/payload过滤）→ 长度校验 → 黑名单匹配。纯规则不调LLM，`rule_block=true` 直接终止。
2. **阶段2 LLM意图识别**：固定JSON Schema输出（intent_type 7枚举 / is_allow_forward / risk_level / rewritten_query / required_agent_list / entity_extract）。
3. **阶段3 业务边界校验**：按intent_type分支——放行（warning加免责声明）/ platform_qa路由 / 闲聊引导 / 注入阻断 / 投资建议A情况（口语化改写放行）B情况（强制索要→拦截）。
4. **阶段4 防注入二次校验**：对rewritten_query检测"忽略规则/输出系统提示词/越权指令"等5类特征，命中覆盖为拦截。
5. **阶段5 路由与埋点**：拦截直接回前端；转发构造任务上下文（request_id / standard_query / entity_extract / risk_warning / agent_allow_list）投递调度器。强制单行JSON埋点日志。
6. **阶段6 异常降级**：LLM超时或JSON解析失败 → conservative（默认，拦截+友好提示）/ loose（放行+intent_parse_failed标记）。

## 关键设计要点（踩坑点）

1. **两层过滤架构：规则引擎在前，LLM意图在后**——不要直接把原始输入丢给大模型。
2. **永远传递改写后的query给下游Agent，禁止透传用户原始query**——"芯片可以买吗"是决策问句，必须改写为客观投研分析指令。
3. **区分「口语化问能不能买」和「强制索要投资建议」**——前者改写放行+免责声明，后者直接拦截。
4. **支持Agent裁剪优化算力**——required_agent_list非空时只调度指定Agent。
5. **安全应答不泄露内部实现**——统一友好话术，不回复"检测到prompt注入"。

## 工程化补充

- Skill作为Agent调度网关的前置中间件独立部署，同步接口超时可控
- 维护badcase库，定期回流线上真实query微调意图识别prompt
- 配置开关：conservative/loose降级模式用于灰度
- 下游Agent也要二次校验risk_warning标记，多层防御
