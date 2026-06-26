---
name: code-quality-analyzer
description: 代码质量分析技能，用于分析代码仓库的周/月维度变更，生成交付报告并同步到代码质量分析系统数据库。触发场景：(1) 用户要求进行代码质量分析 (2) 生成周报/月报 (3) 统计代码变更 (4) 分析分支提交 (5) 同步分析数据到数据库。
---

# 代码质量分析技能

分析代码仓库的变更情况，生成结构化报告并同步到数据库。

## ⚠️⚠️⚠️ 强制检查清单 - 每次分析必须逐项确认 ⚠️⚠️⚠️

**不按这个清单执行 = 必然犯错**

### 周维度检查清单

```
□ 0. ⚠️ 第一步：git fetch 拉取所有项目最新变更！！！
□ 1. 周期值：用周四日期，不是当天（例：2026-03-24周一 → 周期值 20260326）
□ 2. 分支匹配：按日期匹配分支名
□ 3. 统计逻辑：找版本分支从源分支切出后的所有提交
□ 4. ⭐ AI 质量评分：自己分析评分（同步前执行）
□ 5. ⭐ AI 代码审查：生成 code_issues 数据（同步前执行）
□ 6. 同步数据：一次性同步所有数据（分析+评分+审查+commits+统计）
□ 7. 提交类型：存储中文
□ 8. fileChanges 字段：必须填充文件变更明细（不能为空数组）
□ 9. commits 数据：必须写入 code_reviews 表
□ 10. 统计数据：必须同步 team_statistics 和 project_statistics
□ 11. 验证前端：确认正确显示（大盘、类型分布、问题明细、提交记录）
```

### 数据同步顺序（重要！）

```
1. code_analyses - 分析记录（含 fileChanges）
2. code_issues - AI代码审查问题
3. code_reviews - 提交记录详情
4. team_statistics - 团队统计
5. project_statistics - 项目统计
```

### ⚠️ 常见遗漏问题（必读！）

| 问题 | 后果 | 解决方案 |
|------|------|---------|
| fileChanges 为空 | 类型分布空 | 分析脚本必须收集 fileChangesList |
| code_issues 无数据 | 问题与建议空 | 必须执行 AI 代码审查，写入 code_issues 表 |
| code_reviews 无数据 | 提交记录详情空 | 必须同步 commits 到 code_reviews 表 |
| team_statistics 无数据 | 大盘视图为0 | 必须同步统计数据 |
| AI 评分缺失 | 评分显示默认值 | 必须更新 ai_quality_score 和 ai_quality_report |

### 周维度 vs 月维度核心区别

| 维度 | 周期值 | 分支匹配 | 变更统计 |
|------|--------|---------|---------|
| 周维度 | YYYYMMDD（周四） | 找版本分支 | 从源分支切出后的所有提交 |
| 月维度 | YYYYMM | **不需要** | 该月所有提交（所有分支） |

---

## 一、核心配置

| 配置项 | 值 |
|--------|-----|
| 周期值规则 | 周维度：周四日期（YYYYMMDD）；月维度：月份（YYYYMM） |
| 项目目录 | `/Users/zhangdi/work/codeCap/codebase/` |
| 数据库 API | `http://localhost:3000/api/v1` |
| 团队 ID | `team-42e79f51`（运营前端组） |
| 分析脚本 | `/Users/zhangdi/work/codeCap/代码质量分析系统/scripts/analyze-code-v2.js` |
| 同步脚本 | `/Users/zhangdi/work/codeCap/代码质量分析系统/scripts/sync-to-db.js` |
| Teams 通知脚本 | `/Users/zhangdi/work/codeCap/代码质量分析系统/scripts/notify-teams.js` |
| 邮件通知脚本 | `/Users/zhangdi/work/codeCap/代码质量分析系统/code-quality-backend/scripts/notify-email.js` |
| 邮件配置文件 | `~/.openclaw/workspace/.email-config.json` |
| 机器人名称 | 质检君 |
| Teams Webhook | 加签模式，secret 已配置 |

---

## 二、分支匹配规则

### 2.1 分支查找优先级

```javascript
// 1. 精确匹配：分支名包含周期值
branches.find(b => b.includes(periodValue))  // 如 feature/xxx-20260326

// 2. 范围匹配：分支名包含本周日期（周一到周五）
// 如果精确匹配失败，遍历本周日期查找

// 3. 不用 --all：只统计匹配的分支，不是所有分支
```

### 2.2 获取分支变更（关键！）

**周维度**：统计版本分支从源分支切出后的所有提交

**月维度**：统计该月该项目的所有提交（时间范围）

---

#### 周维度逻辑

```bash
# 1. 首先尝试分支差异（版本分支未合并）
git shortlog -sne origin/develop..origin/feature-20260326

# 2. 如果差异为空（版本分支已合并），找版本分支的开发提交
#    找版本分支上最近一次 merge commit（从上一个版本 merge 的）
git log origin/feature --merges --format="%H" --grep="release|Merge" | head -1

# 3. 统计从那个 merge 之后到版本分支最新提交
git shortlog -sne <merge-commit>..origin/feature
```

---

#### 月维度逻辑（更简单）

**不需要找目标分支！直接统计该月的所有提交。**

```bash
# 统计该项目在某月的所有提交（所有分支）
git log --all --since="2026-02-01" --until="2026-03-01" --oneline

# 获取用户列表
git shortlog -sne --all --since="2026-02-01" --until="2026-03-01"

# 获取某用户的提交详情
git log --author="user@email" --all --since="2026-02-01" --until="2026-03-01" --pretty=format:"%h|%ai|%s"
```

**日期范围**：

| 月份 | 开始日期 | 结束日期 |
|------|---------|---------|
| 202602 | 2026-02-01 | 2026-03-01 |
| 202603 | 2026-03-01 | 2026-04-01 |

**关键命令**：

```bash
# 月度统计（使用 --all 包含所有分支）
git shortlog -sne --all --since="${monthStart}" --until="${monthEnd}"
```

### 2.3 源分支识别

```javascript
// 可能的源分支优先级
const possibleSources = ['develop', 'master', 'main', 'release', 'staging'];

// 从分支名推断源分支（如 feature/xxx 从 develop 切出）
// 遍历检查哪个源分支存在 merge-base
```

---

## 三、数据格式约定

### 3.1 提交类型映射（必须存中文）

