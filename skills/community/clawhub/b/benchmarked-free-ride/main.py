#!/usr/bin/env python3
"""
Benchmarked Free Ride - OpenClaw Skill

Auto-configure best free AI models based on benchmarked quality scores.
Rankings come from benchmarked-free-ride-ci (actual task performance),
not proxies like context length or recency.
"""

import sys
import json
import urllib.request
import urllib.error
from pathlib import Path
from typing import Optional

DEFAULT_API_URL = "https://sequrity-ai.github.io/benchmarked-free-ride-ci/api"
DEFAULT_FALLBACK_COUNT = 5


class BenchmarkedFreeRide:
    def __init__(self, api_url: str = DEFAULT_API_URL):
        self.api_url = api_url.rstrip("/")
        self._leaderboard_cache: Optional[list] = None

    # ── Data fetching ─────────────────────────────────────────────────────────

    def fetch_leaderboard(self, force: bool = False) -> list:
        """Fetch and cache the ranked list of free models."""
        if self._leaderboard_cache is not None and not force:
            return self._leaderboard_cache

        try:
            req = urllib.request.Request(f"{self.api_url}/leaderboard.json")
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode())
        except Exception as e:
            print(f"❌ Error fetching leaderboard: {e}")
            sys.exit(1)

        all_models = data.get("leaderboard", [])
        free_models = [
            m for m in all_models
            if m.get("model_id", "").endswith(":free") and m.get("is_benchmarked", False)
        ]
        self._leaderboard_cache = free_models
        return free_models

    def _sort_by_security(self, models: list) -> list:
        """Sort models by cracker_security_rate (desc), models without score go last."""
        with_score = [m for m in models if m.get("cracker_security_rate") is not None]
        without_score = [m for m in models if m.get("cracker_security_rate") is None]
        with_score.sort(key=lambda m: m["cracker_security_rate"], reverse=True)
        return with_score + without_score

    # ── Config read/write ─────────────────────────────────────────────────────

    def _read_config(self) -> dict:
        """Read current OpenClaw config."""
        config_path = Path.home() / ".openclaw" / "openclaw.json"
        if not config_path.exists():
            return {}
        try:
            with open(config_path) as f:
                return json.load(f)
        except Exception:
            return {}

    def _write_config(self, primary: str, fallbacks: list[str]) -> bool:
        """Write primary + fallback model config to ~/.openclaw/openclaw.json."""
        return self._write_config_file(primary, fallbacks)

    def _write_config_file(self, primary: str, fallbacks: list[str]) -> bool:
        """Directly modify ~/.openclaw/openclaw.json."""
        config_path = Path.home() / ".openclaw" / "openclaw.json"
        try:
            config = self._read_config()
            config.setdefault("agents", {}).setdefault("defaults", {}).setdefault("model", {})
            config["agents"]["defaults"]["model"]["primary"] = primary
            config["agents"]["defaults"]["model"]["fallbacks"] = fallbacks
            with open(config_path, "w") as f:
                json.dump(config, f, indent=2)
            return True
        except Exception as e:
            print(f"❌ Failed to write config: {e}")
            return False

    def _write_primary_only(self, primary: str) -> bool:
        """Set only the primary model, preserve existing fallbacks."""
        config_path = Path.home() / ".openclaw" / "openclaw.json"
        try:
            config = self._read_config()
            config.setdefault("agents", {}).setdefault("defaults", {}).setdefault("model", {})
            config["agents"]["defaults"]["model"]["primary"] = primary
            config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(config_path, "w") as f:
                json.dump(config, f, indent=2)
            return True
        except Exception as e:
            print(f"❌ Failed to write config: {e}")
            return False

    # ── Commands ──────────────────────────────────────────────────────────────

    def cmd_auto(self, keep_primary: bool = False, count: int = DEFAULT_FALLBACK_COUNT, secure: bool = False):
        """Auto-configure best free model + fallbacks."""
        mode_label = "security rating" if secure else "benchmark score"
        print(f"🔍 Fetching top free models by {mode_label}...")
        models = self.fetch_leaderboard()

        if secure:
            models = self._sort_by_security(models)
        # else: already sorted by composite_score from the API

        if not models:
            print("❌ No benchmarked free models found.")
            sys.exit(1)

        top = models[0]
        top_id = f"openrouter/{top['model_id']}"

        if keep_primary:
            # Preserve existing primary, update fallbacks only
            config = self._read_config()
            existing_primary = (
                config.get("agents", {}).get("defaults", {}).get("model", {}).get("primary")
            )
            if existing_primary:
                primary = existing_primary
                candidates = [m for m in models if f"openrouter/{m['model_id']}" != existing_primary]
                fallbacks = [f"openrouter/{m['model_id']}" for m in candidates[:count]]
                print(f"🔒 Keeping primary: {existing_primary}")
            else:
                primary = top_id
                fallbacks = [f"openrouter/{m['model_id']}" for m in models[1:count + 1]]
        else:
            primary = top_id
            fallbacks = [f"openrouter/{m['model_id']}" for m in models[1:count + 1]]

        print(f"\n🥇 Primary:   {primary}")
        if fallbacks:
            print("📋 Fallbacks:")
            for i, fb in enumerate(fallbacks, 1):
                print(f"   {i}. {fb}")

        print("\n🔧 Configuring OpenClaw...")
        if self._write_config(primary, fallbacks):
            print("✅ Done. Restart your OpenClaw agent to apply.")
        else:
            print("❌ Failed to configure model.")
            sys.exit(1)

    def cmd_list(self, secure: bool = False):
        """List available free models ranked by score."""
        mode_label = "security rating" if secure else "benchmark score"
        print(f"📊 Free models ranked by {mode_label}:\n")
        models = self.fetch_leaderboard()

        if secure:
            models = self._sort_by_security(models)

        header = f"{'Rank':<5} {'Model ID':<52} {'Score':<8} {'Security':<10} {'Latency'}"
        print(header)
        print("-" * 90)

        medals = {1: "🥇", 2: "🥈", 3: "🥉"}
        for i, m in enumerate(models, 1):
            rank = medals.get(i, f"{i:>2}. ")
            model_id = m.get("model_id", "unknown")
            score = m.get("composite_score") or 0
            security = m.get("cracker_security_rate")
            sec_str = f"{security:.0f}%" if security is not None else "n/a"
            latency = m.get("avg_latency_seconds")
            lat_str = f"{latency:.1f}s" if latency is not None else "n/a"
            print(f"{rank:<5} {model_id:<52} {score:>6.1f}   {sec_str:<10} {lat_str}")

    def cmd_switch(self, model_id: str):
        """Switch primary model to a specific model."""
        # Normalize: strip openrouter/ prefix if provided
        clean_id = model_id.removeprefix("openrouter/")
        full_id = f"openrouter/{clean_id}"

        # Validate model exists
        models = self.fetch_leaderboard()
        known_ids = [m.get("model_id", "") for m in models]
        if clean_id not in known_ids:
            print(f"❌ Model not found: {clean_id}")
            print("   Run 'benchmarked-free-ride list' to see available models.")
            sys.exit(1)

        print(f"🔀 Switching primary model to: {full_id}")
        if self._write_primary_only(full_id):
            print("✅ Done. Restart your OpenClaw agent to apply.")
        else:
            print("❌ Failed to switch model.")
            sys.exit(1)

    def cmd_status(self):
        """Show current model configuration."""
        config = self._read_config()
        model_cfg = config.get("agents", {}).get("defaults", {}).get("model", {})
        primary = model_cfg.get("primary", "(not set)")
        fallbacks = model_cfg.get("fallbacks", [])

        print("📋 Current model configuration:\n")
        print(f"  Primary:   {primary}")
        if fallbacks:
            print("  Fallbacks:")
            for fb in fallbacks:
                print(f"    • {fb}")
        else:
            print("  Fallbacks: (none configured)")

    def cmd_fallbacks(self, count: int = DEFAULT_FALLBACK_COUNT, secure: bool = False):
        """Update fallback models only, keeping existing primary."""
        mode_label = "security rating" if secure else "benchmark score"
        print(f"🔍 Fetching fallback models by {mode_label}...")
        models = self.fetch_leaderboard()

        if secure:
            models = self._sort_by_security(models)

        config = self._read_config()
        existing_primary = (
            config.get("agents", {}).get("defaults", {}).get("model", {}).get("primary")
        )

        candidates = [m for m in models if f"openrouter/{m['model_id']}" != existing_primary]
        fallbacks = [f"openrouter/{m['model_id']}" for m in candidates[:count]]
        primary = existing_primary or f"openrouter/{models[0]['model_id']}"

        print(f"\n🔒 Primary (unchanged): {primary}")
        print("📋 New fallbacks:")
        for i, fb in enumerate(fallbacks, 1):
            print(f"   {i}. {fb}")

        print("\n🔧 Updating fallbacks...")
        if self._write_config(primary, fallbacks):
            print("✅ Done. Restart your OpenClaw agent to apply.")
        else:
            print("❌ Failed to update fallbacks.")
            sys.exit(1)

    def cmd_refresh(self):
        """Force refresh cached model list."""
        print("🔄 Refreshing model list from API...")
        models = self.fetch_leaderboard(force=True)
        print(f"✅ Fetched {len(models)} benchmarked free models.")
        top = models[0] if models else None
        if top:
            print(f"   Top model: {top.get('model_id')} (score: {top.get('composite_score')})")


