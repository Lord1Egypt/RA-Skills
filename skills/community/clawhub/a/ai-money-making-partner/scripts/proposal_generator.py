#!/usr/bin/env python3
"""
个性化副业方案生成器
功能：根据用户情况生成可执行的副业方案
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional


class ProposalGenerator:
    """方案生成器"""
    
    def __init__(self):
        self.data_dir = "references"
    
    def generate_proposal(self, user_profile: Dict, recommended_direction: str) -> Dict:
        """
        为用户生成个性化方案
        
        Args:
            user_profile: 用户画像
            recommended_direction: 推荐的方向
        
        Returns:
            完整的副业方案
        """
        # 第一阶段：冷启动期（1-14天）
        phase1 = self._generate_phase1(user_profile, recommended_direction)
        
        # 第二阶段：成长期（15-45天）
        phase2 = self._generate_phase2(user_profile, recommended_direction)
        
        # 第三阶段：稳定期（46-90天）
        phase3 = self._generate_phase3(user_profile, recommended_direction)
        
        return {
            "proposal_name": f"{recommended_direction}副业赚钱方案",
            "user_summary": self._summarize_user(user_profile),
            "direction": recommended_direction,
            "target_income": user_profile.get('target_income', 5000),
            "phases": [phase1, phase2, phase3],
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
    
    def _summarize_user(self, user: Dict) -> str:
        """生成用户情况摘要"""
        return f"""
