"""
BiliYouTik2Brain — 管线构建器

职责单一：构建 pipeline_graph 节点图。
不执行图（在 process.py）。
"""

from .pipeline_graph import Graph
from .node_collect import _node_collect
from .node_transcribe import _node_transcribe
from .node_enhance import _node_enhance
from .node_ocr import _node_ocr
from .node_bleep import _node_bleep_detect
from .node_save import (
    _node_save_result, _node_update_knowledge, _node_auto_archive,
)
from .node_assess import _node_assess


def build_pipeline_graph(url: str) -> 'Graph':
    """构建视频处理管线任务图
    
    collect → assess → transcribe+ocr+bleep → enhance → save → (knowledge+archive)
    """
    g = Graph()
    
    # 节点1：采集
    g.add_node("collect", _node_collect, depends=[],
               kwargs={"url": url}, timeout=120, continue_on_error=False)
    
    # 节点2：评估（含Phase 2.1系统状态监控）
    g.add_node("assess", _node_assess, depends=["collect"],
               timeout=30, continue_on_error=False)
    
    # 节点3a：转录
    g.add_node("transcribe", _node_transcribe, depends=["assess"],
               max_retries=1, timeout=600, continue_on_error=True)
    
    # 节点3b：OCR并行
    g.add_node("ocr", _node_ocr, depends=["assess"],
               max_retries=0, timeout=120, continue_on_error=True)
    
    # 节点3c：BLEEP并行
    g.add_node("bleep_detect", _node_bleep_detect, depends=["assess"],
               timeout=30, continue_on_error=True)
    
    # 节点4：LLM修复
    g.add_node("enhance", _node_enhance, depends=["transcribe", "ocr", "bleep_detect"],
               max_retries=0, timeout=300, continue_on_error=True)
    
    # 节点5：保存
    g.add_node("save", _node_save_result, depends=["enhance"],
               max_retries=1, timeout=30, continue_on_error=False)
    
    # 节点6：知识库更新
    g.add_node("update_knowledge", _node_update_knowledge, depends=["enhance"],
               timeout=30, continue_on_error=True)
    
    # 节点7：知识自动归档
    g.add_node("auto_archive", _node_auto_archive, depends=["enhance", "save"],
               timeout=30, continue_on_error=True)
    
    return g
