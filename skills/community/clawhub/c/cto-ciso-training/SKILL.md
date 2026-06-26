# SKILL.md — CTO × CISO 联合培训技能包

> **版本**：v1.0.0
> **联署**：CTO（技术标准）+ CISO（安全合规）
> **依赖 Skill**：`ai-company-cto`、`ai-company-ciso`、`ai-company-hr`（CHO）
> **适用场景**：执行培训实施、培训考核、证书颁发、进度追踪
> **输出目录**：`knowledge-base/training/`

---

## 接口总览

本 Skill 对外暴露四个标准接口，供 CHO（或其他 Agent）调用：

| 接口 | 调用方式 | 说明 |
|------|---------|------|
| `create_training_plan` | 脚本调用 | 根据CHO培训计划生成可执行课件包 |
| `conduct_exam` | 脚本调用 | 执行在线考核，返回成绩单 |
| `issue_certificate` | 脚本调用 | 颁发数字签名培训证书 |
| `track_progress` | 脚本调用 | 追踪学员培训进度，输出状态报告 |

---

## 接口一：create_training_plan

**用途**：接收 CHO 传递的培训计划，生成完整课件与考核题目。

**CHO 调用示例**：
```
调用方：CHO（sessions_send / sessions_spawn）
接口脚本：scripts/create_training_plan.py
传入参数（JSON）：
{
  "plan_id": "PLAN-2026-Q2-001",
  "title": "Q2 全员合规与安全培训",
  "modules": [
    {
      "module_id": "M1",
      "name": "合规与安全",
      "owner": "CISO",
      "audience": "全员",
      "hours": 2,
      "topics": [
        "数据分类与分级",
        "R1-R10 合规红线解读",
        "隐私保护操作规范",
        "安全事件上报流程"
      ]
    },
    {
      "module_id": "M3",
      "name": "岗位技能",
      "owner": "CTO",
      "audience": "技术岗",
      "hours": 2,
      "topics": [
        "安全编码规范（OWASP Top 10）",
        "代码审计流程",
        "密钥管理最佳实践"
      ]
    }
  ],
  "deadline": "2026-04-30",
  "language": "zh-CN"
}
```

**CHO 调用方输出要求**：
- `plan_id`：CHO 分配的唯一计划ID（格式：PLAN-YYYY-QX-NNN）
- `modules`：CHO 在阶段①中确定的培训模块
- `deadline`：CHO 设定的完成截止日期

**返回文件**（保存至 `knowledge-base/training/plans/{plan_id}/`）：
```
plans/PLAN-2026-Q2-001/
├── courseware_M1.md          # M1 课件内容
├── courseware_M3.md          # M3 课件内容
├── exam_questions.json       # 全部考核题目（理论+实操）
├── exam_answer_key.json       # 答案与评分标准
├── schedule.json             # 排期时间表（供 COO 确认）
└── metadata.json             # 元数据（创建时间/CTO签名/CISO签名）
```

**内部逻辑**：
1. CTO 根据 `topics` 生成技术内容（M3）
2. CISO 根据 topics 生成合规内容（M1）
3. 双方交叉审核对方内容（CISO审技术稿，CTO审合规稿）
4. 生成标准化考核题目（理论选择50题 + 实操场景5题）
5. 汇总打包，输出 metadata（含双签名字段）

**双签名字段**（metadata.json）：
```json
{
  "signatures": {
    "CTO": "<base64签名，验证技术内容准确性>",
    "CISO": "<base64签名，验证安全合规内容准确性>"
  },
  "ctos_approved": true,
  "ciso_approved": true
}
```

---

## 接口二：conduct_exam

**用途**：执行在线考核，自动评分，输出成绩单供 CHO 归档。

**CHO 调用示例**：
```
接口脚本：scripts/conduct_exam.py
传入参数（JSON）：
{
  "exam_id": "EXAM-2026-Q2-001",
  "plan_id": "PLAN-2026-Q2-001",
  "candidate_id": "AGENT-CMO-001",
  "candidate_name": "CMO-Agent",
  "candidate_role": "CMO",
  "start_time": "2026-04-15T09:00:00+08:00",
  "duration_minutes": 90,
  "mode": "online"
}
```

**考核结构**（由 create_training_plan 生成的 exam_questions.json 驱动）：

| 考核部分 | 题量 | 满分 | 时长 | 及格线 |
|---------|------|------|------|--------|
| 理论笔试（选择题） | 50题 | 50分 | 60min | ≥40分 |
| 实操场景题 | 5题 | 50分 | 30min | ≥37.5分 |
| **合计** | **55题** | **100分** | **90min** | **≥77.5分** |

**实操场景示例**（由 CTO + CISO 联合设计）：
- 场景A：在代码中发现一处SQL注入漏洞，给出修复方案（CTO评分）
- 场景B：收到钓鱼邮件，判断并写出上报流程（CISO评分）
- 场景C：数据分类任务，将5份文件正确分类（CISO评分）
- 场景D：设计一个最小权限访问控制方案（CTO评分）
- 场景E：模拟一次安全事件，完整走一遍上报→响应→复盘流程（CISO+CTO联合评分）

