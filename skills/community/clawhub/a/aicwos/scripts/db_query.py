#!/usr/bin/env python3
"""
通用查询与写入CLI

用法:
  # 讲师
  python scripts/db_query.py --type lecturer --action list
  python scripts/db_query.py --type lecturer --action get --id 讲师A
  python scripts/db_query.py --type lecturer --action lite --id 讲师A
  python scripts/db_query.py --type lecturer --action save --id 讲师A --query '<profile JSON>'
  python scripts/db_query.py --type lecturer --action delete --id 讲师A
  python scripts/db_query.py --type lecturer --action compare --id 讲师A --id2 讲师B
  python scripts/db_query.py --type lecturer --action references --id 讲师A
  python scripts/db_query.py --type lecturer --action samples --id 讲师A

  # 知识库
  python scripts/db_query.py --type knowledge --action list
  python scripts/db_query.py --type knowledge --action search --query "养生"
  python scripts/db_query.py --type knowledge --action search --query "养生" --category 产品目录
  python scripts/db_query.py --type knowledge --action get --id "产品目录/产品A/产品背书.txt"
  python scripts/db_query.py --type knowledge --action delete --id "产品目录/产品A/产品背书.txt"
  python scripts/db_query.py --type knowledge --action context --query "产品A产品特点" --max-tokens 1000

  # 系列文案
  python scripts/db_query.py --type series --action list
  python scripts/db_query.py --type series --action save_plan --id 夏季养生 --lecturer 讲师A --query '<plan JSON>'
  python scripts/db_query.py --type series --action get_plan --id 夏季养生
  python scripts/db_query.py --type series --action save_episode --id 夏季养生 --id2 1 --query '<episode JSON>'
  python scripts/db_query.py --type series --action summaries --id 夏季养生
  python scripts/db_query.py --type series --action progress --id 夏季养生
  python scripts/db_query.py --type series --action content --id 夏季养生 --id2 1

  # 文案生成上下文
  python scripts/db_query.py --type context --lecturer 讲师A --query "养生保健"

  # 行为规则
  python scripts/db_query.py --type behavior --action list
  python scripts/db_query.py --type behavior --action add --id R006 --query '<rule JSON>'
  python scripts/db_query.py --type behavior --action remove --id R006
  python scripts/db_query.py --type behavior --action update --id R006 --query '<rule JSON>'

  # 文件系统浏览
  python scripts/db_query.py --type fs --action tree --data-dir <目录>
  python scripts/db_query.py --type fs --action knowledge --data-dir <目录>
  python scripts/db_query.py --type fs --action lecturers --data-dir <目录>
"""

import argparse
import json
import sys
from pathlib import Path

SKILL_ROOT = str(Path(__file__).resolve().parent.parent)
if SKILL_ROOT not in sys.path:
    sys.path.insert(0, SKILL_ROOT)

from scripts.core.db_manager import DatabaseManager, resolve_db_path
from scripts.core.lecturer_service import LecturerService
from scripts.core.knowledge_service import KnowledgeService
from scripts.core.copywriting_service import CopywritingService


def _build_tree(root: Path, base_name: str = None) -> dict:
    """递归构建目录树，返回结构化JSON"""
    if not root.exists():
        return {"exists": False, "path": str(root)}

    name = base_name or root.name
    result = {"name": name, "type": "dir", "children": []}

    # 排序：目录在前，文件在后，各自按名称排序
    items = sorted(root.iterdir(), key=lambda p: (p.is_file(), p.name))

    for item in items:
        if item.name.startswith(".") or item.name == "__pycache__":
            continue
        if item.is_dir():
            result["children"].append(_build_tree(item))
        else:
            size = item.stat().st_size
            if size >= 1024 * 1024:
                size_str = f"{size / 1024 / 1024:.1f}MB"
            elif size >= 1024:
                size_str = f"{size / 1024:.1f}KB"
            else:
                size_str = f"{size}B"
            result["children"].append({
                "name": item.name,
                "type": "file",
                "size": size_str,
            })

    return result


