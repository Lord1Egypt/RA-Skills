#!/usr/bin/env python3
"""
spawn_planner.py — Task decomposition for agent-spawner skill.

Takes a complex task description and produces a spawn plan with:
- Subtask breakdown
- Dependencies
- Recommended model for each subtask
- Expected output format

Usage:
  python3 spawn_planner.py "task description"
  python3 spawn_planner.py --file plan.md "task description"
"""

import sys
import json
import re
from typing import Optional


def analyze_task(task: str) -> dict:
    """
    Analyze a task description and determine the best spawn pattern.
    
    Returns a structured spawn plan.
    """
    task_lower = task.lower()
    
    # Pattern detection
    has_research = any(w in task_lower for w in ['research', 'find', 'search', 'investigate', 'market'])
    has_compare = any(w in task_lower for w in ['compare', 'versus', 'vs ', 'comparison'])
    has_build = any(w in task_lower for w in ['build', 'create', 'develop', 'implement', 'program'])
    has_test = any(w in task_lower for w in ['test', 'verify', 'validate', 'review'])
    has_doc = any(w in task_lower for w in ['document', 'write', 'guide', 'tutorial', 'manual'])
    has_analyze = any(w in task_lower for w in ['analyze', 'analyze', 'analysis', 'evaluate'])
    has_format = any(w in task_lower for w in ['format', 'csv', 'json', 'html', 'pdf'])
    
    # Count potential parallel agents
    subtasks = []
    dependencies = []
    
    # Detect competitor/comparison tasks
    competitor_count = len(re.findall(r'\b[a-z]+[\d-]*', task))
    competitor_count = min(max(competitor_count - 2, 1), 5)  # 1-5 competitors
    
    if has_build:
        subtasks.append({
            "id": "builder",
            "role": "Builder",
            "description": f"Build the core implementation for: {task}",
            "model": "capable_coding",
            "output_format": "source_files"
        })
        dependencies.append({"from": "builder", "to": None})
    
    if has_test or has_build:
        subtasks.append({
            "id": "tester",
            "role": "Tester",
            "description": "Write comprehensive tests for the implementation",
            "model": "standard",
            "output_format": "test_files"
        })
        if has_build:
            dependencies.append({"from": "tester", "to": "builder"})
    
    if has_doc or has_build:
        subtasks.append({
            "id": "writer",
            "role": "Writer",
            "description": f"Write documentation for: {task}",
            "model": "standard",
            "output_format": "markdown_files"
        })
        if has_build:
            dependencies.append({"from": "writer", "to": "builder"})
    
    if has_research:
        subtasks.append({
            "id": "researcher",
            "role": "Researcher",
            "description": f"Research the topic: {task}",
            "model": "cheapest",
            "output_format": "research_notes"
        })
        dependencies.append({"from": "researcher", "to": None})
    
    if has_compare and not any(s["id"] == "comparator" for s in subtasks):
        subtasks.append({
            "id": "comparator",
            "role": "Comparator",
            "description": f"Create comparison analysis: {task}",
            "model": "standard",
            "output_format": "comparison_table"
        })
        dependencies.append({"from": "comparator", "to": None})
    
    if has_analyze:
        subtasks.append({
            "id": "analyst",
            "role": "Analyst",
            "description": f"Analyze the data/topic: {task}",
            "model": "strong_reasoning",
            "output_format": "analysis_report"
        })
        dependencies.append({"from": "analyst", "to": None})
    
    # Default subtasks if none detected
    if not subtasks:
        subtasks.append({
            "id": "executor",
            "role": "Executor",
            "description": task,
            "model": "standard",
            "output_format": "mixed"
        })
    
    # Detect parallelization opportunity
    parallel_candidates = [s for s in subtasks if s["id"] in ["builder", "researcher", "comparator", "analyst"]]
    can_parallel = len(parallel_candidates) >= 2 and len(dependencies) == 0
    
    # Build spawn plan
    plan = {
        "original_task": task,
        "pattern": detect_pattern(task),
        "can_parallel": can_parallel,
        "subtasks": subtasks,
        "dependencies": dependencies,
        "synthesis_instructions": {
            "step": "After collecting all subtask outputs, synthesize them into a coherent final deliverable. Resolve conflicts, merge overlapping findings, and add context that only the orchestrator possesses.",
            "priority": "quality_over_speed"
        }
    }
    
    return plan


def detect_pattern(task: str) -> str:
    """Detect which spawn pattern best fits the task."""
    task_lower = task.lower()
    
    if any(w in task_lower for w in ['research', 'find', 'search', 'investigate']):
        if any(w in task_lower for w in ['compare', 'versus', 'vs']):
            return "parallel_research_with_comparison"
        return "parallel_research"
    
    if any(w in task_lower for w in ['build', 'create', 'develop', 'implement']):
        if any(w in task_lower for w in ['test', 'document', 'doc']):
            return "build_test_document"
        return "build_parallel"
    
    if any(w in task_lower for w in ['analyze', 'analysis', 'evaluate']):
        return "analyze_summarize_format"
    
    if any(w in task_lower for w in ['review', 'fix', 'verify']):
        return "review_fix_verify"
    
    if any(w in task_lower for w in ['format', 'csv', 'json', 'html']):
        return "multi_format_output"
    
    return "generic"


def main():
    """CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: spawn_planner.py <task description>")
        print("       spawn_planner.py --file <file> <task description>")
        sys.exit(1)
    
    task = " ".join(sys.argv[1:])
    plan = analyze_task(task)
    
    # Output as JSON
    print(json.dumps(plan, indent=2))
    
    # Also output human-readable format
    print("\n" + "=" * 60)
    print(f"TASK: {plan['original_task']}")
    print(f"PATTERN: {plan['pattern']}")
    print(f"PARALLEL: {'Yes' if plan['can_parallel'] else 'No'}")
    print("-" * 60)
    
    for i, sub in enumerate(plan['subtasks'], 1):
        print(f"\n{sub['id'].upper()} (#{i})")
        print(f"  Role: {sub['role']}")
        print(f"  Model: {sub['model']}")
        print(f"  Task: {sub['description']}")
        print(f"  Output: {sub['output_format']}")
    
    if plan['dependencies']:
        print("\nDEPENDENCIES:")
        for dep in plan['dependencies']:
            if dep['from'] and dep['to']:
                print(f"  {dep['from']} → {dep['to']}")
            else:
                print(f"  {dep['from'] or 'All independent'}")
    
    print(f"\n{plan['synthesis_instructions']['step']}")


if __name__ == "__main__":
    main()
