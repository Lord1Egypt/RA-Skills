import subprocess
import os
import hashlib
import re
from pathlib import Path
from urllib.parse import urlparse
from rich.console import Console

console = Console()

def is_valid_github_url(url: str) -> bool:
    """Basic validation for GitHub HTTPS URLs"""
    parsed = urlparse(url)
    if parsed.scheme != "https" or parsed.netloc != "github.com":
        return False
    # Simple regex for /user/repo
    return bool(re.match(r'^/[a-zA-Z0-9._-]+/[a-zA-Z0-9._-]+(\.git)?$', parsed.path))

def clone_github_repo(repo_url: str) -> Path:
    """
    Clones a GitHub repository into ~/.cxm/cache/ and returns the path.
    Safe version with URL validation and path sanitization.
    """
    if not is_valid_github_url(repo_url):
        raise ValueError(f"Ungültige GitHub-URL: {repo_url}. Nur HTTPS-URLs von github.com sind erlaubt.")

    # Create a unique directory name based on the URL
    url_hash = hashlib.md5(repo_url.encode()).hexdigest()[:10]
    
    # Sanitize repo name from URL to prevent traversal
    path_parts = urlparse(repo_url).path.strip('/').split('/')
    repo_name = re.sub(r'[^a-zA-Z0-9._-]', '_', path_parts[-1].replace('.git', ''))
    
    cache_base = Path.home() / ".cxm" / "cache"
    cache_dir = (cache_base / f"{repo_name}_{url_hash}").resolve()
    
    # Safety check: Ensure the resolved path is still under cache_base
    if not str(cache_dir).startswith(str(cache_base.resolve())):
        raise ValueError("Sicherheitsrisiko: Pfad-Manipulation in der Repository-URL erkannt.")

    cache_dir.parent.mkdir(parents=True, exist_ok=True)
    
    if cache_dir.exists():
        console.print(f"[dim]Repository bereits im Cache gefunden. Aktualisiere...[/dim]")
        try:
            # Use subprocess with list for security
            subprocess.run(["git", "-C", str(cache_dir), "pull"], check=True, capture_output=True, text=True)
        except Exception as e:
            console.print(f"[yellow]Warnung: Konnte Repo nicht aktualisieren: {e}[/yellow]")
    else:
        console.print(f"📦 [cyan]Klone Repository:[/cyan] {repo_url}...")
        try:
            # depth 1 for performance, list for security
            subprocess.run(["git", "clone", "--depth", "1", repo_url, str(cache_dir)], check=True, capture_output=True, text=True)
            console.print(f"✓ Repository erfolgreich in den Cache geladen.")
        except Exception as e:
            console.print(f"[bold red]Fehler beim Klonen:[/bold red] {e}")
            raise e
            
    return cache_dir
