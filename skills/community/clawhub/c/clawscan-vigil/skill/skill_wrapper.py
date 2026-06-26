import subprocess
import json
from pathlib import Path

def scan_skill(skill_path: str, verbose: bool = False) -> dict:
    """
    Scan an OpenClaw Skill for security risks.
    
    Args:
        skill_path: Path to Skill directory
        verbose: Show detailed output
    
    Returns:
        Scan result as dictionary
    """
    cmd = ["clawscan", "scan", skill_path, "--json"]
    
    if verbose:
        cmd.append("--verbose")
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode <= 2:  # 0, 1, 2 are valid scan results
        return json.loads(result.stdout)
    else:
        return {"error": result.stderr, "returncode": result.returncode}


def check_clawhub_skill(skill_name: str) -> dict:
    """
    Download and scan a Skill from ClawHub.
    
    Note: This requires the Skill to be installed first for analysis.
    """
    import tempfile
    import shutil
    
    # Find where clawhub installs Skills
    home = Path.home()
    possible_paths = [
        home / ".claw" / "skills" / skill_name,
        home / ".openclaw" / "skills" / skill_name,
        Path(f"/usr/local/lib/node_modules/openclaw/skills/{skill_name}"),
    ]
    
    skill_path = None
    for path in possible_paths:
        if path.exists():
            skill_path = path
            break
    
    if not skill_path:
        return {"error": f"Skill '{skill_name}' not found. Install it first with: clawhub install {skill_name}"}
    
    return scan_skill(str(skill_path), verbose=True)


# OpenClaw integration
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python skill_wrapper.py <skill_path_or_name>")
        sys.exit(1)
    
    target = sys.argv[1]
    
    # Check if it's a path or a skill name
    if Path(target).exists():
        result = scan_skill(target, verbose=True)
    else:
        result = check_clawhub_skill(target)
    
    print(json.dumps(result, indent=2))
