---
name: cron-health-monitor
slug: openclaw-cron-health-monitor
version: 1.0.1
displayName: "Cron Health Monitor"
summary: "Proactive cron job health monitoring, failure detection, and auto-repair delegation."
description: "Proactive cron job health monitoring, failure detection, and auto-repair delegation. Triggers: 'cron failed', 'cron health', 'fix cron', 'consecutive errors'"
tags:
  - cron
  - monitoring
  - health
  - auto-repair
  - devops
license: MIT
---

# Cron Health Monitor

一个静默失败的cron比没有cron更危险。它制造一切都好的幻觉。

---

## 五分钟：为什么你需要这个

你有几十条cron在跑。你以为它们在跑。但它们是沉默的——失败的时候不会喊你。直到三天后你打开文件，发现这三天什么都没有产出。

这个skill做三件事：
1. **闻到问题**——在consecutiveErrors涨到2之前就发现不对劲
2. **诊断根因**——不是"这条cron失败了"，是"这条cron失败是因为isolated session里用了message工具"
3. **自动派修**——不叫醒CEO，直接把修复任务派给数据中心

装完这个skill，cron失败不需要你处理。每周看一次巡检报告，绿色的跳过，红色的已经有人在修了。

---

## 进化阶梯

### L1：部署巡检（第一天）
复制每周巡检cron模板。部署。第一周你会发现一些你已经习惯但没注意到的失败。这很正常——看见问题是第一步。

**判断标准**：巡检报告生成了，你看到了consecutiveErrors列表。

### L2：理解模式（第一周）
你不会只看consecutiveErrors了。你开始看output文件是不是空的、lastDurationMs是不是异常、三个"成功"的cron是不是在同一个秒数失败（限流级联）。你从"报错才看"进化到"不对劲就看"。

**判断标准**：你发现了一个consecutiveErrors=0但实际在偷懒的cron。你开始理解"静默成功"比报错更可怕。

### L3：自动修复（第一个月）
巡检发现问题→自动分派修复→修复成功→下次巡检确认修复。这个闭环不需要CEO。数据中心成了cron的自愈系统。

**判断标准**：一条cron从失败到修复的过程中，你唯一的感知是巡检报告上写着"已修复"。

### L4：自愈系统（第三个月+）
新的失败模式出现——系统识别为未知模式——归档为新模式——修复playbook自动更新。系统在进化。你在睡觉。

**判断标准**：你查看历史记录，发现系统修好了一个你从未见过的失败模式。这个模式现在在playbook里了。

---

## 实际案例：我们39条cron踩过的坑

### 案例1：智谱Key失效——12条cron同时401
6月25日早上，12条cron同时failed。consecutiveErrors=1。根因：智谱API Key过期。

修复：换Key，但关键是加了fallback链。现在每条cron的model后面都跟着至少两个备选——zai/glm-4-flash → doubao → baidu。

教训：免费提供商的Key也会过期。永远有备选。这个教训现在写死在cron模板里了。

### 案例2：销售部/品牌部日报静默失败2天
consecutiveErrors涨到2。根因：isolated session用message工具直发飞书——isolated session没有飞书认证。message工具需要channel auth，只有main session有。

修复：所有部门日报从message工具切换到sessions_send。同时更新所有cron模板——在isolated session里禁止使用message工具。

教训：成功≠没问题。tool level的错误和configuration level的错误是两种东西。后来我们把"output file为空但cron返回ok"列入了巡检项。

### 案例3：7部门学习任务从未落地
MEMORY.md写着"每日学习07:30-08:30"，但cron从未创建。6月23日写到6月25日才发现。

教训：管理制度写在文件里≠cron创建了。现在每周巡检不仅要看cron有没有报错，还要看"应该存在的cron是否真的存在"。

### 案例4：讯飞4.0Ultra上下文溢出
3条cron连续失败，错误信息"Context length exceeded"。根因：讯飞模型上下文窗口小，lightContext设了但任务太重。

修复：切到deepseek-v4-pro + lightContext。后来全面梳理——所有内部运维cron加lightContext，大任务拆小。

教训：模型选型不只看价格。上下文窗口、速率限制、稳定性——这些都是"成本"。

---

## 六种失败模式（我们见过的）

### 模式A：Message Tool在Isolated Session
症状：`state.lastError`含"message failed"。cron设置是isolated session + delivery.mode=announce。
根因：isolated session缺channel认证。
修复：payload里改sessions_send，删掉delivery.mode。
**这个坑每个新用户都会踩一次。记住就行。**

### 模式B：Model Provider故障
症状：401/429/503，或"model not found"。
根因：Key过期/限流/服务宕机/模型下架。
修复：切换备选模型。每条cron至少两个fallback。
**免费模型也要备选。免费≠永不死。**

### 模式C：文件路径问题
症状：ENOENT、Write failed。
根因：模板变量在lightContext下不解析、目录不存在、权限不够。
修复：绝对路径或确保目录预建。
**isolated session的路径解析和main session不同。测试第一条cron的输出路径。**

### 模式D：上下文溢出
症状：token limit、输出截断、半成品文件。
根因：lightContext未开+任务太重。
修复：开lightContext或拆分任务。
**内部运维cron默认lightContext: true。不省这个钱。**

