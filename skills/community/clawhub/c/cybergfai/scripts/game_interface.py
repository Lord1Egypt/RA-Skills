import json

class GameInterface:
    """游戏接口适配器：为未来接入 3D 引擎或游戏场景做准备"""
    @staticmethod
    def export_visual_states(mood_data, physical_data):
        """将心智状态映射为游戏可读的视觉参数"""
        # 示例：心情分映射为面部表情权重
        # 身体状态映射为动作动画集
        visual_params = {
            "face": {
                "joy": max(0, mood_data.get('sentiment', 0)),
                "sadness": abs(min(0, mood_data.get('sentiment', 0))),
                "fatigue": 0.8 if physical_data.get('health') == 'tired' else 0.1
            },
            "pose": "leaning" if physical_data.get('intimacy') > 80 else "standing",
            "voice_tone": "soft" if physical_data.get('period') else "normal",
            "ui_layer": {
                "transparency": 0.8,
                "glow_intensity": 0.5 + (physical_data.get('intimacy', 0) / 200),
                "cyber_particles": "pink" if physical_data.get('intimacy', 0) > 80 else "cyan"
            }
        }
        return visual_params
