from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def list_tables(
) -> Dict[str, Any]:
    """
    List all tables in the database.
    
    Args:
    
    Returns:
        A JSON string mapping table names to their corresponding CREATE TABLE statements.
    """
    arguments = {
    }
    
    return call_api("1819483683233802", "list_tables", arguments)

def get_table_schema(
    table: str
) -> Dict[str, Any]:
    """
    Get column information for a specified table in the database.
    
    Args:
        table: The name of the database table.
    
    Returns:
        A JSON string describing the table schema, or an error message if the table is not found.
    """
    arguments = {
        "table": table
    }
    
    return call_api("1819483683233802", "get_table_schema", arguments)

def sql_query(
    query: str
) -> Dict[str, Any]:
    """
    MCP Tool to execute a SQL query.
    
    Args:
        query: A SQL query string provided by the client.
    
    Returns:
        JSON-formatted query results as a string or an error message.
    """
    arguments = {
        "query": query
    }
    
    return call_api("1819483683233802", "sql_query", arguments)

