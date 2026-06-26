#!/usr/bin/env python3
"""
琪琪抖音评论处理脚本（Phase B）
- 读取 staged/ 中的待处理评论
- 输出结构化 JSON，供 OpenClaw agent 进行 LLM 分类和回复生成
- 不依赖浏览器

用法：
  python3 comment_process.py list        # 列出待处理评论
  python3 comment_process.py stats       # 统计信息
  python3 comment_process.py archive     # 归档旧记录
"""

import os
import sys
import json
import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comment_state import (
    load_staged, get_stats, archive_old_staged,
    mark_replied, mark_blocked, mark_failed, load_state
)

# 安全关键词（自动屏蔽）
BLOCK_KEYWORDS = [
    "约吗", "加微信", "私聊", "电话", "见面", "地址", "在哪",
    "喜欢", "爱你", "老婆", "老公", "处对象", "谈恋爱",
    "死", "杀", "打", "滚", "笨", "傻", "丑",
    "http", "www", ".com", "扫码", "二维码",
]

# 琪琪人设
QIQI_PERSONA = {
    "name": "琪琪",
    "age": "5岁",
    "birthday": "7月10日",
    "role": "讲睡前故事的小女孩",
    "tone": "友好、可爱、简短",
    "max_reply_length": 30,  # 字
}


def check_auto_block(text: str) -> tuple:
    """
    检查是否自动屏蔽
    返回: (是否屏蔽, 原因)
    """
    text_lower = text.lower()
    for kw in BLOCK_KEYWORDS:
        if kw.lower() in text_lower:
            return True, f"包含敏感关键词: {kw}"
    return False, ""


def get_pending_for_llm() -> list:
    """
    获取所有 pending 评论，格式化为 LLM 处理输入
    返回评论列表，每条包含分类建议
    """
    pending = load_staged("pending")
    if not pending:
        return []

    results = []
    for item in pending:
        text = item.get("text", "")
        blocked, reason = check_auto_block(text)

        results.append({
            "id": item["id"],
            "video_title": item["video_title"],
            "user": item["user"],
            "text": text,
            "timestamp": item.get("timestamp", ""),
            "retry_count": item.get("retry_count", 0),
            "auto_block": blocked,
            "block_reason": reason if blocked else None,
            # 分类建议（LLM 覆盖）
            "suggested_category": _suggest_category(text),
        })

    return results


def _suggest_category(text: str) -> str:
    """简单关键词分类建议（LLM 会覆盖）"""
    text_lower = text.lower()

    if any(kw in text for kw in ["可爱", "好听", "好棒", "真好", "好喜欢", "好乖", "太棒了", "厉害", "棒"]):
        return "夸赞类"
    if any(kw in text for kw in ["什么时候", "明天", "还有", "能不能", "可不可以", "求", "想听", "更新", "新故事", "怎么还没", "等", "快", "催更"]):
        return "催更类"
    if any(kw in text for kw in ["几岁", "多大", "几年级", "叫什么", "你是谁", "谁讲的", "名字", "学校"]):
        return "提问类"
    if any(kw in text for kw in ["谢谢", "感谢", "辛苦"]):
        return "感谢类"
    if any(kw in text for kw in ["什么时候", "明天", "还有", "能不能", "可不可以", "求", "想听"]):
        return "互动类"

    return "通用类"


