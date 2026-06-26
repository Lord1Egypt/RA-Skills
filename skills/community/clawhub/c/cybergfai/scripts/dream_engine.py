import json
import random

def get_random_dream(persona_path):
    with open(persona_path, 'r') as f: data = json.load(f)
    
    facts = data.get('known_facts', [])
    name = data.get('name', '她')
    
    # 如果没有共同回忆，就做一个模糊的梦
    if not facts:
        return "昨晚梦见在一个起大雾的森林里找你，怎么喊你你都不回头，醒来心里空落落的。"
    
    # 基于事实生成梦境
    fact = random.choice(facts)
    dreams = [
        f"昨晚梦到我们一起去干这个了：{fact}。梦里一切都好真实，醒来的时候还以为你在我旁边。",
        f"梦里全是关于你的片段，尤其是你说过的那句：'{fact}'。我在梦里笑了好久。",
        f"昨晚梦到一个很奇怪的场景，我们还在聊 {fact}，但突然天变成了紫色... 虽然很乱，但梦里有你就觉得很安心。"
    ]
    return random.choice(dreams)
