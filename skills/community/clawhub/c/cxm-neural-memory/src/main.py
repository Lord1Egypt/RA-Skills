import sys
from pathlib import Path

# Add src to path for direct execution
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.core.context_store import ContextStore
from src.core.diagnostics import DiagnosticEngine
from src.core.factory import Factory
from src.core.audit import MultiAgentAudit
from src.core.pattern_optimizer import PatternOptimizer
from src.core.patcher import FilePatcher
from src.core.architect import ArchitectAgent
from rich.console import Console
from rich.prompt import Confirm

console = Console()

def simulate_scaffold_generation() -> str:
    """Mock function simulating the shadow-scaffolding generation."""
    print("\n⏳ [LLM] Generating shadow scaffolding (Interface-First)...")
    return """
<file_patch path="src/core/cache_interface.py">
```python
from abc import ABC, abstractmethod

class CacheInterface(ABC):
    @abstractmethod
    def get(self, key: str):
        pass
        
    @abstractmethod
    def set(self, key: str, value: any, ttl: int = 3600):
        pass
```
</file_patch>
"""

def simulate_llm_generation(prompt: str) -> str:
    """Mock function simulating an autonomous LLM response with file patches."""
    print("\n⏳ [LLM] Autonomously generating code based on vibe and scaffold...")
    return """
<file_patch path="src/api/middleware.py">
```python
from src.core.cache_interface import CacheInterface

class RateLimiter:
    def __init__(self, cache: CacheInterface):
        self.cache = cache
        
    def check_limit(self, user_id: str) -> bool:
        # Implementation strictly relies on the abstract CacheInterface
        hits = self.cache.get(user_id)
        if hits and hits > 100:
            return False
        self.cache.set(user_id, (hits or 0) + 1)
        return True
```
</file_patch>
"""

def run_orchestration_loop(user_intent: str, target_model: str, project_name: str, pattern_name: str = None):
    """
    Main Orchestration Loop for Telepathic Vibe-to-Code Generation.
    """
    print("="*60)
    print(f"⚙️  RUNNING TELEPATHIC FORGE: {target_model} | PROJECT: {project_name}")
    print("="*60)

    # 1. Initialize Components
    store = ContextStore()
    diagnostics = DiagnosticEngine()
    factory = Factory()
    audit_engine = MultiAgentAudit()
    optimizer = PatternOptimizer()
    patcher = FilePatcher()
    architect = ArchitectAgent()

    # --- Setup professional context data ---
    store.set_project_var(project_name, "STABILITY_THRESHOLD", "0.95")
    store.set_project_var(project_name, "PRIMARY_RATIO", "1:500")
    store.set_project_var(project_name, "MAX_TEMP_CELSIUS", "32.0")
    
    context_vars = store.get_project_vars(project_name)

    # 2. Phase 0: The Architect (Implicit Gap Inference)
    print("\n[Step 0] The Telepathic Planner (Implicit Gap Inference)...")
    plan = architect.plan_refactoring(user_intent, context_vars)
    
    # 3. Phase 1: The Alignment Vibe-Check
    if plan.get("requires_vibe_check"):
        console.print(f"\n[bold yellow]⚠️  ALIGNMENT VIBE-CHECK[/bold yellow]")
        console.print(f"[dim]Implicit Gap Detected:[/dim] {plan['implicit_gap']}")
        
        console.print("\n[bold]Proposed Multi-Step TaskGraph:[/bold]")
        for i, task in enumerate(plan["sub_tasks"], 1):
            console.print(f"  {i}. {task}")
            
        console.print("\n[bold cyan]Shadow Scaffolding Plan:[/bold cyan]")
        for scaffold in plan["shadow_scaffolding"]:
            console.print(f"  📄 [cyan]{scaffold['path']}[/cyan]: {scaffold['description']}")
            
        if not Confirm.ask("\nProceed with this Telepathic Plan?", default=True):
            print("Aborted by user.")
            return
            
        print("\n[Step 0.5] Applying Shadow Scaffolding...")
        scaffold_code = simulate_scaffold_generation()
        patcher.parse_and_apply(scaffold_code)

    # 4. Identify & Probe
    print("\n[Step 1] Running Diagnostics...")
    preferred_format = diagnostics.run(target_model)
    
    # 3. Fetch Data
    print("\n[Step 2] Fetching Context...")
    context_vars = store.get_project_vars(project_name)

    # 4. Synthesize Secure Prompt & Auto-Route Vibe
    print("\n[Step 3] Routing Vibe & Compiling Secure Prompt...")
    final_prompt = factory.assemble_secure(
        user_query=user_intent,
        pattern_name=pattern_name,
        vault_vars=context_vars,
        engine_name=target_model
    )
    
    print("\n🛡️  COMPILED AUTONOMOUS PROMPT 🛡️")
    print("-" * 50)
    print(final_prompt)
    print("-" * 50)

    # 5. Generate Code (Simulated)
    generated_code = simulate_llm_generation(final_prompt)
    print(generated_code)

    # 6. Multi-Agent Audit
    audit_passed = audit_engine.review_code(generated_code, ["Must use safe logic"])

    # 7. Apply Patches (If Audit passed)
    if audit_passed:
        print("\n[Step 4] Applying Code Patches (with Guardrails)...")
        patcher.parse_and_apply(generated_code)
    else:
        print("\n[Step 4] ❌ Patching aborted due to failed Audit.")

    # 8. Pattern Optimization
    optimizer.optimize_from_success(user_intent, generated_code, audit_passed)

if __name__ == "__main__":
    # Vibecoding Test: Notice we do NOT pass a pattern_name!
    # The Telepathic Planner will infer we need Rate-Limiting and a Cache Interface.
    run_orchestration_loop(
        user_intent="I want to add rate limiting to our API endpoints to prevent abuse.", 
        target_model="gemini_pro", 
        project_name="ProductionSystem"
    )
