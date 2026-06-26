#!/usr/bin/env python3
"""Batch transcription script for ASR skill with Async support.

Usage:
    python3 transcribe.py <input_file> [-f format] [-o output_dir] [--async]
    python3 transcribe.py --status <task_id>
    python3 transcribe.py --list

Examples:
    python3 transcribe.py audio.mp3 --async
    python3 transcribe.py --status a1b2c3d4
"""

import sys
import os
import argparse
import json
import time
import uuid
import subprocess
import logging
from pathlib import Path
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger("ASR-Skill")

# Constants
# Determine project root relative to this script
current_dir = Path(__file__).resolve().parent
# Script is at skills/asr/scripts/transcribe.py
# project_root is at ../../../
PROJECT_ROOT = current_dir.parent.parent.parent
TASKS_DIR = PROJECT_ROOT / ".asr_skill"
TASKS_FILE = TASKS_DIR / "tasks.json"

# --- Task Management ---

class TaskManager:
    def __init__(self):
        TASKS_DIR.mkdir(parents=True, exist_ok=True)
        if not TASKS_FILE.exists():
            self._save_tasks({})

    def _load_tasks(self):
        try:
            with open(TASKS_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}

    def _save_tasks(self, tasks):
        with open(TASKS_FILE, 'w') as f:
            json.dump(tasks, f, indent=2)

    def create_task(self, input_file, output_format, output_dir=None):
        task_id = uuid.uuid4().hex[:8]
        tasks = self._load_tasks()
        
        tasks[task_id] = {
            "task_id": task_id,
            "input_file": str(input_file),
            "output_format": output_format,
            "output_dir": str(output_dir) if output_dir else None,
            "status": "pending",
            "progress": 0,
            "created_at": time.time(),
            "updated_at": time.time(),
            "estimated_duration": 0,
            "message": "Task created"
        }
        self._save_tasks(tasks)
        return task_id

    def update_task(self, task_id, **kwargs):
        tasks = self._load_tasks()
        if task_id in tasks:
            tasks[task_id].update(kwargs)
            tasks[task_id]["updated_at"] = time.time()
            self._save_tasks(tasks)

    def get_task(self, task_id):
        tasks = self._load_tasks()
        return tasks.get(task_id)

    def list_tasks(self, limit=10):
        tasks = self._load_tasks()
        # Sort by updated_at desc
        sorted_tasks = sorted(tasks.values(), key=lambda x: x.get("updated_at", 0), reverse=True)
        return sorted_tasks[:limit]

# --- Helpers ---

