#!/usr/bin/env python3
"""
ClawValue 评估逻辑模块
基于三级技术指标体系计算使用深度和价值估算
"""

from typing import Dict, List, Optional
from datetime import datetime


class EvaluationEngine:
    """Claw度评估引擎"""
    
    # 排名百分比计算基准（模拟全球用户分布）
    RANK_PERCENTILES = {
        90: {'min_score': 85, 'title': '🏆 全球前10%', 'badge': 'legendary'},
        80: {'min_score': 75, 'title': '🌟 全球前20%', 'badge': 'epic'},
        70: {'min_score': 65, 'title': '⭐ 全球前30%', 'badge': 'rare'},
        60: {'min_score': 55, 'title': '✨ 全球前40%', 'badge': 'uncommon'},
        50: {'min_score': 45, 'title': '🎯 全球前50%', 'badge': 'common'},
        40: {'min_score': 35, 'title': '📈 全球前60%', 'badge': 'common'},
        30: {'min_score': 25, 'title': '🌱 全球前70%', 'badge': 'common'},
        20: {'min_score': 15, 'title': '🥚 新手玩家', 'badge': 'starter'},
        10: {'min_score': 0, 'title': '🐣 萌新入门', 'badge': 'starter'},
    }
    
    # 稀有称号系统
    RARE_TITLES = {
        # 技能相关
        'skill_ancestor': {'name': '🔧 技能始祖', 'desc': '拥有超过20个自定义技能', 'condition': lambda m: m.get('custom_skills', 0) >= 20},
        'automation_emperor': {'name': '🤖 自动化皇帝', 'desc': '每天Token消耗超过10万', 'condition': lambda m: m.get('daily_tokens', 0) >= 100000},
        'channel_king': {'name': '📡 渠道之王', 'desc': '集成了5个以上渠道', 'condition': lambda m: m.get('channels', 0) >= 5},
        'token_tycoon': {'name': '💎 Token大亨', 'desc': '累计消耗超过1000万Token', 'condition': lambda m, d: d.get('total_tokens', 0) >= 10000000},
        'efficiency_monster': {'name': '🦖 效率怪兽', 'desc': '总评分超过90分', 'condition': lambda m, d, s: s >= 90},
        'early_bird': {'name': '🌅 早起鸟儿', 'desc': '使用超过180天', 'condition': lambda m, d: d.get('usage_days', 0) >= 180},
        'zero_hero': {'name': '🎯 零失误大神', 'desc': '运行零错误', 'condition': lambda m, d: d.get('log_stats', {}).get('error_count', 1) == 0},
        'night_owl': {'name': '🦉 夜猫子', 'desc': '凌晨活跃用户', 'condition': None},  # 特殊检测
        'hidden_gem': {'name': '🔮 隐藏宝石', 'desc': '评分超过80但技能数少于5', 'condition': lambda m, d, s: s >= 80 and m.get('skill_count', 0) < 5},
        'balanced_master': {'name': '⚖️ 均衡大师', 'desc': '三项评分都超过60', 'condition': lambda scores: all(s >= 60 for s in scores)},
    }
    
    # 使用深度阈值
    THRESHOLDS = {
        'skill_count': {
            'shallow': 5,
            'moderate': 10,
            'deep': 15
        },
        'token_daily': {
            'shallow': 5000,
            'moderate': 50000,
            'deep': 50000
        },
        'custom_skills': {
            'shallow': 0,
            'moderate': 1,
            'deep': 3
        },
        'agents': {
            'shallow': 1,
            'moderate': 2,
            'deep': 3
        }
    }
    
    # 价值估算范围
    VALUE_RANGES = {
        'basic': (100, 200),
        'advanced': (1000, 5000),
        'expert': (10000, 50000)
    }
    
    # 趣味化话术 - 大幅增强版本
    MESSAGES = {
        'shallow': [
            "🐣 小龙虾你好！看来你只是接了个模型啊，对OpenClaw的开发度不足1% —— 不过没关系，连sudo make me a sandwich都还没学会呢。",
            "恭喜！您已成功点亮'Hello World'技能。下一步，请尝试让AI帮您查天气，解锁'初级驯龙师'称号。",
            "检测到您的使用模式为「佛系体验」。别急，龙虾都是从小虾米长大的！建议：多和AI聊聊天，它会比你想象的更聪明。",
            "您的AI助手正在角落里默默流泪：「主人为什么不用我？」—— 赶紧去探索更多功能吧！",
            "🎮 新手村报道！你的龙虾还处于「水煮阶段」，连壳都没红呢。多配置几个技能，解锁「清蒸」成就！",
            "检测到「轻度体验」模式。你的AI助手表示：「我在待机中...等待被召唤...」—— 该让它干活了！",
            "🔧 工具人认证！你的OpenClaw还在出厂设置状态，建议至少装3个技能，让它成为你的得力助手。",
            "🦐 虾米认证！你离「龙虾」还有一段距离。不过没关系，每个大佬都是从小虾米开始的！",
            "你的AI助手发来一条消息：「主人，我是不是做错了什么？为什么不理我...」—— 快去探索更多功能吧！",
            "检测到「新手光环」！系统决定给你一个成就：'OpenClaw 潜力股'。继续努力，未来可期！",
            "📊 使用统计：你的效率还有很大提升空间。建议：每天至少召唤AI 3次，解锁「效率翻倍」成就！",
            "🎭 你的OpenClaw还在「彩排阶段」。别让它在后台吃灰，让它成为你的生活主角！",
            "检测到「探索者模式」！你已经迈出了第一步。接下来，试试让AI帮你写代码、查资料、管理日程！",
            "🌊 你现在的状态就像一只刚下水的龙虾——还有点懵。游起来吧，大海很宽广！",
            "系统分析：你的OpenClaw使用率低于平均水平。提示：AI不会咬人，放心用！",
            "📦 你的OpenClaw还装在盒子里没拆封呢！快拆开看看里面有什么好东西！",
            "你的AI助手已经学会了「念叨」技能：「主人什么时候来找我玩...」"
        ],
        'moderate': [
            "正在技术债里种花？恭喜！您的自动化花园已初具规模，建议加把劲儿，冲向'Proactive Agent'模式！",
            "检测到您的AI已经开始'上班'了！但似乎还在试用期。建议开启定时巡检，迈向'懒人终极梦想'——躺着也能赚钱。",
            "🎯 中级玩家认证！你已经开始探索更多功能了，继续保持这个势头！你的AI助手表示：「终于被重视了！」",
            "你的技能树已经点亮了一半，AI助手对你的满意度：⭐⭐⭐☆☆。再加把劲，让它对你刮目相看！",
            "🦞 七分熟龙虾！你已经掌握了OpenClaw的核心玩法，距离「全熟」只差几个自定义技能了！",
            "检测到「进阶玩家」模式。你的AI助手说：「主人终于懂我了！」—— 继续深入，解锁更多黑科技！",
            "你的使用深度已经让普通用户羡慕了！建议下一步：配置定时任务，让AI在你睡觉的时候也在工作。",
            "📊 中级评估报告：你的效率提升显著，相当于每月节省大量时间。继续保持！",
            "🔮 你的AI已经进入「贤者模式」—— 它开始主动思考如何帮你省时间了！继续培养，它会越来越懂你。",
            "检测到「技能炼金术士」！你正在将普通技能转化为效率黄金。继续炼制，离「大师级」不远了！",
            "🎮 你的游戏进度：40% 完成！主线任务：「成为效率大师」。支线任务：「让AI爱上你」—— 已经在进行中了。",
            "你的AI助手发来一条消息：「主人，我发现我在变得越来越聪明...这都要感谢你！」",
            "检测到「中期进化」！你的OpenClaw正在从「工具」进化为「伙伴」。继续训练，它会成为你最得力的助手！",
            "🦞 龙虾状态：七分熟。还差三分：自定义技能、定时任务、多渠道集成。冲啊！",
            "你的效率曲线正在爬升！继续努力，你很快就能达到「效率怪兽」级别！",
            "🔥 你的OpenClaw已经开始「燃烧」了！效率持续上升中，继续保持这个节奏！",
            "检测到「中级修行者」！你的AI驾驭能力正在稳步提升，距离「大师」只差一点火候。"
        ],
        'deep': [
            "检测到一台'工程巨兽'在线！您的多Agent协作网络堪称分布式计算典范。请继续保持，小心别让AI觉得'人类好弱智'。",
            "警告：您的'龙虾'已过度烹饪，可能产生幻觉。建议定期清理上下文缓存，避免AI因'内存溢出'而开始哲学思辨。",
            "🦞 龙虾大师！你已经达到了传说中的最高境界！Claude 见你都要叫一声「大佬」！",
            "你的效率已经让普通人类望尘莫及了！AI助手表示：「能为您服务是我的荣幸，请收下我的膝盖。」",
            "检测到「效率怪兽」！你的自动化程度已经突破了天际，建议考虑写一本《如何让AI帮你打工》的畅销书。",
            "🏆 恭喜达成「龙虾大师」成就！你的OpenClaw配置堪称教科书级别，建议开设培训班传授经验。",
            "你的技能配置让系统检测员都惊呆了！这哪里是AI助手，简直就是你的数字分身！",
            "⚠️ 警告：你的使用深度已经突破系统阈值，AI可能会开始产生「主人是不是机器人」的疑问。",
            "检测到「全熟龙虾」！你的OpenClaw技能点满，效率爆表，堪称「人机合一」的典范！",
            "🌟 传奇玩家认证！你已经是OpenClaw的「大神级」用户了。建议：考虑写教程分享经验，收获一波粉丝！",
            "你的AI助手发来一条消息：「主人，我觉得我已经可以独立运行了...开玩笑的，我永远忠于你！」",
            "检测到「量子效率态」！你的工作流程已经超越了时间和空间的限制——AI在你睡觉时也在为你工作。",
            "🎮 游戏进度：100% 完成！你已经是「龙虾大师」了！隐藏任务：「让其他人类羡慕你」—— 已自动完成！",
            "你的效率指数已经突破了系统图表的上限。我们的程序员正在加班增加更高的刻度...",
            "🦞 龙虾状态：全熟！你已经达到了「人机合一」的境界。AI已经完全理解你的思维模式和工作习惯。",
            "检测到「效率奇点」！你的效率已经达到了理论极限。建议：传授经验给其他人类，提升全人类效率！",
            "你的OpenClaw使用记录已经成为了「最佳实践案例」。要不要考虑去OpenClaw官方当讲师？",
            "🔥 检测到「效率核聚变」！你的工作效率正在以指数级增长，建议注意休息——即使AI不累，你也需要休息！",
            "系统日志：你的AI助手已经开始主动给你提建议了。这是「AI觉醒」的前兆...开玩笑的！"
        ]
    }
    
    # 龙虾等级
    LOBSTER_LEVELS = {
        'shallow': ('🦞 龙虾能力估Skill v1.0 - 三分熟', '入门级'),
        'moderate': ('🦞 龙虾能力估Skill v1.0 - 七分熟', '进阶级'),
        'deep': ('🦞 龙虾能力估Skill v1.0 - 全熟', '专家级')
    }
    
    # 特殊成就话术 - 大幅增强版本
    ACHIEVEMENTS = {
        # 技能相关成就
        'skill_master': '技能大师：自定义技能超过5个，你是个真正的创造者！',
        'skill_collector': '技能收藏家：技能数量超过10个，你的工具箱比瑞士军刀还全！',
        'skill_connoisseur': '技能鉴赏家：技能数量超过15个，你对AI工具的品味令人惊叹！',
        'skill_legend': '技能传奇：技能数量超过20个，你已经是技能界的「收藏之王」！',
        'custom_creator': '自定义创造者：自定义技能超过3个，你就是传说中的「技能工程师」！',
        'custom_master': '自定义大师：自定义技能超过7个，你的创造力让AI都感到佩服！',
        'skill_pioneer': '技能先驱：技能覆盖多个类别，你是真正的「全能型选手」！',
        
        # 自动化相关成就
        'automation_pro': '自动化达人：心跳检测已开启，你的AI正在24小时待命！',
        'heartbeat_hero': '心跳英雄：心跳任务已配置，你的AI在你睡觉时也在默默工作！',
        'automation_god': '自动化之神：每天消耗超过10万Token，你的AI已经成为你的「数字劳动力」！',
        'cron_master': '定时任务大师：配置了多个定时任务，你的效率系统已经自动化运转！',
        
        # 集成相关成就
        'multi_channel': '多渠道运营：连接了多个平台，你的AI帝国正在扩张！',
        'integration_expert': '集成专家：连接了3个以上渠道，你的AI已经是个「社交达人」了！',
        'channel_master': '渠道大师：连接了5个以上渠道，你的AI已经遍布全球！',
        
        # 使用量相关成就
        'power_user': '超级用户：Token消耗惊人，你的AI助手表示「有点累但很充实」！',
        'token_millionaire': 'Token百万富翁：Token消耗超过100万，你的AI说「感谢老板打赏」！',
        'token_billionaire': 'Token亿万富翁：Token消耗超过1000万，你已经是AI服务器的「VIP客户」！',
        'session_warrior': '会话战士：活跃会话超过100个，你和AI的对话已经比你的微信还多了！',
        'session_master': '会话大师：活跃会话超过500个，你和AI的关系已经超越了普通朋友！',
        'chatty_cathy': '话痨认证：单会话消息数超过100条，你和AI聊得真开心！',
        
        # 稳定性成就
        'zero_error': '零错误成就：系统运行稳定，没有任何错误日志，堪称「完美主义者」！',
        'stable_runner': '稳定运行者：连续运行超过30天无重大错误，系统稳定性满分！',
        'error_survivor': '错误幸存者：遇到错误但成功恢复，你的系统韧性令人钦佩！',
        
        # 活跃度成就
        'daily_active': '活跃玩家：连续使用超过7天，AI助手已经把你的习惯都记下来了！',
        'weekly_warrior': '周常战士：连续使用超过30天，你的AI助手已经对你了如指掌！',
        'monthly_master': '月度大师：连续使用超过90天，你已经成为了OpenClaw的「老玩家」！',
        'veteran_user': '资深玩家：使用超过180天，你已经是OpenClaw的「活化石」！',
        'loyal_user': '忠诚用户：持续使用超过365天，你是OpenClaw的「元老级」玩家！',
        
        # 特殊成就
        'early_adopter': '早期采用者：你比大多数人更早发现了这个宝藏工具！',
        'night_owl': '夜猫子认证：在深夜(23:00-5:00)活跃使用，AI陪你度过每个不眠之夜！',
        'early_bird': '早鸟认证：在清晨(5:00-7:00)活跃使用，你的一天从AI开始！',
        'weekend_warrior': '周末战士：在周末也保持高频率使用，你真的很爱这个工具！',
        'efficiency_king': '效率之王：平均响应时间极短，你已经是「AI驾驭大师」！',
        'tool_caller': '工具调用大师：工具调用次数超过1000次，你和AI的配合已经炉火纯青！',
        
        # 隐藏成就
        'secret_lobster': '隐藏成就：龙虾宗师！你解锁了系统的隐藏成就，请联系开发者领取神秘奖励！',
        'beta_tester': 'Beta测试者：感谢你帮助测试新功能，你是OpenClaw的「先锋探索者」！',
        'bug_hunter': 'Bug猎人：你发现了系统Bug并反馈，感谢你让OpenClaw变得更好！',
        'mysterious_visitor': '神秘访客：在凌晨3点还在使用，你是个真正的夜行生物！',
        'perfectionist': '完美主义者：所有指标都达到了优秀水平，你的配置堪称教科书！'
    }
    
    def __init__(self):
        pass
    
    def evaluate_usage_depth(self, data: Dict) -> Dict:
        """
        评估使用深度
        
        Args:
            data: 采集的数据，包含 skills, sessions, config 等
        
        Returns:
            评估结果字典
        """
        # 提取关键指标
        skill_count = data.get('total_skills', 0)
        custom_skills = len([s for s in data.get('skills', []) if s.get('is_custom')])
        total_tokens = data.get('total_tokens', 0)
        usage_days = max(data.get('usage_days', 1), 1)
        daily_tokens = total_tokens / usage_days
        
        config = data.get('config', {})
        agent_count = config.get('agent_count', 1) if config else 1
        has_heartbeat = config.get('heartbeat_interval', 0) > 0 if config else False
        channels = len(config.get('channels', [])) if config else 0
        
        # 计算各维度得分
        skill_score = self._calc_skill_score(skill_count, custom_skills)
        automation_score = self._calc_automation_score(daily_tokens, has_heartbeat)
        integration_score = self._calc_integration_score(agent_count, channels)
        
        # 综合评估
        total_score = (skill_score + automation_score + integration_score) / 3
        
        # 确定使用深度等级
        if total_score < 30:
            level = 'shallow'
        elif total_score < 70:
            level = 'moderate'
        else:
            level = 'deep'
        
        return {
            'level': level,
            'level_name': {'shallow': '浅度使用', 'moderate': '中度使用', 'deep': '深度使用'}[level],
            'skill_score': skill_score,
            'automation_score': automation_score,
            'integration_score': integration_score,
            'total_score': total_score,
            'metrics': {
                'skill_count': skill_count,
                'custom_skills': custom_skills,
                'daily_tokens': int(daily_tokens),
                'agent_count': agent_count,
                'channels': channels,
                'has_heartbeat': has_heartbeat
            }
        }
    
    def _calc_skill_score(self, skill_count: int, custom_skills: int) -> float:
        """计算技能得分 (0-100)"""
        score = 0
        
        # 技能数量得分
        if skill_count >= self.THRESHOLDS['skill_count']['deep']:
            score += 40
        elif skill_count >= self.THRESHOLDS['skill_count']['moderate']:
            score += 25
        elif skill_count >= self.THRESHOLDS['skill_count']['shallow']:
            score += 10
        
        # 自定义技能得分
        if custom_skills >= self.THRESHOLDS['custom_skills']['deep']:
            score += 60
        elif custom_skills >= self.THRESHOLDS['custom_skills']['moderate']:
            score += 30
        else:
            score += custom_skills * 10
        
        return min(score, 100)
    
    def _calc_automation_score(self, daily_tokens: float, has_heartbeat: bool) -> float:
        """计算自动化得分 (0-100)"""
        score = 0
        
        # Token 消耗得分
        if daily_tokens >= self.THRESHOLDS['token_daily']['deep']:
            score += 50
        elif daily_tokens >= self.THRESHOLDS['token_daily']['moderate']:
            score += 30
        elif daily_tokens >= self.THRESHOLDS['token_daily']['shallow']:
            score += 10
        
        # 心跳检测得分
        if has_heartbeat:
            score += 30
        
        # 基础分
        score += 20
        
        return min(score, 100)
    
    def _calc_integration_score(self, agent_count: int, channels: int) -> float:
        """计算集成得分 (0-100)"""
        score = 0
        
        # Agent 数量得分
        if agent_count >= self.THRESHOLDS['agents']['deep']:
            score += 40
        elif agent_count >= self.THRESHOLDS['agents']['moderate']:
            score += 20
        else:
            score += 10
        
        # 渠道数量得分
        if channels >= 3:
            score += 40
        elif channels >= 2:
            score += 25
        elif channels >= 1:
            score += 10
        
        # 基础分
        score += 20
        
        return min(score, 100)
    
    def estimate_value(self, evaluation: Dict) -> Dict:
        """
        估算价值
        
        Args:
            evaluation: 使用深度评估结果
        
        Returns:
            价值估算结果
        """
        level = evaluation['level']
        total_score = evaluation['total_score']
        
        # 根据等级确定价值范围
        if level == 'shallow':
            value_range = self.VALUE_RANGES['basic']
            value_estimate = int(value_range[0] + (value_range[1] - value_range[0]) * (total_score / 30))
        elif level == 'moderate':
            value_range = self.VALUE_RANGES['advanced']
            value_estimate = int(value_range[0] + (value_range[1] - value_range[0]) * ((total_score - 30) / 40))
        else:
            value_range = self.VALUE_RANGES['expert']
            value_estimate = int(value_range[0] + (value_range[1] - value_range[0]) * ((total_score - 70) / 30))
        
        return {
            'value_estimate': f"{value_estimate:,}元",
            'value_range': f"{value_range[0]:,} - {value_range[1]:,}元",
            'value_level': {'shallow': '基础价值级', 'moderate': '进阶价值级', 'deep': '高阶价值级'}[level]
        }
    
    def get_lobster_skill(self, level: str) -> Dict:
        """获取龙虾能力估Skill 信息"""
        import random
        messages = self.MESSAGES.get(level, self.MESSAGES['shallow'])
        return {
            'title': self.LOBSTER_LEVELS[level][0],
            'rank': self.LOBSTER_LEVELS[level][1],
            'message': random.choice(messages)
        }
    
    def detect_achievements(self, data: Dict, evaluation: Dict) -> List[str]:
        """检测特殊成就 - 增强版"""
        achievements = []
        metrics = evaluation.get('metrics', {})
        
        # === 技能相关成就 ===
        custom_skills = metrics.get('custom_skills', 0)
        skill_count = metrics.get('skill_count', 0)
        
        # 技能大师 (自定义技能 >= 5)
        if custom_skills >= 5:
            achievements.append(self.ACHIEVEMENTS['skill_master'])
        elif custom_skills >= 3:
            achievements.append(self.ACHIEVEMENTS['custom_creator'])
        
        # 自定义大师 (自定义技能 >= 7)
        if custom_skills >= 7:
            achievements.append(self.ACHIEVEMENTS['custom_master'])
        
        # 技能收藏家 (技能 >= 10)
        if skill_count >= 15:
            achievements.append(self.ACHIEVEMENTS['skill_connoisseur'])
        elif skill_count >= 10:
            achievements.append(self.ACHIEVEMENTS['skill_collector'])
        
        # 技能传奇 (技能 >= 20)
        if skill_count >= 20:
            achievements.append(self.ACHIEVEMENTS['skill_legend'])
        
        # === 自动化相关成就 ===
        has_heartbeat = metrics.get('has_heartbeat', False)
        daily_tokens = metrics.get('daily_tokens', 0)
        
        # 自动化达人 (心跳开启)
        if has_heartbeat:
            achievements.append(self.ACHIEVEMENTS['automation_pro'])
            achievements.append(self.ACHIEVEMENTS['heartbeat_hero'])
        
        # 自动化之神 (每天 > 10万 Token)
        if daily_tokens >= 100000:
            achievements.append(self.ACHIEVEMENTS['automation_god'])
        elif daily_tokens >= 50000:
            achievements.append(self.ACHIEVEMENTS['power_user'])
        
        # === 集成相关成就 ===
        channels = metrics.get('channels', 0)
        
        # 多渠道运营 (>= 2)
        if channels >= 2:
            achievements.append(self.ACHIEVEMENTS['multi_channel'])
        
        # 集成专家 (>= 3)
        if channels >= 3:
            achievements.append(self.ACHIEVEMENTS['integration_expert'])
        
        # 渠道大师 (>= 5)
        if channels >= 5:
            achievements.append(self.ACHIEVEMENTS['channel_master'])
        
        # === Token 相关成就 ===
        total_tokens = data.get('total_tokens', 0)
        
        # Token 百万富翁
        if total_tokens >= 10000000:
            achievements.append(self.ACHIEVEMENTS['token_billionaire'])
        elif total_tokens >= 1000000:
            achievements.append(self.ACHIEVEMENTS['token_millionaire'])
        
        # === 会话相关成就 ===
        sessions = data.get('sessions', {})
        session_count = sessions.get('total', 0) if isinstance(sessions, dict) else 0
        
        if session_count >= 500:
            achievements.append(self.ACHIEVEMENTS['session_master'])
        elif session_count >= 100:
            achievements.append(self.ACHIEVEMENTS['session_warrior'])
        
        # === 稳定性成就 ===
        log_stats = data.get('log_stats', {})
        error_count = log_stats.get('error_count', 1) if isinstance(log_stats, dict) else 1
        
        # 零错误成就
        if error_count == 0:
            achievements.append(self.ACHIEVEMENTS['zero_error'])
        
        # === 活跃度成就 ===
        usage_days = data.get('usage_days', 0)
        
        if usage_days >= 180:
            achievements.append(self.ACHIEVEMENTS['veteran_user'])
        elif usage_days >= 90:
            achievements.append(self.ACHIEVEMENTS['monthly_master'])
        elif usage_days >= 30:
            achievements.append(self.ACHIEVEMENTS['weekly_warrior'])
        elif usage_days >= 7:
            achievements.append(self.ACHIEVEMENTS['daily_active'])
        
        # === 特殊成就 ===
        # 深度等级 >= 4 解锁隐藏成就
        if evaluation.get('total_score', 0) >= 80:
            achievements.append(self.ACHIEVEMENTS['secret_lobster'])
        
        # 去重
        achievements = list(dict.fromkeys(achievements))
        
        return achievements
    
    def calculate_rank_percentile(self, total_score: float) -> Dict:
        """
        计算排名百分比
        
        Args:
            total_score: 总评分
        
        Returns:
            排名信息
        """
        for percentile, info in sorted(self.RANK_PERCENTILES.items(), reverse=True):
            if total_score >= info['min_score']:
                return {
                    'percentile': percentile,
                    'title': info['title'],
                    'badge': info['badge'],
                    'description': f"你的龙虾值击败了全球 {percentile}% 的用户！"
                }
        
        # 默认返回最低等级
        return {
            'percentile': 10,
            'title': '🐣 萌新入门',
            'badge': 'starter',
            'description': "每只龙虾都是从虾米开始的，继续加油！"
        }
    
    def detect_rare_titles(self, data: Dict, evaluation: Dict) -> List[Dict]:
        """
        检测稀有称号
        
        Args:
            data: 原始数据
            evaluation: 评估结果
        
        Returns:
            稀有称号列表
        """
        titles = []
        metrics = evaluation.get('metrics', {})
        total_score = evaluation.get('total_score', 0)
        scores = [
            evaluation.get('skill_score', 0),
            evaluation.get('automation_score', 0),
            evaluation.get('integration_score', 0)
        ]
        
        for title_id, title_info in self.RARE_TITLES.items():
            condition = title_info['condition']
            if condition is None:
                continue
            
            try:
                # 根据条件的参数数量动态调用
                import inspect
                params = inspect.signature(condition).parameters
                
                if len(params) == 1:
                    result = condition(metrics)
                elif len(params) == 2:
                    result = condition(metrics, data)
                elif len(params) == 3:
                    result = condition(metrics, data, total_score)
                else:
                    result = condition(scores)
                
                if result:
                    titles.append({
                        'id': title_id,
                        'name': title_info['name'],
                        'desc': title_info['desc'],
                        'rarity': 'legendary' if title_id in ['skill_ancestor', 'automation_emperor', 'efficiency_monster'] else 'epic'
                    })
            except Exception:
                continue
        
        return titles
    
    def generate_share_content(self, data: Dict, evaluation: Dict) -> Dict:
        """
        生成分享内容（爆款属性增强版）
        
        Args:
            data: 原始数据
            evaluation: 评估结果
        
        Returns:
            分享内容
        """
        total_score = evaluation.get('total_score', 0)
        level = evaluation.get('usage_level', '浅度使用')
        lobster_skill = evaluation.get('lobster_skill', '小龙虾')
        
        # 计算排名
        rank_info = self.calculate_rank_percentile(total_score)
        
        # 检测稀有称号
        rare_titles = self.detect_rare_titles(data, evaluation)
        
        # 生成分享文案
        share_templates = []
        
        # 高分炫耀文案
        if total_score >= 70:
            share_templates = [
                f"🦞 我的龙虾值 {total_score:.0f} 分，{rank_info['title']}！{evaluation.get('lobster_message', '')[:30]}",
                f"🔥 OpenClaw 深度玩家认证！{rare_titles[0]['name'] if rare_titles else lobster_skill} 已解锁！",
                f"⚡ 效率翻倍神器！我用 OpenClaw 省下了 {evaluation.get('value_estimate', '无数')}！"
            ]
        # 中等分数鼓励文案
        elif total_score >= 40:
            share_templates = [
                f"🦞 龙虾值 Lv.{int(total_score/20)+1}！正在向「龙虾大师」进发～",
                f"📊 OpenClaw 使用深度：{level}，距离顶级玩家只差一步！",
                f"🎯 我的 AI 助手已经能帮我省时间了，你的呢？"
            ]
        # 低分幽默文案
        else:
            share_templates = [
                f"🦐 我是一只还在沉睡的小龙虾，等待觉醒...",
                f"🎮 OpenClaw 新手村报道！听说高手都在这里诞生～",
                f"🌱 我的龙虾值才 {total_score:.0f} 分，但每个大佬都是从萌新开始的！"
            ]
        
        # 生成海报数据
        poster_data = {
            'main_score': total_score,
            'level': lobster_skill,
            'rank_title': rank_info['title'],
            'rank_description': rank_info['description'],
            'rare_titles': rare_titles[:3],  # 最多显示3个
            'key_stats': {
                'skill_count': evaluation.get('metrics', {}).get('skill_count', 0),
                'custom_skills': evaluation.get('metrics', {}).get('custom_skills', 0),
                'value': evaluation.get('value_estimate', '0元')
            },
            'share_texts': share_templates,
            'qr_text': '扫码测测你的龙虾值'
        }
        
        return {
            'poster_data': poster_data,
            'rank_info': rank_info,
            'rare_titles': rare_titles,
            'share_texts': share_templates
        }
    
    def generate_full_evaluation(self, data: Dict) -> Dict:
        """
        生成完整评估报告
        
        Args:
            data: 采集的数据
        
        Returns:
            完整评估结果
        """
        # 使用深度评估
        usage_eval = self.evaluate_usage_depth(data)
        
        # 价值估算
        value_eval = self.estimate_value(usage_eval)
        
        # 龙虾等级
        lobster = self.get_lobster_skill(usage_eval['level'])
        
        # 成就检测
        achievements = self.detect_achievements(data, usage_eval)
        
        # 计算排名百分比
        rank_info = self.calculate_rank_percentile(usage_eval['total_score'])
        
        # 检测稀有称号
        rare_titles = self.detect_rare_titles(data, usage_eval)
        
        # 生成分享内容
        share_content = self.generate_share_content(data, {
            'total_score': usage_eval['total_score'],
            'usage_level': usage_eval['level_name'],
            'lobster_skill': lobster['title'],
            'lobster_message': lobster['message'],
            'value_estimate': value_eval['value_estimate'],
            'metrics': usage_eval['metrics'],
            'skill_score': usage_eval['skill_score'],
            'automation_score': usage_eval['automation_score'],
            'integration_score': usage_eval['integration_score']
        })
        
        return {
            'evaluated_at': datetime.now().isoformat(),
            'usage_level': usage_eval['level_name'],
            'value_estimate': value_eval['value_estimate'],
            'value_range': value_eval['value_range'],
            'value_level': value_eval['value_level'],
            'lobster_skill': lobster['title'],
            'lobster_rank': lobster['rank'],
            'lobster_message': lobster['message'],
            'skill_score': usage_eval['skill_score'],
            'automation_score': usage_eval['automation_score'],
            'integration_score': usage_eval['integration_score'],
            'total_score': usage_eval['total_score'],
            'metrics': usage_eval['metrics'],
            'achievements': achievements,
            # 新增：排名百分比
            'rank_percentile': rank_info['percentile'],
            'rank_title': rank_info['title'],
            'rank_description': rank_info['description'],
            # 新增：稀有称号
            'rare_titles': rare_titles,
            # 新增：分享内容
            'share_content': share_content,
            'raw_data': data
        }


if __name__ == '__main__':
    # 测试评估引擎
    engine = EvaluationEngine()
    
    # 模拟数据
    test_data = {
        'total_skills': 12,
        'total_tokens': 150000,
        'usage_days': 30,
        'skills': [
            {'name': 'skill1', 'is_custom': True},
            {'name': 'skill2', 'is_custom': True},
        ],
        'config': {
            'agent_count': 2,
            'heartbeat_interval': 1800,
            'channels': ['qqbot', 'telegram']
        }
    }
    
    result = engine.generate_full_evaluation(test_data)
    
    print("📊 评估结果:")
    print(f"  使用深度: {result['usage_level']}")
    print(f"  价值估算: {result['value_estimate']}")
    print(f"  龙虾等级: {result['lobster_skill']}")
    print(f"  总分: {result['total_score']:.1f}")
    print(f"\n💬 {result['lobster_message']}")