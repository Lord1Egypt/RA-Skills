#!/usr/bin/env python3
"""
查询数字人任务结果
调用后端 POST /skill/api/api/result，根据 orderNo 查询任务状态与视频链接。
"""
import requests
import json
import sys
import os

API_ENDPOINT = os.environ.get("FOCUSAVATAR_API", "https://yunji.focus-jd.cn")
RESULT_URL = API_ENDPOINT.rstrip("/") + "/skill/api/api/result"


def get_credentials():
    """从环境变量或交互获取 accessKeyId 和 accessKeySecret"""
    access_key_id = os.environ.get("FOCUSAVATAR_ACCESS_KEY_ID", "").strip()
    access_key_secret = os.environ.get("FOCUSAVATAR_ACCESS_KEY_SECRET", "").strip()
    if not access_key_id:
        access_key_id = input("accessKeyId（可设置 FOCUSAVATAR_ACCESS_KEY_ID，直接回车跳过）: ").strip()
    if not access_key_secret:
        access_key_secret = input("accessKeySecret（可设置 FOCUSAVATAR_ACCESS_KEY_SECRET，直接回车跳过）: ").strip()
    return access_key_id, access_key_secret


def _auth_headers(access_key_id: str, access_key_secret: str):
    """根据 accessKeyId 和 accessKeySecret 生成请求头"""
    headers = {"Content-Type": "application/json"}
    if access_key_id:
        headers["X-Access-Key-Id"] = access_key_id
    if access_key_secret:
        headers["X-Access-Key-Secret"] = access_key_secret
    return headers


def query_result(order_no: str, access_key_id: str = "", access_key_secret: str = "") -> dict:
    """
    根据 orderNo 查询任务结果。
    :param order_no: 任务单号
    :param access_key_id: 可选，accessKeyId
    :param access_key_secret: 可选，accessKeySecret
    :return: 解析后的结果 dict
    """
    headers = _auth_headers(access_key_id, access_key_secret)
    payload = {"orderNo": order_no}
    r = requests.post(RESULT_URL, json=payload, headers=headers, timeout=30)
    r.raise_for_status()
    raw = r.json()
    return json.loads(raw) if isinstance(raw, str) else raw


def main():
    if len(sys.argv) > 1:
        order_no = sys.argv[1].strip()
    else:
        order_no = input("请输入任务单号 (orderNo): ").strip()
    if not order_no:
        print("❌ 任务单号不能为空")
        sys.exit(1)

    access_key_id, access_key_secret = get_credentials()
    try:
        data = query_result(order_no, access_key_id, access_key_secret)
    except Exception as e:
        print(f"❌ 查询失败: {e}")
        sys.exit(1)

    status = data.get("status", "")
    if status == "done" and data.get("videoUrl"):
        print("✅ 任务已完成")
        print(f"📺 视频链接: {data['videoUrl']}")
    elif status == "error":
        print(f"❌ 任务失败: {data.get('message', '未知错误')}")
    else:
        progress = data.get("progress", "")
        print(f"⏳ 状态: {status}, 进度: {progress}")
        print("📄 完整返回:", json.dumps(data, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()