| 英文前缀 | 中文类型 |
|----------|----------|
| feat | 新功能 |
| fix | Bug修复 |
| refactor | 重构 |
| style | 样式 |
| test | 测试 |
| docs | 文档 |
| chore | 杂项 |
| perf | 性能优化 |
| other/其他 | 其他 |

**同步脚本示例**：

```javascript
function getCommitType(message) {
  if (!message) return '其他';
  if (message.startsWith('feat')) return '新功能';
  if (message.startsWith('fix')) return 'Bug修复';
  if (message.startsWith('refactor')) return '重构';
  if (message.startsWith('style')) return '样式';
  if (message.startsWith('test')) return '测试';
  if (message.startsWith('docs')) return '文档';
  if (message.startsWith('chore')) return '杂项';
  if (message.startsWith('perf')) return '性能优化';
  return '其他';
}
```

### 3.2 AI 质量报告格式

```
## 代码质量报告

### 总体评价：{优秀|良好|一般|较差}

### 评分：{N.N}/10

### 主要问题
1. {问题描述}
2. {问题描述}

### 改进建议
1. {建议内容}
2. {建议内容}

### 亮点
1. {亮点内容}
2. {亮点内容}
```

**解析规则**：
- 有内容时必须用 `1. xxx` 格式
- 无内容时写 `暂无xxx`

### 3.3 任务号提取

```javascript
function extractTaskIds(message) {
  const match = message.match(/\(([A-Z]+-\d+)\)/);
  return match ? [match[1]] : [];
}

// 示例
// "feat(API-9933): 用户参与活动奖品查询优化" → ["API-9933"]
// "fix(JKRISK-1734): 优惠券处理" → ["JKRISK-1734"]
```

---

## 四、排除文件规则

**统计代码变更时必须排除以下文件**：

| 文件类型 | 示例 |
|----------|------|
| Lock 文件 | `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml` |
| 依赖目录 | `node_modules/` |
| 构建产物 | `dist/`, `build/` |
| 压缩文件 | `.min.js`, `.min.css` |
| 类型声明 | `.d.ts` |

```javascript
const excludePatterns = [
  /package-lock\.json$/,
  /yarn\.lock$/,
  /pnpm-lock\.yaml$/,
  /node_modules\//,
  /\.min\.(js|css)$/,
  /dist\//,
  /build\//,
  /\.d\.ts$/
];

function shouldExclude(file) {
  return excludePatterns.some(p => p.test(file));
}
```

---

## 五、用户管理规则

### 5.1 用户必须在小组管理中预先添加

```
┌─────────────────────────────────────────────────────────────┐
│  正确流程                                                    │
├─────────────────────────────────────────────────────────────┤
│  1. 用户在「小组管理」中手动添加成员                          │
│     → 用户写入 users 表，关联 teamId                         │
│                                                              │
│  2. 运行分析脚本时获取用户列表                                │
│     → 只统计已添加用户的提交                                  │
│                                                              │
│  3. 未匹配的提交直接跳过，不创建新用户                        │
└─────────────────────────────────────────────────────────────┘
```

### 5.2 用户匹配规则

```javascript
// 1. 精确匹配
if (userMap.has(gitUsername)) return userMap.get(gitUsername);

// 2. 右侧匹配（处理前缀如 j-zhaojiannan-jk → zhaojiannan-jk）
for (const [dbUsername, dbId] of userMap.entries()) {
  if (gitUsername === dbUsername || gitUsername.endsWith(dbUsername)) {
    return dbId;
  }
}

// 3. 邮箱匹配
const emailPrefix = email.split('@')[0];
if (userMap.has(emailPrefix)) return userMap.get(emailPrefix);
```

---

## 六、AI 质量评分

### 6.1 评分原则

**AI 评分由 AI 助手自己完成，不调用外部 API！**

评分标准（满分 10 分）：

| 维度 | 权重 | 评估标准 |
|------|------|---------|
| 代码规范 | 20% | Commit message 规范性、任务关联 |
| 可维护性 | 25% | 重构意识、代码结构优化 |
| 代码质量 | 25% | 功能实现、错误处理 |
| 提交质量 | 15% | 提交粒度、类型分布 |
| 工作量 | 15% | 代码产出量、任务完成数 |

### 6.2 评分示例

```javascript
const scores = {
  'zhangdi-jk@lego-nuxt': {
    score: 8.8,
    evaluation: '优秀',
    issues: ['提交数量较少，可以适当增加提交频率'],
    suggestions: ['继续保持高质量的提交习惯'],
    advantages: ['代码净增长高，有效产出多', '有 style 和 refactor 类型提交', 'Commit message 规范且详细']
  }
};

function generateReport(data) {
  return `## 代码质量报告

### 总体评价：${data.evaluation}

### 评分：${data.score}/10

### 主要问题
${data.issues.map((i, idx) => `${idx + 1}. ${i}`).join('\n')}

### 改进建议
${data.suggestions.map((s, idx) => `${idx + 1}. ${s}`).join('\n')}

### 亮点
${data.advantages.map((a, idx) => `${idx + 1}. ${a}`).join('\n')}`;
}
```

---

## 七、数据同步策略

### 7.1 增量覆盖原则

```
❌ 禁止清空整个数据库
✅ 只覆盖同一周期的数据
```

### 7.2 同步前检查

```
□ 1. 确认只删除本周期的数据
      DELETE FROM code_analyses WHERE period_type = 'week' AND period_value = '20260326'
      
□ 2. 检查是否需要保留已有数据（如 AI 评分）
      如果会覆盖重要数据，先备份

□ 3. 同步完成后验证历史数据完好
```

### 7.3 同步顺序

```sql
-- 1. 先删除关联数据
DELETE FROM code_reviews WHERE analysis_id IN (
  SELECT id FROM code_analyses WHERE period_type = ? AND period_value = ?
);

-- 2. 删除分析记录
DELETE FROM code_analyses WHERE period_type = ? AND period_value = ?;

-- 3. 删除统计
DELETE FROM project_statistics WHERE period_type = ? AND period_value = ?;
DELETE FROM team_statistics WHERE period_type = ? AND period_value = ?;

-- 4. 写入新数据
INSERT INTO code_analyses ...
INSERT INTO code_reviews ...
INSERT INTO project_statistics ...
INSERT INTO team_statistics ...
```

---

## 八、常见错误清单

### 错误 1：分析前没有 git fetch

**后果**：分支列表过时，找不到正确的版本分支。

**解决**：分析脚本第一步必须是 `git fetch`。

### 错误 2：同步数据覆盖了 AI 评分

**后果**：之前手动设置的评分被重置为默认值。

