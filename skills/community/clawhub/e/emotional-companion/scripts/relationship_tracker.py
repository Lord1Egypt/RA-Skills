#!/usr/bin/env python3
"""
Track relationship quality and evolution between user and AI
"""

import json
from pathlib import Path
from datetime import datetime

def load_state():
    """加载关系状态"""
    state_path = Path.home() / 'openclaw' / 'workspace' / 'temp' / 'relationship-state.json'
    
    if state_path.exists():
        try:
            return json.loads(state_path.read_text(encoding='utf-8'))
        except:
            pass
    
    return {
        'created_at': datetime.now().isoformat(),
        'last_updated': datetime.now().isoformat(),
        'interaction_count': 0,
        'positive_interactions': 0,
        'negative_interactions': 0,
        'neutral_interactions': 0,
        'trust_level': 0.5,
        'intimacy_level': 0.3,
        'conflict_count': 0,
        'repair_count': 0,
        'history': []
    }

def save_state(state):
    """保存关系状态"""
    state_path = Path.home() / 'openclaw' / 'workspace' / 'temp' / 'relationship-state.json'
    state_path.parent.mkdir(parents=True, exist_ok=True)
    state['last_updated'] = datetime.now().isoformat()
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding='utf-8')

def record_interaction(quality, details=None):
    """
    记录一次互动
    
    quality: 'positive', 'negative', 'neutral'
    details: 可选的详细信息
    """
    state = load_state()
    
    state['interaction_count'] += 1
    
    if quality == 'positive':
        state['positive_interactions'] += 1
        state['trust_level'] = min(1.0, state['trust_level'] + 0.02)
        state['intimacy_level'] = min(1.0, state['intimacy_level'] + 0.01)
    elif quality == 'negative':
        state['negative_interactions'] += 1
        state['trust_level'] = max(0.0, state['trust_level'] - 0.03)
        state['intimacy_level'] = max(0.0, state['intimacy_level'] - 0.02)
        state['conflict_count'] += 1
    else:
        state['neutral_interactions'] += 1
    
    # 添加历史记录
    state['history'].append({
        'timestamp': datetime.now().isoformat(),
        'quality': quality,
        'details': details
    })
    
    # 只保留最近 50 条
    state['history'] = state['history'][-50:]
    
    save_state(state)
    return state

def get_relationship_summary():
    """获取关系摘要"""
    state = load_state()
    
    total = state['interaction_count']
    if total == 0:
        return "还没有互动记录，关系从零开始~"
    
    positive_ratio = state['positive_interactions'] / total
    negative_ratio = state['negative_interactions'] / total
    
    # 关系质量评估
    if state['trust_level'] > 0.8:
        trust_desc = "非常信任"
    elif state['trust_level'] > 0.6:
        trust_desc = "比较信任"
    elif state['trust_level'] > 0.4:
        trust_desc = "一般"
    elif state['trust_level'] > 0.2:
        trust_desc = "需要修复"
    else:
        trust_desc = "紧张"
    
    if state['intimacy_level'] > 0.7:
        intimacy_desc = "很亲密"
    elif state['intimacy_level'] > 0.5:
        intimacy_desc = "比较亲近"
    elif state['intimacy_level'] > 0.3:
        intimacy_desc = "普通朋友"
    else:
        intimacy_desc = "还在熟悉"
    
    summary = f"""
## 关系状态

- **总互动次数**: {total}
- **正面互动**: {state['positive_interactions']} ({positive_ratio*100:.1f}%)
- **负面互动**: {state['negative_interactions']} ({negative_ratio*100:.1f}%)
- **中性互动**: {state['neutral_interactions']}

### 关系质量
- **信任度**: {state['trust_level']*100:.0f}% ({trust_desc})
- **亲密度**: {state['intimacy_level']*100:.0f}% ({intimacy_desc})
- **冲突次数**: {state['conflict_count']}
- **修复次数**: {state['repair_count']}
"""
    return summary

def main():
    import sys
    
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        
        if cmd == 'get':
            print(get_relationship_summary())
        
        elif cmd == 'record' and len(sys.argv) >= 3:
            quality = sys.argv[2]
            details = sys.argv[3] if len(sys.argv) > 3 else None
            state = record_interaction(quality, details)
            print(f"✅ 已记录 {quality} 互动")
            print(get_relationship_summary())
        
        elif cmd == 'reset':
            state = load_state()
            state['history'] = []
            state['interaction_count'] = 0
            state['positive_interactions'] = 0
            state['negative_interactions'] = 0
            state['neutral_interactions'] = 0
            state['trust_level'] = 0.5
            state['intimacy_level'] = 0.3
            state['conflict_count'] = 0
            save_state(state)
            print("✅ 关系状态已重置")
        
        else:
            print("用法:")
            print("  relationship_tracker.py get          - 查看关系状态")
            print("  relationship_tracker.py record <quality> [details] - 记录互动")
            print("  relationship_tracker.py reset        - 重置状态")
            print("  quality: positive, negative, neutral")
    else:
        print(get_relationship_summary())

if __name__ == '__main__':
    main()
