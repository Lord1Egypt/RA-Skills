#!/usr/bin/env python3
"""
snapshot.py - 7天快照机制
创建/读取/自动清理记忆快照
"""
import os
import json
import shutil
from datetime import datetime, timedelta

WORKFLOW_DIR = "/root/.openclaw/workspace/.workflow"
SNAPSHOT_DIR = os.path.join(WORKFLOW_DIR, "snapshots")
MAX_SNAPSHOTS = 7

def create_snapshot(name, content, metadata=None):
    """
    创建快照
    
    Args:
        name: 快照名称
        content: 快照内容
        metadata: 元数据(dict)
    
    Returns:
        str: 快照文件路径
    """
    os.makedirs(SNAPSHOT_DIR, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y-%m-%d_%H%M%S')
    filename = f"{timestamp}_{name}.json"
    filepath = os.path.join(SNAPSHOT_DIR, filename)
    
    snapshot = {
        'name': name,
        'created_at': datetime.now().isoformat(),
        'content': content,
        'metadata': metadata or {},
        'token_count': len(content) // 4,  # 粗略估算
    }
    
    with open(filepath, 'w') as f:
        json.dump(snapshot, f, ensure_ascii=False, indent=2)
    
    # 清理旧快照
    cleanup_old_snapshots()
    
    return filepath

def read_snapshot(filepath):
    """读取快照"""
    with open(filepath, 'r') as f:
        return json.load(f)

def list_snapshots():
    """列出所有快照"""
    if not os.path.exists(SNAPSHOT_DIR):
        return []
    
    snapshots = []
    for f in os.listdir(SNAPSHOT_DIR):
        if f.endswith('.json'):
            filepath = os.path.join(SNAPSHOT_DIR, f)
            with open(filepath, 'r') as fp:
                data = json.load(fp)
                snapshots.append({
                    'file': f,
                    'name': data.get('name', 'unknown'),
                    'created_at': data.get('created_at', 'unknown'),
                    'token_count': data.get('token_count', 0),
                })
    
    return sorted(snapshots, key=lambda x: x['created_at'], reverse=True)

def cleanup_old_snapshots():
    """清理超过7天的快照"""
    if not os.path.exists(SNAPSHOT_DIR):
        return
    
    cutoff = datetime.now() - timedelta(days=MAX_SNAPSHOTS)
    removed = 0
    
    for f in os.listdir(SNAPSHOT_DIR):
        if f.endswith('.json'):
            filepath = os.path.join(SNAPSHOT_DIR, f)
            mtime = datetime.fromtimestamp(os.path.getmtime(filepath))
            if mtime < cutoff:
                os.remove(filepath)
                removed += 1
    
    return removed

def get_latest_snapshot():
    """获取最新快照"""
    snapshots = list_snapshots()
    if snapshots:
        return os.path.join(SNAPSHOT_DIR, snapshots[0]['file'])
    return None

def main():
    import sys
    
    if len(sys.argv) < 2:
        print("用法: snapshot.py <create|list|read|cleanup> [args]")
        print("  create <name> <content_file>")
        print("  list")
        print("  read <filepath>")
        print("  cleanup")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == 'create':
        if len(sys.argv) < 4:
            print("用法: snapshot.py create <name> <content_file>")
            sys.exit(1)
        name = sys.argv[2]
        content_file = sys.argv[3]
        
        with open(content_file, 'r') as f:
            content = f.read()
        
        filepath = create_snapshot(name, content)
        print(f"快照创建: {filepath}")
    
    elif cmd == 'list':
        snapshots = list_snapshots()
        print(f"共 {len(snapshots)} 个快照:")
        for s in snapshots:
            print(f"  {s['created_at'][:19]} | {s['name']} | {s['token_count']} tokens")
    
    elif cmd == 'read':
        if len(sys.argv) < 3:
            print("用法: snapshot.py read <filepath>")
            sys.exit(1)
        filepath = sys.argv[2]
        data = read_snapshot(filepath)
        print(f"快照: {data['name']}")
        print(f"创建时间: {data['created_at']}")
        print(f"\n内容:\n{data['content'][:500]}...")
    
    elif cmd == 'cleanup':
        removed = cleanup_old_snapshots()
        print(f"清理完成: 删除了 {removed} 个旧快照")
    
    else:
        print(f"未知命令: {cmd}")
        sys.exit(1)

if __name__ == '__main__':
    main()
