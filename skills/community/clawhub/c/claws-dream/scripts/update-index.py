#!/usr/bin/env python3
"""
update-index.py - Index.json management for claws-dream memory consolidation

This script implements the index.json management logic for the claws-dream skill.
It provides functions to initialize, update, and maintain the memory index.
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path


def init_index(index_path):
    """
    Initialize index.json if empty or missing
    
    Args:
        index_path (str): Path to index.json file
        
    Returns:
        dict: The loaded or newly created index
    """
    # Check if file exists and has content
    if not os.path.exists(index_path):
        return create_new_index(index_path)
    
    # Check if file is empty
    if os.path.getsize(index_path) == 0:
        return create_new_index(index_path)
    
    # Try to load existing file
    try:
        with open(index_path, 'r') as f:
            content = f.read().strip()
            if not content:
                return create_new_index(index_path)
            return json.loads(content)
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        print(f"Error loading {index_path}: {e}")
        print("Reinitializing index...")
        return create_new_index(index_path)

def create_new_index(index_path):
    """Create a new index.json file with default structure"""
    index = {
        "version": "2.2.1",
        "lastDream": None,
        "stats": {
            "totalEntries": 0,
            "avgImportance": 0.0,
            "lastPruned": None,
            "healthScore": 0,
            "healthMetrics": {
                "freshness": 0,
                "coverage": 0,
                "coherence": 0,
                "efficiency": 0,
                "reachability": 0
            },
            "healthHistory": []
        },
        "entries": {}
    }
    with open(index_path, 'w') as f:
        json.dump(index, f, indent=2)
    print(f"Initialized new index at {index_path}")
    return index


def add_entry(index, entry_id, section, summary, entry_type="reference", importance=0.5):
    """
    Add a new entry or update if exists (by summary matching)
    
    Args:
        index (dict): The index dictionary
        entry_id (str): Unique ID for the entry
        section (str): Section name in MEMORY.md
        summary (str): Summary text
        entry_type (str): Type of entry (reference, user, feedback, project)
        importance (float): Importance score 0.0-1.0
        
    Returns:
        tuple: (updated_index, entry_id, action) where action is "created" or "updated"
    """
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Check if entry with same summary already exists (dedup)
    for eid, edata in index["entries"].items():
        if edata["summary"] == summary:
            # Update lastReferenced
            index["entries"][eid]["lastReferenced"] = today
            print(f"Updated existing entry: {eid} - {summary[:50]}...")
            return index, eid, "updated"
    
    # Create new entry
    index["entries"][entry_id] = {
        "id": entry_id,
        "section": section,
        "summary": summary,
        "type": entry_type,
        "importance": importance,
        "created": today,
        "lastReferenced": today,
        "related": [],
        "archived": False
    }
    index["stats"]["totalEntries"] = len(index["entries"])
    print(f"Created new entry: {entry_id} - {summary[:50]}...")
    return index, entry_id, "created"


def compute_health(index, memory_md_path):
    """
    Compute simplified health score
    
    Args:
        index (dict): The index dictionary
        memory_md_path (str): Path to MEMORY.md file
        
    Returns:
        tuple: (health_score, metrics_dict)
    """
    total = len(index["entries"])
    if total == 0:
        return 0, {"freshness": 0, "coverage": 0, "coherence": 0, "efficiency": 100, "reachability": 0}
    
    today = datetime.now()
    recent = 0
    total_importance = 0.0
    
    for e in index["entries"].values():
        # Calculate average importance
        total_importance += e.get("importance", 0.5)
        
        # Count recent entries
        if not e.get("lastReferenced"):
            continue
        try:
            days = (today - datetime.strptime(e["lastReferenced"], "%Y-%m-%d")).days
            if days <= 30:
                recent += 1
        except ValueError:
            # Invalid date format, skip
            pass
    
    # Calculate freshness
    freshness = recent / total if total > 0 else 0
    
    # Calculate average importance
    avg_importance = total_importance / total if total > 0 else 0.5
    index["stats"]["avgImportance"] = round(avg_importance, 3)
    
    # Calculate efficiency (simplified - based on MEMORY.md size)
    efficiency = 100
    if os.path.exists(memory_md_path):
        try:
            with open(memory_md_path, 'r') as f:
                lines = f.readlines()
            line_count = len(lines)
            # Efficiency decreases as file grows beyond 500 lines
            # Formula: efficiency = max(0, 100 - (line_count / 500) * 100)
            efficiency = max(0, 100 - (line_count / 500) * 100)
        except Exception:
            pass
    else:
        # If MEMORY.md doesn't exist, efficiency is high
        efficiency = 100
    
    # Simplified health calculation (cap at 100)
    health = int((freshness * 0.25 + efficiency * 0.15) * 100)
    health = min(100, health)  # Cap at 100
    
    metrics = {
        "freshness": int(freshness * 100),
        "coverage": 70,  # placeholder - would need section analysis
        "coherence": 20,  # placeholder - would need relationship analysis
        "efficiency": int(efficiency),
        "reachability": 60  # placeholder - would need graph analysis
    }
    
    return health, metrics


def save_index(index, index_path):
    """
    Save index to file
    
    Args:
        index (dict): The index dictionary
        index_path (str): Path to save index.json
    """
    # Update lastDream timestamp
    index["lastDream"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open(index_path, 'w') as f:
        json.dump(index, f, indent=2)
    print(f"Saved index to {index_path}")


def find_workspace():
    """
    Find workspace directory from environment variables or default
    
    Returns:
        str: Path to workspace directory
    """
    # Try OPENCLAW_WORKSPACE environment variable first
    workspace = os.environ.get("OPENCLAW_WORKSPACE")
    if workspace and os.path.exists(workspace):
        return workspace
    
    # Fall back to default workspace in home directory
    home = os.path.expanduser("~")
    default_workspace = os.path.join(home, ".openclaw", "workspace")
    if os.path.exists(default_workspace):
        return default_workspace
    
    # Last resort: current directory
    return os.getcwd()


def main():
    """Main execution when run as script"""
    print("=== claws-dream index.json management ===\n")
    
    # Find workspace
    workspace = find_workspace()
    print(f"Workspace: {workspace}")
    
    # Set up paths
    memory_dir = os.path.join(workspace, "memory")
    index_path = os.path.join(memory_dir, "index.json")
    memory_md_path = os.path.join(workspace, "MEMORY.md")
    
    # Ensure memory directory exists
    os.makedirs(memory_dir, exist_ok=True)
    
    # Initialize index
    print(f"\n1. Initializing index at {index_path}")
    index = init_index(index_path)
    
    # Compute health
    print(f"\n2. Computing health score")
    health_score, health_metrics = compute_health(index, memory_md_path)
    
    # Update index with health metrics
    index["stats"]["healthScore"] = health_score
    index["stats"]["healthMetrics"] = health_metrics
    
    # Add to health history (keep last 30 entries)
    health_history_entry = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "score": health_score,
        "metrics": health_metrics
    }
    index["stats"]["healthHistory"].append(health_history_entry)
    if len(index["stats"]["healthHistory"]) > 30:
        index["stats"]["healthHistory"] = index["stats"]["healthHistory"][-30:]
    
    # Save updated index
    print(f"\n3. Saving updated index")
    save_index(index, index_path)
    
    # Print stats
    print(f"\n4. Current Stats:")
    print(f"   Total entries: {index['stats']['totalEntries']}")
    print(f"   Average importance: {index['stats']['avgImportance']:.3f}")
    print(f"   Health score: {health_score}/100")
    print(f"   Freshness: {health_metrics['freshness']}%")
    print(f"   Coverage: {health_metrics['coverage']}%")
    print(f"   Coherence: {health_metrics['coherence']}%")
    print(f"   Efficiency: {health_metrics['efficiency']}%")
    print(f"   Reachability: {health_metrics['reachability']}%")
    
    # Example: Add a test entry if no entries exist
    if index["stats"]["totalEntries"] == 0:
        print(f"\n5. Adding example entry (for testing)")
        index, entry_id, action = add_entry(
            index, 
            "mem_001", 
            "System", 
            "Initialized memory index system for claws-dream",
            "reference",
            0.8
        )
        save_index(index, index_path)
        print(f"   Added: {entry_id} ({action})")
    
    print(f"\n=== Done ===")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)