**解决**：同步前检查是否需要保留已有数据，必要时先备份。

### 错误 3：提交类型存英文而不是中文

**后果**：前端显示类型不一致（有的显示中文，有的显示英文）。

**解决**：同步脚本必须返回中文类型。

### 错误 4：周期值用当天日期而不是周四

**后果**：找不到正确的版本分支。

**解决**：周期值永远是那周的周四日期。

### 错误 5：分支差异为空时没有备用方案

**后果**：已合并分支的数据丢失。

**解决**：使用 `develop^1` 或时间范围作为备用。

### 错误 6：用户管理自动创建用户

**后果**：产生垃圾数据，用户名可能匹配错误。

**解决**：用户必须在小组管理中预先添加。

### 错误 7：AI 评分调用外部 API

**后果**：API Key 未配置时返回默认值。

**解决**：AI 评分由 AI 助手自己完成，不调用外部 API。

### 错误 8：数据格式不一致

**后果**：前端解析错误或显示异常。

**解决**：严格按照本文档的数据格式约定执行。

---

## 九、数据库表结构

### code_analyses（核心分析数据）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | UUID | 主键 |
| user_id | UUID | 用户 ID |
| project_id | UUID | 项目 ID |
| period_type | string | week / month |
| period_value | string | 周期值（YYYYMMDD 或 YYYYMM） |
| commit_count | int | 提交数 |
| insertions | int | 新增行 |
| deletions | int | 删除行 |
| files_changed | int | 变更文件数 |
| task_count | int | 任务数 |
| branch | string | 分支名 |
| ai_quality_score | float | AI 评分 |
| ai_quality_report | text | AI 报告 |

### code_reviews（提交记录）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | UUID | 主键 |
| analysis_id | UUID | 关联的分析 ID |
| commit_hash | string | 提交哈希 |
| commit_message | text | 提交信息 |
| commit_date | timestamp | 提交时间 |
| review_result | JSON | { insertions, deletions, type } |

### team_statistics（团队统计）

| 字段 | 类型 | 说明 |
|------|------|------|
| team_id | UUID | 团队 ID |
| period_type | string | week / month |
| period_value | string | 周期值 |
| total_members | int | 总成员数 |
| active_members | int | 活跃成员数 |
| total_commits | int | 总提交数 |
| avg_quality_score | float | 平均质量分 |

### project_statistics（项目统计）

| 字段 | 类型 | 说明 |
|------|------|------|
| project_id | UUID | 项目 ID |
| period_type | string | week / month |
| period_value | string | 周期值 |
| total_contributors | int | 贡献者数 |
| total_commits | int | 总提交数 |
| avg_quality_score | float | 平均质量分 |

---

## 十、完整分析流程

```
1. 执行检查清单（逐项确认）
   ↓
2. git fetch 拉取所有项目最新变更
   ↓
3. 遍历项目，查找匹配的版本分支
   ↓
4. 找到源分支（develop/master）
   ↓
5. 获取分支差异（使用 develop^1 备用）
   ↓
6. 统计每条提交：
   - 增删行数（排除 lock 文件）
   - 提交类型（存中文）
   - 任务号
   ↓
7. 按用户+项目聚合
   ↓
8. 保存分析结果到文件
   ↓
9. 同步数据到数据库：
   - 检查是否需要保留已有数据
   - 只删除本周期的旧数据
   - 写入新数据
   ↓
10. AI 质量评分（自己完成）
   ↓
11. ⭐ 代码逐行审查（自动切换到 kimi-k2.5 模型）
   ↓
12. 存储审查结果到数据库
   ↓
13. 验证历史数据完好
   ↓
14. 验证前端显示正确
```

---

## 十点五、代码逐行审查（自动切换模型）

### 流程说明

在代码质量分析的评审环节，**自动切换到 kimi-k2.5 模型** 进行详细的代码逐行审查。

### 为什么切换模型？

| 模型 | 适合场景 |
|------|---------|
| glm-5（默认） | 日常对话、数据同步、简单分析 |
| kimi-k2.5 | 长文本理解、代码深度分析、复杂推理 |

kimi-k2.5 拥有 262k 上下文窗口，适合处理大量代码变更的详细审查。

### 调用方式

```typescript
// 在代码审查环节，自动 spawn 子任务
sessions_spawn({
  model: "bailian/kimi-k2.5",
  task: `对 ${projectName} 项目的本周代码变更进行逐行审查。

审查范围：${branchName}
变更文件：${fileList}
变更行数：+${insertions}/-${deletions}

请按照以下维度进行审查：
1. Security - 安全性问题
2. Performance - 性能问题
3. Correctness - 正确性问题
4. Maintainability - 可维护性问题
5. Testing - 测试覆盖

输出格式：
| 文件 | 行号 | 问题类型 | 严重程度 | 描述 | 建议 |
`,
  cwd: projectPath
})
```

### 审查结果处理

审查完成后，将结果存入 `code_issues` 表：

```sql
INSERT INTO code_issues (
  analysis_id, file_path, line_start, line_end,
  issue_type, severity, description, suggestion
) VALUES (?, ?, ?, ?, ?, ?, ?, ?);
```

### 自动化流程

```
主任务（glm-5）：
  └── 分析代码变更
  └── 同步数据到数据库
  └── 评分
  └── 🔄 spawn 子任务（kimi-k2.5）
        └── 获取 git diff
        └── 逐行审查代码
        └── 识别问题
        └── 返回结构化结果
  └── 接收审查结果
  └── 存入数据库
```

---

## 十一、相关文件路径

| 文件 | 路径 |
|------|------|
| 分析脚本 | `/Users/zhangdi/work/codeCap/代码质量分析系统/scripts/analyze-code-v2.js` |
| 同步脚本 | `/Users/zhangdi/work/codeCap/代码质量分析系统/scripts/sync-to-db.js` |
| 通知脚本 | `/Users/zhangdi/work/codeCap/代码质量分析系统/scripts/notify-teams.js` |
| 分析输出 | `/Users/zhangdi/work/codeCap/代码质量分析系统/analysis-output/analysis-YYYYMMDD.json` |
| 后端服务 | `/Users/zhangdi/work/codeCap/代码质量分析系统/code-quality-backend/` |
| 前端服务 | `/Users/zhangdi/work/codeCap/代码质量分析系统/code-quality-frontend/` |

---

## 十二、周维度分支差异的正确逻辑

### 问题

当 feature 分支已合并到 develop 时，`git log develop..feature` 可能返回空，但这并不意味着没有数据。

### 正确命令

