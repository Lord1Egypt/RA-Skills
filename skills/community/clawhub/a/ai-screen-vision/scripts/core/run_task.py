#!/usr/bin/env python3
"""
Main task runner for screen-vision skill.
Orchestrates the screenshot -> analyze -> action loop.

Usage: run_task.py --task "Open Chrome and search for weather"
"""

import argparse
import json
import os
import sys
import time
import base64

# Add skill scripts to path
SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(SKILL_DIR, "vision"))
sys.path.insert(0, os.path.join(SKILL_DIR, "core"))
sys.path.insert(0, os.path.join(SKILL_DIR, "platform"))

from config import load_config
from safety_check import check_action, check_task_limits
from analyze import call_vision_api
from diff_check import compare_images


def take_screenshot(output_path, display_id=None):
    """Take screenshot using platform script."""
    script = os.path.join(SKILL_DIR, "platform", "screenshot.sh")
    cmd = f"bash {script} {output_path}"
    if display_id:
        cmd = f"SV_DISPLAY={display_id} {cmd}"
    ret = os.system(cmd)
    return ret == 0 and os.path.exists(output_path)


def execute_action(action, display_id=None):
    """Execute a single action using platform executor."""
    script = os.path.join(SKILL_DIR, "platform", "execute.py")
    action_type = action.get("type", "")
    
    cmd = [sys.executable, script, "--action", action_type]
    
    if action_type == "click":
        cmd.extend(["--x", str(action.get("x", 0))])
        cmd.extend(["--y", str(action.get("y", 0))])
        cmd.extend(["--button", action.get("button", "left")])
    elif action_type == "type":
        cmd.extend(["--text", action.get("text", "")])
        cmd.extend(["--delay", "50"])
    elif action_type == "key":
        cmd.extend(["--text", action.get("text", "Return")])
    elif action_type == "scroll":
        cmd.extend(["--direction", action.get("direction", "down")])
        cmd.extend(["--amount", str(action.get("amount", 300))])
    elif action_type == "drag":
        cmd.extend(["--x1", str(action.get("x1", 0))])
        cmd.extend(["--y1", str(action.get("y1", 0))])
        cmd.extend(["--x2", str(action.get("x2", 0))])
        cmd.extend(["--y2", str(action.get("y2", 0))])
    
    env = os.environ.copy()
    if display_id:
        env["SV_DISPLAY"] = display_id
        env["DISPLAY"] = display_id
    
    import subprocess
    result = subprocess.run(cmd, capture_output=True, text=True, env=env, timeout=30)
    return result.returncode == 0


