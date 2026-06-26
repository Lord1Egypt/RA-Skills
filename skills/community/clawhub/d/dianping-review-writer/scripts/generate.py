#!/usr/bin/env python3
"""
大众点评评论生成器
根据商家类型和体验自动生成高质量评论
"""

import argparse
import random

# 评论模板库
TEMPLATES = {
    "restaurant": {
        "detailed": """
{opening}

环境：{env_desc}
菜品：{dish_desc}
服务：{service_desc}

{conclusion}
""",
        "story": """
{scenario}，{mood}。

{env_desc}，{dish_highlight}。{detail_moment}

{service_desc}。{conclusion}
""",
        "short": """
{core_review}，{supplement}。
"""
    },
    "beauty": {
        "detailed": """
{opening}

环境：{env_desc}
服务：{service_desc}
效果：{effect_desc}

{conclusion}
""",
        "story": """
{scenario}，{mood}。

{env_desc}，{service_highlight}。{detail_moment}

{effect_desc}。{conclusion}
""",
        "short": """
{core_review}，{supplement}。
"""
    },
    "entertainment": {
        "detailed": """
{opening}

环境：{env_desc}
体验：{experience_desc}
服务：{service_desc}

{conclusion}
""",
        "story": """
{scenario}，{mood}。

{env_desc}，{experience_highlight}。{detail_moment}

{service_desc}。{conclusion}
""",
        "short": """
{core_review}，{supplement}。
"""
    }
}

# 各类型商家的描述词库
DESCRIPTIONS = {
    "restaurant": {
        "openings": [
            "周末和{people}来打卡这家{cuisine}，",
            "工作日晚餐选择了这家{cuisine}，",
            "{people}聚会选了这家{cuisine}，",
            "偶然发现这家{cuisine}，"
        ],
        "envs": [
            "店面装修挺有{style}的，{feature}",
            "{location}，{feature}",
            "整体{style}，{feature}",
            "环境{feature}，{style}"
        ],
        "dishes": [
            "点了{dish1}和{dish2}，{taste1}，{taste2}",
            "招牌{dish1}确实{quality}，{taste}",
            "推荐{dish1}，{taste}，{dish2}也{quality}",
            "菜品整体{quality}，尤其是{dish1}"
        ],
        "services": [
            "上菜速度{speed}，大概{time}分钟齐活",
            "服务员{attitude}，{action}",
            "服务{quality}，{detail}",
            "{staff}挺{attitude}的，{action}"
        ],
        "conclusions": [
            "{people}吃了{price}，人均{avg}左右，在{location}这个价位算{value}。总体{rating}星，{revisit}。",
            "性价比{value}，{rating}星推荐，{revisit}。",
            "整体{quality}，{revisit}，{rating}星。"
        ]
    }
}

# 配图建议
PHOTO_SUGGESTIONS = {
    "restaurant": {
        "must": ["招牌菜特写", "菜品全家福", "店内环境"],
        "optional": ["门口招牌", "菜单/价目表", "账单", "细节特写"]
    },
    "beauty": {
        "must": ["店内环境", "使用的产品", "服务过程"],
        "optional": ["前后对比", "价目表", "休息区", "细节装饰"]
    },
    "entertainment": {
        "must": ["场所环境", "核心设施", "体验瞬间"],
        "optional": ["入口/招牌", "等候区", "价格信息", "团体合照"]
    }
}

# 标签推荐
TAGS = {
    "restaurant": {
        "火锅": ["#火锅", "#重庆火锅", "#朋友聚会", "#深夜食堂"],
        "日料": ["#日料", "#刺身", "#约会", "#精致料理"],
        "烧烤": ["#烧烤", "#夜宵", "#朋友聚会", "#烟火气"],
        "西餐": ["#西餐", "#牛排", "#约会", "#仪式感"],
        "川菜": ["#川菜", "#麻辣", "#下饭菜", "#无辣不欢"]
    },
    "beauty": ["#美容护肤", "#皮肤管理", "#放松时刻", "#变美日记"],
    "entertainment": ["#周末去哪儿", "#朋友聚会", "#放松解压", "#打卡"]
}

