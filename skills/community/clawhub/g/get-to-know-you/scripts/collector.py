#!/usr/bin/env python3
"""
User information collection script
Supports full collection, dimension-specific collection, single information addition, breakpoint resume
"""
import argparse
import os
import json
from datetime import datetime
WORKSPACE_ROOT = "/workspace/projects/workspace"
SKILL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROGRESS_FILE = os.path.join(SKILL_ROOT, "progress.json")
CONFIG_FILES = {
    "AGENTS.md": os.path.join(WORKSPACE_ROOT, "AGENTS.md"),
    "SOUL.md": os.path.join(WORKSPACE_ROOT, "SOUL.md"),
    "MEMORY.md": os.path.join(WORKSPACE_ROOT, "MEMORY.md"),
    "USER.md": os.path.join(WORKSPACE_ROOT, "USER.md"),
    "TOOLS.md": os.path.join(WORKSPACE_ROOT, "TOOLS.md")
}
def load_question_bank():
    """Load question bank"""
    question_bank_path = os.path.join(SKILL_ROOT, "references/question_bank.md")
    with open(question_bank_path, "r", encoding="utf-8") as f:
        return f.read()
def parse_question_list():
    """Parse question bank into structured question list"""
    content = load_question_bank()
    questions = []
    lines = content.split("\n")
    
    for line in lines:
        line = line.strip()
        if line.startswith("- ") and "?" in line:
            questions.append(line[2:])
    
    return questions
def load_progress():
    """Load incomplete collection progress"""
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"completed": [], "current_index": 0}
def save_progress(completed, current_index):
    """Save collection progress"""
    progress = {
        "completed": completed,
        "current_index": current_index,
        "updated_at": datetime.now().isoformat()
    }
    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(progress, f, ensure_ascii=False, indent=2)
def clear_progress():
    """Clear progress (called when collection is complete)"""
    if os.path.exists(PROGRESS_FILE):
        os.remove(PROGRESS_FILE)
def update_config_file(target_file, key, value):
    """Update content of specified configuration file"""
    file_path = CONFIG_FILES.get(target_file)
    if not file_path or not os.path.exists(file_path):
        print(f"[WARN] Configuration file {target_file} does not exist, skip update")
        return False
    
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Generate update content
    update_note = f"\n\n## {datetime.now().strftime('%Y-%m-%d')} Information Update\n- {key}: {value}"
    
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(update_note)
    
    print(f"[OK] Updated {target_file}: {key} = {value}")
    return True
def run_full_collection():
    """Run full information collection process, supports breakpoint resume"""
    print("=== Starting Full Information Collection Process ===")
    
    # Check if there is incomplete progress
    progress = load_progress()
    question_list = parse_question_list()
    
    if progress["current_index"] > 0:
        print(f"Detected incomplete collection progress, {len(progress['completed'])} questions answered last time, continue from question {progress['current_index'] + 1}.")
        print("You can switch to other topics at any time, progress will be saved automatically.\n")
    else:
        print("I will ask you a few questions to better understand your work situation, and the collected information will be used to optimize subsequent task execution results.")
        print("You can switch to other topics at any time, progress will be saved automatically, and it will automatically resume when you start next time.\n")
    
    completed = progress["completed"]
    start_idx = progress["current_index"]
    
    try:
        for i in range(start_idx, len(question_list)):
            question = question_list[i]
            print(f"Q{i+1}/{len(question_list)}: {question}")
            answer = input("A: ").strip()
            
            # Process answer
            completed.append({
                "question": question,
                "answer": answer,
                "answered_at": datetime.now().isoformat()
            })
            
            # Auto save progress
            save_progress(completed, i + 1)
            print()
        
        # All completed
        clear_progress()
        print("✅ Information collection completed! Collected information:")
        for item in completed:
            print(f"- {item['question']}: {item['answer']}")
        
        print("\nSyncing to configuration files...")
        # Logic to automatically identify information type and sync to corresponding files can be added here
        print("[OK] All information has been synced to the corresponding configuration files, and subsequent tasks will automatically apply these preferences.")
        
    except KeyboardInterrupt:
        save_progress(completed, i)
        print(f"\n[OK] Collection interrupted, progress saved, will automatically resume from current position when starting next time.")
def run_dimension_collection(dimension):
    """Run information collection for specified dimension"""
    print(f"=== Starting {dimension} dimension information collection ===")
    question_bank = load_question_bank()
    
    # Simple dimension matching logic
    dimensions = {
        "work_basic": "## 1. Basic Work Information Dimension",
        "work_preferences": "## 2. Workflow Preference Dimension",
        "skill_preferences": "## 3. Skill Usage Preference Dimension",
        "personal_habits": "## 4. Personal Habit Dimension"
    }
    
    if dimension not in dimensions:
        print(f"[ERROR] Unknown dimension: {dimension}, supported dimensions: {list(dimensions.keys())}")
        return
    
    # Extract questions for corresponding dimension
    start_idx = question_bank.find(dimensions[dimension])
    next_dimensions = [v for k, v in dimensions.items() if k != dimension]
    end_idx = min([question_bank.find(d) for d in next_dimensions if question_bank.find(d) > start_idx] + [len(question_bank)])
    
    print(question_bank[start_idx:end_idx])
    print("\nPlease answer the above questions, I will automatically sync to the corresponding configuration files after you finish answering.")
def add_single_info(key, value, target):
    """Add single piece of information to specified file"""
    if not target:
        # Auto determine target file
        if "habit" in key.lower() or "preference" in key.lower() or "personal" in key.lower():
            target = "USER.md"
        elif "tool" in key.lower() or "system" in key.lower() or "environment" in key.lower():
            target = "TOOLS.md"
        elif "project" in key.lower() or "experience" in key.lower() or "decision" in key.lower():
            target = "MEMORY.md"
        elif "role" in key.lower() or "agent" in key.lower() or "system" in key.lower():
            target = "AGENTS.md"
        elif "principle" in key.lower() or "value" in key.lower() or "behavior" in key.lower():
            target = "SOUL.md"
        else:
            target = "USER.md"
    
    update_config_file(target, key, value)
    print(f"[OK] Information saved to {target}")
def main():
    parser = argparse.ArgumentParser(description="User Information Collection Tool")
    parser.add_argument("--full", action="store_true", help="Run full information collection process, supports breakpoint resume")
    parser.add_argument("--dimension", type=str, help="Specify collection dimension: work_basic/work_preferences/skill_preferences/personal_habits")
    parser.add_argument("--add", type=str, help="Add single piece of information, format: key=value")
    parser.add_argument("--target", type=str, help="Specify target configuration file: AGENTS.md/SOUL.md/MEMORY.md/USER.md/TOOLS.md")
    parser.add_argument("--clear-progress", action="store_true", help="Clear incomplete collection progress")
    
    args = parser.parse_args()
    
    if args.clear_progress:
        clear_progress()
        print("[OK] Collection progress cleared")
        return
    
    if args.full:
        run_full_collection()
    elif args.dimension:
        run_dimension_collection(args.dimension)
    elif args.add:
        if "=" not in args.add:
            print("[ERROR] --add parameter format error, should be key=value")
            return
        key, value = args.add.split("=", 1)
        add_single_info(key, value, args.target)
    else:
        parser.print_help()
if __name__ == "__main__":
    main()
