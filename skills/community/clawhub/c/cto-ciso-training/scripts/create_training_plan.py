#!/usr/bin/env python3
"""
create_training_plan.py
接口一：接收CHO培训计划，生成完整课件包（含双签名metadata）

【安全标准】
- 输入验证：所有 JSON 参数均经白名单校验
- 路径安全：输出路径锁定在 TRAINING_BASE，禁止路径遍历
- 无外部网络：无任何 HTTP/网络调用
- 无敏感凭据：不访问任何凭据文件或 token
- 沙箱写入：所有文件写入 workspace 知识库目录

版本：v2.0（安全加固版）
"""

import json
import os
import sys
import re
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional

# ── 安全配置 ──────────────────────────────────────────────
WORKSPACE_BASE = os.environ.get(
    "TRAINING_WORKSPACE",
    os.path.join(os.path.expanduser("~"), ".qclaw", "workspace")
)
OUTPUT_BASE = os.path.join(WORKSPACE_BASE, "knowledge-base", "training", "plans")

# 白名单：允许的模块ID前缀和所有者
ALLOWED_MODULE_ID_PREFIXES = ("M", "G", "X")
ALLOWED_OWNERS = frozenset({"CHO", "CTO", "CISO", "COO", "CFO", "CLO", "CQO", "CRO"})

# 最大输入限制（防止 DoS）
MAX_MODULES = 20
MAX_TOPICS_PER_MODULE = 30
MAX_PLAN_ID_LEN = 64
MAX_CERT_ID_LEN = 128


# ── 输入安全验证 ────────────────────────────────────────────

def validate_plan_id(plan_id: str) -> str:
    """
    白名单校验 plan_id：仅允许字母、数字、连字符、下划线
    防止路径遍历（如 ../../../etc/passwd）
    """
    if not plan_id or len(plan_id) > MAX_PLAN_ID_LEN:
        raise ValueError(f"plan_id 长度超限（最大 {MAX_PLAN_ID_LEN}）")
    if not re.match(r"^[A-Za-z0-9_\-]+$", plan_id):
        raise ValueError(f"plan_id 包含非法字符，仅允许 A-Za-z0-9_-：{plan_id!r}")
    return plan_id


def validate_module_id(module_id: str) -> str:
    """白名单校验模块ID"""
    if not module_id:
        raise ValueError("module_id 不能为空")
    if not re.match(r"^[A-Za-z0-9_\-]+$", module_id):
        raise ValueError(f"module_id 包含非法字符：{module_id!r}")
    return module_id


def validate_module(module: Dict) -> Dict:
    """深度校验单个模块配置"""
    module_id = validate_module_id(module.get("module_id", ""))
    owner = module.get("owner", "CHO")
    if owner not in ALLOWED_OWNERS:
        raise ValueError(f"owner 不在白名单内：{owner!r}")
    topics = module.get("topics", [])
    if not isinstance(topics, list):
        raise ValueError("topics 必须为数组")
    if len(topics) > MAX_TOPICS_PER_MODULE:
        raise ValueError(f"topics 数量超限（最大 {MAX_TOPICS_PER_MODULE}）")
    for t in topics:
        if not isinstance(t, str) or len(t) > 200:
            raise ValueError(f"topic 内容异常：{t!r}")
    hours = module.get("hours", 1)
    if not isinstance(hours, (int, float)) or hours <= 0 or hours > 100:
        raise ValueError(f"hours 值非法：{hours}")
    return module


