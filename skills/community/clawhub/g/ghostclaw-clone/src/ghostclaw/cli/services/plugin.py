"""PluginService — manages external architectural adapters/plugins."""

import shutil
import json
from pathlib import Path
from typing import List, Dict, Any, Optional


class PluginService:
    """
    Service for managing external architectural adapters/plugins.
    """

    def __init__(self, workspace_path: str = "."):
        self.workspace_path = Path(workspace_path)
        self.plugins_dir = self.workspace_path / ".ghostclaw" / "plugins"
        self.config_path = self.workspace_path / ".ghostclaw" / "ghostclaw.json"

    def initialize_registry(self):
        """Register built-in plugins and any available external ones."""
        # Import registry lazily to allow patching via ghostclaw.cli.services.registry
        from ghostclaw.cli.services import registry
        registry.register_internal_plugins()
        # Always attempt to load external plugins (directory may not exist yet)
        registry.load_external_plugins(self.plugins_dir)

    def list_plugins(self) -> List[Dict[str, Any]]:
        self.initialize_registry()
        from ghostclaw.cli.services import registry
        return registry.get_plugin_metadata()

    def get_plugin_info(self, name: str) -> Optional[Dict[str, Any]]:
        self.initialize_registry()
        from ghostclaw.cli.services import registry
        metadata = registry.get_plugin_metadata()
        for meta in metadata:
            if meta.get("name") == name:
                return meta
        return None

    def add_plugin(self, source_path: str) -> Path:
        source = Path(source_path)
        if not source.exists():
            raise FileNotFoundError(f"Source path '{source}' does not exist.")

        self.plugins_dir.mkdir(parents=True, exist_ok=True)
        target = self.plugins_dir / source.name

        if target.exists():
            print(f"⚠️ Plugin '{source.name}' already installed at {target}. Overwriting...")
            if target.is_dir():
                shutil.rmtree(target)
            else:
                target.unlink()

        try:
            if source.is_dir():
                shutil.copytree(source, target)
            else:
                shutil.copy2(source, target)
            return target
        except Exception as e:
            raise Exception(f"Failed to install plugin: {e}")

    def remove_plugin(self, name: str) -> Path:
        self.initialize_registry()
        from ghostclaw.cli.services import registry
        name = name.lower()

        if name in registry.internal_plugins:
            raise ValueError(f"Cannot remove built-in plugin '{name}'.")

        target = self.plugins_dir / name

        if not target.exists():
            matches = list(self.plugins_dir.glob(f"{name}*"))
            if matches:
                target = matches[0]

        if target.exists():
            try:
                if target.is_dir():
                    shutil.rmtree(target)
                else:
                    target.unlink()
                return target
            except Exception as e:
                raise Exception(f"Failed to remove plugin: {e}")
        else:
            raise FileNotFoundError(f"External plugin '{name}' not found in {self.plugins_dir}.")

    def enable_plugin(self, name: str) -> None:
        self.initialize_registry()
        from ghostclaw.cli.services import registry
        all_names = [m.get("name") for m in registry.get_plugin_metadata()]
        if name not in all_names:
            raise ValueError(f"Plugin '{name}' not found. Available: {', '.join(all_names)}")

        config_data = {}
        if self.config_path.exists():
            try:
                config_data = json.loads(self.config_path.read_text())
            except Exception as e:
                raise Exception(f"Failed to read config: {e}")

        enabled = config_data.get("plugins_enabled")
        if enabled is None:
            print(f"ℹ️ Plugin '{name}' is already enabled (all plugins enabled by default).")
            return

        if name in enabled:
            print(f"ℹ️ Plugin '{name}' is already enabled.")
            return

        enabled.append(name)
        config_data["plugins_enabled"] = enabled

        try:
            self.config_path.write_text(json.dumps(config_data, indent=2))
        except Exception as e:
            raise Exception(f"Failed to write config: {e}")

    def disable_plugin(self, name: str) -> None:
        self.initialize_registry()
        from ghostclaw.cli.services import registry
        all_names = [m.get("name") for m in registry.get_plugin_metadata()]
        if name not in all_names:
            raise ValueError(f"Plugin '{name}' not found. Available: {', '.join(all_names)}")

        config_data = {}
        if self.config_path.exists():
            try:
                config_data = json.loads(self.config_path.read_text())
            except Exception as e:
                raise Exception(f"Failed to read config: {e}")

        enabled = config_data.get("plugins_enabled")
        if enabled is None:
            enabled = [n for n in all_names if n != name]
            config_data["plugins_enabled"] = enabled
            try:
                self.config_path.write_text(json.dumps(config_data, indent=2))
                print(f"✅ Disabled plugin '{name}'. {len(enabled)} plugins remain enabled.")
                return
            except Exception as e:
                raise Exception(f"Failed to write config: {e}")
        else:
            if name not in enabled:
                print(f"ℹ️ Plugin '{name}' is already disabled (not in whitelist).")
                return

            enabled.remove(name)
            config_data["plugins_enabled"] = enabled
            try:
                self.config_path.write_text(json.dumps(config_data, indent=2))
            except Exception as e:
                raise Exception(f"Failed to write config: {e}")

    def test_plugin(self, name: str) -> bool:
        self.initialize_registry()
        from ghostclaw.cli.services import registry
        metadata = registry.get_plugin_metadata()
        return any(m.get("name") == name for m in metadata)

    def scaffold_plugin(self, name: str) -> Path:
        # ... unchanged ...
        name = name.lower().replace("-", "_")
        plugin_dir = self.plugins_dir / name
        plugin_dir.mkdir(parents=True, exist_ok=True)

        init_file = plugin_dir / "__init__.py"
        if init_file.exists():
            raise FileExistsError(f"Plugin '{name}' already exists at {plugin_dir}")

        template = f'''
"""
Ghostclaw Adapter: {name}
"""
from typing import Dict, List, Any, Optional
from ghostclaw.core.adapters.base import MetricAdapter, AdapterMetadata
from ghostclaw.core.adapters.hooks import hookimpl

class CustomAdapter(MetricAdapter):
    def get_metadata(self) -> AdapterMetadata:
        return AdapterMetadata(
            name="{name}",
            version="0.1.0",
            description="Custom architectural analysis.",
            dependencies=[]
        )

    async def is_available(self) -> bool:
        return True

    @hookimpl
    async def ghost_analyze(self, root: str, files: List[str]) -> Dict[str, Any]:
        return {{
            "issues": ["Example issue from {name}"],
            "architectural_ghosts": [],
            "red_flags": []
        }}

    @hookimpl
    def ghost_get_metadata(self) -> Dict[str, Any]:
        meta = self.get_metadata()
        return {{
            "name": meta.name,
            "version": meta.version,
            "description": meta.description
        }}
'''
        init_file.write_text(template)
        return plugin_dir