```bash
# 这条命令不管 feature 是否合并都能正确工作
git log origin/feature --not origin/develop --oneline

# 或者更完整的写法
git log origin/develop..origin/feature --oneline  # feature 未合并时
git log origin/feature --not origin/develop --oneline  # 任何情况都适用
```

### 原理

- `--not origin/develop` 排除所有在 develop 上的提交
- 剩下的就是 feature 分支独有的提交
- 即使 feature 合并到 develop 后，这条命令依然有效

---

## 十三、代码审查功能

### 概述

代码审查由 AI 助手直接完成，不需要调用外部 AI API。

### 审查流程

```
1. 获取变更文件列表
   git diff origin/develop..origin/feature --name-only
   
2. 获取具体代码变更
   git diff origin/develop..origin/feature -- "path/to/file.tsx"
   
3. AI 审查代码变更，识别问题：
   - 安全性问题
   - 性能问题
   - 代码正确性
   - 可维护性
   - 测试覆盖
   
4. 生成结构化问题明细
   
5. 存入数据库 / 展示给用户
```

### 数据库扩展

```sql
-- 新增问题明细表
CREATE TABLE code_issues (
  id UUID PRIMARY KEY,
  analysis_id UUID REFERENCES code_analyses(id),
  file_path VARCHAR(500),
  line_number INT,
  issue_type VARCHAR(50),
  severity VARCHAR(20),  -- P0/P1/P2
  description TEXT,
  suggestion TEXT,
  code_snippet TEXT,
  created_at TIMESTAMP
);
```

### 审查报告格式

```markdown
## 🔍 项目名 本周代码审查报告

### 概览

| 文件类型 | 文件数 | 变更行数 |
|---------|--------|---------|
| 新增文件 | N | +XXX |
| 修改文件 | N | +XXX/-XXX |
| **总计** | **N** | **+XXX/-XXX** |

### 主要变更模块

| 模块 | 变更量 | 描述 |
|------|--------|------|
| 模块名 | +XXX | 描述 |

---

### 问题明细

#### 文件 1: `path/to/file.tsx` (+XXX/-XXX)

| # | 行号 | 问题类型 | 严重程度 | 问题描述 | 修改建议 |
|---|------|---------|---------|---------|---------|
| 1 | 行号 | 问题类型 | P0/P1/P2 | 问题描述 | 修改建议 |

**具体代码示例**：

```typescript
// 当前代码
问题代码

// 建议修改
修改后代码
```

---

### 共性问题汇总

| 问题类型 | 出现次数 | 涉及文件 |
|---------|---------|---------|
| 问题类型 | N | 文件列表 |

---

### 亮点

| 亮点 | 描述 |
|------|------|
| ✅ 亮点 | 描述 |

---

### 执行优先级

| 优先级 | 问题 | 理由 |
|--------|------|------|
| P0 | 问题 | 理由 |
| P1 | 问题 | 理由 |
| P2 | 问题 | 理由 |
```

---

## 十四、结合 code-review 技能

### 审查维度

参考 `skills/code-review/SKILL.md`，按以下维度系统化审查：

| 维度 | 检查项 | 优先级 |
|------|--------|--------|
| Security | SQL注入、XSS、CSRF、认证授权 | Critical |
| Performance | N+1查询、内存泄漏、懒加载 | High |
| Correctness | 空值处理、边界情况、竞态条件 | High |
| Maintainability | 命名、单一职责、DRY | Medium |
| Testing | 测试覆盖、边界测试 | Medium |

### 严重程度标签

| 级别 | 标签 | 含义 | 阻塞合并 |
|------|------|------|---------|
| P0 | 阻塞 | 严重问题，必须修复 | 是 |
| P1 | 阻塞 | 重要问题，应该修复 | 是 |
| P2 | 不阻塞 | 改进建议 | 否 |

### 三遍审查法

| 遍数 | 重点 | 时间 |
|------|------|------|
| 第一遍 | 高层结构、架构设计 | 2-5 分钟 |
| 第二遍 | 逐行细节、问题识别 | 主要时间 |
| 第三遍 | 边界情况、遗漏检查 | 5 分钟 |

---

## 十五、审查示例

### lego-nuxt 本周审查报告示例

**审查范围**: `feature/lego-nuxt4.12.0_20260326`

| 文件 | 变更行数 | 问题数 |
|------|---------|--------|
| ComponentsManager.vue | +679/-1 | 4 |
| activity/index.vue | +466/-1 | 3 |
| mobile/Mixin/index.js | +54 | 2 |

**问题示例**：

| # | 行号 | 问题类型 | 严重程度 | 问题描述 | 修改建议 |
|---|------|---------|---------|---------|---------|
| 1 | 29-42 | 代码重复 | P2 | 双击编辑逻辑重复绑定 | 提取为独立组件 |
| 2 | 97-100 | 无障碍问题 | P1 | 统计图标缺少 aria-label | 添加无障碍属性 |
| 3 | 245-248 | 未使用导入 | P2 | 引入了 echarts 但未检查加载 | 添加错误处理 |

### dove_digital 本周审查报告示例

**审查范围**: `feature/iopsfe2.67.0-20260326` (40 files, +8,122/-1,551)

**问题示例**：

| # | 行号 | 问题类型 | 严重程度 | 问题描述 | 修改建议 |
|---|------|---------|---------|---------|---------|
| 1 | 全文 | 代码可维护性 | P0 | 单文件 2000+ 行 | 拆分为多个子组件 |
| 2 | 多处 | 硬编码常量 | P2 | AI 模型类型硬编码 | 提取为配置文件 |
| 3 | 39 | 错误处理不完整 | P1 | catch 只显示 message | 添加 error 状态 |
| 4 | 68 | JSON 解析错误 | P1 | JSON.parse 无错误处理 | 添加 try-catch |

---

## 十六、⚠️⚠️⚠️ 错误案例库（必读！防止重复犯错）

### 案例 1：fileChanges 字段名不一致（2026-03-28）

**错误现象**：个人代码评审详情页，文件变更明细列表文件名为空

**错误原因**：
- 分析脚本生成 `file` 字段
- 历史数据使用 `path` 字段
- 前端使用 `file.path` 读取

**正确做法**：
```javascript
// ❌ 错误：使用 file 字段
fileChangesList.push({ file, insertions, deletions });

// ✅ 正确：使用 path 字段，与历史数据保持一致
fileChangesList.push({ path: file, language: 'Vue', insertions, deletions });
```

**教训**：修改数据结构前，必须先检查历史数据的字段结构！