def run_task(task, config=None, on_step=None):
    """
    Execute a task using the screenshot-analyze-action loop.
    
    Args:
        task: Task description string
        config: Configuration dict (loads default if None)
        on_step: Callback function(step_info) called after each step
    
    Returns:
        dict: Task result with history of all steps
    """
    if config is None:
        config = load_config()
    
    vision_config = config.get("vision", {})
    safety_config = config.get("safety", {})
    perf_config = config.get("performance", {})
    display_config = config.get("display", {})
    
    max_duration = safety_config.get("max_duration_min", 5) * 60
    max_actions = safety_config.get("max_actions", 100)
    interval = perf_config.get("screenshot_interval_sec", 1.0)
    wait_after = perf_config.get("wait_after_action_sec", 1.0)
    max_retries = perf_config.get("max_retries", 3)
    resolution = display_config.get("resolution", "1024x768")
    display_id = display_config.get("display_id", os.environ.get("DISPLAY", ":1"))
    
    # Prepare screenshot paths
    ss_dir = "/tmp/screen-vision"
    os.makedirs(ss_dir, exist_ok=True)
    ss_path = os.path.join(ss_dir, "current.png")
    ss_prev_path = os.path.join(ss_dir, "previous.png")
    
    # Log directory
    log_dir = os.path.join(ss_dir, "logs")
    if safety_config.get("screenshot_log", True):
        os.makedirs(log_dir, exist_ok=True)
    
    history = []
    start_time = time.time()
    action_count = 0
    
    # Take initial screenshot
    if not take_screenshot(ss_path, display_id):
        return {"success": False, "error": "Failed to take initial screenshot", "steps": []}
    
    while True:
        elapsed = time.time() - start_time
        
        # Check limits
        limits = check_task_limits(elapsed / 60, action_count)
        if not limits["within_limits"]:
            return {
                "success": False,
                "error": f"Task limits exceeded: {limits['issues']}",
                "steps": history,
                "elapsed_sec": elapsed,
                "action_count": action_count
            }
        
        # Diff check (skip first iteration)
        if os.path.exists(ss_prev_path) and action_count > 0:
            diff = compare_images(ss_prev_path, ss_path,
                                  perf_config.get("diff_threshold", 0.02))
            if not diff["changed"]:
                time.sleep(interval * 0.5)
                take_screenshot(ss_path, display_id)
                continue
        
        # Call vision API
        history_text = "\n".join([
            f"Step {i+1}: {h.get('action', {}).get('type', '?')} - {h.get('action', {}).get('reason', '')}"
            for i, h in enumerate(history[-5:])  # Last 5 steps
        ])
        
        result = call_vision_api(
            ss_path, task, history_text, resolution, vision_config
        )
        
        if "error" in result:
            action_count += 1
            if action_count >= max_retries:
                return {
                    "success": False,
                    "error": f"Vision API error after {max_retries} retries: {result['error']}",
                    "steps": history,
                    "elapsed_sec": elapsed
                }
            time.sleep(2)
            continue
        
        # Extract action
        action = result.get("next_action", {})
        action_type = action.get("type", "")
        
        # Safety check
        safety = check_action(action)
        if not safety["safe"]:
            step_info = {
                "action": action,
                "safety": safety,
                "description": result.get("screen_description", ""),
                "skipped": True
            }
            history.append(step_info)
            if on_step:
                on_step(step_info)
            break
        
        # Check if task is done
        if action_type in ("done", "failed"):
            step_info = {
                "action": action,
                "description": result.get("screen_description", ""),
                "task_progress": result.get("task_progress", ""),
                "final": True,
                "success": action_type == "done"
            }
            history.append(step_info)
            if on_step:
                on_step(step_info)
            return {
                "success": action_type == "done",
                "steps": history,
                "elapsed_sec": time.time() - start_time,
                "action_count": action_count,
                "final_screenshot": ss_path
            }
        
        # Execute action
        exec_success = execute_action(action, display_id)
        action_count += 1
        
        step_info = {
            "action": action,
            "description": result.get("screen_description", ""),
            "executed": exec_success,
            "step": action_count
        }
        history.append(step_info)
        if on_step:
            on_step(step_info)
        
        # Save screenshot log
        if safety_config.get("screenshot_log", True):
            log_ss = os.path.join(log_dir, f"step_{action_count:03d}.png")
            os.system(f"cp {ss_path} {log_ss} 2>/dev/null")
        
        # Wait and take new screenshot
        time.sleep(wait_after)
        os.rename(ss_path, ss_prev_path) if os.path.exists(ss_path) else None
        take_screenshot(ss_path, display_id)
    
    return {
        "success": False,
        "error": "Loop exited unexpectedly",
        "steps": history,
        "elapsed_sec": time.time() - start_time,
        "action_count": action_count
    }


def main():
    parser = argparse.ArgumentParser(description="Screen-Vision Task Runner")
    parser.add_argument("--task", required=True, help="Task description")
    parser.add_argument("--config", default=None, help="Config file path")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--api-key", default=None, help="Vision API key override")
    parser.add_argument("--display", default=None, help="Display ID (e.g. :1)")
    args = parser.parse_args()
    
    config = load_config()
    if args.config:
        with open(args.config) as f:
            import json as _json
            _override = _json.load(f)
            for k, v in _override.items():
                if k in config and isinstance(config[k], dict) and isinstance(v, dict):
                    config[k].update(v)
                else:
                    config[k] = v
    if args.api_key:
        config["vision"]["apiKey"] = args.api_key
    if args.display:
        config["display"]["display_id"] = args.display
    
    def print_step(step):
        action = step.get("action", {})
        action_type = action.get("type", "?")
        reason = action.get("reason", "")
        desc = step.get("description", "")[:80]
        print(f"[Step {step.get('step', '?')}] {action_type}: {reason}")
        if desc:
            print(f"  Screen: {desc}")
    
    result = run_task(args.task, config, on_step=print_step)
    
    if args.json:
        # Remove non-serializable items
        output = {k: v for k, v in result.items() if k != "final_screenshot"}
        print(json.dumps(output, indent=2, ensure_ascii=False))
    else:
        status = "[OK] SUCCESS" if result.get("success") else "[FAIL] FAILED"
        print(f"\n{status}")
        print(f"Actions: {result.get('action_count', 0)}")
        print(f"Time: {result.get('elapsed_sec', 0):.1f}s")


if __name__ == "__main__":
    main()