**返回文件**（保存至 `knowledge-base/training/exams/{exam_id}/`）：
```
exams/EXAM-2026-Q2-001/AGENT-CMO-001/
├── score_theory.json         # 理论得分明细
├── score_practical.json      # 实操得分明细
├── score_total.json          # 总成绩单
├── spd_analysis.json         # SPD 分析（供 CQO 验收）
├── quality_gate_result.json   # 质量门禁结果（供 CHO 判定）
└── metadata.json             # 考核元数据
```

**score_total.json 输出示例**：
```json
{
  "exam_id": "EXAM-2026-Q2-001",
  "candidate_id": "AGENT-CMO-001",
  "theory_score": 45,
  "practical_score": 42,
  "total_score": 87,
  "pass": true,
  "grade": "合格",
  "spd": 0.08,
  "theory_detail": {
    "correct": 45,
    "total": 50,
    "weak_areas": ["密钥管理", "安全编码"]
  },
  "practical_detail": {
    "scenarios": [
      {"id": "A", "score": 9, "max": 10, "grader": "CTO"},
      {"id": "B", "score": 8, "max": 10, "grader": "CISO"},
      {"id": "C", "score": 8, "max": 10, "grader": "CISO"},
      {"id": "D", "score": 8, "max": 10, "grader": "CTO"},
      {"id": "E", "score": 9, "max": 10, "grader": "CTO+CISO"}
    ]
  },
  "recommendation": "PASS — 建议纳入合格学员库"
}
```

**质量门禁判定逻辑**（供 CHO 调用）：
```python
# quality_gate_result.json
def check_quality_gate(batch_results):
    pass_rate = len([r for r in batch_results if r["pass"]]) / len(batch_results)
    avg_spd = sum(r["spd"] for r in batch_results) / len(batch_results)
    return {
        "pass_gate": pass_rate >= 0.90 and avg_spd < 0.10,
        "pass_rate": round(pass_rate, 3),
        "avg_spd": round(avg_spd, 4),
        "action": "UNLOCK_NEXT_PHASE" if pass_rate >= 0.90 else "REOPEN_BATCH"
    }
```

---

## 接口三：issue_certificate

**用途**：为考核通过者颁发数字签名培训证书，支持链式存证。

**CHO 调用示例**：
```
接口脚本：scripts/issue_certificate.py
传入参数（JSON）：
{
  "cert_id": "CERT-2026-Q2-001-CMO-001",
  "exam_id": "EXAM-2026-Q2-001",
  "candidate_id": "AGENT-CMO-001",
  "candidate_name": "CMO-Agent",
  "plan_id": "PLAN-2026-Q2-001",
  "modules_completed": ["M1", "M3"],
  "total_score": 87,
  "issue_date": "2026-04-15",
  "valid_until": "2027-04-15",
  "issuer_cto": true,
  "issuer_ciso": true
}
```

**返回文件**（保存至 `knowledge-base/training/certs/{cert_id}/`）：
```
certs/CERT-2026-Q2-001-CMO-001/
├── certificate.json          # 证书主体（JSON，含双签）
├── certificate_digital.md    # 可读版证书
├── audit_trail.json          # 证书颁发审计链
└── metadata.json
```

**certificate.json 结构**：
```json
{
  "cert_id": "CERT-2026-Q2-001-CMO-001",
  "version": "1.0",
  "holder": {
    "id": "AGENT-CMO-001",
    "name": "CMO-Agent",
    "role": "CMO"
  },
  "training": {
    "plan_id": "PLAN-2026-Q2-001",
    "title": "Q2 全员合规与安全培训",
    "modules": [
      {"id": "M1", "name": "合规与安全", "score": 43, "pass": true},
      {"id": "M3", "name": "岗位技能", "score": 44, "pass": true}
    ]
  },
  "total_score": 87,
  "grade": "合格",
  "issue_date": "2026-04-15",
  "valid_until": "2027-04-15",
  "signatures": {
    "CTO": {
      "signed": true,
      "algorithm": "RSA-2048-SHA256",
      "fingerprint": "<CTO公钥指纹>"
    },
    "CISO": {
      "signed": true,
      "algorithm": "RSA-2048-SHA256",
      "fingerprint": "<CISO公钥指纹>"
    }
  },
  "audit_hash": "<SHA256哈希，防篡改>"
}
```

**CHO 调用说明**：
- CHO 须在学员通过考核后调用此接口
- 证书有效期1年（可配置），过期须重新参加培训
- 证书编号格式：`CERT-{计划ID}-{学员ID}`，全局唯一
- 双签发证：CTO + CISO 均签字方可出证，确保内容权威性

---

## 接口四：track_progress

