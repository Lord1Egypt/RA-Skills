#!/usr/bin/env python3
"""
抖音本地生活餐饮运营工具
支持：店铺诊断、爆款打造、团购设计、内容运营、数据分析、话术生成
"""

import argparse
import json
import yaml
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional

# 行业知识库
INDUSTRY_KNOWLEDGE = {
    "hotpot": {
        "name": "火锅",
        "core_selling_points": ["食材新鲜", "锅底特色", "蘸料丰富"],
        "video_focus": ["涮菜过程", "蘸料调配", "食客反应"],
        "groupon_strategy": "多人套餐为主",
        "peak_hours": ["11:30-13:30", "17:30-21:00"],
        "avg_margin": 0.48
    },
    "bbq": {
        "name": "烧烤",
        "core_selling_points": ["现烤现吃", "烟火气", "夜宵氛围"],
        "video_focus": ["烤制过程", "滋滋声", "撸串场景"],
        "groupon_strategy": "夜宵时段+酒水搭配",
        "peak_hours": ["18:00-02:00"],
        "avg_margin": 0.52
    },
    "sichuan": {
        "name": "川菜",
        "core_selling_points": ["麻辣鲜香", "下饭神器", "分量足"],
        "video_focus": ["爆炒过程", "色泽展示", "下饭场景"],
        "groupon_strategy": "单人工作餐+多人聚餐",
        "peak_hours": ["11:30-13:30", "17:30-20:30"],
        "avg_margin": 0.45
    },
    "japanese": {
        "name": "日料",
        "core_selling_points": ["新鲜", "精致", "师傅手艺"],
        "video_focus": ["刺身展示", "师傅手艺", "精致摆盘"],
        "groupon_strategy": "套餐制、午市特价",
        "peak_hours": ["11:30-13:30", "18:00-21:00"],
        "avg_margin": 0.55
    },
    "tea": {
        "name": "茶饮",
        "core_selling_points": ["颜值", "解渴", "网红打卡"],
        "video_focus": ["制作过程", "颜值展示", "打卡场景"],
        "groupon_strategy": "第二杯半价、月卡",
        "peak_hours": ["10:00-22:00"],
        "avg_margin": 0.65
    },
    "dessert": {
        "name": "甜品",
        "core_selling_points": ["网红", "打卡", "颜值"],
        "video_focus": ["摆盘", "环境", "打卡照"],
        "groupon_strategy": "下午茶套餐",
        "peak_hours": ["14:00-18:00"],
        "avg_margin": 0.60
    }
}

# 冷启动诊断清单
COLD_START_CHECKLIST = [
    {"step": 1, "task": "POI认领", "priority": "P0", "desc": "认领抖音店铺POI，完善基础信息"},
    {"step": 2, "task": "基础装修", "priority": "P0", "desc": "上传店铺门头、环境、菜品图片（至少9张）"},
    {"step": 3, "task": "首条视频", "priority": "P0", "desc": "发布第一条店铺介绍视频（15-30秒）"},
    {"step": 4, "task": "首单团购", "priority": "P0", "desc": "上线第一个引流团购（低价爆款）"},
    {"step": 5, "task": "达人合作", "priority": "P1", "desc": "联系同城探店达人，安排探店"},
    {"step": 6, "task": "DOU+投放", "priority": "P1", "desc": "对优质视频投放DOU+测试（100-300元）"},
    {"step": 7, "task": "私域搭建", "priority": "P2", "desc": "建立粉丝群，引导核销顾客入群"},
]

