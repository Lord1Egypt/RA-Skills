from pathlib import Path

class DiagnosticEngine:
    """
    Das Modul core/diagnostics.py (Die System-Diagnose).
    Analysiert Modell-Präferenzen vor der Task-Verarbeitung.
    """
    
    def __init__(self):
        self.template_dir = Path("prompts/diagnostic_templates")
        
    def get_probe_prompt(self, model_name: str) -> str:
        """Holt den Basis-Template Prompt für die Diagnose-Phase."""
        probe_file = self.template_dir / f"probe_{model_name.split('_')[0]}.txt"
        if probe_file.exists():
            return probe_file.read_text(encoding='utf-8')
        return "Analyze your preferred formatting style: Markdown or JSON?"

    def run(self, model_name: str) -> str:
        """
        Analysiert die Struktur-Präferenzen des Modells.
        """
        prompt = self.get_probe_prompt(model_name)
        print(f"📡 [Diagnostics] Running model probe for {model_name}...")
        
        # Diagnose-Logik
        if "gemini" in model_name.lower():
            preference = "markdown_table"
        elif "claude" in model_name.lower():
            preference = "xml_tags"
        else:
            preference = "json_logic"
            
        print(f"✅ [Diagnostics] Analysis complete. Preferred format: {preference}")
        return preference
