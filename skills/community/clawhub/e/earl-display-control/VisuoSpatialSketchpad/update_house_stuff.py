import json
from pathlib import Path
path = Path('earl_mind.json')
mind = json.loads(path.read_text(encoding='utf-8'))
items = mind.get('house_stuff', {}).get('items', [])
items.append({
    "id": "hs_detergent",
    "title": "Buy dishwasher detergent",
    "detail": "Running low—next run will be sad water unless someone grabs a box.",
    "priority": "medium",
    "category": "supplies",
    "icon": "🧼"
})
path.write_text(json.dumps(mind, indent=2, ensure_ascii=False), encoding='utf-8')
