#!/usr/bin/env python3
"""
本地 SDXL 生图脚本 — 通过 ComfyUI REST API 生成图片

用法:
  python3 sdxl_generate.py --prompt "一只狐狸在森林里" [选项]

示例:
  python3 sdxl_generate.py --prompt "赛博朋克城市夜景" --steps 20 --seed 42
  python3 sdxl_generate.py --prompt "动漫风格女孩" --sampler euler --negative "写实, 低质量"
"""
import argparse
import requests
import time
import os
import sys
import random

COMFYUI_URL = "http://localhost:8188"
TIMEOUT_SEC = 120


def parse_args():
    parser = argparse.ArgumentParser(description="本地 SDXL 生图")
    parser.add_argument("--prompt", "-p", required=True, help="图片描述（正向提示词）")
    parser.add_argument("--negative", default="blurry, low quality, distorted, cartoon, paintings, illustrations",
                       help="反向提示词（不想要的内容）")
    parser.add_argument("--steps", type=int, default=20, help="采样步数（默认20，越高质量越好越慢）")
    parser.add_argument("--seed", type=int, default=None, help="随机种子（默认随机）")
    parser.add_argument("--width", type=int, default=1024, help="图片宽度（默认1024）")
    parser.add_argument("--height", type=int, default=768, help="图片高度（默认768）")
    parser.add_argument("--sampler", default="euler",
                        help="采样器: euler/dpmpp_2m/lcm/ddim（默认euler）")
    parser.add_argument("--cfg", type=float, default=7.0,
                        help="CFG强度，1-20（默认7.0，值越大越贴近prompt）")
    parser.add_argument("--output", "-o", default=None, help="输出路径（默认 /tmp/sdxl_gen_种子.png）")
    return parser.parse_args()


def check_comfyui():
    """检查 ComfyUI 是否运行"""
    try:
        r = requests.get(f"{COMFYUI_URL}/system_stats", timeout=5)
        return r.status_code == 200
    except:
        return False


def build_workflow(prompt, negative, steps, seed, width, height, sampler, cfg):
    seed = seed if seed is not None else random.randint(0, 2**32 - 1)
    filename = f"sdxl_{seed}"
    return {
        "loader": {
            "class_type": "CheckpointLoaderSimple",
            "inputs": {"ckpt_name": "sdxl-base-1.0.safetensors"}
        },
        "positive": {
            "class_type": "CLIPTextEncode",
            "inputs": {"text": prompt, "clip": ["loader", 1]}
        },
        "negative": {
            "class_type": "CLIPTextEncode",
            "inputs": {"text": negative, "clip": ["loader", 1]}
        },
        "latent": {
            "class_type": "EmptyLatentImage",
            "inputs": {"width": width, "height": height, "batch_size": 1}
        },
        "sampler": {
            "class_type": "KSampler",
            "inputs": {
                "seed": seed,
                "steps": steps,
                "cfg": cfg,
                "sampler_name": sampler,
                "scheduler": "normal",
                "denoise": 1.0,
                "positive": ["positive", 0],
                "negative": ["negative", 0],
                "model": ["loader", 0],
                "latent_image": ["latent", 0]
            }
        },
        "decode": {
            "class_type": "VAEDecode",
            "inputs": {"samples": ["sampler", 0], "vae": ["loader", 2]}
        },
        "save": {
            "class_type": "SaveImage",
            "inputs": {"images": ["decode", 0], "filename_prefix": filename}
        }
    }


def wait_for_output(filename_prefix, timeout=60):
    """轮询等待图片生成完成"""
    for _ in range(timeout // 2):
        time.sleep(2)
        # 尝试读取输出文件
        for fname in os.listdir("/home/axelhu/ComfyUI/output/"):
            if fname.startswith(filename_prefix) and fname.endswith(".png"):
                return f"/home/axelhu/ComfyUI/output/{fname}"
    return None


def main():
    args = parse_args()

    # 1. 检查 ComfyUI
    if not check_comfyui():
        print("ERROR: ComfyUI 服务未运行。请先启动: python3 ~/ComfyUI/main.py --port 8188")
        sys.exit(1)

    print(f"[SDXL] prompt: {args.prompt}")
    print(f"[SDXL] negative: {args.negative}")
    print(f"[SDXL] steps={args.steps} seed={args.seed or 'random'} sampler={args.sampler} cfg={args.cfg}")
    print(f"[SDXL] size: {args.width}×{args.height}")
    print(f"[SDXL] 预计等待时间: {args.steps * 0.9:.0f}秒")

    # 2. 构建工作流
    workflow = build_workflow(
        args.prompt, args.negative,
        args.steps, args.seed,
        args.width, args.height,
        args.sampler, args.cfg
    )
    seed = args.seed if args.seed else "random"

    # 3. 发送请求
    print("[SDXL] 发送生图请求...")
    r = requests.post(f"{COMFYUI_URL}/prompt", json={"prompt": workflow}, timeout=30)
    if r.status_code != 200:
        print(f"ERROR: HTTP {r.status_code}: {r.text}")
        sys.exit(1)

    result = r.json()
    if "prompt_id" not in result:
        print(f"ERROR: API错误: {result}")
        sys.exit(1)

    prompt_id = result["prompt_id"]
    print(f"[SDXL] prompt_id: {prompt_id}")

    # 4. 轮询结果
    filename_prefix = f"sdxl_{seed if args.seed else '*'}"
    print(f"[SDXL] 等待生成（预计 {args.steps * 0.9:.0f}秒）...")

    output_path = wait_for_output(f"sdxl_{seed if args.seed else 'sdxl_'}")

    if not output_path:
        # 从 history API 查
        for i in range(30):
            time.sleep(2)
            r = requests.get(f"{COMFYUI_URL}/history/{prompt_id}", timeout=10)
            if r.status_code == 200:
                hist = r.json()
                if prompt_id in hist:
                    outputs = hist[prompt_id].get("outputs", {})
                    for node_id, out in outputs.items():
                        if "images" in out:
                            img = out["images"][0]
                            subfolder = img.get("subfolder", "")
                            fname = img["filename"]
                            output_path = f"/home/axelhu/ComfyUI/output/{subfolder}/{fname}" if subfolder else f"/home/axelhu/ComfyUI/output/{fname}"
                            if not os.path.exists(output_path):
                                output_path = f"/home/axelhu/ComfyUI/output/{fname}"
                            break
                    if output_path:
                        break
            print(f"[SDXL] 等待中... {(i+1)*2}s", end="\r")

    if output_path and os.path.exists(output_path):
        # 复制到输出路径
        if args.output:
            import shutil
            final = args.output
        else:
            final = f"/tmp/sdxl_gen_{seed}.png"
            import shutil
            shutil.copy(output_path, final)
        print(f"\n[SDXL] ✅ 生成完成: {final}")
        print(f"[SDXL] OUTPUT:{final}")
    else:
        print("\nERROR: 生成超时或文件未找到")
        sys.exit(1)


if __name__ == "__main__":
    main()
