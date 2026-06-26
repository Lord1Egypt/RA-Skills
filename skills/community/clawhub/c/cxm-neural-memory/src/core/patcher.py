import re
import yaml
from pathlib import Path
from rich.console import Console
from rich.prompt import Confirm

console = Console()

class GuardrailManager:
    """Manages project-specific security rules from .cxm.yaml"""
    def __init__(self, project_root: Path = None):
        self.root = project_root or Path.cwd()
        self.config_path = self.root / ".cxm.yaml"
        self.config = self._load_config()

    def _load_config(self) -> dict:
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    return yaml.safe_load(f) or {}
            except Exception as e:
                console.print(f"[bold red]Error loading .cxm.yaml: {e}[/bold red]")
        return {}

    def is_path_allowed_for_write(self, target_path: str) -> bool:
        """Checks if the target path is within the allowed_write_paths"""
        patching_config = self.config.get("patching", {})
        allowed_paths = patching_config.get("allowed_write_paths", [])
        
        # If no explicit limits, allow all (or default to safe mode depending on policy)
        if not allowed_paths:
            return True
            
        target = Path(target_path)
        for allowed in allowed_paths:
            # Check if target is relative to an allowed path
            try:
                if target.is_relative_to(Path(allowed)):
                    return True
            except AttributeError:
                # Fallback for Python < 3.9
                if str(target).startswith(str(Path(allowed))):
                    return True
        return False

    def get_patch_mode(self) -> str:
        """Returns 'true', 'ask_first', or 'false'"""
        return self.config.get("patching", {}).get("mode", "ask_first")

class FilePatcher:
    """Parses LLM output and applies file patches safely using Guardrails."""
    
    def __init__(self):
        self.guardrails = GuardrailManager()

    def parse_and_apply(self, llm_output: str):
        """Finds <file_patch path="..."> blocks and applies them based on rules."""
        
        # Find all patch blocks: <file_patch path="some/path.py">...code...</file_patch>
        pattern = r'<file_patch\s+path="([^"]+)">\s*```(?:python|py|js|ts|[\w]+)?\n(.*?)```\s*</file_patch>'
        matches = re.finditer(pattern, llm_output, re.DOTALL)
        
        patches_found = False
        mode = self.guardrails.get_patch_mode()

        if mode == "false":
            console.print("\n[yellow]🛡️ Auto-patching is disabled in .cxm.yaml (dry-run only).[/yellow]")

        for match in matches:
            patches_found = True
            file_path = match.group(1).strip()
            code_content = match.group(2).strip()
            
            console.print(f"\n[bold cyan]📦 Discovered Patch for:[/bold cyan] {file_path}")
            
            # Security Check
            if not self.guardrails.is_path_allowed_for_write(file_path):
                console.print(f"   [bold red]❌ BLOCKED:[/bold red] Path '{file_path}' is outside allowed_write_paths in .cxm.yaml.")
                continue
                
            if mode == "false":
                console.print("   [dim]File would be updated with new code...[/dim]")
                continue
                
            # Apply Logic
            target_file = Path.cwd() / file_path
            
            if mode == "ask_first":
                # Preview snippet
                preview = code_content[:200] + ("..." if len(code_content) > 200 else "")
                console.print(f"[dim]Preview:\n{preview}[/dim]")
                
                if not Confirm.ask(f"Do you want CXM to automatically write to {file_path}?", default=True):
                    console.print("   [yellow]⏭️ Skipped by user.[/yellow]")
                    continue
            
            # Actually write the file
            try:
                target_file.parent.mkdir(parents=True, exist_ok=True)
                target_file.write_text(code_content, encoding='utf-8')
                console.print(f"   [bold green]✅ SUCCESSFULLY WRITTEN:[/bold green] {file_path}")
            except Exception as e:
                console.print(f"   [bold red]❌ Failed to write file: {e}[/bold red]")

        if not patches_found:
            console.print("\n[dim]No <file_patch> blocks found in LLM output.[/dim]")
