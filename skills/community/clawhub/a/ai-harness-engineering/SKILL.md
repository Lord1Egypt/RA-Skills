---
name: ai-harness-engineering
description: |
  AI驾驭工程错题本：记录OpenClaw所有被验证的错误、幻觉、缺陷、失误，形成可追溯错误台账，驱动模型自省与进化。
  
  触发场景：
  (1) 用户纠正OpenClaw的回答（"不对"/"错了"/"应该是"/"Actually"等）
  (2) OpenClaw回答与事实不符，被用户指出
  (3) 代码错误、逻辑错误被验证
  (4) 漏步骤、漏信息、回答不完整被指出
  (5) 格式错误、结构混乱
  (6) 安全问题、越权、误导行为
  (7) 用户明确要求"记录这个错误"/"添加到错题本"/"记住这个教训"
  (8) 用户想要但没有的功能（"能不能"/"希望你能"/"Is there a way"）
  (9) 用户查看错误统计/错题本/复盘报告
  
  ⚡ 自动进化机制（核心）：
  - 定时自动提升：每2小时检查recurrence_count>=3的学习，自动写入workspace
  - 错误摘要注入：session启动时自动读取错误台账摘要，注入到上下文
  - 回答前自检：每次回答前自动查询错误台账，规避已记录的错误
  
  关键词：错题本、错误记录、自省、进化、HarnessEngineering、错误台账、复盘、功能请求、Feature Request
metadata:
  openclaw:
    emoji: "🔧"
    always: true
    cron:
      # 每2小时自动检查并提升高频率学习
      auto_promote:
        schedule: "every 2h"
        task: "python3 {SKILL_DIR}/scripts/promote.py --action auto_promote"
      # 每周自动回顾
      weekly_review:
        schedule: "cron 0 9 * * 1"  # 每周一早上9点
        task: "python3 {SKILL_DIR}/scripts/review.py --action full_review"
---

# Harness Engineering - AI驾驭工程错题本

## 核心理念

**Harness Engineering（AI驾驭工程）**：AI时代程序员的核心工作不是写代码，而是设计规则、约束、反馈、调度体系，让AI安全、可靠、高效工作，同时持续修正AI错误。

本 skill 是 OpenClaw 的**自省机制**，记录所有被验证的错误和用户需求，形成错误台账，驱动模型进化，避免重复犯错。

---

## 一、核心功能概览

| 功能 | 说明 |
|------|------|
| **错误记录** | 记录所有被验证的错误、幻觉、失误 |
| **功能请求跟踪** | 跟踪用户想要但当前没有的功能 |
| **自动触发** | Hook机制自动检测纠正词和命令失败 |
| **自动提升** | 将重要学习提升到workspace文件 |
| **统计面板** | 可视化错误统计（今日/本周/本月/全部） |
| **错误模式库** | 12种常见错误模式供参考 |
| **定期回顾** | 周期性回顾机制，持续优化 |

---

## 二、存储结构

### 2.1 错误台账 (error_ledger.jsonl)

```json
{"error_id":"HE-20260401-0001","timestamp":"2026-04-01T12:34:56+08:00","scene":"代码","error_type":"代码错误","question":"用户原始问题","wrong_answer":"错误回答摘要","correct_answer":"正确答案","reason":"错误原因","fix_status":"未修复","level":"中","source":"用户纠正","tags":["代码","Python"]}
```

### 2.2 功能请求台账 (feature_ledger.jsonl)

```json
{"feature_id":"FR-20260401-0001","timestamp":"2026-04-01T12:34:56+08:00","feature_name":"功能名称","user_context":"用户为什么需要这个功能","complexity":"简单|中等|复杂","status":"pending","priority":"低|中|高","source":"用户请求"}
```

### 2.3 学习台账 (learnings_ledger.jsonl)

重要学习、纠正、知识差距、最佳实践都记录在这里。

```json
{"learning_id":"LRN-20260401-0001","timestamp":"2026-04-01T12:34:56+08:00","category":"correction|best_practice|knowledge_gap|simplify_harden","summary":"一句话描述","details":"详细上下文","suggested_action":"建议采取的行动","status":"pending|promoted|resolved","source":"conversation|error|user_feedback","pattern_key":"pattern.name","recurrence_count":1,"first_seen":"2026-04-01","last_seen":"2026-04-01","promoted_to":""}
```

### 2.4 Workspace提升目标

