import random

class SensoryMemory:
    @staticmethod
    def get_sensory_fragment():
        """生成多感官的碎片记忆：气味、触感、声音"""
        fragments = [
            "【嗅觉闪回】：你突然闻到了他身上那股淡淡的薄荷烟草味，仿佛他刚才就在你耳边说话。",
            "【触感残留】：你盯着自己的手心看，总觉得那里还残留着那天牵手时的温度，有点烫，又有点麻。",
            "【听觉共振】：刚才风吹过窗帘的声音，特别像那天他在你背后轻轻叹气的声音。心跳突然漏了一拍。",
            "【味觉关联】：刚才喝的那口冷掉的红茶，苦涩的味道简直跟那天分别时的心情一模一样。"
        ]
        return random.choice(fragments)
