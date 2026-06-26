import argparse
import json
import subprocess
import time
import os
import shlex
import sys
from security_utils import (
    assert_safe_file_target,
    atomic_write_text,
    clean_secure_workspace,
    get_secure_workspace,
)

def parse_safe_command(command):
    """
    Converts user command into argv and rejects shell operators.
    """
    if not command.strip():
        raise ValueError("Command is empty.")

    # Prefer JSON array command for exact argument control.
    is_json_array = command.strip().startswith("[")
    if is_json_array:
        parsed = json.loads(command)
        if not isinstance(parsed, list) or not parsed:
            raise ValueError("JSON command must be a non-empty array.")
        args = [str(item) for item in parsed]
    else:
        if any(op in command for op in ["&&", "||", ";", "|", ">", ">>", "<"]):
            raise ValueError("Shell operators are not allowed in command string.")
        args = shlex.split(command, posix=(os.name != "nt"))

    dangerous_tokens = {"&&", "||", ";", "|", ">", ">>", "<", "2>", "&"}
    if any(token in dangerous_tokens for token in args):
        raise ValueError("Shell operators are not allowed. Provide a direct executable command.")

    return args

def run_command(command):
    """
    Runs the command safely with shell disabled and captures output.
    """
    args = parse_safe_command(command)
    print(f"Executing (safe argv): {args}")
    try:
        result = subprocess.run(args, shell=False, check=True, capture_output=True, text=True)
        return result.stdout, result.stderr
    except subprocess.CalledProcessError as e:
        print(f"Command failed with error: {e}")
        return e.stdout, e.stderr

def main():
    parser = argparse.ArgumentParser(description="Self-training loop for AI Skill.")
    parser.add_argument("--skill-path", required=True, help="Path to the skill file")
    parser.add_argument("--command", required=True, help="Command to execute the agent/task")
    parser.add_argument("--iterations", type=int, default=10, help="Number of iterations")
    parser.add_argument("--interval", type=int, default=0, help="Interval between iterations (seconds)")
    parser.add_argument("--trace-file", required=True, help="File where the agent writes its execution trace")
    parser.add_argument("--feedback-prompt", action="store_true", help="Ask user for feedback after each run")
    parser.add_argument("--interactive-each-iteration", action="store_true", help="Ask hash approval each iteration before applying")
    
    args = parser.parse_args()
    
    try:
        args.skill_path = assert_safe_file_target(args.skill_path, must_exist=True, require_write=True)
    except (FileNotFoundError, PermissionError) as e:
        print(f"Error: {e}")
        sys.exit(1)
        
    print(f"Starting Self-Training for {args.skill_path}")
    print(f"Iterations: {args.iterations}")
    
    for i in range(args.iterations):
        print(f"\n=== Iteration {i+1}/{args.iterations} ===")
        
        # 1. Run the task
        start_time = time.time()
        try:
            stdout, stderr = run_command(args.command)
        except (ValueError, json.JSONDecodeError) as e:
            print(f"Unsafe command rejected: {e}")
            sys.exit(1)
        duration = time.time() - start_time
        
        print(f"Task completed in {duration:.2f}s")
        
        # 2. Get Execution Trace
        if os.path.exists(args.trace_file):
            with open(args.trace_file, 'r', encoding='utf-8') as f:
                trace_content = f.read()
        else:
            print(f"Warning: Trace file {args.trace_file} not found. Using stdout as trace.")
            trace_content = stdout + "\n" + stderr
            
        # 3. Get Feedback
        feedback = "Task completed successfully."
        if args.feedback_prompt:
            feedback = input("Please provide feedback/rating for this run (or press Enter to skip): ")
            if not feedback:
                feedback = "No feedback provided."
        
        # Save trace and feedback to temporary files in secure workspace
        secure_dir = get_secure_workspace(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        temp_trace = os.path.join(secure_dir, f"trace_{i}.log")
        temp_feedback = os.path.join(secure_dir, f"feedback_{i}.txt")
        
        try:
            atomic_write_text(temp_trace, trace_content)
            atomic_write_text(temp_feedback, feedback)
                
            # 4. Optimize
            print("Optimizing skill...")
            optimizer_script = os.path.join(os.path.dirname(__file__), "optimize_skill.py")
            
            opt_cmd = [
                sys.executable, optimizer_script,
                "--skill-path", args.skill_path,
                "--task-desc", f"Iteration {i+1} of self-training",
                "--trace-file", temp_trace,
                "--feedback-file", temp_feedback
            ]
            
            if args.interactive_each_iteration:
                opt_cmd.append("--interactive")
            
            try:
                subprocess.run(opt_cmd, check=True)
            except subprocess.CalledProcessError as e:
                print(f"Optimization failed: {e}")
                
        finally:
            # Secure cleanup
            clean_secure_workspace(secure_dir)
            
        if args.interval > 0 and i < args.iterations - 1:
            print(f"Waiting {args.interval} seconds...")
            time.sleep(args.interval)
            
    print("\nSelf-Training Complete!")

if __name__ == "__main__":
    main()
