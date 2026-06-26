#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Skill Name: Funasr-Punctuation-Restore
Author: 王岷瑞 / https://github.com/wangminrui2022
License: Apache License
Description: 使用 FunASR 官方 ct-punc 模型，为文本、文件或目录一键恢复标点                                                         
✨ 支持三种使用模式：                                              
    1. --text   一段纯文本（直接输出恢复后的文字）                
    2. --file   单个记事本文件（生成 xxx_punctuated.txt）         
    3. --dir    整个目录（同级自动创建「原目录名_punctuated」镜像目录）
           → 目录结构、子文件夹、文件名 100% 一致，原目录完全不修改！                                                  
🚀 核心特性：                                                      
    • GPU 自动加速（cuda:0） + 每次推理后立即清理显存             
    • 模型严格缓存到：models/damo/punc_ct-transformer_cn-en-common-vocab471067-large
    • 下载失败时自动弹出超友好手动下载指南（ModelScope 链接 + 4步操作）
    • 跨平台支持（Windows / Linux / macOS）                        
    • 专为 OpenClaw Agent / ClawHub 设计
"""

import argparse
import os
import gc
import sys
from pathlib import Path
import env_manager
import ensure_package
from config import MODEL_DIR
from logger_manager import LoggerManager
ensure_package.pip("torchaudio")
ensure_package.pip("modelscope","modelscope","snapshot_download")
ensure_package.pip("funasr","funasr","AutoModel")
ensure_package.pip("torch")
from modelscope.hub.snapshot_download import snapshot_download
from funasr import AutoModel
import torch

logger = LoggerManager.setup_logger(logger_name="funasr-punctuation-restore")

# ====================== 模型映射 ======================
MODEL_MAPPING = {
    "ct-punc": "damo/punc_ct-transformer_cn-en-common-vocab471067-large",
}

def download_model(model_name: str, models_dir: Path) -> str:
    """自动下载模型（失败时控制台美观格式化显示）—— 最终路径严格为 models/damo/punc_ct-transformer_cn-en-common-vocab471067-large"""
    if model_name in MODEL_MAPPING:
        repo_id = MODEL_MAPPING[model_name]
    elif "/" in model_name:
        repo_id = model_name
    else:
        repo_id = model_name

    # === 关键修改：强制使用你指定的最终路径结构 ===
    if "/" in repo_id:
        org, name = repo_id.split("/", 1)
        local_dir = models_dir / org / name
    else:
        local_dir = models_dir / repo_id

    logger.info(str(repo_id) + "," + str(local_dir))

    if local_dir.exists() and any(local_dir.iterdir()):
        logger.info(f"✅ 模型已存在: {local_dir}")
        return str(local_dir)

    logger.info(f"🔽 正在从 ModelScope 下载模型: {model_name} → {repo_id}")
    logger.info(f"   保存路径: {local_dir}（严格按你要求：models/damo/...）")

    local_dir.mkdir(parents=True, exist_ok=True)

    try:
        snapshot_download(
            repo_id=repo_id,
            local_dir=str(local_dir),
            allow_patterns=["*"]
        )
        logger.info(f"✅ 下载完成！模型路径: {local_dir}")
        return str(local_dir)
    
    except Exception as e:
        download_url = f"https://modelscope.cn/models/{repo_id}"
        
        # ==================== 你提供的美观格式化输出（完整保留） ====================
        print("\n" + "="*60)
        print("❌ 模型下载失败")
        print("="*60)
        print(f"错误原因: {str(e)}")
        print("\n💡 手动下载方案（推荐，3步搞定）：")
        print("   1. 打开下面链接（直接复制到浏览器）：")
        print(f"      👉 {download_url}")
        print("   2. 点击页面 **下载模型** 按钮（或逐个文件下载）")
        print("      需要下载全部文件：config.json、pytorch_model.bin、tokenizer.json、vocabulary.json 等")
        print(f"   3. 把所有文件放到以下目录：")
        print(f"      📁 {local_dir}")
        print("   4. 重新运行命令即可（自动识别已存在模型）")
        print("\n📋 你的专属模型下载地址（已为你生成）：")
        print(f"   {download_url}")
        print("="*60 + "\n")

        sys.exit(1)

def extract_punctuated(res):
    if isinstance(res, list) and len(res) > 0:
        item = res[0]
        if isinstance(item, dict):
            return item.get('text', '')
        elif isinstance(item, str):
            return item
    elif isinstance(res, str):
        return res
    return ''

def restore_punctuation(model, text: str) -> str:
    if not text.strip():
        return text
    
    res = model.generate(input=text.strip())
    punctuated = extract_punctuated(res)
    
    # === 代码执行完成后 显存 + 内存清理（GPU 专用）===
    del res
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.reset_peak_memory_stats()
    
    return punctuated

def process_file(model, file_path: str):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    punctuated = restore_punctuation(model, text)
    
    name, ext = os.path.splitext(file_path)
    output_path = f"{name}_punctuated{ext}"
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(punctuated)
    
    logger.info(f"✅ 处理完成：{file_path} → {output_path}")
    return output_path

def process_dir(model, input_dir_str: str):
    """目录模式：同级创建 _punctuated 镜像目录（结构+文件名完全一致）"""
    input_dir = Path(input_dir_str)                    # ← 关键修复：强制转为 Path
    output_dir = input_dir.parent / (input_dir.name + "_punctuated")
    output_dir.mkdir(parents=True, exist_ok=True)
    logger.info(f"📁 已创建镜像输出目录: {output_dir}")
    
    for root, dirs, files in os.walk(input_dir):
        rel_path = Path(root).relative_to(input_dir)
        target_root = output_dir / rel_path
        target_root.mkdir(parents=True, exist_ok=True)
        
        for file in files:
            if file.endswith('.txt') and not file.endswith('_punctuated.txt'):
                input_path = Path(root) / file
                output_path = target_root / file   # 文件名完全相同！
                
                with open(input_path, 'r', encoding='utf-8') as f:
                    text = f.read()
                punctuated = restore_punctuation(model, text)
                
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(punctuated)
                
                logger.info(f"✅ 已恢复：{input_path} → {output_path}")
    
    logger.info(f"🎉 目录处理完成！全部文件已保存到：{output_dir}")

def main():
    global args

    # === 模型下载到 models/ + GPU 自动检测 ===
    models_dir = MODEL_DIR
    model_name = "ct-punc"                     # 通过映射得到 damo/punc...
    model_dir_path = download_model(model_name, models_dir)
    logger.info(f"📁 模型加载路径: {model_dir_path}")
    
    # GPU 检测与加载
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    if torch.cuda.is_available():
        logger.info(f"🚀 GPU 可用！使用 {device} 加速推理 + 自动清理显存")
    else:
        logger.info("⚠️ 未检测到 GPU，使用 CPU 模式")
    
    model = AutoModel(
        model=model_dir_path,
        model_revision="v2.0.4",
        device=device  # 或 "cuda"，使用 GPU
    )
    logger.info("✅ FunASR ct-punc 模型加载完成！")
    
    if args.text:
        punctuated = restore_punctuation(model, args.text)
        logger.info("\n=== 恢复后的文本 ===")
        logger.info(punctuated)
        
    elif args.file:
        if not os.path.exists(args.file):
            logger.info(f"❌ 文件不存在：{args.file}")
            return
        process_file(model, args.file)
        
    elif args.dir:
        if not os.path.exists(args.dir):
            logger.info(f"❌ 目录不存在：{args.dir}")
            return
        logger.info(f"📂 开始批量处理目录：{args.dir}")
        process_dir(model, args.dir)
        logger.info("🎉 目录处理完成！")

if __name__ == "__main__":
    env_manager.check_python_version()
    env_manager.setup_venv()

    parser = argparse.ArgumentParser(description="OpenClaw FunASR 标点恢复技能（GPU + 自动清理显存）")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--text', type=str, help='一段纯文本')
    group.add_argument('--file', type=str, help='记事本文件路径 (.txt)')
    group.add_argument('--dir', type=str, help='目录路径（递归处理所有 .txt 文件）')  
    args = parser.parse_args()

    main()