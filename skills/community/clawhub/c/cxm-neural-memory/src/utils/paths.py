import os
import hashlib
from pathlib import Path

def format_path(path_str: str) -> str:
    """
    Format path to be relative to the parent of the current working directory 
    to include the project folder name (e.g. partner/src/...).
    Falls der Pfad außerhalb des Projekts liegt, wird er relativ zum Home-Verzeichnis (if possible) angezeigt.
    """
    try:
        abs_path = Path(path_str).resolve()
        cwd = Path.cwd()
        
        # Versuche Pfad relativ zum Parent des CWD zu machen (inkludiert Projektname)
        try:
            rel_path = os.path.relpath(abs_path, cwd.parent)
            if not rel_path.startswith(".."):
                return rel_path
        except ValueError:
            pass

        # Fallback: Relativ zum Home-Verzeichnis (~/...)
        home = Path.home()
        try:
            if abs_path.is_relative_to(home):
                return "~/" + str(abs_path.relative_to(home))
        except (ValueError, AttributeError):
            pass
            
        return str(abs_path)
    except Exception:
        return str(path_str)

class WorkspaceManager:
    """
    Centralized manager for all file paths, indices, and prompts.
    Eliminates redundancy and ensures a single source of truth.
    """
    @staticmethod
    def get_index_dir(project_name: str = None, github_url: str = None) -> Path:
        """Determines the exact folder where the RAG index (knowledge base) is stored."""
        
        # 1. GitHub Temporary Cache
        if github_url:
            url_hash = hashlib.md5(github_url.encode()).hexdigest()[:10]
            repo_name = github_url.split('/')[-1].replace('.git', '')
            kb_path = Path.home() / ".cxm" / "cache" / f"{repo_name}_{url_hash}" / "knowledge-base"
            kb_path.mkdir(parents=True, exist_ok=True)
            return kb_path

        # 2. Named Project (Global Context)
        if project_name:
            kb_path = Path.home() / ".cxm" / project_name / "knowledge-base"
            kb_path.mkdir(parents=True, exist_ok=True)
            return kb_path

        # 3. Local Project (Inside current working directory)
        local_kb = Path.cwd() / "knowledge-base"
        if local_kb.exists() or Path.cwd().name == "meta-orchestrator":
            local_kb.mkdir(parents=True, exist_ok=True)
            return local_kb
            
        # 4. Fallback: Global Default
        from config import Config
        kb_path = Path(Config().get('workspace'))
        kb_path.mkdir(parents=True, exist_ok=True)
        return kb_path

    @staticmethod
    def get_prompt_output_file() -> Path:
        """Determines where the final, enhanced prompt is written."""
        # Always output to one standard location to prevent clutter
        output_file = Path.home() / ".cxm" / "current_task_prompt.txt"
        output_file.parent.mkdir(parents=True, exist_ok=True)
        return output_file