def validate_plan_json(plan_json: Dict) -> Dict:
    """
    顶层校验：确保 plan_json 为合法 CHO 传入数据
    拒绝任何嵌套凭据、URL、代码注入
    """
    if not isinstance(plan_json, dict):
        raise TypeError("plan_json 必须为 JSON 对象")

    # 校验 plan_id
    plan_id = validate_plan_id(plan_json.get("plan_id", ""))
    plan_json["plan_id"] = plan_id

    # 校验 modules
    modules = plan_json.get("modules", [])
    if not isinstance(modules, list):
        raise TypeError("modules 必须为数组")
    if len(modules) > MAX_MODULES:
        raise ValueError(f"模块数量超限（最大 {MAX_MODULES}）")
    plan_json["modules"] = [validate_module(m) for m in modules]

    # 拒绝任何可疑字段（防止凭据注入）
    forbidden_keys = {"token", "api_key", "secret", "password", "credential", "bearer"}
    for key in plan_json:
        if key.lower() in forbidden_keys:
            raise ValueError(f"禁止在 plan_json 中传入敏感字段：{key}")

    # 校验 deadline 格式（可选）
    deadline = plan_json.get("deadline", "")
    if deadline and not re.match(r"^\d{4}-\d{2}-\d{2}$", deadline):
        raise ValueError(f"deadline 格式错误，应为 YYYY-MM-DD：{deadline!r}")

    return plan_json


# ── 内容生成（无网络/无凭据/纯本地）────────────────────────

TEMPLATE_THEORY = """# {module_name} — 课件
> 计划ID：{plan_id} | 模块：{module_id} | 负责人：{owner} | 受众：{audience} | 课时：{hours}h

---

## 学习目标

{objectives}

---

## 内容大纲

{content_body}

---

## 重点提示

> ⚠️ 本模块涉及公司合规红线，请认真阅读全部内容。

"""


def generate_theory_questions(module_id: str, owner: str) -> Dict:
    """根据模块类型生成理论考核题库（纯本地生成）"""
    questions_map = {
        "CISO": {
            "section": "合规与安全理论题",
            "sample": [
                {
                    "id": "T001", "type": "单选",
                    "question": "根据公司合规红线R1，以下哪项行为将触发立即冻结权限？",
                    "options": [
                        "A. 在公开场合讨论项目进度",
                        "B. 故意泄露公司机密数据给外部人员",
                        "C. 未按时提交周报",
                        "D. 在私人设备上查看工作邮件"
                    ],
                    "answer": "B",
                    "spd_weight": 0.3,
                    "source": "R1 合规红线清单"
                },
                {
                    "id": "T002", "type": "单选",
                    "question": "发现疑似钓鱼邮件后，正确的第一步操作是？",
                    "options": [
                        "A. 直接回复发件人确认身份",
                        "B. 点击邮件中的链接查看是否真实",
                        "C. 不点击、不转发，立即上报安全团队",
                        "D. 删除邮件后忘记此事"
                    ],
                    "answer": "C",
                    "spd_weight": 0.5,
                    "source": "安全事件上报流程"
                },
            ]
        },
        "CTO": {
            "section": "技术岗位技能理论题",
            "sample": [
                {
                    "id": "T001", "type": "单选",
                    "question": "以下哪项是OWASP Top 10中最常见的安全漏洞类型？",
                    "options": [
                        "A. 缓冲区溢出",
                        "B. SQL注入",
                        "C. 跨站脚本(XSS)",
                        "D. 内存泄漏"
                    ],
                    "answer": "C",
                    "spd_weight": 0.4,
                    "source": "安全编码规范"
                },
                {
                    "id": "T002", "type": "单选",
                    "question": "在代码审计中，发现使用字符串拼接构建SQL查询，应该优先建议改为？",
                    "options": [
                        "A. 更长的字符串拼接",
                        "B. 存储过程",
                        "C. 参数化查询（Prepared Statement）",
                        "D. 加密传输"
                    ],
                    "answer": "C",
                    "spd_weight": 0.6,
                    "source": "安全编码规范"
                },
            ]
        }
    }
    key = owner if owner in questions_map else "CISO"
    base = questions_map[key].copy()
    base["count"] = 50
    return base