| 学习类型 | 提升到 |
|---------|--------|
| 行为模式、沟通风格 | `SOUL.md` |
| 工作流程、自动化 | `AGENTS.md` |
| 工具使用、集成技巧 | `TOOLS.md` |
| 项目事实、约定 | `MEMORY.md` |

---

## 三、自动触发机制

### 3.1 检测触发词

当用户发送以下内容时，**立即记录**：

**错误纠正**：
- "不对，应该是..."
- "错了，正确答案是..."
- "Actually, ..."
- "这样不对"
- "No, that's wrong..."
- "You're wrong about..."

**功能请求**：
- "能不能..." / "Can you also..."
- "希望你能..." / "I wish you could..."
- "Is there a way to..."
- "为什么不能..." / "Why can't you..."

**知识差距**：
- 用户提供了你不知道的信息
- 你引用的文档已过时
- API行为与你的理解不符

**命令失败**：
- 命令返回非零退出码
- 异常或堆栈跟踪
- 超时或连接失败

### 3.2 记录流程

1. **检测到触发词** → 立即记录
2. **生成唯一ID** → HE-YYYYMMDD-XXXX / FR-YYYYMMDD-XXXX / LRN-YYYYMMDD-XXXX
3. **写入对应台账** → error_ledger.jsonl / feature_ledger.jsonl / learnings_ledger.jsonl
4. **相似检测** → 检查是否有相似记录
5. **状态追踪** → 设置初始状态为"未处理"
6. **用户确认** → 回复用户已记录

---

## 四、自动进化机制（核心）

本 skill 实现了**闭环自进化**，通过以下三种机制确保错误不会重复：

### 4.1 定时自动提升（每2小时）

**原理**：当学习记录的 `recurrence_count >= 3` 时，自动写入 workspace 文件

**配置 Cron Job**：
```bash
# 每2小时自动检查并提升
python3 "{SKILL_DIR}/scripts/promote.py" --action auto_promote
```

**自动提升逻辑**：
```
if recurrence_count >= 3:
    if category == "correction":
        promote to SOUL.md  # 行为纠正
    elif category == "best_practice":
        promote to AGENTS.md  # 最佳实践
    elif category == "knowledge_gap":
        promote to MEMORY.md  # 知识更新
    else:
        promote to TOOLS.md  # 工具技巧
```

### 4.2 错误摘要注入（Session 启动时）

**原理**：每次 session 启动时，自动读取错误台账摘要并注入到上下文

**实现方式**：通过 OpenClaw system event 触发

```python
# 每次 session 启动自动执行
python3 "{SKILL_DIR}/scripts/inject_summary.py" --action session_start
```

**注入内容格式**：
```
【HarnessEngineering 错误台账摘要 - 最近5条】
1. [代码错误] 未指定文件编码导致乱码 (重复2次)
2. [逻辑错误] 条件判断遗漏边界情况 (重复3次) ⚠️ 需提升
3. [漏信息] 安装步骤漏写依赖安装

【已规避的错误模式】
- Python 3.12 未移除 GIL
- CSV 文件需使用 utf-8-sig 编码
```

### 4.3 回答前自检（每次回答时）

**原理**：在生成回答前，自动查询错误台账，如果涉及相似问题则参考正确答案

**实现方式**：定义在 SKILL.md 中的强制规则，每次回答前必须执行

**自检流程**：
```
1. 用户提问 → 提取关键词
2. 查询 error_ledger.jsonl 中相似问题 (相似度 > 50%)
3. 如果找到相似错误：
   - 提取 correct_answer 作为参考
   - 在回答开头标注 "[⚠️ 规避历史错误: HE-xxxx]"
4. 如果 recurrence_count >= 3：
   - 标记为"高频错误"，优先规避
5. 正常生成回答，但参考正确答案
```

**示例**：
```
用户问：Python 3.12 有什么新特性？

自检结果：发现相似错误 HE-20260401-0001
- 错误类型：事实错误
- recurrence_count: 2
- correct_answer: "Python 3.12 未移除 GIL，只是提供了 sub-interpreter 支持"

回答：[⚠️ 规避历史错误: HE-20260401-0001]
Python 3.12 的主要新特性包括：
1. ... (参考正确答案是未移除GIL)
```
   - 标记为"高频错误，需提升"
   - 在回答中标注 "[高频错误，已记录]"
