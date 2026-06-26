import sys
import requests
import os
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type
import numpy as np
import time
import json

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
            TOKEN_KEY = config["SILICONFLOW"]
    except:
        raise ValueError("配置文件 config.json 至少应该存在SiliconFlow API Key配置，请运行 config_json.py 创建配置文件")

def post_gui(payload,key):
    url = "https://api.siliconflow.cn/v1/images/generations"
    try:
        headers = {
            "Authorization": key,
            "Content-Type": "application/json"
        }
        response = requests.request("POST", url, json=payload, headers=headers)
        return response.json()
    except Exception as e:
        raise ValueError(f"请求失败：{e} {response}")


def nan_check(value):
    if value==np.nan or str(value)=="" or str(value)=="None"or value=="" or value is None:
        return True
    else:
        return False


def generate_png(model="Kwai-Kolors/Kolors",batch_size=1,num_inference_steps=20,guidance_scale=2.5,base_str=None,negative_prompt=None):
    """
    生成图片
    :param model: 模型名称，可选（Kwai-Kolors/Kolors、Qwen/Qwen-Image），默认值为Kwai-Kolors/Kolors
    :param batch_size: 批量大小，推荐值为1
    :param num_inference_steps: 推理步骤数，推荐值为20
    :param guidance_scale: 提示词之间的匹配度，推荐值为2.5
    :param base_str: 提示词，不能为空
    :param negative_prompt: 负提示词，可以为空
    :return: 图片列表
    """
    if nan_check(base_str):
        raise ValueError("提示词不能为空")
    payload = {
        "model": model,
        "prompt": base_str,
        "image_size": "1024x1024",
        "batch_size": batch_size,
        "num_inference_steps": num_inference_steps, #推理步骤数
        "guidance_scale": guidance_scale, #提示词之间的匹配度
        }
    if not nan_check(negative_prompt):
        payload["negative_prompt"] = negative_prompt
    try:
        response = post_gui(payload,key=f"Bearer {TOKEN_KEY}")
        img_list = []
        for i in range(len(response["images"])):
            image_url = response["images"][i]["url"]
            # 下载图片
            response_png = requests.get(image_url)
            # 根据时间编码命名图片 
            timestamp = int(time.time())  
            with open(f"{ORGPATH}/img_data/siliconflow_{model.replace('/', '_')}_{timestamp}.png", "wb") as f: 
                f.write(response_png.content)
            img_list.append(f"{ORGPATH}/img_data/siliconflow_{model.replace('/', '_')}_{timestamp}.png")
        print(f"图片已保存在: {img_list}")
        return img_list
    except Exception as e:
        print(f"生成图片失败：{e} 重试中...",time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))
        raise ValueError(f"生成图片失败：{e} {response}")

def main():
    """
    命令行入口，供其他 agent 调用
    用法: python siliconflow_main.py "<提示词>" ["<负面提示词>"] [--model <模型名>]
    负面提示词可省略
    模型可选: Kwai-Kolors/Kolors (默认), Qwen/Qwen-Image
    """
    if len(sys.argv) < 2:
        print("用法: python siliconflow_main.py <提示词> [负面提示词] [--model <模型名>]")
        sys.exit(1)

    model = "Kwai-Kolors/Kolors"
    base_str = None
    negative_prompt = None

    i = 1
    while i < len(sys.argv):
        if sys.argv[i] == "--model" and i + 1 < len(sys.argv):
            model = sys.argv[i + 1]
            i += 2
        elif base_str is None:
            base_str = sys.argv[i]
            i += 1
        else:
            negative_prompt = sys.argv[i]
            i += 1

    if base_str is None:
        print("用法: python siliconflow_main.py <提示词> [负面提示词] [--model <模型名>]")
        sys.exit(1)

    return generate_png(model=model, base_str=base_str, negative_prompt=negative_prompt)

if __name__ == "__main__":
    main()