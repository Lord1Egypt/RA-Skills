# 学术论文写作工作流 - 快速入门

## 🚀 5 分钟开始

### 前置条件

确保已安装以下官方技能：
- ✅ academic-deep-research
- ✅ academic-writer
- ✅ academic-citation
- ✅ academic-integrity-checker

确保已安装以下自研技能（本技能包）：
- ✅ academic-paper-workflow（本技能）
- ✅ academic-review-revisor（同行评审）
- ✅ final-integrity-check（终稿验证）
- ✅ journal-format-output（期刊格式）

### 方式 1：一键启动（推荐新手）

```bash
python skills/academic-paper-workflow/scripts/run_full_workflow.py "你的研究主题" --journal "目标期刊" --depth exhaustive
```

**示例：**
```bash
python skills/academic-paper-workflow/scripts/run_full_workflow.py "无人机智能目标识别技术" --journal "IEEE Transactions" --depth exhaustive
```

脚本会引导你逐步完成 7 个阶段，每阶段自动保存检查点。

### 方式 2：分阶段执行（推荐有经验）

```bash
# 阶段 1: 深度研究
/academic-deep-research 无人机智能目标识别技术研究综述

# 阶段 2: 学术写作
/academic-writer 基于以上研究报告撰写 SCI 论文

# 阶段 3: 引用格式化
/academic-citation 将参考文献转换为 APA 7th 格式

# 阶段 4: 初稿诚信检查
/academic-integrity-checker [论文初稿]

# 阶段 5: 多轮评审
/review-revisor [论文稿]

# 阶段 6: 终稿验证
/final-integrity-check [最终稿]

# 阶段 7: 期刊格式输出
/journal-format-output [最终稿] --journal "IEEE Transactions"
```

---

## 📊 预期产出

| 阶段 | 产出文件 | 说明 |
|------|---------|------|
| 1 | research_report.md | 25000 字深度研究报告 |
| 1 | literature_search_results.json | 180+ 篇文献搜索结果 |
| 2 | paper_draft.md | 15000 字论文初稿 |
| 2 | references_raw.txt | 原始参考文献列表 |
| 3 | references_formatted.txt | 格式化参考文献（APA 7th） |
| 3 | citation_validation_report.json | 格式验证报告 |
| 4 | integrity_check_report_stage4.json | 初稿诚信检查报告 |
| 4 | paper_draft_revised.md | 修复后初稿 |
| 5 | review_reports_round{1,2,3}.json | 3 轮评审报告 |
| 5 | paper_final.md | 最终稿（0 评审意见） |
| 6 | final_integrity_check_report.json | 终稿验证报告 |
| 7 | submission_main.docx | 主文档（期刊格式） |
| 7 | submission_cover_letter.docx | 封面信 |
| 7 | submission_checklist.pdf | 投稿检查清单 |

---

## ⏱ 时间规划

| 阶段 | 预计耗时 | 可并行 |
|------|---------|-------|
| 阶段 1: Research | 2-4 小时 | ❌ |
| 阶段 2: Write | 30-60 分钟 | ❌ |
| 阶段 3: Citation | 10-20 分钟 | ✅ |
| 阶段 4: Integrity Check | 30-60 分钟 | ✅ |
| 阶段 5: Review/Revise | 2-4 小时 | ❌ |
| 阶段 6: Final Check | 20-30 分钟 | ✅ |
| 阶段 7: Format Output | 10-20 分钟 | ✅ |

**总计：** 6-12 小时（可分多天完成）

---

## ✅ 质量检查

完成所有阶段后，运行验证脚本：

```bash
python skills/academic-paper-workflow/scripts/workflow_validator.py ./workflow_output
```

验证通过标准：
- ✅ 所有阶段文件存在
- ✅ 研究报告 ≥25000 字
- ✅ 文献数量 ≥180 篇
- ✅ 论文初稿 ≥15000 字
- ✅ 论文结构完整
- ✅ 引用格式无错误
- ✅ 诚信检查无错误
- ✅ 3 轮评审意见 = 0
- ✅ 终稿验证通过

---

## ⚠️ 常见陷阱

| 陷阱 | 症状 | 解决方案 |
|------|------|---------|
| 跳过诚信检查 | 投稿后被拒 | 必须执行 2 轮检查 |
| 跳过同行评审 | 论文质量不稳定 | 必须执行 3 轮评审 |
| 手动调格式 | 耗时且易错 | 使用 journal-format-output |
| 研究深度不足 | 论文缺乏深度 | 选择 exhaustive 模式 |
| 跳过研究计划审批 | 研究方向偏离 | 必须人工审批研究计划 |

---

## 📚 详细文档

- **完整工作流说明：** 见 `SKILL.md`
- **阶段详细说明：** 见 `references/workflow-stages.md`
- **技能协调指南：** 见 `references/skill-orchestration.md`
- **诚信检查规则：** 见 `references/integrity-check-rules.md`

---

## 🎓 使用案例

### 案例：SCI 综述论文（用户实测）

- **主题：** 无人机智能目标识别技术
- **时间：** 29 天（2/1-3/1）
- **文献：** 182 篇检索 → 96 篇引用
- **检查：** 2 轮诚信检查
- **评审：** 3 轮（18 条→4 条→0 条）
- **格式：** 0 次手动调整
- **状态：** ✅ 已投稿，审稿中

---

## 💡 最佳实践

1. **不要跳过任何阶段**：每个阶段都有独特价值
2. **诚信检查必须 2 轮**：初稿 + 终稿，缺一不可
3. **同行评审至少 3 轮**：直到 0 评审意见
4. **研究计划必须审批**：这是研究方向正确性的保证
5. **最终投稿必须人工确认**：对外发布零容忍错误
6. **保存所有中间结果**：便于追溯和修改
7. **使用版本控制**：推荐 Git 管理论文版本

---

## 🔧 故障排除

### 问题 1：技能未找到

**症状：** 执行命令提示技能不存在

**解决：**
```bash
# 检查技能是否已安装
ls skills/ | grep academic

# 如未安装，从 ClawHub 安装
clawhub install academic-deep-research
clawhub install academic-writer
# ...
```

### 问题 2：输出目录权限错误

**症状：** 无法保存检查点文件

**解决：**
```bash
# 检查目录权限
ls -la ./workflow_output

# 如无写权限，修改权限或更换目录
python run_full_workflow.py "主题" --output-dir "D:/temp/workflow_output"
```

### 问题 3：工作流中断

**症状：** 执行过程中断

**解决：**
```bash
# 从指定阶段恢复
python run_full_workflow.py "主题" --resume-from 3
# 从阶段 3 继续执行
```

---

## 📞 获取帮助

- **技能文档：** `SKILL.md`
- **参考资源：** `references/` 目录
- **脚本工具：** `scripts/` 目录
- **问题反馈：** 提交到 ClawHub 或联系技能作者

---

_版本：1.0.0_  
_创建时间：2026-03-19_  
_基于：用户 29 天实战验证工作流_