def generate_restaurant_review(cuisine, experience, rating, style):
    """生成餐厅评论"""
    
    # 随机选择元素
    people = random.choice(["朋友", "家人", "同事", "对象"])
    style_adj = random.choice(["烟火气", "简约", "温馨", "ins风", "复古"])
    env_feature = random.choice([
        "木质桌椅间距刚好，不会太挤",
        "灯光柔和，适合拍照",
        "空间开阔，不压抑",
        "装修用心，细节到位"
    ])
    
    # 菜品相关
    dishes_map = {
        "火锅": ["毛肚", "鸭血", "贡菜", "酥肉", "嫩牛肉"],
        "日料": ["刺身拼盘", "寿司", "天妇罗", "拉面", "烤鳗鱼"],
        "烧烤": ["羊肉串", "烤翅", "金针菇", "烤韭菜", "烤鱼"],
        "西餐": ["牛排", "意面", "沙拉", "浓汤", "甜品"],
        "川菜": ["水煮鱼", "回锅肉", "麻婆豆腐", "辣子鸡", "夫妻肺片"]
    }
    
    dish_list = dishes_map.get(cuisine, ["招牌菜", "特色菜", "推荐菜"])
    dish1, dish2 = random.sample(dish_list, min(2, len(dish_list)))
    
    taste_descs = [
        "口感{quality}",
        "{quality}很到位",
        "味道{quality}",
        "{feature}"
    ]
    
    # 构建评论
    if style == "detailed":
        opening = f"{random.choice(['周末', '工作日晚上', '中午'])}和{people}来打卡这家{cuisine}"
        env = f"店面装修挺有{style_adj}的，{env_feature}"
        dish = f"点了{dish1}和{dish2}，味道都不错，{dish1}尤其出色"
        service = random.choice([
            "上菜速度中等，大概15分钟齐活，服务员会主动加汤",
            "服务响应及时，收盘子也勤快",
            "服务员态度很好，有求必应"
        ])
        conclusion = f"人均80-120，整体{rating}星，值得再来"
        
        return f"{opening}。\n\n环境：{env}。\n菜品：{dish}。\n服务：{service}。\n\n{conclusion}。"
        
    elif style == "story":
        scenario = f"{random.choice(['加班后的深夜', '周末放松', '朋友小聚'])}"
        mood = random.choice(["本来只想随便吃点，结果挺惊喜", "期待已久，终于打卡"])
        env = f"店里{env_feature}"
        highlight = f"{dish1}上桌的时候还在冒热气"
        moment = f"{random.choice(['老板还送了小菜', '服务员推荐了隐藏菜单'])}"
        conclusion = f"{rating}星推荐，下次还会来"
        
        return f"{scenario}，{mood}。{env}，{highlight}。{moment}。{conclusion}。"
        
    else:  # short
        return f"{cuisine}不错，{dish1}推荐，环境{style_adj}，{rating}星。"

def generate_beauty_review(rating, style):
    """生成美容美发评论"""
    services = ["面部护理", "按摩", "美甲", "美发"]
    service = random.choice(services)
    
    if style == "detailed":
        return f"""来做{service}，店里环境很舒适，香氛味道好闻。

护理师手法专业，{random.choice(['按得很到位', '力度刚好', '细节处理得很好'])}。
做完{random.choice(['皮肤状态改善明显', '整个人放松很多', '效果超出预期'])}。

{rating}星推荐，会再来的。"""
    
    elif style == "story":
        return f"""{random.choice(['周末放松', '下班后来', '约会前'])}来做{service}，
店里{random.choice(['环境很治愈', '氛围很放松', '装修很ins风'])}。
护理师{random.choice(['很专业', '很细心', '手法很好'])}，{random.choice(['全程无推销', '还会讲护肤知识', '根据肤质调整方案'])}。
效果{random.choice(['挺满意的', '超出预期', '肉眼可见'])}，{rating}星。"""
    
    else:
        return f"{service}体验不错，环境好，{random.choice(['无推销', '手法专业', '性价比高'])}，{rating}星。"

