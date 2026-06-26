"""
抖音发布技能 - 内容生成模块
根据主题自动生成Markdown格式的文章内容
"""

import os
import sys
import json
import random
from datetime import datetime
from typing import Dict, List, Tuple

# 添加工作目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import (
    WORKSPACE_DIR, ARTICLES_DIR, CONTENT_GENERATION, 
    THEME_CATEGORIES, IMAGE_GENERATION
)

class ContentGenerator:
    """内容生成器"""
    
    def __init__(self):
        self.setup_directories()
        
    def setup_directories(self):
        """创建必要的目录结构"""
        os.makedirs(ARTICLES_DIR, exist_ok=True)
        os.makedirs(f"{WORKSPACE_DIR}/images", exist_ok=True)
        
    def generate_title_for_theme(self, theme: str, style: str = None) -> str:
        """
        根据主题生成吸引人的标题
        
        Args:
            theme: 主题
            style: 标题风格（可选）
            
        Returns:
            生成的标题
        """
        # 预设的标题模板
        title_templates = {
            "科技": [
                f"【{theme}】深度解析：{theme}的未来发展趋势",
                f"{theme}新发现：为什么{theme}正在改变世界？",
                f"从零开始了解{theme}：新手必读指南",
                f"{theme}的10个你不知道的秘密",
                f"关于{theme}的真相，99%的人都不知道"
            ],
            "生活": [
                f"生活中的{theme}：让平凡变得精彩",
                f"{theme}带来的生活改变：我的真实体验",
                f"因为{theme}，我的生活变得更好",
                f"{theme}让我学会了{theme}",
                f"从{theme}中找到生活的意义"
            ],
            "学习": [
                f"学习{theme}的正确姿势：新手进阶指南",
                f"{theme}学习心得：如何在{theme}中快速成长",
                f"为什么{theme}是每个人都应该掌握的技能",
                f"{theme}学习的3个关键点",
                f"从{theme}到{theme}：我的成长之路"
            ],
            "旅游": [
                f"秘境{theme}：那些被遗忘的绝美风景",
                f"{theme}旅行攻略：避开人群的冷门美景",
                f"因为{theme}爱上旅行：我的旅行故事",
                f"{theme}的10个必去理由",
                f"从{theme}出发：寻找旅行的意义"
            ]
        }
        
        # 确定分类
        category = "生活"  # 默认分类
        for cat, keywords in THEME_CATEGORIES.items():
            if any(keyword in theme for keyword in keywords):
                category = cat
                break
                
        # 选择模板
        templates = title_templates.get(category, title_templates["生活"])
        if not style or style not in ["科技感", "幽默风趣", "感人", "简洁明了"]:
            style = random.choice(["科技感", "幽默风趣", "感人", "简洁明了"])
            
        # 生成标题
        title = random.choice(templates).replace("{theme}", theme)
        
        return title
        
    def generate_article_content(self, theme: str) -> Tuple[str, str, List[str]]:
        """
        生成完整的文章内容
        
        Args:
            theme: 主题
            
        Returns:
            (标题, 内容, 标签列表)
        """
        title = self.generate_title_for_theme(theme)
        
        # 根据主题生成内容大纲
        outline = self.generate_outline(theme)
        
        # 生成详细内容
        content = self.generate_detailed_content(theme, outline)
        
        # 生成标签
        tags = self.generate_tags(theme, outline)
        
        return title, content, tags
        
    def generate_outline(self, theme: str) -> Dict[str, str]:
        """
        生成文章大纲
        
        Args:
            theme: 主题
            
        Returns:
            大纲字典
        """
        outline = {
            "introduction": f"大家好！今天我想和大家聊聊{theme}。这是一个既熟悉又陌生的话题，让我们一起深入了解。",
            "body_section_1": f"{theme}的核心概念：简单来说，{theme}就是...",
            "body_section_2": f"为什么{theme}越来越重要：在当今时代，{theme}发挥着...",
            "body_section_3": f"{theme}的实际应用：在日常生活中，{theme}可以应用在...",
            "conclusion": f"总结一下，{theme}不仅改变了我们的生活方式，也为我们带来了新的机遇。希望今天的分享对大家有所帮助，记得点赞关注哦！"
        }
        
        return outline
        
    def generate_detailed_content(self, theme: str, outline: Dict[str, str]) -> str:
        """
        生成详细的文章内容
        
        Args:
            theme: 主题
            outline: 大纲
            
        Returns:
            完整的文章内容
        """
        content_parts = []
        
        # 引入部分
        content_parts.append(outline["introduction"])
        content_parts.append("\n\n")
        
        # 主要内容部分
        content_parts.append("## " + theme.capitalize())
        content_parts.append("\n\n")
        content_parts.append(outline["body_section_1"])
        content_parts.append("\n\n")
        
        content_parts.append("## " + theme.capitalize())
        content_parts.append("\n\n")
        content_parts.append(outline["body_section_2"])
        content_parts.append("\n\n")
        
        content_parts.append("## " + theme.capitalize())
        content_parts.append("\n\n")
        content_parts.append(outline["body_section_3"])
        content_parts.append("\n\n")
        
        # 结尾部分
        content_parts.append("## " + theme.capitalize())
        content_parts.append("\n\n")
        content_parts.append(outline["conclusion"])
        
        return "".join(content_parts)
        
    def generate_tags(self, theme: str, outline: Dict[str, str]) -> List[str]:
        """
        生成相关标签
        
        Args:
            theme: 主题
            outline: 大纲
            
        Returns:
            标签列表
        """
        # 基础标签
        base_tags = [
            f"#{theme.replace(' ', '')}",
            "#内容创作",
            "#分享",
            "#生活",
            "#成长"
        ]
        
        # 根据主题添加特定标签
        theme_specific_tags = self.get_theme_specific_tags(theme)
        
        # 随机选择标签
        all_tags = base_tags + theme_specific_tags
        selected_tags = random.sample(all_tags, min(4, len(all_tags)))
        
        return selected_tags
        
    def get_theme_specific_tags(self, theme: str) -> List[str]:
        """
        根据主题获取特定标签
        
        Args:
            theme: 主题
            
        Returns:
            特定标签列表
        """
        theme_tags = {
            "人工智能": ["#AI", "#科技", "#未来"],
            "旅游": ["#旅行", "#风景", "#探索"],
            "美食": ["#美食", "#烹饪", "#推荐"],
            "学习": ["#学习", "#成长", "#技能"],
            "职场": ["#职场", "#工作", "#经验"]
        }
        
        return theme_tags.get(theme, ["#生活", "#分享"])
        
    def save_article_to_file(self, title: str, content: str, tags: List[str], theme: str) -> str:
        """
        保存文章到文件
        
        Args:
            title: 标题
            content: 内容
            tags: 标签
            theme: 主题
            
        Returns:
            文件路径
        """
        # 创建文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"article_{theme.replace(' ', '_')}_{timestamp}.md"
        filepath = os.path.join(ARTICLES_DIR, filename)
        
        # 生成完整内容
        full_content = f"{title}\n\n{content}\n\n"
        if tags:
            full_content += f"{' '.join(tags)}"
            
        # 保存文件
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(full_content)
            
        print(f"文章已保存到: {filepath}")
        return filepath
        
    def generate_and_save_article(self, theme: str) -> str:
        """
        生成并保存文章
        
        Args:
            theme: 主题
            
        Returns:
            文章文件路径
        """
        print(f"正在为主题 '{theme}' 生成文章内容...")
        
        # 生成内容
        title, content, tags = self.generate_article_content(theme)
        
        # 保存到文件
        filepath = self.save_article_to_file(title, content, tags, theme)
        
        return filepath

# 使用示例
if __name__ == "__main__":
    generator = ContentGenerator()
    
    # 测试生成文章
    test_theme = "人工智能"
    filepath = generator.generate_and_save_article(test_theme)
    print(f"测试文章已生成: {filepath}")