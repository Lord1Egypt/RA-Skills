---
name: ai-pr-doctor
description: AI PR 医生 - 自动诊断 GitHub PR 问题、修复 Bug、生成修复报告的端到端工作流。触发词：PR 诊疗、代码审查、修复 PR、PR 医生、自动合并。
category: AI
triggers: PR 诊疗, 代码审查, 修复 PR, PR 医生, 自动合并
---

# AI PR 医生 (ai-pr-doctor)

> GitHub PR → AI 代码审查 → 自动修复 → 合并 → 修复报告 → 飞书通知

## 🎯 解决痛点

- ❌ 团队 PR 堆积，没人及时 review
- ❌ 代码审查耗时，漏掉潜在 bug
- ❌ 简单修复（格式、测试）手动操作太繁琐
- ❌ 合并后没有记录，不知道修了什么

## 💡 解决方案

```
GitHub PR 链接/编号
        ↓
┌──────────────────┐
│  github          │ → gh pr view 获取 PR 信息 + 代码diff
└────────┬─────────┘
         ↓
┌──────────────────┐
│ code-review-skill│ → 5维度 AI 并行审查：CLAUDE.md合规、Bug审计、
└────────┬─────────┘     Git历史分析、过往PR评论、代码注释合规
         ↓
┌──────────────────┐
│ auto-pr-merger  │ → 尝试自动修复 + 重跑测试 + 自动合并
└────────┬─────────┘
         ↓
┌──────────────────┐
│  feishu_doc     │ → 生成修复报告并发布至飞书文档
└──────────────────┘
```

## 📦 包含 Skills

| Skill | 作用 | 调用顺序 |
|-------|------|---------|
| github | 获取 PR 信息、代码diff、合并操作 | 1 |
| code-review-skill | 5维度 AI 并行代码审查 | 2 |
| auto-pr-merger | 自动修复 + 测试 + 合并 | 3 |
| feishu_doc | 生成诊疗报告并发布飞书 | 4 |

## 🔧 前置要求

1. **gh CLI** 已安装并认证 (`gh auth status`)
2. **GitHub 仓库** 可写（用于 auto-pr-merger push 修复）
3. **飞书机器人** 已配置 feishu_doc 权限

## 📝 使用方法

### 触发命令

```
/ai-pr-doctor <PR_URL或编号>
诊断这个 PR
代码审查这个 PR
帮我看看这个 PR
```

### 完整命令

```bash
# 方式 1：通过 OpenClaw
openclaw run ai-pr-doctor --pr https://github.com/owner/repo/pull/123

# 方式 2：通过 cron 定时检查未合并的 PR
openclaw cron add \
  --name "PR 待审查提醒" \
  --schedule "0 10 * * 1-5" \
  --skill ai-pr-doctor \
  --params '{"mode":"check-pending","repo":"owner/repo"}'
```

## 🔄 工作流详情

### Step 1: 获取 PR 信息

```yaml
步骤: 1
技能: github
输入:
  action: pr view
  repo: ${repo_from_input}
  pr_number: ${pr_number}
  output: json
输出:
  pr_title: ${title}
  pr_body: ${body}
  pr_state: ${state}
  changed_files: ${files}
  diff_url: ${diff_url}
  author: ${user.login}
```

### Step 2: AI 代码审查

```yaml
步骤: 2
技能: code-review-skill
输入:
  pr_url: ${pr_url}
  review_dimensions:
    - CLAUDE.md 合规性审查
    - 浅层 Bug 扫描
    - Git 历史上下文分析
    - 过往 PR 评论对照
    - 代码注释合规检查
  output_format: structured_json
输出:
  issues: ${issue_list}
  severity_scores: ${scores}
  review_summary: ${summary}
```

### Step 3: 自动修复与合并

```yaml
步骤: 3
技能: auto-pr-merger
输入:
  pr: ${pr_url}
  test: "npm test"  # 可自定义测试命令
  retries: 2
  auto_merge_if_passed: true
输出:
  fixed_files: ${files_modified}
  test_results: ${test_output}
  merge_result: ${merge_state}
```

### Step 4: 生成修复报告

```yaml
步骤: 4
技能: feishu_doc
输入:
  action: create
  title: "🔬 PR 诊疗报告 #${pr_number} | ${pr_title}"
  content: ${report_markdown}
输出:
  doc_url: ${docUrl}
  doc_id: ${docId}
```

## 📊 输出示例：PR 诊疗报告

```markdown
# 🔬 PR 诊疗报告 #123 | feat: 新增用户认证功能

**仓库**: owner/repo | **PR 链接**: https://github.com/owner/repo/pull/123
**作者**: @zhangsan | **审查时间**: 2026-04-25

---

## 📋 PR 概览

| 字段 | 值 |
|------|-----|
| 状态 | ✅ 已合并 |
| 文件变更 | +127 / -43 |
| 审查轮次 | 1 |
| 自动修复 | 2 处 |

---

## 🩺 AI 审查结果

### 🔴 严重问题 (2)

| # | 文件 | 行号 | 问题描述 |
|---|------|------|---------|
| 1 | src/auth/login.ts | L45 | SQL 注入风险：未使用参数化查询 |
| 2 | src/middleware/logger.ts | L12 | 敏感信息日志外泄 |

### 🟡 中等问题 (3)

| # | 文件 | 问题描述 |
|---|------|---------|
| 1 | src/auth/token.ts | Token 过期时间过长（30天，建议7天）|
| 2 | tests/login.test.ts | 测试覆盖率仅 45%，建议提升至 80% |

### 🟢 低优先级 (1)

| # | 问题 |
|---|------|
| 1 | 缺少 JSDoc 注释 |

---

## 🔧 自动修复记录

| 文件 | 修复内容 | 状态 |
|------|---------|------|
| src/utils/format.ts | Prettier 格式化 | ✅ |
| tests/login.test.ts | Jest 配置修复 | ✅ |
| src/auth/token.ts | Token 过期时间调整 | ⏭️ 跳过（需人工确认）|

---

## ✅ 合并结果

- **自动合并**: 成功
- **CI 状态**: 通过 🟢
- **审查通过**: 2/2 检查项
- **合并时间**: 2026-04-25 20:15 UTC

---

*由 AI PR Doctor 自动生成*
```

## ⚙️ 自定义配置

### 修改测试命令

编辑 `workflow.json` 中的 auto-pr-merger 配置：

```json
{
  "steps": [
    {
      "id": "step3_merge",
      "skill": "auto-pr-merger",
      "input": {
        "test": "pytest tests/ -v",
        "retries": 3
      }
    }
  ]
}
```

### 修改审查维度

```json
{
  "code_review": {
    "dimensions": [
      "security",
      "performance",
      "maintainability",
      "test_coverage"
    ],
    "severity_threshold": 50
  }
}
```

## ⚠️ 注意事项

1. **权限要求**: auto-pr-merger 需要对仓库有写权限才能 push 修复
2. **测试命令**: 请根据实际项目修改测试命令，默认 `npm test`
3. **安全审查**: 涉及安全的 PR 建议人工二次确认
4. **CI 依赖**: 依赖 GitHub Actions 状态，建议开启 required checks

## 📞 故障排除

| 问题 | 原因 | 解决方案 |
|------|------|---------|
| gh auth 失败 | 未登录 | 运行 `gh auth login` |
| 自动修复失败 | 代码冲突 | 手动解决冲突后重试 |
| PR 已被合并 | 无需处理 | 跳过此 PR |
| CI 未通过 | 测试失败 | 查看详细日志，手动修复 |