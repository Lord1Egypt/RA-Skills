#!/usr/bin/env python3
"""
AI邮件分类器
基于关键词规则 + OpenAI兼容API智能分类
"""

import re
from typing import Dict, Optional


# 分类关键词配置
CATEGORY_KEYWORDS = {
    'urgent': {
        'label': '🔴 紧急',
        'priority': 1,
        'keywords': [
            # 退款相关
            '退款', '退款申请', '申请退款', '取消订单', '订单取消',
            '退钱', '退款处理', '退款中', '退款成功', '退款失败',
            'refund', 'cancel order', 'canceled order',
            # 投诉相关
            '投诉', '投诉您', '投诉她', '投诉他', '举报', '差评',
            '非常不满', '强烈不满', '无法接受', '忍无可忍',
            'complaint', 'complain', 'bad review', 'negative feedback',
            # 紧急
            '紧急', '紧急情况', '十万火急', '立刻', '马上', '现在就',
            'urgent', 'emergency', 'immediately', 'asap',
            # 差评预警
            '差评预警', '即将差评', '准备差评', '差评', '给差评',
        ]
    },
    'important': {
        'label': '🟠 重要',
        'priority': 2,
        'keywords': [
            # 售后
            '售后', '售后服务', '维修', '维修中', '申请维修',
            '换货', '申请换货', '换一个新的', '更换',
            'after-sales', 'repair', 'maintenance', 'exchange',
            # 付款
            '付款', '支付', '账单', '发票', '付款问题', '支付问题',
            '未付款', '未支付', '付款失败', '支付失败', '收款',
            'payment', 'invoice', 'bill', 'paid', 'unpaid',
            # 账户
            '账户', '账号', '登录不了', '登录不上', '无法登录',
            '密码错误', '密码忘了', '账户异常', '账号异常',
            'account', 'login', 'password', 'locked',
        ]
    },
    'normal': {
        'label': '🟡 普通',
        'priority': 3,
        'keywords': [
            # 售前咨询
            '咨询', '请问', '问一下', '想问一下', '了解一下',
            '多少钱', '价格', '报价', '优惠', '折扣', '促销',
            '规格', '参数', '尺寸', '大小', '颜色', '款式',
            '怎么买', '在哪里买', '哪里有', '哪有',
            'inquiry', 'price', 'cost', 'how much', 'spec',
            # 物流
            '物流', '快递', '发货', '什么时候发货', '多久到',
            '到货', '签收', '查询物流', '物流查询', '运单号',
            'shipping', 'delivery', 'express', 'tracking',
            # 使用
            '怎么用', '使用', '使用方法', '教程', '说明',
            'how to use', 'manual', 'guide',
        ]
    },
    'deferrable': {
        'label': '🟢 可延后',
        'priority': 4,
        'keywords': [
            # 问候
            '你好', '您好', '嗨', 'hi', 'hello', '早上好', '下午好',
            'good morning', 'good afternoon', 'good evening',
            # 感谢
            '谢谢', '感谢', '多谢', '非常感谢', '十分感谢',
            'thanks', 'thank you', 'appreciate',
            # 已处理
            '已处理', '已解决', '知道了', '好的', '收到',
            '没问题', '没有问题了', '已经好了',
            'done', 'solved', 'resolved', 'okay', 'ok',
            # 告别
            '再见', '拜拜', '下次见', '回头见',
            'goodbye', 'see you', 'bye',
        ]
    }
}