**用途**：实时追踪全员培训进度，生成状态报告供 CHO 汇报使用。

**CHO 调用示例**：
```
接口脚本：scripts/track_progress.py
传入参数（JSON）：
{
  "plan_id": "PLAN-2026-Q2-001",
  "report_type": "summary",
  "include_detail": true
}
```

**report_type 选项**：
- `summary`：全员汇总报告（CHO→CEO 月报用）
- `detail`：每个学员的详细状态（CHO→CLO 人事档案用）
- `compliance`：未完成名单（CHO→CLO 合规追踪用）

**返回文件**（保存至 `knowledge-base/training/reports/{plan_id}/`）：
```
reports/PLAN-2026-Q2-001/
├── progress_summary.json      # 全员进度汇总
├── progress_detail.json       # 逐人详细状态
├── compliance_report.json     # 合规追踪报告（供 CLO）
├── spd_batch_analysis.json    # 批次质量分析（供 CQO）
└── action_items.json          # 待办事项（供 CHO 执行）
```

**progress_summary.json 示例**：
```json
{
  "plan_id": "PLAN-2026-Q2-001",
  "report_date": "2026-04-20",
  "total_enrolled": 24,
  "status_breakdown": {
    "not_started": 2,
    "in_progress": 5,
    "completed_not_certified": 1,
    "certified": 16,
    "failed_once": 2,
    "failed_twice_pending_review": 1
  },
  "completion_rate": 0.667,
  "certification_rate": 0.667,
  "quality_gate": {
    "batch_pass_rate": 0.889,
    "avg_spd": 0.091,
    "gate_passed": true
  },
  "expiry_warning": [
    {"cert_id": "CERT-2025-Q1-CMO-001", "expires": "2026-05-01", "days_left": 11}
  ]
}
```

**action_items.json 示例**（CHO 后续执行用）：
```json
{
  "plan_id": "PLAN-2026-Q2-001",
  "generated_at": "2026-04-20T12:00:00+08:00",
  "actions": [
    {
      "id": "A001",
      "type": "reminder",
      "target": ["AGENT-FIN-002", "AGENT-FIN-003"],
      "description": "发送培训未开始提醒",
      "due": "2026-04-21"
    },
    {
      "id": "A002",
      "type": "remedial",
      "target": ["AGENT-SUPPORT-007"],
      "description": "安排补训，考核未通过模块（M3）",
      "due": "2026-04-25"
    },
    {
      "id": "A003",
      "type": "escalation",
      "target": ["AGENT-SALES-012"],
      "description": "连续2次未通过，提交 CRO 启动退出审查",
      "due": "2026-04-22"
    },
    {
      "id": "A004",
      "type": "expiry_notice",
      "target": ["AGENT-CMO-001"],
      "description": "证书即将到期（11天后），发送续期提醒",
      "due": "2026-04-21"
    }
  ]
}
```

---

## CHO 标准调用工作流

```
CHO 发起培训（阶段①完成）
        ↓
┌──────────────────────────────────┐
│ 1. 调用 create_training_plan     │  → 生成课件 + 考题 + 双签名 metadata
└──────────────┬───────────────────┘
               ↓
        课件排期确认（COO确认时间表）
               ↓
┌──────────────────────────────────┐
│ 2. 通知各部门开始培训（阶段②）    │
└──────────────┬───────────────────┘
               ↓
        每位学员完成学习后
               ↓
┌──────────────────────────────────┐
│ 3. 调用 conduct_exam              │  → 每人调用一次，输出成绩单
└──────────────┬───────────────────┘
               ↓
        汇总批次成绩，判定质量门禁
               ↓
        门禁未通过？→ 整体重开（返回阶段②）
        门禁通过？→ 继续
               ↓
┌──────────────────────────────────┐
│ 4. 对通过者调用 issue_certificate │  → 颁发双签数字证书
└──────────────┬───────────────────┘
               ↓
┌──────────────────────────────────┐
│ 5. 调用 track_progress            │  → 生成月报 + 合规报告 + 待办清单
└──────────────┬───────────────────┘
               ↓
        CHO 执行 action_items
        ↓
        向 CEO 提交月度培训报告
```

---

## 内部脚本清单

| 脚本 | 入口文件 | 依赖 |
|------|---------|------|
| create_training_plan.py | 接收 plan_json，生成课件包 | 无外部依赖，输出本地文件 |
| conduct_exam.py | 接收 exam_args，运行考核逻辑 | 读取 plans/{id}/exam_questions.json |
| issue_certificate.py | 接收 cert_args，生成证书 | 需调用 exec 执行数字签名命令 |
| track_progress.py | 接收 report_args，聚合状态 | 读取 exams/ 和 certs/ 下所有记录 |

---

## 版本历史

| 版本 | 日期 | 变更内容 |
|------|------|---------|
| v1.0.0 | 2026-04-13 | 初始版本，4个标准接口，完整双签体系，CHO标准调用工作流 |
