#!/usr/bin/env python3
"""
假国际品牌检测脚本 v2.1（简化版）
优先使用白名单数据，避免 API 受限导致的误判
"""

import json
from datetime import datetime
import argparse

# 已知品牌白名单
KNOWN_BRANDS = {
    "swisse": {"name": "Swisse Health and Beauty Nutritionals", "origin": "Australia", "verdict": "✅ 真国际品牌", "confidence": 0.92},
    "now": {"name": "NOW Foods", "origin": "USA", "verdict": "✅ 真国际品牌", "confidence": 0.95},
    "gnc": {"name": "General Nutrition Centers", "origin": "Canada", "verdict": "✅ 真国际品牌", "confidence": 0.92},
    "nyo3": {"name": "NYO3 by Omega Nutrition", "origin": "China (青岛逢时科技)", "claimed_origin": "Norway", "verdict": "🚩 假国际品牌", "confidence": 0.85},
    "loeon": {"name": "LOEON Health", "origin": "China", "verdict": "🚩 假国际品牌", "confidence": 0.88}
}

def verify_brand(brand_name, mode="quick"):
    brand = brand_name.lower()
    
    # 白名单检查
    if brand in KNOWN_BRANDS:
        info = KNOWN_BRANDS[brand]
        print(f"\n{'='*70}")
        print(f"🔍 品牌国际性验证报告")
        print(f"📝 品牌名称：{brand}")
        print(f"⚙️ 模式：{mode}")
        print(f"{'='*70}")
        
        # 直接返回白名单结果
        verdict = info["verdict"]
        confidence = info.get("confidence", 0.9)
        origin = info.get("origin", "Unknown")
        name = info.get("name", brand)
        claimed_origin = info.get("claimed_origin", "")
        
        print(f"\n✅ [白名单] 已知国际品牌：{name} ({origin})")
        if claimed_origin:
            print(f"⚠️ 宣称起源：{claimed_origin}")
        
        # 判定结果
        print(f"\n{'='*70}")
        print(f"📝 品牌信息：")
        print(f"   - 官方名称：{name}")
        print(f"   - 真实起源国：{origin}")
        print(f"   - 宣称起源（如不同）：{claimed_origin if claimed_origin else 'N/A'}")
        print(f"\n🎯 判定结论：{verdict}")
        print(f"💪 置信度：{confidence*100:.0f}%")
        
        # 建议
        suggestion = "可以放心购买，是真正的国际知名产品" if "✅" in verdict else "⚠️ 高度可能是假冒或纯国内品牌，建议谨慎处理"
        print(f"✅ 建议：{suggestion}")
        
        return {
            "brand": brand,
            "official_name": name,
            "origin": origin,
            "claimed_origin": claimed_origin,
            "verdict": verdict,
            "confidence": confidence,
            "recommendation": suggestion
        }
    
    # 未知品牌提示
    print(f"\n⚠️ [未识别] 品牌：{brand}")
    print(f"   不在白名单中，建议提供更多信息或手动检测")
    return {"brand": brand, "unknown": True}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="假国际品牌检测脚本 v2.1（简化版）")
    parser.add_argument("--brand", required=True, help="要检测的品牌名称")
    args = parser.parse_args()
    
    result = verify_brand(args.brand)
    print(json.dumps(result, indent=2, ensure_ascii=False))