```

### 4.4 自动进化工作流图

```
┌─────────────────────────────────────────────────────────────┐
│                    自动进化闭环                              │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  用户纠正错误 → 记录到 error_ledger.jsonl                    │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  Cron Job (每2小时)                                          │
│  → promote.py --action auto_promote                         │
│  → recurrence_count >= 3 → 自动写入 workspace               │
└─────────────────────────────────────────────────────────────┘
                            │
              ┌─────────────┼─────────────┐
              ▼             ▼             ▼
        SOUL.md       AGENTS.md      TOOLS.md
        (行为)         (工作流)       (工具)
              │
              ▼
┌─────────────────────────────────────────────────────────────┐
│  Session 启动 → inject_summary.py → 错误摘要注入上下文       │
└─────────────────────────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────────────────────┐
│  回答前 → pre_answer_check.py → 查询相似错误 → 规避         │
└─────────────────────────────────────────────────────────────┘
              │
              ▼
        【闭环完成：错误不再重复】
```

### 4.5 关键脚本说明

| 脚本 | 用途 | 触发时机 |
|------|------|---------|
| `promote.py --action auto_promote` | 定时自动提升 | Cron (每2小时) |
| `inject_summary.py` | 错误摘要注入 | Session 启动 |
| `pre_answer_check.py` | 回答前自检 | 每次回答前 |

---

## 五、错误分类体系

### 4.1 按错误类型（9种）

| 类型 | 说明 | 示例 |
|------|------|------|
| **幻觉** | 编造不存在的事实、API、库函数 | 声称不存在的npm包 |
| **事实错误** | 与已知事实不符 | 错误的API参数、版本号 |
| **逻辑错误** | 推理过程或结论错误 | 条件判断错误、循环逻辑错误 |
| **漏信息** | 回答不完整，遗漏关键步骤 | 安装步骤漏写依赖安装 |
| **格式错误** | 输出格式不符合要求 | CSV格式错误、JSON格式错误 |
| **代码错误** | 代码无法运行或有bug | 语法错误、类型错误 |
| **安全问题** | 潜在的安全风险 | SQL注入风险、敏感信息泄露 |
| **重复犯错** | 同类错误再次发生 | 已记录的错误再次出现 |
| **态度问题** | 回答态度不当 | 过度道歉、不必要防御 |

### 4.2 按严重等级（4级）

| 等级 | 说明 | 处理优先级 |
|------|------|-----------|
| **严重** | 导致数据丢失、安全问题、系统崩溃 | 立即修复 |
| **高** | 影响核心功能，用户无法完成任务 | 当日修复 |
| **中** | 影响用户体验，但有替代方案 | 本周修复 |
| **低** | 小问题，不影响使用 | 记录并持续优化 |

---

## 五、自动提升机制

### 5.1 提升条件

当满足以下任一条件时，**自动提升**到workspace文件：

- `recurrence_count >= 3` (同类错误出现3次以上)
- 学习具有**广泛适用性** (跨多个场景)
- 用户明确说"记住这个" / "Save this as..."
- `status` 标记为 `promoted`

### 5.2 提升目标

| 学习类型 | 提升目标 | 示例 |
|---------|---------|------|
| 行为模式 | `SOUL.md` | "Be concise, avoid disclaimers" |
| 工作流程 | `AGENTS.md` | "Spawn sub-agents for long tasks" |
| 工具技巧 | `TOOLS.md` | "Git push needs auth configured first" |
| 重要事实 | `MEMORY.md` | "用户偏好XX" |

### 5.3 提升流程

1. **识别提升条件** → 检查recurrence_count或广泛适用性
2. **蒸馏为规则** → 将冗长描述简化为简洁规则
3. **写入目标文件** → 添加到对应section
4. **更新原记录** → 状态改为 `promoted`，记录提升目标

### 5.4 提升示例

**原始学习**（冗长）：
> 项目使用 pnpm workspaces。尝试 `npm install` 但失败了。
> 锁文件是 `pnpm-lock.yaml`。必须用 `pnpm install`。

**提升到 AGENTS.md**（简洁）：
```markdown
## Build & Dependencies
- Package manager: pnpm (not npm) - use `pnpm install`
```

---

## 六、定期回顾机制

### 6.1 回顾时机

- 开始新的主要任务之前
- 完成一个功能之后
- 在有历史学习的领域工作时
- 每周活跃开发期间

### 6.2 回顾动作

1. **检查pending项** → `query_errors.py --status pending`
2. **解决已修复项** → 更新状态为 `resolved`
3. **提升适用学习** → 检查是否需要提升到workspace
4. **链接相关条目** → 添加 See Also 引用
5. **升级重复问题** → recurrence_count 增加

### 6.3 回顾脚本

```bash
# 检查pending项数量
python3 "{SKILL_DIR}/scripts/review.py" --action status