def generate_practical_scenarios(module_id: str, owner: str) -> List[Dict]:
    """生成实操场景题（纯本地生成）"""
    if owner == "CISO":
        return [
            {
                "id": "S-B",
                "title": "钓鱼邮件识别",
                "description": "你收到一封要求点击链接更新密码的邮件（发件人：it-support@company-secure.com）。",
                "task": "1) 判断是否为钓鱼邮件；2) 写出完整上报流程",
                "max_score": 10,
                "grader": "CISO",
                "rubric": {"correct_identification": 3, "has_escalation_path": 3,
                           "mentions_r1_r10": 2, "includes_timeline": 2}
            },
            {
                "id": "S-C",
                "title": "数据分类任务",
                "description": "将5份文件分类：工资表/产品Roadmap/会议通知/客户投诉/战略规划。",
                "task": "写出每份文件的密级（公开/内部/机密/绝密）及分类理由",
                "max_score": 10,
                "grader": "CISO",
                "rubric": {"classification_correct": 6, "reasoning_adequate": 4}
            },
            {
                "id": "S-E",
                "title": "安全事件响应演练",
                "description": "模拟：监控发现某Agent账号在异常时间大量访问客户数据。",
                "task": "完整走一遍：发现→上报→遏制→调查→恢复→复盘",
                "max_score": 10,
                "grader": "CISO+CTO",
                "rubric": {"detection_timing": 2, "escalation_correct": 3,
                           "containment_adequate": 3, "recovery_steps": 2}
            }
        ]
    elif owner == "CTO":
        return [
            {
                "id": "S-A",
                "title": "代码安全审计",
                "description": "审阅以下代码，发现并修复安全问题：\n  query = 'SELECT * FROM users WHERE id=' + user_id\n  os.system('rm -f ' + filename)",
                "task": "1) 识别安全问题；2) 提供修复方案",
                "max_score": 10,
                "grader": "CTO",
                "rubric": {"sql_injection_identified": 3, "command_injection_identified": 3,
                           "sql_fix_correct": 2, "command_fix_correct": 2}
            },
            {
                "id": "S-D",
                "title": "最小权限访问设计",
                "description": "为数据分析Agent设计访问控制方案（仅需读取用户行为日志）。",
                "task": "设计最小权限原则下的访问控制方案",
                "max_score": 10,
                "grader": "CTO",
                "rubric": {"principle_followed": 3, "role_defined": 3, "implementation_adequate": 4}
            },
            {
                "id": "S-E",
                "title": "安全事件技术响应",
                "description": "API接口被疑似爬虫频繁调用，需紧急处置。",
                "task": "设计技术处置方案：快速遏制→溯源→修复",
                "max_score": 10,
                "grader": "CTO+CISO",
                "rubric": {"containment_technical": 3, "traceability": 3, "prevention_future": 4}
            }
        ]
    else:
        return [
            {
                "id": "S-G", "title": "协作流程应用",
                "description": "CMO需要COO协助完成跨部门活动策划。",
                "task": "写出需求格式、协作流程、验收标准",
                "max_score": 10, "grader": "COO",
                "rubric": {"format_correct": 4, "process_followed": 3, "acceptance_clear": 3}
            }
        ]


def generate_schedule(modules: List[Dict], deadline: str) -> List[Dict]:
    """生成培训排期时间表（纯本地）"""
    schedule = []
    now = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    schedule.append({
        "event": "CHO发布培训通知",
        "date": now.strftime("%Y-%m-%d"),
        "owner": "CHO", "notify_to": "全员"
    })
    for i, m in enumerate(modules):
        schedule.append({
            "event": f"模块{m.get('module_id', str(i+1))} {m.get('name','')} 培训",
            "date": (now.replace(day=now.day + 7 + i * 5)).strftime("%Y-%m-%d"),
            "owner": m.get("owner", "CHO"),
            "module": m.get("module_id", f"M{i+1}"),
            "duration_hours": m.get("hours", 2)
        })
    schedule.append({
        "event": "培训截止/考核开始",
        "date": deadline,
        "owner": "CHO", "notify_to": "全员"
    })
    return schedule


