# src/cxm/tools/context_gatherer.py

import subprocess
import os
import json
import glob
import shlex
from pathlib import Path
from typing import Dict, Optional, List, Union
from datetime import datetime


def run_cmd(cmd: Union[str, List[str]], timeout: int = 3) -> Optional[str]:
    """Run command safely without shell=True, return stdout or None"""
    try:
        # If it's a string, we split it safely, but prefer lists
        if isinstance(cmd, str):
            cmd = shlex.split(cmd)
            
        result = subprocess.run(
            cmd, 
            shell=False, 
            capture_output=True, 
            text=True, 
            timeout=timeout,
            stderr=subprocess.DEVNULL
        )
        return result.stdout.strip() if result.returncode == 0 else None
    except Exception:
        return None


def gather_git_context(cwd: Path = None) -> Optional[Dict]:
    """Git repository context"""
    
    if cwd:
        try:
            os.chdir(cwd)
        except Exception:
            return None
    
    if not run_cmd(["git", "rev-parse", "--git-dir"]):
        return None
    
    # We only want git status for the current path ('.')
    # and we limit the lines so it doesn't blow up the prompt.
    git_status = run_cmd(["git", "status", "--short", "."])
    if git_status and len(git_status.splitlines()) > 20:
        lines = git_status.splitlines()
        git_status = "\n".join(lines[:20]) + f"\n... and {len(lines)-20} more files"

    return {
        'repo': Path.cwd().name,
        'branch': run_cmd(["git", "branch", "--show-current"]),
        'remote_url': run_cmd(["git", "config", "--get", "remote.origin.url"]),
        'status': git_status,
        'recent_commits': run_cmd(["git", "log", "--oneline", "-5"]),
        'diff_stats': run_cmd(["git", "diff", "--stat", "."]),
    }


def gather_file_context() -> Dict:
    """Recently edited files and CWD"""
    
    # Using find as a list. We handle the limit in Python to avoid shell pipes.
    find_cmd = [
        "find", ".", "-type", "f", "-mmin", "-60",
        "(", "-name", "*.py", "-o", "-name", "*.js", "-o", "-name", "*.ts", "-o", "-name", "*.md", ")"
    ]
    
    recent_output = run_cmd(find_cmd)
    recent_files = []
    if recent_output:
        recent_files = recent_output.splitlines()[:10]
    
    return {
        'cwd': str(Path.cwd()),
        'recent_edits': recent_files,
    }


def gather_shell_context() -> Dict:
    """Shell history"""
    
    history_file = Path.home() / ".bash_history"
    commands = []
    
    if history_file.exists():
        try:
            with open(history_file, errors='ignore') as f:
                commands = [l.strip() for l in f.readlines()[-10:] if l.strip()]
        except Exception:
            pass
    
    return {
        'last_commands': commands,
        'user': os.getenv('USER', 'unknown'),
        'shell': os.getenv('SHELL', '/bin/bash'),
    }


def gather_system_context() -> Dict:
    """System resources - parsing output in Python instead of awk"""
    
    # Load average
    uptime = run_cmd(["uptime"])
    load = None
    if uptime and "load average:" in uptime:
        load = uptime.split("load average:")[1].strip()

    # Memory
    free = run_cmd(["free", "-h"])
    mem = None
    if free:
        lines = free.splitlines()
        if len(lines) > 1:
            parts = lines[1].split()
            if len(parts) > 6:
                mem = parts[6] # available column

    # Disk
    df = run_cmd(["df", "-h", "."])
    disk = None
    if df:
        lines = df.splitlines()
        if len(lines) > 1:
            parts = lines[1].split()
            if len(parts) > 3:
                disk = parts[3] # Available column

    return {
        'hostname': run_cmd(["hostname"]),
        'load': load,
        'memory_available': mem,
        'disk_available': disk,
    }


