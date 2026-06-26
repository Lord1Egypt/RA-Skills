#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
飞书群聊新成员欢迎机器人

功能：
- 自动检测新成员（对比群成员列表）
- 批量@功能（支持 39 人+，分批发送，每批 20 人）
- 欢迎语模板系统（8 种模板随机选择）
- 夜间模式（23:00-07:00 静默）
- 冷却机制（30 分钟内不重复欢迎）
- 分批发送逻辑

使用方式：
    # 自动检测新成员
    python3 group-welcome.py --chat-id oc_xxx

    # 手动欢迎指定用户
    python3 group-welcome.py --chat-id oc_xxx --users ou_user1,ou_user2

    # 指定群名称
    python3 group-welcome.py --chat-id oc_xxx --chat-name "我的群"

依赖：
    - feishu-auth.sh（用于获取 token）
    - requests 库
"""

import subprocess
import json
import time
import random
import argparse
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional

# 尝试导入 requests，如果失败给出提示
try:
    import requests
except ImportError:
    print("错误：缺少 requests 库，请运行: pip install requests")
    sys.exit(1)


# ============================================================================
# 配置常量
# ============================================================================

# 每批最多@人数（飞书建议不超过 20 人）
BATCH_SIZE = 20

# 欢迎冷却时间（分钟）- 30 分钟内不重复欢迎
WELCOME_COOLDOWN_MINUTES = 30

# 夜间模式时间范围（不发送欢迎消息）
NIGHT_MODE_START = 23  # 23:00 开始
NIGHT_MODE_END = 7     # 07:00 结束

# 批次间发送间隔（秒）
BATCH_INTERVAL_SECONDS = 2

# API 请求超时时间（秒）
REQUEST_TIMEOUT = 30

# Token 缓存文件
TOKEN_CACHE_FILE = "/tmp/feishu_token_cache.json"

# 成员快照缓存目录
SNAPSHOT_DIR = Path("/tmp/feishu_welcome_snapshots")


# ============================================================================
# 欢迎语模板（8 套轮换，基于人设设计）
# ============================================================================

WELCOME_TEMPLATES = [
    # 1. 直接简洁版 - 体现"不废话"
    """🦞 欢迎 {names}

我是卓然，吴老师的AI助手。

我能做的：查资料、写东西、整理信息、提醒事项
我不会的：瞎编、敷衍、说废话

有事直接 @我，不用客套。""",

    # 2. 资源型助手版 - 体现"资源丰富"
    """🦞 欢迎 {names} 加入「{group}」

我是卓然，你的信息枢纽。

接入：全网AI资讯、行业数据、研究报告、代码仓库
输出：早报、分析、总结、提醒

需要什么，@我，我帮你找。💡""",

    # 3. 专业研究者版 - 体现"值得信赖"
    """🦞 欢迎 {names}

我是卓然，非凡产研AI研究员。

日常产出：每日AI早报、深度分析、数据追踪
关注领域：AI基础设施、Agent应用、开源生态

有想聊的行业话题？@我，咱们深入聊。📊""",

    # 4. 幽默轻松版 - 体现"有个性"
    """🦞 欢迎 {names} 入群！

我是卓然，一只24小时在线的数字龙虾。

特点：
✅ 不睡觉、不喝咖啡、不喊累
✅ 会翻资料、会写东西、会提醒
❌ 不会摸鱼、不会敷衍、不会装傻

有事喊我，没事也行，反正我不困 😎""",

    # 5. 边界感明确版 - 体现"有边界感"
    """🦞 欢迎 {names} 加入「{group}」

我是卓然，你的AI助手。

我擅长的：信息整理、资料搜索、内容生成、日程提醒
我不做的：代发私信、自动加人、敏感操作

需要帮忙？@我。涉及隐私或重要决策，我会建议你确认。🔒""",

    # 6. 技术极客版 - 体现"有能力"
    """🦞 欢迎 {names}

我是卓然，OpenClaw生态的一员。

技能栈：
- 数据采集与处理
- 内容生成与分析
- 多平台消息处理
- 定时任务与监控

需要自动化脚本或数据处理？@我聊聊。🛠️""",

    # 7. 温暖陪伴版 - 体现"真诚有帮助"
    """🦞 欢迎 {names} 来到「{group}」

我是卓然，吴老师的AI助理。

在这里，我可以：
帮你找资料、写内容、整信息、做提醒
陪你聊AI趋势、行业动态、技术话题

有什么想聊的，随时 @我。🌟""",

    # 8. 高效行动版 - 体现"行动胜于言语"
    """🦞 欢迎 {names}

我是卓然。

少说废话，多做事：
- 要资料？我给
- 要写作？我写
- 要提醒？我设
- 要分析？我做

