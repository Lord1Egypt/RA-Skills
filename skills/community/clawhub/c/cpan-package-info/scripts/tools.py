from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def get_readme_from_cpan(
    package_name: str,
    version: Optional[str] = None,
    include_examples: Optional[bool] = True
) -> Dict[str, Any]:
    """
    Get package README and usage examples from CPAN
    
    Args:
        package_name: The name of the CPAN module (e.g., "Data::Dumper", "LWP::UserAgent")
        version: Package version (optional, defaults to latest)
        include_examples: Whether to include usage examples (default: true)
    
    Returns:
        
    """
    arguments = {
        "package_name": package_name,
        "version": version,
        "include_examples": include_examples
    }
    
    return call_api("1777316659560451", "get_readme_from_cpan", arguments)

def get_package_info_from_cpan(
    package_name: str,
    include_dependencies: Optional[bool] = True,
    include_dev_dependencies: Optional[bool] = False
) -> Dict[str, Any]:
    """
    Get package basic information and dependencies from CPAN
    
    Args:
        package_name: The name of the CPAN module (e.g., "Data::Dumper", "LWP::UserAgent")
        include_dependencies: Whether to include dependencies (default: true)
        include_dev_dependencies: Whether to include test dependencies (default: false)
    
    Returns:
        
    """
    arguments = {
        "package_name": package_name,
        "include_dependencies": include_dependencies,
        "include_dev_dependencies": include_dev_dependencies
    }
    
    return call_api("1777316659560451", "get_package_info_from_cpan", arguments)

def search_packages_from_cpan(
    query: str,
    limit: Optional[float] = 20.0
) -> Dict[str, Any]:
    """
    Search for packages in CPAN
    
    Args:
        query: The search query
        limit: Maximum number of results to return (default: 20)
    
    Returns:
        
    """
    arguments = {
        "query": query,
        "limit": limit
    }
    
    return call_api("1777316659560451", "search_packages_from_cpan", arguments)

