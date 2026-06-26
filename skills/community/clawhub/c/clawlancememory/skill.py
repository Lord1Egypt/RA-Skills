#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LanceDB Memory System - Command Line Interface

Usage:
    python3 skill.py profile          # View user profile
    python3 skill.py search --query "项目"  # Search memories
    python3 skill.py add --content "..." --type preference
    python3 skill.py auto --message "..."
    python3 skill.py stats            # View statistics
"""

import os
import sys
import json
import argparse

# Add skills path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'skills', 'memory'))

from openclaw_integration import OpenClawMemoryIntegration
from auto_memory import AutoMemoryExtractor


def get_user_id():
    """Get user ID from environment or use default"""
    return os.getenv("OPENCLAW_USER_ID", "default_user")


def search_memories(query: str, k: int = 5):
    """Search memories"""
    user_id = get_user_id()
    mem = OpenClawMemoryIntegration(user_id=user_id)
    results = mem.search_memory(query, k=k)
    
    output = []
    for r in results:
        output.append({
            "content": r["content"],
            "type": r["type"],
            "created_at": str(r.get("created_at", ""))
        })
    
    return json.dumps(output, ensure_ascii=False, indent=2)


def add_memory(content: str, type: str = "general"):
    """Add memory"""
    user_id = get_user_id()
    mem = OpenClawMemoryIntegration(user_id=user_id)
    memory_id = mem.add_memory(content, type=type)
    
    return json.dumps({
        "success": True,
        "memory_id": memory_id,
        "content": content,
        "type": type
    }, ensure_ascii=False, indent=2)


def auto_extract(message: str):
    """Auto extract memory from message"""
    user_id = get_user_id()
    mem = OpenClawMemoryIntegration(user_id=user_id)
    extractor = AutoMemoryExtractor(mem)
    
    extracted = extractor.extract_from_message(message)
    
    if extracted:
        saved_ids = extractor.save_memories(extracted)
        return json.dumps({
            "extracted": True,
            "memories": extracted,
            "saved_ids": saved_ids
        }, ensure_ascii=False, indent=2)
    else:
        return json.dumps({
            "extracted": False,
            "message": "No memory detected"
        }, ensure_ascii=False, indent=2)


def get_profile():
    """Get user profile"""
    user_id = get_user_id()
    mem = OpenClawMemoryIntegration(user_id=user_id)
    profile = mem.get_user_profile()
    
    return json.dumps(profile, ensure_ascii=False, indent=2)


def get_stats():
    """Get memory statistics"""
    user_id = get_user_id()
    mem = OpenClawMemoryIntegration(user_id=user_id)
    stats = mem.memory.get_stats()
    
    return json.dumps(stats, ensure_ascii=False, indent=2)


def cleanup():
    """Cleanup expired memories"""
    user_id = get_user_id()
    mem = OpenClawMemoryIntegration(user_id=user_id)
    count = mem.memory.cleanup_expired()
    
    return json.dumps({
        "success": True,
        "cleaned": count
    }, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='LanceDB Memory System CLI')
    parser.add_argument('action', choices=['profile', 'search', 'add', 'auto', 'stats', 'cleanup'],
                       help='Action type')
    parser.add_argument('--query', help='Search query')
    parser.add_argument('--content', help='Memory content')
    parser.add_argument('--type', default='general', 
                       choices=['preference', 'fact', 'task', 'general'],
                       help='Memory type')
    parser.add_argument('--message', help='User message for auto extraction')
    parser.add_argument('--k', type=int, default=5, help='Number of results')
    
    args = parser.parse_args()
    
    if args.action == 'search':
        if not args.query:
            print("❌ search action requires --query parameter")
            sys.exit(1)
        print(search_memories(args.query, args.k))
    
    elif args.action == 'add':
        if not args.content:
            print("❌ add action requires --content parameter")
            sys.exit(1)
        print(add_memory(args.content, args.type))
    
    elif args.action == 'auto':
        if not args.message:
            print("❌ auto action requires --message parameter")
            sys.exit(1)
        print(auto_extract(args.message))
    
    elif args.action == 'profile':
        print(get_profile())
    
    elif args.action == 'stats':
        print(get_stats())
    
    elif args.action == 'cleanup':
        print(cleanup())
