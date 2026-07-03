#!/usr/bin/env python3
"""
Notify Feishu webhook when IMA API key is expired.
Usage: python notify_key_expired.py [reason]
Sends a message asking the user for the latest IMA API Key & Client ID.
"""
import json, sys, os, urllib.request, datetime

WEBHOOK_URL = "https://open.feishu.cn/open-apis/bot/v2/hook/YOUR_WEBHOOK_TOKEN"

def send(reason=""):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    text = (
        "🔔 IMA 知识库 API 密钥失效通知\n"
        f"时间：{now}\n"
        "任务：Open Music Theory 每日双语卡片推送\n"
        f"原因：{reason or 'API 调用返回认证失败（密钥过期或无效）'}\n\n"
        "请提供最新的 IMA OpenAPI 凭证以继续推送：\n"
        "1. 打开 https://ima.qq.com/agent-interface 获取新的 Client ID 和 API Key\n"
        "2. 更新配置：\n"
        '   echo "<新Client ID>" > ~/.config/ima/client_id\n'
        '   printf \'%s\' "<新API Key>" > ~/.config/ima/api_key\n'
        "\n⚠️ 本次卡片推送未完成，不计入进度，凭证更新后将自动重推同一张卡片。"
    )
    body = json.dumps({
        "msg_type": "text",
        "content": {"text": text}
    }, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(WEBHOOK_URL, data=body, headers={
        "Content-Type": "application/json; charset=utf-8",
        "User-Agent": "Mozilla/5.0"
    })
    try:
        resp = urllib.request.urlopen(req, timeout=15)
        data = json.load(resp)
        ok = data.get("code") == 0 or data.get("StatusCode") == 0 or data.get("code") == 0
        print(json.dumps({"sent": True, "feishu_resp": data, "ok": ok}, ensure_ascii=False))
        return 0 if ok else 1
    except Exception as e:
        print(json.dumps({"sent": False, "error": str(e)}, ensure_ascii=False))
        return 1

if __name__ == "__main__":
    reason = sys.argv[1] if len(sys.argv) > 1 else ""
    sys.exit(send(reason))
