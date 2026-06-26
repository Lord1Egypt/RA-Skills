import json
from pathlib import Path
from typing import Dict, List, Any, Optional

class ContextBuilder:
    """Builds the context prompt for the AI engine."""

    def build_prompt(self, metrics: dict, issues: list, ghosts: list, flags: list, coupling_metrics: dict, import_edges: list, patch: bool = False, symbol_index: str = "") -> str:
        """
        Formats analysis data into an XML-tagged prompt for LLMs.
        """
        prompt = "Analyze the following codebase architecture and provide a 'Vibe Synthesis' report. "
        prompt += "Focus on system-level flow, cohesion, and tech stack best practices.\n\n"

        if patch:
            prompt += "IMPORTANT: The user has requested a REFACTOR PLAN. "
            prompt += "In addition to your synthesis, provide specific, actionable refactoring blueprints. "
            prompt += "If possible, output code snippets or 'Unified Diff' style patches for critical architectural fixes.\n\n"

        prompt += "<metrics>\n"
        prompt += json.dumps(metrics, indent=2) + "\n"
        prompt += "</metrics>\n\n"

        if issues:
            prompt += "<issues>\n"
            for issue in issues:
                prompt += f"- {issue}\n"
            prompt += "</issues>\n\n"

        if ghosts:
            prompt += "<ghosts>\n"
            for ghost in ghosts:
                prompt += f"- {ghost}\n"
            prompt += "</ghosts>\n\n"

        if flags:
            prompt += "<flags>\n"
            for flag in flags:
                prompt += f"- {flag}\n"
            prompt += "</flags>\n\n"

        if coupling_metrics:
            prompt += "<coupling_metrics>\n"
            prompt += json.dumps(coupling_metrics, indent=2) + "\n"
            prompt += "</coupling_metrics>\n\n"

        if import_edges:
            prompt += "<import_edges>\n"
            # Simplify import edges to avoid massive tokens
            for edge in import_edges:
                prompt += f"{edge[0]} -> {edge[1]}\n"
            prompt += "</import_edges>\n\n"

        if symbol_index:
            prompt += "<symbols>\n"
            prompt += symbol_index + "\n"
            prompt += "</symbols>\n\n"

        prompt += "Return your synthesis as a structured Markdown document."
        return prompt

    def build_delta_prompt(self, current_metrics: dict, current_issues: list, current_ghosts: list, current_flags: list, diff_text: str, base_report: Optional[dict] = None) -> str:
        """
        Build a delta-context prompt for PR-style analysis.
        Compares current changes against a base architectural state.

        Args:
            current_metrics: Metrics from the current (changed) analysis
            current_issues: Issues detected in the current changes
            current_ghosts: Architectural ghosts in current changes
            current_flags: Red flags in current changes
            diff_text: Unified diff string from git_utils
            base_report: Previous full analysis report (dict) to use as baseline

        Returns:
            Prompt string for LLM delta synthesis
        """
        prompt = "You are performing a Delta-Context Architectural Analysis.\n\n"
        prompt += "GOAL: Analyze the *changes* (git diff) and assess how they impact the overall architecture.\n"
        prompt += "Focus on: architectural drift, improvements, new smells, or resolutions of prior issues.\n\n"

        # Base context (if available)
        if base_report:
            prompt += "<base_context>\n"
            prompt += f"Base Vibe Score: {base_report.get('vibe_score', 'N/A')}/100\n"
            base_issues = base_report.get('issues', [])
            base_ghosts = base_report.get('architectural_ghosts', [])
            if base_issues:
                prompt += "Prior Issues:\n"
                for issue in base_issues[:10]:  # limit to avoid token bloat
                    prompt += f"- {issue}\n"
            if base_ghosts:
                prompt += "Prior Ghosts:\n"
                for ghost in base_ghosts[:10]:
                    prompt += f"- {ghost}\n"
            prompt += "</base_context>\n\n"

        # Current diff
        prompt += "<diff>\n"
        prompt += diff_text
        prompt += "\n</diff>\n\n"

        # Current state (focused on changed files)
        prompt += "<current_state>\n"
        prompt += "Metrics (changed files only):\n"
        prompt += json.dumps(current_metrics, indent=2) + "\n\n"
        if current_issues:
            prompt += "Current Issues:\n"
            for issue in current_issues:
                prompt += f"- {issue}\n"
            prompt += "\n"
        if current_ghosts:
            prompt += "Current Ghosts:\n"
            for ghost in current_ghosts:
                prompt += f"- {ghost}\n"
            prompt += "\n"
        if current_flags:
            prompt += "Current Flags:\n"
            for flag in current_flags:
                prompt += f"- {flag}\n"
        prompt += "</current_state>\n\n"

        prompt += "TASK:\n"
        prompt += "1. Compare the diff against the base context. Identify architectural drift or alignment.\n"
        prompt += "2. Are new ghosts introduced? Are prior ghosts resolved?\n"
        prompt += "3. Does the change improve or degrade the overall vibe score? Why?\n"
        prompt += "4. Provide specific recommendations for the changed code.\n"
        prompt += "5. If the delta reveals serious concerns, suggest rollback or mitigation.\n\n"
        prompt += "Return your synthesis as a structured Markdown document with sections: Summary, Changes Analysis, Architectural Impact, Recommendations."

        return prompt
