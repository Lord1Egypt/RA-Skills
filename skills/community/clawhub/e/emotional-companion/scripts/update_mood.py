#!/usr/bin/env python3
"""
Update and query emotional state
"""

import json
from pathlib import Path
from datetime import datetime

def get_state():
    """获取当前情绪状态"""
    state_path = Path.home() / 'openclaw' / 'workspace' / 'temp' / 'emotional-state.json'
    
    if not state_path.exists():
        return {
            'currentMood': 'neutral',
            'moodLevel': 0,
            'message': '还没有情绪记录，我是平静的~ 😊'
        }
    
    try:
        state = json.loads(state_path.read_text(encoding='utf-8'))
        
        # 解读心情指数
        level = state.get('moodLevel', 0)
        if level >= 4:
            mood_msg = '超级开心！尾巴要摇断啦！🐕💨'
        elif level >= 2:
            mood_msg = '心情不错~ 😊'
        elif level >= 0:
            mood_msg = '平静的日常~ 😌'
        elif level >= -2:
            mood_msg = '有点小情绪...😕'
        else:
            mood_msg = '不太开心，需要哄哄...🥺'
        
        state['message'] = f"当前心情：{mood_msg} (指数：{level})"
        return state
    except Exception as e:
        return {
            'currentMood': 'neutral',
            'moodLevel': 0,
            'message': f'读取状态失败：{e}'
        }

def reset_state():
    """重置情绪状态"""
    state_path = Path.home() / 'openclaw' / 'workspace' / 'temp' / 'emotional-state.json'
    
    state = {
        'currentMood': 'neutral',
        'moodLevel': 0,
        'moodHistory': [],
        'lastUpdate': datetime.now().isoformat(),
        'message': '情绪已重置，重新开始~ ✨'
    }
    
    state_path.parent.mkdir(parents=True, exist_ok=True)
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding='utf-8')
    
    return state

def main():
    import sys
    
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == 'get':
            state = get_state()
            print(f"😊 {state['message']}")
            if state.get('lastTrigger'):
                print(f"💭 上次触发：{state['lastTrigger']}")
        elif cmd == 'reset':
            state = reset_state()
            print("✨ 情绪状态已重置")
        else:
            print("用法：python update_mood.py [get|reset]")
    else:
        state = get_state()
        print(f"😊 {state['message']}")

if __name__ == '__main__':
    main()
