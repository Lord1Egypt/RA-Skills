"""MCP Server for diskman."""

import os
from typing import Any

from fastmcp import FastMCP

from ..ai import AIConfig, AIService
from ..analysis import DirectoryAnalyzer
from ..operations import DirectoryCleaner, DirectoryMigrator, DirectoryScanner


def create_mcp_server(ai_config: AIConfig | None = None) -> FastMCP:
    """Create and configure MCP server.
    
    Args:
        ai_config: AI configuration (optional, defaults to environment variables)
    """

    # Initialize components
    mcp = FastMCP("diskman")
    scanner = DirectoryScanner()
    migrator = DirectoryMigrator()
    cleaner = DirectoryCleaner()
    analyzer = DirectoryAnalyzer()
    
    # AI Service - 支持参数传入或环境变量
    if ai_config is None:
        ai_config = AIConfig(
            api_key=os.getenv("AI_API_KEY") or os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("AI_BASE_URL") or os.getenv("OPENAI_BASE_URL") or "https://api.openai.com",
            model=os.getenv("AI_MODEL") or os.getenv("OPENAI_MODEL") or "gpt-4o-mini",
        )
    ai_service = AIService(ai_config)

    # === Local Tools (No external dependencies) ===

    @mcp.tool()
    def scan_directory(path: str) -> dict[str, Any]:
        """
        Scan a single directory and return size and link status.

        Args:
            path: Directory path to scan

        Returns:
            Directory information including size and link type
        """
        info = scanner.scan_directory(path)
        return info.to_dict()

    @mcp.tool()
    def scan_user_profile(
        base_path: str | None = None,
        depth: int = 3,
    ) -> dict[str, Any]:
        """
        Scan user profile directory for all subdirectories.

        Args:
            base_path: Base path to scan (default: user home)
            depth: Scan depth (1-3)

        Returns:
            Scan results with all directories found
        """
        result = scanner.scan_user_profile(base_path, depth)
        return result.to_dict()

    @mcp.tool()
    def check_link_status(path: str) -> dict[str, Any]:
        """
        Check if a path is a symbolic link, junction, or normal directory.

        Args:
            path: Path to check

        Returns:
            Link type and target if applicable
        """
        link_type, target = scanner.check_link_type(path)
        return {
            "path": path,
            "link_type": link_type.value,
            "target": target,
        }

    @mcp.tool()
    def analyze_directory(
        path: str,
        user_context: str | None = None,
    ) -> dict[str, Any]:
        """
        Analyze a directory and get recommendations.

        Uses built-in rules to determine if a directory can be
        safely deleted, should be moved, or should be kept.

        Args:
            path: Directory path to analyze
            user_context: Optional context (e.g., "Python developer")

        Returns:
            Analysis result with recommendations
        """
        from ..models import AnalysisContext

        # Scan directory
        info = scanner.scan_directory(path)

        # Create context
        context = None
        if user_context:
            context = AnalysisContext(
                user_type="developer" if "developer" in user_context.lower() else None,
            )

        # Analyze
        result = analyzer.analyze(info, context)
        return result.to_dict()

    @mcp.tool()
    def migrate_directory(
        source: str,
        target: str,
    ) -> dict[str, Any]:
        """
        Migrate a directory to another location using symbolic link.

        This operation:
        1. Copies the directory to the target location
        2. Deletes the original directory
        3. Creates a symbolic link from source to target

        WARNING: This modifies the file system. Backup important data first.

        Args:
            source: Source directory path
            target: Target directory path

        Returns:
            Migration result
        """
        result = migrator.migrate(source, target)
        return result.to_dict()

    @mcp.tool()
    def clean_directory(
        path: str,
        dry_run: bool = True,
    ) -> dict[str, Any]:
        """
        Clean a directory.

        Args:
            path: Directory path to clean
            dry_run: If True, only preview what would be deleted

        Returns:
            Clean result with space that would be freed
        """
        result = cleaner.clean(path, dry_run=dry_run)
        return result.to_dict()

    # === Smart Analysis Tool (Auto-switch between AI and Rules) ===

    @mcp.tool()
    async def analyze_directories(
        base_path: str | None = None,
        user_context: str | None = None,
        target_drive: str | None = None,
        prefer_ai: bool = True,
    ) -> dict[str, Any]:
        """
        Scan and analyze directories with auto-switching analysis mode.

        Analysis Mode Selection:
        - AI configured & available + prefer_ai=True → AI-powered analysis
        - No AI config or AI unavailable → Rule-based analysis

        Args:
            base_path: Base path to scan (default: user home)
            user_context: Context about the user (e.g., "Python developer")
            target_drive: Target drive for migration suggestions
            prefer_ai: Prefer AI analysis if available (default: True)

        Returns:
            Analysis results with mode indicator
        """
        # Step 1: Local scan
        scan_result = scanner.scan_user_profile(base_path)
        directories = scan_result.directories[:50]

        # Step 2: Determine analysis mode
        use_ai = prefer_ai and ai_service.available

        if use_ai:
            # AI-powered analysis
            try:
                ai_result = await ai_service.analyze(
                    directories=directories,
                    user_context=user_context,
                    target_drive=target_drive,
                )
                return {
                    "scan_count": len(scan_result.directories),
                    "total_size_mb": scan_result.total_size_mb,
                    "analysis_mode": "ai",
                    "ai_analysis": ai_result,
                    "status": "success",
                }
            except Exception as e:
                # Fall back to rule-based on AI failure
                local_results = [analyzer.analyze(d).to_dict() for d in directories[:20]]
                return {
                    "scan_count": len(scan_result.directories),
                    "total_size_mb": scan_result.total_size_mb,
                    "analysis_mode": "rules",
                    "rule_analysis": local_results,
                    "fallback_reason": f"AI analysis failed: {str(e)}",
                    "status": "fallback",
                }

        # Rule-based analysis (no AI config or prefer_ai=False)
        local_results = [analyzer.analyze(d).to_dict() for d in directories[:20]]
        return {
            "scan_count": len(scan_result.directories),
            "total_size_mb": scan_result.total_size_mb,
            "analysis_mode": "rules",
            "rule_analysis": local_results,
            "status": "success",
        }

    @mcp.tool()
    async def get_ai_provider_info() -> dict[str, Any]:
        """
        Get AI provider status.

        Returns:
            Provider information including availability and model
        """
        if not ai_service.available:
            return {
                "available": False,
                "reason": "No API key configured. Set AI_API_KEY or OPENAI_API_KEY environment variable.",
            }
        
        try:
            return await ai_service.get_provider_info()
        except Exception as e:
            return {"error": str(e), "available": False}

    return mcp


def run(ai_config: AIConfig | None = None):
    """Run the MCP server.
    
    Args:
        ai_config: AI configuration (optional, defaults to environment variables)
    """
    mcp = create_mcp_server(ai_config)
    mcp.run()


# For running directly
mcp = create_mcp_server()

if __name__ == "__main__":
    mcp.run()
