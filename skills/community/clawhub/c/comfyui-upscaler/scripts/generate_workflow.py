#!/usr/bin/env python3
"""
ComfyUI 三重超清放大工作流生成器

生成可导入 ComfyUI 的 JSON 工作流文件，包含：
1. 潜空间放大 (Latent Scale + K采样器)
2. 分区放大 (SD Upscale)
3. 模型放大 (Image Upscale with Model)
"""

import json
import argparse
from pathlib import Path

def generate_workflow(
    base_model: str = "models/checkpoints/v1-5-pruned-emaonly.safetensors",
    upscale_model: str = "4x-UltraSharp.pth",
    tile_size: int = 1024,
    scale: float = 2.0,
    denoise: float = 0.35,
    seed: int = 42
) -> dict:
    """生成三重放大工作流"""
    
    workflow = {
        "version": "1.0",
        "name": "Triple Upscale Workflow",
        "nodes": {}
    }
    
    # 1. 模型加载器
    workflow["nodes"]["checkpoint_loader"] = {
        "class_type": "CheckpointLoaderSimple",
        "inputs": {
            "ckpt_name": base_model
        },
        "outputs": ["model", "clip", "vae"]
    }
    
    # 2. CLIP 文本编码器 - 正向提示词
    workflow["nodes"]["clip_positive"] = {
        "class_type": "CLIPTextEncode",
        "inputs": {
            "text": "masterpiece, best quality, high resolution, detailed, sharp focus",
            "clip": ["checkpoint_loader", "clip"]
        },
        "outputs": ["conditioning"]
    }
    
    # 3. CLIP 文本编码器 - 负向提示词
    workflow["nodes"]["clip_negative"] = {
        "class_type": "CLIPTextEncode",
        "inputs": {
            "text": "worst quality, low quality, blurry, fuzzy, noise",
            "clip": ["checkpoint_loader", "clip"]
        },
        "outputs": ["conditioning"]
    }
    
    # 4. VAE 解码器（用于图生图阶段）
    workflow["nodes"]["vae_decode"] = {
        "class_type": "VAEDecode",
        "inputs": {},
        "outputs": ["pixel_image"]
    }
    
    # 5. 潜空间放大节点
    workflow["nodes"]["latent_scale"] = {
        "class_type": "LatentScaleByFactor",
        "inputs": {
            "samples": None,  # 后续连接
            "scale_by": scale
        },
        "outputs": ["samples"]
    }
    
    # 6. K采样器（潜空间重采样）
    workflow["nodes"]["k_sampler_latent"] = {
        "class_type": "KSampler",
        "inputs": {
            "model": ["checkpoint_loader", "model"],
            "seed": seed,
            "steps": 20,
            "cfg": 8.0,
            "sampler_name": "dpmpp_2m",
            "scheduler": "normal",
            "positive": ["clip_positive", "conditioning"],
            "negative": ["clip_negative", "conditioning"],
            "latent_image": ["latent_scale", "samples"],
            "denoise": denoise
        },
        "outputs": ["latent"]
    }
    
    # 7. VAE 解码（潜空间 -> 像素空间）
    workflow["nodes"]["vae_decode_latent"] = {
        "class_type": "VAEDecode",
        "inputs": {
            "samples": ["k_sampler_latent", "latent"]
        },
        "outputs": ["pixel_image"]
    }
    
    # 8. SD Upscale 分区放大
    workflow["nodes"]["sd_upscale"] = {
        "class_type": "SDUpscale",
        "inputs": {
            "pixels": ["vae_decode_latent", "pixel_image"],
            "model": ["checkpoint_loader", "model"],
            "upscale_model": upscale_model,
            "tile_width": tile_size,
            "tile_height": tile_size,
            "mask_blur": 8,
            "tile_padding": 256,
            "seam_fix_width": 64,
            "seam_fix_denoise": 0.35,
            "seam_fix_padding": 256,
            "seam_fix_guidance_scale": 10.0,
            "seam_fix_threshold": 0.5,
            "upscaler_name": "None",
            "seed": seed,
            "steps": 20,
            "cfg": 8.0,
            "sampler_name": "dpmpp_2m",
            "positive": ["clip_positive", "conditioning"],
            "negative": ["clip_negative", "conditioning"],
            "denoise": denoise
        },
        "outputs": ["pixel_image"]
    }
    
    # 9. 模型放大（全局锐化）
    workflow["nodes"]["image_upscale_model"] = {
        "class_type": "ImageUpscaleWithModel",
        "inputs": {
            "upscale_model": upscale_model,
            "image": ["sd_upscale", "pixel_image"]
        },
        "outputs": ["pixel_image"]
    }
    
    # 10. 保存图像
    workflow["nodes"]["save_image"] = {
        "class_type": "SaveImage",
        "inputs": {
            "images": ["image_upscale_model", "pixel_image"],
            "filename_prefix": "upscaled_",
            "output_dir": "output/upscaled"
        },
        "outputs": []
    }
    
    return workflow


def save_workflow(workflow: dict, output_path: str):
    """保存工作流到 JSON 文件"""
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output, 'w', encoding='utf-8') as f:
        json.dump(workflow, f, indent=2, ensure_ascii=False)
    
    print(f"✅ 工作流已保存到: {output.absolute()}")
    print(f"   放大倍数: {workflow['nodes']['latent_scale']['inputs']['scale_by']}x")
    print(f"   分块大小: {workflow['nodes']['sd_upscale']['inputs']['tile_width']}px")


def main():
    parser = argparse.ArgumentParser(description="ComfyUI 三重超清放大工作流生成器")
    parser.add_argument("--base_model", type=str, default="sd_xl_base_1.0.safetensors",
                        help="基础模型文件名")
    parser.add_argument("--upscale_model", type=str, default="4x-UltraSharp.pth",
                        help="放大模型文件名")
    parser.add_argument("--tile_size", type=int, default=1024,
                        help="分块大小（像素）")
    parser.add_argument("--scale", type=float, default=2.0,
                        help="放大倍数")
    parser.add_argument("--denoise", type=float, default=0.35,
                        help="重采样去噪强度 (0.0-1.0)")
    parser.add_argument("--seed", type=int, default=42,
                        help="随机种子")
    parser.add_argument("--output", type=str, default="triple_upscale_workflow.json",
                        help="输出JSON文件路径")
    
    args = parser.parse_args()
    
    workflow = generate_workflow(
        base_model=args.base_model,
        upscale_model=args.upscale_model,
        tile_size=args.tile_size,
        scale=args.scale,
        denoise=args.denoise,
        seed=args.seed
    )
    
    save_workflow(workflow, args.output)


if __name__ == "__main__":
    main()
