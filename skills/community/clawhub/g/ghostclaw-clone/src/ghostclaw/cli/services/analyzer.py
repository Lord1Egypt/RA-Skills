"""AnalyzerService — orchestrates the full codebase analysis pipeline."""

import asyncio
import subprocess
import datetime
import sys
import json
import shutil
from pathlib import Path
from typing import Dict, Any, List, Optional

from ghostclaw.core.analyzer import CodebaseAnalyzer
from ghostclaw.core.cache import LocalCache
from ghostclaw.core.config import GhostclawConfig
from ghostclaw.core.migration import migrate_legacy_storage

try:
    from rich.console import Console
    from rich.markdown import Markdown
    from rich.status import Status
    from rich.text import Text
    HAS_RICH = True
except ImportError:
    HAS_RICH = False

# Import the services package for access to GhostAgent and AgentEvent (patchable)
import ghostclaw.cli.services as services
from .pr import PRService


class AnalyzerService:
    """
    Service for orchestrating the codebase analysis.
    """

    def __init__(self, repo_path: str, config_overrides: Dict[str, Any], use_cache: bool = True,
                 cache_dir: Optional[Path] = None, cache_ttl: int = 7, json_output: bool = False,
                 benchmark: bool = False):
        self.repo_path = repo_path
        self.config_overrides = config_overrides
        self.use_cache = use_cache
        self.cache_dir = cache_dir
        self.cache_ttl = cache_ttl
        self.json_output = json_output
        self.benchmark = benchmark
        self.cache: Optional[LocalCache] = None
        self.timings: Dict[str, float] = {}
        self.synthesis_streamed = False

    async def run(self) -> Dict[str, Any]:
        """Run the analysis pipeline."""
        try:
            config = GhostclawConfig.load(self.repo_path, **self.config_overrides)
        except Exception as e:
            print(f"Configuration Error: {e}", file=sys.stderr)
            raise Exception(f"Analysis Error: Configuration Error: {e}")

        # Perform storage migration if needed (old .ghostclaw/{reports,cache} -> storage/)
        repo_path = Path(self.repo_path)
        if migrate_legacy_storage(repo_path):
            print("🔧 Migrated storage to new layout under .ghostclaw/storage/", file=sys.stderr)

        # Initialize cache if needed
        if self.use_cache:
            self.cache = LocalCache(
                cache_dir=self.cache_dir,
                ttl_days=self.cache_ttl,
                compression=config.cache_compression
            )

        analyzer = CodebaseAnalyzer(cache=self.cache if self.use_cache else None)
        agent = services.GhostAgent(config, self.repo_path, analyzer=analyzer)

        console = Console() if HAS_RICH and not self.json_output else None
        status = None
        live = None
        synthesis_content = []

        async def on_pre_analyze(data):
            nonlocal status
            if console:
                status = console.status("[bold green]Ghostclaw is analyzing architecture...[/bold green]", spinner="dots")
                status.start()

        async def on_post_metrics(data):
            nonlocal status
            if status:
                status.update("[bold blue]Metrics collected. Preparing Ghost Engine...[/bold blue]")

        async def on_pre_synthesis(data):
            nonlocal status
            if status:
                status.update("[bold cyan]🧠 Ghost Engine Synthesis starting...[/bold cyan]")
                print("\n" + "="*50 + "\n")
                print("🧠 Ghost Engine Synthesis:\n")

        async def on_synthesis_chunk(data):
            nonlocal status, live
            self.synthesis_streamed = True
            chunk = data["chunk"]
            if chunk is None:
                return  # Skip None chunks
            synthesis_content.append(chunk)

            if console:
                if status:
                    status.stop()
                    status = None

                if not live:
                    from rich.live import Live
                    live = Live(Text(""), console=console, refresh_per_second=10, transient=True)
                    live.start()

                try:
                    live.update(Text("".join(synthesis_content)))
                except Exception as e:
                    import traceback
                    console.print(f"[red]Error joining synthesis_content: {e}[/red]")
                    traceback.print_exc()
            else:
                output_stream = sys.stderr if self.json_output else sys.stdout
                output_stream.write(chunk)
                output_stream.flush()

        async def on_reasoning_chunk(data):
            nonlocal status, live
            chunk = data["chunk"]
            if console:
                if status:
                    status.stop()
                    status = None
                if not live:
                    from rich.live import Live
                    live = Live(Text(""), console=console, refresh_per_second=10, transient=True)
                    live.start()
                current_text = live.get_renderable()
                if isinstance(current_text, Text):
                    current_text.append(chunk, style="dim italic")
                    live.update(current_text)
            else:
                output_stream = sys.stderr if self.json_output else sys.stdout
                output_stream.write(f"\033[2m{chunk}\033[0m")
                output_stream.flush()

        async def on_post_synthesis(data):
            nonlocal live, status
            if live:
                live.stop()
                live = None
            if status:
                status.stop()
                status = None

            output_stream = sys.stderr if self.json_output else sys.stdout
            if data.get("synthesis_performed"):
                output_stream.write("\n\n" + "="*50)
            output_stream.flush()
            if console and synthesis_content:
                full_text = "".join(synthesis_content)
                if full_text.strip():
                    console.print(Markdown(full_text))

        agent.on(services.AgentEvent.PRE_ANALYZE, on_pre_analyze)
        agent.on(services.AgentEvent.POST_METRICS, on_post_metrics)
        agent.on(services.AgentEvent.PRE_SYNTHESIS, on_pre_synthesis)
        agent.on(services.AgentEvent.REASONING_CHUNK, on_reasoning_chunk)
        agent.on(services.AgentEvent.SYNTHESIS_CHUNK, on_synthesis_chunk)
        agent.on(services.AgentEvent.POST_SYNTHESIS, on_post_synthesis)

        try:
            report = await agent.run()

            # Stop any active Rich UI elements before proceeding
            if status:
                status.stop()
                status = None
            if live:
                live.stop()
                live = None

            if self.benchmark:
                self.timings = getattr(agent, 'timings', {})

            report["_synthesis_streamed"] = self.synthesis_streamed

            # Add token usage to metadata if available (only if AI was used)
            if config.use_ai and hasattr(agent, 'llm_client'):
                lc = agent.llm_client
                try:
                    total = lc.total_tokens
                    if isinstance(total, (int, float)) and total > 0:
                        report.setdefault('metadata', {})['tokens'] = {
                            'prompt': int(getattr(lc, 'prompt_tokens', 0)),
                            'completion': int(getattr(lc, 'completion_tokens', 0)),
                            'total': int(total)
                        }
                except Exception:
                    pass

            if self.use_cache and self.cache and not config.dry_run and "metadata" in report and "fingerprint" in report["metadata"]:
                self.cache.set(report["metadata"]["fingerprint"], report)

            return report

        except Exception as e:
            if status: status.stop()
            if live: live.stop()
            raise Exception(f"Analysis Error: {e}") from e
