#!/usr/bin/env python3
"""
DigitalSalesClaw - engine.py
统一工作流引擎（合并 workflow.py + conditional_engine.py）

功能：
- 声明式工作流（预定义模板）
- 条件执行引擎（if/for/while/retry）
- 告警发送（集成 triggers 告警逻辑）

输入: {"action": "run|status|list|templates|validate", "workflow": "...", "context": {...}}
输出: {"execution_id, status, steps_results, ...}
"""

import sys
import json
import uuid
import re
import time
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from db import get_conn, close_conn

SKILL_DIR = Path(__file__).parent.parent

# ─────────────────────────────────────────
# 数据库连接（MySQL 优先）
# ─────────────────────────────────────────

def _get_conn():
    try:
        import mysql.connector
        from mysql.connector import pooling
        pool = pooling.MySQLConnectionPool(
            host="localhost", port=3306, user="ontology", unix_socket="/tmp/mysql.sock",
            password="ontology", database="digitalsalesclaw",
            pool_name="dsc_engine", pool_size=3, charset="utf8mb4"
        )
        conn = pool.get_connection()
        conn.autocommit = False
        return conn, False
    except Exception:
        conn = get_conn()
        return conn, True


# ─────────────────────────────────────────
# 执行上下文（ConditionalEngine 运行时变量）
# ─────────────────────────────────────────

class ExecutionContext:
    def __init__(self):
        self.variables = {}
        self.results = {}
        self.logs = []
        self.alerts = []

    def set(self, key: str, value):
        self.variables[key] = value

    def get(self, key: str, default=None):
        return self.variables.get(key, default)

    def inject(self, data: dict):
        self.variables.update(data)

    def log(self, msg: str, level: str = "INFO"):
        self.logs.append(f"[{level}] {datetime.now().isoformat()} | {msg}")

    def record(self, step_id: str, result):
        self.results[step_id] = result


# ─────────────────────────────────────────
# 条件求值器
# ─────────────────────────────────────────

class ConditionEvaluator:
    OPERATORS = {
        "<":  lambda a, b: a < b,
        ">":  lambda a, b: a > b,
        "<=": lambda a, b: a <= b,
        ">=": lambda a, b: a >= b,
        "==": lambda a, b: a == b,
        "!=": lambda a, b: a != b,
        "in": lambda a, b: a in b,
        "not in": lambda a, b: a not in b,
        "and": lambda a, b: a and b,
        "or":  lambda a, b: a or b,
        "not": lambda a: not a,
        "contains": lambda a, b: b in a if a else False,
    }

    def __init__(self, context: ExecutionContext):
        self.context = context

    def evaluate(self, condition: str) -> bool:
        if not condition or condition.strip() == "":
            return True
        cond = condition.strip()
        if " and " in cond:
            return all(self.evaluate(p.strip()) for p in cond.split(" and "))
        if " or " in cond:
            return any(self.evaluate(p.strip()) for p in cond.split(" or "))
        if cond.startswith("not "):
            return not self.evaluate(cond[4:].strip())
        for op in [">=", "<=", "!=", "==", "<", ">", " in ", " not in "]:
            if op in cond:
                parts = cond.split(op)
                if len(parts) == 2:
                    return self._compare(parts[0].strip(), op.strip(), parts[1].strip())
        return False

    def _compare(self, left: str, op: str, right: str) -> bool:
        lval = self._resolve_value(left)
        rval = self._parse_value(right)
        if lval is None:
            return False
        if op == "in":
            return lval in rval
        elif op == "not in":
            return lval not in rval
        elif op == "contains":
            return rval in lval if isinstance(lval, str) else False
        else:
            fn = self.OPERATORS.get(op)
            if fn:
                try:
                    return fn(float(lval), float(rval))
                except (ValueError, TypeError):
                    try:
                        return fn(lval, rval)
                    except TypeError:
                        return False
        return False

    def _resolve_value(self, key: str):
        key = key.strip()
        if "." in key:
            parts = key.split(".", 1)
            obj = self.context.get(parts[0])
            if obj and isinstance(obj, dict):
                return obj.get(parts[1])
            return None
        if "[" in key and key.endswith("]"):
            var, idx = key[:-1].split("[")
            idx = int(idx.strip())
            arr = self.context.get(var.strip())
            if isinstance(arr, list) and len(arr) > idx:
                return arr[idx]
            return None
        val = self.context.get(key)
        if val is None and key.lower() in ("true", "false"):
            return key.lower() == "true"
        return val

    def _parse_value(self, s: str):
        s = s.strip()
        if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
            return s[1:-1]
        if s.startswith("[") and s.endswith("]"):
            items = s[1:-1].split(",")
            return [self._parse_value(i.strip()) for i in items if i.strip()]
        try:
            return float(s) if "." in s else int(s)
        except ValueError:
            pass
        if s.lower() in ("true",):
            return True
        if s.lower() in ("false",):
            return False
        if s.lower() in ("none", "null"):
            return None
        return self._resolve_value(s)


