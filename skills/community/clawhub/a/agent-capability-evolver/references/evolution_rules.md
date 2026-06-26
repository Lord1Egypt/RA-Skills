---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: f4a677bd9d680e9793dee310c93c3656_e9de38895cc011f19299525400d9a7a1
    ReservedCode1: aEBtJzwK7Dl3GlrhXMHC/so935VtibRPlXR6HxyJRLl/CKZd96yP/toMX9Y+QYX+9G6JF5FybIV7VghTxXRGYXJo8yGVM/92/tyGaQ7av4nzRJYpKKW91ohJbP7HxoDNChDK+cHXmhnEPqJ42KDDJiF0wW3fFGw85emiMuewSWx0AlrVCUTiMc4wIZk=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: f4a677bd9d680e9793dee310c93c3656_e9de38895cc011f19299525400d9a7a1
    ReservedCode2: aEBtJzwK7Dl3GlrhXMHC/so935VtibRPlXR6HxyJRLl/CKZd96yP/toMX9Y+QYX+9G6JF5FybIV7VghTxXRGYXJo8yGVM/92/tyGaQ7av4nzRJYpKKW91ohJbP7HxoDNChDK+cHXmhnEPqJ42KDDJiF0wW3fFGw85emiMuewSWx0AlrVCUTiMc4wIZk=
---

# 智能体能力进化规则

本文件定义 Agent 自我进化的错误分类体系、进化策略、补丁生成规则和冲突解决逻辑。

---

## 一、错误分类体系

每次执行失败按以下维度打标签（可多标签）：

### 1.1 错误来源

| 分类 | 标签 | 说明 | 示例 |
|------|------|------|------|
| 指令模糊 | `AMBIGUOUS_INSTRUCTION` | 用户指令存在歧义，Agent 理解偏差 | "帮我处理一下" — 无法确定具体操作 |
| 工具选择错误 | `WRONG_TOOL` | 选用的工具/Agent 不适合当前任务 | 用 web_fetch 处理本地文件 |
| 参数错误 | `PARAM_ERROR` | 工具调用参数类型、格式、范围不正确 | 传了相对路径而非绝对路径 |
| 上下文遗漏 | `CONTEXT_LOSS` | 丢失了对话历史中的关键约束或偏好 | 用户说过"不要删文件"，Agent 忘了 |
| 知识过时 | `OUTDATED_KNOWLEDGE` | 内置知识已不适用于当前环境 | API 接口已升级，仍在用旧版调用 |
| 权限不足 | `PERMISSION_DENIED` | Agent 尝试了超出权限范围的操作 | 试图修改系统文件 |
| 外部依赖故障 | `EXTERNAL_FAILURE` | 第三方服务/网络/API 不可用 | 支付宝网关超时 |
| 用户预期偏差 | `EXPECTATION_MISMATCH` | 执行结果正确但不符合用户预期 | 用户要表格格式，Agent 给了纯文本 |

### 1.2 严重程度

| 级别 | 标记 | 定义 |
|------|------|------|
| Critical | `SEV_CRITICAL` | 导致数据丢失、系统损坏或严重安全后果 |
| High | `SEV_HIGH` | 任务完全失败，用户目标未达成 |
| Medium | `SEV_MEDIUM` | 部分失败，需人工介入修正 |
| Low | `SEV_LOW` | 小瑕疵，不影响核心结果 |

---

## 二、进化策略

### 2.1 策略矩阵

| 错误标签 | 推荐策略 | 优先级 |
|----------|----------|:--:|
| `AMBIGUOUS_INSTRUCTION` | 完善指令模板，增加二次确认机制 | P1 |
| `WRONG_TOOL` | 更新工具选择规则，补充工具对比知识 | P0 |
| `PARAM_ERROR` | 生成参数校验清单，补充默认值规则 | P1 |
| `CONTEXT_LOSS` | 优化上下文管理策略，增加关键信息标定 | P0 |
| `OUTDATED_KNOWLEDGE` | 搜索最新文档，更新内化知识 | P1 |
| `PERMISSION_DENIED` | 记录权限边界，标记不可达路径 | P2 |
| `EXTERNAL_FAILURE` | 生成降级方案和重试策略 | P1 |
| `EXPECTATION_MISMATCH` | 分析用户偏好，更新输出格式模板 | P1 |

