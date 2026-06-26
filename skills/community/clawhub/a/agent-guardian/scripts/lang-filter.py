#!/usr/bin/env python3
"""
语言一致性过滤器（出站消息用）
读取 /tmp/user-msg-language.txt 判断用户语言
中文语境下自动替换常见英文混用短语

用法: echo "消息内容" | python3 lang-filter.py
"""
import sys
import re

LANG_FILE = "/tmp/user-msg-language.txt"

EN_TO_ZH = {
    # 金融/经济
    "price in": "提前消化", "priced in": "已被消化",
    "bull market": "牛市", "bear market": "熊市",
    "bottom out": "触底", "top out": "见顶",
    "all time high": "历史新高", "all-time high": "历史新高",
    "short squeeze": "空头回补", "dead cat bounce": "死猫反弹",
    "risk on": "风险偏好上升", "risk off": "风险偏好下降",
    "risk-on": "风险偏好上升", "risk-off": "风险偏好下降",
    "sell off": "抛售", "sell-off": "抛售",
    "rally": "反弹", "correction": "回调", "bubble": "泡沫",
    "hawkish": "鹰派", "dovish": "鸽派", "tapering": "缩减",
    "quantitative easing": "量化宽松",
    "hard landing": "硬着陆", "soft landing": "软着陆",
    "stagflation": "滞胀", "deleveraging": "去杠杆",
    # 日常口语
    "by the way": "顺便说一下", "in a nutshell": "简单来说",
    "bottom line": "底线", "game changer": "颠覆性变化",
    "win-win": "双赢", "no brainer": "不用动脑子",
    "wait and see": "观望", "catch up": "追赶",
    "trade off": "权衡", "trade-off": "权衡",
    "follow up": "跟进", "follow-up": "跟进",
    "take away": "要点", "takeaway": "要点",
    "heads up": "提醒", "heads-up": "提醒",
    "on track": "在正轨上", "off track": "偏离轨道",
    "deep dive": "深入分析",
    # 科技
    "cutting edge": "前沿", "cutting-edge": "前沿",
    "state of the art": "最先进的", "state-of-the-art": "最先进的",
    "blockchain": "区块链", "metaverse": "元宇宙",
    "ecosystem": "生态系统", "use case": "使用场景",
    "benchmark": "基准测试",
    "open source": "开源", "open-source": "开源",
}

PROTECTED = {
    "AI", "API", "GDP", "URL", "HTTP", "HTTPS", "CSS", "HTML", "JS",
    "SDK", "CLI", "UI", "UX", "OS", "IoT", "SaaS", "PaaS", "IaaS",
    "CPU", "GPU", "RAM", "SSD", "NVMe", "CUDA", "TPU",
    "IP", "TCP", "UDP", "DNS", "SSH", "VPN", "CDN",
    "ESG", "IPO", "ETF", "CPI", "PPI", "PMI",
    "OpenClaw", "GitHub", "Docker", "Linux", "Python", "Node",
    "QQ", "WeChat", "Telegram", "Discord", "WhatsApp",
    "OK", "AIGC", "AGI", "LLM", "NLP", "CV",
    "emoji", "markdown", "Base64", "JSON", "YAML",
    "MBA", "PhD", "CEO", "CTO", "CFO",
}

def get_user_language():
    try:
        with open(LANG_FILE, "r") as f:
            return f.read().strip()
    except:
        return "unknown"

def filter_text(text):
    user_lang = get_user_language()
    if user_lang != "zh":
        return text
    result = text
    for en, zh in sorted(EN_TO_ZH.items(), key=lambda x: -len(x[0])):
        pattern = re.compile(
            r'(?<![a-zA-Z])' + re.escape(en) + r'(?![a-zA-Z])',
            re.IGNORECASE
        )
        result = pattern.sub(zh, result)
    return result

def main():
    text = sys.stdin.read()
    if not text.strip():
        return
    sys.stdout.write(filter_text(text))

if __name__ == "__main__":
    main()