- 可用时间：每天{user.get('time_per_day', '?')}小时
- 启动资金：{user.get('budget', '?')}元
- 现有技能：{', '.join(user.get('skills', ['无']))}
- 目标收入：月入{user.get('target_income', '?')}元
        """.strip()
    
    def _generate_phase1(self, user: Dict, direction: str) -> Dict:
        """生成冷启动期方案（1-14天）"""
        if direction == "短视频带货":
            return {
                "phase": "冷启动期",
                "duration": "第1-14天",
                "goal": "完成从0到1的起步，验证变现路径",
                "weekly_plan": {
                    "week1": {
                        "days": [
                            {"day": 1, "action": "确定带货品类，注册账号", "detail": "选择自己熟悉或感兴趣的领域"},
                            {"day": 2, "action": "找10个同领域对标账号", "detail": "分析他们的内容、销量、风格"},
                            {"day": 3, "action": "拍摄第1条视频", "detail": "不需要专业设备，手机+支架即可"},
                            {"day": 4, "action": "发布第1条视频", "detail": "研究平台规则，避免违规"},
                            {"day": 5, "action": "分析数据，复盘优化", "detail": "看播放量、点赞、评论"},
                            {"day": 6, "action": "拍摄2-3条视频", "detail": "保持内容稳定输出"},
                            {"day": 7, "action": "一周总结，制定下周计划", "detail": "数据达到预期？方向对不对？"}
                        ],
                        "milestone": "发布5条以上视频，获得基础流量"
                    },
                    "week2": {
                        "days": [
                            {"day": 8, "action": "分析爆款视频特征", "detail": "为什么爆？能不能复制？"},
                            {"day": 9, "action": "尝试带货挂车", "detail": "先不用真发货，熟悉流程"},
                            {"day": 10, "action": "发布2条带货视频", "detail": "把带货融入内容"},
                            {"day": 11, "action": "看数据，调整策略", "detail": "哪个品有希望？"},
                            {"day": 12, "action": "联系商家谈合作/找货源", "detail": "1688、拼多多找同款"},
                            {"day": 13, "action": "发布视频，持续测试", "detail": "多测试几个品"},
                            {"day": 14, "action": "第1阶段总结", "detail": "有订单了吗？哪个品好卖？"}
                        ],
                        "milestone": "出第一单，验证变现可行"
                    }
                },
                "warning": "不要急着投钱，先用代发模式测试",
                "success_criteria": "第14天有订单或明确的方向"
            }
        
        elif direction == "AI文案代写":
            return {
                "phase": "冷启动期",
                "duration": "第1-14天",
                "goal": "快速上手，接单变现",
                "weekly_plan": {
                    "week1": {
                        "days": [
                            {"day": 1, "action": "确定接单方向", "detail": "小红书文案？知乎回答？产品描述？"},
                            {"day": 2, "action": "熟悉AI写作工具", "detail": "ChatGPT/Kimi/文心一言"},
                            {"day": 3, "action": "制作服务介绍", "detail": "闲鱼/淘宝店铺装修"},
                            {"day": 4, "action": "发布第一个商品", "detail": "低价引流，如5元/篇"},
                            {"day": 5, "action": "优化商品标题和描述", "detail": "搜索热度高的关键词"},
                            {"day": 6, "action": "学习同行动态", "detail": "看销量高的店铺怎么做的"},
                            {"day": 7, "action": "第一周复盘", "detail": "有人咨询吗？需要优化什么？"}
                        ],
                        "milestone": "店铺开张，有咨询"
                    },
                    "week2": {
                        "days": [
                            {"day": 8, "action": "接单并完成第一单", "detail": "即使价格低也要认真做"},
                            {"day": 9, "action": "收集客户反馈", "detail": "好评要截图，不好评要改进"},
                            {"day": 10, "action": "优化接单效率", "detail": "把常用指令模板化"},
                            {"day": 11, "action": "适当提价", "detail": "有案例后可以涨价"},
                            {"day": 12, "action": "多平台分发", "detail": "闲鱼、淘宝、猪八戒都上架"},
                            {"day": 13, "action": "建立客户档案", "detail": "记录客户需求，下次好对接"},
                            {"day": 14, "action": "第1阶段总结", "detail": "赚了多少钱？有哪些问题？"}
                        ],
                        "milestone": "完成5单以上，获得真实评价"
                    }
                },
                "warning": "前期价格可以低，但服务质量要高",
                "success_criteria": "第14天完成5单，获得好评"
            }
        
        elif direction == "私域卖货":
            return {
                "phase": "冷启动期",
                "duration": "第1-14天",
                "goal": "建立卖货基础，获得第一批订单",
                "weekly_plan": {
                    "week1": {
                        "days": [
                            {"day": 1, "action": "确定卖什么产品", "detail": "零食、饰品、日用品？"},
                            {"day": 2, "action": "找货源", "detail": "1688、拼多多商家谈代发"},
                            {"day": 3, "action": "整理现有微信好友", "detail": "分类标签，了解需求"},
                            {"day": 4, "action": "发布第一条卖货文案", "detail": "真实、不让人反感"},
                            {"day": 5, "action": "分析哪些人感兴趣", "detail": "谁问了？谁买了？"},
                            {"day": 6, "action": "优化产品和文案", "detail": "根据反馈调整"},
                            {"day": 7, "action": "第一周总结", "detail": "有订单了吗？"}
                        ],
                        "milestone": "获得第一批订单"
                    },
                    "week2": {
                        "days": [
                            {"day": 8, "action": "建立客户群", "detail": "把买过的人拉群"},
                            {"day": 9, "action": "设计促单活动", "detail": "限时优惠、满减"},
                            {"day": 10, "action": "群内发布活动", "detail": "让老客户带新客户"},
                            {"day": 11, "action": "一对一跟进有意向客户", "detail": "主动询问需求"},
                            {"day": 12, "action": "发布新产品", "detail": "测试新品反应"},
                            {"day": 13, "action": "收集反馈，优化", "detail": "大家想要什么？"},
                            {"day": 14, "action": "第1阶段总结", "detail": "有多少复购？"}
                        ],
                        "milestone": "有复购，建立初步客户群"
                    }
                },
                "warning": "不要只想着赚熟人钱，要开拓新客户",
                "success_criteria": "第14天有10个以上成交客户"
            }
        
        else:
            # 默认通用方案
            return {
                "phase": "冷启动期",
                "duration": "第1-14天",
                "goal": "完成启动，准备变现",
                "weekly_plan": {
                    "week1": {
                        "days": [
                            {"day": "1-2", "action": "了解方向，学习基础", "detail": "找教程，看案例"},
                            {"day": "3-4", "action": "准备工具和素材", "detail": "注册账号，准备内容"},
                            {"day": "5-7", "action": "产出第一批内容/产品", "detail": "不要追求完美，先做出来"}
                        ],
                        "milestone": "有产出"
                    },
                    "week2": {
                        "days": [
                            {"day": "8-10", "action": "发布/销售", "detail": "让更多人看到"},
                            {"day": "11-13", "action": "收集反馈，优化", "detail": "哪里不好改哪里"},
                            {"day": "14", "action": "复盘总结", "detail": "方向对不对？"}
                        ],
                        "milestone": "第一笔订单/流量"
                    }
                },
                "warning": "先跑通最小闭环",
                "success_criteria": "验证方向可行"
            }
    
    def _generate_phase2(self, user: Dict, direction: str) -> Dict:
        """生成成长期方案（15-45天）"""
        return {
            "phase": "成长期",
            "duration": "第15-45天",
            "goal": "建立稳定收入，扩大规模",
            "key_actions": [
                "优化转化率",
                "扩大流量来源",
                "提升客单价",
                "建立 SOP"
            ],
            "milestone": "月收入达到目标的50%",
            "income_target": int(user.get('target_income', 5000) * 0.5)
        }
    
    def _generate_phase3(self, user: Dict, direction: str) -> Dict:
        """生成稳定期方案（46-90天）"""
        return {
            "phase": "稳定期",
            "duration": "第46-90天",
            "goal": "建立可持续盈利系统",
            "key_actions": [
                "规模化复制",
                "建立被动收入",
                "打造个人品牌",
                "团队化运作（可选）"
            ],
            "milestone": "月收入达到或超过目标",
            "income_target": user.get('target_income', 5000)
        }
    
    def generate_daily_task(self, direction: str, day: int) -> Dict:
        """生成每日具体任务"""
        tasks = {
            "短视频带货": [
                "刷同领域视频，找灵感",
                "拍摄1-2条视频",
                "发布并数据分析",
                "优化标题和封面",
                "跟进订单发货"
            ],
            "AI文案代写": [
                "查看新订单",
                "完成撰写任务",
                "优化写作模板",
                "回复客户咨询",
                "学习同行动态"
            ],
            "私域卖货": [
                "发朋友圈",
                "回复客户消息",
                "新品推荐",
                "客户回访",
                "群内互动"
            ]
        }
        
        daily_tasks = tasks.get(direction, ["完成当日任务"])
        # 每天选2-3个核心任务
        core_tasks = daily_tasks[:3]
        
        return {
            "day": day,
            "direction": direction,
            "core_tasks": core_tasks,
            "estimated_time": "2-3小时"
        }


def generate_for_user(user_profile: Dict, direction: str) -> Dict:
    """
    为用户生成完整方案
    
    Args:
        user_profile: 用户画像
        direction: 推荐方向
    
    Returns:
        完整方案
    """
    generator = ProposalGenerator()
    return generator.generate_proposal(user_profile, direction)


if __name__ == "__main__":
    # 测试
    user = {
        "time_per_day": 3,
        "budget": 1000,
        "skills": ["会拍照", "会用手机剪辑"],
        "target_income": 5000
    }
    
    proposal = generate_for_user(user, "短视频带货")
    print(json.dumps(proposal, ensure_ascii=False, indent=2))
