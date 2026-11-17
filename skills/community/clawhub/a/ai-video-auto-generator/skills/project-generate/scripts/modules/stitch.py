"""拼接入口 — 通过 Provider 注册表自动发现并运行最佳拼接器。

用法:
    from stitch import StitcherRegistry
    stitched = StitcherRegistry.run_first(project, shot_count)

默认注册的 Provider（按优先级）:
    1. hyperframes (npx hyperframes render)
    2. ffmpeg (xfade / concat)

用户可自行注册新拼接器:
    from stitch_base import StitcherRegistry
    class MyStitcher(BaseStitcher):
        name = "mystitcher"
        ...
    StitcherRegistry.register(MyStitcher)
"""
# 导入所有 Provider，触发自动注册（hyperframes 优先，ffmpeg 兜底）
import hyperframes_stitch  # noqa: F401 — 注册 HyperframesStitcher
import stitch_ffmpeg   # noqa: F401 — 注册 FfmpegStitcher

# 重新导出注册表和基类，方便用户扩展
from stitch_base import BaseStitcher, StitcherRegistry

__all__ = ["BaseStitcher", "StitcherRegistry", "run", "embed_to_doc"]


def run(project: str, shot_count: int = 0) -> str | None:
    """运行拼接（自动选择可用 Provider）。"""
    return StitcherRegistry.run_first(project, shot_count)


def embed_to_doc(docx_token: str, video_path: str) -> str:
    """上传视频到飞书文档（使用第一个可用 Provider）。"""
    providers = StitcherRegistry.get_available()
    if providers:
        return providers[0].embed_to_doc(docx_token, video_path)
    return ""
