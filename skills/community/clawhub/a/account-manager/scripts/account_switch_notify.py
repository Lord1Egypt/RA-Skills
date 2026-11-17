#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
换号通知脚本 - 执行好友通知策略

功能：
1. 高价值好友：1 对 1 私信通知
2. 普通好友：朋友圈公告
3. 风险好友：通知 CEO 办
4. 低价值好友：跳过

输入：JSON 格式（通过 stdin）
输出：JSON 格式（通过 stdout）

使用示例：
```powershell
echo '{"categories":{...},"new_account":"wx_002","phone_number":"138****0002"}' | python account_switch_notify.py
```
"""

import json
import sys
from datetime import datetime
from typing import Any, Dict, List, Optional

from pathlib import Path as _Path
sys.path.insert(0, str(_Path(__file__).resolve().parent.parent.parent.parent / "scripts"))
sys.path.insert(0, str(_Path(__file__).resolve().parents[3]))  # T4-4: 添加项目根以支持mcps.shared导入
from mcps.shared.db_logger import get_logger
logger = get_logger("account-manager", source="skills/account-manager/scripts/account_switch_notify.py")


def generate_high_value_message(
    friend: Dict[str, str], new_account: str, phone_number: str
) -> str:
    """生成高价值好友 1 对 1 通知消息

    模板：
    {昵称}，我微信号可能近期会被限制使用，如果联系不上我，
    可以添加我的备用号：
    新微信号：{new_account}
    手机号：{phone_number}
    如果看到这个信息，麻烦通过一下，谢谢~

    Args:
        friend (Dict[str, str]): 参数说明
        new_account (str): 参数说明
        phone_number (str): 参数说明

    Returns:
        str: 返回值说明
    """
    nickname = friend.get("nickname", "好友")
    message = f"{nickname}，我微信号可能近期会被限制使用，如果联系不上我，可以添加我的备用号：\n新微信号：{new_account}\n手机号：{phone_number}\n如果看到这个信息，麻烦通过一下，谢谢~"
    return message


def generate_moment_template(new_account: str, phone_number: Optional[str] = None) -> str:
    """生成朋友圈公告模板（拟人化话术）

    模板选项：
    1. 生活化：最近换了个微信号，大家加一下这个新号~
    2. 随意型：旧号不怎么用了，有事找新号：{new_account}
    3. 简洁型：新号：{new_account}，备注名字就行

    Args:
        new_account (str): 参数说明
        phone_number (Optional[str]): 参数说明

    Returns:
        str: 返回值说明
    """
    import random

    templates = [
        f"最近换了个微信号，大家加一下这个新号：{new_account}\n有事找我就加这个号，备注名字就行~",
        f"旧号不怎么用了，有事找新号：{new_account}\n看到消息会回，不急~",
        f"新号：{new_account}\n懂的都懂，备注名字我通过",
        f"换个地方继续生活，新号：{new_account}\n老朋友都在，就差你了",
    ]

    message = random.choice(templates)

    if phone_number and random.random() > 0.5:  # 50% 概率附加手机号
        message += f"\n手机号也存一下：{phone_number}"

    return message


def generate_ceo_alert(
    risk_friends: List[Dict[str, Any]], agent_id: str, account_id: str
) -> str:
    """生成给 CEO 办的风险好友评估请求

    格式：
    【风险好友评估请求】
    员工：{agent_id}
    当前账号：{account_id}（即将换号）
    风险好友数：{count}个

    风险列表：
    1. {friend_id}（昵称：{nickname}）- 被举报{report_count}次，标签"风险"
    2. ...

    建议：全部放弃，不通知
    请确认是否执行？

    Args:
        risk_friends (List[Dict[str, Any]]): 参数说明
        agent_id (str): 参数说明
        account_id (str): 参数说明

    Returns:
        str: 返回值说明
    """
    alert = f"【风险好友评估请求】\n员工：{agent_id}\n当前账号：{account_id}（即将换号）\n风险好友数：{len(risk_friends)}个\n\n风险列表：\n"

    for i, friend in enumerate(risk_friends, 1):
        friend_id = friend.get("friend_id", "unknown")
        nickname = friend.get("nickname", "未知")
        report_count = friend.get("report_count", 0)
        blacklist_count = friend.get("blacklist_count", 0)
        tags = friend.get("tags", [])

        reason = []
        if report_count >= 2:
            reason.append(f"被举报{report_count}次")
        if blacklist_count >= 3:
            reason.append(f"被拉黑{blacklist_count}次")
        if "风险" in tags:
            reason.append("标签'风险'")

        alert += f"{i}. {friend_id}（昵称：{nickname}）- {'，'.join(reason)}\n"

    alert += "\n建议：全部放弃，不通知\n请确认是否执行？"
    return alert


def execute_notifications(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """执行通知策略

    Args:
        input_data (Dict[str, Any]): 参数说明

    返回：
    {
        "success": True,
        "notifications_sent": {...},
        "skipped": {...},
        "pending_manual_review": {...}
    }
    """
    categories = input_data.get("categories", {})
    high_value_friends = categories.get("high_value", {}).get("friends", [])
    normal_friends = categories.get("normal", {}).get("friends", [])
    risk_friends = categories.get("risk", {}).get("friends", [])
    low_value_friends = categories.get("low_value", {}).get("friends", [])

    new_account = input_data.get("new_account")
    phone_number = input_data.get("phone_number")
    agent_id = input_data.get("agent_id", "unknown")
    old_account = input_data.get("old_account", "unknown")

    result = {
        "success": True,
        "notifications_sent": {"high_value": [], "normal": [], "ceo_alert": None},
        "skipped": {
            "low_value_count": len(low_value_friends),
            "risk_count": len(risk_friends),
        },
        "pending_manual_review": [],
        "statistics": {},
    }

    # 1. 高价值好友 1 对 1 通知
    high_value_messages = []
    for friend in high_value_friends:
        message = generate_high_value_message(friend, new_account, phone_number)
        high_value_messages.append(
            {
                "friend_id": friend.get("friend_id"),
                "nickname": friend.get("nickname"),
                "message": message,
                "status": "pending",  # pending/sent/failed
                "method": "1 对 1 私信",
            }
        )

    result["notifications_sent"]["high_value"] = high_value_messages
    result["statistics"]["high_value_sent"] = len(high_value_messages)

    # 2. 普通好友朋友圈公告
    if normal_friends:
        moment_message = generate_moment_template(new_account, phone_number)
        result["notifications_sent"]["normal"] = {
            "message": moment_message,
            "visibility": f"{len(normal_friends)}个普通好友",
            "status": "pending",
            "method": "朋友圈公告",
            "scheduled_time": "新号登录后第 1 天",
        }
        result["statistics"]["normal_moment_scheduled"] = 1
    else:
        result["statistics"]["normal_moment_scheduled"] = 0

    # 3. 风险好友通知 CEO 办
    if risk_friends:
        ceo_alert = generate_ceo_alert(risk_friends, agent_id, old_account)
        result["notifications_sent"]["ceo_alert"] = {
            "message": ceo_alert,
            "recipient": "CEO 办",
            "status": "pending",
            "method": "消息通知",
            "priority": "P1",
        }
        result["pending_manual_review"] = risk_friends
        result["statistics"]["risk_pending_review"] = len(risk_friends)
    else:
        result["statistics"]["risk_pending_review"] = 0

    # 4. 低价值好友 - 跳过
    result["statistics"]["low_value_skipped"] = len(low_value_friends)

    # 总计
    result["statistics"]["total_processed"] = (
        len(high_value_friends)
        + len(normal_friends)
        + len(risk_friends)
        + len(low_value_friends)
    )

    return result


def main():
    """主函数"""
    try:
        # 读取输入
        input_data = json.loads(sys.stdin.read())

        # 验证必填字段
        if not input_data.get("categories"):
            print(
                json.dumps(
                    {
                        "success": False,
                        "error": "缺少 categories 字段",
                        "code": "MISSING_CATEGORIES",
                    }
                ),
                file=sys.stderr,
            )
            sys.exit(1)

        if not input_data.get("new_account"):
            print(
                json.dumps(
                    {
                        "success": False,
                        "error": "缺少 new_account 字段",
                        "code": "MISSING_NEW_ACCOUNT",
                    }
                ),
                file=sys.stderr,
            )
            sys.exit(1)

        # 执行通知
        result = execute_notifications(input_data)

        # 添加元数据
        result["processed_at"] = datetime.now().isoformat()
        result["agent_id"] = input_data.get("agent_id", "unknown")
        result["old_account"] = input_data.get("old_account", "unknown")
        result["new_account"] = input_data.get("new_account")

        # JSON 输出
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(0)

    except json.JSONDecodeError as e:
        logger.error(
            json.dumps(
                {
                    "success": False,
                    "error": f"输入 JSON 格式错误：{str(e)}",
                    "code": "INVALID_JSON_INPUT",
                }
            ),
            file=sys.stderr,
        )
        sys.exit(1)
    except Exception as e:
        logger.error(f"account switch notify异常: {e}", exc_info=True)
        logger.error(
            json.dumps(
                {
                    "success": False,
                    "error": f"脚本执行错误：{str(e)}",
                    "code": "SCRIPT_ERROR",
                }
            ),
            file=sys.stderr,
        )
        sys.exit(2)


if __name__ == "__main__":
    main()
