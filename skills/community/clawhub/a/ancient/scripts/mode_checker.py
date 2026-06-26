#!/usr/bin/env python3
"""
古代人模式检测器
用于检测用户输入是否包含古代人模式触发词
"""

import re
from typing import Dict, List, Optional, Tuple

class AncientmanModeDetector:
    """古代人模式检测类"""
    
    def __init__(self):
        # 中文触发词
        self.chinese_triggers = [
            "古代人模式", "古代人", "原始人模式", "原始人", "少用点token", "简洁点", "压缩模式",
            "精简模式", "省点token", "少说废话", "直接点", "简单点"
        ]
        
        # 英文触发词
        self.english_triggers = [
            "ancientman mode", "ancientman", "caveman mode", "caveman", "less tokens", "be brief", 
            "be concise", "use ancientman", "talk like ancientman"
        ]
        
        # 强度级别关键词
        self.intensity_keywords = {
            "lite": ["轻度", "lite", "简单", "简单模式"],
            "full": ["标准", "full", "默认", "正常"],
            "ultra": ["极致", "ultra", "极限", "超级"],
            "classical": ["古风", "classical", "文言", "古典", "文雅", "雅致"]
        }
        
        # 大模型风格关键词
        self.platform_keywords = {
            "doubao": ["豆包", "字节", "bytedance"],
            "deepseek": ["deepseek", "深度求索", "深度"],
            "qianwen": ["千问", "通义", "alibaba"],
            "minimax": ["minimax", "abab", "moonshot"]
        }
    
    def detect_mode(self, user_input: str) -> Dict:
        """
        检测用户输入中的古代人模式相关信息
        
        Args:
            user_input: 用户输入文本
            
        Returns:
            Dict: 包含检测结果的字典
        """
        result = {
            "mode_triggered": False,
            "intensity": "full",  # 默认强度
            "platform_hint": None,
            "triggers_found": [],
            "clear_command": False
        }
        
        # 转换为小写便于匹配
        input_lower = user_input.lower()
        
        # 检测退出命令
        if any(cmd in input_lower for cmd in ["stop ancientman", "stop caveman", "normal mode", "古代人关", "原始人关", "正常模式"]):
            result["clear_command"] = True
            return result
        
        # 检测触发词
        all_triggers = self.chinese_triggers + self.english_triggers
        found_triggers = []
        
        for trigger in all_triggers:
            if trigger.lower() in input_lower:
                found_triggers.append(trigger)
                result["mode_triggered"] = True
        
        if found_triggers:
            result["triggers_found"] = found_triggers
            
            # 检测强度级别
            for intensity, keywords in self.intensity_keywords.items():
                for keyword in keywords:
                    if keyword.lower() in input_lower:
                        result["intensity"] = intensity
                        break
                if result["intensity"] != "full":  # 如果找到了非默认强度
                    break
            
            # 检测大模型平台提示
            for platform, keywords in self.platform_keywords.items():
                for keyword in keywords:
                    if keyword.lower() in input_lower:
                        result["platform_hint"] = platform
                        break
                if result["platform_hint"]:
                    break
        
        return result
    
    def get_intensity_description(self, intensity: str) -> str:
        """获取强度级别描述"""
        descriptions = {
            "lite": "轻度模式：去除填充词，保留完整句子，专业但紧凑",
            "full": "标准模式：片段化句子，省略助词，直接表达核心信息",
            "ultra": "极致模式：使用缩写，删除连词，箭头表示因果关系",
            "classical": "古风小生模式：使用文言文表达，融入古典元素，风格典雅"
        }
        return descriptions.get(intensity, descriptions["full"])
    
    def get_platform_style_guide(self, platform: Optional[str]) -> str:
        """获取平台风格指南"""
        if not platform:
            return "通用风格：平衡技术和易懂性"
        
        guides = {
            "doubao": "豆包风格：口语化、接地气，多用生活化比喻",
            "deepseek": "DeepSeek风格：技术解释强，喜欢结构化表达",
            "qianwen": "千问风格：综合性强，适合多种风格",
            "minimax": "Minimax风格：中英混合友好，技术术语用英文"
        }
        return guides.get(platform, "通用风格")
    
    def compress_text(self, text: str, intensity: str = "full", platform: Optional[str] = None) -> str:
        """
        根据指定强度和平台压缩文本
        
        Args:
            text: 原始文本
            intensity: 压缩强度 (lite, full, ultra, classical)
            platform: 目标平台风格
            
        Returns:
            str: 压缩后的文本
        """
        # 这里只是一个示例实现，实际应用中需要更复杂的自然语言处理
        if intensity == "lite":
            # 轻度压缩：去除客套话
            patterns_to_remove = [
                r"^好的，", r"^明白了，", r"^没问题，",
                r"其实", r"实际上", r"基本上"
            ]
            compressed = text
            for pattern in patterns_to_remove:
                compressed = re.sub(pattern, "", compressed)
            return compressed.strip()
        
        elif intensity == "full":
            # 标准压缩：进一步简化
            # 这里可以添加更多规则
            return text
        
        elif intensity == "ultra":
            # 极致压缩：使用符号和缩写
            # 这里可以添加更多规则
            return text
        
        elif intensity == "classical":
            # 古风小生模式：使用文言文表达
            # 这里可以添加更多规则
            return text
        
        return text


def main():
    """测试函数"""
    detector = CavemanModeDetector()
    
    test_inputs = [
        "使用原始人模式，极致压缩",
        "豆包，开启原始人模式",
        "caveman mode lite",
        "正常模式",
        "帮我看看这个React组件为什么重渲染",
        "少用点token，直接说重点",
        "开启古风小生模式",
        "caveman classical",
        "使用文言文回答"
    ]
    
    print("原始人模式检测器测试：")
    print("=" * 50)
    
    for test_input in test_inputs:
        print(f"\n输入: {test_input}")
        result = detector.detect_mode(test_input)
        
        if result["mode_triggered"]:
            print(f"  检测到原始人模式")
            print(f"  强度: {result['intensity']} - {detector.get_intensity_description(result['intensity'])}")
            if result["platform_hint"]:
                print(f"  平台提示: {result['platform_hint']} - {detector.get_platform_style_guide(result['platform_hint'])}")
            if result["triggers_found"]:
                print(f"  触发词: {', '.join(result['triggers_found'])}")
        elif result["clear_command"]:
            print(f"  检测到退出命令")
        else:
            print(f"  未检测到原始人模式")


if __name__ == "__main__":
    main()