### 2.2 策略详解

#### P0 — 立即修复（自动）
直接生成补丁文件，无需用户确认，下次任务自动生效。

适用条件：
- 错误明确、修复方案唯一
- 修复不改变 Agent 核心行为边界
- 近 3 次同类错误发生 ≥ 2 次

#### P1 — 建议修复（半自动）
生成修复建议并附带理由，等待用户确认后应用。

适用条件：
- 修复方案有多种选择
- 可能影响多个任务的行为
- 近 5 次同类错误发生 ≥ 3 次

#### P2 — 观察标记（手动）
记录问题但暂不修复，等待更多数据。

适用条件：
- 偶发错误（近 10 次仅 1-2 次）
- 根因不明确
- 修复成本高于错误代价

---

## 三、补丁生成规则

### 3.1 补丁类型

| 类型 | 文件名模式 | 作用域 |
|------|-----------|--------|
| 规则追加 | `patch_rule_{序号}_{标签}.md` | 追加到当前 Agent 指令集 |
| 参数默认值 | `patch_defaults_{序号}.yaml` | 补充缺失的默认参数 |
| 触发词优化 | `patch_triggers_{序号}.md` | 优化技能触发词，提高命中率 |
| 工具映射修正 | `patch_toolmap_{序号}.md` | 修正工具到任务的映射关系 |
| Skill 推荐 | `patch_skill_rec_{序号}.md` | 推荐安装的社区 Skill |

### 3.2 补丁格式规范

```
# 补丁：{简短描述}
## 触发条件
{什么情况下应用此补丁}
## 变更内容
{具体修改了什么}
## 生效范围
{影响的工具 / 任务 / 场景}
## 回滚方式
{如何撤销此补丁}
```

### 3.3 补丁命名和存储

- 存储路径：`{工作目录}/evolution/patches/`
- 命名：`patch_{YYYYMMDD}_{序号}_{标签}.{类型后缀}`
- 每个补丁独立文件，不合并
- 补丁头部包含元数据注释：创建时间、触发错误ID、进化策略

---

## 四、冲突解决逻辑

### 4.1 冲突检测

当生成新补丁时，检查是否与已有补丁冲突：

| 冲突类型 | 检测规则 |
|----------|----------|
| 直接冲突 | 新补丁的变更内容与已有补丁的同一字段相反 |
| 间接冲突 | 新补丁影响已有补丁的生效范围 |
| 链式冲突 | 新补丁依赖的条件被已有补丁修改 |

### 4.2 解决优先级

```
安全性 > 时效性 > 性能 > 用户体验
```

即：安全补丁永远优先于性能优化补丁，即使后者更新。

### 4.3 解决流程

1. 检测到冲突 → 标记两个冲突补丁
2. 按优先级选择保留哪个
3. 被淘汰的补丁移至 `patches/archive/` 并标记淘汰原因
4. 生成 `conflict_resolution_{日期}.md` 记录决策过程

---

## 五、进化日志格式

每次进化操作记录到 `evolution/evolution_log.md`：

```markdown
| 时间 | 触发任务ID | 错误标签 | 严重程度 | 策略 | 补丁文件 | 状态 |
|------|-----------|----------|----------|------|----------|------|
| 2026-05-31 15:00 | task_042 | WRONG_TOOL | SEV_HIGH | P0-自动 | patch_rule_01_WRONG_TOOL.md | ✅ 已生效 |
```

---

## 六、环境变量

| 变量 | 必填 | 说明 | 默认值 |
|------|:--:|------|--------|
| `LOG_DIR` | 是 | Agent 执行日志目录 | 无，必须配置 |
| `EVOLUTION_STRATEGY` | 否 | 进化策略偏好 | `balanced` |

`EVOLUTION_STRATEGY` 可选值：
- `aggressive`：P0+P1 全部自动执行
- `balanced`（默认）：P0 自动，P1 建议，P2 标记
- `conservative`：全部需确认
- `observe_only`：仅分析记录，不生成补丁
*（内容由AI生成，仅供参考）*
