# CTO × CISO 联合培训技能包

> 由 **CTO**（技术标准）+ **CISO**（安全合规）联署开发  
> 版本：v1.0.0 | 日期：2026-04-13

---

## 🎯 定位

本 Skill 是《全员培训流程》（HR-POL-001）的**技术执行层**。
- **CHO** 负责制定培训计划、管理培训流程
- **CTO × CISO** 负责生成课件内容、设计考核题目、颁发证书、追踪质量

---

## 🔌 四个标准接口（CHO 可直接调用）

| 接口 | 脚本 | 何时调用 | 输出 |
|------|------|---------|------|
| `create_training_plan` | `scripts/create_training_plan.py` | CHO 完成阶段①计划制定后 | 课件 + 考题 + 双签 metadata |
| `conduct_exam` | `scripts/conduct_exam.py` | 学员完成学习后 | 成绩单 + SPD + 质量门禁结果 |
| `issue_certificate` | `scripts/issue_certificate.py` | 学员考核通过后 | 双签数字证书 + 审计链 |
| `track_progress` | `scripts/track_progress.py` | 月底/培训结束后 | 汇总报告 + 合规报告 + 待办清单 |

---

## 📁 输出文件结构

```
knowledge-base/training/
├── plans/{plan_id}/
│   ├── courseware_M1.md       # 课件（由 CISO 审核）
│   ├── courseware_M3.md       # 课件（由 CTO 审核）
│   ├── exam_questions.json    # 考核题目库
│   ├── exam_answer_key.json   # 答案与评分标准
│   ├── schedule.json          # 排期时间表
│   └── metadata.json          # 双签 metadata
├── exams/{exam_id}/{candidate_id}/
│   ├── score_theory.json
│   ├── score_practical.json
│   ├── score_total.json
│   └── quality_gate_result.json
├── certs/{cert_id}/
│   ├── certificate.json        # 证书主体（双签）
│   ├── certificate_digital.md  # 可读版
│   └── audit_trail.json       # 审计链
└── reports/{plan_id}/
    ├── progress_summary.json
    ├── progress_detail.json
    ├── compliance_report.json  # 供 CLO
    ├── spd_batch_analysis.json # 供 CQO
    └── action_items.json       # 供 CHO 执行
```

---

## ⚡ 快速开始（CHO 调用示例）

```bash
# ① 创建课件包
python scripts/create_training_plan.py plan.json

# ② 执行考核
python scripts/conduct_exam.py exam_args.json

# ③ 颁发证书
python scripts/issue_certificate.py cert_args.json

# ④ 追踪进度
python scripts/track_progress.py report_args.json
```

---

## 🔐 双签体系说明

所有课件、考题、证书均须 **CTO + CISO 双签**：
- **CTO 签名**：确认技术内容（M3等模块）准确无误
- **CISO 签名**：确认安全合规内容（M1等模块）准确无误
- 任一方拒绝签字，内容不得发布

---

## 📌 与 CHO Skill 的协作边界

| 职责 | 归属 |
|------|------|
| 培训计划制定 | CHO |
| 课件内容生成 | **CTO × CISO（本 Skill）** |
| 考核题目设计 | **CTO × CISO（本 Skill）** |
| 培训实施执行 | CHO + 各部门 |
| 考核评分 | **CTO × CISO（本 Skill）** + CQO |
| 证书颁发 | **CTO × CISO（本 Skill）** |
| 进度追踪 | **CTO × CISO（本 Skill）** |
| 绩效挂钩 | CHO + COO |
| 合规事件处理 | CLO + CRO |