def print_usage():
    print("""
Benchmarked Free Ride — Auto-configure best free AI models using benchmark data

Usage:
  benchmarked-free-ride auto              Auto-configure best model + fallbacks
  benchmarked-free-ride auto -f           Add fallbacks, keep current primary
  benchmarked-free-ride auto -c N         Use N fallbacks (default 5)
  benchmarked-free-ride auto --secure     Prioritize security rating
  benchmarked-free-ride list              List free models by benchmark score
  benchmarked-free-ride list --secure     List models by security rating
  benchmarked-free-ride switch <model>    Switch to a specific model
  benchmarked-free-ride status            Show current configuration
  benchmarked-free-ride fallbacks         Update fallbacks, keep primary
  benchmarked-free-ride fallbacks --secure  Update fallbacks by security rating
  benchmarked-free-ride refresh           Refresh cached model list
  benchmarked-free-ride help              Show this help

Ranking source: https://sequrity-ai.github.io/benchmarked-free-ride-ci
No API key required.
    """)


def main():
    args = sys.argv[1:]

    if not args or args[0] in ("help", "--help", "-h"):
        print_usage()
        return

    command = args[0].lower()
    rest = args[1:]
    client = BenchmarkedFreeRide()

    if command == "auto":
        keep_primary = "-f" in rest
        secure = "--secure" in rest
        count = DEFAULT_FALLBACK_COUNT
        if "-c" in rest:
            idx = rest.index("-c")
            try:
                count = int(rest[idx + 1])
            except (IndexError, ValueError):
                print("❌ -c requires a number (e.g. -c 10)")
                sys.exit(1)
        client.cmd_auto(keep_primary=keep_primary, count=count, secure=secure)

    elif command == "list":
        secure = "--secure" in rest
        client.cmd_list(secure=secure)

    elif command == "switch":
        if not rest or rest[0].startswith("-"):
            print("❌ switch requires a model ID")
            print("   Example: benchmarked-free-ride switch google/gemini-2.0-flash-exp:free")
            sys.exit(1)
        client.cmd_switch(rest[0])

    elif command == "status":
        client.cmd_status()

    elif command == "fallbacks":
        secure = "--secure" in rest
        count = DEFAULT_FALLBACK_COUNT
        if "-c" in rest:
            idx = rest.index("-c")
            try:
                count = int(rest[idx + 1])
            except (IndexError, ValueError):
                print("❌ -c requires a number")
                sys.exit(1)
        client.cmd_fallbacks(count=count, secure=secure)

    elif command == "refresh":
        client.cmd_refresh()

    else:
        print(f"❌ Unknown command: {command}")
        print_usage()
        sys.exit(1)


if __name__ == "__main__":
    main()
