"""Plugin registry for Ghostclaw's modular architecture."""

import pluggy
import importlib.util
import inspect
import sys
import logging
from pathlib import Path

logger = logging.getLogger(__name__)
from typing import List, Dict, Any, Optional, Set, Tuple
from ghostclaw.core.adapters.hooks import GhostclawPluginSpecs
from ghostclaw.core.adapters.base import AdapterMetadata
from ghostclaw.core.config import GhostclawConfig

# Internal plugin names (for default enable/disable logic)
INTERNAL_PLUGINS = ["pyscn", "ai-codeindex", "sqlite", "qmd", "json_target", "lizard"]


class PluginRegistry:
    """Manages the lifecycle and invocation of Ghostclaw plugins."""

    def __init__(self, project_root: Optional[Path] = None):
        self.pm = pluggy.PluginManager("ghostclaw")
        self.pm.add_hookspecs(GhostclawPluginSpecs)
        # Wrap pm.register to track all plugins (name, instance)
        self._registered_plugins: List[Tuple[str, Any]] = []
        _original_register = self.pm.register

        def _tracked_register(plugin, name=None):
            _original_register(plugin, name=name)
            self._registered_plugins.append((name, plugin))

        self.pm.register = _tracked_register
        self.project_root = project_root

        # Track plugin names and their sources
        self.internal_plugins = set()
        self.external_plugins = set()

        # Accumulate errors during analysis runs
        self.errors: List[str] = []

        # Plugin enable/disable filter (None = all enabled)
        self.enabled_plugins: Optional[Set[str]] = None
        self._file_cache = None  # Lazy init

        # Internal registry of plugins for runtime filtering

    def register_internal_plugins(self):
        """Register built-in adapters if not already registered."""
        from ghostclaw.core.adapters.metric.pyscn import PySCNAdapter
        from ghostclaw.core.adapters.metric.ai_codeindex import AICodeIndexAdapter
        from ghostclaw.core.adapters.storage.sqlite import SQLiteStorageAdapter
        from ghostclaw.core.adapters.storage.qmd import QMDStorageAdapter
        from ghostclaw.core.adapters.target.json import JsonTargetAdapter
        from ghostclaw.core.adapters.scoring.lizard import LizardScoringAdapter

        adapters = {
            "pyscn": PySCNAdapter,
            "ai-codeindex": AICodeIndexAdapter,
            "sqlite": SQLiteStorageAdapter,
            "qmd": QMDStorageAdapter,
            "json_target": JsonTargetAdapter,
            "lizard": LizardScoringAdapter,
        }

        for name, adapter_cls in adapters.items():
            if not self.pm.get_plugin(name):
                self.pm.register(adapter_cls(), name=name)
                self.internal_plugins.add(name)

        # Always discover entry-point plugins (like orchestrator, coderabbit, nomad)
        self.discover_entry_points()

    def discover_entry_points(self):
        """Discover pip-installed plugins via setuptools entry points."""
        try:
            import importlib.metadata

            eps = importlib.metadata.entry_points()
            group = eps.select(group="ghostclaw.plugins")
            for ep in group:
                # Skip if already registered
                if self.pm.get_plugin(ep.name):
                    logger.debug(
                        f"Plugin {ep.name} already registered, skipping entry point"
                    )
                    continue
                try:
                    obj = ep.load()
                    if inspect.isclass(obj):
                        try:
                            obj = obj()
                        except Exception as e:
                            logger.error(
                                f"Failed to instantiate plugin {ep.name} from {ep.value}: {e}"
                            )
                            continue
                    self.pm.register(obj, name=ep.name)
                    logger.debug(f"Loaded plugin {ep.name} from entry point {ep.value}")
                except Exception as e:
                    logger.error(f"Failed to load entry point {ep.name}: {e}")
        except Exception as e:
            logger.debug(f"Error loading setuptools entry points: {e}")

        # Update external_plugins set
        for name, _ in self._registered_plugins:
            if name not in self.internal_plugins:
                self.external_plugins.add(name)

    def load_external_plugins(self, plugins_dir: Optional[Path] = None):
        """
        Scan a directory for plugins and register them.
        Entry-point discovery is now handled by discover_entry_points().
        """
        # Load from local plugins directory if it exists
        if plugins_dir and plugins_dir.exists():
            for path in plugins_dir.iterdir():
                if path.is_dir() and (path / "__init__.py").exists():
                    self._load_module_plugin(path.name, path / "__init__.py")
                elif path.suffix == ".py":
                    self._load_module_plugin(path.stem, path)

        # Entry point discovery is now handled in register_internal_plugins or discover_entry_points

    def _load_module_plugin(self, name: str, path: Path):
        """Dynamically load a python module and register its adapters."""
        try:
            spec = importlib.util.spec_from_file_location(
                f"ghostclaw.plugins.{name}", str(path)
            )
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                sys.modules[f"ghostclaw.plugins.{name}"] = module
                spec.loader.exec_module(module)

                import inspect

                for _, obj in inspect.getmembers(module, inspect.isclass):
                    if obj.__module__ == module.__name__:
                        try:
                            instance = obj()
                            # Determine friendly name from metadata if available
                            try:
                                meta = instance.get_metadata()
                                plugin_name = meta.name
                            except Exception:
                                plugin_name = f"{name}_{obj.__name__}"
                                meta = None

                            # Check if plugin is enabled
                            if (
                                self.enabled_plugins is not None
                                and plugin_name not in self.enabled_plugins
                            ):
                                logger.debug(
                                    f"Plugin '{plugin_name}' is disabled by config; skipping."
                                )
                                continue

                            # Version compatibility check (only if we have metadata)
                            if meta and (
                                meta.min_ghostclaw_version or meta.max_ghostclaw_version
                            ):
                                try:
                                    # Avoid circular import by fetching version via a central version module
                                    from ghostclaw.version import (
                                        __version__ as gc_version,
                                    )

                                    if not self._check_version_compatible(
                                        gc_version, meta
                                    ):
                                        logger.warning(
                                            f"Plugin '{plugin_name}' incompatible with Ghostclaw {gc_version} "
                                            f"(requires {meta.min_ghostclaw_version or 'any'} - {meta.max_ghostclaw_version or 'any'}). Skipping."
                                        )
                                        continue
                                except Exception as e:
                                    logger.debug(
                                        f"Version check error for plugin {plugin_name}: {e}"
                                    )

                            self.pm.register(instance, name=plugin_name)

                            self._registered_plugins.append((plugin_name, instance))
                            self.external_plugins.add(plugin_name)
                        except Exception as e:
                            logger.error(
                                f"Failed to load plugin class {obj.__name__}: {e}"
                            )
        except Exception as e:
            logger.debug(f"Error loading plugin module at {path}: {e}")

    async def run_analysis(
        self, root: str, files: List[str], config: Optional[GhostclawConfig] = None
    ) -> List[Dict[str, Any]]:
        """Invoke all enabled metric adapters concurrently, collecting errors."""
        import asyncio
        from ghostclaw.core.cache import PerFileAnalysisCache
        from ghostclaw.core.config import GhostclawConfig

        # Backward compatibility: if no config provided, create a default
        if config is None:
            config = GhostclawConfig()

        self.errors = []  # reset

        # Initialize file cache if not already done
        if self._file_cache is None:
            self._file_cache = PerFileAnalysisCache()

        # Prepare initialization context for plugins
        context = {
            "config": config,
            "registry": self,
        }
        # Call ghost_initialize on plugins that implement it
        for name, plugin in self.pm.list_name_plugin():
            # Only initialize enabled plugins
            enabled = self.enabled_plugins
            if enabled is not None and (name is None or name not in enabled):
                continue
            if hasattr(plugin, "ghost_initialize"):
                try:
                    # Hook is async
                    await plugin.ghost_initialize(context)
                except Exception as e:
                    logger.warning(f"Plugin {name} ghost_initialize failed: {e}")

        tasks = []
        # Determine which plugins to run
        for name, plugin in self.pm.list_name_plugin():
            # Filter by enabled_plugins if set
            enabled = self.enabled_plugins
            if enabled is not None and (name is None or name not in enabled):
                continue
            # Only consider adapters with ghost_analyze
            if hasattr(plugin, "ghost_analyze"):
                # Determine per-file caching strategy
                use_per_file = False
                try:
                    meta = plugin.get_metadata()
                    # Support both AdapterMetadata objects and plain dicts
                    if hasattr(meta, 'supports_per_file_cache'):
                        use_per_file = bool(meta.supports_per_file_cache)
                    elif isinstance(meta, dict) and 'supports_per_file_cache' in meta:
                        use_per_file = bool(meta['supports_per_file_cache'])
                except Exception:
                    use_per_file = False
                if use_per_file:
                    tasks.append(self._run_adapter_with_cache(name, plugin, root, files))
                else:
                    tasks.append(self._run_adapter(name, plugin, root, files))

        if not tasks:
            return []

        results = await asyncio.gather(*tasks)
        return list(results)

    async def _run_adapter_with_cache(
        self, name: str, plugin, root: str, files: List[str]
    ) -> Dict[str, Any]:
        """Run a single adapter with per-file caching."""
        if self._file_cache is None:
            from ghostclaw.core.cache import PerFileAnalysisCache

            self._file_cache = PerFileAnalysisCache()

        root_path = Path(root)
        to_analyze = []
        cached_results = []

        # 1. Check cache for each file
        for f in files:
            f_path = Path(f)
            abs_f = f_path if f_path.is_absolute() else root_path / f
            cached = self._file_cache.get(abs_f, name)
            if cached is not None:
                cached_results.append(cached)
            else:
                to_analyze.append(f)

        # 2. If all files cached, merge and return (include global data if present)
        if not to_analyze:
            global_cached = self._file_cache.get(Path("<global>"), name)
            if global_cached is not None:
                cached_results.append(global_cached)
            return self._merge_results(cached_results)

        # 3. Run adapter on non-cached files
        new_result = await self._run_adapter(name, plugin, root, to_analyze)

        # 4. Split and cache new results (per-file + global)
        split_map, global_data = self._split_result_by_file(new_result, to_analyze)
        for f_path_str, f_res in split_map.items():
            abs_p = (
                Path(f_path_str)
                if Path(f_path_str).is_absolute()
                else root_path / f_path_str
            )
            self._file_cache.set(abs_p, name, f_res)
        # Also cache global data under a special key
        if global_data:
            self._file_cache.set(Path("<global>"), name, global_data)

        # 5. Merge results without duplication
        # Collect per-file parts: new split results + any cached per-file results
        all_parts = list(split_map.values()) + cached_results

        # Global data: prefer current run's global_data; if absent, try cached global
        if global_data:
            all_parts.append(global_data)
        else:
            global_cached = self._file_cache.get(Path("<global>"), name)
            if global_cached is not None:
                all_parts.append(global_cached)

        return self._merge_results(all_parts)

    def _split_result_by_file(
        self, result: Dict[str, Any], files: List[str]
    ) -> tuple[Dict[str, Dict[str, Any]], Dict[str, Any]]:
        """Split adapter results into per-file dictionaries and global unmatched data.

        Returns:
            (split_map, global_data)
            - split_map: {file_path: {key: items}}
            - global_data: {key: items} for results not attributable to any file
        """
        split_map = {f: {} for f in files}
        global_data: Dict[str, Any] = {}

        # Common keys in ArchitectureReport
        for key in ["issues", "architectural_ghosts", "red_flags"]:
            items = result.get(key, [])
            if not isinstance(items, list):
                # Non-list values are global
                global_data[key] = items
                continue

            for item in items:
                file_found = None
                if isinstance(item, str):
                    for f in files:
                        if f in item:
                            file_found = f
                            break
                elif isinstance(item, dict):
                    for field in ["file", "path", "filename"]:
                        if field in item and item[field] in files:
                            file_found = item[field]
                            break

                if file_found:
                    split_map[file_found].setdefault(key, []).append(item)
                else:
                    # Could not attribute to a specific file → global
                    global_data.setdefault(key, []).append(item)

        # Coupling metrics: per-file or global if not matching any file
        coupling = result.get("coupling_metrics", {})
        if isinstance(coupling, dict):
            for f, metrics in coupling.items():
                if f in split_map:
                    split_map[f]["coupling_metrics"] = {f: metrics}
                else:
                    global_data.setdefault("coupling_metrics", {})[f] = metrics

        # Preserve any other top-level keys that we didn't split (e.g., symbol_index, metadata, etc.)
        for key in ["symbol_index", "metadata", "coupling_metrics", "architecture"]:
            if key == "coupling_metrics":
                continue  # already handled above
            if key in result and key not in ["issues", "architectural_ghosts", "red_flags"]:
                # These are global by nature
                global_data.setdefault(key, result[key])

        return split_map, global_data

    def _merge_results(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Merge multiple adapter results into one."""
        if not results:
            return {}
        if len(results) == 1:
            return results[0]

        merged = {}
        for res in results:
            for k, v in res.items():
                if isinstance(v, list):
                    merged.setdefault(k, []).extend(v)
                elif isinstance(v, dict):
                    merged.setdefault(k, {}).update(v)
                elif isinstance(v, bool):
                    merged[k] = v  # Last-writer wins for booleans
                elif isinstance(v, (int, float)):
                    merged[k] = merged.get(k, 0) + v
                else:
                    merged[k] = v
        return merged

    async def _run_adapter(
        self, name: str, plugin, root: str, files: List[str]
    ) -> Dict[str, Any]:
        """Run a single adapter and capture errors."""
        try:
            return await plugin.ghost_analyze(root, files)
        except Exception as e:
            self.errors.append(f"Plugin '{name}': {type(e).__name__}: {e}")
            return {}

    def _check_version_compatible(self, current: str, meta: AdapterMetadata) -> bool:
        """Check if current Ghostclaw version is within plugin's required range using simple version comparison."""

        def parse(v: str):
            parts = v.split(".")
            nums = []
            for p in parts[:3]:
                try:
                    nums.append(int(p))
                except ValueError:
                    # numeric prefix only
                    num = ""
                    for ch in p:
                        if ch.isdigit():
                            num += ch
                        else:
                            break
                    nums.append(int(num) if num else 0)
            while len(nums) < 3:
                nums.append(0)
            return tuple(nums)

        cur_t = parse(current)
        if meta.min_ghostclaw_version:
            min_t = parse(meta.min_ghostclaw_version)
            if cur_t < min_t:
                return False
        if meta.max_ghostclaw_version:
            max_t = parse(meta.max_ghostclaw_version)
            if cur_t > max_t:
                return False
        return True

    async def emit_event(self, event_type: str, data: Any):
        """Broadcast events to all target adapters."""
        import asyncio

        coroutines = self.pm.hook.ghost_emit(event_type=event_type, data=data)
        if coroutines:
            await asyncio.gather(*coroutines)

    async def save_report(self, report: Any) -> List[str]:
        """Save report via all enabled storage adapters."""
        import asyncio

        tasks = []
        for name, plugin in self.pm.list_name_plugin():
            # Filter by enabled_plugins if set
            if self.enabled_plugins is not None and name not in self.enabled_plugins:
                continue
            # Only call if plugin has ghost_save_report
            if hasattr(plugin, "ghost_save_report"):
                tasks.append(plugin.ghost_save_report(report=report))
        if not tasks:
            return []
        ids = await asyncio.gather(*tasks)
        return [i for i in ids if i] if ids else []

    def get_plugin_metadata(self) -> List[Dict[str, Any]]:
        """Get metadata for all registered plugins."""
        return self.pm.hook.ghost_get_metadata()

    async def compute_custom_vibe(self, context: Any) -> Optional[float]:
        """Invoke the first available ScoringAdapter to compute the vibe score."""
        import asyncio

        coroutines = self.pm.hook.ghost_compute_vibe(context=context)
        if not coroutines:
            return None

        results = await asyncio.gather(*coroutines)

        for res in results:
            if res is not None:
                return res
        return None

    async def validate_all(self) -> Dict[str, bool]:
        """Validate all registered plugins by calling is_available."""
        results = {}
        for name, plugin in self._registered_plugins:
            if hasattr(plugin, "is_available"):
                try:
                    results[name] = await plugin.is_available()
                except Exception:
                    results[name] = False
            else:
                results[name] = True
        return results


# Global registry instance
registry = PluginRegistry()
