"""Workspace Manager for Symphony

Manages isolated per-build workspaces with lifecycle hooks.
Based on OpenAI's Symphony workspace management pattern.
"""

import logging
import shutil
import subprocess
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Callable, Dict, List, Optional

logger = logging.getLogger('builder-agent.symphony.workspace')


class WorkspaceHook(Enum):
    """Lifecycle hooks for workspace management"""
    AFTER_CREATE = "after_create"
    BEFORE_RUN = "before_run"
    AFTER_RUN = "after_run"
    BEFORE_REMOVE = "before_remove"


@dataclass
class WorkspaceConfig:
    """Configuration for workspace management"""
    base_dir: Path = Path("/tmp/dev-factory-workspaces")
    auto_cleanup: bool = True
    retention_hours: int = 24
    create_git_repo: bool = True
    hooks: Dict[WorkspaceHook, List[str]] = field(default_factory=dict)

    def __post_init__(self):
        if isinstance(self.base_dir, str):
            self.base_dir = Path(self.base_dir)


@dataclass
class Workspace:
    """An isolated workspace for a build task"""
    task_id: str
    path: Path
    created_at: datetime = field(default_factory=datetime.now)
    last_used: Optional[datetime] = None
    size_bytes: int = 0

    def exists(self) -> bool:
        """Check if workspace directory exists"""
        return self.path.exists() and self.path.is_dir()

    def age_hours(self) -> float:
        """Get workspace age in hours"""
        return (datetime.now() - self.created_at).total_seconds() / 3600

    def calculate_size(self) -> int:
        """Calculate workspace size in bytes"""
        if not self.exists():
            return 0

        total = 0
        for item in self.path.rglob('*'):
            if item.is_file():
                total += item.stat().st_size
        self.size_bytes = total
        return total