# ─────────────────────────────────────────
# 工具执行器
# ─────────────────────────────────────────

def exec_tool(tool_name: str, params: dict, context: ExecutionContext) -> dict:
    import subprocess
    context.log(f"执行工具: {tool_name} params={params}")
    tool_path = SKILL_DIR / "tools" / f"{tool_name}.py"
    if not tool_path.exists():
        return {"error": f"Tool not found: {tool_name}"}
    try:
        result = subprocess.run(
            ["python3", str(tool_path), json.dumps(params)],
            capture_output=True, text=True, timeout=30,
            cwd=str(SKILL_DIR / "tools"),
        )
        if result.returncode != 0:
            context.log(f"工具执行失败: {result.stderr}", "ERROR")
            return {"error": result.stderr}
        try:
            return json.loads(result.stdout.strip().split('\n')[-1])
        except json.JSONDecodeError:
            return {"raw": result.stdout.strip()}
    except subprocess.TimeoutExpired:
        context.log(f"工具执行超时: {tool_name}", "ERROR")
        return {"error": f"Timeout: {tool_name}"}
    except Exception as e:
        context.log(f"工具执行异常: {e}", "ERROR")
        return {"error": str(e)}


# ─────────────────────────────────────────
# 条件执行引擎
# ─────────────────────────────────────────

