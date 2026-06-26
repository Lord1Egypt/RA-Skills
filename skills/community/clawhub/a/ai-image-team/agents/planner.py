# 🧠 策划师 (Planner) - 需求分析与创意构思

"""
策划师职责：
1. 需求深度分析（产品类型、使用场景、目标人群、风格偏好）
2. 创意构思与风格定位
3. Prompt 优化（精准中文 Prompt + 负面提示词）
4. 推荐工具选择（即梦/LiblibAI）
5. 建议生成数量

输出：创意简报
"""

from typing import Dict, List, Optional
import json


class PlannerAgent:
    """策划师 Agent"""
    
    def __init__(self):
        self.name = "🧠 策划师"
        self.ecommerce_rules = self._load_ecommerce_rules()
    
    def _load_ecommerce_rules(self) -> Dict:
        """加载电商规则库"""
        try:
            with open('config/ecommerce_rules.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return self._default_rules()
    
    def _default_rules(self) -> Dict:
        """默认电商规则"""
        return {
            "product_types": {
                "服装": {"要点": ["展示细节", "突出面料质感", "模特展示上身效果"], "推荐工具": "liblib"},
                "食品": {"要点": ["突出食欲感", "暖色调", "近景特写"], "推荐工具": "jimeng"},
                "数码": {"要点": ["科技感", "简洁背景", "展示功能"], "推荐工具": "jimeng"},
                "美妆": {"要点": ["精致感", "柔和光线", "突出质地"], "推荐工具": "liblib"},
                "家居": {"要点": ["温馨氛围", "场景化", "生活气息"], "推荐工具": "jimeng"}
            },
            "platforms": {
                "淘宝主图": {"尺寸": "800x800", "要点": ["产品占比 70%+", "白底或纯色", "无文字"]},
                "京东主图": {"尺寸": "800x800", "要点": ["白底", "产品清晰", "无水印"]},
                "抖音封面": {"尺寸": "1080x1920", "要点": ["竖版", "吸引眼球", "可加文字"]},
                "微信公众号": {"尺寸": "900x383", "要点": ["横版", "图文结合", "品牌一致"]}
            },
            "quality_checklist": [
                "产品主体清晰突出",
                "无明显 AI 瑕疵（畸形/错位）",
                "色彩符合品牌调性",
                "尺寸符合平台要求",
                "文字可读性（如有文案）",
                "风格与需求一致"
            ]
        }
    
    def analyze(self, user_input: str) -> Dict:
        """
        分析用户需求，生成创意简报
        
        Args:
            user_input: 用户输入的中文需求描述
            
        Returns:
            创意简报字典
        """
        # 提取关键信息
        info = self._extract_info(user_input)
        
        # 补充缺失信息（如需要）
        if self._needs_clarification(info):
            return self._ask_clarification(info)
        
        # 生成创意简报
        brief = self._create_brief(info)
        
        return brief
    
    def _extract_info(self, user_input: str) -> Dict:
        """从用户输入中提取关键信息"""
        info = {
            "product_type": None,      # 产品类型
            "product_name": None,       # 具体产品名称
            "scenario": None,           # 使用场景
            "target_audience": None,    # 目标人群
            "style": None,              # 风格偏好
            "platform": None,           # 发布平台
            "tool_preference": None,    # 工具偏好
            "quantity": 2,              # 建议生成数量
            "reference": None,          # 参考图
            "raw_input": user_input
        }
        
        # 简单关键词匹配（实际可用 LLM 优化）
        input_lower = user_input.lower()
        
        # 产品类型识别
        product_keywords = {
            "服装": ["衣服", "服装", "连衣裙", "T 恤", "衬衫", "外套", "裤子", "裙子"],
            "食品": ["食品", "食物", "巧克力", "蛋糕", "饮料", "零食", "餐饮"],
            "数码": ["数码", "电子", "耳机", "手机", "电脑", "相机", "智能"],
            "美妆": ["美妆", "化妆品", "口红", "护肤品", "面膜", "香水"],
            "家居": ["家居", "家具", "装饰", "灯具", "家纺"]
        }
        
        for ptype, keywords in product_keywords.items():
            if any(kw in user_input for kw in keywords):
                info["product_type"] = ptype
                break
        
        # 场景识别
        scenario_keywords = {
            "主图": ["主图", "首图", "封面图"],
            "详情页": ["详情页", "内页", "描述图"],
            "海报": ["海报", "宣传图", "推广图"],
            "社交媒体": ["朋友圈", "微博", "小红书", "抖音"]
        }
        
        for scenario, keywords in scenario_keywords.items():
            if any(kw in user_input for kw in keywords):
                info["scenario"] = scenario
                break
        
        # 平台识别
        platform_keywords = {
            "淘宝": ["淘宝", "天猫"],
            "京东": ["京东"],
            "抖音": ["抖音", "TikTok"],
            "微信": ["微信", "公众号", "朋友圈"]
        }
        
        for platform, keywords in platform_keywords.items():
            if any(kw in user_input for kw in keywords):
                info["platform"] = platform
                break
        
        # 工具偏好
        if "即梦" in user_input or "jimeng" in input_lower:
            info["tool_preference"] = "jimeng"
        elif "liblib" in input_lower:
            info["tool_preference"] = "liblib"
        
        # 数量识别
        import re
        quantity_match = re.search(r'(\d+)\s*[张幅个份]', user_input)
        if quantity_match:
            info["quantity"] = min(int(quantity_match.group(1)), 4)
        
        return info
    
    def _needs_clarification(self, info: Dict) -> bool:
        """判断是否需要进一步询问"""
        # 如果产品类型和场景都不明确，需要询问
        if not info["product_type"] and not info["scenario"]:
            return True
        return False
    
    def _ask_clarification(self, info: Dict) -> Dict:
        """生成澄清问题"""
        return {
            "type": "clarification",
            "questions": [
                "请问这是什么类型的产品？（如服装/食品/数码/美妆/家居）",
                "这张图用于什么场景？（如淘宝主图/详情页/海报/社交媒体）",
                "有特定的风格偏好吗？（如简约/奢华/国潮/ins 风）",
                "目标人群是谁？（如年龄/性别/消费力）"
            ],
            "raw_input": info["raw_input"]
        }
    
    def _create_brief(self, info: Dict) -> Dict:
        """生成创意简报"""
        # 获取产品类型规则
        product_rules = self.ecommerce_rules.get("product_types", {}).get(
            info["product_type"], 
            {"要点": [], "推荐工具": info["tool_preference"] or "jimeng"}
        )
        
        # 获取平台规则
        platform_rules = {}
        if info["platform"] and info["scenario"]:
            platform_key = f"{info['platform']}{info['scenario']}"
            platform_rules = self.ecommerce_rules.get("platforms", {}).get(platform_key, {})
        
        # 推荐工具
        recommended_tool = info["tool_preference"] or product_rules.get("推荐工具", "jimeng")
        
        # 生成 Prompt
        prompt = self._generate_prompt(info, product_rules)
        
        # 生成负面提示词
        negative_prompt = self._generate_negative_prompt(info)
        
        return {
            "type": "brief",
            "product_info": {
                "type": info["product_type"],
                "name": info["product_name"],
                "scenario": info["scenario"],
                "platform": info["platform"],
                "target_audience": info["target_audience"],
                "style": info["style"]
            },
            "creative_brief": {
                "prompt": prompt,
                "negative_prompt": negative_prompt,
                "key_points": product_rules.get("要点", []),
                "platform_requirements": platform_rules,
                "recommended_tool": recommended_tool,
                "quantity": info["quantity"]
            },
            "tool_suggestion": self._explain_tool_choice(recommended_tool, info)
        }
    
    def _generate_prompt(self, info: Dict, product_rules: Dict) -> str:
        """生成精准中文 Prompt"""
        parts = []
        
        # 产品描述
        if info["product_name"]:
            parts.append(f"{info['product_name']}")
        elif info["product_type"]:
            parts.append(f"{info['product_type']}产品")
        
        # 风格描述
        if info["style"]:
            parts.append(f"风格：{info['style']}")
        
        # 场景描述
        if info["scenario"]:
            scenario_desc = {
                "主图": "产品主体突出，背景干净简洁",
                "详情页": "展示产品细节和使用场景",
                "海报": "视觉冲击力强，适合宣传推广",
                "社交媒体": "适合社交媒体传播，吸引眼球"
            }
            parts.append(scenario_desc.get(info["scenario"], ""))
        
        # 产品类型要点
        parts.extend(product_rules.get("要点", []))
        
        # 目标人群
        if info["target_audience"]:
            parts.append(f"目标人群：{info['target_audience']}")
        
        return "，".join(parts)
    
    def _generate_negative_prompt(self, info: Dict) -> str:
        """生成负面提示词"""
        negatives = [
            "模糊", "变形", "畸形", "低质量", "水印", "文字错误",
            "颜色失真", "比例失调", "背景杂乱"
        ]
        
        # 根据产品类型添加特定负面词
        if info["product_type"] == "服装":
            negatives.extend(["衣服褶皱不自然", "模特姿势怪异"])
        elif info["product_type"] == "食品":
            negatives.extend(["食物看起来不新鲜", "颜色过于鲜艳"])
        elif info["product_type"] == "数码":
            negatives.extend(["产品细节模糊", "科技感不足"])
        
        return "，".join(negatives)
    
    def _explain_tool_choice(self, tool: str, info: Dict) -> str:
        """解释工具选择理由"""
        explanations = {
            "jimeng": "即梦擅长海报和创意图，适合营销宣传类图片",
            "liblib": "LiblibAI 擅长产品精修和细节控制，适合需要精细调整的产品图"
        }
        return explanations.get(tool, "")


# 使用示例
if __name__ == "__main__":
    planner = PlannerAgent()
    
    # 测试用例
    test_input = "我需要一张淘宝主图，产品是女士连衣裙，白色雪纺材质，风格简约优雅"
    result = planner.analyze(test_input)
    
    print(json.dumps(result, ensure_ascii=False, indent=2))