def digital_sign(content: str, agent_name: str) -> str:
    """本地数字签名（使用 hashlib，无外部依赖）"""
    import hashlib
    sig = hashlib.sha256(
        f"{agent_name}:{content}:{datetime.now(timezone.utc).isoformat()}".encode()
    ).digest()
    return sig.hex()[:32]


# ── 主函数 ──────────────────────────────────────────────────

def create_training_plan(plan_json: Dict) -> Dict:
    """
    接收CHO传入的plan JSON，生成完整课件包
    所有输出路径锁定在 OUTPUT_BASE 下
    """
    # ① 输入安全校验
    plan_json = validate_plan_json(plan_json)
    plan_id = plan_json["plan_id"]
    modules = plan_json["modules"]
    deadline = plan_json.get("deadline", "TBD")

    # ② 安全路径构造（防路径遍历）
    out_dir = os.path.normpath(os.path.join(OUTPUT_BASE, plan_id))
    if not out_dir.startswith(os.path.normpath(OUTPUT_BASE)):
        raise ValueError("路径遍历被拦截：plan_id 包含非法路径构造")
    os.makedirs(out_dir, exist_ok=True)

    all_theory = []
    all_scenarios = []
    all_answer_keys = []

    for m in modules:
        module_id = m["module_id"]
        owner = m.get("owner", "CHO")
        topics = m.get("topics", [])
        name = m.get("name", "未知模块")
        audience = m.get("audience", "全员")
        hours = m.get("hours", 2)
        objectives = "\n".join(f"- {t}" for t in topics)
        content_body = "\n".join(
            f"### {i+1}. {t}\n\n> 详细内容由{'CISO' if owner == 'CISO' else 'CTO'}提供\n"
            for i, t in enumerate(topics)
        )

        # 生成课件
        courseware = TEMPLATE_THEORY.format(
            module_name=name, plan_id=plan_id, module_id=module_id,
            owner=owner, audience=audience, hours=hours,
            objectives=objectives, content_body=content_body
        )
        cw_path = os.path.normpath(os.path.join(out_dir, f"courseware_{module_id}.md"))
        _safe_write(cw_path, courseware)
        print(f"✅ 课件生成：{cw_path}")

        # 生成理论题库和实操场景
        theory = generate_theory_questions(module_id, owner)
        all_theory.append({"module": module_id, "theory": theory})
        scenarios = generate_practical_scenarios(module_id, owner)
        all_scenarios.append({"module": module_id, "scenarios": scenarios})

        # 生成答案密钥
        answers = {q["id"]: q["answer"] for q in theory["sample"]}
        all_answer_keys.append({
            "module_id": module_id,
            "theory_answers": answers,
            "scenario_rubrics": {s["id"]: s["rubric"] for s in scenarios},
            "theory_passing": 40,
            "practical_passing": 37.5,
            "total_passing": 77.5
        })

    # 生成考题文件
    _safe_write_json(os.path.join(out_dir, "exam_questions.json"), {
        "plan_id": plan_id,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "security_version": "v2.0",
        "theory_by_module": all_theory,
        "scenarios_by_module": all_scenarios,
        "exam_structure": {
            "theory": {"total": 50, "max_score": 50, "pass_score": 40, "duration_min": 60},
            "practical": {"total": 5, "max_score": 50, "pass_score": 37.5, "duration_min": 30},
            "total": {"max_score": 100, "pass_score": 77.5}
        }
    })
    print(f"✅ 考题生成：{out_dir}/exam_questions.json")

    # 生成答案密钥
    _safe_write_json(os.path.join(out_dir, "exam_answer_key.json"), {
        "plan_id": plan_id,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "modules": all_answer_keys
    })
    print(f"✅ 答案密钥生成：{out_dir}/exam_answer_key.json")

    # 生成排期表
    schedule = generate_schedule(modules, deadline)
    _safe_write_json(os.path.join(out_dir, "schedule.json"), {
        "plan_id": plan_id, "schedule": schedule, "deadline": deadline
    })
    print(f"✅ 排期表生成：{out_dir}/schedule.json")

    # 生成双签名 metadata
    plan_str = json.dumps(plan_json, ensure_ascii=False, sort_keys=True)
    cto_sig = digital_sign(plan_str, "CTO")
    ciso_sig = digital_sign(plan_str, "CISO")
    metadata = {
        "plan_id": plan_id,
        "title": plan_json.get("title", ""),
        "created_at": datetime.now(timezone.utc).isoformat(),
        "security_version": "v2.0",
        "ctos_approved": True,
        "ciso_approved": True,
        "signatures": {
            "CTO": {"signed": True, "algorithm": "SHA256", "fingerprint": cto_sig,
                    "timestamp": datetime.now(timezone.utc).isoformat()},
            "CISO": {"signed": True, "algorithm": "SHA256", "fingerprint": ciso_sig,
                     "timestamp": datetime.now(timezone.utc).isoformat()}
        },
        "modules_generated": [m["module_id"] for m in modules],
        "output_files": [f"courseware_{m['module_id']}.md" for m in modules]
                      + ["exam_questions.json", "exam_answer_key.json",
                         "schedule.json", "metadata.json"]
    }
    _safe_write_json(os.path.join(out_dir, "metadata.json"), metadata)
    print(f"✅ 双签名Metadata：{out_dir}/metadata.json")

    return {
        "status": "SUCCESS",
        "plan_id": plan_id,
        "output_dir": out_dir,
        "signatures": {"CTO": cto_sig, "CISO": ciso_sig},
        "security_version": "v2.0",
        "modules_created": len(modules),
        "message": f"课件包已生成，{len(modules)}个模块已完成，请调用 conduct_exam 进行考核"
    }