class EmailClassifier:
    """AI邮件分类器"""

    def __init__(self, config: dict):
        self.config = config
        self.api_endpoint = config.get('api_endpoint', '')
        self.api_key = config.get('api_key', '')
        self.model = config.get('model', 'gpt-3.5-turbo')
        self.use_ai = config.get('use_ai', False)
        self._keyword_cache = self._build_keyword_cache()

    def _build_keyword_cache(self) -> Dict:
        """构建关键词缓存用于快速匹配"""
        cache = {}
        for category, data in CATEGORY_KEYWORDS.items():
            for keyword in data['keywords']:
                cache[keyword.lower()] = {
                    'category': category,
                    'label': data['label'],
                    'priority': data['priority']
                }
        return cache

    def classify(self, email: dict) -> str:
        """
        分类邮件

        Args:
            email: 邮件字典，包含subject, body, from等

        Returns:
            分类标签，如 '🔴 紧急'
        """
        subject = email.get('subject', '').lower()
        body = email.get('body', '').lower()
        snippet = email.get('snippet', '').lower()

        # 合并文本用于匹配
        text = f"{subject} {snippet} {body[:500]}"

        # 关键词快速匹配
        match_scores = {}

        for keyword, info in self._keyword_cache.items():
            if keyword in text:
                category = info['category']
                priority = info['priority']
                if category not in match_scores or priority < match_scores[category]:
                    match_scores[category] = priority

        # 找到最高优先级匹配
        if match_scores:
            best_category = min(match_scores.items(), key=lambda x: x[1])[0]
            return CATEGORY_KEYWORDS[best_category]['label']

        # 如果没有关键词匹配，使用AI分类
        if self.use_ai and self.api_endpoint:
            return self._ai_classify(email)

        # 默认普通
        return '🟡 普通'

    def _ai_classify(self, email: dict) -> str:
        """调用AI进行分类"""
        try:
            import openai

            client = openai.OpenAI(
                api_key=self.api_key,
                base_url=self.api_endpoint
            )

            subject = email.get('subject', '')
            body = email.get('snippet', '') or email.get('body', '')[:500]

            prompt = f"""请分析以下邮件，判断紧急程度：

邮件主题: {subject}
邮件内容: {body}

分类选项（只返回标签）：
- 🔴 紧急：退款申请、投诉、差评预警、账号安全等需要立即处理
- 🟠 重要：售后问题、付款问题、账户异常等需要当天处理
- 🟡 普通：售前咨询、物流查询等一般咨询
- 🟢 可延后：问候、已处理等可以稍后处理

只返回分类标签，不要其他内容。"""

            response = client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=20,
                temperature=0
            )

            result = response.choices[0].message.content.strip()

            # 验证返回结果
            for category, data in CATEGORY_KEYWORDS.items():
                if data['label'] in result or category in result.lower():
                    return data['label']

            return '🟡 普通'

        except Exception as e:
            print(f"AI分类失败: {e}")
            return '🟡 普通'

    def classify_with_confidence(self, email: dict) -> Dict:
        """带置信度的分类"""
        subject = email.get('subject', '').lower()
        body = email.get('body', '').lower()
        snippet = email.get('snippet', '').lower()
        text = f"{subject} {snippet} {body[:500]}"

        match_scores = {}
        match_counts = {}

        for keyword, info in self._keyword_cache.items():
            if keyword in text:
                category = info['category']
                if category not in match_scores:
                    match_scores[category] = info['priority']
                    match_counts[category] = 0
                match_counts[category] += 1

        if match_counts:
            best_category = max(match_counts.items(), key=lambda x: x[1])[0]
            count = match_counts[best_category]
            total = sum(match_counts.values())
            confidence = count / total if total > 0 else 0.5

            return {
                'category': CATEGORY_KEYWORDS[best_category]['label'],
                'confidence': min(confidence, 1.0),
                'matches': count,
                'all_matches': match_counts
            }

        return {
            'category': '🟡 普通',
            'confidence': 0.5,
            'matches': 0,
            'all_matches': {}
        }

    def get_priority(self, category: str) -> int:
        """获取分类优先级（数字越小越紧急）"""
        for cat, data in CATEGORY_KEYWORDS.items():
            if data['label'] == category:
                return data['priority']
        return 3  # 默认普通

    def sort_by_priority(self, emails: list) -> list:
        """按优先级排序邮件"""
        return sorted(
            emails,
            key=lambda e: self.get_priority(e.get('category', '🟡 普通'))
        )