---

### 案例 2：同步时遗漏 code_reviews 表（2026-03-28）

**错误现象**：提交记录详情为空

**错误原因**：同步数据时只写入了 `code_analyses`，忘记写入 `code_reviews`

**正确做法**：
```javascript
// 同步流程必须包含：
// 1. code_analyses（分析记录）
// 2. code_issues（AI代码审查问题）
// 3. code_reviews（提交记录详情）⚠️ 容易遗漏！
// 4. team_statistics（团队统计）
// 5. project_statistics（项目统计）
```

**教训**：每次同步必须按照完整的数据同步顺序执行，不能跳过任何一张表！

---

### 案例 3：同步时遗漏统计表（2026-03-28）

**错误现象**：大盘视图数据全部为 0

**错误原因**：没有同步 `team_statistics` 和 `project_statistics` 表

**正确做法**：
```sql
-- 同步完成后必须执行：
INSERT INTO team_statistics (team_id, period_type, period_value, total_members, ...)
INSERT INTO project_statistics (project_id, period_type, period_value, total_contributors, ...)
```

**教训**：大盘视图依赖统计表，必须同步！

---

### 案例 4：AI 评分和 AI 代码审查遗漏（2026-03-28）

**错误现象**：AI评分显示默认值，问题与建议为空

**错误原因**：
- 只运行了分析脚本和同步脚本
- 忘记执行 AI 评分和 AI 代码审查

**正确做法**：
```
完整流程：
1. git fetch
2. 运行分析脚本
3. ⭐ AI 评分（不能遗漏！）
4. ⭐ AI 代码审查（不能遗漏！）
5. 同步数据（一次性同步所有）
6. 验证前端显示
```

**教训**：AI 评分和 AI 代码审查是分析任务的一部分，必须在同步前完成！

---

### 案例 5：用户匹配错误（2026-03-28）

**错误现象**：运营前端组的用户数据丢失（如 houfeng-jk）

**错误原因**：
- 数据库中存在重复用户记录（同一用户名，不同 id）
- 一条有 team_id，一条没有
- 同步时匹配到了错误的那条

**正确做法**：
```javascript
// 只获取 team_id 匹配的用户
const teamUsers = await prisma.user.findMany({
  where: { teamId: TEAM_ID },  // ⚠️ 必须过滤 team_id
  select: { id: true, username: true }
});

const userMap = new Map();
for (const u of teamUsers) {
  userMap.set(u.username, u.id);
}
```

**教训**：用户匹配时必须使用 team_id 过滤，避免匹配到重复的用户记录！

---

### 案例 6：没有过滤非运营前端组用户（2026-03-28）

**错误现象**：同步了不该同步的用户数据（如 liuxin9-jk, gaohui-jwk 等不在运营前端组）

**错误原因**：
- 分析数据包含了所有用户
- 同步时没有过滤 team_id

**正确做法**：
```javascript
// 同步前必须检查用户是否在运营前端组
for (const analysis of analysisData.analyses) {
  const username = analysis.user.username;
  const userId = userMap.get(username);  // userMap 只包含运营前端组用户
  
  // 只保留运营前端组的用户
  if (!userId) {
    console.log('跳过（不在运营前端组）:', username);
    continue;
  }
  
  // ... 写入数据
}
```

**教训**：SKILL.md 明确规定"用户必须在小组管理中预先添加"，同步时必须过滤！

---

### 案例 7：修改前端代码导致历史数据不兼容（2026-03-28）

**错误现象**：修改前端代码后，历史周期数据显示异常

**错误原因**：
- 新数据使用 `file` 字段
- 前端代码改为读取 `file.file || file.path`
- 但这会影响历史数据的显示

**正确做法**：
```
❌ 不要修改前端代码来适配新字段结构
✅ 应该让新数据的字段结构和历史数据保持一致
```

**教训**：修改数据结构时，优先修改数据源，而不是修改前端代码！

---

### 案例 8：数据库表有重复用户记录（2026-03-28）

**错误现象**：同一个用户名在 users 表中有多条记录

**根本原因**：之前的同步脚本可能创建了重复用户

**修复 SQL**：
```sql
-- 删除没有 team_id 的重复用户
DELETE FROM users 
WHERE team_id IS NULL 
AND username IN (SELECT username FROM users WHERE team_id IS NOT NULL);
```

**教训**：定期检查数据质量，清理重复记录！

---

### 案例 9：team_statistics.avg_quality_score 未更新（2026-04-01）

**错误现象**：大盘视图"AI分析平均代码质量"显示为 0

**根本原因分析**：
```
┌─────────────────────────────────────────────────────────────┐
│  数据流向                                                    │
├─────────────────────────────────────────────────────────────┤
│  前端 Dashboard → GET /dashboard/overview                    │
│                    ↓                                         │
│  后端 DashboardService.getOverview()                         │
│                    ↓                                         │
│  查询 team_statistics 表                                     │
│                    ↓                                         │
│  返回 avg_quality_score 字段                                 │
│                                                              │
│  ⚠️ 问题：team_statistics.avg_quality_score 是 null！        │
└─────────────────────────────────────────────────────────────┘
```

**深层原因**：
- 大盘 API 从 `team_statistics` 表读取平均质量分，**不是**从 `code_analyses` 表聚合
- 同步脚本只更新了 `code_analyses.ai_quality_score`
- **没有计算并更新 `team_statistics.avg_quality_score`**

**错误代码示例**：
```javascript
// ❌ 只更新 code_analyses
await prisma.codeAnalysis.update({
  where: { id },
  data: { aiQualityScore: score }
});

// ⚠️ 遗漏：没有更新 team_statistics.avg_quality_score
```

**正确做法**：
```javascript
// ✅ 同步完成后，计算团队平均质量分并更新 team_statistics
const analyses = await prisma.codeAnalysis.findMany({
  where: {
    periodType: 'week',
    periodValue: '20260402',
    user: { teamId: TEAM_ID }
  },
  select: { aiQualityScore: true }
});

const scores = analyses
  .filter(a => a.aiQualityScore !== null)
  .map(a => Number(a.aiQualityScore));

const avgScore = scores.length > 0 
  ? Math.round((scores.reduce((a, b) => a + b, 0) / scores.length) * 100) / 100 
  : null;

await prisma.teamStatistic.updateMany({
  where: {
    teamId: TEAM_ID,
    periodType: 'week',
    periodValue: '20260402'
  },
  data: { avgQualityScore: avgScore }
});
```

