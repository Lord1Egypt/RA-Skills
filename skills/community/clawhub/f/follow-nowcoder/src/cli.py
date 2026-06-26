"""统一 CLI 工具

封装所有命令行操作，提供安全的接口给 Agent 使用。
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

# 添加父目录到路径以导入模块
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils import (
    load_config,
    save_config,
    get_default_config,
    load_prompt,
    save_prompt,
    reset_prompt,
    USER_CONFIG_PATH,
    USER_PROMPTS_DIR,
    USER_CONFIG_DIR,
)
from src.search import search_posts, get_post_detail, SearchResult
from src.analyzer import prepare_summary


# ==================== 辅助函数 ====================

def json_output(data: Any) -> str:
    """输出 JSON 格式结果"""
    # 在 Windows 上设置 UTF-8 编码输出
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding='utf-8')
    return json.dumps(data, ensure_ascii=False, indent=2)


def error_output(message: str) -> str:
    """输出错误信息"""
    return json_output({"error": message})


def print_json(data: Any) -> None:
    """安全地打印 JSON 输出"""
    # 在 Windows 上设置 UTF-8 编码输出
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding='utf-8')
    print(json.dumps(data, ensure_ascii=False, indent=2))


# ==================== Onboarding 命令 ====================

def cmd_check_onboarding(args) -> Dict[str, Any]:
    """检查 onboarding 状态"""
    try:
        config = load_config()
        complete = config.get("onboarding_complete", False)
        return {"complete": bool(complete)}
    except Exception as e:
        return {"error": str(e), "complete": False}


def cmd_check_deps(args) -> Dict[str, Any]:
    """检查依赖是否安装"""
    missing = []
    all_installed = True

    # 检查 requests
    try:
        import requests
    except ImportError:
        missing.append("requests")
        all_installed = False

    # 检查 pydantic
    try:
        import pydantic
    except ImportError:
        missing.append("pydantic")
        all_installed = False

    return {
        "installed": all_installed,
        "missing": missing,
    }


def cmd_init_config(args) -> Dict[str, Any]:
    """初始化配置

    支持从 JSON 输入或参数读取配置
    """
    try:
        # 优先从 json_input 读取
        if args.json_input:
            config = json.loads(args.json_input)
        # 否则使用默认配置
        else:
            config = get_default_config()
            config["onboarding_complete"] = True

        save_config(config)
        return {"success": True, "config": config}
    except Exception as e:
        return {"error": str(e), "success": False}


# ==================== 配置管理命令 ====================

def cmd_get_config(args) -> Dict[str, Any]:
    """获取完整配置"""
    try:
        config = load_config()
        return {"config": config}
    except Exception as e:
        return {"error": str(e)}


def cmd_set_config(args) -> Dict[str, Any]:
    """设置单个配置项

    用法: set-config <key> <value>
    """
    try:
        if len(args.args) < 2:
            return {"error": "需要提供 key 和 value 参数", "success": False}

        key = args.args[0]
        value_str = args.args[1]

        # 尝试解析 JSON 值
        try:
            value = json.loads(value_str)
        except json.JSONDecodeError:
            # 保持为字符串
            value = value_str

        config = load_config()
        config[key] = value
        save_config(config)

        return {"success": True, "config": config}
    except Exception as e:
        return {"error": str(e), "success": False}


def cmd_update_config(args) -> Dict[str, Any]:
    """批量更新配置

    用法: update-config --json-input '{"key": "value"}'
    """
    try:
        if not args.json_input:
            return {"error": "需要提供 --json-input 参数", "success": False}

        updates = json.loads(args.json_input)
        config = load_config()
        config.update(updates)
        save_config(config)

        return {"success": True, "config": config}
    except Exception as e:
        return {"error": str(e), "success": False}


def cmd_reset_config(args) -> Dict[str, Any]:
    """重置为默认配置"""
    try:
        config = get_default_config()
        config["onboarding_complete"] = True  # 保持 onboarding 状态
        save_config(config)
        return {"success": True, "config": config}
    except Exception as e:
        return {"error": str(e), "success": False}


# ==================== 搜索相关命令 ====================

def cmd_search_posts(args) -> Dict[str, Any]:
    """搜索帖子

    使用当前配置搜索
    """
    try:
        config = load_config()

        # 执行搜索
        search_results = search_posts(
            keywords=config['search_keywords'],
            max_pages=config['max_pages'],
            tag=config['tag'],
            order=config['order'],
            delay=config['request_delay'],
            max_results=config.get('max_results_per_keyword', 5),
            time_window_days=config.get('time_window_days', 3)
        )

        # 统计信息
        total_count = sum(result.size for result in search_results.values())
        total_found = sum(result.total for result in search_results.values())

        # 序列化结果
        serialized_results = {}
        for keyword, result in search_results.items():
            serialized_results[keyword] = {
                "size": result.size,
                "total": result.total,
                "total_page": result.total_page,
                "records": [
                    {
                        "title": r.title,
                        "rc_type": r.rc_type,
                        "uuid": r.uuid,
                        "content_id": r.content_id,
                        "created_at": r.created_at,
                        "view_count": r.view_count,
                        "like_count": r.like_count,
                        "comment_count": r.comment_count,
                        "company": r.company,
                        "job_title": r.job_title,
                    }
                    for r in result.records
                ]
            }

        return {
            "results": serialized_results,
            "stats": {
                "total_count": total_count,
                "total_found": total_found,
                "keywords_count": len(search_results)
            }
        }
    except Exception as e:
        return {"error": str(e), "results": {}, "stats": {"total_count": 0}}


def cmd_get_post_details(args) -> Dict[str, Any]:
    """获取帖子详情

    用法: get-post-details --json-input '[{"title": "...", "rc_type": 201, "uuid": "..."}]'
    """
    try:
        if not args.json_input:
            return {"error": "需要提供 --json-input 参数", "details": {}}

        records = json.loads(args.json_input)
        if not isinstance(records, list):
            return {"error": "json_input 必须是数组", "details": {}}

        details = {}
        for record in records:
            try:
                # 重建 SearchRecord 对象
                from src.search import SearchRecord
                search_record = SearchRecord(**record)

                detail = get_post_detail(search_record)
                if detail:
                    record_key = search_record.uuid or search_record.content_id
                    details[record_key] = {
                        "title": detail.title,
                        "content": detail.content[:5000] if len(detail.content) > 5000 else detail.content,
                        "truncated": len(detail.content) > 5000,
                    }
            except Exception:
                continue

        return {"details": details}
    except Exception as e:
        return {"error": str(e), "details": {}}


# ==================== 报告准备命令 ====================

def cmd_prepare_report(args) -> Dict[str, Any]:
    """完整报告准备流程

    整合：加载配置 -> 搜索帖子 -> 获取详情 -> 准备提示词 -> 保存到文件

    返回轻量级元数据，完整数据保存到文件供 Agent 读取
    """
    try:
        config = load_config()

        # 搜索帖子
        search_results = search_posts(
            keywords=config['search_keywords'],
            max_pages=config['max_pages'],
            tag=config['tag'],
            order=config['order'],
            delay=config['request_delay'],
            max_results=config.get('max_results_per_keyword', 5),
            time_window_days=config.get('time_window_days', 3)
        )

        # 准备报告数据
        result = prepare_summary(search_results, config, fetch_details=True)

        # 保存到临时文件（.claude/temp 目录）
        from pathlib import Path
        temp_dir = Path(".claude/temp")
        temp_dir.mkdir(parents=True, exist_ok=True)
        output_file = temp_dir / "report_data.json"

        # 确保 UTF-8 编码写入
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        # 返回轻量级元数据，完整数据在文件中
        return {
            "success": True,
            "output_file": str(output_file.absolute()),
            "metadata": {
                "total_count": result.get("context", {}).get("total_count", 0),
                "keywords": result.get("context", {}).get("keywords", ""),
                "time_window_days": result.get("context", {}).get("time_window_days", 0),
                "prompt_length": len(result.get("prompt", "")),
            }
        }
    except Exception as e:
        return {"error": str(e), "success": False}


# ==================== 提示词管理命令 ====================

def cmd_get_prompt(args) -> Dict[str, Any]:
    """获取提示词内容

    用法: get-prompt <name>
    """
    try:
        if not args.args:
            return {"error": "需要提供提示词名称", "content": ""}

        name = args.args[0]
        content = load_prompt(name)
        return {"content": content}
    except FileNotFoundError:
        return {"error": f"提示词不存在: {args.args[0]}", "content": ""}
    except Exception as e:
        return {"error": str(e), "content": ""}


def cmd_set_prompt(args) -> Dict[str, Any]:
    """设置提示词

    用法: set-prompt <name> <content>
         或: set-prompt <name> --json-input '{"content": "..."}'
    """
    try:
        if not args.args:
            return {"error": "需要提供提示词名称", "success": False}

        name = args.args[0]

        # 优先从 json_input 读取内容
        if args.json_input:
            data = json.loads(args.json_input)
            content = data.get("content", "")
        # 否则从参数读取
        elif len(args.args) >= 2:
            content = args.args[1]
        else:
            return {"error": "需要提供提示词内容", "success": False}

        save_prompt(name, content)
        return {"success": True}
    except Exception as e:
        return {"error": str(e), "success": False}


def cmd_reset_prompt(args) -> Dict[str, Any]:
    """重置提示词为默认

    用法: reset-prompt <name>
    """
    try:
        if not args.args:
            return {"error": "需要提供提示词名称", "success": False}

        name = args.args[0]
        success = reset_prompt(name)
        return {"success": success}
    except Exception as e:
        return {"error": str(e), "success": False}


# ==================== 主函数 ====================

def main():
    parser = argparse.ArgumentParser(
        description="NowCoder 面经搜索 CLI 工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument("command", help="命令名称")
    parser.add_argument("args", nargs="*", help="命令参数")
    parser.add_argument("--json-input", help="JSON 输入参数")

    args = parser.parse_args()

    # 命令映射
    COMMANDS = {
        "check-onboarding": cmd_check_onboarding,
        "check-deps": cmd_check_deps,
        "init-config": cmd_init_config,
        "get-config": cmd_get_config,
        "set-config": cmd_set_config,
        "update-config": cmd_update_config,
        "reset-config": cmd_reset_config,
        "search-posts": cmd_search_posts,
        "get-post-details": cmd_get_post_details,
        "prepare-report": cmd_prepare_report,
        "get-prompt": cmd_get_prompt,
        "set-prompt": cmd_set_prompt,
        "reset-prompt": cmd_reset_prompt,
    }

    if args.command not in COMMANDS:
        print_json({"error": f"未知命令: {args.command}"})
        sys.exit(1)

    # 执行命令
    try:
        result = COMMANDS[args.command](args)
        print_json(result)
    except Exception as e:
        print_json({"error": str(e)})
        sys.exit(1)


if __name__ == "__main__":
    main()