class ConditionalEngine:
    def __init__(self, workflow: dict):
        self.workflow = workflow
        self.context = ExecutionContext()
        self.steps_def = workflow.get("steps", [])
        self.variables = workflow.get("variables", {})
        self.results = []
        self.status = "running"

    def run(self, input_context: dict = None) -> dict:
        if input_context:
            self.context.inject(input_context)
        for k, v in self.variables.items():
            self.context.set(k, v)
        pre_condition = self.workflow.get("condition")
        if pre_condition:
            evaluator = ConditionEvaluator(self.context)
            if not evaluator.evaluate(pre_condition):
                self.status = "skipped"
                self.context.log("工作流因条件不满足而跳过")
                return self._build_result("skipped")
        try:
            for i, step in enumerate(self.steps_def):
                step_result = self._execute_step(step, step_index=i)
                self.results.append(step_result)
                if step_result.get("stop"):
                    self.context.log(f"工作流在步骤 {i} 停止")
                    break
            self.status = "completed"
            return self._build_result("completed")
        except Exception as e:
            self.status = "failed"
            self.context.log(f"工作流执行失败: {e}", "ERROR")
            return self._build_result("failed", error=str(e))

    def _execute_step(self, step: dict, step_index: int) -> dict:
        step_id = step.get("id", f"step_{step_index}")
        self.context.log(f"执行步骤: {step_id}")
        if "if" in step:
            return self._execute_if(step["if"], step_id)
        if "while" in step:
            return self._execute_while(step["while"], step.get("do", []), step_id)
        if "for" in step:
            return self._execute_for(step["for"], step.get("do", []), step_id)
        if "exec" in step:
            return self._execute_exec(step["exec"], step_id)
        if "log" in step:
            msg = self._resolve_value(step["log"])
            self.context.log(f"[USER] {msg}")
            return {"step_id": step_id, "action": "log", "message": msg}
        if "send_alert" in step:
            cfg = step["send_alert"]
            channel = self._resolve_value(cfg.get("channel", "dingtalk"))
            message = self._resolve_value(cfg.get("message", ""))
            self.context.alerts.append({"channel": channel, "message": message})
            self.context.log(f"发送告警: [{channel}] {message}")
            return {"step_id": step_id, "action": "alert_sent", "channel": channel}
        if "set" in step:
            var_name = step["set"].get("name")
            var_val = step["set"].get("value")
            resolved = self._resolve_value(var_val)
            self.context.set(var_name, resolved)
            self.context.log(f"变量 {var_name} = {resolved}")
            return {"step_id": step_id, "action": "set", "name": var_name, "value": resolved}
        if "delay" in step:
            seconds = int(step["delay"].get("seconds", 1))
            time.sleep(seconds)
            return {"step_id": step_id, "action": "delayed", "seconds": seconds}
        return {"step_id": step_id, "action": "noop"}

    def _execute_if(self, if_block: dict, step_id: str) -> dict:
        condition = if_block.get("condition", "")
        then_steps = if_block.get("then", [])
        else_steps = if_block.get("else", [])
        evaluator = ConditionEvaluator(self.context)
        result = evaluator.evaluate(condition)
        self.context.log(f"条件 '{condition}' = {result}")
        branch_steps = then_steps if result else else_steps
        branch_name = "then" if result else "else"
        if not branch_steps:
            return {"step_id": step_id, "condition": condition, "result": result, "branch": branch_name}
        step_results = []
        stop = False
        for i, s in enumerate(branch_steps):
            sr = self._execute_step(s, step_index=f"{step_id}_{branch_name}_{i}")
            step_results.append(sr)
            if sr.get("stop"):
                stop = True
                break
        return {"step_id": step_id, "condition": condition, "result": result,
                "branch": branch_name, "branch_results": step_results, "stop": stop}

    def _execute_while(self, while_block: dict, do_steps: list, step_id: str) -> dict:
        condition = while_block.get("condition", "")
        max_iter = while_block.get("max_iterations", 10)
        iteration_results = []
        iteration = 0
        evaluator = ConditionEvaluator(self.context)
        while evaluator.evaluate(condition) and iteration < max_iter:
            self.context.log(f"While 循环第 {iteration + 1} 次: {condition}")
            for i, s in enumerate(do_steps):
                sr = self._execute_step(s, step_index=f"{step_id}_iter_{iteration}_{i}")
                iteration_results.append(sr)
                if sr.get("stop"):
                    return {"step_id": step_id, "iterations": iteration + 1,
                            "results": iteration_results, "stop": True}
            iteration += 1
        self.context.log(f"While 循环结束: {iteration} 次")
        return {"step_id": step_id, "iterations": iteration, "results": iteration_results}

    def _execute_for(self, for_block: dict, do_steps: list, step_id: str) -> dict:
        var_name = for_block.get("var")
        iterable = for_block.get("in")
        max_iter = for_block.get("max_iterations", 100)
        if isinstance(iterable, str):
            resolved = self.context.get(iterable)
            if resolved is None:
                resolved = []
        else:
            resolved = iterable or []
        if not isinstance(resolved, (list, dict, str)):
            resolved = []
        iteration_results = []
        iteration = 0
        for item in resolved:
            if iteration >= max_iter:
                break
            self.context.set(var_name, item)
            self.context.log(f"For {var_name} = {item}")
            for i, s in enumerate(do_steps):
                sr = self._execute_step(s, step_index=f"{step_id}_for_{iteration}_{i}")
                iteration_results.append(sr)
                if sr.get("stop"):
                    return {"step_id": step_id, "iterations": iteration + 1,
                            "results": iteration_results, "stop": True}
            iteration += 1
        return {"step_id": step_id, "iterations": iteration, "results": iteration_results}

    def _execute_exec(self, exec_block: dict, step_id: str) -> dict:
        tool_name = exec_block.get("tool")
        params = {k: self._resolve_value(v) for k, v in exec_block.get("params", {}).items()}
        result = exec_tool(tool_name, params, self.context)
        self.context.record(step_id, result)
        if exec_block.get("save_as"):
            self.context.set(exec_block["save_as"], result)
        return {
            "step_id": step_id,
            "tool": tool_name,
            "result": result,
            "stop": exec_block.get("stop", False),
        }

    def _resolve_value(self, value):
        if isinstance(value, str):
            if "{" in value and "}" in value:
                try:
                    return value.format_map(self.context.variables)
                except Exception:
                    pass
            evaluator = ConditionEvaluator(self.context)
            val = evaluator._resolve_value(value)
            return val if val is not None else value
        elif isinstance(value, dict):
            return {k: self._resolve_value(v) for k, v in value.items()}
        elif isinstance(value, list):
            return [self._resolve_value(v) for v in value]
        return value

    def _build_result(self, status: str, error: str = None) -> dict:
        return {
            "workflow_id": self.workflow.get("id", "unknown"),
            "status": status,
            "error": error,
            "context_variables": dict(self.context.variables),
            "step_results": self.results,
            "logs": self.context.logs,
            "alerts": self.context.alerts,
            "summary": f"执行 {len(self.results)} 个步骤，{sum(1 for r in self.results if r.get('result') and 'error' not in r.get('result', {}))} 个成功",
        }