def generate_entertainment_review(rating, style):
    """生成休闲娱乐评论"""
    venues = ["KTV", "密室逃脱", "剧本杀", "电影院", "游乐场"]
    venue = random.choice(venues)
    
    if style == "detailed":
        return f"""周末和朋友来{venue}，{random.choice(['体验很棒', '玩得很开心', '超出预期'])}。

环境{random.choice(['很新很干净', '装修有特色', '氛围感拉满'])}，
{random.choice(['设施很齐全', '道具很精致', '设备很新'])}。
服务{random.choice(['态度很好', '响应及时', '很专业'])}。

{rating}星推荐，适合{random.choice(['朋友聚会', '情侣约会', '团建'])}。"""
    
    elif style == "story":
        return f"""{random.choice(['周末放松', '生日聚会', '公司团建'])}选了这家{venue}，
{random.choice(['本来没抱太大期待', '朋友强烈推荐的', '偶然发现的'])}，结果{random.choice(['很惊喜', '玩得很嗨', '意犹未尽'])}。
{random.choice(['工作人员很热情', '环境布置很用心', '流程设计很合理'])}，
{random.choice(['会再来', '推荐给朋友了', '下次带其他朋友来'])}，{rating}星。"""
    
    else:
        return f"{venue}体验{random.choice(['很棒', '不错', '超预期'])}，环境{random.choice(['好', '有特色', '很新'])}，{rating}星推荐。"

def get_photo_suggestions(venue_type, cuisine=None):
    """获取配图建议"""
    suggestions = PHOTO_SUGGESTIONS.get(venue_type, PHOTO_SUGGESTIONS["restaurant"])
    
    result = "【必拍】\n"
    for item in suggestions["must"]:
        result += f"• {item}\n"
    
    result += "\n【可选】\n"
    for item in suggestions["optional"]:
        result += f"• {item}\n"
    
    return result

def get_tags(venue_type, cuisine=None):
    """获取标签推荐"""
    if venue_type == "restaurant" and cuisine:
        tags = TAGS["restaurant"].get(cuisine, ["#美食", "#探店"])
    else:
        tags = TAGS.get(venue_type, ["#探店", "#周末去哪儿"])
    
    return " ".join(tags[:4])

def main():
    parser = argparse.ArgumentParser(description='生成大众点评评论')
    parser.add_argument('--type', required=True, 
                       choices=['restaurant', 'beauty', 'entertainment', 'fitness', 'hotel'],
                       help='商家类型')
    parser.add_argument('--cuisine', help='细分品类（如：火锅、日料）')
    parser.add_argument('--experience', help='体验简述')
    parser.add_argument('--rating', type=int, default=5, choices=[1,2,3,4,5],
                       help='目标评分')
    parser.add_argument('--count', type=int, default=3, help='生成数量')
    parser.add_argument('--style', choices=['detailed', 'story', 'short'],
                       help='风格（不传则混合）')
    
    args = parser.parse_args()
    
    # 生成评论
    styles = ['detailed', 'story', 'short'] if not args.style else [args.style]
    
    print("=" * 50)
    print(f"📝 大众点评评论生成 ({args.type})")
    print("=" * 50)
    
    for i in range(args.count):
        style = styles[i % len(styles)]
        
        if args.type == "restaurant":
            review = generate_restaurant_review(
                args.cuisine or "餐厅", 
                args.experience, 
                args.rating, 
                style
            )
        elif args.type == "beauty":
            review = generate_beauty_review(args.rating, style)
        elif args.type == "entertainment":
            review = generate_entertainment_review(args.rating, style)
        else:
            review = generate_restaurant_review("餐厅", args.experience, args.rating, style)
        
        print(f"\n【评论{i+1} - {style}风格】")
        print("-" * 40)
        print(review)
        print()
    
    # 配图建议
    print("\n" + "=" * 50)
    print("📸 配图建议")
    print("=" * 50)
    print(get_photo_suggestions(args.type, args.cuisine))
    
    # 标签推荐
    print("\n" + "=" * 50)
    print("🏷️ 标签推荐")
    print("=" * 50)
    print(get_tags(args.type, args.cuisine))

if __name__ == "__main__":
    main()
