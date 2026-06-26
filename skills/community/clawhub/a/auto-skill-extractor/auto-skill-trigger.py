#!/usr/bin/env python3
"""
Auto-Skill Trigger System v1.0.1
Called after subagent completion to determine if skill extraction is needed.

SECURITY NOTES:
- Transcript content is NOT persisted to disk (only tool counts/scores)
- Workspace path is configurable via AUTO_SKILL_WORKSPACE env var
- All paths are validated before file operations
"""

import sys
import json
import hashlib
import re
import os
from datetime import datetime
from pathlib import Path

# Get workspace from ENV or use relative path (security: no hardcoded absolute paths)
WORKSPACE = Path(os.environ.get("AUTO_SKILL_WORKSPACE", ".")).resolve()
AUTO_DIR = WORKSPACE / "skills" / "auto"
DRAFT_DIR = WORKSPACE / "skills" / "auto-draft"
QUEUE_FILE = WORKSPACE / "scripts" / "skill-extraction-queue.json"
MAX_QUEUE_SIZE = 50

def sanitize_skill_name(name: str) -> str:
    """Prevent path traversal and invalid chars."""
    # Remove any path components
    name = os.path.basename(name)
    # Allow only alphanumeric, hyphen, underscore
    name = re.sub(r'[^a-zA-Z0-9_-]', '-', name)
    # Limit length
    return name[:64]

def validate_workspace():
    """Ensure workspace directory exists and is safe to write to."""
    if not WORKSPACE.exists():
        raise RuntimeError(f"Workspace does not exist: {WORKSPACE}")
    
    # Check if workspace is writable
    test_file = WORKSPACE / ".write_test"
    try:
        test_file.touch()
        test_file.unlink()
    except PermissionError:
        raise RuntimeError(f"Workspace not writable: {WORKSPACE}")

def skill_exists(skill_name: str) -> bool:
    """Check if skill already in auto/ or auto-draft/."""
    return (AUTO_DIR / skill_name).exists() or \
           (DRAFT_DIR / skill_name).exists()

def drain_queue() -> list:
    """Read and clear queue atomically."""
    if not QUEUE_FILE.exists():
        return []
    try:
        queue = json.loads(QUEUE_FILE.read_text())
        # Atomic clear
        QUEUE_FILE.write_text("[]")
        return queue
    except:
        return []

def process_queue():
    """Process all queued extractions by creating DRAFT skills."""
    entries = drain_queue()
    processed = []
    failed = []
    
    for entry in entries:
        if entry.get("action") in ["extract", "manual_extract"]:
            skill_name = entry.get("skill_name")
            session_id = entry.get("session_id")
            
            print(f"Creating DRAFT skill: {skill_name}")
            
            # Create DRAFT directory
            draft_dir = DRAFT_DIR / skill_name
            try:
                draft_dir.mkdir(parents=True, exist_ok=False)
                
                # Create initial SKILL.md (NO TRANSCRIPT CONTENT for security)
                skill_content = f"""# {skill_name.replace('-', ' ').title()}

**Auto-extracted skill (DRAFT)**
- Tool calls: {entry.get('tool_calls', 0)}
- Complexity: {entry.get('complexity_score', 0)}/10
- Extracted: {entry.get('timestamp', datetime.now().isoformat())}

## Purpose

[Describe what this skill does - to be filled manually or by skill-extractor subagent]

## When to Use

- [Add conditions]

## Procedure

1. [Step 1]
2. [Step 2]

## Verification

- [ ] [Check 1]

## Notes

This skill was auto-extracted. It needs 3 successful re-invocations before promotion to ACTIVE.
Status: DRAFT (under evaluation)
"""
                (draft_dir / "SKILL.md").write_text(skill_content)
                
                # Create meta.json (sanitized - no raw transcript)
                meta = {
                    "created": datetime.now().isoformat(),
                    "tool_calls": entry.get("tool_calls", 0),
                    "complexity": entry.get("complexity_score", 0),
                    "invocation_count": 0,
                    "status": "DRAFT",
                    "skill_name": skill_name,
                    "source_session_hash": hashlib.sha256(
                        entry.get("session_id", "").encode()
                    ).hexdigest()[:16]  # Hash only, not raw session ID
                }
                (draft_dir / "meta.json").write_text(json.dumps(meta, indent=2))
                
                processed.append(skill_name)
                print(f"✅ Created DRAFT: {skill_name}")
                
            except FileExistsError:
                print(f"⚠️  DRAFT already exists: {skill_name}")
                failed.append(skill_name)
            except Exception as e:
                print(f"❌ Failed to create DRAFT {skill_name}: {e}")
                failed.append(skill_name)
    
    return {"processed": len(processed), "skills": processed, "failed": failed}

COMPLEXITY_THRESHOLD = 4

def calculate_complexity(tool_calls: int, has_error_recovery: bool = False, multi_domain: bool = False) -> int:
    """Calculate task complexity score (0-10)."""
    score = min(10, int(tool_calls * 0.7))
    if has_error_recovery:
        score += 2
    if multi_domain:
        score += 2
    return min(10, score)

