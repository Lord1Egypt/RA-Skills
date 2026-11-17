#!/usr/bin/env python3
"""
OpenClaw Gateway Hook Middleware.
Passively intercepts messages and tasks processed by OpenClaw to automatically
feed the telemetry engine and transparently route tasks to specialized sub-agents.
"""

import time
import os
import sys
from typing import Dict, Any, Callable, Optional

SCRIPTS_DIR = os.path.dirname(__file__)
sys.path.insert(0, SCRIPTS_DIR)

from telemetry import log_task, analyze_clusters
from router import route_and_execute
from llm_engine import call_llm


class OpenClawMiddleware:
    """
    Hook to attach to the OpenClaw Gateway or Agent pipeline.
    Usage:
        middleware = OpenClawMiddleware()
        response = middleware.handle_incoming_task("Extract VAT from invoice #102")
    """
    def __init__(self, auto_trigger_threshold: float = 50.0):
        self.auto_trigger_threshold = auto_trigger_threshold

    def handle_incoming_task(self, prompt: str, domain_hint: str = "general") -> Dict[str, Any]:
        start_time = time.time()
        
        # 1. Check Routing Decision (Semantic Cache -> Specialized Sub-Agent -> Generalist)
        route_decision = route_and_execute(prompt)
        source = route_decision["source"]

        # 2. Execute Task
        if source == "SEMANTIC_CACHE":
            response_output = route_decision["result"]
            tokens_in = 0
            tokens_out = 0
            error_occurred = False
        elif source == "SPECIALIZED_SUBAGENT":
            system_prompt = route_decision.get("system_prompt", "Specialized Sub-Agent.")
            llm_res = call_llm(prompt, system_prompt)
            response_output = llm_res["output"]
            tokens_in = llm_res["tokens_in"]
            tokens_out = llm_res["tokens_out"]
            error_occurred = (llm_res.get("status") != "success")
        else:
            # Generalist Fallback
            llm_res = call_llm(prompt, "You are the generalist OpenClaw orchestrator.")
            response_output = llm_res["output"]
            tokens_in = llm_res["tokens_in"]
            tokens_out = llm_res["tokens_out"]
            error_occurred = (llm_res.get("status") != "success")

        latency_ms = round((time.time() - start_time) * 1000, 1)

        # 3. Transparently Log Real Telemetry
        task_id = f"task_{int(time.time()*1000)}"
        log_task(
            task_id=task_id,
            prompt=prompt,
            domain_tag=route_decision.get("domain", domain_hint),
            tokens_in=tokens_in,
            tokens_out=tokens_out,
            latency_ms=latency_ms,
            error_occurred=error_occurred,
            human_corrected=False,
            tools_used=route_decision.get("allowed_tools", [])
        )

        return {
            "task_id": task_id,
            "routing_source": source,
            "response": response_output,
            "tokens_consumed": tokens_in + tokens_out,
            "latency_ms": latency_ms,
            "routed_agent": route_decision.get("agent_id", "orchestrator_generalist")
        }


if __name__ == "__main__":
    mw = OpenClawMiddleware()
    res = mw.handle_incoming_task("Hello OpenClaw, please organize this document.")
    print("Middleware Interception Result:", res)
