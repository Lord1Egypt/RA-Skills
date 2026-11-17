"""拼接器抽象基类 — 定义所有拼接 Provider 的标准接口。

所有拼接器必须实现 BaseStitcher，注册后通过 stitch.py 自动发现调用。
"""
from typing import Optional


class BaseStitcher:
    """拼接器基类。子类必须设置 name 并实现所有静态方法。"""

    name: str = "base"

    @staticmethod
    def check_available() -> bool:
        """检查当前环境是否支持该拼接器。"""
        return False

    @staticmethod
    def run(project: str, shot_count: int = 0,
            script_config: Optional[dict] = None) -> Optional[str]:
        """执行拼接，返回 final.mp4 路径，失败返回 None。"""
        raise NotImplementedError

    @staticmethod
    def embed_to_doc(docx_token: str, video_path: str) -> str:
        """将视频上传到飞书文档，返回视频 token。"""
        return ""


class StitcherRegistry:
    """拼接器注册表 — 管理所有可用的拼接 Provider。"""

    _providers: list[type[BaseStitcher]] = []

    @classmethod
    def register(cls, provider_cls: type[BaseStitcher]) -> type[BaseStitcher]:
        """注册拼接器（可作为装饰器使用）。"""
        if provider_cls not in cls._providers:
            cls._providers.append(provider_cls)
        return provider_cls

    @classmethod
    def get_available(cls) -> list[type[BaseStitcher]]:
        """返回当前环境下可用的拼接器列表（通过 check_available 筛选）。"""
        return [p for p in cls._providers if p.check_available()]

    @classmethod
    def run_first(cls, project: str, shot_count: int = 0,
                  script_config: Optional[dict] = None) -> Optional[str]:
        """按注册顺序尝试每个拼接器，第一个成功的返回结果。"""
        for provider_cls in cls.get_available():
            try:
                result = provider_cls.run(project, shot_count, script_config)
                if result:
                    return result
            except Exception as e:
                print(f"  [stitch] ⚠️ {provider_cls.name} 失败: {e}")
        return None