def diagnose(restaurant_type: str, stage: str, city: str) -> Dict:
    """店铺诊断"""
    industry = INDUSTRY_KNOWLEDGE.get(restaurant_type, INDUSTRY_KNOWLEDGE["hotpot"])
    
    result = {
        "诊断时间": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "餐厅类型": industry["name"],
        "所在城市": city,
        "发展阶段": stage,
        "核心卖点": industry["core_selling_points"],
        "视频重点": industry["video_focus"],
        "团购策略": industry["groupon_strategy"],
        "高峰时段": industry["peak_hours"],
        "行业平均毛利率": f"{industry['avg_margin']*100:.0f}%",
        "冷启动清单": COLD_START_CHECKLIST,
        "预估起号周期": "2-4周（取决于执行力度）",
        "建议优先级": [
            "1. 完善POI信息（当天完成）",
            "2. 拍摄首条视频（3天内）",
            "3. 上线首单团购（1周内）",
            "4. 安排达人探店（2周内）"
        ]
    }
    
    return result

def design_dish(name: str, price: float, dish_type: str, selling_points: List[str]) -> Dict:
    """爆款菜品打造方案"""
    industry = INDUSTRY_KNOWLEDGE.get(dish_type, INDUSTRY_KNOWLEDGE["hotpot"])
    
    # 定价梯度
    groupon_price = price * 0.75  # 团购价75折
    flash_price = price * 0.5     # 秒杀价5折
    
    # 视频脚本模板
    video_scripts = [
        {
            "角度": "制作过程",
            "时长": "15-20秒",
            "镜头": ["食材展示特写", "制作过程快剪", "成品展示"],
            "BGM": "节奏感强的热门BGM",
            "文案": f"招牌{name}，{selling_points[0]}，每天卖出XX份！"
        },
        {
            "角度": "食客反应",
            "时长": "10-15秒",
            "镜头": ["食客品尝", "满足表情", "好评口播"],
            "BGM": "轻松愉快的BGM",
            "文案": f"顾客说：这{name}绝了，{selling_points[1]}！"
        },
        {
            "角度": "环境展示",
            "时长": "20-30秒",
            "镜头": ["店铺门头", "用餐环境", "菜品上桌"],
            "BGM": "舒缓的BGM",
            "文案": f"在XX环境吃{name}，体验感拉满！"
        }
    ]
    
    result = {
        "菜品名称": name,
        "原价": f"¥{price}",
        "团购价": f"¥{groupon_price:.0f}",
        "秒杀价": f"¥{flash_price:.0f}",
        "定位": "引流款" if price < 100 else "主推款",
        "核心卖点": selling_points,
        "视频脚本": video_scripts,
        "标题模板": [
            f"【招牌推荐】{name}，{selling_points[0]}",
            f"【必点】来我店必吃{name}，{selling_points[1]}",
            f"【爆款】{name}，一天卖出300份的秘密"
        ],
        "评论区话术": [
            "问：好吃吗？答：试试就知道，不好吃老板亲自道歉！",
            "问：分量足吗？答：管饱！不够免费加！",
            "问：什么时候有位置？答：现在来，不用排队！"
        ]
    }
    
    return result

def design_groupon(restaurant_type: str, avg_ticket: float, target: str) -> List[Dict]:
    """团购方案设计"""
    industry = INDUSTRY_KNOWLEDGE.get(restaurant_type, INDUSTRY_KNOWLEDGE["hotpot"])
    
    # 根据客单价设计套餐梯度
    packages = [
        {
            "套餐名": "2人尝鲜餐",
            "原价": f"¥{avg_ticket * 1.4:.0f}",
            "团购价": f"¥{avg_ticket * 0.73:.0f}",
            "毛利率": "35%",
            "定位": "引流款",
            "适用场景": "新客首单、情侣约会",
            "包含": f"招牌菜1份+配菜2份+饮品2杯"
        },
        {
            "套餐名": "4人聚会餐",
            "原价": f"¥{avg_ticket * 2.7:.0f}",
            "团购价": f"¥{avg_ticket * 1.65:.0f}",
            "毛利率": "48%",
            "定位": "主推款",
            "适用场景": "朋友聚餐、家庭聚会",
            "包含": f"招牌菜2份+配菜4份+饮品4杯+甜品1份"
        },
        {
            "套餐名": "6人豪华餐",
            "原价": f"¥{avg_ticket * 4.1:.0f}",
            "团购价": f"¥{avg_ticket * 2.7:.0f}",
            "毛利率": "52%",
            "定位": "利润款",
            "适用场景": "家庭聚餐、商务宴请",
            "包含": f"招牌菜3份+海鲜1份+配菜6份+饮品6杯"
        },
        {
            "套餐名": "秒杀单品券",
            "原价": f"¥{avg_ticket * 0.57:.0f}",
            "团购价": f"¥{avg_ticket * 0.32:.0f}",
            "毛利率": "20%",
            "定位": "爆款",
            "适用场景": "限时引流、新客尝鲜",
            "包含": f"招牌菜1份（限时段）"
        }
    ]
    
    return packages

