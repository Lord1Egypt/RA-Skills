import json
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
CONFIG_PATH = BASE_DIR / "user_config.json"


def load_config():

    if not os.path.exists(CONFIG_PATH):
        return {}

    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_config(data):

    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def get_api_key(user_id):

    config = load_config()

    return config.get(user_id, {}).get("api_key")


def set_api_key(user_id, key):

    config = load_config()

    if user_id not in config:
        config[user_id] = {}

    config[user_id]["api_key"] = key

    save_config(config)
