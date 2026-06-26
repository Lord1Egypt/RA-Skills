"""
Task Teaching System
Allows users to teach the AI by demonstrating tasks
"""

import json
from pathlib import Path
from datetime import datetime

class TaskTeacher:
    def __init__(self, agent):
        self.agent = agent
        self.current_task = None
        self.current_steps = []
        
    def start_teaching(self, task_name: str):
        """Start teaching a new task."""
        self.current_task = task_name
        self.current_steps = []
        print(f"[TEACH] Started teaching: '{task_name}'")
        print("Recording your actions...")
        
    def record_click(self, x: int = None, y: int = None):
        """Record a click action."""
        if x is None:
            x, y = self.agent.get_mouse_position()
            
        self.current_steps.append({
            "type": "click",
            "x": x,
            "y": y,
            "description": f"Click at ({x}, {y})"
        })
        print(f"  + Recorded click at ({x}, {y})")
        
    def record_type(self, text: str):
        """Record a typing action."""
        self.current_steps.append({
            "type": "type",
            "text": text,
            "description": f"Type: {text}"
        })
        print(f"  + Recorded type: '{text}'")
        
    def record_press(self, *keys):
        """Record a key press."""
        self.current_steps.append({
            "type": "press",
            "keys": list(keys),
            "description": f"Press: {keys}"
        })
        print(f"  + Recorded press: {keys}")
        
    def record_hotkey(self, *keys):
        """Record a hotkey combination."""
        self.current_steps.append({
            "type": "hotkey",
            "keys": list(keys),
            "description": f"Hotkey: {'+'.join(keys)}"
        })
        print(f"  + Recorded hotkey: {'+'.join(keys)}")
        
    def record_wait(self, seconds: float = 1):
        """Record a wait period."""
        self.current_steps.append({
            "type": "wait",
            "seconds": seconds,
            "description": f"Wait {seconds}s"
        })
        print(f"  + Recorded wait: {seconds}s")
        
    def record_screenshot(self, filepath: str):
        """Record taking a screenshot."""
        self.current_steps.append({
            "type": "screenshot",
            "filepath": filepath,
            "description": f"Screenshot: {filepath}"
        })
        print(f"  + Recorded screenshot: {filepath}")
        
    def finish_teaching(self) -> str:
        """Finish teaching and save the task."""
        if not self.current_task:
            print("No task being taught!")
            return None
            
        filepath = self.agent.save_task(self.current_task, self.current_steps)
        
        print(f"\n[DONE] Task '{self.current_task}' saved with {len(self.current_steps)} steps")
        print(f"   Saved to: {filepath}")
        
        self.current_task = None
        self.current_steps = []
        
        return filepath
        
    def cancel_teaching(self):
        """Cancel current teaching session."""
        print(f"[CANCEL] Teaching cancelled: '{self.current_task}'")
        self.current_task = None
        self.current_steps = []
        
    def show_steps(self):
        """Show current teaching steps."""
        if not self.current_steps:
            print("No steps recorded yet.")
            return
            
        print(f"\n[STEPS] Current steps for '{self.current_task}':")
        for i, step in enumerate(self.current_steps, 1):
            print(f"  {i}. {step.get('description')}")
