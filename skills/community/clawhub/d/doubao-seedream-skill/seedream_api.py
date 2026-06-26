"""
Seedream API 调用模块
可直接导入使用: from seedream_api import generate_image
"""
import requests
import os
import sys
import base64
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("VOLCENGINE_API_KEY")
API_URL = "https://ark.cn-beijing.volces.com/api/v3/images/generations"

MODELS = {
    "5.0": "doubao-seedream-5-0-260128",
    "4.5": "doubao-seedream-4-5-251128",
    "4.0": "doubao-seedream-4-0-250828",
    "3.0-t2i": "doubao-seedream-3-0-t2i-250415",
    "3.0-i2i": "doubao-seededit-3-0-i2i-250415",
}

DEFAULT_MODEL = MODELS["5.0"]


def image_to_base64(image_path):
    """
    将图片文件转换为 Base64 编码
    
    参数:
        image_path (str): 图片文件路径
    
    返回:
        str: Base64 编码字符串，格式为 data:image/<格式>;base64,<编码>
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"图片文件不存在: {image_path}")
    
    ext = os.path.splitext(image_path)[1].lower().lstrip('.')
    if ext == 'jpg':
        ext = 'jpeg'
    
    with open(image_path, 'rb') as f:
        encoded = base64.b64encode(f.read()).decode('utf-8')
    
    return f"data:image/{ext};base64,{encoded}"


def prepare_image_param(image):
    """
    准备图片参数，支持文件路径、Base64 字符串或 URL
    
    参数:
        image (str/list): 图片路径、Base64 或 URL，单图或列表
    
    返回:
        str/list: 处理后的图片参数
    """
    if isinstance(image, list):
        result = []
        for img in image:
            if os.path.exists(img):
                result.append(image_to_base64(img))
            else:
                result.append(img)
        return result
    else:
        if os.path.exists(image):
            return image_to_base64(image)
        return image


def generate_image(prompt, model=None, size="2048x2048", 
                  image=None, sequential_image_generation="disabled", 
                  num_inference_steps=50, guidance_scale=7.5, seed=None, negative_prompt=None,
                  tools=None, download=True, output_dir="output"):
    """
    调用火山引擎 Seedream 生成图片
    
    参数:
        prompt (str): 文本提示词
        model (str): 模型 ID，可选 "5.0", "4.5", "4.0", "3.0-t2i" 或具体 ID，默认最新 5.0
        size (str): 图片尺寸，如 "2048x2048"
        image (str/list): 参考图片，支持文件路径、URL 或 Base64，单图或列表
        sequential_image_generation (str): "auto" 组图，"disabled" 单图
        num_inference_steps (int): 推理步数 1-50
        guidance_scale (float): 引导系数 1-20
        seed (int): 随机种子
        negative_prompt (str): 负向提示词
        tools (list): 工具列表，如 [{"type": "web_search"}]
        download (bool): 是否下载到本地，默认 True
        output_dir (str): 输出目录，默认 "output"
    
    返回:
        dict: 包含生成的图片 URL 和本地路径
    
    可用模型:
        - "5.0" / "doubao-seedream-5-0-260128" (默认，最新)
        - "4.5" / "doubao-seedream-4-5-251128"
        - "4.0" / "doubao-seedream-4-0-250828"
        - "3.0-t2i" / "doubao-seedream-3-0-t2i-250415" (仅文生图)
        - "3.0-i2i" / "doubao-seededit-3-0-i2i-250415" (图生图)
    """
    if not API_KEY:
        raise ValueError("未设置 VOLCENGINE_API_KEY 环境变量")
    
    if model is None:
        model = DEFAULT_MODEL
    elif model in MODELS:
        model = MODELS[model]
    
    if tools and model != "doubao-seedream-5-0-260128":
        raise ValueError("tools 参数仅支持 doubao-seedream-5-0-260128 模型")
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": model,
        "prompt": prompt,
        "size": size,
    }
    
    if guidance_scale != 7.5:
        data["guidance_scale"] = guidance_scale
    if sequential_image_generation != "disabled":
        data["sequential_image_generation"] = sequential_image_generation
    if num_inference_steps != 50:
        data["num_inference_steps"] = num_inference_steps
    
    if image:
        if isinstance(image, list):
            data["image"] = prepare_image_param(image)
        else:
            data["image"] = prepare_image_param(image)
    if seed is not None:
        data["seed"] = seed
    if negative_prompt:
        data["negative_prompt"] = negative_prompt
    if tools:
        data["tools"] = tools
    
    response = requests.post(API_URL, headers=headers, json=data)
    result = response.json()
    
    if "data" in result:
        urls = [img["url"] for img in result["data"]]
        local_paths = []
        
        if download:
            os.makedirs(output_dir, exist_ok=True)
            for i, url in enumerate(urls, 1):
                filename = f"{prompt[:20]}_{i}.jpg"
                filename = "".join(c for c in filename if c not in r'<>:"/\|?*')
                filepath = os.path.join(output_dir, filename)
                
                img_response = requests.get(url)
                with open(filepath, "wb") as f:
                    f.write(img_response.content)
                local_paths.append(filepath)
                print(f"已保存: {filepath}")
        
        return {
            "success": True,
            "model": model,
            "images": urls,
            "local_paths": local_paths if download else [],
            "usage": result.get("usage", {})
        }
    else:
        error_msg = result.get("error", {}).get("message", "未知错误")
        raise Exception(f"API 调用失败: {error_msg}")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Seedream 图片生成")
    parser.add_argument("prompt", nargs="?", default="一只可爱的橘猫坐在窗台上", help="图片描述")
    parser.add_argument("-m", "--model", help=f"模型版本: {', '.join(MODELS.keys())} (默认: 5.0)")
    parser.add_argument("-s", "--size", default="2048x2048", help="图片尺寸 (默认: 2048x2048)")
    parser.add_argument("-o", "--output-dir", default="output", help="输出目录 (默认: output)")
    parser.add_argument("--steps", type=int, default=50, help="推理步数 1-50 (默认: 50)")
    parser.add_argument("--guidance", type=float, default=7.5, help="引导系数 1-20 (默认: 7.5)")
    parser.add_argument("--seed", type=int, help="随机种子 (用于可复现结果)")
    parser.add_argument("--negative", help="负向提示词")
    parser.add_argument("-i", "--image", help="参考图片路径或URL (支持图生图)")
    parser.add_argument("--images", nargs="+", help="多张参考图片路径或URL (支持多图生图/组图)")
    parser.add_argument("--group", action="store_true", help="启用组图模式 (sequential_image_generation=auto)")
    parser.add_argument("--tools", nargs="+", help="工具列表，如 web_search (启用联网搜索)")
    
    args = parser.parse_args()
    
    image_list = []
    if args.image:
        image_list.append(args.image)
    if args.images:
        image_list.extend(args.images)
    
    image_param = None
    if image_list:
        image_param = image_list if len(image_list) > 1 else image_list[0]
    
    sequential_mode = "auto" if args.group else "disabled"
    
    tools_param = None
    if args.tools:
        tools_param = [{"type": tool} for tool in args.tools]
    
    print(f"正在生成图片: {args.prompt}")
    if args.model:
        print(f"使用模型: {args.model}")
    if image_param:
        print(f"使用参考图片: {image_param}")
    if args.group:
        print("启用组图模式")
    if tools_param:
        print(f"使用工具: {[t['type'] for t in tools_param]}")
    
    result = generate_image(
        prompt=args.prompt,
        model=args.model,
        size=args.size,
        image=image_param,
        sequential_image_generation=sequential_mode,
        num_inference_steps=args.steps,
        guidance_scale=args.guidance,
        seed=args.seed,
        negative_prompt=args.negative,
        tools=tools_param,
        output_dir=args.output_dir
    )
    
    print(f"\n生成成功! (模型: {result['model']})")
    print("图片 URL:")
    for i, url in enumerate(result["images"], 1):
        print(f"  {i}. {url}")
    
    if result["local_paths"]:
        print("\n本地文件:")
        for path in result["local_paths"]:
            print(f"  {path}")


if __name__ == "__main__":
    main()