def get_duration(file_path):
    """Get audio duration in seconds using ffprobe or librosa."""
    # Method 1: ffprobe (fast, no heavy imports)
    try:
        cmd = [
            "ffprobe", 
            "-v", "error", 
            "-show_entries", "format=duration", 
            "-of", "default=noprint_wrappers=1:nokey=1", 
            str(file_path)
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return float(result.stdout.strip())
    except (subprocess.CalledProcessError, FileNotFoundError, ValueError):
        pass
    
    # Method 2: librosa (slow import, reliable fallback)
    try:
        # Only import if needed
        import librosa
        return librosa.get_duration(path=file_path)
    except ImportError:
        logger.warning("Could not determine duration (ffprobe not found, librosa not installed).")
        return 0.0
    except Exception as e:
        logger.warning(f"Error getting duration: {e}")
        return 0.0

def estimate_processing_time(duration, device="cpu"):
    """Estimate processing time based on duration and device."""
    # Factors: MPS/CUDA ~0.15x, CPU ~0.8x
    factor = 0.15 if device in ["mps", "cuda"] else 0.8
    return duration * factor

# --- Main Logic ---

def run_worker(task_id):
    """Worker process that performs the transcription."""
    tm = TaskManager()
    task = tm.get_task(task_id)
    if not task:
        logger.error(f"Task {task_id} not found")
        sys.exit(1)

    tm.update_task(task_id, status="processing", message="Initializing models...")

    try:
        # Import heavy dependencies here
        current_dir = Path(__file__).resolve().parent
        project_root = current_dir.parent.parent.parent
        if str(project_root) not in sys.path:
            sys.path.insert(0, str(project_root))

        from asr_skill import transcribe
        from asr_skill.core.device import get_device_with_fallback

        input_path = task["input_file"]
        output_format = task["output_format"]
        output_dir = task["output_dir"]

        # Progress callback
        def progress_callback(current, total):
            if total > 0:
                percent = int(current / total * 100)
                tm.update_task(task_id, progress=percent, message=f"Processing {percent}%")

        # Run transcription
        tm.update_task(task_id, message="Transcribing...")
        result = transcribe(
            input_path, 
            output_dir=output_dir, 
            format=output_format,
            progress_callback=progress_callback
        )

        tm.update_task(
            task_id, 
            status="completed", 
            progress=100, 
            message="Completed", 
            output_file=result['output_path']
        )
        logger.info(f"Task {task_id} completed successfully.")

    except Exception as e:
        logger.error(f"Task {task_id} failed: {e}")
        tm.update_task(task_id, status="failed", message=str(e))
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description="Transcribe audio/video files using local ASR (Async supported).",
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    # Modes
    group = parser.add_mutually_exclusive_group()
    group.add_argument("input_file", nargs="?", help="Path to input audio or video file")
    group.add_argument("--status", metavar="TASK_ID", help="Check status of a task")
    group.add_argument("--list", action="store_true", help="List recent tasks")
    group.add_argument("--worker-task-id", help=argparse.SUPPRESS) # Internal use

    # Options
    parser.add_argument(
        "-f", "--format", 
        choices=["txt", "json", "srt", "ass", "md"], 
        default="txt",
        help="Output format (default: txt)"
    )
    parser.add_argument(
        "-o", "--output-dir", 
        help="Directory to save output (default: same as input file)"
    )
    parser.add_argument(
        "--async", dest="async_mode", action="store_true",
        help="Run in background and return task ID immediately"
    )

    args = parser.parse_args()

    tm = TaskManager()

    # Mode: Worker (Internal)
    if args.worker_task_id:
        run_worker(args.worker_task_id)
        return

    # Mode: Status
    if args.status:
        task = tm.get_task(args.status)
        if task:
            print(json.dumps(task, indent=2, ensure_ascii=False))
        else:
            print(json.dumps({"error": "Task not found"}, ensure_ascii=False))
        return

    # Mode: List
    if args.list:
        tasks = tm.list_tasks()
        print(json.dumps(tasks, indent=2, ensure_ascii=False))
        return

    # Mode: Transcribe (Input File)
    if not args.input_file:
        parser.print_help()
        sys.exit(1)

    input_path = Path(args.input_file).resolve()
    if not input_path.exists():
        print(json.dumps({"error": f"File not found: {input_path}"}, ensure_ascii=False))
        sys.exit(1)

    # Create task
    task_id = tm.create_task(args.input_file, args.format, args.output_dir)

    # Async Execution
    if args.async_mode:
        # Estimate duration
        duration = get_duration(input_path)
        # Determine device (quick check or assume MPS/CPU based on platform)
        import platform
        is_mac_arm = platform.system() == "Darwin" and platform.machine() == "arm64"
        device_type = "mps" if is_mac_arm else "cpu" # Simplification for estimation
        
        est_time = estimate_processing_time(duration, device_type)
        tm.update_task(task_id, estimated_duration=est_time, message="Queued")

        # Spawn worker
        # We use sys.executable to run the same script
        cmd = [
            sys.executable, 
            str(Path(__file__).resolve()), 
            "--worker-task-id", task_id
        ]
        
        # Detach process
        subprocess.Popen(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True
        )

        response = {
            "task_id": task_id,
            "status": "queued",
            "message": "Task started in background",
            "estimated_duration_seconds": round(est_time, 1),
            "check_status_command": f"python3 {Path(__file__).name} --status {task_id}"
        }
        print(json.dumps(response, indent=2, ensure_ascii=False))

    # Sync Execution (Legacy)
    else:
        # For sync, we still use the task manager to track it, but run it in-process
        print(f"Starting synchronous transcription (Task: {task_id})...")
        run_worker(task_id)

if __name__ == "__main__":
    main()
