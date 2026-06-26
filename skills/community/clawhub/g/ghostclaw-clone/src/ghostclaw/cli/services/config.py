"""ConfigService — initializes Ghostclaw project configuration."""

import json
from pathlib import Path
from typing import Dict, Any


class ConfigService:
    """
    Service for initializing Ghostclaw project configuration.
    """

    @staticmethod
    def init_project(path: str = ".") -> None:
        """
        Scaffold local project configuration.

        Args:
            path (str): The directory where the .ghostclaw config should be created.
        """
        cwd = Path(path)
        gc_dir = cwd / ".ghostclaw"
        gc_dir.mkdir(parents=True, exist_ok=True)
        config_file = gc_dir / "ghostclaw.json"

        if config_file.exists():
            raise FileExistsError(f"⚠️ {config_file} already exists. Skipping initialization.")

        template = {
            "use_ai": True,
            "ai_provider": "openrouter",
            "ai_model": None,
            "use_pyscn": False,
            "use_ai_codeindex": False,
            # Delta-Context (v0.1.10)
            "delta_mode": False,
            "delta_base_ref": "HEAD~1",
            # Orchestrator (v0.2.2a)
            "orchestrate": False,
            "orchestrator": {
                "enabled": False,
                "use_llm": False,
                "weights": {
                    "complexity": 0.4,
                    "coupling": 0.3,
                    "cohesion": 0.3
                }
            },
            # QMD Backend (v0.2.0)
            "use_qmd": False
        }

        # Write JSON5 if available for nicer formatting with comments/trailing commas
        try:
            import json5
            with open(config_file, "w", encoding="utf-8") as f:
                json5.dump(template, f, indent=2)
        except ImportError:
            with open(config_file, "w", encoding="utf-8") as f:
                json.dump(template, f, indent=2)

        print(f"✅ Created template config at {config_file}")
        print("💡 Remember: Do NOT save your GHOSTCLAW_API_KEY in this file. Use an environment variable or ~/.ghostclaw/ghostclaw.json.")
