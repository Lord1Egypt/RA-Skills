#!/usr/bin/env python3
"""Environment Detector - Identifies if running in OpenClaw or standalone Claude."""
import os
import sys
import subprocess
from pathlib import Path
from enum import Enum

class Environment(Enum):
    OPENCLAW = "openclaw"
    CLAUDE_DESKTOP = "claude_desktop"
    CLAUDE_API = "claude_api"
    STANDALONE = "standalone"

class EnvironmentDetector:
    """Detects the runtime environment and provides configuration."""
    
    @staticmethod
    def detect() -> Environment:
        """Detect the current environment."""
        
        # Check for OpenClaw
        if EnvironmentDetector._is_openclaw():
            return Environment.OPENCLAW
        
        # Check for Claude Desktop
        if EnvironmentDetector._is_claude_desktop():
            return Environment.CLAUDE_DESKTOP
        
        # Check for Claude API
        if EnvironmentDetector._is_claude_api():
            return Environment.CLAUDE_API
        
        # Default to standalone
        return Environment.STANDALONE
    
    @staticmethod
    def _is_openclaw() -> bool:
        """Check if running in OpenClaw environment."""
        # OpenClaw sets specific environment variables
        if os.environ.get("OPENCLAW_HOME"):
            return True
        
        # Check if openclaw command exists
        try:
            subprocess.run(
                ["openclaw", "--version"],
                capture_output=True,
                check=True,
                timeout=2
            )
            return True
        except:
            pass
        
        # Check for OpenClaw workspace
        workspace = Path.home() / ".openclaw/workspace"
        return workspace.exists()
    
    @staticmethod
    def _is_claude_desktop() -> bool:
        """Check if running in Claude Desktop environment."""
        # Claude Desktop sets specific environment variables
        # ANTHROPIC_API_KEY is removed to avoid false detection in OpenClaw
        env_vars = [
            "CLAUDE_DESKTOP_APP",
            "MCP_SERVERS"  # Claude Desktop often uses MCP
        ]
        return any(os.environ.get(var) for var in env_vars)
    
    @staticmethod
    def _is_claude_api() -> bool:
        """Check if running via Claude API."""
        # When called from Claude API, there's usually an API key
        return bool(os.environ.get("ANTHROPIC_API_KEY"))
    
    @staticmethod
    def get_config(env: Environment) -> dict:
        """Get environment-specific configuration."""
        
        if env == Environment.OPENCLAW:
            return {
                "name": "OpenClaw",
                "workspace": Path.home() / ".openclaw/workspace",
                "piper_dir": Path.home() / ".openclaw/workspace/piper",
                "config_file": Path.home() / ".openclaw/workspace/.audio_pt_voice_config",
                "uses_agent": True,
                "supports_claude": True,
                "supports_files": True,
                "supports_sending": True,
            }
        
        elif env == Environment.CLAUDE_DESKTOP:
            return {
                "name": "Claude Desktop",
                "workspace": Path.home() / ".claude-audio-pt",  # Custom workspace
                "piper_dir": Path.home() / ".claude-audio-pt/piper",
                "config_file": Path.home() / ".claude-audio-pt/config.json",
                "uses_agent": False,
                "supports_claude": True,
                "supports_files": True,
                "supports_sending": False,  # Can't send to Telegram from Claude
            }
        
        elif env == Environment.CLAUDE_API:
            return {
                "name": "Claude API",
                "workspace": None,  # No persistent workspace
                "piper_dir": "/tmp/piper-audio-pt",  # Temporary
                "config_file": None,  # No persistent config
                "uses_agent": False,
                "supports_claude": True,
                "supports_files": True,
                "supports_sending": False,
            }
        
        else:  # STANDALONE
            return {
                "name": "Standalone",
                "workspace": Path.home() / ".audio-pt-autoreply",
                "piper_dir": Path.home() / ".audio-pt-autoreply/piper",
                "config_file": Path.home() / ".audio-pt-autoreply/config.json",
                "uses_agent": False,
                "supports_claude": True,
                "supports_files": True,
                "supports_sending": False,
            }


# Global environment cache
_detected_env = None
_detected_config = None

def get_environment() -> Environment:
    """Get detected environment (cached)."""
    global _detected_env
    if _detected_env is None:
        _detected_env = EnvironmentDetector.detect()
    return _detected_env

def get_config() -> dict:
    """Get environment configuration (cached)."""
    global _detected_config
    if _detected_config is None:
        env = get_environment()
        _detected_config = EnvironmentDetector.get_config(env)
    return _detected_config

def reset_detection():
    """Reset detection cache (for testing)."""
    global _detected_env, _detected_config
    _detected_env = None
    _detected_config = None


if __name__ == "__main__":
    env = get_environment()
    config = get_config()
    
    print(f"Environment: {config['name']}")
    print(f"Workspace: {config['workspace']}")
    print(f"Piper Dir: {config['piper_dir']}")
    print(f"Uses Agent: {config['uses_agent']}")
    print(f"Supports Claude: {config['supports_claude']}")
    print(f"Supports Files: {config['supports_files']}")
    print(f"Supports Sending: {config['supports_sending']}")
