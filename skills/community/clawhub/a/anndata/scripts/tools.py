from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def view_raw_data(
    path: str,
    attribute: str,
    key: Optional[null] = None,
    columns_or_genes: Optional[null] = None,
    row_start_index: Optional[int] = 0.0,
    row_stop_index: Optional[int] = 5.0,
    col_start_index: Optional[int] = 0.0,
    col_stop_index: Optional[int] = 5.0,
    filter_column: Optional[null] = None,
    filter_operator: Optional[null] = None,
    filter_value: Optional[null] = None
) -> Dict[str, Any]:
    """
    View the raw data of an AnnData object.
    
    Args:
        path: Absolute path or URL to the AnnData file
        attribute: The attribute to view
        key: The key of the attribute value to view. Can be a single string or a list of strings for nested key retrieval (e.g., ['key1', 'key2'] to access attr_obj['key1']['key2']).
        columns_or_genes: Column names or gene names to select. For pandas.DataFrame attributes (e.g., obs, var), these are column names. For 'X' or 'layers' attributes, these are gene names (from var_names) and are used instead of col_start_index/col_stop_index. If None, the entire attribute is considered or col_start_index/col_stop_index is used. Also accepts glob-like patterns as input, e.g. ['RE*', 'CD4*'].
        row_start_index: The start index for the row slice. Only applied to attributes or attribute values with a suitable type.
        row_stop_index: The stop index for the row slice. Only applied to attributes or attribute values with a suitable type.
        col_start_index: The start index for the column slice. Only applied to attributes or attribute values with a suitable type.
        col_stop_index: The stop index for the column slice. Only applied to attributes or attribute values with a suitable type.
        filter_column: The column name of the dataframe to filter by. Only applicable when the selected attribute (or attribute value) is a dataframe. Must be provided TOGETHER with filter_operator and filter_value.
        filter_operator: The operator to use for the dataframe filter.
        filter_value: The value(s) to filter the dataframe by.
    
    Returns:
        null
    """
    arguments = {
        "path": path,
        "attribute": attribute,
        "key": key,
        "columns_or_genes": columns_or_genes,
        "row_start_index": row_start_index,
        "row_stop_index": row_stop_index,
        "col_start_index": col_start_index,
        "col_stop_index": col_stop_index,
        "filter_column": filter_column,
        "filter_operator": filter_operator,
        "filter_value": filter_value
    }
    
    return call_api("1777419073301507", "view_raw_data", arguments)

def get_summary(
    path: str
) -> Dict[str, Any]:
    """
    Get a summary of an AnnData object from a file or URL.
    
    Args:
        path: Absolute path or URL to the AnnData file (.h5ad or .zarr)
    
    Returns:
        null
    """
    arguments = {
        "path": path
    }
    
    return call_api("1777419073301507", "get_summary", arguments)

def get_descriptive_stats(
    path: str,
    attribute: str,
    key: Optional[null] = None,
    columns_or_genes: Optional[null] = None,
    return_value_counts_for_categorical: Optional[bool] = False,
    filter_attribute: Optional[str] = None,
    filter_column: Optional[null] = None,
    filter_operator: Optional[null] = None,
    filter_value: Optional[null] = None
) -> Dict[str, Any]:
    """
    Provide basic descriptive statistics (e.g., count, mean, std, min, max, etc. or value counts) for an attribute or attribute value of an optionally filtered AnnData object.
    
    Args:
        path: Absolute path or URL to the AnnData file (.h5ad or .zarr)
        attribute: The attribute to describe
        key: The key of the attribute value to explore. Can be a single string or a list of strings for nested key retrieval (e.g., ['key1', 'key2'] to access attr_obj['key1']['key2']). Should be None for attributes X, obs, and var.
        columns_or_genes: The columns or genes to describe. For pandas.DataFrame attributes (e.g., obs, var), these are column names. For 'X' or 'layers' attributes, these are gene names (from var_names). If None, the entire dataset is considered. Also accepts glob-like patterns as input, e.g. ['RE*', 'CD4*'].
        return_value_counts_for_categorical: Whether to return the value counts for categorical columns.
        filter_attribute: The attribute to filter by. One of 'obs' or 'var' or None for no filtering. Has to be provided TOGETHER with filter_column, filter_operator, and filter_value.
        filter_column: The column name of the obs or var dataframe to filter by.
        filter_operator: The operator to use for the filter.
        filter_value: The value(s) to filter by.
    
    Returns:
        null
    """
    arguments = {
        "path": path,
        "attribute": attribute,
        "key": key,
        "columns_or_genes": columns_or_genes,
        "return_value_counts_for_categorical": return_value_counts_for_categorical,
        "filter_attribute": filter_attribute,
        "filter_column": filter_column,
        "filter_operator": filter_operator,
        "filter_value": filter_value
    }
    
    return call_api("1777419073301507", "get_descriptive_stats", arguments)

