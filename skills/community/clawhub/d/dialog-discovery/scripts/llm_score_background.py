#!/usr/bin/env python3
"""
后台 LLM 评分脚本
- 批量调用 LLM 评分
- 自动轮询等待
- 保存结果到文件
- 支持断点续传
"""
import argparse
import json
import os
import sys
import time
from datetime import datetime
from typing import Any, Dict, List

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from llm_client import call_messages, parse_json_response, get_model_config, create_client
from common import WORKSPACE_DIR


def load_dialogs(input_path: str) -> List[Dict[str, Any]]:
    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("dialogs", data.get("results", []))


def load_progress(progress_path: str) -> Dict[str, Any]:
    """加载已完成的进度"""
    if os.path.exists(progress_path):
        with open(progress_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"completed": [], "results": []}


def save_progress(progress_path: str, progress: Dict[str, Any]):
    """保存进度"""
    with open(progress_path, "w", encoding="utf-8") as f:
        json.dump(progress, f, ensure_ascii=False, indent=2)


def score_single_dialog(dialog: Dict[str, Any], model_name: str, scene: str = "loan") -> Dict[str, Any]:
    """评分单条对话"""
    from batch_score_dialogs import build_llm_prompt
    
    try:
        messages = build_llm_prompt(dialog, scene)
        raw_response = call_messages(messages, model_name=model_name)
        parsed = parse_json_response(raw_response)
        
        if parsed:
            parsed["dialog_id"] = dialog.get("dialog_id") or dialog.get("dialog", {}).get("dialog_id")
            parsed["raw_response"] = raw_response[:500]  # 只保留前500字符
            return parsed
        else:
            return {
                "dialog_id": dialog.get("dialog_id"),
                "error": "parse_failed",
                "raw_response": raw_response[:500],
            }
    except Exception as e:
        return {
            "dialog_id": dialog.get("dialog_id"),
            "error": str(e),
        }


def batch_score_background(
    input_path: str,
    output_path: str,
    model_name: str,
    batch_size: int = 10,
    delay_seconds: float = 0.5,
    scene: str = "loan",
):
    """后台批量评分"""
    dialogs = load_dialogs(input_path)
    progress_path = output_path.replace(".json", "-progress.json")
    
    # 加载已有进度
    progress = load_progress(progress_path)
    completed_ids = set(progress.get("completed", []))
    results = progress.get("results", [])
    
    # 过滤已完成的
    pending = [d for d in dialogs if (d.get("dialog_id") or d.get("dialog", {}).get("dialog_id")) not in completed_ids]
    
    print(f"=== LLM 评分任务 ===")
    print(f"总数: {len(dialogs)} 条")
    print(f"已完成: {len(completed_ids)} 条")
    print(f"待处理: {len(pending)} 条")
    print(f"模型: {model_name}")
    print(f"批次大小: {batch_size}")
    print()
    
    if not pending:
        print("✅ 所有对话已评分完成")
        return
    
    # 批量处理
    for i in range(0, len(pending), batch_size):
        batch = pending[i:i + batch_size]
        batch_num = i // batch_size + 1
        total_batches = (len(pending) + batch_size - 1) // batch_size
        
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 处理批次 {batch_num}/{total_batches} ({len(batch)} 条)...")
        
        for dialog in batch:
            dialog_id = dialog.get("dialog_id") or dialog.get("dialog", {}).get("dialog_id")
            
            result = score_single_dialog(dialog, model_name, scene=scene)
            results.append(result)
            completed_ids.add(dialog_id)
            
            # 显示进度
            if result.get("total_score"):
                print(f"  ✓ {dialog_id}: {result['total_score']} 分 ({result.get('classification')})")
            elif result.get("error"):
                print(f"  ✗ {dialog_id}: {result['error']}")
            else:
                print(f"  ? {dialog_id}: 解析失败")
            
            # 延迟避免限流
            time.sleep(delay_seconds)
        
        # 保存进度
        progress["completed"] = list(completed_ids)
        progress["results"] = results
        progress["updated_at"] = datetime.now().isoformat()
        save_progress(progress_path, progress)
        
        print(f"  进度已保存: {len(completed_ids)}/{len(dialogs)}")
        print()
    
    # 最终保存
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump({
            "total": len(results),
            "results": results,
            "created_at": datetime.now().isoformat(),
            "model": model_name,
        }, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 评分完成: {output_path}")
    
    # 统计
    success = sum(1 for r in results if r.get("total_score") is not None)
    failed = len(results) - success
    print(f"   成功: {success} 条")
    print(f"   失败: {failed} 条")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="后台 LLM 评分")
    parser.add_argument("--input", required=True, help="输入对话 JSON")
    parser.add_argument("--output", required=True, help="输出评分 JSON")
    parser.add_argument("--model", default="jdcloud", help="模型名称")
    parser.add_argument("--batch-size", type=int, default=5, help="批次大小")
    parser.add_argument("--scene", default="loan", help="场景名称")
    parser.add_argument("--delay", type=float, default=1.0, help="请求间隔（秒）")
    args = parser.parse_args()
    
    batch_score_background(
        args.input,
        args.output,
        args.model,
        args.batch_size,
        args.delay,
        scene=args.scene,
    )