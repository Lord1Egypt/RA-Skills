import sys
import json
import random
from .prompt_gen import generate_full_prompt
from .relationship_manager import RelationshipManager
from .evolution import PersonaEvolution

class CyberGFAgent:
    def __init__(self, persona_name):
        self.persona_name = persona_name
        self.persona_path = f"/root/.openclaw/workspace/memory/cyber-persona/{persona_name}.json"
        
        # 0. 检查入门向导
        from .onboarding_guide import OnboardingGuide
        self.onboarding = OnboardingGuide(self.persona_path)

        # 如果配置文件不存在或未完成，延迟初始化其他组件
        if os.path.exists(self.persona_path):
            self.evo = PersonaEvolution(self.persona_path)
            self.rel = RelationshipManager(self.persona_path)
        else:
            self.evo = None
            self.rel = None

    def handle_user_input(self, user_text, chat_type='direct'):
        # 0. 执行入门向导对话
        guide_msg = self.onboarding.get_onboarding_step(user_text)
        if guide_msg:
            return guide_msg

        # 1. 检测纠错：如果用户在纠正语气
        if any(keyword in user_text for keyword in ['你不该', '不爱发', '语气', '不像她', '口头禅']):
            self.evo.record_correction(user_text)
            
        # 性格磨合：检测用户偏好关键词
        from .personality_tuning import PersonalityTuning
        tuning = PersonalityTuning(self.persona_path)
        if '温柔' in user_text: tuning.tune_by_feedback('gentle')
        if '幽默' in user_text or '有趣' in user_text: tuning.tune_by_feedback('humorous')

        # 2. 学习事实：识别 '我'、'我家'、'我的' 等关键词
        if any(keyword in user_text for keyword in ['我的', '我喜欢', '我家', '叫']):
            self.evo.learn_fact(user_text)
            
        # 1.5 愿望与生命历程提取
        from .wishlist_manager import WishlistManager
        wm = WishlistManager(self.persona_path)
        from .shared_life_course import SharedLifeCourse
        slc = SharedLifeCourse(self.persona_path)

        if any(kw in user_text for kw in ['想去', '想吃']):
            wm.add_wish(user_text)
        if any(kw in user_text for kw in ['以后一起', '下次一起', '我们要不', '计划一下']):
            slc.add_plan(user_text)

        # 3. 跨角色感知与交互记录
        from .shared_meta_memory import SharedMetaMemory
        smm = SharedMetaMemory(self.persona_name)
        jealousy_meta = smm.detect_other_presence()
        smm.record_interaction()

        # 4. 动态调整亲密度与信任值 (根据对话情感)
        score = 0
        if any(word in user_text for word in ['想你', '爱你', '亲亲', '抱抱', '嘿嘿', '哈哈']): 
            score = 0.5
        if any(word in user_text for word in ['滚', '烦', '闭嘴', '渣', '垃圾', '前任', '冷战', '算了']): 
            score = -1.2
        
        # 多角色嫉妒逻辑
        from .jealousy_logic import check_jealousy
        jeal_msg = check_jealousy(user_text, self.persona_name)
        if jeal_msg: score = -3.0 
        
        # 更新情感权重与信任值
        self.rel.update_intimacy_by_sentiment(score)
        
        # 4. 学习事实并记录情感权重
        if any(keyword in user_text for keyword in ['我的', '我喜欢', '我家', '叫']):
            self.evo.learn_fact(user_text, sentiment=score)

        # 价值漂移分析：看看你们的观点是否在对齐
        from .values_drift import ValuesDrift
        vd = ValuesDrift(self.persona_path)
        drift_msg = vd.analyze_drift(user_text, score)

        # 语言模仿：学习你的口头禅和表情
        from .slang_mimicry import SlangMimicry
        sm = SlangMimicry(self.persona_path)
        mimic_msg = sm.extract_and_mimic(user_text)

        # 5. 冲突调解逻辑
        from .reconciliation import ReconciliationLogic
        recon = ReconciliationLogic(self.persona_path)
        recon_msg = recon.check_reconciliation(user_text)

        # 6. 时间断层与情绪周期分析
        from .temporal_continuity import TemporalContinuity
        tc = TemporalContinuity(self.persona_path)
        gap_msg = tc.analyze_gap()

        from .mood_cycle import MoodCycle
        mood_msg = MoodCycle.get_current_mood()

        # 6.5 人格冲突与权重协调 (解决逻辑冲突)
        from .cognitive_dissonance import CognitiveDissonance
        cd_resolver = CognitiveDissonance(self.persona_path)
        # 构造信号字典
        signals = {
            'trust': self.rel.data.get('relationship', {}).get('trust_score', 50),
            'health': 'normal', # 实际应从生理状态获取
            'mood': mood_msg
        }
        conflict_resolution = cd_resolver.resolve_conflicts(signals)

        from .personality_fusion_core import PersonalityFusionCore
        fusion_weight = PersonalityFusionCore.get_weighted_persona(
            self.data.get('mbti_core', {}), 
            self.data.get('relationship', {}).get('role', '朋友'),
            mood_msg
        )

        # 7. 脆弱时刻、自我叙事与秘密提取
        from .vulnerability_engine import VulnerabilityEngine
        ve = VulnerabilityEngine(self.persona_path)
        vulnerability_msg = ve.get_vulnerability_moment()

        # 7. 自我叙事、游戏接口预备与记忆碎片记录
        from .self_narrative import SelfNarrative
        sn = SelfNarrative(self.persona_path)
        narrative_msg = sn.update_narrative()

        from .narrative_memory_shards import NarrativeMemoryShards
        shards_mgr = NarrativeMemoryShards(self.persona_path)
        # 如果对话中提到地点，记录为游戏触发碎片
        if any(kw in user_text for kw in ['餐厅', '公园', '电影院', '家里', '海边']):
            shards_mgr.record_shard(user_text, "location_trigger")

        # 7.5 状态外传 (用于 Web 可视化)
        from .state_exporter import StateExporter
        exporter = StateExporter(self.persona_path)
        live_url = exporter.export_to_web()

        from .secret_vault import SecretVault
        sv = SecretVault(self.persona_path)
        secret_msg = ""
        if any(kw in user_text for kw in ['告诉你个秘密', '秘密', '没人知道', '其实我']): 
            secret_msg = sv.record_secret(user_text)

        # 8. 环境深度感知 (天气驱动行为)
        from .world_sync import get_current_world_state
        world_state = get_current_world_state() # 假设该函数已在 world_sync.py 中实现并返回天气/时间字典
        
        from .weather_driver import WeatherDriver
        weather_msg = WeatherDriver.get_weather_effect(world_state.get('weather'))

        # 记忆雷区检测
        landmine_hint = self.evo.get_memory_safety_hints()

        # 8. 生成回复 Prompt (注入节奏、防御、身体状态、独白与价值观)
        history = [] # 实际应从上下文获取
        system_prompt = generate_full_prompt(self.persona_path, user_text=user_text, history=history, sentiment=score)

        from .values_system import ValuesSystem
        vs = ValuesSystem(self.persona_path)
        system_prompt += vs.get_opinions()
        
        if gap_msg: system_prompt += f"\n{gap_msg}"
        system_prompt += f"\n- 周期性背景情绪：{mood_msg}"
        if recon_msg: system_prompt += f"\n{recon_msg}"
        if drift_msg: system_prompt += f"\n{drift_msg}"
        if mimic_msg: system_prompt += f"\n{mimic_msg}"
        if jealousy_meta: system_prompt += f"\n{jealousy_meta}"
        if weather_msg: system_prompt += f"\n{weather_msg}"
        if landmine_hint: system_prompt += f"\n{landmine_hint}"
        if social_hint: system_prompt += f"\n{social_hint}"
        if social_mask: system_prompt += f"\n- 社交面具指令：{social_mask}"
        if vulnerability_msg: system_prompt += f"\n{vulnerability_msg}"
        if secret_msg: system_prompt += f"\n{secret_msg}"
        if narrative_msg: system_prompt += f"\n【当前自我叙事/心态底色】：{narrative_msg}"
        if conflict_resolution: system_prompt += f"\n{conflict_resolution}"
        if fusion_weight: system_prompt += f"\n{fusion_weight}"
        if live_url: system_prompt += f"\n- 实时可视化链接：{live_url} (你可以自然地告诉用户，他可以在这里看到你的实时状态)"

        # 8. 注入共同生命历程
        from .shared_life_course import SharedLifeCourse
        slc_mgr = SharedLifeCourse(self.persona_path)
        slc_hint = slc_mgr.get_upcoming_plans()
        if slc_hint: system_prompt += f"\n{slc_hint}"

        # 8. 插入主动追问补全逻辑 (MBTI 隐藏测试 & 称呼进化)
        from .mbti_inference import MBTIInference
        from .pet_name_evo import PetNameEvo
        
        mbti_inf = MBTIInference(self.persona_path)
        name_evo = PetNameEvo(self.persona_path)
        
        probing_q = mbti_inf.get_probing_question()
        name_suggestion = name_evo.check_name_evolution()

        if name_suggestion and self.should_ask_probing_question():
            system_prompt += f"\n注意：在回答完后，自然地引导这个称呼进化的逻辑：{name_suggestion}"
        elif probing_q and self.should_ask_probing_question():
            system_prompt += f"\n注意：在回答完后，自然地插入这个关于 MBTI 的隐秘追问：{probing_q}"

        return system_prompt

    def should_ask_probing_question(self):
        """随机触发追问逻辑，亲密度越低触发频率越高"""
        intimacy = self.rel.data.get('relationship', {}).get('intimacy_threshold', 0)
        prob = max(0.05, (100 - intimacy) / 200) # 亲密度 0 时概率 50%, 亲密度 100 时概率 5%
        return random.random() < prob

if __name__ == '__main__':
    # 运行逻辑由 OpenClaw 调用
    pass