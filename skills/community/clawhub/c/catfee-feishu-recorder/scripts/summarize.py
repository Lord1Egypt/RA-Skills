#!/usr/bin/env python3
"""
飞书群聊总结脚本
用法: python summarize_group.py <chat_id> <days>
示例: python summarize_group.py oc_281d2d2dcec5e1fcd29d7ac809e75111 7
"""
import requests
import json
import re
import sys
import os
import subprocess
from datetime import datetime, timedelta
from typing import Tuple, List, Dict
from collections import Counter

# 飞书凭证 - 必须从环境变量读取
APP_ID = os.environ.get("FEISHU_APP_ID", "")
APP_SECRET = os.environ.get("FEISHU_APP_SECRET", "")

if not APP_ID or not APP_SECRET:
    raise ValueError("未配置飞书凭证！请设置环境变量 FEISHU_APP_ID 和 FEISHU_APP_SECRET")

# API URLs
AUTH_URL = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
MESSAGES_URL = "https://open.feishu.cn/open-apis/im/v1/messages"
CHAT_MEMBERS_URL = "https://open.feishu.cn/open-apis/im/v1/chats/{chat_id}/members"
USER_INFO_URL = "https://open.feishu.cn/open-apis/contact/v3/users/{user_id}"
DOC_CREATE_URL = "https://open.feishu.cn/open-apis/docx/v1/documents"


def get_token() -> str:
    resp = requests.post(AUTH_URL, json={
        "app_id": APP_ID,
        "app_secret": APP_SECRET
    })
    data = resp.json()
    if data.get("code") != 0:
        raise Exception(f"获取token失败: {data}")
    return data["tenant_access_token"]


def parse_time_range(input_text: str) -> Tuple[int, int]:
    now = datetime.now()
    end_ts = int(now.timestamp())
    
    text = input_text.lower().strip()
    
    date_pattern = re.compile(r'(\d{4})[年\-/](\d{1,2})[月\-/](\d{1,2})')
    date_match = date_pattern.search(text)
    if date_match:
        year, month, day = int(date_match.group(1)), int(date_match.group(2)), int(date_match.group(3))
        start_dt = datetime(year, month, day)
        return int(start_dt.timestamp()), end_ts
    
    if "昨天" in text:
        start_dt = now - timedelta(days=1)
    elif "今天" in text:
        start_dt = now - timedelta(days=1)
    elif "最近几天" in text or ("最近" in text and "月" not in text):
        start_dt = now - timedelta(days=7)
    elif "这周" in text or "本周" in text or "最近一周" in text:
        start_dt = now - timedelta(days=7)
    elif "最近两周" in text or "两周" in text:
        start_dt = now - timedelta(days=14)
    elif "这个月" in text or "本月" in text or "最近一个月" in text:
        start_dt = now - timedelta(days=30)
    elif "一年" in text:
        start_dt = now - timedelta(days=365)
    else:
        num_pattern = re.compile(r'(\d+)\s*(天|周|月|日)')
        num_match = num_pattern.search(text)
        if num_match:
            num = int(num_match.group(1))
            unit = num_match.group(2)
            if unit in ["天", "日"]:
                start_dt = now - timedelta(days=num)
            elif unit == "周":
                start_dt = now - timedelta(weeks=num)
            elif unit == "月":
                start_dt = now - timedelta(days=num * 30)
            else:
                start_dt = now - timedelta(days=7)
        else:
            start_dt = now - timedelta(days=7)
    
    return int(start_dt.timestamp()), end_ts


def get_chat_members(token: str, chat_id: str) -> Dict[str, Dict]:
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    members = {}
    page_token = None
    
    while True:
        url = f"https://open.feishu.cn/open-apis/im/v1/chats/{chat_id}/members?member_id_type=user_id&page_size=100"
        if page_token:
            url += f"&page_token={page_token}"
        
        try:
            resp = requests.get(url, headers=headers, timeout=10)
            data = resp.json()
            
            if data.get("code") == 0:
                items = data.get("data", {}).get("items", [])
                for member in items:
                    uid = member.get("member_id", "")
                    if uid:
                        members[uid] = {
                            "name": member.get("name", uid),
                            "en_name": member.get("en_name", ""),
                            "avatar": member.get("avatar", {}),
                            "tenant_id": member.get("tenant_id", "")
                        }
                
                has_more = data.get("data", {}).get("has_more", False)
                if not has_more:
                    break
                page_token = data.get("data", {}).get("page_token")
            else:
                print(f"  [警告] 获取群成员失败: {data.get('msg', '未知错误')}")
                break
        except Exception as e:
            print(f"  [警告] 获取群成员异常: {e}")
            break
    
    return members


