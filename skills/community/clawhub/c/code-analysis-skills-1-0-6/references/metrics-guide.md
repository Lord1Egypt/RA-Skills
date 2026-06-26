# 指标含义与健康值参考

本文档说明代码分析技能产出的各项指标的含义、计算方式和建议的健康值范围。

## 📝 提交习惯指标

| 指标 | 含义 | 计算方式 | 健康值范围 |
|------|------|---------|-----------| 
| Total Commits | 总提交次数 | 统计所有非过滤提交 | — |
| Merge Ratio | 合并提交占比 | merge_commits / total_commits | < 30% |
| Avg Commits/Active Day | 每个活跃日的平均提交数 | total_commits / unique_active_days | 2-8 |
| Avg Message Length | 平均提交消息长度(字符) | sum(msg_len) / count | 30-100 |
| Avg Lines Added | 平均每次提交新增行数 | sum(added) / count | 10-200 |
| Avg Lines Deleted | 平均每次提交删除行数 | sum(deleted) / count | 5-100 |
| Avg Files Changed | 平均每次提交修改文件数 | sum(files) / count | 1-10 |

## ⏰ 工作习惯指标

| 指标 | 含义 | 计算方式 | 关注阈值 |
|------|------|---------|---------| 
| Peak Hour | 提交最多的小时 | mode(commit_hours) | — |
| Weekend Ratio | 周末提交占比 | weekend_commits / total | > 20% 需关注 |
| Late Night Ratio | 深夜(22:00-05:00)提交占比 | late_night_commits / total | > 15% 需关注 |
| Longest Streak | 最长连续编码天数 | 连续日期计数 | — |
| Avg Gap Between Commits | 两次提交的平均间隔(小时) | avg(time_gaps) | — |

### 时段定义

| 时段 | 时间范围 |
|------|---------|
| Early Morning | 05:00 - 08:59 |
| Morning | 09:00 - 11:59 |
| Afternoon | 12:00 - 17:59 |
| Evening | 18:00 - 21:59 |
| Late Night | 22:00 - 04:59 |

## 🚀 研发效率指标

| 指标 | 含义 | 计算方式 | 健康值范围 |
|------|------|---------|-----------| 
| Churn Rate | 代码流失率（写了又删的比例） | total_deleted / total_added | < 50% |
| Rework Ratio | 返工率（7天内重复修改同一文件） | rework_mods / total_mods | < 30% |
| Lines per Commit | 每次提交的总变更行数 | (added + deleted) / commits | 20-300 |
| Ownership Ratio | 文件所有权比例（贡献 >50% 的文件） | owned_files / unique_files | — |
| Bus Factor | 仓库平均总线因子（每个文件的独立贡献者数） | avg(unique_authors_per_file) | > 2 为佳 |

### 指标解读

- **Churn Rate 高**: 可能表示需求变更频繁、技术方案不稳定或探索性编码
- **Rework Ratio 高**: 可能表示代码质量问题、需求不明确或 review 反馈多
- **Bus Factor 低**: 知识集中在少数人手中，团队有风险

## 🎨 代码风格指标

| 指标 | 含义 | 计算方式 | 建议 |
|------|------|---------|------| 
| Conventional Commit Ratio | 遵循 Conventional Commits 规范的比例 | conventional_count / total | > 80% 为佳 |
| Issue Reference Ratio | 提交消息中引用 Issue/Ticket 的比例 | issue_ref_count / total | > 50% 为佳 |
| Language Distribution | 修改的文件语言分布 | 按文件扩展名统计 | — |
| File Category Distribution | 修改的文件类别分布 | source/test/config/docs 等 | — |

### Conventional Commits 格式

```
<type>(<scope>): <description>
```

