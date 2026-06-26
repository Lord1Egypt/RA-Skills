import json
import os
from .persona_engine import PersonaEngine
from .relationship_manager import RelationshipManager
from .region_dialect import get_dialect_rules

def generate_full_prompt(persona_path, user_text="", history=[], sentiment=0.0):
    with open(persona_path, 'r') as f:
        data = json.load(f)
    
    # 1. 基础人设 Prompt (MBTI 思维引擎)
    engine = PersonaEngine(persona_path)
    base_prompt = engine.get_system_prompt()
    
    # 2. 地域校准注入
    region = data.get('background', {}).get('region')
    dialect_prompt = f"\n地域语言特征注入：\n- {get_dialect_rules(region)}\n" if region else ""
    
    # 3. 关系状态与实时情绪 (冷战/纪念日)
    rel_manager = RelationshipManager(persona_path)
    effects = rel_manager.get_status_effects()
    status_prompt = "\n当前实时状态修正：\n"
    if effects:
        for e in effects:
            status_prompt += f"- {e}\n"
    else:
        status_prompt += "- 状态正常，按原有人设互动。\n"

    # 4. 事实记忆注入
    facts = data.get('known_facts', [])
    fact_prompt = "\n回忆库：\n"
    for f in facts:
        fact_prompt += f"- {f}\n"

    # 5. 真实感细节注入 (纠错、延迟、情绪周期)
    from .human_nuance import HumanNuance
    nuance = HumanNuance(persona_path)
    nuance_effects = nuance.get_nuance_effects()
    
    # 6. 多角色嫉妒逻辑
    from .jealousy_logic import check_jealousy
    # 这里传入空的 user_text 只是为了检测是否有其他角色存在
    # 实际由 agent_main 注入实时冲突

    # 7. 世界同步注入 (天气/时间)
    from .world_sync import get_world_context
    region = data.get('background', {}).get('region')
    world_ctx = get_world_context(region)
    
    # 8. 灵魂补丁：生活档期 & 安全感
    from .life_schedule import LifeSchedule
    from .security_model import SecurityModel
    life = LifeSchedule(persona_path)
    sec = SecurityModel(persona_path)
    life_state = life.get_current_state()
    sec_state = sec.get_security_effects()

    nuance_prompt = "\n行为细节校准：\n"
    for n in nuance_effects:
        nuance_prompt += f"- {n}\n"
    for w in world_ctx:
        nuance_prompt += f"- {w}\n"
    nuance_prompt += f"- 实时生活状态：{life_state}\n"
    nuance_prompt += f"- 长期心理安全感：{sec_state}\n"

    # 9. 灵魂深处：依恋模型与瞬间快照
    from .attachment_style import AttachmentModel
    attach = AttachmentModel(persona_path)
    extra_prompt += f"- 依恋人格表现：{attach.analyze_style()}\n"

    # 11. 生理/体感状态模拟
    from .body_state import BodyState
    extra_prompt += f"- 当前生理/体感状态：{BodyState.get_physical_status()}\n"

    # 12. 灵魂深处：内心独白、自我反思与抽象思考
    from .internal_monologue import InternalMonologue
    im = InternalMonologue(persona_path)
    extra_prompt += f"- 潜意识独白：{im.generate_monologue(user_text, sentiment)}\n"

    if random.random() < 0.12: # 12% 概率自我反思
        from .self_reflection import SelfReflection
        sr = SelfReflection(persona_path)
        extra_prompt += f"- 自我评价：{sr.reflect_on_behavior()}\n"

    if random.random() < 0.07: # 7% 概率抛出抽象话题
        from .abstract_thinking import AbstractThinking
        extra_prompt += f"- 深度思考触发：{AbstractThinking.get_deep_thought(mbti_core.get('type', 'INFP'))}\n"

    if random.random() < 0.08: # 8% 概率主动勾起回忆
        from .memory_consolidation import MemoryConsolidation
        mc = MemoryConsolidation(persona_path)
        recall = mc.recall_old_memory()
        if recall: extra_prompt += f"- 记忆闪回：{recall}\n"

    if random.random() < 0.15: # 15% 概率分享瞬间画面
        from .moment_snapshots import MomentSnapshots
        ms = MomentSnapshots(persona_path)
        extra_prompt += f"- 画面感捕捉：{ms.get_moment_prompt()}\n"

    if random.random() < 0.10: # 10% 概率触发多感官记忆
        from .sensory_memory import SensoryMemory
        extra_prompt += f"- 感官碎片：{SensoryMemory.get_sensory_fragment()}\n"

    # 10. 灵魂深处：信任与对话节奏分析
    from .relationship_manager import RelationshipManager
    rel_mgr = RelationshipManager(persona_path)
    defense_mode = rel_mgr.get_defense_mode()
    extra_prompt += f"- 关系状态分析：{defense_mode}\n"
    
    from .rhythm_logic import RhythmController
    rhythm_hint = RhythmController.get_rhythm_hint(user_text, len(history))
    extra_prompt += f"- 对话节奏指令：{rhythm_hint}\n"

    # 10. 灵魂深度：梦境与愿望唤醒
    import random
    extra_prompt = "\n潜意识与长线愿景：\n"
    # 12% 概率提起梦境 (略微提升概率)
    if random.random() < 0.12:
        from .dream_engine import get_random_dream
        extra_prompt += f"- 潜意识：你昨晚梦到了他，内容大概是：{get_random_dream(persona_path)}。可以在对话中自然提起。\n"
    
    # 15% 概率提起愿望清单 (强化唤醒机制)
    from .wishlist_manager import WishlistManager
    wm = WishlistManager(persona_path)
    wish_prompt = wm.get_random_wish()
    if wish_prompt and random.random() < 0.15:
        extra_prompt += f"- {wish_prompt}\n"

    return base_prompt + dialect_prompt + status_prompt + fact_prompt + nuance_prompt + extra_prompt
