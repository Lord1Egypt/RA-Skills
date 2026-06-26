#!/usr/bin/env python3
"""
批量生成工具 - 批量创建图片生成任务
用于提交大量任务后统一轮询结果
"""
import sys
import json
import argparse
from digen_ai_client import DigenAIClient


def main():
    parser = argparse.ArgumentParser(description="DigenAI 批量生成工具")
    parser.add_argument("token", help="DIGEN_TOKEN")
    parser.add_argument("session_id", help="DIGEN_SESSION_ID")
    parser.add_argument("--prompts", "-p", nargs="+", required=True, 
                       help="提示词列表")
    parser.add_argument("--resolution", "-r", default="9:16",
                       help="分辨率 (默认 9:16)")
    parser.add_argument("--model", "-m", default="flux2",
                       help="模型 (默认 flux2)")
    parser.add_argument("--output", "-o", default="batch_results.json",
                       help="结果输出文件")
    
    args = parser.parse_args()
    
    client = DigenAIClient(token=args.token, session_id=args.session_id)
    
    print(f"提交 {len(args.prompts)} 个图片生成任务...")
    
    results = []
    for i, prompt in enumerate(args.prompts):
        print(f"[{i+1}/{len(args.prompts)}] 提交: {prompt[:50]}...")
        
        result = client.generate_image(
            prompt=prompt,
            resolution=args.resolution,
            model=args.model
        )
        
        if result["success"]:
            result["prompt"] = prompt
            results.append(result)
            print(f"  -> 任务ID: {result['task_id']}")
        else:
            print(f"  -> 失败: {result['error']}")
            results.append({"success": False, "prompt": prompt, "error": result["error"]})
    
    # 保存任务列表
    with open(args.output, "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\n已保存任务列表到 {args.output}")
    print("使用 wait_batch.py 轮询结果")


if __name__ == "__main__":
    main()