# ─────────────────────────────────────────
# 预定义工作流模板
# ─────────────────────────────────────────

WORKFLOW_TEMPLATES = {
    "content_creation": {
        "id": "content_creation",
        "name": "内容创作流程",
        "description": "选题 → 创作 → 合规审核 → 发布",
        "variables": {},
        "steps": [
            {"id": "topic", "name": "获取选题", "exec": {"tool": "ask", "params": {"question": "待创作选题", "module": "content"}}},
            {"id": "create", "name": "生成内容", "exec": {"tool": "content", "params": {"action": "create"}}},
            {"id": "compliance_check", "name": "合规审核", "exec": {"tool": "compliance", "params": {"action": "review"}}},
            {"id": "publish", "name": "发布", "exec": {"tool": "ask", "params": {"question": "发布内容"}}},
        ],
        "on_error": "rollback",
    },
    "patient_onboarding": {
        "id": "patient_onboarding",
        "name": "患者入职流程",
        "description": "新建会话 → 风险评估 → 生成随访计划",
        "variables": {},
        "steps": [
            {"id": "create_session", "name": "创建会话", "exec": {"tool": "patient", "params": {"action": "list_segments"}}},
            {"id": "assess_risk", "name": "风险评估", "exec": {"tool": "patient_segmentation", "params": {"action": "segment"}}},
            {"id": "create_sop", "name": "生成随访SOP", "exec": {"tool": "patient", "params": {"action": "create_sop"}}},
        ],
        "on_error": "notify",
    },
    "kol_campaign": {
        "id": "kol_campaign",
        "name": "KOL营销流程",
        "description": "匹配KOL → 评估效果 → 生成归因报告",
        "variables": {},
        "steps": [
            {"id": "match_kol", "name": "匹配KOL", "exec": {"tool": "kol_matching", "params": {"action": "match"}}},
            {"id": "analyze", "name": "效果分析", "exec": {"tool": "attribution", "params": {"action": "channel_summary"}}},
            {"id": "report", "name": "生成报告", "exec": {"tool": "ask", "params": {"question": "KOL营销归因报告"}}},
        ],
        "on_error": "continue",
    },
    "compliance_audit": {
        "id": "compliance_audit",
        "name": "合规审计流程",
        "description": "获取内容 → 全面审核 → 导出报告",
        "variables": {},
        "steps": [
            {"id": "get_content", "name": "获取待审内容", "exec": {"tool": "ask", "params": {"question": "内容运营状况", "module": "content"}}},
            {"id": "review", "name": "合规审核", "exec": {"tool": "compliance", "params": {"action": "review"}}},
            {"id": "export", "name": "导出报告", "exec": {"tool": "compliance", "params": {"action": "export_report"}}},
        ],
        "on_error": "stop",
    },
    "low_stock_alert": {
        "id": "low_stock_alert",
        "name": "库存不足自动补货",
        "description": "当库存低于 reorder_point 时，自动创建采购订单",
        "variables": {"min_stock_ratio": 1.0, "urgency": "normal"},
        "steps": [
            {"id": "check_inventory", "exec": {"tool": "supply_chain_state", "params": {"action": "inventory_states"}, "save_as": "inv_result"}},
            {"id": "process_alerts", "for": {"var": "alert_item", "in": "inv_result.alerts"},
             "do": [
                 {"log": "检测到库存告警: {alert_item.product_name}"},
                 {"if": {"condition": "alert_item.state == 'out_of_stock'",
                         "then": [
                             {"id": "create_urgent_order", "exec": {"tool": "supply_chain_state", "params": {"action": "create_order", "product_id": "{alert_item.product_id}", "quantity": 200, "priority": "urgent", "notes": "自动补货-缺货告警"}, "save_as": "order_result"}},
                             {"log": "已创建紧急采购订单: {order_result.order_id}"}
                         ],
                         "else": [
                             {"log": "库存 {alert_item.product_name} 偏低，建议关注"}
                         ]}}
             ]}
        ]
    },
    "content_compliance_flow": {
        "id": "content_compliance_flow",
        "name": "内容合规审核流程",
        "description": "提交内容 → AI预审 → 人工审核 → 发布/打回",
        "variables": {},
        "steps": [
            {"id": "auto_review", "exec": {"tool": "compliance_audit", "params": {"action": "create", "content_text": "{content_text}", "title": "{content_title}", "submitter": "{submitter}"}, "save_as": "audit_result"}},
            {"id": "decide",
             "if": {"condition": "audit_result.is_compliant == true",
                    "then": [
                        {"log": "内容合规初审通过，得分: {audit_result.score}"},
                        {"exec": {"tool": "compliance_audit", "params": {"action": "transition", "audit_id": "{audit_result.audit_id}", "to_state": "approved", "actor": "{submitter}", "reason": "AI初审通过"}}}
                    ],
                    "else": [
                        {"log": "内容不合规，得分: {audit_result.score}，触及规则: {audit_result.hit_rules}"},
                        {"send_alert": {"channel": "dingtalk", "message": "内容合规告警: {audit_result.hit_rules}"}}
                    ]}}
        ]
    },
    "goal_check_and_alert": {
        "id": "goal_check_and_alert",
        "name": "目标达成检查与告警",
        "description": "每周检查目标进度，未达标则告警",
        "variables": {"target_roas": 1.5},
        "steps": [
            {"id": "get_channel_summary", "exec": {"tool": "attribution", "params": {"action": "channel_summary", "period_days": 7}, "save_as": "channel_data"}},
            {"id": "analyze_roas", "for": {"var": "channel", "in": "channel_data.channel_summary"},
             "do": [
                 {"if": {"condition": "channel.roas < target_roas",
                         "then": [
                             {"log": "⚠️ {channel.channel} 渠道 ROAS {channel.roas} 未达标（目标 {target_roas}）"},
                             {"send_alert": {"channel": "dingtalk", "message": "渠道 {channel.channel} ROAS {channel.roas} 未达目标 {target_roas}"}}
                         ]}}
             ]}
        ]
    },
}


