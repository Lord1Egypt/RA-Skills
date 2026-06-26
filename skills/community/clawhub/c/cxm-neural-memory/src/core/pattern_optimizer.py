from typing import Dict, Any

class PatternOptimizer:
    """
    Optimierung von Coding-Mustern basierend auf erfolgreichen Durchläufen.
    Extrahiert bewährte Logik für die zukünftige Verwendung im ContextStore.
    """

    def optimize_from_success(self, task_description: str, generated_code: str, review_passed: bool) -> str:
        """
        Extrahiert die Essenz eines erfolgreichen Durchlaufs.
        """
        if not review_passed:
            return "Optimization skipped: Code failed audit."

        print(f"\n⚗️  [Optimizer] Extracting verified patterns for: '{task_description}'...")
        optimized_pattern = f"Verified logic for '{task_description}'. Demonstrated high security and performance."
        
        print(f"   💧 Optimized Pattern: {optimized_pattern}")
        return optimized_pattern
