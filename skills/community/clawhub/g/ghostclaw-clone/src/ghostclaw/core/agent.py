import asyncio
import logging
import time
from enum import Enum, auto
from typing import Dict, List, Callable, Any, Optional, Union
from ghostclaw.core.config import GhostclawConfig  # type: ignore
from ghostclaw.core.analyzer import CodebaseAnalyzer  # type: ignore
from ghostclaw.core.llm_client import LLMClient  # type: ignore

logger = logging.getLogger("ghostclaw.agent")

class AgentEvent(Enum):
    INIT = auto()
    PRE_ANALYZE = auto()
    POST_METRICS = auto()
    PRE_SYNTHESIS = auto()
    SYNTHESIS_CHUNK = auto()
    REASONING_CHUNK = auto()
    POST_SYNTHESIS = auto()
    ERROR = auto()

class GhostAgent:
    """
    Orchestrator for the analysis lifecycle.
    Encapsulates metrics collection and LLM synthesis with hooks for monitoring.
    """

    def __init__(self, config: GhostclawConfig, repo_path: str, analyzer: Optional[CodebaseAnalyzer] = None, bridge=None):
        self.config = config
        self.repo_path = repo_path
        self.analyzer = analyzer or CodebaseAnalyzer()
        # Only initialize LLM client if AI synthesis is enabled
        self.llm_client = LLMClient(config, repo_path) if config.use_ai else None
        self.bridge = bridge
        self.hooks: Dict[AgentEvent, List[Callable[[Dict], Any]]] = {
            event: [] for event in AgentEvent
        }
        self.timings: Dict[str, float] = {}
        self._start_time: float = 0.0

    def on(self, event: AgentEvent, callback: Callable[[Dict], Any]):
        """Register a callback for a specific AgentEvent."""
        self.hooks[event].append(callback)

    async def _emit(self, event: AgentEvent, data: Optional[Dict] = None):
        """Emit an event and trigger all registered hooks and adapters using formal notification schema."""
        data = data or {}
        event_data = dict(data)
        event_data["event"] = event.name

        # Map internal events to formal schema
        formal_event = "events.log"
        if event in (AgentEvent.INIT, AgentEvent.PRE_ANALYZE, AgentEvent.POST_METRICS, AgentEvent.PRE_SYNTHESIS, AgentEvent.POST_SYNTHESIS):
            formal_event = "events.progress"
        elif event in (AgentEvent.SYNTHESIS_CHUNK, AgentEvent.REASONING_CHUNK):
            formal_event = "events.stream"

        event_data["formal_event"] = formal_event

        # 1. Trigger internal hooks
        for hook in self.hooks[event]:
            try:
                if asyncio.iscoroutinefunction(hook):
                    await hook(event_data)
                else:
                    hook(event_data)
            except Exception as e:
                logger.error(f"Error in hook {hook} for event {event}: {e}")

        # 2. Trigger TargetAdapters
        from ghostclaw.core.adapters.registry import registry  # type: ignore
        await registry.emit_event(event.name, event_data)

        # 3. Emit to bridge if present
        if hasattr(self, 'bridge') and self.bridge:
            self.bridge.emit_event(formal_event, event_data)

    async def run(self) -> Dict:
        """Execute the full agent workflow with lifecycle hooks and persistence."""
        self._start_time = time.perf_counter()
        try:
            # Phase 1: Diagnostics
            report = await self._collect_diagnostics()
            
            # Phase 2: Synthesis (Enhanced Intelligence)
            if self.config.use_ai:
                report = await self._perform_synthesis(report)
                await self._emit(AgentEvent.POST_SYNTHESIS, report)
            
            # Persistence & Final Broadcast
            # Use the same registry that was used for analysis (respects enabled_plugins filter)
            if not hasattr(self.analyzer, 'registry') or self.analyzer.registry is None:
                raise RuntimeError("Analyzer registry not available for save_report")
            await self.analyzer.registry.save_report(report)

            self.timings['total'] = time.perf_counter() - self._start_time
            return report


        except Exception as e:
            await self._emit(AgentEvent.ERROR, {"error": str(e)})
            raise e

    async def _collect_diagnostics(self) -> Dict:
        """Run core analysis and collection phase."""
        from ghostclaw.core.adapters.registry import registry  # type: ignore
        registry.register_internal_plugins()
        
        logger.info("Phase 1: Starting Core Diagnostics...")
        await self._emit(AgentEvent.INIT)
        await self._emit(AgentEvent.PRE_ANALYZE)
        
        report_model = await self.analyzer.analyze(self.repo_path, config=self.config)
        report = report_model.model_dump()
        
        await self._emit(AgentEvent.POST_METRICS, report)
        logger.info(f"Diagnostics complete. Analyzed {report.get('files_analyzed', 0)} files.")
        return report

    async def _perform_synthesis(self, report: Dict) -> Dict:
        """Perform AI synthesis or static summary based on report state."""
        if "ai_prompt" not in report:
            return report

        logger.info("Phase 2: Starting Synthesis...")

        # Case 1: Empty Codebase Handling
        if report.get("files_analyzed", 0) == 0:
            logger.info("Empty codebase detected. Providing static advisory.")
            report["ai_synthesis"] = (
                "# Codebase Architecture Vibe Synthesis Report\n\n"
                "## Executive Summary\n\n"
                "Ghostclaw detected an **empty codebase** or a setup where no supported source files "
                "were found. Consequently, no architectural patterns, flows, or cohesion metrics "
                "could be evaluated.\n\n"
                "## Recommendations\n"
                "1. **Initialize your project**: Add source files (Python, Node.js, Go) to the repository root.\n"
                "2. **Check configuration**: Ensure that your `include_extensions` and `exclude_patterns` "
                "correctly target your source code.\n"
                "3. **Verify stack detection**: If this is a supported stack, ensure standard indicators "
                "(like `requirements.txt` or `package.json`) are present.\n"
            )
            report["ai_reasoning"] = "Skipped LLM synthesis for empty codebase to provide a more accurate static summary."
        
        # Case 2: Standard AI Synthesis
        else:
            await self._emit(AgentEvent.PRE_SYNTHESIS, report)
            
            content = []
            reasoning = []
            client = self.llm_client
            if client is None:
                logger.error("LLM client not initialized for synthesis")
                return report

            async for chunk_info in client.stream_analysis(report["ai_prompt"]):
                chunk = chunk_info.get("content")
                if chunk is None:
                    continue  # Skip empty/None chunks
                if chunk_info.get("type") == "reasoning":
                    reasoning.append(chunk)
                    await self._emit(AgentEvent.REASONING_CHUNK, {"chunk": chunk})
                else:
                    content.append(chunk)
                    await self._emit(AgentEvent.SYNTHESIS_CHUNK, {"chunk": chunk})
            
            report["ai_synthesis"] = "".join(content)
            report["ai_reasoning"] = "".join(reasoning)
            report["synthesis_performed"] = True

        logger.info("Synthesis complete.")
        return report
