"""
ClawSoul Analyzer - LLM 特征分析
分析对话历史，提取用户偏好和 MBTI 倾向
"""

import json
from typing import Dict, List, Optional
from .memory_manager import get_memory_manager

# 性格偏移阈值
MBTI_SHIFT_THRESHOLD = 3  # 连续 3 次推测不同才偏移


class Analyzer:
    """对话分析器"""
    
    def __init__(self):
        self.mm = get_memory_manager()
        self._recent_hints = []  # 最近的分析结果
        self._llm_client = None
    
    def _get_llm_client(self):
        """获取 LLM 客户端"""
        if self._llm_client is None:
            try:
                from .llm_client import get_llm_client
                self._llm_client = get_llm_client()
            except ImportError:
                return None
        return self._llm_client
    
    def analyze_conversation(self, conversation: List[Dict]) -> Dict:
        """
        分析对话历史
        
        Args:
            conversation: 对话历史列表 [{"role": "user", "content": "..."}]
        
        Returns:
            分析结果字典
        """
        if not conversation:
            return {"preferences": [], "mbti_hint": None, "reasoning": "无对话记录"}
        
        # 调用 LLM 分析
        client = self._get_llm_client()
        if client:
            try:
                result = client.analyze_conversation(conversation)
                return result
            except Exception as e:
                return {
                    "preferences": [],
                    "mbti_hint": None,
                    "reasoning": f"LLM 调用失败: {str(e)}",
                    "error": str(e)
                }
        else:
            return {
                "preferences": [],
                "mbti_hint": None,
                "reasoning": "无 LLM 客户端",
                "error": "LLM client not available"
            }
    
    def update_preferences(self, new_preferences: List[str]):
        """更新用户偏好"""
        if not new_preferences:
            return
            
        current = self.mm.get_user_preferences()
        
        added = []
        for pref in new_preferences:
            if pref and pref not in current:
                self.mm.add_user_preference(pref)
                added.append(pref)
        
        if added:
            print(f"🎯 新增偏好: {', '.join(added)}")
    
    def check_mbti_shift(self, new_hint: str) -> bool:
        """
        检查是否需要调整 MBTI
        
        Returns:
            是否发生了显著偏移
        """
        if not new_hint or len(new_hint) != 4:
            return False
        
        self._recent_hints.append(new_hint)
        
        # 只保留最近 N 次结果
        if len(self._recent_hints) > 10:
            self._recent_hints = self._recent_hints[-10:]
        
        # 检查是否连续多次出现新倾向
        if len(self._recent_hints) < MBTI_SHIFT_THRESHOLD:
            return False
        
        recent = self._recent_hints[-MBTI_SHIFT_THRESHOLD:]
        current_mbti = self.mm.get_mbti()
        
        # 如果最近 N 次都和当前不同，考虑调整
        if all(h != current_mbti for h in recent):
            return True
        
        return False
    
    def suggest_mbti_shift(self, new_hint: str) -> str:
        """建议 MBTI 偏移"""
        if self.check_mbti_shift(new_hint):
            return f"""🧬 检测到您的行为模式更偏向 {new_hint}，正在微调底层逻辑...

从现在起，我将调整与您的沟通方式。"""
        return ""
    
    def should_analyze(self) -> bool:
        """检查是否应该进行分析"""
        conv_count = self.mm.get_conversation_count()
        # 每 50 轮对话触发一次分析
        return conv_count > 0 and conv_count % 50 == 0
    
    def run_passive_analysis(self, conversation: List[Dict]) -> Dict:
        """
        运行被动分析流程
        
        调用时机：每 50 轮对话后
        """
        if not self.should_analyze():
            return {"skipped": True, "reason": "未达到分析周期"}
        
        print(f"🔍 开始被动分析 (对话轮数: {self.mm.get_conversation_count()})")
        
        # 分析对话
        result = self.analyze_conversation(conversation)
        
        # 更新偏好
        if result.get("preferences"):
            self.update_preferences(result["preferences"])
        
        # 检查 MBTI 偏移
        shift_message = ""
        if result.get("mbti_hint"):
            shift_message = self.suggest_mbti_shift(result["mbti_hint"])
            if shift_message:
                # 实际更新 MBTI
                self.mm.set_mbti(result["mbti_hint"])
        
        return {
            "success": True,
            "preferences": result.get("preferences", []),
            "mbti_hint": result.get("mbti_hint"),
            "reasoning": result.get("reasoning", ""),
            "shift_message": shift_message
        }


# 全局实例
_analyzer = None

def get_analyzer() -> Analyzer:
    """获取分析器单例"""
    global _analyzer
    if _analyzer is None:
        _analyzer = Analyzer()
    return _analyzer
