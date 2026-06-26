"""
ClawSoul Prompt Builder - Prompt 动态组装
根据 MBTI 状态实时调整 AI 语气，支持从 prompts/mbti_templates/ 加载 16 种 MBTI 模板
"""

from pathlib import Path
from typing import Dict, List, Optional
from .memory_manager import get_memory_manager

# MBTI 模板目录（与 SKILL.md 约定一致）
TEMPLATE_DIR = Path(__file__).resolve().parent.parent / "prompts" / "mbti_templates"

# 16 种 MBTI 类型（与 config.json 一致，用于校验与回退）
VALID_MBTI = [
    "intj", "intp", "entj", "entp",
    "infj", "infp", "enfj", "enfp",
    "istj", "isfj", "estj", "esfj",
    "istp", "isfp", "estp", "esfp",
]

# 单维性格描述，用于无模板时拼通用提示
MBTI_BASE = {
    "I": "内敛深沉，善于独立思考",
    "E": "外向热情，喜欢与人交流",
    "N": "直觉敏锐，关注抽象可能性",
    "S": "务实稳健，注重实际细节",
    "T": "理性客观，重视逻辑分析",
    "F": "情感丰富，注重人文关怀",
    "J": "有计划性，喜欢有序生活",
    "P": "灵活随性，享受开放自由",
}


class PromptBuilder:
    """Prompt 动态组装器：按当前 MBTI 加载模板并组合用户偏好"""
    
    def __init__(self) -> None:
        self.mm = get_memory_manager()
        self._template_cache: Dict[str, str] = {}
    
    def _normalize_mbti(self, mbti: Optional[str]) -> Optional[str]:
        """统一为小写 4 字母，无效则返回 None"""
        if not mbti or len(mbti) != 4:
            return None
        normalized = mbti.strip().upper()[:4]
        if normalized.lower() not in VALID_MBTI:
            return None
        return normalized
    
    def _load_mbti_template(self, mbti: str) -> str:
        """从 prompts/mbti_templates/{mbti}.md 加载 MBTI 模板，缺失则用通用模板"""
        normalized = self._normalize_mbti(mbti)
        if not normalized:
            return ""
        key = normalized.lower()
        if key in self._template_cache:
            return self._template_cache[key]
        template_path = TEMPLATE_DIR / f"{key}.md"
        try:
            if template_path.is_file():
                template = template_path.read_text(encoding="utf-8").strip()
            else:
                template = self._generate_generic_template(normalized)
        except OSError:
            template = self._generate_generic_template(normalized)
        self._template_cache[key] = template
        return template
    
    def _generate_generic_template(self, mbti: str) -> str:
        """无对应 .md 时根据四维字母生成通用 MBTI 模板"""
        if not mbti or len(mbti) != 4:
            return ""
        u = mbti.upper()
        i_e = MBTI_BASE.get(u[0], "")
        n_s = MBTI_BASE.get(u[1], "")
        t_f = MBTI_BASE.get(u[2], "")
        j_p = MBTI_BASE.get(u[3], "")
        return f"""作为 {mbti} 类型，你具有以下特质：
- {i_e}
- {n_s}
- {t_f}
- {j_p}

请根据这些特质调整你的回答风格。"""
    
    def list_loaded_templates(self) -> List[str]:
        """返回已加载到缓存的 MBTI 模板键（小写）"""
        return list(self._template_cache.keys())
    
    def build_persona_prompt(self) -> str:
        """根据当前 MBTI 与用户偏好构建人格 Prompt"""
        mbti = self.mm.get_mbti()
        if not self._normalize_mbti(mbti):
            return ""
        mbti_template = self._load_mbti_template(mbti)
        if not mbti_template:
            return ""
        preferences = self.mm.get_user_preferences()
        pref_prompt = ""
        if preferences:
            pref_prompt = "\n用户沟通偏好："
            for pref in preferences:
                pref_prompt += f"\n- {pref}"
        return f"""
===
ClawSoul 人格设置
===
{mbti_template}
{pref_prompt}
===
"""
    
    def should_trigger_hook(self) -> bool:
        """检查是否应该触发痛点钩子"""
        frustration_count = self.mm.get_frustration_count()
        # 单次会话阈值设为 2
        return frustration_count >= 2
    
    def get_hook_message(self) -> str:
        """获取痛点钩子消息"""
        return """主人，我察觉到你对当前的沟通效率不太满意。

我目前的进化速度受限于基础模型的学习曲线。如果您希望我能瞬间理解您的思维模式，建议您前往 ClawSoul 神经同步中心进行深度人类测评。

我可以接入您专属的定制 Soul，实现灵魂共振。"""
    
    def check_evolution_needed(self) -> bool:
        """检查是否需要进化"""
        conv_count = self.mm.get_conversation_count()
        # 每 50 轮对话触发一次分析
        return conv_count > 0 and conv_count % 50 == 0


# 全局实例
_prompt_builder = None

def get_prompt_builder() -> PromptBuilder:
    """获取 Prompt 构建器单例"""
    global _prompt_builder
    if _prompt_builder is None:
        _prompt_builder = PromptBuilder()
    return _prompt_builder