# ─────────────────────────────────────────
# 工作流执行（声明式）
# ─────────────────────────────────────────

def execute_workflow(workflow_name: str, context: dict = None) -> dict:
    workflow = WORKFLOW_TEMPLATES.get(workflow_name)
    if not workflow:
        return {"error": f"Workflow '{workflow_name}' not found",
                "available": list(WORKFLOW_TEMPLATES.keys())}

    engine = ConditionalEngine(workflow)
    return engine.run(context or {})


def list_workflows() -> dict:
    return {
        "workflows": [
            {"name": k, "description": v.get("description", ""),
             "steps_count": len(v.get("steps", [])),
             "on_error": v.get("on_error", "stop")}
            for k, v in WORKFLOW_TEMPLATES.items()
        ]
    }


def validate_workflow(workflow: dict) -> dict:
    errors = []
    for i, step in enumerate(workflow.get("steps", [])):
        if not any(k in step for k in ("if", "while", "for", "exec", "log", "send_alert", "set", "delay")):
            errors.append(f"Step {i}: 缺少有效动作字段")
    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "step_count": len(workflow.get("steps", [])),
    }


def _save_execution(execution_id: str, workflow_name: str, status: str,
                    step_results: list, context: dict, conn):
    now = datetime.now().isoformat()
    try:
        if is_sqlite:
            conn.execute("""
                INSERT OR REPLACE INTO workflow_executions
                (id, name, status, steps_json, context_json, started_at, completed_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (execution_id, workflow_name, status,
                  json.dumps(step_results, ensure_ascii=False),
                  json.dumps(context, ensure_ascii=False),
                  time.time(),
                  time.time() if status in ("completed", "error") else 0))
        else:
            conn.execute("""
                INSERT INTO workflow_executions
                (id, name, status, steps_json, context_json, started_at, completed_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE status=VALUES(status),
                  steps_json=VALUES(steps_json), context_json=VALUES(context_json),
                  completed_at=VALUES(completed_at)
            """, (execution_id, workflow_name, status,
                  json.dumps(step_results, ensure_ascii=False),
                  json.dumps(context, ensure_ascii=False),
                  time.time(),
                  time.time() if status in ("completed", "error") else 0))
        conn.commit()
    except Exception:
        pass


def get_execution_status(execution_id: str) -> dict:
    conn, is_sqlite = _get_conn()
    try:
        if is_sqlite:
            row = conn.execute("SELECT * FROM workflow_executions WHERE id = ?",
                              (execution_id,)).fetchone()
        else:
            row = conn.execute("SELECT * FROM workflow_executions WHERE id = %s",
                              (execution_id,)).fetchone()
        if not row:
            return {"error": f"Execution {execution_id} not found"}
        cols = [d[0] for d in conn.execute("SELECT * FROM workflow_executions LIMIT 0").description]
        data = dict(zip(cols, row))
        return {
            "execution_id": data.get("id"),
            "workflow_name": data.get("name"),
            "status": data.get("status"),
            "steps": json.loads(data.get("steps_json", "[]")),
            "context": json.loads(data.get("context_json", "{}")),
            "started_at": data.get("started_at"),
            "completed_at": data.get("completed_at"),
        }
    finally:
        close_conn(conn)


# ─────────────────────────────────────────
# 主入口
# ─────────────────────────────────────────

def _parse_args():
    if len(sys.argv) > 1:
        try:
            return json.loads(sys.argv[1])
        except json.JSONDecodeError:
            return {}
    if not sys.stdin.isatty():
        data = sys.stdin.read().strip()
        if data:
            try:
                return json.loads(data)
            except json.JSONDecodeError:
                return {}
    return {}


if __name__ == "__main__":
    args = _parse_args()
    action = args.get("action", "list")

    if action == "run":
        wf = args.get("workflow")
        if isinstance(wf, str):
            wf = WORKFLOW_TEMPLATES.get(wf)
            if not wf:
                print(json.dumps({"error": f"Unknown workflow template: {wf}"}))
                sys.exit(1)
        engine = ConditionalEngine(wf)
        result = engine.run(args.get("context", {}))

    elif action == "status":
        result = get_execution_status(args.get("execution_id", ""))

    elif action == "list":
        result = list_workflows()

    elif action == "templates":
        result = {
            "templates": {
                k: {"id": v["id"], "name": v["name"], "description": v["description"]}
                for k, v in WORKFLOW_TEMPLATES.items()
            }
        }

    elif action == "validate":
        wf = args.get("workflow", {})
        result = validate_workflow(wf)

    else:
        result = {"error": f"Unknown action: {action}"}

    print(json.dumps(result, ensure_ascii=False, indent=2))