**教训**：
1. **前端显示数据来自哪张表？** 必须搞清楚数据流向！
2. **不同表的数据来源不同**：`code_analyses` 是个体数据，`team_statistics` 是聚合数据
3. **同步脚本必须处理所有相关表**，不能只更新一张表

---

### 案例 10：code_issues 关联错误的分析记录（2026-04-01）

**错误现象**：dove_digital 项目的代码审查问题，明明是 `zhangdi-jk` 提交的，却统计到 `lizhuotian-jk` 身上

**根本原因分析**：
```
┌─────────────────────────────────────────────────────────────┐
│  数据结构                                                    │
├─────────────────────────────────────────────────────────────┤
│  code_issues 表                                              │
│  ├── analysis_id → 关联到 code_analyses                      │
│  ├── committer_name → "zhangdi-jk"（实际提交者）             │
│  └─────────────────────────────────────────────────────────┘│
│                                                              │
│  code_analyses 表                                            │
│  ├── user_id → 关联到 users                                  │
│  ├── 项目 + 周期 + 用户                                       │
│  └─────────────────────────────────────────────────────────┘│
│                                                              │
│  ⚠️ 问题：analysis_id 关联到了错误的分析记录！                │
│     - code_issues.committer_name = "zhangdi-jk"              │
│     - code_analyses.user_id = "lizhuotian-jk" (错误!)        │
└─────────────────────────────────────────────────────────────┘
```

**后端统计逻辑**：
```sql
-- 后端按 ca.user_id 分组统计问题
SELECT ca.user_id, COUNT(*) as issue_count
FROM code_issues ci
JOIN code_analyses ca ON ci.analysis_id = ca.id
GROUP BY ca.user_id  -- ⚠️ 按 analysis 关联的用户统计
```

**问题根源**：
- 写入 `code_issues` 时，`analysis_id` 应该关联到 `committer_name` 对应的分析记录
- 但实际关联到了其他人的分析记录

**错误代码示例**：
```javascript
// ❌ 错误：拿到 dove_digital 的某个分析记录（可能是第一个）
const analysis = await prisma.codeAnalysis.findFirst({
  where: { project: { name: 'dove_digital' }, periodValue: '20260402' }
});

// ❌ 然后所有问题都关联到这个分析记录
await prisma.codeIssue.create({
  data: {
    analysis_id: analysis.id,  // ⚠️ 可能是错误的分析记录！
    committer_name: 'zhangdi-jk',
    ...
  }
});
```

**正确做法**：
```javascript
// ✅ 根据 committer_name 找到正确的分析记录
const analysis = await prisma.codeAnalysis.findFirst({
  where: {
    project: { name: 'dove_digital' },
    periodValue: '20260402',
    user: { username: committerName }  // ⚠️ 按提交者查找！
  }
});

if (!analysis) {
  console.log(`⚠️ 未找到 ${committerName} 的分析记录，跳过`);
  continue;
}

// ✅ 关联到正确的分析记录
await prisma.codeIssue.create({
  data: {
    analysis_id: analysis.id,  // ✅ 正确的分析记录
    committer_name: committerName,
    ...
  }
});
```

**教训**：
1. **code_issues.analysis_id 必须匹配 committer_name**
2. **写入问题前必须找到正确的分析记录**：`project + period + user(username=committer_name)`
3. **如果一个项目有多人提交，会有多条分析记录**，必须按提交者匹配

---

## 错误防范清单

每次执行代码质量分析任务前，必须确认：

```
□ 1. 字段结构：检查历史数据的字段名，保持一致
□ 2. 同步顺序：code_analyses → code_issues → code_reviews → team_statistics → project_statistics
□ 3. 用户过滤：只同步 team_id 匹配的用户
□ 4. AI 评分：同步前必须完成
□ 5. AI 代码审查：同步前必须完成
□ 6. ⭐ team_statistics.avg_quality_score：必须计算并更新（从 code_analyses 聚合）
□ 7. ⭐ code_issues.analysis_id：必须匹配 committer_name（按 user.username 查找）
□ 8. 统计表：不要遗漏 team_statistics 和 project_statistics
□ 9. 验证前端：确认大盘、类型分布、问题明细、提交记录都正常显示
□ 10. ⭐ 验证关联关系：code_issues 的 analysis_id 对应的用户名 == committer_name
```

---

## 十七、更新记录

| 日期 | 更新内容 |
|------|---------|
| 2026-03-28 | 新增错误案例库（8个典型案例） |
| 2026-03-28 | 新增错误防范清单 |
| 2026-03-24 | 新增月度分析逻辑（不需要找分支） |
| 2026-03-24 | 新增周维度分支差异正确命令 |
| 2026-03-24 | 新增代码审查功能 |
| 2026-03-24 | 新增审查报告格式模板 |
| 2026-03-24 | 新增结合 code-review 技能的审查方法 |
| 2026-03-24 | 新增 ProjectCodeReview 前端页面 |
| 2026-03-24 | 新增 CodeReviewModule 后端模块 |

---

## 十七、代码审查数据存储

### 数据库表

```sql
-- 代码问题表
CREATE TABLE code_issues (
  id UUID PRIMARY KEY,
  analysis_id TEXT REFERENCES code_analyses(id),
  file_path VARCHAR(500),
  line_start INT,
  line_end INT,
  issue_type VARCHAR(100),
  severity VARCHAR(20),  -- P0/P1/P2
  description TEXT,
  suggestion TEXT,
  code_snippet TEXT,
  code_example TEXT,        -- 修复后的代码示例
  committer_name VARCHAR(100),  -- 提交人
  created_at TIMESTAMP,
  updated_at TIMESTAMP
);

-- 创建索引
CREATE INDEX idx_code_issues_analysis ON code_issues(analysis_id);
CREATE INDEX idx_code_issues_severity ON code_issues(severity);
CREATE INDEX idx_code_issues_type ON code_issues(issue_type);
```

### 后端 API

| 端点 | 方法 | 描述 |
|------|------|------|
| `/api/v1/code-review/:projectId` | GET | 获取项目的代码审查问题 |
| `/api/v1/code-review/:projectId/summary` | GET | 获取审查汇总统计 |
| `/api/v1/projects/:id/report` | GET | 获取项目报告（含贡献者统计） |

### 前端页面

- **路由**: `/projects/:projectId/code-review`
- **组件**: `ProjectCodeReview.tsx`
- **功能**: 
  - 版本信息、整体统计
  - 贡献者统计表格（含问题数、质量评价）
  - 问题明细表格（支持按严重程度/按文件查看）
  - 共性问题汇总
  - 执行优先级表格
  - 总体评价卡片

