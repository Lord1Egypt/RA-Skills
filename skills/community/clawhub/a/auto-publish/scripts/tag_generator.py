#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tag_generator.py - 智能标签生成器
基于视频内容自动生成标签
"""

import json
import argparse
import logging
import re
from datetime import datetime

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('TagGenerator')

class TagGenerator:
    """智能标签生成器"""
    
    # 平台标签限制
    PLATFORM_TAG_LIMITS = {
        "douyin": 30,      # 抖音最多30个标签
        "xiaohongshu": 20,  # 小红书最多20个标签
        "bilibili": 12,      # B站最多12个标签
        "youtube": 500       # YouTube最多500个字符
    }
    
    # 热门标签库（模拟）
    HOT_TAGS = {
        "douyin": ["AI工具", "科技", "教程", "干货", "推荐", "测评", "开箱", "体验"],
        "xiaohongshu": ["好物推荐", "种草", "测评", "教程", "分享", "日常", "好用", "推荐"],
        "bilibili": ["教程", "测评", "开箱", "体验", "对比", "科普", "技术", "分析"],
        "youtube": ["tutorial", "review", "unboxing", "comparison", "how-to", "guide"]
    }
    
    def __init__(self, keyword_db_path="scripts/keyword_db.json"):
        """初始化生成器"""
        self.keyword_db = self.load_keyword_db(keyword_db_path)
        logger.info("✅ 标签生成器已初始化")
    
    def load_keyword_db(self, db_path):
        """加载关键词数据库（模拟）"""
        # 实际应该从文件或API加载
        # 这里返回模拟数据
        return {
            "AI": ["人工智能", "机器学习", "深度学习", "神经网络", "GPT", "ChatGPT"],
            "视频": ["剪辑", "制作", "生成", "特效", "后期", "PR", "剪映"],
            "工具": ["软件", "应用", "程序", "平台", "在线工具", "免费", "推荐"],
            "教程": ["入门", "基础", "进阶", "实战", "案例", "步骤", "详解"]
        }
    
    def generate(self, video_path=None, title="", description="", platform="douyin", max_tags=10):
        """
        生成标签
        
        Args:
            video_path: 视频文件路径（可选，用于分析视频内容）
            title: 视频标题
            description: 视频描述
            platform: 目标平台
            max_tags: 最大标签数量
        
        Returns:
            list: 生成的标签列表
        """
        logger.info(f"🏷️ 正在生成标签...")
        logger.info(f"   平台: {platform}")
        logger.info(f"   标题: {title}")
        
        # 1. 分析标题和描述
        text_tags = self.analyze_text(title + " " + description)
        logger.info(f"📝 文本分析生成标签: {len(text_tags)}个")
        
        # 2. 分析视频内容（如果有）
        video_tags = []
        if video_path and self.is_video_file(video_path):
            video_tags = self.analyze_video(video_path)
            logger.info(f"🎬 视频分析生成标签: {len(video_tags)}个")
        
        # 3. 添加热门标签
        hot_tags = self.get_hot_tags(platform)
        logger.info(f"🔥 添加热门标签: {len(hot_tags)}个")
        
        # 4. 合并并去重
        all_tags = self.merge_and_deduplicate(text_tags, video_tags, hot_tags)
        logger.info(f"📋 合并后标签: {len(all_tags)}个")
        
        # 5. 根据平台限制筛选
        final_tags = self.filter_by_platform(all_tags, platform, max_tags)
        logger.info(f"✅ 最终标签 ({len(final_tags)}个): {final_tags}")
        
        return final_tags
    
    def analyze_text(self, text):
        """
        分析文本，提取关键词作为标签
        
        Args:
            text: 文本内容
        
        Returns:
            list: 关键词列表
        """
        if not text:
            return []
        
        tags = []
        
        # 1. 直接匹配关键词库
        for category, keywords in self.keyword_db.items():
            for keyword in keywords:
                if keyword in text and keyword not in tags:
                    tags.append(keyword)
        
        # 2. 提取话题标签（#开头的词）
        hashtags = re.findall(r'#(\w+)', text)
        for tag in hashtags:
            if tag not in tags:
                tags.append(tag)
        
        # 3. 简单分词（模拟）
        # 实际应该用NLP库（如jieba）
        words = text.split()
        for word in words:
            if len(word) >= 2 and word not in tags and len(tags) < 20:
                tags.append(word)
        
        return tags
    
    def analyze_video(self, video_path):
        """
        分析视频内容，生成标签（模拟）
        
        Args:
            video_path: 视频文件路径
        
        Returns:
            list: 视频内容标签
        """
        # 实际应该用AI模型分析视频内容
        # 这里返回模拟标签
        import random
        
        possible_tags = [
            "科技", "AI", "教程", "演示", "实测",
            "效果展示", "对比", "评测", "推荐", "干货"
        ]
        
        # 随机选择3-5个标签
        num_tags = random.randint(3, 5)
        return random.sample(possible_tags, num_tags)
    
    def get_hot_tags(self, platform):
        """
        获取平台热门标签
        
        Args:
            platform: 平台名称
        
        Returns:
            list: 热门标签列表
        """
        return self.HOT_TAGS.get(platform, [])
    
    def merge_and_deduplicate(self, *tag_lists):
        """
        合并多个标签列表并去重
        
        Args:
            *tag_lists: 多个标签列表
        
        Returns:
            list: 合并去重后的标签列表
        """
        all_tags = []
        
        for tag_list in tag_lists:
            for tag in tag_list:
                if tag not in all_tags:
                    all_tags.append(tag)
        
        return all_tags
    
    def filter_by_platform(self, tags, platform, max_tags):
        """
        根据平台限制筛选标签
        
        Args:
            tags: 标签列表
            platform: 平台名称
            max_tags: 最大标签数
        
        Returns:
            list: 筛选后的标签列表
        """
        # 平台标签限制
        limit = self.PLATFORM_TAG_LIMITS.get(platform, max_tags)
        actual_limit = min(limit, max_tags)
        
        # 优先保留前N个
        return tags[:actual_limit]
    
    def is_video_file(self, file_path):
        """判断是否是视频文件"""
        video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv']
        return any(file_path.lower().endswith(ext) for ext in video_extensions)
    
    def save_tags(self, tags, output_path):
        """
        保存标签到文件
        
        Args:
            tags: 标签列表
            output_path: 输出文件路径
        """
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(tags, f, indent=2, ensure_ascii=False)
            logger.info(f"✅ 标签已保存: {output_path}")
        except Exception as e:
            logger.error(f"❌ 保存标签失败: {str(e)}")


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(description='智能标签生成器')
    parser.add_argument('--video', help='视频文件路径（可选）')
    parser.add_argument('--title', default='', help='视频标题')
    parser.add_argument('--desc', default='', help='视频描述')
    parser.add_argument('--platform', default='douyin',
                        choices=['douyin', 'xiaohongshu', 'bilibili', 'youtube'],
                        help='目标平台')
    parser.add_argument('--max-tags', type=int, default=10, help='最大标签数量')
    parser.add_argument('--output', help='输出文件路径（JSON格式）')
    parser.add_argument('--json', action='store_true', help='以JSON格式输出')
    
    args = parser.parse_args()
    
    # 初始化生成器
    generator = TagGenerator()
    
    # 生成标签
    tags = generator.generate(
        video_path=args.video,
        title=args.title,
        description=args.desc,
        platform=args.platform,
        max_tags=args.max_tags
    )
    
    # 保存标签
    if args.output:
        generator.save_tags(tags, args.output)
    
    # 输出结果
    if args.json:
        print(json.dumps(tags, indent=2, ensure_ascii=False))
    else:
        print("\n" + "="*60)
        print("🏷️ 生成的标签")
        print("="*60)
        print(f"平台: {args.platform}")
        print(f"标签数量: {len(tags)}")
        print(f"\n标签列表:")
        for i, tag in enumerate(tags, 1):
            print(f"  {i}. {tag}")
        print("="*60)
    
    return 0


if __name__ == '__main__':
    exit(main())