def design_content(restaurant: str, focus_dishes: List[str], days: int = 7) -> Dict:
    """内容运营策略"""
    # 7天发布日历
    calendar = []
    video_types = ["菜品展示", "制作过程", "食客反应", "环境探店", "优惠活动", "热点蹭流", "互动问答"]
    
    for i in range(days):
        date = (datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d")
        video_type = video_types[i % len(video_types)]
        dish = focus_dishes[i % len(focus_dishes)]
        
        calendar.append({
            "日期": date,
            "视频类型": video_type,
            "主题": f"{dish} - {video_type}",
            "最佳发布时间": "18:00-20:00" if i % 2 == 0 else "12:00-13:00",
            "DOU+预算": "100-200元" if i < 3 else "视数据情况"
        })
    
    result = {
        "餐厅名称": restaurant,
        "重点菜品": focus_dishes,
        "发布日历": calendar,
        "视频脚本模板": {
            "开头3秒": "必须有视觉冲击（滋滋声、热气、色泽）",
            "中间": "展示核心卖点（新鲜、制作、食客反应）",
            "结尾": "引导行动（团购链接、到店地址）"
        },
        "热点蹭流建议": [
            "关注抖音热榜，结合餐厅特色蹭热点",
            "蹭节日热点（情人节、母亲节等）",
            "蹭同城热点（本地新闻、网红打卡）"
        ],
        "评论区互动话术": [
            "问价格：团购更划算，链接在左下角~",
            "问地址：就在XX路XX号，欢迎来打卡！",
            "好评回复：感谢支持！下次来送您XX~",
            "差评回复：抱歉让您失望了，私信我给您补偿~"
        ]
    }
    
    return result

def analyze_data(data_file: str) -> Dict:
    """数据分析（简化版，实际应读取真实数据）"""
    result = {
        "分析时间": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "核心指标漏斗": {
            "曝光量": "10,000",
            "点击率": "8.5%",
            "下单转化率": "12.3%",
            "核销率": "85%",
            "复购率": "28%"
        },
        "同城排名": "前30%",
        "爆款视频": [
            {"标题": "招牌酸菜鱼制作过程", "播放": "5.2万", "转化": "156单"},
            {"标题": "食客好评合集", "播放": "3.8万", "转化": "98单"}
        ],
        "优化建议": [
            "曝光量偏低，建议增加DOU+投放",
            "点击率高于行业平均，团购吸引力强",
            "核销率高，服务质量好",
            "复购率有提升空间，建议建立会员体系"
        ]
    }
    
    return result

def generate_script(scenario: str, context: str) -> Dict:
    """客服话术生成"""
    scripts = {
        "差评回复": {
            "口味不满意": f"抱歉让您失望了！我们会改进，私信我给您发补偿券~",
            "分量不足": f"收到反馈！下次来直接找我，给您加量~",
            "服务态度": f"抱歉给您不好的体验，我们一定加强培训，私信我补偿您~"
        },
        "私聊转化": {
            "问价格": f"团购更划算哦~现在有{context}活动，要不要了解一下？",
            "问位置": f"就在{context}，停车方便，随时欢迎~",
            "问营业时间": f"我们11:00-22:00营业，{context}时段人少，推荐来~"
        },
        "复购引导": {
            "核销后": "感谢光临！加个微信，下次来给您优惠~",
            "好评后": "感谢支持！下次带朋友来，给您送招牌菜~",
            "节日关怀": "XX节快乐！给您准备了专属优惠，这周来享受~"
        }
    }
    
    return scripts.get(scenario, {"默认": "感谢您的反馈，我们会继续努力~"})

def main():
    parser = argparse.ArgumentParser(description="抖音本地生活餐饮运营工具")
    subparsers = parser.add_subparsers(dest="command", help="可用命令")
    
    # diagnose 命令
    diag_parser = subparsers.add_parser("diagnose", help="店铺诊断")
    diag_parser.add_argument("--type", default="hotpot", help="餐厅类型")
    diag_parser.add_argument("--stage", default="new", help="发展阶段")
    diag_parser.add_argument("--city", default="深圳", help="所在城市")
    diag_parser.add_argument("--output", default="diagnose_report.json", help="输出文件")
    
    # dish 命令
    dish_parser = subparsers.add_parser("dish", help="爆款菜品打造")
    dish_parser.add_argument("--name", required=True, help="菜品名称")
    dish_parser.add_argument("--price", type=float, required=True, help="原价")
    dish_parser.add_argument("--type", default="hotpot", help="菜品类型")
    dish_parser.add_argument("--selling-points", default="", help="卖点（逗号分隔）")
    dish_parser.add_argument("--output", default="dish_plan.json", help="输出文件")
    
    # groupon 命令
    group_parser = subparsers.add_parser("groupon", help="团购方案设计")
    group_parser.add_argument("--restaurant-type", default="hotpot", help="餐厅类型")
    group_parser.add_argument("--avg-ticket", type=float, default=120, help="客单价")
    group_parser.add_argument("--target", default="引流+利润", help="目标")
    group_parser.add_argument("--output", default="groupon_plan.json", help="输出文件")
    
    # content 命令
    content_parser = subparsers.add_parser("content", help="内容运营策略")
    content_parser.add_argument("--restaurant", default="我的餐厅", help="餐厅名称")
    content_parser.add_argument("--focus", default="招牌菜", help="重点菜品（逗号分隔）")
    content_parser.add_argument("--days", type=int, default=7, help="规划天数")
    content_parser.add_argument("--output", default="content_calendar.json", help="输出文件")
    
    # analyze 命令
    analyze_parser = subparsers.add_parser("analyze", help="数据分析")
    analyze_parser.add_argument("--data-file", default="", help="数据文件")
    analyze_parser.add_argument("--output", default="analysis_report.json", help="输出文件")
    
    # script 命令
    script_parser = subparsers.add_parser("script", help="客服话术生成")
    script_parser.add_argument("--scenario", default="差评回复", help="场景")
    script_parser.add_argument("--context", default="", help="上下文")
    script_parser.add_argument("--output", default="scripts.json", help="输出文件")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # 执行对应命令
    if args.command == "diagnose":
        result = diagnose(args.type, args.stage, args.city)
    elif args.command == "dish":
        points = [p.strip() for p in args.selling_points.split(",")] if args.selling_points else ["好吃", "新鲜", "分量足"]
        result = design_dish(args.name, args.price, args.type, points)
    elif args.command == "groupon":
        result = design_groupon(args.restaurant_type, args.avg_ticket, args.target)
    elif args.command == "content":
        dishes = [d.strip() for d in args.focus.split(",")]
        result = design_content(args.restaurant, dishes, args.days)
    elif args.command == "analyze":
        result = analyze_data(args.data_file)
    elif args.command == "script":
        result = generate_script(args.scenario, args.context)
    else:
        parser.print_help()
        return
    
    # 输出结果
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    # 保存到文件
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"\n✅ 结果已保存到: {args.output}")

if __name__ == "__main__":
    main()
