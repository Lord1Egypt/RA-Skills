from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def get_schema(
) -> Dict[str, Any]:
    """
    Get the schema of the graph database, includes nodes, their properties, and relationships.
    
    Args:
    
    Returns:
        Returns nodes, their properties (with types and indexed flags), and relationships.
    """
    arguments = {
    }
    
    return call_api("1815531499719690", "get_schema", arguments)

def execute_read_cypher(
    query: str
) -> Dict[str, Any]:
    """
    MCP Tool to execute a read Cypher query on the graph database.
    
    Args:
        query: The Cypher query to execute.
    
    Returns:
        JSON-formatted query results as a string or an error message.
    """
    arguments = {
        "query": query
    }
    
    return call_api("1815531499719690", "execute_read_cypher", arguments)

