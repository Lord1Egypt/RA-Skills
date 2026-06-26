"""
抖音发布技能 - 发布模块
调用sau命令发布文章到抖音
"""

import os
import sys
import subprocess
import json
from datetime import datetime
from typing import Optional, Dict, Any

# 添加工作目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import (
    WORKSPACE_DIR, ARTICLES_DIR, IMAGES_DIR, PUBLISH_CONFIG,
    THEME_CATEGORIES, COVER_STYLES
)

class Publisher:
    """发布器"""
    
    def __init__(self):
        self.setup_directories()
        
    def setup_directories(self):
        """创建必要的目录结构"""
        os.makedirs(ARTICLES_DIR, exist_ok=True)
        os.makedirs(IMAGES_DIR, exist_ok=True)
        
    def check_sau_available(self) -> bool:
        """
        检查sau命令是否可用
        
        Returns:
            是否可用
        """
        try:
            # 检查sau命令是否存在
            result = subprocess.run(
                ["which", "sau"],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                print("✓ 发现sau命令")
                return True
            else:
                print("✗ 未找到sau命令")
                return False
        except Exception as e:
            print(f"检查sau命令时出错: {e}")
            return False
            
    def find_article_file(self, theme: str) -> Optional[str]:
        """
        查找对应主题的文章文件
        
        Args:
            theme: 主题
            
        Returns:
            文章文件路径，如果找不到返回None
        """
        try:
            # 获取最近生成的文章文件
            files = os.listdir(ARTICLES_DIR)
            matching_files = []
            
            for file in files:
                if file.startswith(f"article_{theme.replace(' ', '_')}") and file.endswith(".md"):
                    matching_files.append(file)
                    
            if matching_files:
                # 返回最新创建的文件
                latest_file = max(matching_files, key=lambda f: os.path.getmtime(os.path.join(ARTICLES_DIR, f)))
                return os.path.join(ARTICLES_DIR, latest_file)
                
            return None
        except Exception as e:
            print(f"查找文章文件时出错: {e}")
            return None
            
    def find_cover_file(self, theme: str) -> Optional[str]:
        """
        查找对应的封面图片文件
        
        Args:
            theme: 主题
            
        Returns:
            封面图片路径，如果找不到返回None
        """
        try:
            # 获取最近生成的封面图片
            files = os.listdir(IMAGES_DIR)
            matching_files = []
            
            for file in files:
                if file.startswith(f"cover_{theme.replace(' ', '_')[:20]}") and file.endswith((".jpg", ".jpeg", ".png")):
                    matching_files.append(file)
                    
            if matching_files:
                # 返回最新创建的文件
                latest_file = max(matching_files, key=lambda f: os.path.getmtime(os.path.join(IMAGES_DIR, f)))
                return os.path.join(IMAGES_DIR, latest_file)
                
            return None
        except Exception as e:
            print(f"查找封面图片时出错: {e}")
            return None
            
    def validate_files(self, article_path: str, cover_path: str) -> bool:
        """
        验证文件是否有效
        
        Args:
            article_path: 文章文件路径
            cover_path: 封面图片路径
            
        Returns:
            文件是否有效
        """
        if not article_path or not os.path.exists(article_path):
            print("✗ 文章文件不存在")
            return False
            
        if not cover_path or not os.path.exists(cover_path):
            print("✗ 封面图片不存在")
            return False
            
        # 检查文件大小
        article_size = os.path.getsize(article_path)
        cover_size = os.path.getsize(cover_path)
        
        if article_size == 0:
            print("✗ 文章文件为空")
            return False
            
        if cover_size == 0:
            print("✗ 封面图片为空")
            return False
            
        print("✓ 文件验证通过")
        return True
        
    def prepare_publish_command(self, article_path: str, cover_path: str) -> str:
        """
        准备发布命令
        
        Args:
            article_path: 文章文件路径
            cover_path: 封面图片路径
            
        Returns:
            完整的发布命令
        """
        command = f"{PUBLISH_CONFIG['sau_command']} {PUBLISH_CONFIG['platform']} {PUBLISH_CONFIG['account_name']} upload-article \"{article_path}\" --cover \"{cover_path}\""
        return command
        
    def execute_publish_command(self, command: str) -> Dict[str, Any]:
        """
        执行发布命令
        
        Args:
            command: 发布命令
            
        Returns:
            发布结果字典
        """
        print(f"执行发布命令: {command}")
        
        try:
            # 执行命令
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=300  # 5分钟超时
            )
            
            output = result.stdout
            error = result.stderr
            
            if result.returncode == 0 and len(output.strip()) > 0:
                # 解析抖音的响应
                response = self.parse_douyin_response(output)
                return {
                    "success": True,
                    "output": output,
                    "response": response,
                    "command": command
                }
            else:
                # 错误处理
                error_msg = f"发布失败 - {command}\n"
                error_msg += f"返回码: {result.returncode}\n"
                if output:
                    error_msg += f"输出: {output}\n"
                if error:
                    error_msg += f"错误: {error}\n"
                    
                return {
                    "success": False,
                    "error": error_msg,
                    "output": output,
                    "error_output": error,
                    "command": command
                }
                
        except subprocess.TimeoutExpired:
            error_msg = f"发布超时 - {command}"
            return {
                "success": False,
                "error": error_msg,
                "command": command
            }
        except Exception as e:
            error_msg = f"执行发布命令时出错: {e}\n命令: {command}"
            return {
                "success": False,
                "error": error_msg,
                "command": command
            }
            
    def parse_douyin_response(self, output: str) -> Dict[str, Any]:
        """
        解析抖音API响应
        
        Args:
            output: 抖音返回的原始输出
            
        Returns:
            解析后的响应字典
        """
        try:
            # 尝试解析JSON响应
            if '{' in output and '}' in output:
                start = output.find('{')
                end = output.rfind('}') + 1
                json_str = output[start:end]
                return json.loads(json_str)
            else:
                # 无JSON响应的情况
                return {"raw_output": output}
        except:
            # 解析失败，直接返回原始输出
            return {"raw_output": output}
            
    def create_publish_log(self, result: Dict[str, Any], theme: str) -> str:
        """
        创建发布日志
        
        Args:
            result: 发布结果
            theme: 主题
            
        Returns:
            日志文件路径
        """
        log_data = {
            "timestamp": datetime.now().isoformat(),
            "theme": theme,
            "command": result.get("command"),
            "success": result.get("success"),
            "output": result.get("output"),
            "response": result.get("response"),
            "error": result.get("error"),
            "error_output": result.get("error_output")
        }
        
        # 创建日志文件
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_filename = f"publish_log_{theme.replace(' ', '_')}_{timestamp}.json"
        log_filepath = os.path.join(WORKSPACE_DIR, "logs", log_filename)
        
        # 确保logs目录存在
        os.makedirs(os.path.dirname(log_filepath), exist_ok=True)
        
        # 保存日志
        with open(log_filepath, "w", encoding="utf-8") as f:
            json.dump(log_data, f, ensure_ascii=False, indent=2)
            
        return log_filepath
        
    def publish_theme(self, theme: str) -> Dict[str, Any]:
        """
        发布指定主题的内容到抖音
        
        Args:
            theme: 主题
            
        Returns:
            发布结果
        """
        print(f"开始发布主题: {theme}")
        
        # 检查sau命令
        if not self.check_sau_available():
            return {
                "success": False,
                "error": "sau命令不可用，请先安装并配置抖音发布工具"
            }
            
        # 查找文件
        article_path = self.find_article_file(theme)
        cover_path = self.find_cover_file(theme)
        
        if not article_path:
            return {
                "success": False,
                "error": f"找不到匹配主题 '{theme}' 的文章文件"
            }
            
        if not cover_path:
            return {
                "success": False,
                "error": f"找不到匹配主题 '{theme}' 的封面图片"
            }
            
        # 验证文件
        if not self.validate_files(article_path, cover_path):
            return {
                "success": False,
                "error": "文件验证失败"
            }
            
        # 准备命令
        command = self.prepare_publish_command(article_path, cover_path)
        
        # 执行发布
        result = self.execute_publish_command(command)
        
        # 保存日志
        if result.get("success"):
            log_file = self.create_publish_log(result, theme)
            print(f"✓ 发布成功！日志已保存到: {log_file}")
        else:
            print(f"✗ 发布失败: {result.get('error')}")
            
        return result

# 使用示例
if __name__ == "__main__":
    publisher = Publisher()
    
    # 测试发布
    test_theme = "人工智能"
    result = publisher.publish_theme(test_theme)
    
    if result.get("success"):
        print("测试发布成功！")
    else:
        print(f"测试发布失败: {result.get('error')}")