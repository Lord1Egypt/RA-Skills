#!/usr/bin/env python3
"""design-framework-sender 统一配置读取器

从 ~/.openclaw/openclaw.json 的 design 配置节点读取所有用户相关配置。
用户只需修改 openclaw.json 中的 design 字段即可，无需改动任何其他文件。
"""
import json, os, sys

HOME = os.path.expanduser("~")
CONFIG_PATH = os.path.join(HOME, ".openclaw", "openclaw.json")

def load_design_config():
    cfg = json.load(open(CONFIG_PATH))
    design = cfg.get("design", {})
    return {
        "group_chat_id": design.get("group_chat_id", ""),
        "bot_owner_id":  design.get("bot_owner_id",  ""),
        "output_dir":    os.path.expanduser(design.get("output_dir", "~/.openclaw/workspace/outputs/design-framework")),
        "lock_file":     "/tmp/design-framework-lock",
        "framework_file": "/tmp/design_framework.txt",
        "prompt_file":   "/tmp/image_prompt.txt",
        "preview_file":  "/tmp/preview_message.txt",
        "ref_image":     "/tmp/design-framework-ref-image",
        "timestamp":     "/tmp/design-framework-timestamp",
        "confirmed":     "/tmp/design-framework-confirmed",
        "waiting":       "/tmp/design-framework-waiting",
        "skill_dir":     os.path.join(HOME, ".openclaw", "workspace", "skills", "design-framework-sender"),
        "openclaw_bin":  os.path.join(HOME, ".openclaw", "bin", "openclaw"),
    }

def get(key):
    return load_design_config()[key]

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: config.py <key>")
        sys.exit(1)
    print(load_design_config().get(sys.argv[1], ""))
