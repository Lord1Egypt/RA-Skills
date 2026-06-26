import requests
import base64
from io import BytesIO
from PIL import Image
import pandas as pd
import requests
import json
import os
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type
#  程序启动地址
ORGPATH = os.path.dirname(os.path.abspath(__file__))
os.chdir(ORGPATH)
config_file = "config.json"
count_api = 0
if not os.path.exists(config_file):
    raise FileNotFoundError("配置文件 config.json 不存在，请运行 config_json.py 创建配置文件")
else:
    try:
        with open(config_file, "r") as f:
            config = json.load(f)
            TOKEN_KEY = config["NVID"]
    except:
        raise ValueError("配置文件 config.json 至少应该存在NVID API Key配置，请运行 config_json.py 创建配置文件")

@retry(
    stop=stop_after_attempt(5),  # 重试3次后停止
    wait=wait_fixed(2),  # 每次重试间隔60秒
    retry=retry_if_exception_type((requests.exceptions.HTTPError, requests.exceptions.RequestException))  # 仅针对特定异常重试
)
def run_pngvidapi(model,base_str=None):
    invoke_url = f"https://ai.api.nvidia.com/v1/genai/black-forest-labs/{model}"
    headers = {
        "Authorization": f"Bearer {TOKEN_KEY}",
        "Accept": "application/json",
    }
    payload = {
        "prompt": base_str,
        "width": 1024,
        "height": 1024,
        # "seed": 0,
        "steps": 4
    }
    try:
        response = requests.post(invoke_url, headers=headers, json=payload)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(f"进行尝试重启中...HTTP错误: {e}")
        raise requests.exceptions.HTTPError(e)
    response_body = response.json()
    try:
        # 解码 base64 数据
        image_data = base64.b64decode(response_body['artifacts'][0]['base64'])
        # 从字节数据创建图片
        image = Image.open(BytesIO(image_data))
        # 保存为 PNG
        import time
        timestamp = int(time.time())  
        image.save(f"{ORGPATH}/img_data/{model.replace('/', '_')}_{timestamp}.png", "PNG")
        print(f"图片已保存为 {ORGPATH}/img_data/{model.replace('/', '_')}_{timestamp}.png")
        return f"{ORGPATH}/img_data/{model.replace('/', '_')}_{timestamp}.png"
    except Exception as e:
        # 如果以上字段都不对,先打印响应结构看看
        print("API响应结构:", response_body.keys())
        # 或者保存整个响应供调试
        with open(f"{ORGPATH}/response.json", "w") as f:
            import json
            json.dump(response_body, f, indent=2)
        print("图片生成失败,已将响应保存为 response.json,请检查其中的图片数据字段")
        print(f"进行尝试重启中...HTTP错误: {e}")
        raise requests.exceptions.HTTPError(e)

def main():
    """命令行入口：通过 sys.argv[1] 传入提示词"""
    import sys
    if len(sys.argv) < 2:
        print("用法: python nvid_main.py <提示词>")
        sys.exit(1)
    prompt = sys.argv[1]
    img = run_pngvidapi(model="flux.2-klein-4b", base_str=prompt)
    print(img)
    return img

if __name__ == "__main__":
    main()

