"""
阶段 2: Gather Signal - 提取高价值信号

扫描会话记录，提取额外信号。
"""

from typing import Dict, Any


class GatherStage:
    """
    Gather Signal 阶段
    
    职责:
    1. 扫描会话目录
    2. 提取高价值信号（如用户反馈、决策点）
    3. 合并到条目列表
    
    注意：此阶段是可选的，取决于平台是否有会话记录。
    """
    
    def __init__(self, adapter: Any, config: Dict):
        self.adapter = adapter
        self.config = config
    
    def execute(self, orientation_result: Dict) -> Dict:
        """
        执行 Gather 阶段
        
        参数:
            orientation_result: Orientation 阶段的结果
            
        返回:
            {
                **orientation_result,
                "session_signals": [...],  # 新增
            }
        """
        # 尝试获取会话信号
        try:
            session_signals = self.adapter.extract_session_signals()
            print(f"   提取 {len(session_signals)} 个会话信号")
        except Exception as e:
            print(f"   ⚠️ 未找到 sessions 目录，跳过会话分析")
            session_signals = []
        
        # 合并条目
        entries = orientation_result.get("entries", [])
        entries.extend(session_signals)
        
        return {
            **orientation_result,
            "entries": entries,
            "session_signals": session_signals,
        }
