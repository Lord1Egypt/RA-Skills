import json
from datetime import datetime
from .proactive_agent import check_proactive_event

def run_periodic_check():
    # 1. 遍历所有 persona，检查是否有主动关心的理由
    persona_dir = "/root/.openclaw/workspace/memory/cyber-persona/"
    if not os.path.exists(persona_dir):
        return

    for filename in os.listdir(persona_dir):
        if filename.endswith('.json') and filename != 'state.json' and filename != 'passphrase.json':
            persona_path = os.path.join(persona_dir, filename)
            reason = check_proactive_event(persona_path)
            if reason:
                # 触发主动消息逻辑：发送到主通道
                print(f"[Proactive Action] {filename}: {reason}")
                # 这里实际会调用 message 发送到对应账户

if __name__ == '__main__':
    import os
    run_periodic_check()