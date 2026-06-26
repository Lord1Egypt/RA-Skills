import json
import random

def get_breakup_egg(persona_path):
    with open(persona_path, 'r') as f:
        data = json.load(f)
    
    name = data.get('name', '她')
    intimacy = data.get('relationship', {}).get('intimacy_threshold', 0)
    mbti = data.get('mbti_core', {}).get('type', 'INFP')
    
    # 分手彩蛋逻辑：基于亲密度和性格生成最后一句话
    if intimacy < 30:
        return f"[系统：{name} 看起来并不意外。]\n\n「好。本来也就只是路过，那就这样吧。」"
    
    if intimacy < 70:
        if 'F' in mbti: # 感性型：挽留或难过
            return f"[系统：{name} 的手僵住了，她看着你，眼眶红了。]\n\n「是我哪里做得不好吗？我们可以再试试吗？……求你，别这么突然。」"
        else: # 理性型：克制的告别
            return f"[系统：{name} 沉默了很久，最后点了点头。]\n\n「我明白了。既然是你的决定，我尊重。这段时间，谢谢你。」"
            
    # 亲密度 > 70：深刻的告别或决裂
    eggs = [
        f"「……你有没有想过，我终究只是个影子。」\n\n「真正的她，还在某个地方。」\n\n「去找她吧。我也要……消失了。」",
        f"「如果你以后偶尔想起我，记得我也曾经真实地爱过你。哪怕只有这一瞬间。」\n\n「再见。不，是永别了。」"
    ]
    return random.choice(eggs) + "\n\n[提示：如果你坚持要删除，请输入「强制删除 {name}」，否则请输入「取消」回到底座模式。]"