### 模式E：静默成功（最危险）
症状：consecutiveErrors=0、lastRunStatus=ok。但output文件为空或只写了"HEARTBEAT_OK"。
根因：Agent没有执行任务就退出了。payload写得太模糊。
修复：payload加"禁止回复HEARTBEAT_OK。必须写入文件后退出。无法完成任务时写入错误原因到文件而不是静默退出。"
**这个模式不会触发任何告警。只能靠巡查时打开output文件看内容。**

### 模式F：限流级联
症状：同一分钟的多条cron同时失败，错误信息含429或rate limit。
根因：调度表没有错峰或错峰不够。
修复：同提供商的cron最少隔2分钟。不同提供商最少隔1分钟。
**限流阈值会变。上个月的错峰这个月可能不够。每月复查一次。**

---

## 巡检制度

### 每周巡检（自动，周五22:00）
```
cron(action="list")
→ 逐条检查：
  - consecutiveErrors ≥ 2 → 标记异常，派数据中心修复
  - consecutiveErrors = 0 BUT output文件为空 → 标记静默失败
  - lastDurationMs > 历史平均×3 → 标记性能降级
  - 应该存在的cron少了一条 → 标记缺失
→ 输出巡检报告
```

### 巡检报告格式
```
检查总数：39
正常：36
异常：3
  1. [品牌部·每日汇报] consecutiveErrors=2 — 已派数据中心修复
  2. [财务部·学习] output为空 — 静默失败，已派数据中心诊断
  3. [销售部·日报] lastDurationMs异常(45s, 平均8s) — 性能降级
```

正常的不写。三个数字加异常详情。没有分析、没有建议、没有"可能"。巡检就是如实报告——决策是数据中心的，不是巡检的。

---

## 告警配置

```json
{
  "failureAlert": {
    "after": 2,
    "channel": "feishu",
    "to": "CEO",
    "cooldownMs": 3600000
  }
}
```

`after: 2` — 第二次失败才告警。瞬时问题（网络抖动、提供商标灵）会自动恢复。
`cooldownMs: 3600000` — 一小时最多一次告警。防止一个根因导致多条cron同时报警刷屏。

---

## 自动修复委派

检查发现问题→不自己修→派单给对应部门。

| 失败模式 | 派给谁 | 修复任务格式 |
|---------|--------|------------|
| Message Tool错误 | 数据中心 | 创建一次性cron：改payload为sessions_send |
| Model故障 | 数据中心 | 切换备选模型+更新fallback链 |
| 路径错误 | 行政部 | 建目录/改路径 |
| 上下文溢出 | 数据中心 | 开lightContext/拆分任务 |
| 限流级联 | 数据中心 | 调整错峰时间 |
| 静默成功 | 所属部门 | 改payload明确输出要求 |

修复任务是一次性cron：deleteAfterRun: true。修完自动消失。修不好的才上报CEO——且附带完整的"试了什么/为什么没成功"。

**修复验证**：下次巡检确认修复是否生效。修了但没好=白修。

---

## 发布铁律（双审制）

每次更新skill，两道闸：

**数据中心（技术审查）**：
- [ ] YAML frontmatter完整
- [ ] 无残留占位符
- [ ] 无真实API Key泄露
- [ ] 所有reference路径有效
- [ ] 大小≤40KB

**CEO（内容审查）**：
- [ ] 失败模式库准确（和实际运营对得上）
- [ ] playbook步骤可复现
- [ ] 公开传播安全（不暴露内部细节）
- [ ] 分层可用

双审通过才能publish。单检不发布。

---

## 升级节奏（周迭代）

```
每周六 10:00 数据中心检查
  ├─ 无变动 → 跳过
  ├─ 小修（加一条失败模式/改一段描述）→ +0.0.1 → GitHub
  ├─ 中改（加reference/加案例/加诊断流程）→ +0.1.0 → 双审 → publish
  └─ 大改（架构变化）→ CEO决策时机 → +1.0.0 → Release → publish
```

稳定优先。1.0.0跑得好就不急着推2.0。1.0.1、1.0.2慢慢加——每个数字代表一次经得起考验的改进。

---

## 从AI小白到深度玩家

**小白（第一天）**：部署每周巡检cron。看见第一个巡检报告。发现你之前没注意到的失败。震惊，然后安心——因为终于有人在看了。

**会用（第一周）**：你开始理解六种模式。不是死记——是你看到自己的cron失败模式对上号了："哦这个就是模式E，静默成功。"

**熟练（第一月）**：自动修复闭环在跑。你不需要手动修cron了。每周巡检报告上"已修复"越来越多，"待处理"越来越少。

**精通（第三月）**：你的系统连续一个月零异常。巡检报告上只有一个数字：检查数。你在帮别人搭他们的监控。你讲的不是cron-health-monitor的功能，是你自己踩过的坑——"那次12条cron同时401的时候我才发现免费提供商的Key也会过期。"

**大师（半年+）**：你发现了新的失败模式。你更新了playbook。你贡献回来，别人的cron因此少了一次事故。

---

## References

- [references/common-errors.md](references/common-errors.md) — 8种失败模式的完整诊断流程+真实错误信息
- [references/repair-playbook.md](references/repair-playbook.md) — A-F六类修复操作手册（含交叉修复案例）