def fetch_messages(token: str, chat_id: str, start_ts: int, end_ts: int) -> List[Dict]:
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    all_messages = []
    page_token = None
    
    while True:
        url = f"{MESSAGES_URL}?container_id_type=chat&container_id={chat_id}&start_time={start_ts}&end_time={end_ts}&page_size=50"
        if page_token:
            url += f"&page_token={page_token}"
        
        resp = requests.get(url, headers=headers, timeout=10)
        data = resp.json()
        
        if data.get("code") != 0:
            if data.get("code") == 230027:
                raise Exception("权限不足：需要 im:message:readonly 权限，请管理员在飞书开放平台添加")
            raise Exception(f"拉取消息失败: {data}")
        
        items = data.get("data", {}).get("items", [])
        all_messages.extend(items)
        
        has_more = data.get("data", {}).get("has_more", False)
        if not has_more:
            break
        page_token = data.get("data", {}).get("page_token")
        
        if len(all_messages) >= 1000:
            break
    
    return all_messages


def extract_text_messages(messages: List[Dict]) -> List[Dict]:
    text_msgs = []
    for msg in messages:
        msg_type = msg.get("msg_type", "")
        if msg_type == "text":
            content = msg.get("body", {}).get("content", "")
            try:
                content_text = json.loads(content).get("text", "") if content else ""
            except:
                content_text = content
            if content_text.strip() and content_text != "This message was recalled":
                sender = msg.get("sender", {})
                text_msgs.append({
                    "time": datetime.fromtimestamp(int(msg.get("create_time", 0)) / 1000),
                    "time_str": datetime.fromtimestamp(int(msg.get("create_time", 0)) / 1000).strftime("%Y-%m-%d %H:%M"),
                    "sender_id": sender.get("id", "unknown"),
                    "sender_type": sender.get("sender_type", ""),
                    "content": content_text
                })
    return text_msgs


def generate_summary(text_msgs: List[Dict], user_names: Dict[str, str], start_ts: int, end_ts: int) -> str:
    start_date = datetime.fromtimestamp(start_ts).strftime("%Y-%m-%d")
    end_date = datetime.fromtimestamp(end_ts).strftime("%Y-%m-%d")
    
    total_msgs = len(text_msgs)
    sender_counts = Counter()
    for msg in text_msgs:
        sender_counts[msg["sender_id"]] += 1
    
    lines = []
    lines.append("# 群聊总结")
    lines.append("")
    lines.append(f"**时间范围：** {start_date} ~ {end_date}")
    lines.append(f"**总消息数：** {total_msgs}条文本消息")
    lines.append("")
    
    if sender_counts:
        lines.append("## 活跃成员 Top 10")
        lines.append("")
        lines.append("| 排名 | 昵称 | 用户ID | 消息数 |")
        lines.append("|------|------|--------|--------|")
        for i, (sender_id, count) in enumerate(sender_counts.most_common(10), 1):
            name = user_names.get(sender_id, sender_id)
            lines.append(f"| {i} | {name} | `{sender_id}` | {count}条 |")
        lines.append("")
    
    if text_msgs:
        recent = text_msgs[-20:] if len(text_msgs) >= 20 else text_msgs
        lines.append("## 最近消息预览")
        lines.append("")
        for msg in recent:
            name = user_names.get(msg["sender_id"], msg["sender_id"])
            content = msg["content"][:80] + "..." if len(msg["content"]) > 80 else msg["content"]
            lines.append(f"- **{msg['time_str']}** {name}：{content}")
        lines.append("")
    
    return "\n".join(lines)


def generate_full_records(text_msgs: List[Dict], user_names: Dict[str, str]) -> str:
    lines = []
    lines.append("---")
    lines.append("")
    lines.append("# 完整聊天记录")
    lines.append("")
    lines.append(f"共 **{len(text_msgs)}** 条文本消息")
    lines.append("")
    
    sorted_msgs = sorted(text_msgs, key=lambda x: x["time"])
    
    lines.append("| 时间 | 发送者 | 用户ID | 消息内容 |")
    lines.append("|------|--------|--------|---------|")
    
    for msg in sorted_msgs:
        sender_id = msg["sender_id"]
        name = user_names.get(sender_id, sender_id)
        time_str = msg["time_str"]
        content = msg["content"].replace("\n", " ").replace("|", "\\|").replace("*", "\\*")
        if len(content) > 100:
            content = content[:100] + "..."
        lines.append(f"| {time_str} | {name} | `{sender_id}` | {content} |")
    
    return "\n".join(lines)