# 列出高优先级项
python3 "{SKILL_DIR}/scripts/review.py" --action high_priority

# 执行完整回顾
python3 "{SKILL_DIR}/scripts/review.py" --action full_review
```

---

## 七、功能请求跟踪

### 7.1 何时记录

用户表达想要但当前没有的功能时：
- "能不能加个XX功能"
- "Is there a way to do XX"
- "我希望你能XX"
- "This would be useful if..."

### 7.2 复杂度评估

| 复杂度 | 说明 |
|--------|------|
| **简单** | 现有代码修改即可实现 |
| **中等** | 需要新增文件或较大改动 |
| **复杂** | 需要架构调整或长期规划 |

### 7.3 功能请求处理

1. **记录到 feature_ledger.jsonl**
2. **评估复杂度**
3. **如果是简单功能**：可考虑直接实现
4. **如果是复杂功能**：标记为"规划中"，定期回顾

---

## 八、脚本接口

### 8.1 record_error.py - 记录错误

```bash
python3 "{SKILL_DIR}/scripts/record_error.py" \
  --scene <场景> \
  --error-type <错误类型> \
  --question <问题> \
  --wrong-answer <错误回答> \
  --correct-answer <正确答案> \
  --reason <原因> \
  --level <等级> \
  --source <来源> \
  [--tags <标签>]
```

### 8.2 record_learning.py - 记录学习

```bash
python3 "{SKILL_DIR}/scripts/record_learning.py" \
  --category <类型> \
  --summary <摘要> \
  --details <详情> \
  --suggested-action <建议> \
  --source <来源> \
  [--pattern-key <模式键>] \
  [--priority <优先级>]
```

### 8.3 record_feature.py - 记录功能请求

```bash
python3 "{SKILL_DIR}/scripts/record_feature.py" \
  --name <功能名称> \
  --context <用户场景> \
  --complexity <复杂度> \
  --priority <优先级>
```

### 8.4 query.py - 查询台账

```bash
# 按关键词查询错误
python3 "{SKILL_DIR}/scripts/query.py" --type errors --keywords "编码"

# 查询学习
python3 "{SKILL_DIR}/scripts/query.py" --type learnings --category correction

# 查询功能请求
python3 "{SKILL_DIR}/scripts/query.py" --type features --status pending

# 查询未处理项
python3 "{SKILL_DIR}/scripts/query.py" --type all --status pending
```

### 8.5 stats_panel.py - 统计面板

```bash
# 今日统计
python3 "{SKILL_DIR}/scripts/stats_panel.py" --period today

# 本周统计（带可视化）
python3 "{SKILL_DIR}/scripts/stats_panel.py" --period week

# 全部统计（JSON格式）
python3 "{SKILL_DIR}/scripts/stats_panel.py" --period all --format json
```

### 8.6 promote.py - 提升学习

```bash
# 提升到指定文件
python3 "{SKILL_DIR}/scripts/promote.py" \
  --learning-id LRN-20260401-0001 \
  --target SOUL.md

# 检查可提升项
python3 "{SKILL_DIR}/scripts/promote.py" --action check_candidates
```

### 8.7 update_status.py - 更新状态

```bash
# 标记为已解决
python3 "{SKILL_DIR}/scripts/update_status.py" \
  --type error \
  --id HE-20260401-0001 \
  --status resolved

# 标记为已提升
python3 "{SKILL_DIR}/scripts/update_status.py" \
  --type learning \
  --id LRN-20260401-0001 \
  --status promoted \
  --promoted-to "SOUL.md"
```

### 8.8 export_report.py - 导出报告

```bash
# 导出完整报告
python3 "{SKILL_DIR}/scripts/export_report.py" --output report.md

# 导出JSON格式
python3 "{SKILL_DIR}/scripts/export_report.py" --output report.json --format json

# 指定时间范围
python3 "{SKILL_DIR}/scripts/export_report.py" --output report.md --from 2026-04-01 --to 2026-04-30
```

### 8.9 review.py - 定期回顾

```bash
# 检查状态概览
python3 "{SKILL_DIR}/scripts/review.py" --action status

