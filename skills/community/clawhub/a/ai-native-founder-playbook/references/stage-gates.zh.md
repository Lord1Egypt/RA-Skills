# 阶段门

用这个 reference 判断 AI-native startup 当前处于哪个阶段，以及进入下一阶段需要什么证据。

## 阶段选择

| 信号 | 可能阶段 |
| --- | --- |
| 只有 idea、目标客户猜测或市场假设，缺少直接证据 | Idea |
| 已验证一个具体问题，正在决定第一版产品做什么 | MVP |
| 已有早期 traction，需要让增长、产品、安全和运营可重复 | Launch |
| 已有规模、enterprise 压力、成熟 GTM 需求或 founder bottleneck | Scale |
| 多个阶段信号混在一起 | 先诊断最危险的缺失 stage gate |

## Idea 阶段

目标：在动手 build 前，验证一个真实、具体、高频的问题是否存在于一个可触达市场里。

阶段门：Problem-solution fit。

必须要求的证据：

- 明确 target segment，并能说明 pain、frequency、severity、current workaround、budget 或 urgency。
- 来自真实用户访谈或等价的一手证据。
- competitive map 覆盖 direct、indirect、adjacent、incumbent solutions。
- 主动寻找 disconfirming evidence。
- solution concept 对应验证后发现的问题，而不是 founder 一开始的假设。

只有在以下条件成立时才退出：

- 问题真实且具体。
- 方案解决的是验证后暴露出来的真实问题。
- 有足够 qualitative signal 支撑进入 MVP，即使还没有 certainty。

常见失败模式：

- 把 prototype 当成 validation。
- 让 agentic coding 跑在证据前面。
- 让 AI 帮 founder 证明自己是对的，而不是反驳自己。
- 还没找到 wedge 就去做 broad market。

默认下一步：

1. 收紧 problem hypothesis。
2. 做 adversarial research。
3. 审核 discovery questions 是否 leading、future-facing、too broad。
4. 访谈真实 target users。
5. 每 5 次访谈后分开综合 supporting evidence 与 challenging evidence。
6. 只 build 一个用于测试 core interaction 的最小 prototype。

## MVP 阶段

目标：把已验证的问题转化为最小可用产品，产生真实价值证据，同时避免 architecture、scope、security、context 因 AI 速度过快而失控。

阶段门：早期 product-market fit evidence。

必须要求的证据：

- 来自特定 user group 的 retention、revenue、referral 或 repeat usage。
- 书面的 MVP scope，明确 included 与 deliberately excluded。
- 面向 coding agents 的 architecture/context document。
- launch 前定义好的 measurement framework。
- 接触真实用户数据前的 security review。
- 能区分 user signal 与 founder enthusiasm 的 feedback loop。

只有在以下条件成立时才退出：

- 某个明确群体会回来、付费、推荐或反复使用。
- 指标在多个 iteration cycles 中保持。
- 产品开始 pull usage，而不是完全依赖 founder push。

常见失败模式：

- 没有 architecture/context，导致 agentic technical debt。
- 把 launch spike 或朋友用户误判成 PMF。
- zero-friction scope creep。
- 代码能跑但不安全。

默认下一步：

1. 写 `MVP_SCOPE.md`。
2. 写 architecture context。
3. 使用短 coding-agent sessions。
4. 定义 activation、retention、revenue、referral 和 false-positive metrics。
5. 真实用户前做 security pass。
6. 朝 evidence 迭代，而不是朝 feature completeness 迭代。
7. 三轮弱迭代后做 pivot diagnostic。

## Launch 阶段

目标：把早期 traction 变成 repeatable growth 和 production-grade operations，同时不让 founder 成为关键瓶颈。

阶段门：可重复 channel-driven growth、production readiness、founder-independent operating loops。

必须要求的证据：

- acquisition channels 有可解释 unit economics，例如 CAC、LTV、payback period。
- infrastructure、security、compliance、reliability、test coverage 能承受 production conditions。
- support、triage、sprint planning、reporting、documentation 不依赖 founder 记忆触发。
- technical debt remediation 已排序。

只有在以下条件成立时才退出：

- 增长来自可重复渠道，而不是一次性发布热度。
- 产品与基础设施能承受真实 production load。
- recurring operations 不靠 founder 每次亲自兜底。

常见失败模式：

- MVP debt 变成 structural liability。
- Founder 仍在每个 loop 里。
- security 与 compliance 在真实 exposure 后才处理。
- 过早 expansion 让原始 PMF signal 变模糊。

默认下一步：

1. 审计 architecture、brittle areas 和 test gaps。
2. 把 remediation 分成 release blockers、next sprint、acceptable debt。
3. 盘点 founder attention。
4. 把 repeatable work 系统化、自动化或委托。
5. 把 security/compliance 变成 product workstream。
6. 建立 lightweight product management operating system。

## Scale 阶段

目标：建立 systematic growth、mature operations、enterprise trust 和 defensible advantages，让 founder 从 builder/operator 转为 executive。

阶段门：公司能在 founder 不亲自跑日常运营的情况下持续增长、被审计、被信任，并形成 moat。

必须要求的证据：

- governance、compliance、finance、support、reliability infrastructure 可被外部审计。
- enterprise-grade documentation、SLAs、support playbooks、observability、incident response。
- 真正的 GTM function：segmentation、messaging、pipeline reporting、sales playbooks、customer success loops。
- domain expertise 已进入 product 和 agent context。
- data loops 与 workflow integrations 让 switching cost 增加。

退出条件：

- sustainable profitability、IPO readiness 或 acquisition readiness。
- growth systematic and auditable。
- well-funded copycat 难以复制你的 domain depth、data loops、integrations 和 workflow lock-in。

常见失败模式：

- context 没有 codify，导致 founder 无法放心交接。
- 交付 enterprise 前 support/security/compliance/reliability 不成熟。
- founder-led growth 到顶，但还没有 GTM engine。
- 只做 visible features，没有累计难复制的 context/data/workflow。

默认下一步：

1. 做 founder bottleneck map。
2. 测试 founder 离开一周哪些 workflow 会停。
3. 把 institutional knowledge 写进 playbooks、decision rules 和 reusable agent context。
4. 准备 enterprise procurement artifacts。
5. 建立 GTM engine，而不是只做 campaign。
6. 把 vertical edge cases 转成 tests、validations、prompts、integrations 或 support workflows。
7. 设计 data flywheel 与 workflow integration audit。