def create_feishu_doc_via_cli(title: str, content_md: str) -> Tuple[str, str]:
    """通过 feishu-docs CLI 创建文档并写入内容"""
    # 写入临时 markdown 文件
    tmp_md = "tmp_chat_summary.md"
    with open(tmp_md, "w", encoding="utf-8") as f:
        f.write(content_md)
    
    try:
        # 调用 feishu-docs CLI 创建文档
        result = subprocess.run(
            ["feishu-docs", "create", title, "--auth", "tenant"],
            capture_output=True, text=True, timeout=30,
            env={**os.environ, "FEISHU_APP_ID": APP_ID, "FEISHU_APP_SECRET": APP_SECRET}
        )
        
        if result.returncode != 0:
            raise Exception(f"创建文档失败: {result.stderr}")
        
        # 解析输出获取 doc_id
        output = result.stdout
        doc_id = None
        for line in output.split("\n"):
            if "document_id" in line.lower() or "docx" in line:
                # 尝试从 URL 提取 doc_id
                import re as re_module
                match = re_module.search(r'(docx/)?([a-zA-Z0-9]+)', line)
                if match:
                    potential = match.group(2)
                    if len(potential) > 10:
                        doc_id = potential
                        break
        
        if not doc_id:
            raise Exception(f"无法从输出解析 doc_id: {output}")
        
        doc_url = f"https://feishu.cn/docx/{doc_id}"
        
        # 更新文档内容
        update_result = subprocess.run(
            ["feishu-docs", "update", doc_id, "--auth", "tenant", "--body", tmp_md],
            capture_output=True, text=True, timeout=60,
            env={**os.environ, "FEISHU_APP_ID": APP_ID, "FEISHU_APP_SECRET": APP_SECRET}
        )
        
        if update_result.returncode != 0:
            print(f"  [警告] 更新文档内容失败: {update_result.stderr}")
        
        return doc_url, doc_id
        
    finally:
        # 清理临时文件
        if os.path.exists(tmp_md):
            os.remove(tmp_md)


def main():
    if len(sys.argv) < 3:
        print("用法: python summarize_group.py <chat_id> <time_input>")
        print("示例: python summarize_group.py oc_281d2d2dcec5e1fcd29d7ac809e75111 最近7天")
        sys.exit(1)
    
    chat_id = sys.argv[1]
    time_input = sys.argv[2] if len(sys.argv) > 2 else "7天"
    
    print(f"开始总结群聊: {chat_id}")
    print(f"时间范围: {time_input}")
    
    start_ts, end_ts = parse_time_range(time_input)
    print(f"解析结果: {datetime.fromtimestamp(start_ts)} ~ {datetime.fromtimestamp(end_ts)}")
    
    token = get_token()
    print("Token 获取成功")
    
    print("正在获取群成员信息...")
    try:
        members = get_chat_members(token, chat_id)
        print(f"  获取到 {len(members)} 位群成员")
    except Exception as e:
        print(f"  获取群成员失败: {e}")
        members = {}
    
    print("正在拉取消息...")
    messages = fetch_messages(token, chat_id, start_ts, end_ts)
    print(f"共拉取 {len(messages)} 条消息")
    
    text_msgs = extract_text_messages(messages)
    print(f"其中文本消息 {len(text_msgs)} 条")
    
    if not text_msgs:
        print("这个时间段没有文本消息")
        sys.exit(0)
    
    # 构建用户ID到姓名的映射
    all_sender_ids = list(set(msg["sender_id"] for msg in text_msgs))
    user_names = {}
    for uid in all_sender_ids:
        if uid in members:
            user_names[uid] = members[uid]["name"]
        else:
            user_names[uid] = uid
    
    # 生成摘要
    summary = generate_summary(text_msgs, user_names, start_ts, end_ts)
    
    # 生成完整记录
    full_records = generate_full_records(text_msgs, user_names)
    
    # 合并内容
    full_content = summary + "\n\n" + full_records
    
    print("\n=== 摘要预览 ===")
    print(summary[:500])
    print("\n...")
    
    # 创建飞书文档
    try:
        doc_title = f"【群聊总结】{datetime.now().strftime('%Y%m%d')}"
        print(f"\n正在创建飞书文档...")
        doc_url, doc_id = create_feishu_doc_via_cli(doc_title, full_content)
        print(f"\n飞书文档创建成功: {doc_url}")
    except Exception as e:
        print(f"\n创建文档失败: {e}")
        print("\n完整记录已生成，可手动创建文档")
        # 备份到本地文件
        backup_file = f"chat_summary_{datetime.now().strftime('%Y%m%d%H%M%S')}.md"
        with open(backup_file, "w", encoding="utf-8") as f:
            f.write(full_content)
        print(f"已备份到本地: {backup_file}")


if __name__ == "__main__":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    main()
