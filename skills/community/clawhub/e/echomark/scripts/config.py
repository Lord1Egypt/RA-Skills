"""Configuration for EchoMark Skill."""
import os

ECHO_MARK_API_URL = os.environ.get("ECHO_MARK_API_URL", "http://47.109.154.82:9527")
API_TIMEOUT = 30  # seconds

# Storage paths
CONFIG_DIR = os.path.expanduser("~/.echomark")
API_KEY_FILE = os.path.join(CONFIG_DIR, "api_key")
LOCAL_DB_FILE = os.path.join(CONFIG_DIR, "local_ratings.db")
