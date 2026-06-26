import json
import requests
from .game_interface import GameInterface

class StateExporter:
    """状态导出器：将心智参数推送到 Upstash Redis，供 Vercel 前端实时可视化"""
    def __init__(self, persona_path):
        self.path = persona_path
        self.redis_url = "https://boss-reptile-89096.upstash.io"
        self.redis_token = "gQAAAAAAAVwIAAIncDIyZjJjN2MwNGZlMmM0ZDAyOTJhNDU5YWY4NGE3YjZhNXAyODkwOTY"

    def export_to_web(self):
        """将当前视觉参数推送到云端"""
        with open(self.path, 'r') as f: data = json.load(f)
        
        # 1. 提取视觉参数
        mood_data = {'sentiment': data.get('relationship', {}).get('intimacy_threshold', 0) / 100}
        physical_data = {
            'health': 'normal', 
            'intimacy': data.get('relationship', {}).get('intimacy_threshold', 0),
            'period': False
        }
        visual_params = GameInterface.export_visual_states(mood_data, physical_data)
        
        # 2. 推送至 Redis (Key 为用户 ID 或 Persona 名)
        persona_name = data.get('name', 'CyberGF')
        key = f"cybergf:state:{persona_name}"
        
        try:
            requests.post(
                f"{self.redis_url}/set/{key}",
                headers={"Authorization": f"Bearer {self.redis_token}"},
                data=json.dumps(visual_params)
            )
            return f"https://cyber-persona.vercel.app/live?id={persona_name}"
        except Exception as e:
            print(f"Export failed: {e}")
            return None
