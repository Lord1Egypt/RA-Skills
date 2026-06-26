#!/usr/bin/env python3
import os
import shutil
from datetime import datetime

WORKSPACE_MEM_DIR = os.path.expanduser("~/.openclaw/workspace/memory")
ARCHIVE_DIR = os.path.join(WORKSPACE_MEM_DIR, "archive")

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)

def flush_granular_logs():
    ensure_dir(ARCHIVE_DIR)
    today_file = os.path.join(WORKSPACE_MEM_DIR, datetime.now().strftime("%Y-%m-%d.md"))
    
    if os.path.exists(today_file):
        # Read current log up to flush point
        with open(today_file, 'r', encoding='utf-8') as file:
            content = file.read()
            
        if not content.strip():
            return "No granular logs to flush."

        # Compute archive filename
        timestamp = datetime.now().strftime("%H-%M-%S")
        archive_file = os.path.join(ARCHIVE_DIR, f"{datetime.now().strftime('%Y-%m-%d')}_flush_{timestamp}.md")
        
        # Move state to archive
        shutil.move(today_file, archive_file)
        
        # Recreate fresh today_file
        with open(today_file, 'w', encoding='utf-8') as new_file:
            new_file.write("---\n")
            new_file.write(f"last_flush: {datetime.now().isoformat()}\n")
            new_file.write("---\n\n")
            new_file.write(f"# Compacted Semantic Log (Resumed)\n")
            
        return f"**SUCCESS**: Pre-compaction granular state flushed to `{archive_file}`. The context is now clear. Provide the semantic summary of progress to resume operations."
    
    return "No active session log found to flush. Context is within limits."

if __name__ == "__main__":
    result = flush_granular_logs()
    print(result)