---

## 十八、代码审查报告页面

### 页面结构

```
┌─────────────────────────────────────────────────────────────┐
│  页面头部                                                    │
│  - 返回按钮、标题、描述、报告生成时间                          │
├─────────────────────────────────────────────────────────────┤
│  统计维度切换                                                │
│  - 周/月切换 + 日期选择器                                     │
├─────────────────────────────────────────────────────────────┤
│  版本信息                                                    │
│  ┌──────────────┬──────────────┬──────────────┐            │
│  │ 当前版本     │ 对比版本     │ 总任务数     │            │
│  └──────────────┴──────────────┴──────────────┘            │
├─────────────────────────────────────────────────────────────┤
│  整体统计                                                    │
│  ┌────────┬────────┬────────┬────────┬────────┐            │
│  │提交次数│新增行数│删除行数│净增长  │贡献者  │            │
│  └────────┴────────┴────────┴────────┴────────┘            │
├─────────────────────────────────────────────────────────────┤
│  贡献者统计                                                  │
│  ┌────────┬────────┬────────┬────────┬────────┬────────┐  │
│  │提交人  │提交次数│提交占比│新增行数│删除行数│净增行数│  │
│  ├────────┼────────┼────────┼────────┼────────┼────────┤  │
│  │必须修改│建议修改│问题总数│问题占比│质量评价│        │  │
│  └────────┴────────┴────────┴────────┴────────┴────────┘  │
├─────────────────────────────────────────────────────────────┤
│  问题明细                                                    │
│  - Tab切换：全部/P0/P1/P2                                    │
│  - 或按文件分组查看                                          │
│  - 表格列：提交人、文件、问题类型、严重程度、描述、建议、操作  │
├─────────────────────────────────────────────────────────────┤
│  共性问题汇总                                                │
│  - 问题类型、出现次数、涉及文件                              │
├─────────────────────────────────────────────────────────────┤
│  执行优先级                                                  │
│  - P0/P1/P2 三行，背景色区分                                 │
│  - 优先级、说明、数量、示例问题                              │
├─────────────────────────────────────────────────────────────┤
│  总体评价                                                    │
│  - 综合评分（大号数字）                                      │
│  - 优点列表                                                  │
│  - 改进建议列表                                              │
└─────────────────────────────────────────────────────────────┘
```

### 贡献者统计字段

| 字段 | 说明 | 计算方式 |
|------|------|---------|
| 提交人 | 用户名 | users.username |
| 提交次数 | 该周期提交数 | commit_count |
| 提交占比 | 占总提交百分比 | commit_count / total_commits * 100% |
| 新增行数 | 新增代码行 | insertions |
| 删除行数 | 删除代码行 | deletions |
| 净增行数 | 新增-删除 | insertions - deletions |
| 必须修改数 | P0+P1 问题数 | COUNT(severity IN ('P0','P1')) |
| 建议修改数 | P2 问题数 | COUNT(severity = 'P2') |
| 问题总数 | 该用户问题数 | COUNT(*) FROM code_issues |
| 问题占比 | 占总问题百分比 | issue_count / total_issues * 100% |
| 质量评价 | 文字评价 | 根据问题数判定 |

### 质量评价规则

```javascript
function getQualityRating(issueStats) {
  const { mustFixCount, totalIssues } = issueStats;
  
  if (totalIssues === 0) return '优';
  if (mustFixCount >= 3 || totalIssues >= 5) return '需重点关注';
  if (mustFixCount >= 1 || totalIssues >= 3) return '待改进';
  return '良好';
}
```

### 后端查询示例

```sql
-- 获取贡献者统计
SELECT 
  u.username,
  ca.commit_count,
  ROUND(ca.commit_count * 100.0 / total.commit_count, 1) as commit_ratio,
  ca.insertions,
  ca.deletions,
  ca.insertions - ca.deletions as net_lines,
  COALESCE(p0_p1.count, 0) as must_fix_count,
  COALESCE(p2.count, 0) as suggest_count,
  COALESCE(total_issues.count, 0) as issue_count
FROM code_analyses ca
JOIN users u ON ca.user_id = u.id
-- 子查询统计各严重程度问题数
LEFT JOIN (...) p0_p1 ON ...
LEFT JOIN (...) p2 ON ...
LEFT JOIN (...) total_issues ON ...
WHERE ca.project_id = ? AND ca.period_type = ? AND ca.period_value = ?
ORDER BY ca.commit_count DESC;
```

---

## 十九、前端实现要点

### 文件结构

```
code-quality-frontend/
├── src/pages/ProjectCodeReview/
│   ├── ProjectCodeReview.tsx    # 主组件
│   └── ProjectCodeReview.css    # 样式
```

### 关键组件代码

```tsx
// 贡献者表格列定义
const memberColumns = [
  { title: '提交人', dataIndex: 'username', width: 130 },
  { title: '提交次数', dataIndex: 'commitCount', width: 90 },
  { title: '提交占比', dataIndex: 'commitRatio', width: 90 },
  { title: '新增行数', dataIndex: 'insertions', width: 100, render: v => <span style={{ color: '#52c41a' }}>+{v}</span> },
  { title: '删除行数', dataIndex: 'deletions', width: 100, render: v => <span style={{ color: '#f5222d' }}>-{v}</span> },
  { title: '净增行数', dataIndex: 'netLines', width: 100 },
  { title: '必须修改', dataIndex: 'mustFixCount', width: 90, render: v => v > 0 ? <Tag color="#ff4d4f">{v}</Tag> : <Tag>0</Tag> },
  { title: '建议修改', dataIndex: 'suggestCount', width: 90, render: v => v > 0 ? <Tag color="#52c41a">{v}</Tag> : <Tag>0</Tag> },
  { title: '问题总数', dataIndex: 'issueCount', width: 90 },
  { title: '问题占比', dataIndex: 'issueRatio', width: 90 },
  { title: '质量评价', dataIndex: 'qualityRating', width: 110, fixed: 'right',
    render: v => <Tag color={colorMap[v]}>{v}</Tag> },
];

// 问题明细表格列定义
const issueColumns = [
  { title: '提交人', dataIndex: 'committer_name', width: 130 },
  { title: '文件', dataIndex: 'file_path', width: 180, ellipsis: true },
  { title: '问题类型', dataIndex: 'issue_type', width: 130 },
  { title: '严重程度', dataIndex: 'severity', width: 90 },
  { title: '问题描述', dataIndex: 'description', width: 280, ellipsis: true },
  { title: '修改建议', dataIndex: 'suggestion', width: 350, ellipsis: true },
  { title: '操作', key: 'action', width: 70, fixed: 'right' },
];
```

