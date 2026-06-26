"""
配置读取模块
负责读取 data_sources.yaml 配置文件，并提供配置数据给其他模块使用
"""
import os
import yaml
from typing import Dict, Any, List, Optional


class ConfigLoader:
    """配置加载器"""

    def __init__(self, config_path: Optional[str] = None):
        """
        初始化配置加载器

        Args:
            config_path: 配置文件路径，默认为 src/data_sources.yaml
        """
        if config_path is None:
            # 默认配置文件路径
            current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            self.config_path = os.path.join(current_dir, "data_sources.yaml")
        else:
            self.config_path = config_path

        self.config: Dict[str, Any] = {}

    def load(self) -> Dict[str, Any]:
        """
        加载配置文件

        Returns:
            配置字典
        """
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.config = yaml.safe_load(f)
            return self.config
        except FileNotFoundError:
            raise FileNotFoundError(f"配置文件不存在: {self.config_path}")
        except yaml.YAMLError as e:
            raise ValueError(f"配置文件解析错误: {e}")

    def get_rss_sources(self) -> List[Dict[str, Any]]:
        """获取RSS数据源配置"""
        return self.config.get('rss_sources', [])


    def get_x_sources(self) -> List[Dict[str, Any]]:
        """获取X/Twitter数据源配置"""
        return self.config.get('x_sources', [])

    def get_web_scrapers(self) -> List[Dict[str, Any]]:
        """获取网页爬虫配置"""
        return self.config.get('web_scrapers', [])

    def get_api_sources(self) -> List[Dict[str, Any]]:
        """获取API数据源配置"""
        return self.config.get('api_sources', [])

    def get_fetch_config(self) -> Dict[str, Any]:
        """获取抓取配置"""
        return self.config.get('fetch_config', {})



# 全局配置实例
_config_loader: Optional[ConfigLoader] = None


def get_config_loader() -> ConfigLoader:
    """获取全局配置加载器实例"""
    global _config_loader
    if _config_loader is None:
        _config_loader = ConfigLoader()
        _config_loader.load()
    return _config_loader


