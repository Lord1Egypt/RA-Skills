"""
抖音发布技能 - 主模块
整合内容生成、图片生成和发布功能
"""

import os
import sys
import json
from datetime import datetime
from typing import Optional, Dict, Any

# 添加工作目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from generate_content import ContentGenerator
from generate_image import ImageGenerator
from publish import Publisher
from config import WORKSPACE_DIR, ARTICLES_DIR, IMAGES_DIR

class DouyinUploadSkill:
    """抖音发布技能主类"""
    
    def __init__(self):
        self.version = "1.0.0"
        self.description = "自动发布抖音文章内容"
        
        # 初始化各个模块
        self.content_generator = None
        self.image_generator = None
        self.publisher = None
        
        self.setup_skill()
        
    def setup_skill(self):
        """设置技能"""
        print("正在初始化抖音发布技能...")
        
        try:
            # 创建目录
            os.makedirs(ARTICLES_DIR, exist_ok=True)
            os.makedirs(IMAGES_DIR, exist_ok=True)
            
            # 初始化各个模块
            self.content_generator = ContentGenerator()
            self.image_generator = ImageGenerator()
            self.publisher = Publisher()
            
            print("✓ 技能初始化成功")
            
        except Exception as e:
            print(f"✗ 技能初始化失败: {e}")
            raise
            
    def validate_theme(self, theme: str) -> bool:
        """
        验证主题是否有效
        
        Args:
            theme: 主题
            
        Returns:
            主题是否有效
        """
        if not theme or not isinstance(theme, str) or len(theme.strip()) == 0:
            return False
            
        if len(theme) > 100:
            return False
            
        return True
        
    def get_theme_info(self, theme: str) -> Dict[str, Any]:
        """
        获取主题信息
        
        Args:
            theme: 主题
            
        Returns:
            主题信息字典
        """
        # 确定主题分类
        theme_categories = {
            "人工智能": "科技",
            "旅游": "生活", 
            "美食": "生活",
            "学习": "学习",
            "科技": "科技",
            "数码": "科技",
            "运动": "生活",
            "音乐": "生活",
            "电影": "娱乐",
            "设计": "生活",
            "美妆": "生活",
            "宠物": "生活"
        }
        
        category = "生活"
        for cat_keyword, cat in theme_categories.items():
            if cat_keyword in theme:
                category = cat
                break
                
        return {
            "theme": theme.strip(),
            "category": category,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
    def generate_article_content(self, theme: str, force_generate: bool = False) -> str:
        """
        生成文章内容
        
        Args:
            theme: 主题
            force_generate: 是否强制重新生成
            
        Returns:
            文章文件路径
        """
        if not self.validate_theme(theme):
            raise ValueError("无效的主题")
            
        print(f"🔄 为'{theme}'生成文章内容...")
        
        # 生成内容
        article_path = self.content_generator.generate_and_save_article(theme)
        
        print(f"✓ 文章内容已生成: {article_path}")
        return article_path
        
    def generate_cover_image(self, theme: str, article_title: str = None, force_generate: bool = False) -> str:
        """
        生成封面图片
        
        Args:
            theme: 主题
            article_title: 文章标题
            force_generate: 是否强制重新生成
            
        Returns:
            封面图片路径
        """
        if not self.validate_theme(theme):
            raise ValueError("无效的主题")
            
        print(f"🎨 为'{theme}'生成封面图片...")
        
        # 生成封面
        cover_path = self.image_generator.generate_and_save_cover(theme, article_title)
        
        if not cover_path:
            raise RuntimeError("封面图片生成失败")
            
        print(f"✓ 封面图片已生成: {cover_path}")
        return cover_path
        
    def publish_to_douyin(self, theme: str) -> Dict[str, Any]:
        """
        发布到抖音
        
        Args:
            theme: 主题
            
        Returns:
            发布结果
        """
        if not self.validate_theme(theme):
            raise ValueError("无效的主题")
            
        print(f"🚀 开始发布主题: {theme}")
        
        # 发布
        result = self.publisher.publish_theme(theme)
        
        return result
        
    def process_theme(self, theme: str, skip_publish: bool = False) -> Dict[str, Any]:
        """
        处理整个发布流程
        
        Args:
            theme: 主题
            skip_publish: 是否跳过发布步骤
            
        Returns:
            处理结果
        """
        if not self.validate_theme(theme):
            return {
                "success": False,
                "error": "无效的主题"
            }
            
        print(f"🎨 抖音发布技能 - 处理主题: {theme}")
        print("=" * 50)
        
        result = {
            "success": True,
            "theme": theme,
            "processed_at": datetime.now().isoformat(),
            "steps": {}
        }
        
        try:
            # 步骤1: 生成文章内容
            print("步骤1: 生成文章内容...")
            article_path = self.generate_article_content(theme)
            result["steps"]["content"] = {
                "success": True,
                "path": article_path
            }
            
            # 步骤2: 生成封面图片
            print("步骤2: 生成封面图片...")
            article_title = self.extract_title_from_file(article_path)
            cover_path = self.generate_cover_image(theme, article_title)
            result["steps"]["image"] = {
                "success": True,
                "path": cover_path
            }
            
            # 步骤3: 发布到抖音
            if not skip_publish:
                print("步骤3: 发布到抖音...")
                publish_result = self.publish_to_douyin(theme)
                result["steps"]["publish"] = publish_result
                
                if not publish_result.get("success"):
                    result["success"] = False
                    
            else:
                print("步骤3: 跳过发布步骤（仅生成内容和图片）")
                result["steps"]["publish"] = {
                    "success": True,
                    "skipped": True,
                    "message": "已跳过发布步骤"
                }
                
            # 步骤4: 创建处理日志
            print("步骤4: 创建处理日志...")
            self.create_process_log(result)
            
        except Exception as e:
            result["success"] = False
            result["error"] = str(e)
            print(f"✗ 处理过程中出错: {e}")
            
        print("=" * 50)
        return result
        
    def extract_title_from_file(self, file_path: str) -> Optional[str]:
        """
        从文章文件中提取标题
        
        Args:
            file_path: 文章文件路径
            
        Returns:
            标题，如果找不到返回None
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read().strip()
                
            # 简单提取第一行作为标题
            lines = content.split("\n")
            for line in lines:
                if line and not line.startswith("#"):
                    return line.strip()
                    
            return None
        except:
            return None
            
    def create_process_log(self, result: Dict[str, Any]) -> str:
        """
        创建处理日志
        
        Args:
            result: 处理结果
            
        Returns:
            日志文件路径
        """
        log_data = {
            "timestamp": result.get("processed_at"),
            "theme": result.get("theme"),
            "version": self.version,
            "success": result.get("success"),
            "steps": result.get("steps"),
            "error": result.get("error")
        }
        
        # 创建日志文件
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_filename = f"process_log_{result.get('theme').replace(' ', '_')}_{timestamp}.json"
        log_filepath = os.path.join(WORKSPACE_DIR, "logs", log_filename)
        
        # 确保logs目录存在
        os.makedirs(os.path.dirname(log_filepath), exist_ok=True)
        
        # 保存日志
        with open(log_filepath, "w", encoding="utf-8") as f:
            json.dump(log_data, f, ensure_ascii=False, indent=2)
            
        print(f"✓ 处理日志已保存到: {log_filepath}")
        return log_filepath
        
    def get_available_categories(self) -> list:
        """
        获取可用的主题分类
        
        Returns:
            分类列表
        """
        from config import THEME_CATEGORIES
        return list(THEME_CATEGORIES.keys())
        
    def get_available_styles(self) -> list:
        """
        获取可用的图片风格
        
        Returns:
            风格列表
        """
        from config import COVER_STYLES
        return COVER_STYLES
        
    def get_skill_status(self) -> Dict[str, Any]:
        """
        获取技能状态
        
        Returns:
            状态信息
        """
        status = {
            "name": "抖音发布技能",
            "version": self.version,
            "description": self.description,
            "available": True,
            "requirements": {
                "sau_command": self.publisher.check_sau_available() if self.publisher else False,
                "directories": {
                    "articles": os.path.exists(ARTICLES_DIR),
                    "images": os.path.exists(IMAGES_DIR),
                    "workspace": os.path.exists(WORKSPACE_DIR)
                }
            },
            "config": {
                "workspace_dir": WORKSPACE_DIR,
                "articles_dir": ARTICLES_DIR,
                "images_dir": IMAGES_DIR
            },
            "last_update": datetime.now().isoformat()
        }
        
        return status

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="抖音发布技能")
    parser.add_argument("theme", help="要发布的主题")
    parser.add_argument("--skip-publish", action="store_true", help="跳过发布步骤")
    parser.add_argument("--status", action="store_true", help="显示技能状态")
    parser.add_argument("--categories", action="store_true", help="显示可用分类")
    
    args = parser.parse_args()
    
    if args.status:
        # 显示技能状态
        skill = DouyinUploadSkill()
        status = skill.get_skill_status()
        print(json.dumps(status, ensure_ascii=False, indent=2))
        return
        
    if args.categories:
        # 显示可用分类
        skill = DouyinUploadSkill()
        categories = skill.get_available_categories()
        print("可用主题分类:")
        for cat in categories:
            print(f"  - {cat}")
        return
        
    if not args.theme:
        print("请提供主题参数")
        return
        
    # 执行发布
    try:
        skill = DouyinUploadSkill()
        result = skill.process_theme(args.theme, skip_publish=args.skip_publish)
        
        if result.get("success"):
            print("✓ 处理成功！")
            if result.get("steps", {}).get("publish", {}).get("skipped"):
                print("  (已跳过发布步骤，仅生成内容)")
        else:
            print(f"✗ 处理失败: {result.get('error')}")
            
    except ValueError as e:
        print(f"✗ 错误: {e}")
    except Exception as e:
        print(f"✗ 未知错误: {e}")

if __name__ == "__main__":
    main()