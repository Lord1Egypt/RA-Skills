#!/usr/bin/env python3
"""
演示脚本 - 生成示例报告（无需API Key）
让用户快速体验报告效果
"""

import os
import sys

# 导入同目录下的模块
sys.path.insert(0, os.path.dirname(__file__))
from generate_report import generate_html_report


def main():
    print("🎯 正在生成示例报告...")
    
    # 模拟产品信息
    product_info = {
        "asin": "B08N5WRWNW",
        "title": "Amazon Basics Wireless Earbuds - 示例产品",
        "price": "$29.99",
        "rating": 4.2,
        "total_reviews": 1250,
        "image_url": "https://m.media-amazon.com/images/I/71mP8V15RtL._AC_SL1500_.jpg",
        "url": "https://www.amazon.com/dp/B08N5WRWNW"
    }
    
    # 模拟打标结果（基于真实场景）
    tagged_reviews = [
        {
            "review": {
                "rating": 5,
                "title": "性价比很高，音质不错",
                "body": "用了两周，音质对得起价格。降噪效果还行，日常通勤够用。续航大概4-5小时，基本满足需求。",
                "author": "买家A",
                "date": "2024-03-15"
            },
            "tags": {
                "sentiment": "positive",
                "pain_points": [],
                "selling_points": ["性价比高", "音质好", "降噪还行"],
                "use_cases": ["日常通勤"],
                "user_profile": "注重性价比的上班族",
                "improvement_suggestions": [],
                "summary": "性价比高，日常够用"
            }
        },
        {
            "review": {
                "rating": 2,
                "title": "续航太短，半天就没电",
                "body": "说好的5小时续航，实际用下来只有3小时不到。半天就没电了，非常不方便。充电盒也不经用。",
                "author": "买家B",
                "date": "2024-02-20"
            },
            "tags": {
                "sentiment": "negative",
                "pain_points": ["续航短", "充电盒不经用"],
                "selling_points": [],
                "use_cases": [],
                "user_profile": "重度使用者",
                "improvement_suggestions": ["提升电池容量", "优化续航"],
                "summary": "续航太短，不实用"
            }
        },
        {
            "review": {
                "rating": 4,
                "title": "Good for the price",
                "body": "Decent earbuds for the price. Sound quality is good enough for casual listening. Battery life is okay, gets me through the day.",
                "author": "BuyerC",
                "date": "2024-01-10"
            },
            "tags": {
                "sentiment": "positive",
                "pain_points": [],
                "selling_points": ["good value", "decent sound"],
                "use_cases": ["casual listening"],
                "user_profile": "budget-conscious listener",
                "improvement_suggestions": [],
                "summary": "Good value for money"
            }
        },
        {
            "review": {
                "rating": 1,
                "title": "佩戴不舒服，容易掉",
                "body": "戴了半小时耳朵就疼。运动的时候特别容易掉，完全不敢用。耳塞配件也不够多。",
                "author": "买家D",
                "date": "2024-03-05"
            },
            "tags": {
                "sentiment": "negative",
                "pain_points": ["佩戴不舒服", "容易掉", "配件少"],
                "selling_points": [],
                "use_cases": ["运动"],
                "user_profile": "运动爱好者",
                "improvement_suggestions": ["改进人体工学设计", "增加耳塞配件"],
                "summary": "佩戴不适，不适合运动"
            }
        },
        {
            "review": {
                "rating": 5,
                "title": "连接稳定，操作便捷",
                "body": "蓝牙连接很稳定，没有断连问题。触控操作灵敏，来电自动暂停，很方便。",
                "author": "买家E",
                "date": "2024-02-28"
            },
            "tags": {
                "sentiment": "positive",
                "pain_points": [],
                "selling_points": ["连接稳定", "操作便捷", "功能智能"],
                "use_cases": ["办公", "通话"],
                "user_profile": "商务人士",
                "improvement_suggestions": [],
                "summary": "连接稳定，功能实用"
            }
        },
        {
            "review": {
                "rating": 3,
                "title": "音质一般，低音不足",
                "body": "中规中矩吧，音质没有特别惊艳。低音不足，听流行音乐还行，古典就不行了。",
                "author": "买家F",
                "date": "2024-01-18"
            },
            "tags": {
                "sentiment": "neutral",
                "pain_points": ["音质一般", "低音不足"],
                "selling_points": [],
                "use_cases": ["流行音乐"],
                "user_profile": "音乐爱好者",
                "improvement_suggestions": ["提升音质", "增强低音"],
                "summary": "音质普通，适合流行"
            }
        },
        {
            "review": {
                "rating": 4,
                "title": "物流快，包装好",
                "body": "亚马逊物流很快，隔天就到了。包装严实，产品完好。第一次买这个牌子，体验不错。",
                "author": "买家G",
                "date": "2024-03-10"
            },
            "tags": {
                "sentiment": "positive",
                "pain_points": [],
                "selling_points": ["物流快", "包装好"],
                "use_cases": ["首次购买"],
                "user_profile": "首次尝试新品牌",
                "improvement_suggestions": [],
                "summary": "物流好，首次购买体验佳"
            }
        },
        {
            "review": {
                "rating": 2,
                "title": "麦克风效果差，通话不清晰",
                "body": "打电话的时候对方说听不清。麦克风效果很差，风噪也大。通话需求多的不建议买。",
                "author": "买家H",
                "date": "2024-02-15"
            },
            "tags": {
                "sentiment": "negative",
                "pain_points": ["麦克风效果差", "通话不清晰", "风噪大"],
                "selling_points": [],
                "use_cases": ["通话"],
                "user_profile": "通话需求多",
                "improvement_suggestions": ["改进麦克风", "增加降噪"],
                "summary": "通话效果差，不推荐"
            }
        },
        {
            "review": {
                "rating": 5,
                "title": "Great budget option",
                "body": "For the price, these are amazing. Sound quality is surprisingly good. Comfortable for long sessions.",
                "author": "BuyerI",
                "date": "2024-01-25"
            },
            "tags": {
                "sentiment": "positive",
                "pain_points": [],
                "selling_points": ["budget-friendly", "good sound", "comfortable"],
                "use_cases": ["long sessions"],
                "user_profile": "budget buyer",
                "improvement_suggestions": [],
                "summary": "Great budget earbuds"
            }
        },
        {
            "review": {
                "rating": 3,
                "title": "做工一般，有瑕疵",
                "body": "收到的时候发现充电盒有划痕，感觉像二手的。虽然不影响使用，但心里不舒服。品控需要加强。",
                "author": "买家J",
                "date": "2024-03-01"
            },
            "tags": {
                "sentiment": "neutral",
                "pain_points": ["做工一般", "品控差", "像二手"],
                "selling_points": [],
                "use_cases": [],
                "user_profile": "注重细节",
                "improvement_suggestions": ["加强品控", "检查外观"],
                "summary": "品控有问题，体验打折"
            }
        }
    ]
    
    # 复制更多数据（模拟500条评论的聚合效果）
    expanded_reviews = []
    pain_point_counts = {}
    selling_point_counts = {}
    
    for item in tagged_reviews:
        # 复制10份（模拟多条类似评论）
        for i in range(10):
            expanded_reviews.append(item)
            
            # 统计高频痛点/卖点
            for point in item["tags"]["pain_points"]:
                pain_point_counts[point] = pain_point_counts.get(point, 0) + 1
            for point in item["tags"]["selling_points"]:
                selling_point_counts[point] = selling_point_counts.get(point, 0) + 1
    
    # 生成报告
    output_path = os.path.abspath("../demo_report.html")
    print(f"  产品: {product_info['title']}")
    print(f"  模拟评论数: {len(expanded_reviews)}")
    print(f"  高频痛点: {len(pain_point_counts)} 个")
    print(f"  高频卖点: {len(selling_point_counts)} 个")
    print()
    
    generate_html_report(product_info, expanded_reviews, output_path, debug=False)
    
    print()
    print("=" * 60)
    print(f"✅ 示例报告已生成：")
    print(f"   {output_path}")
    print("=" * 60)
    print()
    print("🌐 正在打开报告...")
    
    import webbrowser
    webbrowser.open(f"file://{output_path}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()
