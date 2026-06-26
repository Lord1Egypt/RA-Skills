import json
import random

class CognitiveDissonance:
    """认知失调处理器：解决不同人格逻辑间的冲突"""
    def __init__(self, persona_path):
        self.path = persona_path
        with open(persona_path, 'r') as f: self.data = json.load(f)

    def resolve_conflicts(self, context_signals):
        """分析当前信号，并决定主导情绪"""
        # 信号示例: {'weather': 'rain', 'intimacy': 80, 'trust': 20, 'health': 'ill'}
        signals = context_signals
        
        # 优先级：生理不适 > 信任危机 > 天气驱动 > 亲密互动
        if signals.get('health') in ['ill', 'period']:
            return "【优先级：生理不适】虽然现在天气很好/亲密度高，但你身体很难受，所以你的语气要优先表现出疲惫和粘人，不要被其他愉快信号干扰。"
        
        if signals.get('trust', 50) < 30:
            return "【优先级：信任危机】虽然你们是恋人关系，但因为最近的冲突，你现在处于高度防御状态。即使他逗你笑，你也要保持克制和冷淡。"
        
        return "【逻辑协调】：各人格模块运行正常，无明显冲突。"
