# Example: Team Weekly Report

## Scenario

Every Friday afternoon, the Platform Engineering team sends a weekly summary to the company-wide 飞书 group. The repo has 30-50 commits per week with mixed commit quality — some follow Conventional Commits, many don't. The audience is non-technical stakeholders (PMs, Design, Leadership).

## Input

```bash
cd ~/projects/platform
python3 ~/.openclaw/skills/changelog-weaver/scripts/weaver.py collect \
  --since "2026-06-08" \
  --until "2026-06-15" \
  -o weekly-2026-06-15.json
```

**Output:** `[SUMMARY] 38 commits, 6 contributors, 0 breaking changes`

## AI Processing

> **Prompt:** "Load `weekly-2026-06-15.json`. 38 commits in a week is too many for a team announcement. Do the following:
>
> 1. Reclassify any `other` commits by analyzing their descriptions
> 2. Merge related commits (same feature/fix across multiple commits)
> 3. Rewrite all descriptions in concise Chinese, focusing on business impact
> 4. Sort by importance — features first, then critical fixes, then infrastructure
> 5. Limit to top 12 entries
> 6. Generate plain text for 飞书 platform
>
> The audience is non-technical — avoid jargon like 'refactor', 'optimize query planner', 'migrate to...'. Instead say 'improved performance', 'made faster', 'simplified'."

## Step-by-Step

### 1. AI reclassifies `other` commits

The AI scans 14 `other` commits and reclassifies:
- `"update login flow"` → `feat` (new feature flag added)
- `"fix the thing"` → `fix` (resolved caching issue)
- `"cleanup"` → `chore` (removed dead code)
- 11 commits merged or deferred as too minor

### 2. AI merges related commits

Three commits about "export performance" are merged into one:
- `perf: optimize export query` + `perf: cache export results` + `fix: export timeout`
- → "优化数据导出性能，支持 50 万行导出无超时"

### 3. AI rewrites in Chinese, business-focused

Technical → Business:
- `refactor(auth): extract token refresh logic` → "优化登录态刷新机制，减少用户掉线"
- `ci: migrate to GitHub Actions v4` → "CI 构建速度提升 50%"
- `fix: null pointer in billing calc` → "修复极端情况下账单计算错误（影响 <0.1% 用户）"

## Final Output

```bash
python3 scripts/weaver.py generate \
  -i weekly-2026-06-15.json \
  -f plain \
  -p feishu \
  -o feishu-weekly-2026-06-15.txt
```

**feishu-weekly-2026-06-15.txt:**
```
📦 平台周报 (2026-06-08 ~ 2026-06-15)

【新功能】
  • 用户画像页新增「活跃度趋势」图表，可按周/月/季度切换时间粒度
  • 数据导出支持自定义字段选择，导出体积减少约 60%
  • Dashboard 新增「最近访问」快捷入口，减少 3 步操作

【重要修复】
  • 修复 Safari 浏览器下 Dashboard 加载白屏问题（已影响约 5% 用户）
  • 修复大文件上传偶发超时，现支持 500MB 以下文件稳定上传
  • 修复深夜时段（02:00-04:00）定时任务偶发漏执行

【体验优化】
  • 优化登录态刷新机制，减少切换页面时的加载闪烁
  • 搜索响应速度提升 40%，支持模糊匹配和拼音搜索
  • 移动端页面适配优化，表单和表格在小屏上不再错位

【基础设施】
  • CI 构建时间从 12 分钟优化至 6 分钟，PR 等待时间减半
  • 升级 Redis 集群至 7.2，内存使用降低约 30%，节省成本

👥 本周贡献者: 张三, 李四, 王五, 赵六, 孙七, 周八

📋 详细变更见 internal 频道或 GitLab Changelog
```

## Key Takeaways

1. **Non-technical audience**: AI rewrites tech jargon into plain language
2. **Chinese localization**: The same JSON generates both English (CHANGELOG.md) and Chinese (飞书) output
3. **Prioritization**: AI sorts by importance (features → critical fixes → nice-to-haves → infra)
4. **Merging**: 38 commits collapsed to 12 meaningful entries
5. **Context**: Business impact noted (affected user %, time saved, cost savings)
