#!/usr/bin/env python3
"""
教培机构私域运营 Agent 核心工具
支持招生策略、社群运营、话术生成、数据分析等功能
"""

import json
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional


class EduPrivateOperations:
    """教培机构私域运营工具类"""
    
    def __init__(self):
        self.industry_metrics = {
            "cac": {"excellent": 200, "good": 400, "poor": float('inf')},
            "trial_conversion": {"excellent": 0.4, "good": 0.25, "poor": 0},
            "community_activity": {"excellent": 0.15, "good": 0.08, "poor": 0},
            "renewal_rate": {"excellent": 0.85, "good": 0.70, "poor": 0},
            "referral_rate": {"excellent": 0.30, "good": 0.15, "poor": 0}
        }
    
    def generate_enrollment_plan(self, institution: Dict) -> Dict:
        """
        生成招生方案
        institution: {
            "name": 机构名称,
            "type": K12/素质教育/职业教育/...,
            "scale": 小班/中型/大型,
            "target_age": 目标年龄段,
            "pain_point": 主要痛点
        }
        """
        plan = {
            "target_persona": self._generate_persona(institution),
            "channels": self._generate_channels(institution),
            "conversion_path": self._generate_conversion_path(institution),
            "timeline": self._generate_timeline(institution),
            "budget_estimate": self._estimate_budget(institution),
            "kpis": self._generate_kpis(institution)
        }
        return plan
    
    def _generate_persona(self, inst: Dict) -> Dict:
        """生成目标客户画像"""
        inst_type = inst.get("type", "K12")
        age_range = inst.get("target_age", "6-15岁")
        
        persona_templates = {
            "K12": {
                "age_range": "25-45岁",
                "relation": "孩子父母(妈妈为主)",
                "occupation": "都市白领/中产家庭",
                "core_concerns": ["孩子的学习成绩", "升学压力", "综合素质培养"],
                "decision_factors": ["口碑评价", "师资力量", "距离便利", "价格"]
            },
            "素质教育": {
                "age_range": "28-45岁",
                "relation": "孩子父母",
                "occupation": "中产及以上家庭",
                "core_concerns": ["兴趣培养", "艺术修养", "体质健康"],
                "decision_factors": ["专业资质", "教学环境", "成果展示"]
            },
            "职业教育": {
                "age_range": "22-35岁",
                "relation": "学员本人",
                "occupation": "职场新人/转行者",
                "core_concerns": ["就业前景", "证书含金量", "学习时间灵活度"],
                "decision_factors": ["品牌知名度", "课程实用性", "价格"]
            }
        }
        
        return persona_templates.get(inst_type, persona_templates["K12"])
    
    def _generate_channels(self, inst: Dict) -> List[Dict]:
        """生成获客渠道"""
        channels = [
            {
                "channel": "短视频平台(抖音/视频号)",
                "priority": "高",
                "cost": "低(内容成本)",
                "conversion": "中",
                "action": [
                    "发布校区日常/学员作品/教学成果",
                    "投放在线体验课广告",
                    "评论区私信转化"
                ]
            },
            {
                "channel": "本地微信社群",
                "priority": "高",
                "cost": "低(人情成本)",
                "conversion": "高",
                "action": [
                    "加入小区/学校家长群",
                    "异业合作(书店/文具店)",
                    "社区活动赞助"
                ]
            },
            {
                "channel": "大众点评/美团",
                "priority": "中",
                "cost": "中(平台入驻+推广)",
                "conversion": "中",
                "action": [
                    "优化店铺评分(>4.8)",
                    "推出体验课套餐",
                    "引导好评沉淀"
                ]
            },
            {
                "channel": "地推/社区活动",
                "priority": "中",
                "cost": "中(人力+物料)",
                "conversion": "中",
                "action": [
                    "学校门口/商场摆点",
                    "免费测评/资料领取",
                    "现场预约体验"
                ]
            },
            {
                "channel": "老带新/转介绍",
                "priority": "高",
                "cost": "低(奖励成本)",
                "conversion": "高",
                "action": [
                    "设置转介绍奖励机制",
                    "老学员作品展示",
                    "家长口碑激励"
                ]
            }
        ]
        return channels
    
    def _generate_conversion_path(self, inst: Dict) -> List[Dict]:
        """生成转化路径"""
        return [
            {
                "stage": "认知",
                "touch_point": "刷到短视频/看到地推",
                "action": "引导添加微信",
                "copy": "免费领取【XX测评】+【学习规划方案】"
            },
            {
                "stage": "兴趣",
                "touch_point": "朋友圈/社群内容",
                "action": "预约免费体验课",
                "copy": "本周开放20个体验名额，扫码预约"
            },
            {
                "stage": "考虑",
                "touch_point": "体验课进行中",
                "action": "课后1v1沟通",
                "copy": "根据孩子情况定制学习方案"
            },
            {
                "stage": "决策",
                "touch_point": "体验课后24小时",
                "action": "限时优惠促进成交",
                "copy": "本月报名立减XX元，赠送XX资料包"
            },
            {
                "stage": "成交",
                "touch_point": "报名后",
                "action": "拉入学员群+学情跟进",
                "copy": "欢迎加入XX大家庭！"
            }
        ]
    
    def _generate_timeline(self, inst: Dict) -> Dict:
        """生成时间规划"""
        return {
            "week_1": [
                "完成账号矩阵搭建(抖音/视频号/小红书)",
                "发布首批内容(5-10条)",
                "启动本地社群渗透"
            ],
            "week_2": [
                "发布首批体验课招募",
                "地推+社区活动启动",
                "老带新机制上线"
            ],
            "month_1": [
                "收集首批体验数据",
                "优化转化话术",
                "启动社群日常运营"
            ],
            "quarter_goal": [
                "月均获客100+",
                "体验课转化率>30%",
                "社群活跃度>10%"
            ]
        }
    
    def _estimate_budget(self, inst: Dict) -> Dict:
        """预估预算"""
        scale = inst.get("scale", "中型")
        budget_map = {
            "小班": {"monthly": "3000-5000元", "items": ["内容制作", "广告投放", "活动物料"]},
            "中型": {"monthly": "8000-15000元", "items": ["平台推广", "人员激励", "活动费用"]},
            "大型": {"monthly": "20000+元", "items": ["团队配置", "品牌投放", "系统工具"]}
        }
        return budget_map.get(scale, budget_map["中型"])
    
    def _generate_kpis(self, inst: Dict) -> Dict:
        """生成KPI指标"""
        return {
            "acquisition": {
                "monthly_leads": 100,
                "channel_efficiency": {"organic": "40%", "paid": "30%", "referral": "30%"}
            },
            "conversion": {
                "trial_to_paid": ">30%",
                "avg_cycle": "7-14天"
            },
            "retention": {
                "renewal_rate": ">80%",
                "churn_rate": "<10%"
            },
            "economics": {
                "cac_target": "<300元",
                "ltv": ">3000元",
                "ltv_cac_ratio": ">3"
            }
        }
    
    def generate_community_sop(self, inst: Dict) -> Dict:
        """
        生成社群运营SOP
        """
        sop = {
            "group_setup": {
                "group_type": self._get_group_type(inst),
                "group_name": f"【{inst.get('name', 'XX机构')}】XX家长交流群",
                "welcome_msg": self._generate_welcome_msg(inst),
                "group_rules": [
                    "禁止广告/链接/外部招生信息",
                    "友善交流，尊重他人",
                    "问题咨询请@群主/助教"
                ]
            },
            "daily_content": self._generate_daily_content(inst),
            "weekly_routine": self._generate_weekly_routine(inst),
            "activation_strategy": self._generate_activation_strategy(inst),
            "conversion_nodes": self._generate_conversion_nodes(inst),
            "forbidden_items": [
                "频繁刷屏广告",
                "负面情绪传播",
                "竞品提及",
                "未经验证的信息转发"
            ]
        }
        return sop
    
    def _get_group_type(self, inst: Dict) -> str:
        """获取社群类型"""
        type_map = {
            "K12": "年级群/学科群",
            "素质教育": "兴趣培养群",
            "职业教育": "学员学习群"
        }
        return type_map.get(inst.get("type", "K12"), "家长交流群")
    
    def _generate_welcome_msg(self, inst: Dict) -> str:
        """生成入群话术"""
        return f"""🎉 欢迎加入【{inst.get('name', 'XX机构')}】大家庭！

📚 我们是专注于{inst.get('type', '学科培训')}的教育机构

📋 群内福利：
• 每周学习资料免费领
• 名师答疑解惑
• 独家活动优先参与
• 家长育儿干货分享

📌 群规提醒：
请勿发广告/链接，共同维护良好氛围～

有疑问请@群主或私信助教老师

让我们一起见证孩子的成长！🌟"""
    
    def _generate_daily_content(self, inst: Dict) -> List[Dict]:
        """生成每日内容安排"""
        return [
            {
                "time": "07:30-08:00",
                "type": "早安问候",
                "content": "励志语/今日学习小目标",
                "template": "☀️ 周X早安！新的一天，新的开始~\n今日小目标：XXX\n打卡接龙：+1"
            },
            {
                "time": "09:00-10:00",
                "type": "知识干货",
                "content": "学习技巧/考点分析",
                "template": "📚 【每日学习】\n今日分享：XXX\n收藏保存，学习更高效！"
            },
            {
                "time": "12:00-13:00",
                "type": "学员展示",
                "content": "作业/作品/进步展示",
                "template": "⭐ 【学员风采】\n恭喜XXX同学完成XX任务！\n表现：XXX\n#成长记录 #学员风采"
            },
            {
                "time": "15:00-16:00",
                "type": "互动问答",
                "content": "趣味知识问答",
                "template": "🤔 【有奖问答】\n问题：XXX\n首位答对家长可获得XX奖励~\n快来留言吧！"
            },
            {
                "time": "19:30-20:30",
                "type": "家长课堂",
                "content": "育儿经验/教育方法",
                "template": "📖 【家长课堂】\n今晚分享主题：XXX\n主讲人：XXX\n预约提醒：记得来听哦~"
            },
            {
                "time": "21:00-22:00",
                "type": "好评互动",
                "content": "感谢反馈/学员进步",
                "template": "💝 【今日好评】\n感谢XX家长的认可！\n孩子进步点：XXX\n#家长认可 #教学成果"
            }
        ]
    
    def _generate_weekly_routine(self, inst: Dict) -> Dict:
        """生成每周固定活动"""
        return {
            "周一": "周一晨读打卡(07:30)",
            "周二": "知识小测验(19:00)",
            "周三": "家长课堂(20:00)",
            "周四": "优秀作业展(12:00)",
            "周五": "周末活动预告(19:00)",
            "周六": "直播公开课(10:00)",
            "周日": "本周总结+下周计划(18:00)"
        }
    
    def _generate_activation_strategy(self, inst: Dict) -> List[Dict]:
        """生成激活策略"""
        return [
            {
                "strategy": "打卡激励",
                "mechanism": "连续打卡7天/30天解锁不同奖励",
                "rewards": {"7天": "学习资料包", "30天": "课时赠送"}
            },
            {
                "strategy": "积分体系",
                "mechanism": "发言/提问/分享/邀请都可积分",
                "rewards": {"积分兑换": "周边礼品/课时折扣"}
            },
            {
                "strategy": "荣誉榜单",
                "mechanism": "周冠军/月冠军公示",
                "rewards": {"榜单展示": "增强参与感"}
            },
            {
                "strategy": "限时福利",
                "mechanism": "特定时段专属优惠",
                "rewards": {"秒杀": "体验课/资料包/周边"}
            }
        ]
    
    def _generate_conversion_nodes(self, inst: Dict) -> List[Dict]:
        """生成转化节点"""
        return [
            {
                "trigger": "入群48小时内",
                "action": "私信+电话",
                "content": "了解孩子情况，预约体验",
                "copy": "您好！看到您加入了我们的家长群，想了解一下孩子目前在XX方面的学习情况，方便给您推荐适合的课程~"
            },
            {
                "trigger": "活跃用户(发言3次+)",
                "action": "邀请体验课",
                "content": "免费体验+1v1评估",
                "copy": "您好！看您一直关注孩子的教育，我们正好有免费的体验课机会，可以给孩子做一个全面的学习评估，需要预约吗？"
            },
            {
                "trigger": "体验课结束",
                "action": "限时优惠",
                "content": "当日报名优惠",
                "copy": "感谢您今天的参与！今天报名可以享受XX优惠（仅限今天），想了解更多课程详情吗？"
            },
            {
                "trigger": "学期结束前1个月",
                "action": "续费提醒",
                "content": "早续费早优惠",
                "copy": "您好！下学期续费窗口已开启，早续费可享受XX优惠，名额有限，欢迎联系我们~"
            }
        ]
    
    def generate_moments_content(self, inst: Dict, month_theme: str = "") -> Dict:
        """
        生成朋友圈内容日历
        """
        content_calendar = {
            "monthly_theme": month_theme or "春季成长季",
            "weekly_plan": self._generate_weekly_content_plan(inst),
            "content_templates": self._generate_content_templates(inst),
            "posting_schedule": {
                "morning": {"time": "07:30-08:30", "type": "早安/励志/干货"},
                "noon": {"time": "12:00-13:00", "type": "学员展示/好评"},
                "evening": {"time": "20:00-22:00", "type": "课程推广/活动"}
            },
            "interaction_tips": [
                "发布后1小时内回复所有评论",
                "用疑问句引导评论互动",
                "适当使用位置标签增加曝光",
                "配合Dou+投放高互动内容"
            ]
        }
        return content_calendar
    
    def _generate_weekly_content_plan(self, inst: Dict) -> List[Dict]:
        """生成每周内容计划"""
        return [
            {
                "day": "周一",
                "theme": "成长励志",
                "content_type": "早安+干货",
                "ratio": "3:7干货",
                "examples": [
                    "新一周开始，鼓励孩子坚持",
                    "本周学习计划制定方法"
                ]
            },
            {
                "day": "周二",
                "theme": "教学成果",
                "content_type": "学员作品/成绩",
                "ratio": "1:9成果",
                "examples": [
                    "学员进步案例分享",
                    "前后对比展示"
                ]
            },
            {
                "day": "周三",
                "theme": "专业知识",
                "content_type": "学习方法/考点",
                "ratio": "8:2专业",
                "examples": [
                    "期中/期末备考技巧",
                    "各科学习方法论"
                ]
            },
            {
                "day": "周四",
                "theme": "互动活动",
                "content_type": "问答/投票/福利",
                "ratio": "5:5互动",
                "examples": [
                    "趣味知识问答",
                    "家长投票：孩子最需要什么"
                ]
            },
            {
                "day": "周五",
                "theme": "学员风采",
                "content_type": "课堂日常/活动",
                "ratio": "2:8日常",
                "examples": [
                    "课堂精彩瞬间",
                    "活动花絮"
                ]
            },
            {
                "day": "周六",
                "theme": "活动推广",
                "content_type": "体验课/公开课",
                "ratio": "1:9推广",
                "examples": [
                    "周末体验课招募",
                    "公开课预约"
                ]
            },
            {
                "day": "周日",
                "theme": "家长沟通",
                "content_type": "育儿经验/好评",
                "ratio": "4:6沟通",
                "examples": [
                    "家长教育心得",
                    "学员好评截图"
                ]
            }
        ]
    
    def _generate_content_templates(self, inst: Dict) -> Dict:
        """生成内容模板"""
        return {
            "early_morning": [
                "☀️ 周{day}早安！\n\n新的一周，新的开始！\n今天也要加油鸭～\n\n#学习打卡 #XX机构",
                "🌟 早起的鸟儿有虫吃~\n\n今日份学习目标：{target}\n\n宝贝们准备好了吗？\n评论区打卡接龙！\n\n#早安 #学习"
            ],
            "achievement": [
                "🎉 恭喜{student}同学！\n\n本次考试进步{score}分\n排名提升{percent}%\n\n努力的汗水终有回报💪\n\n#学员进步 #XX机构",
                "⭐ 今日优秀作业来自{student}！\n\n作业完成度：100%\n知识点掌握：优秀\n\n值得所有同学学习！\n\n#优秀作业 #学习记录"
            ],
            "knowledge": [
                "📚 【每日干货】\n\n{subject}学习技巧第{num}期\n\n要点：\n1. {point1}\n2. {point2}\n3. {point3}\n\n收藏起来慢慢看！\n\n#学习方法 #XX机构",
                "🎯 【考点速记】\n\n{topic}核心知识点\n\n考试经常考，快记下来！\n\n#考点 #学习资料"
            ],
            "trial_invitation": [
                "🔥 免费体验课来啦！\n\n适合：{target_grade}年级\n科目：{subject}\n时间：{date} {time}\n\n名额有限，扫码预约！\n\n#免费体验 #XX机构",
                "💡 {subject}0元体验课\n\n限量{num}个名额\n专业老师1v1评估\n\n扫码立即报名👇\n\n#体验课 #预约"
            ],
            "praise": [
                "💝 感谢家长的认可！\n\n「{feedback}」\n\n——{parent}家长\n\n您的认可是我们最大的动力！\n\n#家长好评 #XX机构",
                "🏆 又收到家长的肯定！\n\n孩子的进步是我们共同的骄傲\n\n感谢选择{inst_name}\n\n#好评 #教学成果"
            ],
            "activity": [
                "🎈 本周六公开课报名中！\n\n主题：{topic}\n讲师：{teacher}\n时间：{time}\n\n私信预约，名额有限~\n\n#公开课 #XX机构",
                "📢 {activity_name}来啦！\n\n{content}\n\n感兴趣的同学抓紧报名！\n\n#活动 #XX机构"
            ]
        }
    
    def generate_parent_script(self, scenario: str, inst: Dict) -> Dict:
        """
        生成家长沟通话术
        scenario: consultation/renewal/complaint/referral
        """
        scripts = {
            "consultation": {
                "title": "咨询接待话术",
                "phases": [
                    {
                        "phase": "开场破冰",
                        "objective": "了解基本情况",
                        "script": f"""您好！欢迎咨询{inst.get('name', 'XX机构')}～

我是您的课程顾问[姓名]，请问怎么称呼您？

孩子多大了？目前在读哪个年级呢？""",
                        "tips": "语气亲切，不要急于推销"
                    },
                    {
                        "phase": "需求挖掘",
                        "objective": "了解痛点和期望",
                        "script": """请问您是想提升哪方面的能力呢？
之前有在其他机构学习过吗？
对孩子的学习有什么期望和目标？""",
                        "tips": "多问开放式问题，倾听为主"
                    },
                    {
                        "phase": "课程介绍",
                        "objective": "推荐适合课程",
                        "script": """根据您说的情况，我推荐我们的XX课程...

这个课程的优势是：
• [优势1]
• [优势2]
• [优势3]

我们的老师都是[背景]，已经帮助[数量]位学员提升了[成果]""",
                        "tips": "结合前面了解到的需求，有针对性介绍"
                    },
                    {
                        "phase": "邀约体验",
                        "objective": "预约免费体验",
                        "script": """非常推荐您带孩子来体验一下！

本周{maybe_time}我们正好有体验课，可以让孩子感受一下课堂氛围~

免费体验还包括一份学习能力评估报告哦！""",
                        "tips": "强调免费，消除顾虑"
                    }
                ]
            },
            "renewal": {
                "title": "续费话术",
                "phases": [
                    {
                        "phase": "成果回顾",
                        "objective": "展示学习效果",
                        "script": """您好！{student}在我们这里学习已经{period}了～

这段时间的进步：
• {improvement1}
• {improvement2}
• {improvement3}

孩子的努力+老师的专业，效果很明显呢！""",
                        "tips": "用具体数据说话，展示价值"
                    },
                    {
                        "phase": "续费通知",
                        "objective": "说明续费安排",
                        "script": """下学期的课程续费已经开始了～

我们的早鸟优惠是：立减{discount}元
还赠送：{gift}

优惠截止到{deadline}，需要我帮您预留名额吗？""",
                        "tips": "明确优惠截止时间，制造紧迫感"
                    },
                    {
                        "phase": "异议处理",
                        "objective": "解决顾虑",
                        "script": """完全理解您的顾虑～

关于{concern}，我们的解决方案是：
{solution}

其实很多家长一开始也有类似担心，但后来都发现...（案例）""",
                        "tips": "先认可情绪，再提供解决方案"
                    }
                ]
            },
            "complaint": {
                "title": "投诉处理话术",
                "phases": [
                    {
                        "phase": "倾听道歉",
                        "objective": "安抚情绪",
                        "script": """非常抱歉给您带来不好的体验！

您说的这些我完全理解，如果是我也会着急...

能具体跟我说说是怎么回事吗？""",
                        "tips": "先道歉，不要急于解释或推卸"
                    },
                    {
                        "phase": "了解详情",
                        "objective": "掌握全貌",
                        "script": """谢谢您的反馈，我需要了解一下具体情况...

请问这件事是什么时候发生的？
当时是哪位老师/员工接待的？
您希望我们怎么解决呢？""",
                        "tips": "详细记录，表示重视"
                    },
                    {
                        "phase": "解决方案",
                        "objective": "给出补救措施",
                        "script": """非常感谢您的理解！

针对这个问题，我们决定：
1. {measure1}
2. {measure2}
3. {measure3}

您看这样的处理方式可以吗？""",
                        "tips": "给出具体解决方案，不要空口承诺"
                    },
                    {
                        "phase": "后续跟进",
                        "objective": "闭环反馈",
                        "script": """再次为给您带来的不便道歉...

后续我们会{take_action}，避免类似问题再次发生。

请问还有其他问题吗？有什么建议也欢迎提出～""",
                        "tips": "表示会改进，争取转化投诉为忠诚客户"
                    }
                ]
            },
            "referral": {
                "title": "转介绍话术",
                "phases": [
                    {
                        "phase": "感谢回顾",
                        "objective": "唤醒好感",
                        "script": """您好！我是XX机构的课程顾问～

感谢您一直对我们工作的支持！孩子的进步我们也看在眼里，特别开心！""",
                        "tips": "真诚感谢，不要上来就提转介绍"
                    },
                    {
                        "phase": "说明机制",
                        "objective": "介绍福利",
                        "script": """跟您分享个好消息～

我们最近推出了老带新活动：
推荐1位朋友报名，您可以获得{reward1}
朋友报名也可以享受{reward2}

都是实实在在的福利！""",
                        "tips": "双方都有好处，强调互利"
                    },
                    {
                        "phase": "自然请求",
                        "objective": "请求转介绍",
                        "script": """您身边有没有朋友的孩子也在学{subject}呢？

如果有的话，可以把我的微信推荐给他们～
推荐成功报名后，您和朋友的福利我一起安排！""",
                        "tips": "给家长一个自然的推荐理由"
                    }
                ]
            }
        }
        return scripts.get(scenario, scripts["consultation"])
    
    def analyze_data(self, data: Dict) -> Dict:
        """
        分析运营数据
        data: {
            "leads": 来访数,
            "trials": 体验课人数,
            "paid": 付费人数,
            "active": 社群活跃人数,
            "total": 社群总人数,
            "renewals": 续费人数,
            "total_students": 总学员数,
            "cost": 总成本,
            "revenue": 总营收
        }
        """
        analysis = {
            "acquisition_metrics": self._analyze_acquisition(data),
            "conversion_metrics": self._analyze_conversion(data),
            "community_metrics": self._analyze_community(data),
            "retention_metrics": self._analyze_retention(data),
            "economics": self._analyze_economics(data),
            "benchmark_comparison": self._compare_benchmark(data),
            "recommendations": self._generate_recommendations(data)
        }
        return analysis
    
    def _analyze_acquisition(self, data: Dict) -> Dict:
        """分析获客指标"""
        leads = data.get("leads", 0)
        cost = data.get("cost", 0)
        cac = cost / leads if leads > 0 else 0
        
        return {
            "total_leads": leads,
            "cac": round(cac, 2),
            "cac_level": self._get_level("cac", cac),
            "cost_breakdown": {
                "ads": cost * 0.4,
                "content": cost * 0.3,
                "activities": cost * 0.3
            } if cost > 0 else {}
        }
    
    def _analyze_conversion(self, data: Dict) -> Dict:
        """分析转化指标"""
        leads = data.get("leads", 1)
        trials = data.get("trials", 0)
        paid = data.get("paid", 0)
        
        trial_rate = trials / leads if leads > 0 else 0
        conversion_rate = paid / trials if trials > 0 else 0
        
        return {
            "leads_to_trial": f"{trial_rate:.1%}",
            "trial_to_paid": f"{conversion_rate:.1%}",
            "overall_conversion": f"{paid/leads:.1%}" if leads > 0 else "0%",
            "trial_rate_level": self._get_level("trial_conversion", trial_rate),
            "conversion_level": self._get_level("trial_conversion", conversion_rate)
        }
    
    def _analyze_community(self, data: Dict) -> Dict:
        """分析社群指标"""
        active = data.get("active", 0)
        total = data.get("total", 1)
        
        activity_rate = active / total if total > 0 else 0
        
        return {
            "total_members": total,
            "active_members": active,
            "activity_rate": f"{activity_rate:.1%}",
            "activity_level": self._get_level("community_activity", activity_rate),
            "daily_avg_messages": int(data.get("daily_messages", 50)),
            "peak_hours": ["12:00-13:00", "20:00-21:00"]
        }
    
    def _analyze_retention(self, data: Dict) -> Dict:
        """分析留存指标"""
        renewals = data.get("renewals", 0)
        total = data.get("total_students", 1)
        
        renewal_rate = renewals / total if total > 0 else 0
        
        return {
            "renewal_rate": f"{renewal_rate:.1%}",
            "renewal_level": self._get_level("renewal_rate", renewal_rate),
            "churn_rate": f"{1-renewal_rate:.1%}",
            "referral_rate": f"{data.get('referrals', 0)/total:.1%}" if total > 0 else "0%"
        }
    
    def _analyze_economics(self, data: Dict) -> Dict:
        """分析经济指标"""
        cost = data.get("cost", 0)
        revenue = data.get("revenue", 0)
        paid = data.get("paid", 1)
        
        return {
            "total_cost": cost,
            "total_revenue": revenue,
            "profit": revenue - cost,
            "roi": f"{(revenue-cost)/cost*100:.1f}%" if cost > 0 else "N/A",
            "arpu": f"{revenue/paid:.0f}" if paid > 0 else "N/A",
            "ltv": f"{revenue/paid*3:.0f}" if paid > 0 else "N/A"  # 假设LTV=3*ARPU
        }
    
    def _compare_benchmark(self, data: Dict) -> Dict:
        """对标行业基准"""
        trials = data.get("trials", 0)
        leads = data.get("leads", 1)
        trial_rate = trials / leads if leads > 0 else 0
        
        return {
            "vs_cac": f"{data.get('cost', 0)/leads:.0f}元 vs 行业200元" if leads > 0 else "N/A",
            "vs_conversion": f"{trial_rate:.0%} vs 行业40%",
            "vs_activity": f"社群活跃度需提升至15%",
            "vs_renewal": f"续费率需提升至85%"
        }
    
    def _generate_recommendations(self, data: Dict) -> List[str]:
        """生成优化建议"""
        recommendations = []
        
        # CAC 建议
        cac = data.get("cost", 0) / max(data.get("leads", 1), 1)
        if cac > 400:
            recommendations.append("💰 获客成本偏高，建议：1)优化广告投放ROI 2)增加口碑转介绍比例 3)提升内容获客占比")
        
        # 转化建议
        trials = data.get("trials", 0)
        leads = data.get("leads", 1)
        if trials / leads < 0.3:
            recommendations.append("📱 来访-体验转化率低，建议：1)优化首电话术 2)增加体验课频次 3)提供更多诱饵（测评报告等）")
        
        # 社群建议
        active = data.get("active", 0)
        total = data.get("total", 1)
        if active / total < 0.1:
            recommendations.append("💬 社群活跃度低，建议：1)固定每日内容时间 2)增加互动活动 3)培养核心KOL家长")
        
        # 续费建议
        renewals = data.get("renewals", 0)
        students = data.get("total_students", 1)
        if renewals / students < 0.8:
            recommendations.append("📈 续费率有提升空间，建议：1)提前1个月启动续费 2)增加增值服务 3)完善学情反馈")
        
        if not recommendations:
            recommendations.append("🎉 各项指标表现良好！继续保持，优化细节以追求卓越")
        
        return recommendations
    
    def _get_level(self, metric: str, value: float) -> str:
        """获取指标等级"""
        metrics = self.industry_metrics.get(metric, {})
        
        if metric == "cac":  # CAC越低越好
            if value < metrics.get("excellent", 200):
                return "优秀"
            elif value < metrics.get("good", 400):
                return "良好"
            else:
                return "需改进"
        else:  # 其他指标越高越好
            if value >= metrics.get("excellent", 0.85):
                return "优秀"
            elif value >= metrics.get("good", 0.70):
                return "良好"
            else:
                return "需改进"
    
    def generate_activity_plan(self, activity_type: str, inst: Dict) -> Dict:
        """
        生成活动策划方案
        activity_type: trial/expo/holiday/seasonal
        """
        templates = {
            "trial": {
                "name": "免费体验课",
                "duration": "60-90分钟",
                "objectives": ["吸引新客户", "展示教学实力", "收集潜在客户信息"],
                "flow": [
                    {"time": "0-10min", "content": "签到+资料收集", "staff": "课程顾问"},
                    {"time": "10-30min", "content": "公开课/Demo演示", "staff": "主讲教师"},
                    {"time": "30-45min", "content": "互动答疑", "staff": "主讲教师"},
                    {"time": "45-60min", "content": "1v1咨询", "staff": "课程顾问"}
                ],
                "materials": ["签到表", "宣传单页", "体验课报名表", "优惠券"],
                "kpis": {"target_attendance": 20, "target_conversion": "30%", "cost_per_head": "50元"}
            },
            "expo": {
                "name": "教育展会/讲座",
                "duration": "2-3小时",
                "objectives": ["品牌曝光", "行业影响力", "批量获客"],
                "flow": [
                    {"time": "开场", "content": "品牌宣讲", "staff": "校长"},
                    {"time": "核心", "content": "专家讲座/干货分享", "staff": "特邀专家"},
                    {"time": "互动", "content": "家长问答", "staff": "全体"},
                    {"time": "收尾", "content": "课程咨询+报名", "staff": "课程顾问"}
                ],
                "materials": ["易拉宝", "宣传册", "体验卡", "抽奖券"],
                "kpis": {"target_attendance": 100, "target_leads": 50, "cost": "5000元"}
            },
            "holiday": {
                "name": "节日主题活动",
                "duration": "1-2小时",
                "objectives": ["社群激活", "家长粘性", "品牌温度"],
                "flow": [
                    {"time": "开场", "content": "节日祝福+活动介绍", "staff": "班主任"},
                    {"time": "互动", "content": "亲子活动/游戏", "staff": "教师团队"},
                    {"time": "展示", "content": "学员成果展示", "staff": "学员"},
                    {"time": "留念", "content": "合影+分享", "staff": "全体"}
                ],
                "materials": ["活动道具", "奖品", "背景板", "摄影设备"],
                "kpis": {"target_participation": "80%", "photo_sharing": "50%", "feedback_score": "4.8+"}
            }
        }
        
        activity = templates.get(activity_type, templates["trial"])
        activity["inst_name"] = inst.get("name", "XX机构")
        activity["inst_type"] = inst.get("type", "教培")
        
        return activity


# CLI 入口
if __name__ == "__main__":
    import sys
    
    tool = EduPrivateOperations()
    
    # 示例调用
    example_inst = {
        "name": "学而思培优",
        "type": "K12",
        "scale": "中型",
        "target_age": "6-15岁",
        "pain_point": "招生难"
    }
    
    # 测试功能
    print("=== 教培机构私域运营 Agent ===\n")
    
    # 1. 招生方案
    print("1. 招生方案生成中...")
    plan = tool.generate_enrollment_plan(example_inst)
    print(json.dumps(plan, ensure_ascii=False, indent=2))
    
    # 2. 社群SOP
    print("\n2. 社群SOP生成中...")
    sop = tool.generate_community_sop(example_inst)
    print(json.dumps(sop, ensure_ascii=False, indent=2))
    
    # 3. 朋友圈内容
    print("\n3. 朋友圈内容日历生成中...")
    content = tool.generate_moments_content(example_inst, "春季成长季")
    print(json.dumps(content, ensure_ascii=False, indent=2))
    
    print("\n✅ 所有功能测试完成！")