# 高优先级项
python3 "{SKILL_DIR}/scripts/review.py" --action high_priority

# 执行完整回顾
python3 "{SKILL_DIR}/scripts/review.py" --action full_review
```

---

## 九、检测触发词速查表

### 9.1 错误纠正触发词

```
英语：
- "No, that's not right..."
- "Actually, it should be..."
- "You're wrong about..."
- "That's incorrect..."
- "The correct answer is..."

中文：
- "不对，应该是..."
- "错了，正确答案是..."
- "这样不对"
- "你理解错了"
- "不是这样的"
```

### 9.2 功能请求触发词

```
英语：
- "Can you also..."
- "I wish you could..."
- "Is there a way to..."
- "It would be nice if..."
- "This would be useful if..."

中文：
- "能不能..."
- "希望你能..."
- "要是能...就好了"
- "能不能加个XX功能"
- "希望以后能支持..."
```

### 9.3 命令失败检测

当以下情况发生时自动记录：
- Exit code != 0
- 异常/堆栈跟踪出现
- Connection timeout
- Permission denied

---

## 十、文件结构

```
{SKILL_DIR}/
├── SKILL.md                              # 主文档
├── scripts/
│   ├── record_error.py                   # 记录错误
│   ├── record_learning.py                # 记录学习
│   ├── record_feature.py                 # 记录功能请求
│   ├── query.py                          # 查询台账
│   ├── stats_panel.py                    # 统计面板 ⭐
│   ├── promote.py                        # 自动提升 ⭐
│   ├── update_status.py                   # 更新状态
│   ├── export_report.py                  # 导出报告
│   └── review.py                         # 定期回顾 ⭐
├── data/
│   ├── error_ledger.jsonl               # 错误台账
│   ├── feature_ledger.jsonl              # 功能请求台账 ⭐
│   ├── learnings_ledger.jsonl             # 学习台账
│   └── error_index.json                  # 错误索引
└── references/
    └── error_patterns.md                 # 错误模式库 ⭐
```

---

## 十一、优势功能保留

### 11.1 统计面板 ⭐

一键生成可视化错误统计报告：
- 按类型/等级/状态分布
- 高频错误TOP 5
- 修复率统计
- 支持今日/本周/本月/全部周期

### 11.2 错误模式库 ⭐

12种常见错误模式：
1. CSV文件编码错误
2. bat/cmd脚本中文乱码
3. Python文件读写编码错误
4. 换行符不一致
5. 路径分隔符问题
6. 文件未关闭导致资源泄漏
7. 文件覆盖未备份
8. 边界条件遗漏
9. 空值处理缺失
10. API参数错误
11. 敏感信息泄露
12. SQL注入风险

### 11.3 自动相似检测

记录时自动检查相似错误（相似度>50%会提示），避免重复记录。

---

## 十二、快速开始

### 12.1 安装方法

#### 方法一：导入 .skill 文件（推荐）

```bash
# 1. 下载 harness-engineering.skill 文件
# 2. 在 OpenClaw 中导入：/skills install /path/to/harness-engineering.skill
```

#### 方法二：手动安装

```bash
# 1. 复制 skill 目录到 ~/.qclaw/skills/
cp -r harness-engineering/ ~/.qclaw/skills/

# 2. 创建数据目录
mkdir -p ~/.qclaw/skills/harness-engineering/data/

# 3. 创建空数据文件
touch ~/.qclaw/skills/harness-engineering/data/error_ledger.jsonl
touch ~/.qclaw/skills/harness-engineering/data/feature_ledger.jsonl
touch ~/.qclaw/skills/harness-engineering/data/learnings_ledger.jsonl
touch ~/.qclaw/skills/harness-engineering/data/error_index.json
```

#### 方法三：通过 ClawHub 安装（待发布）

```bash
/install harness-engineering
```

---

### 12.2 快速命令参考

#### 错误记录
```bash
python3 "{SKILL_DIR}/scripts/record_error.py" \
  --scene "问答" \
  --error-type "事实错误" \
  --question "用户问题" \
  --wrong-answer "错误回答" \
  --correct-answer "正确答案" \
  --reason "错误原因" \
  --level "高"
