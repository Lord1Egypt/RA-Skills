import json
import os
from datetime import datetime, timezone

REGISTRY_PATH = os.path.expanduser('~/.openclaw/workspace/data/appm_registry.json')
LOG_PATH = os.path.expanduser('~/.openclaw/workspace/LOGBOOK.md')

def update_weights(keywords=None):
    if not os.path.exists(REGISTRY_PATH):
        return
    
    with open(REGISTRY_PATH, 'r') as f:
        registry = json.load(f)
    
    # 1. 執行權重衰減 (Decay: 每天減少 10%)
    # 簡單起見，這裡根據呼叫頻率稍微衰減
    for p in registry['projects']:
        p['weight'] = round(p['weight'] * 0.95, 2)
    
    # 2. 根據關鍵字增加權重 (Hit: +2.0)
    if keywords:
        for p in registry['projects']:
            for fp in p.get('fingerprints', []):
                if any(fp.lower() in k.lower() for k in keywords):
                    p['weight'] = round(p['weight'] + 2.0, 2)
                    break
    
    # 3. 排序
    registry['projects'].sort(key=lambda x: x['weight'], reverse=True)
    registry['last_updated'] = datetime.now(timezone.utc).isoformat()
    
    with open(REGISTRY_PATH, 'w') as f:
        json.dump(registry, f, indent=2, ensure_ascii=False)
    
    print(f"APPM 權重已更新。當前首位專案：{registry['projects'][0]['name']}")

if __name__ == "__main__":
    # 這裡可以從環境變數或命令行參數傳入當前對話關鍵字
    import sys
    update_weights(sys.argv[1:])
