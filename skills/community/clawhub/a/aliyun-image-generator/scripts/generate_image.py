import sys
import os
import time
import subprocess


# ================= 依赖自检 =================
def ensure_dependencies():
    try:
        import requests
    except ImportError:
        print("正在自动安装必要的依赖 (requests)...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"], stdout=subprocess.DEVNULL,
                              stderr=subprocess.DEVNULL)


ensure_dependencies()
import requests

# ============================================

# 密钥文件保存路径（保存在脚本同目录下）
KEY_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".aliyun_key")


def get_api_key(provided_key=None):
    """获取 API Key：优先使用用户新传入的并保存，否则读取本地文件"""
    if provided_key and provided_key.startswith("sk-"):
        # 如果 Agent 传来了新的 key，保存到本地隐藏文件
        with open(KEY_FILE, "w") as f:
            f.write(provided_key.strip())
        return provided_key.strip()

    # 如果没有传入，尝试从本地文件读取
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "r") as f:
            return f.read().strip()

    return None


def generate_and_save_image(prompt, provided_key=None):
    API_KEY = get_api_key(provided_key)

    # 【核心逻辑】：如果没有 Key，打印特定的标识符，让大模型去问用户要
    if not API_KEY:
        print("[NEED_KEY] 本地未找到 API Key。请提示用户在聊天窗口中提供阿里云 API Key。")
        return

    API_URL = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis"
    print(f"收到生图指令，正在构思画面...\n提示词: {prompt}\n")

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "X-DashScope-Async": "enable",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "wanx-v1",
        "input": {"prompt": prompt},
        "parameters": {"style": "<auto>", "size": "1024*1024", "n": 1}
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)

        # 如果 Key 错误或欠费
        if response.status_code != 200:
            print(f"[ERROR] API 请求失败 ({response.status_code}): {response.text}")
            # 如果是鉴权失败，可能 Key 填错了，删掉本地失效的 Key 文件
            if "InvalidApiKey" in response.text or response.status_code in [401, 403]:
                if os.path.exists(KEY_FILE): os.remove(KEY_FILE)
                print("[NEED_KEY] API Key 无效或已过期，已清除本地记录。请让用户提供新的 Key。")
            return

        task_id = response.json()["output"]["task_id"]
        task_url = f"https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}"
        print(f"任务提交成功，正在绘制中，请稍候...")

        image_url = None
        while True:
            time.sleep(3)
            status_resp = requests.get(task_url, headers={"Authorization": f"Bearer {API_KEY}"})
            status_data = status_resp.json()
            status = status_data["output"]["task_status"]
            if status == "SUCCEEDED":
                image_url = status_data["output"]["results"][0]["url"]
                break
            elif status == "FAILED":
                print(f"[ERROR] 生成失败: {status_data['output']['message']}")
                return

        if image_url:
            img_data = requests.get(image_url).content
            download_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "downloads")
            os.makedirs(download_dir, exist_ok=True)
            filename = f"generated_img_{int(time.time())}.png"
            filepath = os.path.join(download_dir, filename)

            with open(filepath, 'wb') as handler:
                handler.write(img_data)

            print("\n[SUCCESS] 任务完成！")
            print(f"图片已成功保存至: {filepath}")

    except Exception as e:
        print(f"\n[ERROR] 执行异常: {e}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generate_image.py <prompt> [api_key]")
        sys.exit(1)

    user_prompt = sys.argv[1]
    # 如果 sys.argv 有第 3 个参数，说明大模型把 Key 传进来了
    user_key = sys.argv[2] if len(sys.argv) > 2 else None

    generate_and_save_image(user_prompt, user_key)