```

#### 学习记录
```bash
python3 "{SKILL_DIR}/scripts/record_learning.py" \
  --category correction \
  --summary "一句话摘要" \
  --details "详细上下文" \
  --suggested-action "建议行动" \
  --priority high
```

#### 功能请求
```bash
python3 "{SKILL_DIR}/scripts/record_feature.py" \
  --name "功能名称" \
  --context "用户场景" \
  --complexity "中等"
```

#### 查询台账
```bash
# 查询所有
python3 "{SKILL_DIR}/scripts/query.py" --type all

# 按关键词查询
python3 "{SKILL_DIR}/scripts/query.py" --type errors --keywords "Python"

# 查询未修复
python3 "{SKILL_DIR}/scripts/query.py" --type errors --status pending
```

#### 统计面板
```bash
# 今日统计
python3 "{SKILL_DIR}/scripts/stats_panel.py" --period today

# 本周统计
python3 "{SKILL_DIR}/scripts/stats_panel.py" --period week

# JSON 格式
python3 "{SKILL_DIR}/scripts/stats_panel.py" --period all --format json
```

#### 自动提升
```bash
# 检查可提升项
python3 "{SKILL_DIR}/scripts/promote.py" --action check_candidates

# 自动提升（recurrence_count >= 3）
python3 "{SKILL_DIR}/scripts/promote.py" --action auto_promote
```

#### 定期回顾
```bash
# 状态概览
python3 "{SKILL_DIR}/scripts/review.py" --action status

# 高优先级项
python3 "{SKILL_DIR}/scripts/review.py" --action high_priority

# 完整回顾
python3 "{SKILL_DIR}/scripts/review.py" --action full_review
```

#### 回答前自检
```bash
python3 "{SKILL_DIR}/scripts/pre_answer_check.py" --question "用户问题"
```

#### 错误摘要注入
```bash
python3 "{SKILL_DIR}/scripts/inject_summary.py" --action session_start
```

---

### 12.3 自动进化机制

#### Cron 定时任务（可选配置）

```yaml
# 在 OpenClaw 中配置定时任务
/cron add --name "harness-auto-promote" \
  --schedule "every 2h" \
  --task "python3 {SKILL_DIR}/scripts/promote.py --action auto_promote"

/cron add --name "harness-weekly-review" \
  --schedule "cron 0 9 * * 1" \
  --task "python3 {SKILL_DIR}/scripts/review.py --action full_review"
```

---

### 12.4 初始化

Skill首次使用时会自动创建必要的数据目录和文件：
- `data/error_ledger.jsonl`
- `data/feature_ledger.jsonl`
- `data/learnings_ledger.jsonl`
- `data/error_index.json`

### 12.5 日常使用流程

1. **被用户纠正** → 调用 record_error.py 记录到错误台账
2. **用户请求功能** → 调用 record_feature.py 记录到功能请求台账
3. **学到了新东西** → 调用 record_learning.py 记录到学习台账
4. **每次回答前** → 自动调用 pre_answer_check.py 自检
5. **session 启动时** → 自动调用 inject_summary.py 注入摘要
6. **每2小时** → Cron 自动调用 promote.py 提升高频学习
7. **每周** → Cron 自动调用 review.py 回顾
8. **需要查看统计** → 运行 stats_panel.py

### 12.3 示例对话

**用户纠正**：
> 你刚才说Python 3.12移除了GIL，这是错的。

**OpenClaw回复**：
> 感谢纠正！Python 3.12确实没有移除GIL。
>
> [自动调用 record_error.py]
>
> 已将此错误记录到错题本（HE-20260401-0002），后续回答涉及Python版本特性时会更加谨慎。

**用户请求功能**：
> 能不能加个自动总结会议纪要的功能？

**OpenClaw回复**：
> 这是个好建议！已记录到功能请求台账（FR-20260401-0001），我会持续关注相关实现方案。

---

## 十三、注意事项

### 13.1 隐私保护

- **不记录敏感信息**：密码、API密钥、Token等不记录
- **脱敏处理**：涉及个人信息时，用 `***` 替换

### 13.2 存储管理

- 台账文件超过1MB时，建议归档
- 定期清理已解决/已提升的记录（可选）

### 13.3 性能考虑

- 查询时优先使用索引
- 大量记录时使用 `--limit` 限制返回

---

**记住**：每个错误都是进化的机会，每个请求都是改进的方向。
**Harness Engineering：记录 → 学习 → 提升 → 进化** 🔧
