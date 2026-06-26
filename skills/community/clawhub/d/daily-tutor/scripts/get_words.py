import json
import os
import random
import sys

# Use absolute paths relative to this script
SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_FILE = os.path.join(SKILL_DIR, 'data', 'data.json')
LEARNED_FILE = os.path.join(SKILL_DIR, 'data', 'learned_items.json')
CONFIG_FILE = os.path.join(SKILL_DIR, 'data', 'config.json')

# Legacy fallback paths (backward compatibility)
LEGACY_VOCAB_FILE = os.path.join(SKILL_DIR, 'data', 'vocab.json')
LEGACY_LEARNED_FILE = os.path.join(SKILL_DIR, 'data', 'learned_words.json')

DEFAULT_NUM_ITEMS = 10

def load_config():
    """Load optional config.json, return defaults if not found."""
    defaults = {
        "primary_key": None,  # auto-detect from first key of first item
        "num_items": DEFAULT_NUM_ITEMS,
        "subject_name": None  # auto-generated if not set
    }
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                user_config = json.load(f)
            defaults.update(user_config)
        except Exception as e:
            print(f"Warning: Failed to read config.json ({e}), using defaults.", file=sys.stderr)
    return defaults

def resolve_data_file():
    """Find data file, supporting legacy vocab.json fallback."""
    if os.path.exists(DATA_FILE):
        return DATA_FILE
    if os.path.exists(LEGACY_VOCAB_FILE):
        return LEGACY_VOCAB_FILE
    return None

def resolve_learned_file():
    """Find learned file, supporting legacy learned_words.json fallback."""
    if os.path.exists(LEARNED_FILE):
        return LEARNED_FILE
    if os.path.exists(LEGACY_LEARNED_FILE):
        return LEGACY_LEARNED_FILE
    return LEARNED_FILE  # default to new name for fresh start

def detect_primary_key(data):
    """Auto-detect primary key from the first key of the first item."""
    if data and isinstance(data[0], dict) and data[0]:
        return list(data[0].keys())[0]
    return None

def main():
    config = load_config()

    # Resolve data file path (data.json > vocab.json fallback)
    data_path = resolve_data_file()
    if not data_path:
        print("Error: data.json (or legacy vocab.json) not found. Please create a study data file.")
        return

    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    if not data or not isinstance(data, list):
        print("Error: Data file is empty or invalid format (expected JSON array).")
        return

    # Determine primary key for tracking progress
    primary_key = config.get('primary_key') or detect_primary_key(data)
    if not primary_key:
        print("Error: Cannot determine primary key. Check data file or add config.json with primary_key.")
        return

    num_items = config.get('num_items', DEFAULT_NUM_ITEMS)
    subject_name = config.get('subject_name')

    # Load learned items (with legacy fallback)
    learned_path = resolve_learned_file()
    learned_items = []
    if os.path.exists(learned_path):
        try:
            with open(learned_path, 'r', encoding='utf-8') as f:
                learned_items = json.load(f)
        except:
            pass

    # Filter out items already learned (matching by primary_key)
    learned_keys = set(item.get(primary_key) for item in learned_items)
    available_items = [item for item in data if item.get(primary_key) not in learned_keys]

    if not available_items:
        label = f" ({subject_name})" if subject_name else ""
        print(f"All items completed{label}. Add more data to data.json to continue learning.")
        return

    # Select random items
    samples_count = min(num_items, len(available_items))
    selected_items = random.sample(available_items, samples_count)

    # Append to learned items
    learned_items.extend(selected_items)

    # Save progress (always use new filename)
    with open(LEARNED_FILE, 'w', encoding='utf-8') as f:
        json.dump(learned_items, f, ensure_ascii=False, indent=2)

    # Output header
    header = f"Successfully retrieved {samples_count} new items"
    if subject_name:
        header += f" [{subject_name}]"
    remaining = len(available_items) - samples_count
    print(f"{header} ({remaining} remaining):\n")

    # Output items dynamically — print ALL fields, no hardcoded structure
    for i, item in enumerate(selected_items, 1):
        first = True
        for key, value in item.items():
            if first:
                print(f"{i}. {key}: {value}")
                first = False
            else:
                print(f"   {key}: {value}")
        print("")

if __name__ == '__main__':
    main()
