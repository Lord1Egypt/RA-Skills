import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from src.core.rag import RAGEngine
from src.utils.logger import logger
from src.utils.paths import format_path, WorkspaceManager

class RAGWatchdogHandler(FileSystemEventHandler):
    """Handles file system events and updates the RAG index."""
    
    def __init__(self, rag: RAGEngine, project_root: Path):
        self.rag = rag
        self.project_root = project_root
        super().__init__()

    def _is_valid_file(self, path_str: str) -> bool:
        path = Path(path_str)
        if not path.is_file():
            return False
            
        # Basic filtering (can be expanded to match RAGEngine's index_directory logic)
        skip_dirs = {
            '.git', '__pycache__', 'node_modules', '.venv', 'venv', 'env',
            '.cxm', 'knowledge-base', 'build', 'dist', '.pytest_cache'
        }
        if any(part in skip_dirs for part in path.parts):
            return False
            
        skip_exts = {
            '.pyc', '.pyo', '.pyd', '.so', '.dll', '.exe', '.zip', '.tar', '.gz',
            '.jpg', '.png', '.pdf', '.lock'
        }
        if path.suffix.lower() in skip_exts:
            return False
            
        return True

    def on_modified(self, event):
        if not event.is_directory and self._is_valid_file(event.src_path):
            logger.info(f"File modified: {event.src_path}")
            # Try to index. RAGEngine checks hash, so it only re-indexes if actually changed.
            self.rag.index_file(Path(event.src_path), force=True)
            self.rag.save()

    def on_created(self, event):
        if not event.is_directory and self._is_valid_file(event.src_path):
            logger.info(f"File created: {event.src_path}")
            self.rag.index_file(Path(event.src_path))
            self.rag.save()

    def on_deleted(self, event):
        if not event.is_directory:
            logger.info(f"File deleted: {event.src_path}")
            self.rag._remove_file_chunks(Path(event.src_path))
            self.rag.save()

def start_watcher(project_name: str = None, github_url: str = None):
    """Starts the background watcher daemon."""
    workspace = WorkspaceManager.get_index_dir(project_name, github_url)
    rag = RAGEngine(workspace)
    
    project_root = Path.cwd()
    if github_url:
        from src.tools.github_cloner import clone_github_repo
        project_root = clone_github_repo(github_url)
        
    handler = RAGWatchdogHandler(rag, project_root)
    observer = Observer()
    observer.schedule(handler, str(project_root), recursive=True)
    
    logger.info(f"Starting CXM Watcher for: {project_root}")
    print(f"👀 Watching {project_root} for changes... (Press Ctrl+C to stop)")
    
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\nStopping Watcher...")
    
    observer.join()