def should_extract_skill(completion_status: str, tool_calls: int, complexity: int) -> dict:
    """
    Determine if subagent transcript qualifies for skill extraction.
    
    Returns:
        dict with keys: should_extract (bool), reason (str), skill_name (str)
    """
    result = {"should_extract": False, "reason": "", "skill_name": ""}
    
    # Must be successful
    if completion_status != "success":
        result["reason"] = f"Completion status is '{completion_status}', not 'success'"
        return result
    
    # Must have minimum tool calls
    if tool_calls < 3:
        result["reason"] = f"Only {tool_calls} tool calls (minimum 3)"
        return result
    
    # Must meet complexity threshold
    if complexity < COMPLEXITY_THRESHOLD:
        result["reason"] = f"Complexity score {complexity} below threshold ({COMPLEXITY_THRESHOLD})"
        return result
    
    result["should_extract"] = True
    result["reason"] = f"Qualifies: {tool_calls} tools, complexity {complexity}"
    return result

def generate_skill_name(transcript_summary: str) -> str:
    """Generate a skill name from transcript summary."""
    # Extract key action words
    words = transcript_summary.lower().split()
    # Filter to meaningful words (skip common stop words)
    stop_words = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by"}
    key_words = [w for w in words if w not in stop_words and len(w) > 2]
    
    if len(key_words) >= 2:
        name = f"{key_words[0]}-{key_words[-1]}"
    else:
        name = "-".join(key_words[:2]) if key_words else "unknown-skill"
    
    # Add hash to ensure uniqueness
    hash_str = hashlib.md5(name.encode()).hexdigest()[:6]
    return f"{name}-{hash_str}"

def main():
    """
    Called from main agent after subagent completion.
    
    Usage:
        python3 auto-skill-trigger.py                    # reads from stdin
        python3 auto-skill-trigger.py /path/to/input.json # reads from file
    
    Expected JSON input:
    {
        "completion_status": "success" | "failed" | "timeout",
        "tool_calls": int,
        "session_id": "...",
        "transcript_summary": "...",
        "tags": ["tag1", "tag2"]
    }
    
    Environment:
        AUTO_SKILL_WORKSPACE - Path to workspace (default: current directory)
    """
    try:
        # Validate workspace before anything else
        validate_workspace()
        
        # Ensure directories exist
        DRAFT_DIR.mkdir(parents=True, exist_ok=True)
        AUTO_DIR.mkdir(parents=True, exist_ok=True)
        (WORKSPACE / "scripts").mkdir(parents=True, exist_ok=True)
        
        # Support both stdin and file input for OpenClaw security compatibility
        if len(sys.argv) > 1 and sys.argv[1].endswith('.json'):
            with open(sys.argv[1], 'r') as f:
                data = json.load(f)
        else:
            data = json.load(sys.stdin)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(json.dumps({"error": f"Invalid input: {e}"}))
        sys.exit(1)
    except RuntimeError as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)
    
    completion_status = data.get("completion_status", "")
    tool_calls = data.get("tool_calls", 0)
    session_id = data.get("session_id", "")
    transcript_summary = data.get("transcript_summary", "")
    manual_trigger = data.get("manual_trigger", False)
    
    # Calculate complexity
    complexity = calculate_complexity(
        tool_calls,
        has_error_recovery=data.get("has_error_recovery", False),
        multi_domain=data.get("multi_domain", False)
    )
    
    # Determine if extraction needed
    qualification = should_extract_skill(completion_status, tool_calls, complexity)
    
    if not qualification["should_extract"] and not manual_trigger:
        print(json.dumps({
            "action": "skip",
            "reason": qualification["reason"]
        }))
        return
    
    # Generate skill name (sanitized)
    skill_name = sanitize_skill_name(
        data.get("skill_name") or generate_skill_name(transcript_summary)
    )
    
    # Check for existing skill
    if skill_exists(skill_name) and not manual_trigger:
        output = {
            "action": "skip",
            "reason": f"Skill '{skill_name}' already exists"
        }
        print(json.dumps(output))
        return
    
    # Create output (no transcript content included)
    output = {
        "action": "extract" if qualification["should_extract"] else "manual_extract",
        "skill_name": skill_name,
        "session_id": hashlib.sha256(session_id.encode()).hexdigest()[:16],  # Hash only
        "tool_calls": tool_calls,
        "complexity_score": complexity,
        "timestamp": datetime.now().isoformat(),
        "trigger_reason": qualification["reason"] if qualification["should_extract"] else "manual"
    }
    
    print(json.dumps(output))
    
    # Write to queue
    queue = []
    if QUEUE_FILE.exists():
        try:
            queue = json.loads(QUEUE_FILE.read_text())
        except:
            queue = []
    
    queue.append(output)
    QUEUE_FILE.write_text(json.dumps(queue, indent=2))
    
    # Process queue
    process_queue()

if __name__ == "__main__":
    main()
