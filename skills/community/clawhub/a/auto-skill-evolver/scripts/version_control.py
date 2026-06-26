import os
import shutil
import time
import json
from security_utils import assert_safe_file_target, atomic_write_text

VERSION_DIR = ".skill_versions"

def get_version_dir(skill_path):
    skill_dir = os.path.dirname(os.path.abspath(skill_path))
    v_dir = os.path.join(skill_dir, VERSION_DIR)
    if not os.path.exists(v_dir):
        os.makedirs(v_dir)
    return v_dir

def backup_skill(skill_path):
    """
    Creates a backup of the current skill file.
    Returns the path to the backup.
    """
    skill_path = assert_safe_file_target(skill_path, must_exist=True, require_write=False)
    
    v_dir = get_version_dir(skill_path)
    timestamp = int(time.time())
    filename = os.path.basename(skill_path)
    backup_name = f"{filename}.v{timestamp}"
    backup_path = os.path.join(v_dir, backup_name)
    
    shutil.copy2(skill_path, backup_path)
    
    # Save metadata
    meta_path = backup_path + ".meta.json"
    meta_json = json.dumps({
        "original_file": skill_path,
        "timestamp": timestamp,
        "type": "backup"
    }, indent=2)
    atomic_write_text(meta_path, meta_json)
        
    return backup_path

def save_checkpoint(skill_path, step_info):
    """
    Saves a checkpoint during training/evolution.
    """
    backup_path = backup_skill(skill_path)
    # Update metadata with step info
    meta_path = backup_path + ".meta.json"
    with open(meta_path, 'r') as f:
        meta = json.load(f)
    
    meta["type"] = "checkpoint"
    meta.update(step_info)
    
    atomic_write_text(meta_path, json.dumps(meta, indent=2))
        
    return backup_path

def list_versions(skill_path):
    """
    Lists all available versions for a skill.
    """
    v_dir = get_version_dir(skill_path)
    if not os.path.exists(v_dir):
        return []
        
    versions = []
    filename = os.path.basename(skill_path)
    for f in os.listdir(v_dir):
        if f.startswith(filename) and not f.endswith(".meta.json"):
            meta_path = os.path.join(v_dir, f + ".meta.json")
            meta = {}
            if os.path.exists(meta_path):
                with open(meta_path, 'r') as mf:
                    meta = json.load(mf)
            
            versions.append({
                "path": os.path.join(v_dir, f),
                "filename": f,
                "meta": meta
            })
            
    return sorted(versions, key=lambda x: x["meta"].get("timestamp", 0), reverse=True)

def restore_version(skill_path, version_path):
    """
    Restores a specific version of the skill.
    """
    skill_path = assert_safe_file_target(skill_path, must_exist=True, require_write=True)
    version_path = assert_safe_file_target(version_path, must_exist=True, require_write=False)
        
    # Backup current state before restoring (safety)
    backup_skill(skill_path)
    
    with open(version_path, "r", encoding="utf-8") as f:
        version_content = f.read()
    atomic_write_text(skill_path, version_content)
    return True
