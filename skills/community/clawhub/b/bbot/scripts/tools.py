from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def list_bbot_modules(
) -> Dict[str, Any]:
    """
    List all available bbot modules
    
    Args:
    
    Returns:
        null
    """
    arguments = {
    }
    
    return call_api("1777419071520771", "list_bbot_modules", arguments)

def list_bbot_presets(
) -> Dict[str, Any]:
    """
    List all available bbot presets
    
    Args:
    
    Returns:
        null
    """
    arguments = {
    }
    
    return call_api("1777419071520771", "list_bbot_presets", arguments)

def start_bbot_scan(
    targets: str,
    modules: Optional[str] = "",
    presets: Optional[str] = "",
    flags: Optional[str] = "",
    no_deps: Optional[bool] = True
) -> Dict[str, Any]:
    """
    
Start a new bbot scan

Args:
    targets: Comma-separated list of targets (domains, IPs, URLs)
    modules: Comma-separated list of modules to use (optional)
    presets: Comma-separated list of presets to use (optional)
    flags: Comma-separated list of flags to use (optional)
    no_deps: Disable dependency installation to prevent sudo prompts (default: True)

    
    Args:
        targets: null
        modules: null
        presets: null
        flags: null
        no_deps: null
    
    Returns:
        null
    """
    arguments = {
        "targets": targets,
        "modules": modules,
        "presets": presets,
        "flags": flags,
        "no_deps": no_deps
    }
    
    return call_api("1777419071520771", "start_bbot_scan", arguments)

def get_scan_status(
    scan_id: str
) -> Dict[str, Any]:
    """
    Get the status of a specific scan
    
    Args:
        scan_id: null
    
    Returns:
        null
    """
    arguments = {
        "scan_id": scan_id
    }
    
    return call_api("1777419071520771", "get_scan_status", arguments)

def get_scan_results(
    scan_id: str,
    limit: Optional[int] = 100.0
) -> Dict[str, Any]:
    """
    
Get results from a specific scan

Args:
    scan_id: The ID of the scan
    limit: Maximum number of results to return (default: 100)

    
    Args:
        scan_id: null
        limit: null
    
    Returns:
        null
    """
    arguments = {
        "scan_id": scan_id,
        "limit": limit
    }
    
    return call_api("1777419071520771", "get_scan_results", arguments)

def list_active_scans(
) -> Dict[str, Any]:
    """
    List all active scans
    
    Args:
    
    Returns:
        null
    """
    arguments = {
    }
    
    return call_api("1777419071520771", "list_active_scans", arguments)

def wait_for_scan_completion(
    scan_id: str,
    timeout: Optional[int] = 300.0,
    poll_interval: Optional[int] = 5.0,
    include_progress: Optional[bool] = True
) -> Dict[str, Any]:
    """
    
Wait for a scan to complete with timeout and progress reporting

Args:
    scan_id: The ID of the scan to wait for
    timeout: Maximum time to wait in seconds (default: 300 = 5 minutes)
    poll_interval: How often to check scan status in seconds (default: 5)
    include_progress: Whether to include progress updates in the response (default: True)

    
    Args:
        scan_id: null
        timeout: null
        poll_interval: null
        include_progress: null
    
    Returns:
        null
    """
    arguments = {
        "scan_id": scan_id,
        "timeout": timeout,
        "poll_interval": poll_interval,
        "include_progress": include_progress
    }
    
    return call_api("1777419071520771", "wait_for_scan_completion", arguments)

def get_dependency_info(
) -> Dict[str, Any]:
    """
    Get information about dependency management in bbot scans
    
    Args:
    
    Returns:
        null
    """
    arguments = {
    }
    
    return call_api("1777419071520771", "get_dependency_info", arguments)

