#!/usr/bin/env python3
"""
workflow-orchestrator.py — 多代理工作流编排器

扩展 review-orchestrator.py，支持完整的开发生命周期编排：
  1. 任务分类（frontend/backend/fullstack）
  2. 规划阶段（只读，不修改代码）
  3. 执行阶段（按计划修改代码）
  4. 审查阶段（多代理并行审查）
  5. 优化阶段（根据审查结果修复）

核心设计原则：
  - 规划与执行分离：避免"边想边做"的质量问题
  - 前后端路由：自动识别任务类型，选择对应的专属代理
  - 与现有审查体系兼容：审查阶段复用 review-orchestrator.py

用法：
  python workflow-orchestrator.py classify --description "实现用户登录页面"
  python workflow-orchestrator.py plan --task "frontend" --files "src/pages/Login.tsx"
  python workflow-orchestrator.py execute --plan "plans/login-feature.json"
  python workflow-orchestrator.py review --files "src/pages/Login.tsx" --auto-select
  python workflow-orchestrator.py pipeline --description "实现用户登录功能" --files "src/"
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


# ─── 常量 ───────────────────────────────────────────────────────────────────

PLANS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "plans")

# 任务分类路由
TASK_ROUTING = {
    "frontend": {
        "patterns": [
            r"component", r"layout", r"style", r"animation", r"UI", r"页面", r"组件", r"样式",
            r"React", r"Vue", r"CSS", r"SCSS", r"Tailwind", r"前端", r"界面", r"交互",
            r"responsive", r"响应式", r"mobile", r"移动端", r"desktop", r"桌面端",
        ],
        "lead_agent": "typescript-reviewer",
        "support_agent": "code-reviewer",
        "file_extensions": [".tsx", ".jsx", ".vue", ".css", ".scss", ".less"],
    },
    "backend": {
        "patterns": [
            r"API", r"database", r"algorithm", r"auth", r"接口", r"数据库", r"算法",
            r"server", r"服务端", r"backend", r"后端", r"model", r"schema", r"migration",
            r"query", r"SQL", r"Redis", r"cache", r"消息队列", r"MQ",
        ],
        "lead_agent": "python-reviewer",
        "support_agent": "security-auditor",
        "file_extensions": [".py", ".go", ".java", ".rs"],
    },
    "fullstack": {
        "patterns": [],  # 默认
        "lead_agent": "code-reviewer",
        "support_agents": ["typescript-reviewer", "python-reviewer"],
        "file_extensions": [],
    },
}


# ─── 工具函数 ────────────────────────────────────────────────────────────────

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_plans_dir():
    """确保 plans 目录存在。"""
    os.makedirs(PLANS_DIR, exist_ok=True)


def classify_task(description: str, files: list = None) -> dict:
    """分类任务类型：frontend/backend/fullstack。"""
    scores = {"frontend": 0, "backend": 0, "fullstack": 0}
    
    # 基于描述关键词
    for task_type, config in TASK_ROUTING.items():
        if task_type == "fullstack":
            continue
        for pattern in config["patterns"]:
            if re.search(pattern, description, re.IGNORECASE):
                scores[task_type] += 2
    
    # 基于文件扩展名
    if files:
        for f in files:
            ext = Path(f).suffix.lower()
            for task_type, config in TASK_ROUTING.items():
                if ext in config.get("file_extensions", []):
                    scores[task_type] += 1
    
    # 确定最高分
    max_score = max(scores.values())
    if max_score == 0:
        return {"type": "fullstack", "confidence": 0.5, "reason": "未匹配到明确特征，使用默认"}
    
    best_type = max(scores, key=scores.get)
    confidence = min(1.0, max_score / 10)  # 归一化
    
    return {
        "type": best_type,
        "confidence": confidence,
        "scores": scores,
        "reason": f"基于关键词和文件特征分类为 {best_type}",
    }


def get_routing_config(task_type: str) -> dict:
    """获取任务类型的路由配置。"""
    return TASK_ROUTING.get(task_type, TASK_ROUTING["fullstack"])


# ─── 子命令实现 ──────────────────────────────────────────────────────────────

def cmd_classify(args: argparse.Namespace) -> None:
    """分类任务类型。"""
    files = args.files.split(",") if args.files else []
    result = classify_task(args.description, files)
    
    print(json.dumps({
        "success": True,
        "action": "classify",
        "description": args.description,
        "classification": result,
        "routing_config": get_routing_config(result["type"]),
    }, ensure_ascii=False, indent=2))


def cmd_plan(args: argparse.Namespace) -> None:
    """生成实现计划（只读阶段）。"""
    ensure_plans_dir()
    
    # 分类任务
    files = args.files.split(",") if args.files else []
    classification = classify_task(args.description, files)
    task_type = classification["type"]
    routing = get_routing_config(task_type)
    
    # 生成计划
    plan = {
        "id": f"plan-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
        "description": args.description,
        "task_type": task_type,
        "classification": classification,
        "routing": routing,
        "files": files,
        "stages": [
            {
                "name": "context",
                "description": "上下文检索",
                "actions": [
                    "读取相关文件",
                    "分析依赖关系",
                    "识别影响范围",
                ],
            },
            {
                "name": "design",
                "description": "设计方案",
                "actions": [
                    "定义接口/组件结构",
                    "确定数据流",
                    "设计错误处理策略",
                ],
            },
            {
                "name": "implementation",
                "description": "实现计划",
                "actions": [
                    "列出需要创建/修改的文件",
                    "每个文件的修改内容",
                    "依赖注入点",
                ],
            },
            {
                "name": "testing",
                "description": "测试计划",
                "actions": [
                    "单元测试用例",
                    "集成测试用例",
                    "边界条件测试",
                ],
            },
        ],
        "agents": {
            "lead": routing["lead_agent"],
            "support": routing.get("support_agent") or routing.get("support_agents", []),
        },
        "created_at": now_iso(),
        "status": "draft",
    }
    
    # 保存计划
    plan_path = os.path.join(PLANS_DIR, f"{plan['id']}.json")
    with open(plan_path, "w", encoding="utf-8") as f:
        json.dump(plan, f, ensure_ascii=False, indent=2)
    
    print(json.dumps({
        "success": True,
        "action": "plan",
        "plan_id": plan["id"],
        "plan_path": plan_path,
        "task_type": task_type,
        "stages": [s["name"] for s in plan["stages"]],
        "agents": plan["agents"],
        "message": f"已生成计划: {plan['id']} (类型: {task_type})",
    }, ensure_ascii=False, indent=2))


def cmd_execute(args: argparse.Namespace) -> None:
    """执行计划（输出执行指令）。"""
    plan_path = args.plan
    
    if not os.path.exists(plan_path):
        # 尝试从 plans 目录查找
        plan_path = os.path.join(PLANS_DIR, f"{args.plan}.json")
        if not os.path.exists(plan_path):
            print(json.dumps({
                "success": False,
                "message": f"计划不存在: {args.plan}"
            }, ensure_ascii=False))
            return
    
    with open(plan_path, "r", encoding="utf-8") as f:
        plan = json.load(f)
    
    # 更新状态
    plan["status"] = "executing"
    plan["executed_at"] = now_iso()
    
    # 保存更新
    with open(plan_path, "w", encoding="utf-8") as f:
        json.dump(plan, f, ensure_ascii=False, indent=2)
    
    # 输出执行指令
    print(json.dumps({
        "success": True,
        "action": "execute",
        "plan_id": plan["id"],
        "task_type": plan["task_type"],
        "stages": plan["stages"],
        "instructions": {
            "step_1": "读取相关文件，理解现有代码结构",
            "step_2": "按照设计阶段创建/修改文件",
            "step_3": "实现功能代码",
            "step_4": "添加测试用例",
            "step_5": "运行测试验证",
        },
        "message": f"开始执行计划: {plan['id']}",
    }, ensure_ascii=False, indent=2))


def cmd_review(args: argparse.Namespace) -> None:
    """审查代码（复用 review-orchestrator.py 的逻辑）。"""
    # 导入 review-orchestrator
    scripts_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, scripts_dir)
    
    from importlib import import_module
    review_module = import_module("review-orchestrator")
    
    # 构建参数
    files = args.files.split(",") if args.files else []
    
    # 调用 auto_select_agents
    agents = review_module.auto_select_agents(files, args.focus or "")
    
    print(json.dumps({
        "success": True,
        "action": "review",
        "files": files,
        "selected_agents": agents,
        "instruction": "使用 sessions_spawn 并行启动以上代理执行审查",
        "message": f"已选择 {len(agents)} 个审查代理",
    }, ensure_ascii=False, indent=2))


def cmd_pipeline(args: argparse.Namespace) -> None:
    """完整流水线：分类 → 规划 → 执行 → 审查 → 优化。"""
    ensure_plans_dir()
    
    files = args.files.split(",") if args.files else []
    
    # Step 1: 分类
    classification = classify_task(args.description, files)
    task_type = classification["type"]
    routing = get_routing_config(task_type)
    
    # Step 2: 生成计划
    plan = {
        "id": f"pipeline-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
        "description": args.description,
        "task_type": task_type,
        "classification": classification,
        "routing": routing,
        "files": files,
        "pipeline": {
            "stages": [
                {"name": "classify", "status": "completed", "result": classification},
                {"name": "plan", "status": "pending"},
                {"name": "execute", "status": "pending"},
                {"name": "review", "status": "pending"},
                {"name": "optimize", "status": "pending"},
            ],
            "agents": {
                "lead": routing["lead_agent"],
                "support": routing.get("support_agent") or routing.get("support_agents", []),
            },
        },
        "created_at": now_iso(),
        "status": "planning",
    }
    
    # 保存计划
    plan_path = os.path.join(PLANS_DIR, f"{plan['id']}.json")
    with open(plan_path, "w", encoding="utf-8") as f:
        json.dump(plan, f, ensure_ascii=False, indent=2)
    
    print(json.dumps({
        "success": True,
        "action": "pipeline",
        "pipeline_id": plan["id"],
        "plan_path": plan_path,
        "task_type": task_type,
        "classification": classification,
        "agents": plan["pipeline"]["agents"],
        "stages": [
            {"name": "classify", "status": "completed", "instruction": "任务已分类"},
            {"name": "plan", "status": "pending", "instruction": "生成实现计划（只读）"},
            {"name": "execute", "status": "pending", "instruction": "按计划修改代码"},
            {"name": "review", "status": "pending", "instruction": "多代理并行审查"},
            {"name": "optimize", "status": "pending", "instruction": "根据审查结果修复"},
        ],
        "message": f"流水线已启动: {plan['id']} (类型: {task_type})",
    }, ensure_ascii=False, indent=2))


# ─── 参数解析 ────────────────────────────────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="多代理工作流编排器 — 支持完整的开发生命周期编排",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", help="子命令")
    
    # classify
    p_classify = subparsers.add_parser("classify", help="分类任务类型")
    p_classify.add_argument("--description", required=True, help="任务描述")
    p_classify.add_argument("--files", help="相关文件（逗号分隔）")
    
    # plan
    p_plan = subparsers.add_parser("plan", help="生成实现计划（只读阶段）")
    p_plan.add_argument("--description", required=True, help="任务描述")
    p_plan.add_argument("--task", help="任务类型（frontend/backend/fullstack）")
    p_plan.add_argument("--files", help="相关文件（逗号分隔）")
    
    # execute
    p_execute = subparsers.add_parser("execute", help="执行计划")
    p_execute.add_argument("--plan", required=True, help="计划 ID 或路径")
    
    # review
    p_review = subparsers.add_parser("review", help="审查代码")
    p_review.add_argument("--files", required=True, help="要审查的文件（逗号分隔）")
    p_review.add_argument("--auto-select", action="store_true", help="自动选择代理")
    p_review.add_argument("--focus", help="特殊关注点")
    
    # pipeline
    p_pipeline = subparsers.add_parser("pipeline", help="完整流水线")
    p_pipeline.add_argument("--description", required=True, help="任务描述")
    p_pipeline.add_argument("--files", help="相关文件（逗号分隔）")
    
    return parser


# ─── 主入口 ──────────────────────────────────────────────────────────────────

def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    commands = {
        "classify": cmd_classify,
        "plan": cmd_plan,
        "execute": cmd_execute,
        "review": cmd_review,
        "pipeline": cmd_pipeline,
    }
    
    handler = commands.get(args.command)
    if handler:
        handler(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
