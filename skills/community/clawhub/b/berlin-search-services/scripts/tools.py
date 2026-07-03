from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def search_services(
    query: str
) -> Dict[str, Any]:
    """
    Search for Berlin administrative services by name or description. Returns a list of matching services with basic information.
    
    Args:
        query: Search query (searches in service name and description)
    
    Returns:
        
    """
    arguments = {
        "query": query
    }
    
    return call_api("1777316659740675", "search_services", arguments)

def get_service_details(
    service_id: str
) -> Dict[str, Any]:
    """
    Get detailed information about a specific Berlin service by its ID. Returns comprehensive information including requirements, forms, fees, appointments, and more.
    
    Args:
        service_id: The ID of the service
    
    Returns:
        
    """
    arguments = {
        "service_id": service_id
    }
    
    return call_api("1777316659740675", "get_service_details", arguments)

def list_services(
    limit: Optional[float] = 50.0
) -> Dict[str, Any]:
    """
    List all available Berlin administrative services. Returns a paginated list of services with their names and IDs.
    
    Args:
        limit: Maximum number of services to return (default: 50, max: 200)
    
    Returns:
        
    """
    arguments = {
        "limit": limit
    }
    
    return call_api("1777316659740675", "list_services", arguments)

def get_services_stats(
) -> Dict[str, Any]:
    """
    Get statistics about the Berlin services dataset (total count, last update, etc.)
    
    Args:
    
    Returns:
        
    """
    arguments = {
    }
    
    return call_api("1777316659740675", "get_services_stats", arguments)