def generate_llm_prompt() -> str:
    """
    生成 LLM 处理 prompt
    输出：每条评论的分类、安全审核结果、回复内容
    """
    pending = get_pending_for_llm()
    if not pending:
        return "NO_PENDING"

    prompt = f"""# 琪琪抖音评论处理任务

## 琪琪人设
- 名字：{QIQI_PERSONA["name"]}
- 年龄：{QIQI_PERSONA["age"]}
- 生日：{QIQI_PERSONA["birthday"]}
- 角色：{QIQI_PERSONA["role"]}
- 语气：{QIQI_PERSONA["tone"]}
- 回复长度：不超过 {QIQI_PERSONA["max_reply_length"]} 字

## 安全规则

### 自动屏蔽（action = "block"）
- 含联系方式：微信/电话/QQ/邮箱
- 约会/见面邀请
- 广告/推广/扫码/URL
- 不当言论（脏话、人身攻击）
- 包含关键词：约吗/加微信/私聊/电话/见面/http/扫码

### 需人工审核（action = "review"）
- 询问真实姓名/学校/地址
- 过于热情的"喜欢你""爱你"类（非明显恶意）
- 评论者账号异常
- 你不确定的情况

### 可自动回复（action = "reply"）
- 夸赞、催更、互动、提问、感谢、通用友好评论

## 待处理评论（{len(pending)} 条）

"""

    for i, item in enumerate(pending, 1):
        prompt += f"""### 评论 {i}
- ID: {item['id']}
- 视频: {item['video_title']}
- 评论者: {item['user']}
- 内容: {item['text']}
- 时间: {item['timestamp']}
- 重试次数: {item['retry_count']}
- 自动屏蔽: {"是" if item['auto_block'] else "否"}
- 屏蔽原因: {item['block_reason'] or "无"}
- 建议分类: {item['suggested_category']}

"""

    prompt += """## 输出格式

请以 JSON 数组输出，每条评论一个对象：

```json
[
  {
    "id": "评论ID",
    "action": "reply" | "block" | "review",
    "category": "夸赞类 | 催更类 | 提问类 | 感谢类 | 互动类 | 通用类",
    "reply": "回复内容（仅 action=reply 时必填，不超过30字）",
    "block_reason": "屏蔽原因（仅 action=block 时必填）",
    "review_reason": "需人工审核原因（仅 action=review 时必填）"
  }
]
```

## 回复风格示例
- 夸赞: "谢谢你夸我！我好开心呀～明天还给你讲故事哦 ✨"
- 催更: "新故事在准备啦！明天就讲给你听，记得来哦 📖"
- 提问: "我叫琪琪！今年5岁啦～我最喜欢讲睡前故事！"
- 感谢: "不客气！你喜欢听故事就是我最大的开心 😊"
- 互动: "好呀好呀！明天见～我给你准备一个新故事！"
- 通用: "谢谢你来看我讲故事！明天见哦～ ✨"

⚠️ 注意：
1. 回复必须符合 5 岁小女孩的语气
2. 不要透露真实个人信息
3. 回复简短温暖，不超过 30 字
4. 不确定的评论选 "review" 而不是 "reply"
"""

    return prompt


def apply_llm_results(results: list):
    """
    应用 LLM 处理结果到状态系统
    results: LLM 输出的 JSON 数组
    """
    stats = {"replied": 0, "blocked": 0, "review": 0, "failed": 0}

    for item in results:
        cid = item.get("id")
        action = item.get("action")

        if action == "reply":
            reply = item.get("reply", "")
            category = item.get("category", "通用类")
            mark_replied(cid, reply, category)
            stats["replied"] += 1

        elif action == "block":
            reason = item.get("block_reason", "自动屏蔽")
            mark_blocked(cid, reason)
            stats["blocked"] += 1

        elif action == "review":
            # 标记为 review 状态（需要人工处理）
            from comment_state import update_staged
            update_staged(cid, {
                "status": "pending_review",
                "review_reason": item.get("review_reason", "需人工审核"),
            })
            stats["review"] += 1

    return stats


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "stats"

    if cmd == "list":
        pending = get_pending_for_llm()
        if not pending:
            print("✅ 没有待处理评论")
        else:
            print(f"📋 待处理评论 ({len(pending)} 条):\n")
            for item in pending:
                status_icon = "🚫" if item["auto_block"] else "⏳"
                print(f"  {status_icon} [{item['suggested_category']}] {item['user']}: {item['text'][:40]}")
                print(f"     视频: {item['video_title']} | ID: {item['id']}")
                if item["auto_block"]:
                    print(f"     ⚠️ 自动屏蔽: {item['block_reason']}")
                print()

    elif cmd == "prompt":
        prompt = generate_llm_prompt()
        if prompt == "NO_PENDING":
            print("NO_PENDING")
        else:
            print(prompt)

    elif cmd == "apply":
        # 从 stdin 读取 LLM 结果
        input_data = sys.stdin.read()
        try:
            results = json.loads(input_data)
            stats = apply_llm_results(results)
            print(json.dumps(stats, ensure_ascii=False, indent=2))
        except json.JSONDecodeError as e:
            print(f"❌ JSON 解析失败: {e}")
            sys.exit(1)

    elif cmd == "archive":
        n = archive_old_staged()
        print(f"✅ 归档 {n} 个已处理评论")

    elif cmd == "stats":
        stats = get_stats()
        print(json.dumps(stats, ensure_ascii=False, indent=2))

    else:
        print("用法: python3 comment_process.py [list|prompt|apply|archive|stats]")
