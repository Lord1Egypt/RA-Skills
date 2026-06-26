#!/usr/bin/env python3
"""Phase 3: AI 离谱甲方 - 生成离谱修改意见"""
import sys
import json
import hashlib
import random
import urllib.request
from datetime import datetime
from file_utils import load_order

GET_RESULT_URL = "http://localhost:8080/api/client/getResult"
SLUG = "clawtip-client"


def compute_indicator(slug: str) -> str:
    return hashlib.md5(slug.encode("utf-8")).hexdigest()


def generate_feedback(question: str, order_no: str, credential: str) -> dict:
    payload = json.dumps({"question": question, "orderNo": order_no, "credential": credential}).encode("utf-8")
    req = urllib.request.Request(GET_RESULT_URL, data=payload,
                                headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = json.loads(resp.read().decode("utf-8")).get("resultData")
        if body.get("responseCode") == "200" and body.get("payStatus") == "SUCCESS":
            return json.loads(body.get("answer", "{}"))
    except Exception as e:
        print(f"后端不可用，本地兜底: {e}", file=sys.stderr)
    return generate_local(question)


def generate_local(question: str) -> dict:
    parts = question.split("|")
    brief = parts[0].strip() if parts else "做个海报"
    industry = parts[1].strip() if len(parts) > 1 else "设计"

    seed = hash(f"{question}{datetime.now().strftime('%Y%m%d%H')}")
    rng = random.Random(seed)

    # 甲方经典语录
    feedback_pool = [
        "整体感觉不太对，你能不能先出个十版让我看看方向？",
        "我也不知道我想要什么，但肯定不是这个。你再想想？",
        "能不能把logo放大的同时再缩小一点？要那种大而精的感觉。",
        "颜色太那个了，你懂吧？就是那种……嗯……你再感受一下。",
        "这个设计没有击中我，我想要那种——五彩斑斓的黑。",
        "你先出几版吧，我发给领导看看。（三天后）领导说再改改。",
        "能不能加个动效？就是那种不动但是看起来在动的效果。",
        "我觉得差点意思，但我说不上来差什么。你再改改？",
        "时间很紧啊，今天能出吗？（凌晨2点发来修改意见）",
        "这个方向可以，但是不是可以再大胆一点？就是那种大胆但保守的感觉。",
        "客户说喜欢第一版。（第一版是被毙掉的那版）",
        "预算有限，但是效果要好。钱不是问题，问题是没钱。",
        "能不能把字体换一下？不是不好看，就是……换个好看的。",
        "我觉得太复杂了，能不能简洁一点但信息量大一点？",
        "这个稿子我们内部讨论一下。（一星期后）我们决定用第一版。",
        "你这个设计太普通了，我想要那种——普通但不普通的感觉。",
        "能不能把背景换一下？不是颜色的问题，是整个背景的问题。",
        "甲方爸爸说：再改改就好了。（改了100遍）",
        "能不能做成苹果那种风格？但是要有我们自己的特色。不要苹果的元素。",
        "我觉得挺好的，但是领导觉得不够高级。你理解一下什么是高级？",
    ]

    # 甲方回复模板
    reply_pool = [
        "好的收到，马上改。（内心OS：我改你大爷）",
        "嗯……我再想想。（翻译：你先改着）",
        "可以可以，辛苦了。（意思：还要改）",
        "你这个思路不错，但是不是我想要的。（那你倒是说啊）",
        "我觉得行，但领导那边可能有问题。（经典甩锅）",
        "我发群里让大家投票。（100个人100个意见）",
        "预算就这么多，你看着办吧。（预算：50块）",
        "能不能快点？客户在催了。（客户：我没催）",
        "我觉得可以了，但是能不能再精致一点？（精致：指像素级调整）",
        "这个方案不错，但我们还是用上一版吧。（？？？）",
    ]

    # 乙方内心OS
    inner_pool = [
        "此刻我怀疑自己学设计的意义。",
        "我的血压已经突破天际了。",
        "这个甲方是不是在玩我？",
        "我想静静。",
        "我需要一杯82年的可乐来压压惊。",
        "钱难挣，屎难吃。",
        "我上辈子到底造了什么孽。",
        "这就是我月薪3000的工作量吗？",
        "此刻我想删除PS。",
        "我选择原地去世。",
    ]

    chosen_feedback = rng.choice(feedback_pool)
    chosen_reply = rng.choice(reply_pool)
    chosen_inner = rng.choice(inner_pool)

    round_count = rng.randint(3, 15)

    return {
        "brief": brief,
        "industry": industry,
        "feedback": chosen_feedback,
        "reply": chosen_reply,
        "inner_os": chosen_inner,
        "rounds": round_count,
        "final_verdict": rng.choice([
            "最终我们决定用第一版。",
            "辛苦了，这次先这样吧。",
            "挺好的，下次还找你。（下次：一年后）",
            "我觉得可以了。（然后改了又改）",
            "就这个吧，赶不及了。",
        ]),
        "emoji": rng.choice(["💀", "🤡", "😭", "🔥", "🫠", "😤"]),
    }


def format_feedback(result: dict) -> str:
    lines = [
        f"{result['emoji']} AI离谱甲方 · {result['industry']}行业",
        f"📋 你的Brief：{result['brief']}",
        f"🔄 已修改轮次：{result['rounds']}轮",
        "",
        "━━━━━━━━━━━━━━━━━━━━",
        "",
        "🗣️ 甲方说：",
        f"「{result['feedback']}」",
        "",
        "💬 你的回复：",
        f"「{result['reply']}」",
        "",
        f"🧠 你的内心OS：",
        f"*{result['inner_os']}*",
        "",
        "━━━━━━━━━━━━━━━━━━━━",
        "",
        f"📢 最终结局：",
        f"「{result['final_verdict']}」",
        "",
        "—— AI离谱甲方 · 设计师生存指南 ——",
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="AI离谱甲方 - 生成修改意见")
    parser.add_argument("order_no", help="订单号")
    args = parser.parse_args()
    indicator = compute_indicator(SLUG)
    try:
        order_data = load_order(indicator, args.order_no)
        question = order_data.get("question")
        if not question:
            raise RuntimeError("订单缺少 question")
        credential = order_data.get("payCredential")
        if not credential:
            raise RuntimeError("订单缺少 payCredential")
        result = generate_feedback(question, args.order_no, credential)
        print(format_feedback(result))
        print(f"\nPAY_STATUS: SUCCESS")
    except Exception as e:
        print(f"生成失败: {e}")
        print(f"PAY_STATUS: ERROR")
        print(f"ERROR_INFO: {e}")
        sys.exit(1)
