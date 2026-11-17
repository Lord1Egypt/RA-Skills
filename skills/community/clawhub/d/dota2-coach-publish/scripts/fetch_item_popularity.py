#!/usr/bin/env python3
"""
抓取每个英雄的装备选择率数据
保存至 item_popularity.json
"""
import json, time, subprocess, os, sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ITEMS_FILE = f'{SCRIPT_DIR}/items_db.json'
HEROES_FILE = f'{SCRIPT_DIR}/heroes_db.json'
OUTPUT_FILE = f'{SCRIPT_DIR}/item_popularity.json'

def load_heroes():
    with open(HEROES_FILE) as f:
        return json.load(f)

def load_items():
    with open(ITEMS_FILE) as f:
        items = json.load(f)
    return {item['id']: item for item in items}

def fetch_item_popularity(hero_id):
    url = f'https://api.opendota.com/api/heroes/{hero_id}/itemPopularity'
    try:
        result = subprocess.run(
            ['curl', '-sL', url, '-H', 'User-Agent: Mozilla/5.0', '--max-time', '15'],
            capture_output=True, text=True, timeout=20
        )
        if result.returncode == 0 and result.stdout.strip():
            return json.loads(result.stdout)
    except Exception as e:
        print(f'  [ERROR] Hero {hero_id}: {e}', file=sys.stderr)
    return None

def main():
    heroes = load_heroes()
    id_to_item = load_items()

    # Load existing
    existing = {}
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE) as f:
            existing = json.load(f)
    done_ids = set(existing.keys())
    print(f'Already have: {len(done_ids)} heroes')

    fetched = 0
    errors = 0

    for h in heroes:
        hero_id = h['id']
        hero_name = h.get('localized_name', h['name'])

        if str(hero_id) in done_ids:
            continue

        print(f'Fetching {hero_name} (ID:{hero_id})...', end=' ', flush=True)
        data = fetch_item_popularity(hero_id)

        if data is not None:
            # Convert item IDs to names/localized_names
            phases = ['start_game_items', 'early_game_items', 'mid_game_items', 'late_game_items']
            simplified = {}
            for phase in phases:
                items_raw = data.get(phase, {})
                if items_raw:
                    simplified[phase] = {}
                    for item_id, count in items_raw.items():
                        try:
                            item_id_int = int(item_id)
                            item_info = id_to_item.get(item_id_int, {})
                            item_name = item_info.get('localized_name') or item_info.get('name', f'item_{item_id}')
                            simplified[phase][item_name] = count
                        except (ValueError, TypeError):
                            pass

            existing[str(hero_id)] = {
                'hero_name': hero_name,
                'hero_key': h.get('key', ''),
                'phases': simplified
            }
            fetched += 1
            print(f'OK ({len(simplified)} phases)')
        else:
            errors += 1
            print(f'FAILED')

        # Save incrementally
        with open(OUTPUT_FILE, 'w') as f:
            json.dump(existing, f, ensure_ascii=False, indent=2)

        # Delay to avoid 403
        time.sleep(2.5)

    print(f'\nDone. Fetched: {fetched}, Errors: {errors}, Total: {len(existing)}')

if __name__ == '__main__':
    main()
