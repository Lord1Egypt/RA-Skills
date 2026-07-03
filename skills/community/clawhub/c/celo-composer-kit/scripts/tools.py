from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def list_components(
) -> Dict[str, Any]:
    """
    List all available Composer Kit components with their descriptions and categories. Returns a comprehensive overview of the component library.
    
    Args:
    
    Returns:
        
    """
    arguments = {
    }
    
    return call_api("1777419068377091", "list_components", arguments)

def get_component(
    component_name: str
) -> Dict[str, Any]:
    """
    Get detailed information about a specific Composer Kit component, including source code, props, and usage information.
    
    Args:
        component_name: The name of the component to retrieve (e.g., 'button', 'wallet', 'payment', 'swap')
    
    Returns:
        
    """
    arguments = {
        "component_name": component_name
    }
    
    return call_api("1777419068377091", "get_component", arguments)

def get_component_example(
    component_name: str,
    example_type: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get example usage code for a specific Composer Kit component. Returns real-world examples from the documentation.
    
    Args:
        component_name: The name of the component to get examples for
        example_type: Optional: specific type of example (e.g., 'basic', 'advanced', 'with-props')
    
    Returns:
        
    """
    arguments = {
        "component_name": component_name,
        "example_type": example_type
    }
    
    return call_api("1777419068377091", "get_component_example", arguments)

def search_components(
    query: str
) -> Dict[str, Any]:
    """
    Search for Composer Kit components by name, description, or functionality. Useful for finding components that match specific needs.
    
    Args:
        query: Search query (e.g., 'wallet', 'payment', 'token', 'nft')
    
    Returns:
        
    """
    arguments = {
        "query": query
    }
    
    return call_api("1777419068377091", "search_components", arguments)

def get_component_props(
    component_name: str
) -> Dict[str, Any]:
    """
    Get detailed prop information for a specific component, including types, descriptions, and whether props are required or optional.
    
    Args:
        component_name: The name of the component to get props for
    
    Returns:
        
    """
    arguments = {
        "component_name": component_name
    }
    
    return call_api("1777419068377091", "get_component_props", arguments)

def get_installation_guide(
    package_manager: Optional[str] = None
) -> Dict[str, Any]:
    """
    Get installation instructions for Composer Kit, including setup steps and configuration for different package managers.
    
    Args:
        package_manager: Package manager to use (npm, yarn, pnpm, bun). Defaults to npm if not specified.
    
    Returns:
        
    """
    arguments = {
        "package_manager": package_manager
    }
    
    return call_api("1777419068377091", "get_installation_guide", arguments)

def get_components_by_category(
    category: str
) -> Dict[str, Any]:
    """
    Get all components in a specific category (e.g., 'Wallet Integration', 'Payment & Transactions', 'Core Components', 'NFT Components').
    
    Args:
        category: The category name (e.g., 'Core Components', 'Wallet Integration', 'Payment & Transactions', 'Token Management', 'NFT Components')
    
    Returns:
        
    """
    arguments = {
        "category": category
    }
    
    return call_api("1777419068377091", "get_components_by_category", arguments)

def get_celo_composer_cli_info(
) -> Dict[str, Any]:
    """
    Get detailed information on the Celo Composer CLI `create` command, including all available flags like `--description`, `--wallet-provider`, and `--contracts`. Provides documentation, options, and usage examples to help construct `create` commands.
    
    Args:
    
    Returns:
        
    """
    arguments = {
    }
    
    return call_api("1777419068377091", "get_celo_composer_cli_info", arguments)

