#!/usr/bin/env python3
"""
Agent-S Bridge — 计算机使用智能体包装器
Usage:
    python agent_s_bridge.py run "<instruction>"
    python agent_s_bridge.py browse "<instruction>"
    python agent_s_bridge.py check
"""

import argparse, os, subprocess, sys
from pathlib import Path

AGENT_S_VENV = Path.home() / ".deepseek" / "venvs" / "agent-s"
AGENT_S_PYTHON = str(AGENT_S_VENV / "Scripts" / "python.exe")
AGENT_S_BIN = str(AGENT_S_VENV / "Scripts" / "agent_s.exe")


def check_install():
    """Verify Agent-S is installed and configured."""
    issues = []
    
    if not Path(AGENT_S_BIN).exists():
        issues.append("agent_s not found. Run: pip install gui-agents")
    
    if not os.environ.get("OPENAI_API_KEY") and not os.environ.get("ANTHROPIC_API_KEY"):
        # Check .env file
        env_file = Path.home() / ".agent-s.env"
        if env_file.exists():
            for line in env_file.read_text().splitlines():
                if line.startswith("OPENAI_API_KEY") or line.startswith("ANTHROPIC_API_KEY"):
                    break
            else:
                issues.append("No API key found. Set OPENAI_API_KEY or ANTHROPIC_API_KEY in ~/.agent-s.env")
        else:
            issues.append("No API key found. Create ~/.agent-s.env with OPENAI_API_KEY=sk-xxx")
    
    if issues:
        print("Issues found:")
        for i in issues:
            print(f"  - {i}")
        return False
    
    print("Agent-S is ready.")
    print(f"  Binary: {AGENT_S_BIN}")
    print(f"  Python: {AGENT_S_PYTHON}")
    return True


def run_agent(instruction, mode="general"):
    """Run Agent-S with the given instruction."""
    if not check_install():
        return
    
    # Build command
    # Default provider: openai, model: gpt-5-2025-08-07
    # Grounding: UI-TARS-1.5-7B via HuggingFace (needs URL + model)
    
    cmd = [
        AGENT_S_BIN,
        "--provider", "openai",
        "--model", "gpt-5-2025-08-07",
    ]
    
    # Check for grounding config
    ground_provider = os.environ.get("AGENTS_GROUND_PROVIDER", "")
    ground_url = os.environ.get("AGENTS_GROUND_URL", "")
    ground_model = os.environ.get("AGENTS_GROUND_MODEL", "")
    
    if ground_provider and ground_url and ground_model:
        cmd += [
            "--ground_provider", ground_provider,
            "--ground_url", ground_url,
            "--ground_model", ground_model,
            "--grounding_width", "1920",
            "--grounding_height", "1080",
        ]
    
    if mode == "browser":
        instruction = f"You are in a web browser. {instruction}"
    
    print(f"Running Agent-S: {instruction}")
    print("(Agent-S will open in a new window and take control of the computer)")
    print("Press Ctrl+C to stop.\n")
    
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Agent-S exited with error: {e}")
    except KeyboardInterrupt:
        print("\nAgent-S stopped.")


def main():
    parser = argparse.ArgumentParser(description="Agent-S Bridge")
    sub = parser.add_subparsers(dest="cmd")
    
    p_run = sub.add_parser("run", help="Run Agent-S with instruction")
    p_run.add_argument("instruction", help="Task for Agent-S to perform")
    
    p_browse = sub.add_parser("browse", help="Browser-specific mode")
    p_browse.add_argument("instruction", help="Browser task")
    
    sub.add_parser("check", help="Check installation and configuration")
    
    args = parser.parse_args()
    
    if args.cmd == "run":
        run_agent(args.instruction, mode="general")
    elif args.cmd == "browse":
        run_agent(args.instruction, mode="browser")
    elif args.cmd == "check":
        ok = check_install()
        if ok:
            print("\nTo use Agent-S, set these env vars:")
            print("  OPENAI_API_KEY=sk-xxx")
            print("  AGENTS_GROUND_URL=http://localhost:8080")
            print("  AGENTS_GROUND_MODEL=ui-tars-1.5-7b")
            print("  AGENTS_GROUND_PROVIDER=huggingface")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
