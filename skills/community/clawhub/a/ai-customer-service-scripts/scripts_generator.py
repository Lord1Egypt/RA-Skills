#!/usr/bin/env python3
"""
AI 客服话术生成器
用途：根据行业/场景/客户消息，生成专业客服回复
"""

import os
import json
from openclaw import OpenClaw

class ScriptGenerator:
    """话术生成器"""
    
    INDUSTRIES = {
        "电商": ["物流", "退换货", "商品咨询", "促销活动", "支付问题"],
        "金融": ["账户查询", "转账汇款", "理财咨询", "信用卡", "贷款"],
        "教育": ["课程咨询", "报名缴费", "学习进度", "证书发放", "退费"],
        "医疗": ["预约挂号", "检查报告", "用药咨询", "住院流程", "医保"],
        "餐饮": ["预订", "菜品咨询", "外卖", "会员卡", "投诉建议"],
        "旅游": ["预订", "行程变更", "退款", "签证", "保险"],
        "物流": ["查件", "投诉", "寄件", "理赔", "时效"],
        "游戏": ["充值", "账号问题", "活动咨询", "bug反馈", "封号申诉"],
        "软件": ["安装", "使用教程", "功能咨询", "续费", "退款"],
        "房产": ["房源咨询", "看房预约", "合同", "交房", "物业"]
    }
    
    def __init__(self, model="deepseek-chat"):
        self.model = model
        self.api_key = os.getenv("OPENCLAW_API_KEY")
        if not self.api_key:
            raise ValueError("请设置环境变量 OPENCLAW_API_KEY")
    
    def analyze_sentiment(self, message):
        """分析客户情绪"""
        negative_keywords = ["不满", "投诉", "垃圾", "骗子", "退款", "差评", "慢", "坑"]
        positive_keywords = ["感谢", "满意", "好评", "推荐", "赞"]
        
        message_lower = message.lower()
        neg_count = sum(1 for k in negative_keywords if k in message_lower)
        pos_count = sum(1 for k in positive_keywords if k in message_lower)
        
        if neg_count > pos_count:
            return "negative"
        elif pos_count > 0:
            return "positive"
        return "neutral"
    
    def generate(self, industry, scenario, customer_message, tone="professional"):
        """生成客服回复话术"""
        sentiment = self.analyze_sentiment(customer_message)
        
        prompt = f"""你是专业的{industry}行业客服培训专家。
场景：{scenario}
客户消息：{customer_message}
客户情绪：{sentiment}
语气要求：{tone}

请生成一段专业的客服回复话术（100-200字），要求：
1. 先共情客户（特别是负面情绪）
2. 清晰说明解决方案
3. 给出具体行动步骤
4. 结尾表示感谢

直接输出话术内容，不要解释。"""

        client = OpenClaw(api_key=self.api_key)
        response = client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=500
        )
        
        return response.choices[0].message.content
    
    def score_script(self, script):
        """评估话术质量（0-100分）"""
        score = 50
        
        # 长度适中
        if 100 <= len(script) <= 300:
            score += 15
        
        # 包含共情词汇
        empathy_words = ["抱歉", "理解", "不便", "感谢"]
        score += sum(5 for w in empathy_words if w in script)
        
        # 包含行动词
        action_words = ["帮您", "已经", "正在", "可以"]
        score += sum(3 for w in action_words if w in script)
        
        return min(score, 100)

def main():
    import argparse
    parser = argparse.ArgumentParser(description="AI 客服话术生成器")
    parser.add_argument("--industry", required=True, help="行业")
    parser.add_argument("--scenario", required=True, help="场景")
    parser.add_argument("--message", required=True, help="客户消息")
    parser.add_argument("--tone", default="professional", help="语气")
    args = parser.parse_args()
    
    gen = ScriptGenerator()
    
    print(f"\n📋 行业：{args.industry}")
    print(f"📌 场景：{args.scenario}")
    print(f"💬 客户消息：{args.message}")
    print("-" * 50)
    
    reply = gen.generate(args.industry, args.scenario, args.message, args.tone)
    score = gen.score_script(reply)
    
    print(f"🤖 客服回复：\n{reply}")
    print("-" * 50)
    print(f"📊 话术评分：{score}/100")

if __name__ == "__main__":
    main()