def gather_gemini_cli_context() -> Optional[Dict]:
    """Gather the active Gemini CLI session context if available"""
    try:
        from ..config import Config
        config = Config()
        
        # Locate the latest Gemini CLI session file
        chats_dir = Path(config.get('gemini_chats_dir'))
        if not chats_dir.exists():
            return None
            
        session_files = glob.glob(str(chats_dir / "session-*.json"))
        if not session_files:
            return None
            
        # Sort by modification time to get the newest
        latest_file = max(session_files, key=os.path.getmtime)
        
        with open(latest_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        # Extract the last few user messages to understand current context
        messages = data.get('messages', [])
        user_messages = [
            m for m in messages 
            if m.get('type') == 'user'
        ]
        
        # Format the last 2 user messages
        recent_prompts = []
        for msg in user_messages[-2:]:
            content = msg.get('content', [])
            if isinstance(content, list) and len(content) > 0:
                text = content[0].get('text', '')
                if text:
                    # Truncate if very long
                    recent_prompts.append(text[:200] + ('...' if len(text) > 200 else ''))
        
        return {
            'session_id': data.get('sessionId'),
            'last_updated': data.get('lastUpdated'),
            'recent_prompts': recent_prompts
        }
    except Exception as e:
        return {'error': str(e)}

def gather_claudecode_context() -> Optional[Dict]:
    """Gather the Claude Code CLI session context if available"""
    try:
        from ..config import Config
        config = Config()
        
        base_dir = Path(config.get('claudecode_dir'))
        projects_dir = base_dir / "projects"
        if not projects_dir.exists():
            return None
            
        # Claude uses project-specific folders. Try to find one matching current CWD.
        cwd_str = str(Path.cwd()).replace("/", "-")
        # Find project directories that match our current path
        project_folders = [d for d in projects_dir.iterdir() if d.is_dir() and cwd_str in d.name]
        
        if not project_folders:
            # Fallback: look for any very recently modified projects
            project_folders = sorted(
                [d for d in projects_dir.iterdir() if d.is_dir()],
                key=os.path.getmtime,
                reverse=True
            )[:1]
            
        if not project_folders:
            return None
            
        # Get newest session from the chosen project
        target_project = project_folders[0]
        session_files = list(target_project.glob("*.jsonl"))
        if not session_files:
            return None
            
        latest_session = max(session_files, key=os.path.getmtime)
        
        recent_prompts = []
        with open(latest_session, 'r', encoding='utf-8') as f:
            # Read backwards or just last lines since it's JSONL
            lines = f.readlines()
            # In JSONL, we want user messages. 
            # Looking for typical Claude JSON structure in those lines
            for line in reversed(lines):
                try:
                    data = json.loads(line)
                    # Extract user messages (structure might vary slightly depending on version)
                    # Assuming standard message format or similar to what we saw in search
                    if data.get('role') == 'user' or (data.get('type') == 'message' and data.get('role') == 'user'):
                        content = data.get('content', '')
                        if isinstance(content, list):
                            text = "".join([c.get('text', '') for c in content if isinstance(c, dict)])
                        else:
                            text = str(content)
                            
                        if text:
                            recent_prompts.insert(0, text[:200] + ('...' if len(text) > 200 else ''))
                            if len(recent_prompts) >= 2:
                                break
                except:
                    continue
        
        return {
            'project': target_project.name,
            'last_updated': datetime.fromtimestamp(latest_session.stat().st_mtime).isoformat(),
            'recent_prompts': recent_prompts
        }
    except Exception as e:
        return {'error': str(e)}

def gather_all(cwd: Path = None) -> Dict:
    """Gather complete context"""
    
    from datetime import datetime
    
    return {
        'timestamp': datetime.now().isoformat(),
        'git': gather_git_context(cwd),
        'files': gather_file_context(),
        'shell': gather_shell_context(),
        'system': gather_system_context(),
        'gemini_cli': gather_gemini_cli_context(),
        'claudecode': gather_claudecode_context(),
    }

def main():
    """CLI Interface for debugging"""
    context = gather_all()
    print(json.dumps(context, indent=2))

if __name__ == '__main__':
    main()