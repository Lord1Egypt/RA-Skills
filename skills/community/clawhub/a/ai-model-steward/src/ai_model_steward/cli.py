"""
AI Model Steward - CLI 入口
"""

import argparse
import json
import sys


def main():
    parser = argparse.ArgumentParser(
        prog="ai-model-steward",
        description="🤖 AI 模型智能管家 - 全自动模型监控与部署系统",
    )
    sub = parser.add_subparsers(dest="command")

    # daily
    p_daily = sub.add_parser("daily", help="每日情报搜集")
    p_daily.add_argument("--save-bitable", action="store_true", help="保存到飞书多维表格")
    p_daily.add_argument("--app-token", help="飞书多维表格 token")
    p_daily.add_argument("--table-id", help="飞书多维表格 table_id")

    # weekly
    p_weekly = sub.add_parser("weekly", help="生成周度部署建议报告")

    # history
    p_history = sub.add_parser("history", help="查看情报历史")
    p_history.add_argument("-n", "--limit", type=int, default=10, help="显示条数，默认10")
    p_history.add_argument("--free-only", action="store_true", help="仅显示免费/tokens相关")

    # approve
    p_approve = sub.add_parser("approve", help="审批通过并部署新模型")
    p_approve.add_argument("model", help="模型 ID")
    p_approve.add_argument("--position", type=int, help="插入位置")

    # reject/remove
    p_reject = sub.add_parser("reject", help="移除模型")
    p_reject.add_argument("model", help="模型 ID")

    # deploy
    p_deploy = sub.add_parser("deploy", help="执行部署")
    p_deploy.add_argument("action", choices=["add", "remove", "rollback", "list"], help="部署操作")
    p_deploy.add_argument("--model", help="模型ID")
    p_deploy.add_argument("--position", type=int)
    p_deploy.add_argument("--backup-path", help="回滚备份路径")

    args = parser.parse_args()

    if args.command == "daily":
        from .daily_intelligence import daily_intelligence
        result = daily_intelligence()
        print(f"\n✅ 完成: 新增 {result['new_items']} 条 | 总计 {result['total_items']} 条 | 免费 {result['free_related']} 条")

    elif args.command == "weekly":
        from .weekly_report import generate_weekly_report, load_weekly_data
        data = load_weekly_data()
        print(f"\n📥 加载 {len(data)} 条情报数据")
        result = generate_weekly_report(data)
        print(f"\n✅ 报告已生成: {result['report_file']}")

    elif args.command == "history":
        from pathlib import Path
        from datetime import datetime
        cache = Path.home() / ".openclaw" / ".ai-model-steward" / "daily_intelligence.json"
        if not cache.exists():
            print("暂无情报历史")
            sys.exit(0)
        data = json.loads(cache.read_text())
        if args.free_only:
            data = [i for i in data if i.get("is_free") or i.get("is_free_related")]
        for i in data[-args.limit:]:
            ts = i.get("fetched_at", "?")
            src = i.get("source", "?")
            title = i.get("title", "?")
            tag = "🎁" if (i.get("is_free") or i.get("is_free_related")) else "📰"
            print(f"  {tag} [{ts[:10]}] {src}: {title}")

    elif args.command == "approve":
        from .deployer import add_to_fallbacks
        result = add_to_fallbacks(args.model, args.position)
        print(json.dumps(result, indent=2, ensure_ascii=False))

    elif args.command == "reject":
        from .deployer import remove_from_fallbacks
        result = remove_from_fallbacks(args.model)
        print(json.dumps(result, indent=2, ensure_ascii=False))

    elif args.command == "deploy":
        if args.action == "list":
            from pathlib import Path
            import json
            config_path = Path.home() / ".openclaw" / "openclaw.json"
            if config_path.exists():
                config = json.loads(config_path.read_text())
                fallbacks = config["agents"]["defaults"]["model"].get("fallbacks", [])
                print(f"当前切换链 ({len(fallbacks)} 个模型):")
                for i, m in enumerate(fallbacks):
                    print(f"  {i+1}. {m}")
        elif args.action == "rollback":
            from .deployer import rollback_config
            if not args.backup_path:
                print("❌ 需要指定 --backup-path")
                sys.exit(1)
            rollback_config(args.backup_path)
        else:
            from .deployer import add_to_fallbacks, remove_from_fallbacks
            if not args.model:
                print("❌ 需要指定 --model")
                sys.exit(1)
            if args.action == "add":
                result = add_to_fallbacks(args.model, args.position)
            else:
                result = remove_from_fallbacks(args.model)
            print(json.dumps(result, indent=2, ensure_ascii=False))

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