支持的 type: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`

## 🔍 代码质量指标

| 指标 | 含义 | 计算方式 | 关注阈值 |
|------|------|---------|---------| 
| Bug Fix Ratio | Bug 修复提交占比 | bugfix_commits / total | > 40% 需关注 |
| Revert Ratio | 回滚提交占比 | revert_commits / total | > 5% 需关注 |
| Large Commit Ratio | 大提交(>500行变更)占比 | large_commits / total | > 20% 需关注 |
| Test Modification Ratio | 测试文件修改占文件修改总数的比例 | test_mods / total_mods | > 20% 为佳 |
| Doc Modification Ratio | 文档文件修改占比 | doc_mods / total_mods | — |
| Avg Python Complexity | Python 代码平均圈复杂度 | radon cc_visit 结果平均 | < 10 为佳 |

### 圈复杂度参考

| 复杂度 | 等级 | 说明 |
|--------|------|------|
| 1-5 | A | 低风险，容易维护 |
| 6-10 | B | 中等，仍可接受 |
| 11-20 | C | 高风险，建议重构 |
| 21-50 | D | 非常高，应当拆分 |
| 50+ | F | 不可维护 |

## 🐟 摸鱼指数 (Slacking Index)

摸鱼指数是一个综合评分 (0-100)，通过分析多个行为信号来评估开发者的投入程度。

### 信号说明

| 信号 | 含义 | 计算方式 | 最大贡献分 |
|------|------|---------|-----------|
| Sparsity (稀疏度) | 活跃天数占总时间跨度的比例 | 1 - (unique_days / span_days) | 25 |
| Trivial Commits (琐碎提交) | 变更 ≤5 行的提交占比 | trivial_count / total | 20 |
| Disappearance (消失) | 超过72小时无提交的间隔占比 | large_gap_count / total_gaps | 20 |
| Low Output (低产出) | 每活跃日的变更行数 | total_lines / unique_days | 15 |
| Non-code (非代码) | 仅修改配置/文档的提交占比 | non_code_commits / total | 10 |
| Procrastination (拖延) | 周五提交多、周一提交少的模式 | friday_ratio - monday_ratio | 10 |
| Copy-paste (复制粘贴) | 新增/删除行比率过高 | added / deleted > 10 | 5 |

### 摸鱼等级

| 等级 | 分数范围 | Emoji | 含义 |
|------|----------|-------|------|
| Workaholic (工作狂) | 0-20 | 🔥 | 高度投入，持续贡献 |
| Normal (正常) | 21-40 | ✅ | 健康的工作模式 |
| Suspicious (有嫌疑) | 41-60 | 😏 | 检测到部分摸鱼信号 |
| Slacker (摸鱼达人) | 61-80 | 🐟 | 显著的低参与指标 |
| Professional Slacker (摸鱼大师) | 81-100 | 🏆 | 职业摸鱼选手 |

### 注意

- 摸鱼指数仅基于 Git 提交行为，不能反映代码审查、会议、设计等非编码贡献
- 某些角色（如架构师、技术经理）天然提交较少，需结合角色理解
- 该指标带有一定的幽默性质，但底层数据是严肃的

## 🏆 开发者评估体系

### 综合评分 (0-100)

综合评分由六大维度加权计算得出：

| 维度 | 权重 | 评估内容 |
|------|------|----------|
| Commit Discipline (提交纪律) | 15% | 提交频率、消息质量、规范遵循率 |
| Work Consistency (工作一致性) | 15% | 作息规律度、连续编码天数、周末/深夜占比 |
| Efficiency (效率) | 20% | 代码流失率、返工率、每次提交的变更量 |
| Code Quality (代码质量) | 25% | Bug修复率、回滚率、大提交率、测试覆盖、复杂度 |
| Code Style (代码风格) | 10% | Conventional Commits 遵循率、Issue引用率 |
| Engagement (参与度) | 15% | 摸鱼指数的反向 (100 - slacking_index) |

### 等级对照表

| Grade | 分数 | 含义 |
|-------|------|------|
| S | 90-100 | 顶级贡献者 |
| A | 80-89 | 优秀开发者 |
| B | 70-79 | 扎实贡献者 |
| C | 60-69 | 合格水平 |
| D | 50-59 | 勉强及格 |
| E | 35-49 | 低于预期 |
| F | 0-34 | 需要严肃对待 |

### 评估输出

每位开发者的评估包含：

1. **综合评分**: 0-100 的数值 + S/A/B/C/D/E/F 等级
2. **六维度分数**: 每个维度 0-100 分，带可视化条形图
3. **优点列表**: 每条基于具体数据，如 "Low code churn (12%) — writes stable code"
4. **缺点列表**: 直白指出问题，如 "Bug fix ratio at 45% — nearly half your commits are fixing bugs"
5. **建议列表**: 可立即执行的改进措施
6. **一句话定论**: 如 "⭐ Top-tier contributor. Reliable, disciplined, and productive."