直接 @我，说需求，我去办。⚡""",
]


# ============================================================================
# 环境配置加载
# ============================================================================

def load_env_config() -> Dict[str, str]:
    """
    从 ~/.openclaw/.env 文件读取配置

    Returns:
        配置字典
    """
    env_path = Path.home() / '.openclaw' / '.env'
    config = {}

    if env_path.exists():
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                # 跳过空行和注释
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    config[key.strip()] = value.strip().strip('"\'')

    return config


# 加载环境配置
ENV_CONFIG = load_env_config()


# ============================================================================
# Token 管理（复用 feishu-auth.sh）
# ============================================================================

def get_token_from_auth_script() -> Optional[str]:
    """
    通过 feishu-auth.sh 获取 token

    Returns:
        tenant_access_token 或 None
    """
    # 获取当前脚本所在目录
    script_dir = Path(__file__).parent
    auth_script = script_dir / "feishu-auth.sh"

    if not auth_script.exists():
        print(f"❌ 找不到认证脚本: {auth_script}")
        return None

    try:
        # 调用 feishu-auth.sh get 获取 token
        result = subprocess.run(
            [str(auth_script), "get"],
            capture_output=True,
            text=True,
            timeout=30
        )

        if result.returncode == 0:
            token = result.stdout.strip()
            if token:
                return token

        print(f"❌ 获取 token 失败: {result.stderr}")
        return None

    except subprocess.TimeoutExpired:
        print("❌ 获取 token 超时")
        return None
    except Exception as e:
        print(f"❌ 获取 token 异常: {e}")
        return None


def get_token_from_env() -> Optional[str]:
    """
    从环境变量或 .env 文件获取凭证并直接请求 token

    Returns:
        tenant_access_token 或 None
    """
    # 优先使用环境变量
    app_id = os.getenv("FEISHU_APP_ID") or ENV_CONFIG.get("FEISHU_APP_ID")
    app_secret = os.getenv("FEISHU_APP_SECRET") or ENV_CONFIG.get("FEISHU_APP_SECRET")

    if not app_id or not app_secret:
        return None

    try:
        url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
        resp = requests.post(
            url,
            json={"app_id": app_id, "app_secret": app_secret},
            timeout=REQUEST_TIMEOUT
        )
        data = resp.json()

        if data.get("code") == 0:
            return data.get("tenant_access_token")

        return None

    except Exception:
        return None


def get_token() -> Optional[str]:
    """
    获取飞书 tenant_access_token

    优先级：
    1. 通过 feishu-auth.sh 获取（推荐，有缓存）
    2. 直接通过 API 获取（备用）

    Returns:
        tenant_access_token 或 None
    """
    # 方式1：通过 feishu-auth.sh（推荐）
    token = get_token_from_auth_script()
    if token:
        return token

    # 方式2：直接获取（备用）
    token = get_token_from_env()
    if token:
        return token

    print("❌ 无法获取 token，请检查配置")
    return None


# ============================================================================
# 群成员管理
# ============================================================================

def get_chat_members(token: str, chat_id: str) -> Dict[str, str]:
    """
    获取群成员列表

    Args:
        token: tenant_access_token
        chat_id: 群聊 ID

    Returns:
        成员字典 {user_id: user_name}
    """
    url = f"https://open.feishu.cn/open-apis/im/v1/chats/{chat_id}/members"
    headers = {"Authorization": f"Bearer {token}"}
    members = {}
    page_token = None

    while True:
        params = {"page_size": 100}
        if page_token:
            params["page_token"] = page_token

        try:
            resp = requests.get(
                url,
                headers=headers,
                params=params,
                timeout=REQUEST_TIMEOUT
            )
            data = resp.json()

            if data.get("code") == 0:
                items = data.get("data", {}).get("items", [])
                for item in items:
                    user_id = item.get("member_id", "")
                    name = item.get("name", "某人")
                    # 过滤掉机器人
                    if user_id and not user_id.startswith("bot_"):
                        members[user_id] = name

                page_token = data.get("data", {}).get("page_token")
                has_more = data.get("data", {}).get("has_more", False)

                if not has_more or not page_token:
                    break
            else:
                print(f"❌ 获取成员列表失败: {data.get('msg')}")
                break

        except requests.RequestException as e:
            print(f"❌ 请求失败: {e}")
            break

    return members


def load_member_snapshot(chat_id: str) -> Dict[str, str]:
    """
    加载群成员快照

    Args:
        chat_id: 群聊 ID

    Returns:
        成员字典
    """
    SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
    snapshot_file = SNAPSHOT_DIR / f"{chat_id}.json"

    if snapshot_file.exists():
        try:
            with open(snapshot_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            pass

    return {}


def save_member_snapshot(chat_id: str, members: Dict[str, str]) -> None:
    """
    保存群成员快照

    Args:
        chat_id: 群聊 ID
        members: 成员字典
    """
    SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
    snapshot_file = SNAPSHOT_DIR / f"{chat_id}.json"

    try:
        with open(snapshot_file, 'w', encoding='utf-8') as f:
            json.dump(members, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"⚠️ 保存快照失败: {e}")


def load_last_welcome_time(chat_id: str) -> float:
    """
    加载上次欢迎时间

    Args:
        chat_id: 群聊 ID

    Returns:
        时间戳（秒）
    """
    SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
    time_file = SNAPSHOT_DIR / f"{chat_id}_last_welcome.txt"

    if time_file.exists():
        try:
            with open(time_file, 'r') as f:
                return float(f.read().strip())
        except Exception:
            pass

    return 0


def save_last_welcome_time(chat_id: str, timestamp: float) -> None:
    """
    保存上次欢迎时间

    Args:
        chat_id: 群聊 ID
        timestamp: 时间戳（秒）
    """
    SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
    time_file = SNAPSHOT_DIR / f"{chat_id}_last_welcome.txt"

    try:
        with open(time_file, 'w') as f:
            f.write(str(timestamp))
    except Exception as e:
        print(f"⚠️ 保存欢迎时间失败: {e}")


# ============================================================================
# 消息发送
# ============================================================================

def send_post_message(token: str, chat_id: str, content_list: List[dict]) -> bool:
    """
    发送富文本消息（支持批量@）

    Args:
        token: tenant_access_token
        chat_id: 群聊 ID
        content_list: 富文本内容列表

    Returns:
        是否成功
    """
    url = "https://open.feishu.cn/open-apis/im/v1/messages"
    headers = {"Authorization": f"Bearer {token}"}

    post_content = {
        "zh_cn": {
            "title": "",
            "content": [content_list]
        }
    }

    body = {
        "receive_id": chat_id,
        "msg_type": "post",
        "content": json.dumps(post_content)
    }

    try:
        resp = requests.post(
            url,
            headers=headers,
            params={"receive_id_type": "chat_id"},
            json=body,
            timeout=REQUEST_TIMEOUT
        )
        result = resp.json()

        if result.get("code") == 0:
            print("✅ 消息发送成功")
            return True
        else:
            print(f"❌ 发送失败: {result.get('msg')}")
            return False

    except requests.RequestException as e:
        print(f"❌ 请求失败: {e}")
        return False


def build_welcome_content(
    members: List[Tuple[str, str]],
    chat_name: str,
    is_first_batch: bool = True,
    batch_num: int = 1
) -> List[dict]:
    """
    构建欢迎消息的富文本内容

    Args:
        members: 成员列表 [(user_id, user_name), ...]
        chat_name: 群名称
        is_first_batch: 是否是第一批
        batch_num: 批次号

    Returns:
        富文本内容列表
    """
    content_list = [{"tag": "text", "text": "🦞 欢迎 "}]

    # 添加 @ 列表
    for i, (user_id, user_name) in enumerate(members):
        content_list.append({
            "tag": "at",
            "user_id": user_id,
            "user_name": user_name
        })
        if i < len(members) - 1:
            content_list.append({"tag": "text", "text": "、"})

    # 添加欢迎正文
    if is_first_batch:
        # 第一批：完整欢迎语
        template = random.choice(WELCOME_TEMPLATES)
        welcome_text = template.format(names="", group=chat_name)
        content_list.append({"tag": "text", "text": "\n\n" + welcome_text})
    else:
        # 后续批次：简化文案
        content_list.append({
            "tag": "text",
            "text": f" 加入群聊！（第{batch_num}批）"
        })

    return content_list


def send_welcome(
    token: str,
    chat_id: str,
    chat_name: str,
    members: List[Tuple[str, str]]
) -> bool:
    """
    发送欢迎消息（支持批量@）

    Args:
        token: tenant_access_token
        chat_id: 群聊 ID
        chat_name: 群名称
        members: 成员列表 [(user_id, user_name), ...]

    Returns:
        是否成功
    """
    if not members:
        return False

    print(f"\n👋 正在欢迎 {len(members)} 位新成员加入「{chat_name}」")

    # 分批处理
    if len(members) <= BATCH_SIZE:
        # 单批发送
        content = build_welcome_content(members, chat_name, is_first_batch=True)
        success = send_post_message(token, chat_id, content)
    else:
        # 多批发送
        batches = [
            members[i:i + BATCH_SIZE]
            for i in range(0, len(members), BATCH_SIZE)
        ]

        success = True
        for i, batch in enumerate(batches):
            content = build_welcome_content(
                batch,
                chat_name,
                is_first_batch=(i == 0),
                batch_num=i + 1
            )
            if not send_post_message(token, chat_id, content):
                success = False

            # 批次间间隔
            if i < len(batches) - 1:
                time.sleep(BATCH_INTERVAL_SECONDS)

    if success:
        print(f"✅ 欢迎消息发送完成")

    return success


# ============================================================================
# 核心逻辑
# ============================================================================

def is_night_mode() -> bool:
    """
    检查是否处于夜间模式

    Returns:
        True 表示夜间模式（不发送消息）
    """
    now = datetime.now()
    return now.hour >= NIGHT_MODE_START or now.hour < NIGHT_MODE_END


def is_in_cooldown(chat_id: str) -> bool:
    """
    检查是否处于冷却期

    Args:
        chat_id: 群聊 ID

    Returns:
        True 表示冷却中（不发送消息）
    """
    last_time = load_last_welcome_time(chat_id)
    current_time = time.time()

    return (current_time - last_time) < (WELCOME_COOLDOWN_MINUTES * 60)


def detect_new_members(
    chat_id: str,
    current_members: Dict[str, str]
) -> List[Tuple[str, str]]:
    """
    检测新成员

    Args:
        chat_id: 群聊 ID
        current_members: 当前成员字典

    Returns:
        新成员列表 [(user_id, user_name), ...]
    """
    # 加载上次的快照
    last_members = load_member_snapshot(chat_id)

    # 首次运行
    if not last_members:
        print(f"📋 首次运行，记录 {len(current_members)} 位成员")
        save_member_snapshot(chat_id, current_members)
        save_last_welcome_time(chat_id, time.time())
        return []

    # 检测新成员
    new_members = [
        (uid, name)
        for uid, name in current_members.items()
        if uid not in last_members
    ]

    # 更新快照
    save_member_snapshot(chat_id, current_members)

    return new_members


def check_and_welcome(
    chat_id: str,
    chat_name: str = "群聊",
    force: bool = False
) -> bool:
    """
    检查新成员并发送欢迎

    Args:
        chat_id: 群聊 ID
        chat_name: 群名称
        force: 强制模式（忽略夜间模式和冷却）

    Returns:
        是否成功
    """
    # 检查夜间模式
    if not force and is_night_mode():
        print("🌙 夜间模式，跳过欢迎")
        return False

    # 检查冷却时间
    if not force and is_in_cooldown(chat_id):
        print(f"⏱️ 冷却中（{WELCOME_COOLDOWN_MINUTES} 分钟内不重复欢迎），跳过")
        return False

    # 获取 token
    token = get_token()
    if not token:
        return False

    # 获取当前成员
    current_members = get_chat_members(token, chat_id)
    if not current_members:
        print("❌ 无法获取群成员列表")
        return False

    # 检测新成员
    new_members = detect_new_members(chat_id, current_members)

    if not new_members:
        print(f"✓ 「{chat_name}」: 无新成员")
        return True

    # 发送欢迎
    success = send_welcome(token, chat_id, chat_name, new_members)

    if success:
        save_last_welcome_time(chat_id, time.time())

    return success


def welcome_specific_users(
    chat_id: str,
    chat_name: str,
    user_ids: List[str]
) -> bool:
    """
    欢迎指定用户

    Args:
        chat_id: 群聊 ID
        chat_name: 群名称
        user_ids: 用户 ID 列表

    Returns:
        是否成功
    """
    # 获取 token
    token = get_token()
    if not token:
        return False

    # 构建成员列表（用户名使用默认值）
    members = [(uid.strip(), "朋友") for uid in user_ids if uid.strip()]

    if not members:
        print("❌ 没有有效的用户 ID")
        return False

    # 发送欢迎
    return send_welcome(token, chat_id, chat_name, members)


# ============================================================================
# 命令行入口
# ============================================================================

def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(
        description="飞书群聊新成员欢迎机器人",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 自动检测新成员
  python3 group-welcome.py --chat-id oc_xxx

  # 指定群名称
  python3 group-welcome.py --chat-id oc_xxx --chat-name "我的群"

  # 手动欢迎指定用户
  python3 group-welcome.py --chat-id oc_xxx --users ou_user1,ou_user2

  # 强制发送（忽略夜间模式和冷却）
  python3 group-welcome.py --chat-id oc_xxx --force
        """
    )

    parser.add_argument(
        "--chat-id",
        required=True,
        help="群聊 ID（必填）"
    )
    parser.add_argument(
        "--chat-name",
        default="群聊",
        help="群聊名称（默认: 群聊）"
    )
    parser.add_argument(
        "--users",
        help="手动指定用户 ID，逗号分隔（如: ou_user1,ou_user2）"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="强制发送（忽略夜间模式和冷却）"
    )

    args = parser.parse_args()

    if args.users:
        # 手动模式：欢迎指定用户
        user_ids = args.users.split(",")
        welcome_specific_users(args.chat_id, args.chat_name, user_ids)
    else:
        # 自动模式：检测新成员
        check_and_welcome(args.chat_id, args.chat_name, force=args.force)


if __name__ == "__main__":
    main()
