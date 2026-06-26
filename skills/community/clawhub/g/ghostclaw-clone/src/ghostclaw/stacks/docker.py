"""Docker stack analyzer for infrastructure hygiene."""

from typing import Dict, List
from .base import StackAnalyzer


class DockerAnalyzer(StackAnalyzer):
    """Analyzes Docker projects for architectural and hygiene issues."""

    def get_extensions(self) -> List[str]:
        # Return generic names that are often in Docker projects
        return ['Dockerfile', 'docker-compose.yml', 'compose.yaml', '.dockerignore']

    def get_large_file_threshold(self) -> int:
        # Dockerfiles should be small; 100 lines is quite a lot for a single file
        return 100

    def analyze(self, root: str, files: List[str], metrics: Dict) -> Dict:
        """Analyze Docker configuration for common patterns."""
        issues = []
        ghosts = []
        flags = []

        # Find specific files to report in metadata
        dockerfiles = [f for f in files if 'Dockerfile' in f]
        compose_files = [f for f in files if 'compose' in f.lower() and (f.endswith('.yml') or f.endswith('.yaml'))]

        if not dockerfiles and not compose_files:
            issues.append("No active Dockerfile or Compose file found in analysis set")

        return {
            "stack": "docker",
            "issues": issues,
            "architectural_ghosts": ghosts,
            "red_flags": flags,
            "docker_stats": {
                "dockerfile_count": len(dockerfiles),
                "compose_file_count": len(compose_files)
            }
        }