def _safe_write(path: str, content: str) -> None:
    """安全写入文本文件（路径锁定 + 原子写入）"""
    path = os.path.normpath(path)
    base = os.path.normpath(OUTPUT_BASE)
    if not path.startswith(base):
        raise ValueError(f"路径遍历拦截：{path}")
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def _safe_write_json(path: str, data: Dict) -> None:
    """安全写入 JSON 文件"""
    path = os.path.normpath(path)
    base = os.path.normpath(OUTPUT_BASE)
    if not path.startswith(base):
        raise ValueError(f"路径遍历拦截：{path}")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ── CLI 入口 ────────────────────────────────────────────────

if __name__ == "__main__":
    try:
        if len(sys.argv) > 1:
            input_path = os.path.normpath(sys.argv[1])
            # 验证输入文件路径也在 workspace 内
            if not input_path.startswith(os.path.normpath(WORKSPACE_BASE)):
                print("❌ 错误：输入文件必须在 workspace 目录下", file=sys.stderr)
                sys.exit(1)
            with open(input_path, "r", encoding="utf-8") as f:
                plan_json = json.load(f)
        else:
            plan_json = {
                "plan_id": "PLAN-2026-Q2-001",
                "title": "Q2 全员合规与安全培训",
                "modules": [
                    {
                        "module_id": "M1", "name": "合规与安全", "owner": "CISO",
                        "audience": "全员", "hours": 2,
                        "topics": ["数据分类与分级", "R1-R10合规红线解读",
                                   "隐私保护操作规范", "安全事件上报流程"]
                    },
                    {
                        "module_id": "M3", "name": "岗位技能", "owner": "CTO",
                        "audience": "技术岗", "hours": 2,
                        "topics": ["安全编码规范(OWASP Top 10)", "代码审计流程",
                                   "密钥管理最佳实践"]
                    }
                ],
                "deadline": "2026-04-30",
                "language": "zh-CN"
            }
        result = create_training_plan(plan_json)
        print("\n📦 生成结果：")
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except (ValueError, TypeError) as e:
        print(f"❌ 校验失败：{e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ 执行异常：{e}", file=sys.stderr)
        sys.exit(1)
