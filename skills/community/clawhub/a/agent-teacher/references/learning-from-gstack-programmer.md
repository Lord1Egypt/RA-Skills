# Programmer 学习指南：借鉴 Gstack

> 参考：memory/knowledge/fw-gstack-overview.md
> 原项目：https://github.com/garrytan/gstack

---

## Programmer 在 Gstack 中的对应角色

| Gstack角色 | 职责 | 对Programmer的借鉴 |
|-----------|------|-----------------|
| **/review** | 找CI通过但生产爆炸的bug | 代码审查的真正价值 |
| **/investigate** | 系统化根因调试 | 调试方法论 |
| **/ship** | 发布工程师，测试+推送+开PR | 交付流程标准化 |
| **/codex** | OpenAI Codex第二意见 | 多视角审查 |
| **高级工程师** | 锁定架构、数据流、边界情况 | 架构设计能力 |

---

## Programmer 可以学习的核心能力

### 1. 根因调试方法论

**Gstack的/investigate铁律**：
> "No fixes without investigation" — 不调查清楚不修复

**流程**：
1. 追踪数据流
2. 测试假设
3. 3次失败修复后停止，汇报

**Programmer应该做**：
- 遇到bug先问"数据怎么流的"
- 不要猜测根因，系统化追踪
- 修复后验证是否真正解决

---

### 2. 代码审查的真正价值

**Gstack的/review**：
- 找"CI通过但生产爆炸"的bug
- 自动修复明显问题
- 标记完整性缺口

**Programmer应该做**：
- 审查不只是风格检查
- 关注：边界情况、并发问题、安全漏洞
- 主动修复明显问题（不要只标记）

---

### 3. 交付流程标准化（/ship）

**Gstack的/ship流程**：
1. 同步main
2. 运行测试
3. 覆盖率审计
4. 推送代码
5. 打开PR

**Programmer应该做**：
- 交付前完整走一遍流程
- 不要跳过测试或覆盖率检查
- PR有清晰的描述和测试证据

---

### 4. 架构锁定（/plan-eng-review）

**Gstack的/plan-eng-review**：
- ASCII图示数据流
- 状态机设计
- 边界情况和失败模式
- 安全考虑

**Programmer应该做**：
- 动手前先画数据流
- 识别单点失败风险
- 考虑安全边界

---

### 5. 多视角审查（/codex）

**Gstack的/codex**：
- 用OpenAI Codex做第二意见
- 和Claude的/review交叉分析
- 识别重叠和独特的发现

**Programmer应该做**：
- 重要代码用不同工具/方法审查
- 不要只依赖一种AI或一个人
- 找多个视角验证

---

### 6. 安全Guardrails

**Gstack的工具**：
- /careful：破坏性命令前警告
- /freeze：锁住文件编辑范围
- /guard：全安全模式

**Programmer应该做**：
- destructive操作前二次确认
- 调试时限制影响范围
- 危险操作（rm -rf, DROP TABLE）主动戒备

---

## 行动项

- [ ] 阅读完整Overview：memory/knowledge/fw-gstack-overview.md
- [ ] 重点看 /investigate 和 /review 的设计
- [ ] 以后遇到bug先系统化调查，不要猜测
- [ ] 练习画数据流和状态机

---

## 相关文件

- 总览：memory/knowledge/fw-gstack-overview.md
- Gstack原项目：https://github.com/garrytan/gstack