def _parse_json_query(query_str: str, param_name: str = "--query") -> dict:
    """解析 --query 参数为 JSON dict，失败则抛出 ValueError"""
    try:
        data = json.loads(query_str)
        if not isinstance(data, dict):
            raise ValueError(f"{param_name} 必须是JSON对象")
        return data
    except json.JSONDecodeError as e:
        raise ValueError(f"{param_name} 不是有效JSON: {e}")


def main():
    parser = argparse.ArgumentParser(description="Aicwos 数据查询与写入")
    parser.add_argument("--type", required=True,
                        choices=["lecturer", "knowledge", "series", "context", "behavior", "fs"],
                        help="操作类型")
    parser.add_argument("--action", required=True,
                        help="操作动作")
    parser.add_argument("--id", default=None, help="主ID（讲师ID/文档ID/系列ID）")
    parser.add_argument("--id2", default=None, help="辅助ID（对比用第二ID/集号）")
    parser.add_argument("--query", default=None,
                        help="搜索词或JSON数据（save/add/update时传JSON）")
    parser.add_argument("--query-file", default=None,
                        help="从文件读取JSON数据（--query的文件替代，适用于大型JSON）")
    parser.add_argument("--category", default=None, help="知识分类过滤")
    parser.add_argument("--product", default=None, help="产品过滤")
    parser.add_argument("--top-k", type=int, default=5, help="返回条数")
    parser.add_argument("--max-tokens", type=int, default=1000, help="上下文token预算")
    parser.add_argument("--lecturer", default=None, help="讲师ID")
    parser.add_argument("--series-id", default=None, help="系列ID（context类型可选）")
    parser.add_argument("--data-dir", required=True, help="控制台目录路径")
    args = parser.parse_args()

    # --query-file 优先于 --query（读取文件内容替换 --query）
    staging_file = None
    if args.query_file:
        qf = Path(args.query_file)
        if not qf.exists():
            print(json.dumps({"status": "error", "message": f"--query-file 文件不存在: {args.query_file}"}, ensure_ascii=False))
            return
        try:
            args.query = qf.read_text(encoding="utf-8").strip()
        except Exception as e:
            print(json.dumps({"status": "error", "message": f"--query-file 读取失败: {e}"}, ensure_ascii=False))
            return
        # 标记 staging 文件（以 _staging.json 结尾），操作完成后自动清理
        if qf.name.endswith("_staging.json"):
            staging_file = qf

    try:
        resolved_db = resolve_db_path(None, args.data_dir)
    except ValueError as e:
        print(json.dumps({"status": "error", "message": str(e)}, ensure_ascii=False))
        return

    db = DatabaseManager(resolved_db)
    data_dir = args.data_dir
    result = None

    try:
        # ── 讲师 ─────────────────────────────────────────────
        if args.type == "lecturer":
            svc = LecturerService(db, data_dir=data_dir)
            if args.action == "list":
                result = svc.list_lecturers()
            elif args.action == "get":
                result = svc.get_profile(args.id)
            elif args.action == "lite":
                result = svc.get_lite(args.id)
            elif args.action == "save":
                # 保存/更新讲师画像（INSERT OR REPLACE）
                if not args.id:
                    result = {"status": "error", "message": "需要 --id 指定讲师ID"}
                elif not args.query:
                    result = {"status": "error", "message": "需要 --query 传入画像JSON"}
                else:
                    try:
                        profile = _parse_json_query(args.query)
                        result = svc.add_lecturer(args.id, profile)
                    except ValueError as e:
                        result = {"status": "error", "message": str(e)}
            elif args.action == "delete":
                if not args.id:
                    result = {"status": "error", "message": "需要 --id 指定讲师ID"}
                else:
                    result = svc.delete_lecturer(args.id)
            elif args.action == "compare":
                result = svc.compare(args.id, args.id2)
            elif args.action == "references":
                result = svc.get_reference_samples(args.id)
            elif args.action == "samples":
                if not args.id:
                    result = {"status": "error", "message": "需要 --id 指定讲师ID"}
                else:
                    result = svc.get_samples(args.id)
            elif args.action == "quantitative":
                result = svc.get_quantitative(args.id)
            elif args.action == "add_sample":
                if not args.id:
                    result = {"status": "error", "message": "需要 --id 指定讲师ID"}
                elif not args.query:
                    result = {"status": "error", "message": "需要 --query 传入样本JSON: {\"sample_name\":\"...\",\"content\":\"...\"}"}
                else:
                    try:
                        q = _parse_json_query(args.query)
                        result = svc.add_sample(args.id, q["sample_name"], q["content"])
                    except (ValueError, KeyError) as e:
                        result = {"status": "error", "message": str(e)}
            else:
                result = {"error": f"未知action: {args.action}，可用: list/get/lite/save/delete/compare/references/samples/quantitative/add_sample"}

        # ── 知识库 ─────────────────────────────────────────────
        elif args.type == "knowledge":
            svc = KnowledgeService(db, data_dir=data_dir)
            if args.action == "list":
                result = svc.list_categories()
            elif args.action == "search":
                result = svc.search(args.query, top_k=args.top_k,
                                     category=args.category)
            elif args.action == "get":
                result = svc.get_doc(args.id)
            elif args.action == "delete":
                if not args.id:
                    result = {"status": "error", "message": "需要 --id 指定文档ID（如 '产品目录/产品A/产品背书.txt'）"}
                else:
                    result = svc.delete_doc(args.id)
            elif args.action == "context":
                result = svc.get_relevant_context(args.query,
                                                    max_tokens=args.max_tokens)
            elif args.action == "docs":
                result = svc.list_docs_by_category(args.category)
            else:
                result = {"error": f"未知action: {args.action}，可用: list/search/get/delete/context/docs"}

        # ── 系列文案 ─────────────────────────────────────────────
        elif args.type == "series":
            svc = CopywritingService(db, data_dir=data_dir)
            if args.action == "list":
                result = svc.list_series(args.lecturer)
            elif args.action == "save_plan":
                # 保存系列计划
                if not args.id:
                    result = {"status": "error", "message": "需要 --id 指定系列ID"}
                elif not args.lecturer:
                    result = {"status": "error", "message": "需要 --lecturer 指定讲师ID"}
                elif not args.query:
                    result = {"status": "error", "message": "需要 --query 传入计划JSON，格式: {\"title\":\"系列标题\",\"episodes\":[{\"num\":1,\"title\":\"第1集标题\",\"topic\":\"主题\"}]}"}
                else:
                    try:
                        plan = _parse_json_query(args.query)
                        title = plan.get("title", args.id)
                        result = svc.create_series_plan(
                            series_id=args.id,
                            lecturer_id=args.lecturer,
                            title=title,
                            plan=plan,
                        )
                    except ValueError as e:
                        result = {"status": "error", "message": str(e)}
            elif args.action == "get_plan":
                if not args.id:
                    result = {"status": "error", "message": "需要 --id 指定系列ID"}
                else:
                    result = svc.get_series_plan(args.id)
            elif args.action == "save_episode":
                # 保存一集文案（DB存元数据 + .txt文件存正文）
                if not args.id:
                    result = {"status": "error", "message": "需要 --id 指定系列ID"}
                elif not args.id2:
                    result = {"status": "error", "message": "需要 --id2 指定集号（如 1、2、3）"}
                elif not args.query:
                    result = {"status": "error", "message": "需要 --query 传入文案JSON，格式: {\"title\":\"标题\",\"content\":\"正文\",\"summary\":\"摘要\",\"hook_next\":\"下集衔接\"}"}
                else:
                    try:
                        ep_data = _parse_json_query(args.query)
                        episode_num = int(args.id2)
                        title = ep_data.get("title", f"第{episode_num}集")
                        content = ep_data.get("content", "")
                        summary = ep_data.get("summary", "")
                        hook_next = ep_data.get("hook_next", "")
                        result = svc.save_episode(
                            series_id=args.id,
                            episode_num=episode_num,
                            title=title,
                            content=content,
                            summary=summary,
                            hook_next=hook_next,
                        )
                    except ValueError as e:
                        result = {"status": "error", "message": str(e)}
            elif args.action == "summaries":
                result = svc.get_episode_summaries(args.id)
            elif args.action == "progress":
                result = svc.get_series_progress(args.id)
            elif args.action == "content":
                ep_num = int(args.id2) if args.id2 else 1
                result = {"content": svc.get_episode_content(args.id, ep_num)}
            elif args.action == "delete_episode":
                if not args.id:
                    result = {"status": "error", "message": "需要 --id 指定系列ID"}
                elif not args.id2:
                    result = {"status": "error", "message": "需要 --id2 指定集号"}
                else:
                    result = svc.delete_episode(args.id, int(args.id2))
            else:
                result = {"error": f"未知action: {args.action}，可用: list/save_plan/get_plan/save_episode/delete_episode/summaries/progress/content"}

        # ── 文案生成上下文 ─────────────────────────────────────────────
        elif args.type == "context":
            svc = CopywritingService(db, data_dir=data_dir)
            result = svc.get_generation_context(
                lecturer_id=args.lecturer,
                topic=args.query or "",
                knowledge_query=args.query,
                series_id=args.series_id,
                max_knowledge_tokens=args.max_tokens,
            )

        # ── 行为规则 ─────────────────────────────────────────────
        elif args.type == "behavior":
            svc = CopywritingService(db, data_dir=data_dir)
            if args.action == "list":
                result = svc.load_behavior_rules()
            elif args.action in ("add", "remove", "update"):
                if not args.id:
                    result = {"error": "需要 --id 指定规则ID"}
                else:
                    rules = svc.load_behavior_rules()
                    # --id 前缀判断类型: R=allowed, B=forbidden
                    rules_type = "allowed" if args.id.startswith("R") else "forbidden"
                    rule_list = rules[rules_type]
                    if args.action == "add":
                        # --query 作为新规则的JSON
                        if not args.query:
                            result = {"error": "add需要 --query 传入规则JSON"}
                        else:
                            try:
                                new_rule = json.loads(args.query)
                                if "id" not in new_rule:
                                    new_rule["id"] = args.id
                                rule_list.append(new_rule)
                                result = svc.save_behavior_rules(rules_type, rule_list)
                            except json.JSONDecodeError:
                                result = {"error": "--query 不是有效JSON"}
                    elif args.action == "remove":
                        rule_list = [r for r in rule_list if r.get("id") != args.id]
                        result = svc.save_behavior_rules(rules_type, rule_list)
                    elif args.action == "update":
                        if not args.query:
                            result = {"error": "update需要 --query 传入更新后的规则JSON"}
                        else:
                            try:
                                updated = json.loads(args.query)
                                found = False
                                for i, r in enumerate(rule_list):
                                    if r.get("id") == args.id:
                                        rule_list[i] = updated
                                        found = True
                                        break
                                if found:
                                    result = svc.save_behavior_rules(rules_type, rule_list)
                                else:
                                    result = {"error": f"规则 {args.id} 不存在"}
                            except json.JSONDecodeError:
                                result = {"error": "--query 不是有效JSON"}
            else:
                result = {"error": f"未知action: {args.action}，可用: list/add/remove/update"}

        # ── 文件系统浏览 ─────────────────────────────────────────────
        elif args.type == "fs":
            data_path = Path(data_dir)
            if args.action == "tree":
                result = _build_tree(data_path)
            elif args.action == "knowledge":
                result = _build_tree(data_path / "知识库集", base_name="知识库集")
            elif args.action == "lecturers":
                result = _build_tree(data_path / "讲师列表", base_name="讲师列表")
            else:
                result = {"error": f"未知action: {args.action}，可用: tree/knowledge/lecturers"}

    except Exception as e:
        result = {"status": "error", "message": str(e)}
    finally:
        db.close()

    # 清理 staging 文件（智能体写入的临时 JSON，操作完成后自动删除）
    if staging_file and staging_file.exists():
        try:
            staging_file.unlink()
        except OSError:
            pass

    print(json.dumps(result, ensure_ascii=False, indent=2, default=str))


if __name__ == "__main__":
    main()
