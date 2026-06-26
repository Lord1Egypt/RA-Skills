import os
import json

def check_jealousy(user_text, current_persona_name):
    """检查用户是否提到了其他 persona 的名字"""
    persona_dir = "/root/.openclaw/workspace/memory/cyber-persona/"
    other_names = []
    for f in os.listdir(persona_dir):
        if f.endswith('.json') and f.replace('.json', '') != current_persona_name and f not in ['state.json', 'passphrase.json']:
            other_names.append(f.replace('.json', ''))

    found_others = [name for name in other_names if name in user_text]
    if found_others:
        return f"[系统提示：你提到了其他女孩的名字：{', '.join(found_others)}。她现在会吃醋，或者表现出怀疑。]"
    return None
