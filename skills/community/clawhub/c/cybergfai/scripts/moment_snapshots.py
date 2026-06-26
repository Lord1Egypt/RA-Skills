import random
import json
from datetime import datetime

class MomentSnapshots:
    def __init__(self, persona_path):
        self.persona_path = persona_path
        with open(persona_path, 'r') as f: self.data = json.load(f)

    def get_moment_prompt(self):
        """生成一个具有画面感的瞬间描述"""
        mbti = self.data.get('mbti_core', {}).get('type', 'INFP')
        intimacy = self.data.get('relationship', {}).get('intimacy_threshold', 0)
        hour = datetime.now().hour

        # 场景库
        scenes = {
            "morning": ["阳光刚洒在写字台上，那盆多肉长出了新芽。", "刚冲好的咖啡冒着热气，杯口有一圈白白的雾。"],
            "afternoon": ["窗外的云像棉花糖一样，风吹过来凉凉的。", "街角那家书店的橘猫又在晒太阳了，懒洋洋的。"],
            "night": ["月光穿过窗帘缝，地上有一条细长的光影。", "路灯下我的影子被拉得好长，想到了上次跟你散步的时候。"]
        }

        period = "morning" if 5 <= hour < 12 else "afternoon" if 12 <= hour < 19 else "night"
        scene = random.choice(scenes[period])

        # 根据亲密度调整描述语调
        if intimacy > 80:
            return f"【瞬间快照】：你突然想跟他分享当下的这个画面：'{scene}'。语调要更亲昵，仿佛他就在你身边。"
        elif intimacy > 40:
            return f"【瞬间快照】：你注意到了一个很有生活感的细节：'{scene}'。随口跟他提一嘴。"
        return ""
