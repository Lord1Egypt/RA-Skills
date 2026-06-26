#!/usr/bin/env python3
"""
face-reading-cn 图像识别分析模块
Phase 1: 开天眼 - 集成图像识别功能
使用 vita 技能进行面部图像分析
"""

import subprocess
import sys
import os
import json
from datetime import datetime

# vita 技能路径
VITA_SCRIPT = "/root/.openclaw/workspace/skills/vita/scripts/main.py"

def analyze_face_image(image_url: str, analysis_type: str = "general") -> dict:
    """
    分析面部图像
    
    Args:
        image_url: 图片URL（需可公开访问）
        analysis_type: 分析类型 (general/three-stops/five-eyes/features/combined)
    
    Returns:
        分析结果字典
    """
    
    # 定义不同分析类型的prompt
    prompts = {
        "general": """请分析这张面部照片，从面相学角度描述：
1. 面部整体轮廓和比例
2. 三停（上停、中停、下停）比例
3. 五眼比例
4. 五官特征（眉、眼、鼻、口、耳）
5. 面部气色
请用专业的面相学术语描述。""",

        "three-stops": """请重点分析这张面部照片的"三停"比例：
- 上停：发际线到眉毛
- 中停：眉毛到鼻底
- 下停：鼻底到下巴
分析三停是否匀称，各代表什么运势。""",

        "five-eyes": """请重点分析这张面部照片的"五眼"比例：
- 面部宽度是否约等于五只眼睛的宽度
- 两眼间距
- 眼睛大小和形状
分析五眼比例对面相的影响。""",

        "features": """请详细分析这张面部照片的五官特征：
1. 眉毛：浓淡、长短、形状
2. 眼睛：大小、神采、眼型
3. 鼻子：高挺、大小、鼻翼
4. 嘴巴：大小、唇形、嘴角
5. 耳朵：大小、厚薄、耳垂
结合面相学分析各五官含义。""",

        "combined": """请对这张面部照片进行全面面相学分析：
1. 三停五眼整体比例
2. 十二宫位重点区域
3. 五官特征详解
4. 面部痣/纹特征（如有）
5. 五行面相分类
6. 综合运势简评
请提供详细的面相学分析报告。"""
    }
    
    prompt = prompts.get(analysis_type, prompts["general"])
    
    # 构建vita调用命令
    cmd = [
        "python3", VITA_SCRIPT,
        "--image", image_url,
        "--prompt", prompt
    ]
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            return {
                "success": True,
                "analysis": result.stdout,
                "analysis_type": analysis_type,
                "timestamp": datetime.now().isoformat()
            }
        else:
            return {
                "success": False,
                "error": result.stderr,
                "analysis_type": analysis_type
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "analysis_type": analysis_type
        }

def format_face_report(analysis_result: dict) -> str:
    """格式化面相分析报告"""
    
    if not analysis_result["success"]:
        return f"❌ 分析失败: {analysis_result.get('error', '未知错误')}"
    
    report = f"""👤 **面相图像分析报告**

⏰ 分析时间: {analysis_result['timestamp']}
📊 分析类型: {analysis_result['analysis_type']}

---

{analysis_result['analysis']}

---

⚠️ **免责声明**: 
本分析仅供娱乐和传统文化学习参考，不具备科学依据。
请勿用于重大决策或歧视他人。
"""
    return report

def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print("用法: python3 face_image_analysis.py <图片URL> [分析类型]")
        print("分析类型: general, three-stops, five-eyes, features, combined")
        sys.exit(1)
    
    image_url = sys.argv[1]
    analysis_type = sys.argv[2] if len(sys.argv) > 2 else "combined"
    
    print(f"🔍 正在分析面部图像...")
    print(f"📷 图片: {image_url}")
    print(f"📊 类型: {analysis_type}")
    print()
    
    result = analyze_face_image(image_url, analysis_type)
    report = format_face_report(result)
    print(report)

if __name__ == "__main__":
    main()
