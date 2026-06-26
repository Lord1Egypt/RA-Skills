#!/usr/bin/env python3
"""
BOM/SOP 校对后台处理脚本
用于 sub-agent 并行执行校对任务
"""

import sys
import os
import json
import time
from pathlib import Path

# 添加脚本目录到路径
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

from compare_bom_sop import parse_bom_file, parse_sop_file, compare_items, generate_marked_file

def main():
    if len(sys.argv) < 3:
        print("用法: python background_compare.py <bom_file> <sop_file> [output_dir]")
        sys.exit(1)
    
    bom_file = sys.argv[1]
    sop_file = sys.argv[2]
    output_dir = sys.argv[3] if len(sys.argv) > 3 else str(Path(bom_file).parent / "output")
    
    # 验证文件存在
    if not os.path.exists(bom_file):
        print(f"错误: BOM 文件不存在: {bom_file}")
        sys.exit(1)
    if not os.path.exists(sop_file):
        print(f"错误: SOP 文件不存在: {sop_file}")
        sys.exit(1)
    
    print(f"[后台任务] 开始处理...")
    print(f"  BOM: {bom_file}")
    print(f"  SOP: {sop_file}")
    print(f"  输出目录: {output_dir}")
    
    start_time = time.time()
    
    try:
        # 解析文件
        print("\n[1/4] 解析 BOM 文件...")
        bom_items = parse_bom_file(bom_file)
        print(f"  BOM 共有 {len(bom_items)} 项物料")
        
        print("\n[2/4] 解析 SOP 文件...")
        sop_items = parse_sop_file(sop_file)
        print(f"  SOP 共有 {len(sop_items)} 项物料")
        
        # 对比
        print("\n[3/4] 执行对比校对...")
        differences = compare_items(bom_items, sop_items)
        print(f"  发现 {len(differences)} 项差异")
        
        # 生成输出文件
        print("\n[4/4] 生成标注文件...")
        os.makedirs(output_dir, exist_ok=True)
        
        sop_basename = Path(sop_file).stem
        output_file = os.path.join(output_dir, f"{sop_basename}_marked.xlsx")
        
        generate_marked_file(sop_file, differences, output_file, bom_items)
        print(f"  输出文件: {output_file}")
        
        # 生成报告 JSON
        report = {
            "status": "success",
            "bom_items": len(bom_items),
            "sop_items": len(sop_items),
            "differences": len(differences),
            "output_file": output_file,
            "processing_time": round(time.time() - start_time, 2),
            "difference_list": differences[:20]  # 只保留前20条
        }
        
        report_file = os.path.join(output_dir, f"{sop_basename}_report.json")
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"\n[完成] 处理时间: {report['processing_time']}秒")
        print(f"  报告文件: {report_file}")
        
        # 输出摘要（供 sub-agent 读取）
        print("\n" + "="*60)
        print("## 校对结果摘要")
        print(f"- BOM 物料数: {len(bom_items)}")
        print(f"- SOP 物料数: {len(sop_items)}")
        print(f"- 差异数量: {len(differences)}")
        print(f"- 输出文件: {output_file}")
        print("="*60)
        
    except Exception as e:
        print(f"\n[错误] 处理失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