class WorkspaceManager:
    """Manages isolated per-build workspaces

    Pattern: /tmp/dev-factory-workspaces/{task_id}/

    Features:
    - Automatic cleanup after completion
    - Lifecycle hooks for initialization
    - Size tracking
    - Retention policy enforcement
    """

    def __init__(self, config: Optional[WorkspaceConfig] = None):
        """Initialize workspace manager

        Args:
            config: Workspace configuration
        """
        self.config = config or WorkspaceConfig()
        self.workspaces: Dict[str, Workspace] = {}

        # Ensure base directory exists
        self.config.base_dir.mkdir(parents=True, exist_ok=True)

        logger.info(
            "Workspace manager initialized: base_dir=%s, auto_cleanup=%s",
            self.config.base_dir, self.config.auto_cleanup
        )

    def create_workspace(self, task_id: str, hooks: Optional[Dict[WorkspaceHook, List[str]]] = None) -> Workspace:
        """Create a new isolated workspace

        Args:
            task_id: Task identifier
            hooks: Optional custom hooks for this workspace

        Returns:
            Created workspace
        """
        workspace_path = self.config.base_dir / task_id

        if workspace_path.exists():
            logger.warning("Workspace %s already exists, cleaning up", task_id)
            self.remove_workspace(task_id)

        # Create workspace directory
        workspace_path.mkdir(parents=True, exist_ok=True)

        workspace = Workspace(
            task_id=task_id,
            path=workspace_path,
        )

        # Create git repo if enabled
        if self.config.create_git_repo:
            self._init_git_repo(workspace_path)

        # Run after_create hooks
        self._run_hooks(
            workspace,
            WorkspaceHook.AFTER_CREATE,
            self.config.hooks.get(WorkspaceHook.AFTER_CREATE, [])
        )
        if hooks:
            self._run_hooks(
                workspace,
                WorkspaceHook.AFTER_CREATE,
                hooks.get(WorkspaceHook.AFTER_CREATE, [])
            )

        self.workspaces[task_id] = workspace
        logger.info("Created workspace for task %s at %s", task_id, workspace_path)

        return workspace

    def get_workspace(self, task_id: str) -> Optional[Workspace]:
        """Get existing workspace

        Args:
            task_id: Task identifier

        Returns:
            Workspace if exists, None otherwise
        """
        return self.workspaces.get(task_id)

    def remove_workspace(self, task_id: str) -> bool:
        """Remove a workspace

        Args:
            task_id: Task identifier

        Returns:
            True if successful, False otherwise
        """
        workspace = self.get_workspace(task_id)
        if not workspace:
            logger.warning("Workspace %s not found", task_id)
            return False

        # Run before_remove hooks
        self._run_hooks(
            workspace,
            WorkspaceHook.BEFORE_REMOVE,
            self.config.hooks.get(WorkspaceHook.BEFORE_REMOVE, [])
        )

        try:
            if workspace.exists():
                shutil.rmtree(workspace.path)
                logger.info("Removed workspace for task %s", task_id)

            del self.workspaces[task_id]
            return True

        except Exception as e:
            logger.error("Failed to remove workspace %s: %s", task_id, e)
            return False

    def cleanup_old_workspaces(self, older_than_hours: Optional[int] = None) -> int:
        """Remove workspaces older than specified hours

        Args:
            older_than_hours: Age threshold (uses config default if not specified)

        Returns:
            Number of workspaces removed
        """
        threshold = older_than_hours or self.config.retention_hours
        cutoff = datetime.now() - timedelta(hours=threshold)

        to_remove = [
            task_id for task_id, ws in self.workspaces.items()
            if ws.created_at < cutoff
        ]

        for task_id in to_remove:
            self.remove_workspace(task_id)

        logger.info("Cleaned up %d old workspaces (older than %d hours)",
                    len(to_remove), threshold)
        return len(to_remove)

    def cleanup_all_workspaces(self) -> int:
        """Remove all workspaces

        Returns:
            Number of workspaces removed
        """
        count = len(self.workspaces)
        for task_id in list(self.workspaces.keys()):
            self.remove_workspace(task_id)

        logger.info("Cleaned up all %d workspaces", count)
        return count

    def before_run(self, task_id: str) -> bool:
        """Run hooks before task execution

        Args:
            task_id: Task identifier

        Returns:
            True if successful, False otherwise
        """
        workspace = self.get_workspace(task_id)
        if not workspace:
            logger.warning("Workspace %s not found for before_run", task_id)
            return False

        hooks = self.config.hooks.get(WorkspaceHook.BEFORE_RUN, [])
        return self._run_hooks(workspace, WorkspaceHook.BEFORE_RUN, hooks)

    def after_run(self, task_id: str) -> bool:
        """Run hooks after task execution

        Args:
            task_id: Task identifier

        Returns:
            True if successful, False otherwise
        """
        workspace = self.get_workspace(task_id)
        if not workspace:
            logger.warning("Workspace %s not found for after_run", task_id)
            return False

        hooks = self.config.hooks.get(WorkspaceHook.AFTER_RUN, [])
        success = self._run_hooks(workspace, WorkspaceHook.AFTER_RUN, hooks)

        # Update last used time
        workspace.last_used = datetime.now()

        return success

    def get_workspace_size(self, task_id: str) -> int:
        """Get workspace size in bytes

        Args:
            task_id: Task identifier

        Returns:
            Size in bytes
        """
        workspace = self.get_workspace(task_id)
        if not workspace:
            return 0

        return workspace.calculate_size()

    def get_total_size(self) -> int:
        """Get total size of all workspaces in bytes

        Returns:
            Total size in bytes
        """
        total = 0
        for workspace in self.workspaces.values():
            total += workspace.calculate_size()
        return total

    def get_statistics(self) -> Dict:
        """Get workspace statistics

        Returns:
            Dictionary with statistics
        """
        total_size = self.get_total_size()

        return {
            'total_workspaces': len(self.workspaces),
            'total_size_bytes': total_size,
            'total_size_mb': round(total_size / (1024 * 1024), 2),
            'base_dir': str(self.config.base_dir),
            'auto_cleanup': self.config.auto_cleanup,
            'retention_hours': self.config.retention_hours,
        }

    def _init_git_repo(self, path: Path) -> bool:
        """Initialize a git repository in the workspace

        Args:
            path: Workspace path

        Returns:
            True if successful, False otherwise
        """
        try:
            subprocess.run(
                ['git', 'init'],
                cwd=str(path),
                capture_output=True,
                timeout=10,
                check=True
            )

            # Create .gitignore
            gitignore = path / ".gitignore"
            gitignore.write_text("""# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
env/
ENV/
.venv

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db
""")

            logger.debug("Initialized git repo in %s", path)
            return True

        except Exception as e:
            logger.warning("Failed to initialize git repo in %s: %s", path, e)
            return False

    def _run_hooks(self, workspace: Workspace, hook: WorkspaceHook,
                   commands: List[str]) -> bool:
        """Run lifecycle hooks

        Args:
            workspace: Workspace to run hooks in
            hook: Hook type
            commands: List of commands to run

        Returns:
            True if all hooks succeeded, False otherwise
        """
        if not commands:
            return True

        all_success = True

        for cmd in commands:
            try:
                logger.info("Running %s hook: %s", hook.value, cmd)

                result = subprocess.run(
                    cmd,
                    shell=True,
                    cwd=str(workspace.path),
                    capture_output=True,
                    text=True,
                    timeout=60
                )

                if result.returncode != 0:
                    logger.warning(
                        "Hook %s failed: %s\nstderr: %s",
                        hook.value, cmd, result.stderr
                    )
                    all_success = False
                else:
                    logger.debug("Hook %s succeeded: %s", hook.value, cmd)

            except subprocess.TimeoutExpired:
                logger.warning("Hook %s timed out: %s", hook.value, cmd)
                all_success = False
            except Exception as e:
                logger.error("Hook %s error: %s: %s", hook.value, cmd, e)
                all_success = False

        return all_success


class WorkspaceFactory:
    """Factory for creating workspace managers with different configurations"""

    @staticmethod
    def create_default() -> WorkspaceManager:
        """Create workspace manager with default configuration"""
        return WorkspaceManager(WorkspaceConfig())

    @staticmethod
    def create_with_cleanup(base_dir: Path, retention_hours: int = 24) -> WorkspaceManager:
        """Create workspace manager with custom cleanup policy"""
        return WorkspaceManager(WorkspaceConfig(
            base_dir=base_dir,
            auto_cleanup=True,
            retention_hours=retention_hours
        ))

    @staticmethod
    def create_with_hooks(base_dir: Path, hooks: Dict[WorkspaceHook, List[str]]) -> WorkspaceManager:
        """Create workspace manager with custom hooks"""
        return WorkspaceManager(WorkspaceConfig(
            base_dir=base_dir,
            hooks=hooks
        ))
