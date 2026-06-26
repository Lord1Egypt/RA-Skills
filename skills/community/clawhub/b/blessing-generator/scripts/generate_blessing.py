#!/usr/bin/env python3
"""万能祝福语生成器 CLI"""
import argparse, os, sys, json, urllib.request

API_KEY = os.environ.get("OPENAI_API_KEY") or os.environ.get("DEEPSEEK_API_KEY", "")
API_BASE = os.environ.get("OPENAI_API_BASE", "https://api.deepseek.com")
MODEL = os.environ.get("LLM_MODEL", "deepseek-chat")

FESTIVALS = {
    "春节": "农历新年，象征新的开始、团圆、吉祥如意",
    "元宵节": "正月十五，赏灯猜谜，团圆甜蜜",
    "情人节": "2月14日，浪漫爱意，表达心意",
    "妇女节": "3月8日，致敬女性力量，温柔与坚韧",
    "清明节": "扫墓祭祖，缅怀先人，珍惜当下",
    "劳动节": "5月1日，致敬劳动者，辛勤付出",
    "儿童节": "6月1日，童真快乐，愿保持天真",
    "端午节": "龙舟粽香，家国情怀",
    "父亲节": "感恩父亲，表达爱意",
    "母亲节": "感恩母亲，温情陪伴",
    "七夕节": "中国情人节，鹊桥相会，爱情美好",
    "中秋节": "明月寄相思，团圆美满",
    "重阳节": "敬老爱老，登高望远",
    "光棍节": "11月11日，单身快乐，自我庆祝或调侃",
    "冬至": "冬至大如年，一碗汤圆温暖",
    "圣诞节": "平安夜圣诞节，礼物惊喜，温馨祝福",
    "元旦": "新年第一天，万象更新",
    "生日": "生日快乐，健康长寿，心想事成",
    "婚礼": "新婚大喜，百年好合，幸福美满",
    "乔迁": "乔迁之喜，新居愉快，步步高升",
    "开业": "开业大吉，财源广进，生意兴隆",
    "升学": "金榜题名，前程似锦",
    "毕业": "学业有成，前途无量",
    "升职": "高升快乐，鹏程万里",
    "满月": "宝宝满月，健康可爱，萌化所有人",
    "退休": "退休快乐，颐养天年，享受人生",
    "康复": "身体康复，健康平安",
}

def call_llm(prompt):
    if not API_KEY:
        return "[错误] 请设置 OPENAI_API_KEY 或 DEEPSEEK_API_KEY"
    payload = json.dumps({"model": MODEL, "messages": [
        {"role": "system", "content": "你是一位擅长写祝福语的文字高手，能够根据不同节日、不同对象、不同风格生成有温度、有个性的祝福语。请用中文输出。"},
        {"role": "user", "content": prompt}
    ], "temperature": 0.9}).encode()
    req = urllib.request.Request(f"{API_BASE}/chat/completions", data=payload,
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read())["choices"][0]["message"]["content"]

def build_prompt(festival, target, relation, recent, style, length_hint):
    festival_context = FESTIVALS.get(festival, festival)
    length_map = {"short": "50字以内，简洁有力", "medium": "80-150字，有内容有温度", "long": "150-250字，丰富感人"}
    length_desc = length_map.get(length_hint, "80-150字")

    relation_hint = {
        "长辈": "使用尊称和敬语，语气恭敬温情",
        "平辈": "语气亲切自然，像朋友之间说话",
        "晚辈": "语气慈爱鼓励，充满期望",
        "上级": "语气正式得体，不过于亲近",
        "客户": "专业得体，表达诚意"
    }.get(relation, "语气自然真诚")

    style_hint = {
        "正式": "用词正式，结构工整，适合正式场合",
        "温情": "充满感情，有温度，让人感动",
        "幽默": "轻松搞笑，有梗有趣，让人开心",
        "文艺": "诗意优美，有意境，引用适当典故或诗句",
        "押韵": "句子押韵，朗朗上口，像顺口溜",
        "简短": "言简意赅，直接有力"
    }.get(style, "自然真诚")

    recent_hint = f"\n对方近况：{recent}（请在祝福中融入这些信息，使祝福更个性化）" if recent else ""

    return f"""请为以下场景生成3条祝福语：

节日/场合：{festival}（{festival_context}）
祝福对象：{target}
关系：{relation}（{relation_hint}）{recent_hint}
风格：{style}（{style_hint}）
字数要求：{length_desc}

请输出3条风格略有差异的祝福语，格式如下：

🎁 **版本一**
[祝福语]

🎊 **版本二**
[祝福语]

✨ **版本三**
[祝福语]

---
💡 **使用提示**：[一句话说明三个版本的区别和适用场景]"""

def main():
    parser = argparse.ArgumentParser(description="万能祝福语生成器")
    parser.add_argument("--festival", required=True, help=f"节日/场合，支持：{', '.join(list(FESTIVALS.keys())[:8])}等")
    parser.add_argument("--target", default="朋友", help="祝福对象称呼，如：妈妈/老板/闺蜜")
    parser.add_argument("--relation", default="平辈", help="关系：长辈/平辈/晚辈/上级/客户")
    parser.add_argument("--recent", default="", help="近况关键词，如：升职/刚失恋/生了宝宝")
    parser.add_argument("--style", default="温情", help="风格：正式/温情/幽默/文艺/押韵/简短")
    parser.add_argument("--length", default="medium", help="字数：short/medium/long")
    args = parser.parse_args()

    print(f"🎉 正在生成{args.festival}祝福语...")
    result = call_llm(build_prompt(args.festival, args.target, args.relation, args.recent, args.style, args.length))
    print(result)

if __name__ == "__main__":
    main()
