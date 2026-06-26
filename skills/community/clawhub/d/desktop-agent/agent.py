#!/usr/bin/env python3
"""
Desktop AI Agent CLI
Usage: python agent.py <command> [args]
"""

import sys
import os

# Add parent to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from desktop_agent import get_agent
from desktop_agent.teacher import TaskTeacher
import argparse

def main():
    parser = argparse.ArgumentParser(description="Desktop AI Agent")
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Screenshot
    subparsers.add_parser("screenshot", help="Take a screenshot")
    subparsers.add_parser("capture", help="Capture screen")
    
    # Mouse commands
    subparsers.add_parser("mouse-pos", help="Get mouse position")
    subparsers.add_parser("click", help="Click at position")
    subparsers.add_parser("double-click", help="Double click")
    subparsers.add_parser("right-click", help="Right click")
    
    # Keyboard commands
    subparsers.add_parser("type", help="Type text")
    subparsers.add_parser("press", help="Press key")
    
    # Task commands
    task_parser = subparsers.add_parser("task", help="Task management")
    task_parser.add_argument("action", choices=["list", "run", "show"])
    task_parser.add_argument("name", nargs="?", help="Task name")
    
    # Teach command
    teach_parser = subparsers.add_parser("teach", help="Teach a new task")
    teach_parser.add_argument("action", choices=["start", "add", "show", "save", "cancel"])
    teach_parser.add_argument("args", nargs="*", help="Additional arguments")
    
    args = parser.parse_args()
    
    agent = get_agent()
    teacher = TaskTeacher(agent)
    
    if args.command in ("screenshot", "capture"):
        import time
        filename = f"screen_{int(time.time())}.png"
        agent.capture_to_file(filename)
        print(f"Saved: {filename}")
        
    elif args.command == "mouse-pos":
        pos = agent.get_mouse_position()
        print(f"Mouse position: {pos}")
        
    elif args.command == "click":
        agent.click()
        
    elif args.command == "double-click":
        agent.double_click()
        
    elif args.command == "right-click":
        agent.right_click()
        
    elif args.command == "type":
        text = input("Text to type: ")
        agent.type(text)
        
    elif args.command == "press":
        key = input("Key to press: ")
        agent.press(key)
        
    elif args.command == "task":
        if args.action == "list":
            tasks = agent.list_tasks()
            print("Learned tasks:")
            for t in tasks:
                print(f"  - {t}")
        elif args.action == "run" and args.name:
            print(f"Running task: {args.name}")
            results = agent.execute_task(args.name)
            for r in results:
                print(f"  {r}")
        elif args.action == "show" and args.name:
            task = agent.load_task(args.name)
            print(f"Task: {task['name']}")
            print(f"Steps: {len(task['steps'])}")
            for i, step in enumerate(task['steps'], 1):
                print(f"  {i}. {step}")
                
    elif args.command == "teach":
        if args.action == "start" and args.args:
            teacher.start_teaching(args.args[0])
        elif args.action == "add" and args.args:
            step_type = args.args[0]
            if step_type == "click":
                teacher.record_click()
            elif step_type == "wait":
                teacher.record_wait(float(args.args[1] if len(args.args) > 1 else 1))
        elif args.action == "show":
            teacher.show_steps()
        elif args.action == "save":
            teacher.finish_teaching()
        elif args.action == "cancel":
            teacher.cancel_teaching()
            
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