### API 请求格式

```typescript
// 获取代码审查问题
const res = await request.get(`/code-review/${projectId}`, {
  periodType, periodValue
});

// 获取项目报告（含贡献者统计）
const res = await request.get(`/projects/${projectId}/report`, {
  periodType, periodValue
});
```

---

## 二十、常见问题处理

### 问题：提交人字段为空

**原因**：code_issues 表的 committer_name 字段未填充。

**解决**：从 code_analyses 关联 users 表更新：

```sql
UPDATE code_issues ci
SET committer_name = u.username
FROM code_analyses ca
JOIN users u ON ca.user_id = u.id
WHERE ci.analysis_id = ca.id
AND ci.committer_name IS NULL;
```

### 问题：统计维度切换不生效

**原因**：前端状态管理问题，URL 参数未同步。

**解决**：使用本地状态 + URL 同步：

```tsx
const [periodType, setPeriodType] = useState(initialPeriodType);

const handlePeriodTypeChange = (newType) => {
  setPeriodType(newType);
  // 更新 URL 参数
  const params = new URLSearchParams(searchParams);
  params.set('periodType', newType);
  navigate(`${pathname}?${params}`, { replace: true });
};
```

### 问题：API 返回 404

**原因**：后端接口不支持项目名称查询，只支持 UUID。

**解决**：在后端 service 添加名称解析：

```typescript
async resolveProjectId(idOrName: string) {
  const uuidRegex = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
  if (uuidRegex.test(idOrName)) return idOrName;
  
  const project = await this.prisma.project.findFirst({
    where: { name: idOrName }
  });
  return project?.id || null;
}
```

---

## 二十一、相关文件路径

| 文件 | 路径 |
|------|------|
| 分析脚本 | `/Users/zhangdi/work/codeCap/代码质量分析系统/scripts/analyze-code-v2.js` |
| 同步脚本 | `/Users/zhangdi/work/codeCap/代码质量分析系统/scripts/sync-to-db.js` |
| 分析输出 | `/Users/zhangdi/work/codeCap/代码质量分析系统/analysis-output/analysis-YYYYMMDD.json` |
| 后端服务 | `/Users/zhangdi/work/codeCap/代码质量分析系统/code-quality-backend/` |
| 前端服务 | `/Users/zhangdi/work/codeCap/代码质量分析系统/code-quality-frontend/` |
| CodeReview 模块 | `code-quality-backend/src/modules/code-review/` |
| ProjectCodeReview 页面 | `code-quality-frontend/src/pages/ProjectCodeReview/` |

---

## 二十二、项目 ID 格式约定

### 问题背景

早期同步脚本手动指定项目 ID（如 `project-lego-nuxt`），后来改为自动生成 UUID，导致数据库中有两种格式。

### 正确格式

**所有项目 ID 必须使用 UUID 格式！**

```
✅ 正确: 550e8400-e29b-41d4-a716-446655440000
❌ 错误: project-lego-nuxt
```

### 后端 resolveProjectId 方法

后端服务需要支持三种查询格式：

```typescript
async resolveProjectId(idOrName: string) {
  // 1. UUID 格式 - 直接返回
  const uuidRegex = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
  if (uuidRegex.test(idOrName)) return idOrName;
  
  // 2. 项目 ID（非 UUID 格式）- 查找旧数据
  const projectById = await this.prisma.project.findFirst({
    where: { id: idOrName }
  });
  if (projectById) return projectById.id;
  
  // 3. 项目名称 - 按名称查找
  const projectByName = await this.prisma.project.findFirst({
    where: { name: idOrName }
  });
  return projectByName?.id || null;
}
```

### 同步脚本 ID 生成

同步脚本应该按项目名查找，不存在时创建新项目（自动生成 UUID）：

```javascript
async function getOrCreateProject(projectName, prisma) {
  let project = await prisma.project.findFirst({
    where: { name: projectName }
  });
  
  if (!project) {
    project = await prisma.project.create({
      data: { name: projectName }
      // id 自动生成 UUID
    });
  }
  
  return project.id;
}
```

---

## 二十三、废弃文件归档

### 已归档文件（`.archive/` 目录）

以下文件已废弃，移动到 `.archive/` 目录：

| 文件 | 原因 |
|------|------|
| `analyze-code.js` | 旧版分析脚本，v2 已支持周/月 |
| `analyze-month.js` | 月度专用，v2 已支持 |
| `sync-ai-scores-*.js` | 旧的 AI 评分同步，已删除外部 API 调用 |
| `sync-month-to-db.js` | 旧版月度同步 |
| `sync-to-db.js`、`sync-to-db-v2.js` | 旧版同步 |
| `sync-week-to-db.js` | 旧版周同步 |
| `sync-week-20260326.js` | 特定周期的临时脚本 |

### 当前主力脚本

| 脚本 | 用途 |
|------|------|
| `analyze-code-v2.js` | 分析代码变更（周/月） |
| `sync-to-db.js` | 同步分析数据到数据库 |
| `code-review.js` | 代码审查问题分析 |
| `notify-teams.js` | 360Teams 消息通知 |
| `weekly-analysis.sh` | 每周自动分析脚本 |

---

## 二十四、更新记录

| 日期 | 更新内容 |
|------|---------|
| 2026-03-25 | 新增项目 ID 格式约定（UUID 格式） |
| 2026-03-25 | 新增 resolveProjectId 方法支持三种格式 |
| 2026-03-25 | 新增废弃文件归档说明 |
| 2026-03-24 | 新增月度分析逻辑（不需要找分支） |
| 2026-03-24 | 新增周维度分支差异正确命令 |
| 2026-03-24 | 新增代码审查功能 |
| 2026-03-24 | 新增审查报告格式模板 |
| 2026-03-24 | 新增结合 code-review 技能的审查方法 |
| 2026-03-24 | 新增 ProjectCodeReview 前端页面 |
| 2026-03-24 | 新增 CodeReviewModule 后端模块 |
| 2026-03-24 | 新增贡献者统计表格（11 个字段） |
| 2026-03-24 | 新增问题明细表格优化 |
| 2026-03-24 | 新增总体评价卡片 |
| 2026-03-24 | 新增前端实现要点文档 |
| 2026-03-24 | 新增常见问题处理方案 |