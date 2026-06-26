"""
Resolve Bitable target module.

Responsibilities:
- Resolve target table and field from provided parameters
- Support table_id or table_name
- Support field_id or field_name
- Support lookup to find record_id
- Support create_new_record mode when record_id is empty

Resolution priority:
- table_id > table_name
- field_id > field_name

This module enables the skill to work with ANY Bitable by dynamically
resolving names to IDs at runtime.
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass

from common import (
    log,
    make_authenticated_request,
    get_feishu_base_url,
    BitableResolveError,
    API_BITABLE_LIST_TABLES,
    API_BITABLE_LIST_FIELDS,
    API_BITABLE_SEARCH_RECORDS,
)


@dataclass
class TargetResult:
    """Resolved target information."""
    app_token: str
    table_id: str
    table_name: str
    field_id: str
    field_name: str
    record_id: Optional[str]
    create_new_record: bool
    lookup_field_id: Optional[str] = None
    lookup_field_name: Optional[str] = None
    lookup_value: Optional[str] = None


def resolve_bitable_target(
    target: Dict[str, Any],
    app_id: str,
    app_secret: str
) -> TargetResult:
    """
    Resolve Bitable target from input parameters.

    This function enables the skill to work with ANY Bitable by:
    - Accepting app_token from input (not hardcoded)
    - Resolving table_name to table_id dynamically
    - Resolving field_name to field_id dynamically
    - Supporting lookup to find record_id

    Args:
        target: Target config from input with these possible fields:
            - app_token (required): Bitable app token
            - table_id (optional): Table ID (overrides table_name)
            - table_name (optional): Table display name
            - field_id (optional): Field ID (overrides field_name)
            - field_name (optional): Field display name
            - record_id (optional): Record ID
            - lookup (optional): Lookup config {field_name, field_id, value}
            - allow_create_if_lookup_missing (optional): bool
        app_id: Feishu app ID
        app_secret: Feishu app secret

    Returns:
        TargetResult with resolved IDs

    Raises:
        BitableResolveError: If resolution fails
        SkillInputError: If required parameters are missing
    """
    from common import SkillInputError

    app_token = target.get("app_token")
    table_id = target.get("table_id", "")
    table_name = target.get("table_name", "")
    field_id = target.get("field_id", "")
    field_name = target.get("field_name", "")
    record_id = target.get("record_id", "")
    lookup = target.get("lookup", {})
    allow_create_if_lookup_missing = target.get("allow_create_if_lookup_missing", False)

    # Validate app_token
    if not app_token:
        raise SkillInputError("app_token is required")

    # Resolve table_id (priority: table_id > table_name)
    if not table_id:
        if not table_name:
            raise SkillInputError("Either table_id or table_name must be provided")
        table_id = _resolve_table_id(app_token, table_name, app_id, app_secret)
        log.info(f"Resolved table_name '{table_name}' to table_id '{table_id}'")
    else:
        log.info(f"Using provided table_id: {table_id}")
        # Optionally fetch table_name for logging
        table_name = table_name or _get_table_name(app_token, table_id, app_id, app_secret)

    # Resolve field_id (priority: field_id > field_name)
    if not field_id:
        if not field_name:
            raise SkillInputError("Either field_id or field_name must be provided")
        field_id = _resolve_field_id(app_token, table_id, field_name, app_id, app_secret)
        log.info(f"Resolved field_name '{field_name}' to field_id '{field_id}'")
    else:
        log.info(f"Using provided field_id: {field_id}")
        # Optionally fetch field_name for logging
        field_name = field_name or _get_field_name(app_token, table_id, field_id, app_id, app_secret)

    # Resolve record_id
    create_new_record = False
    lookup_field_id = None
    lookup_field_name = None
    lookup_value = None

    if record_id:
        log.info(f"Using provided record_id: {record_id}")
    elif lookup:
        # Lookup record by field value
        lookup_field_id = lookup.get("field_id", "")
        lookup_field_name = lookup.get("field_name", "")
        lookup_value = lookup.get("value")

        if not lookup_value:
            raise SkillInputError("lookup.value is required when lookup is provided")

        # Resolve lookup field_id if needed
        if not lookup_field_id:
            if not lookup_field_name:
                raise SkillInputError("Either lookup.field_id or lookup.field_name must be provided")
            lookup_field_id = _resolve_field_id(app_token, table_id, lookup_field_name, app_id, app_secret)
            log.info(f"Resolved lookup field_name '{lookup_field_name}' to field_id '{lookup_field_id}'")

        # Search for record
        record_id = _lookup_record(app_token, table_id, lookup_field_id, lookup_value, app_id, app_secret)

        if record_id:
            log.info(f"Lookup found record_id: {record_id}")
        elif allow_create_if_lookup_missing:
            log.info("Lookup found no record, will create new record")
            create_new_record = True
            record_id = None
        else:
            raise BitableResolveError(
                f"No record found with {lookup_field_name or lookup_field_id} = '{lookup_value}'. "
                f"Set allow_create_if_lookup_missing=true to create a new record."
            )
    else:
        # No record_id and no lookup - create new record mode
        log.info("No record_id provided, will create new record")
        create_new_record = True
        record_id = None

    return TargetResult(
        app_token=app_token,
        table_id=table_id,
        table_name=table_name,
        field_id=field_id,
        field_name=field_name,
        record_id=record_id,
        create_new_record=create_new_record,
        lookup_field_id=lookup_field_id,
        lookup_field_name=lookup_field_name,
        lookup_value=lookup_value
    )


# ============================================================================
# Table Resolution
# ============================================================================

def _resolve_table_id(
    app_token: str,
    table_name: str,
    app_id: str,
    app_secret: str
) -> str:
    """
    Resolve table_id from table_name.

    Lists all tables in the Bitable and matches by name.
    Matching priority: exact match > case-insensitive > partial match

    Args:
        app_token: Bitable app token
        table_name: Table display name
        app_id: Feishu app ID
        app_secret: Feishu app secret

    Returns:
        table_id string

    Raises:
        BitableResolveError: If table not found
    """
    base_url = get_feishu_base_url()
    url = f"{base_url}{API_BITABLE_LIST_TABLES.format(app_token=app_token)}"

    response = make_authenticated_request("GET", url, app_id, app_secret)

    tables = response.get("data", {}).get("items", [])
    if not tables:
        raise BitableResolveError(f"No tables found in Bitable {app_token}")

    # Try exact match first
    for table in tables:
        if table.get("name") == table_name:
            return table.get("table_id")

    # Try case-insensitive match
    table_name_lower = table_name.lower()
    for table in tables:
        if table.get("name", "").lower() == table_name_lower:
            return table.get("table_id")

    # Try partial match (contains)
    for table in tables:
        if table_name_lower in table.get("name", "").lower():
            log.warning(f"Using partial match for table: '{table_name}' -> '{table.get('name')}'")
            return table.get("table_id")

    available_tables = [t.get("name") for t in tables]
    raise BitableResolveError(
        f"Table '{table_name}' not found in Bitable {app_token}. "
        f"Available tables: {', '.join(available_tables)}"
    )


def _get_table_name(
    app_token: str,
    table_id: str,
    app_id: str,
    app_secret: str
) -> str:
    """
    Get table name from table_id.

    Returns empty string if not found (used for logging only).
    """
    base_url = get_feishu_base_url()
    url = f"{base_url}{API_BITABLE_LIST_TABLES.format(app_token=app_token)}"

    try:
        response = make_authenticated_request("GET", url, app_id, app_secret)
        tables = response.get("data", {}).get("items", [])
        for table in tables:
            if table.get("table_id") == table_id:
                return table.get("name", "")
    except Exception:
        pass

    return ""


# ============================================================================
# Field Resolution
# ============================================================================

def _resolve_field_id(
    app_token: str,
    table_id: str,
    field_name: str,
    app_id: str,
    app_secret: str
) -> str:
    """
    Resolve field_id from field_name.

    Lists all fields in the table and matches by name.
    Matching priority: exact match > case-insensitive > partial match

    Args:
        app_token: Bitable app token
        table_id: Table ID
        field_name: Field display name
        app_id: Feishu app ID
        app_secret: Feishu app secret

    Returns:
        field_id string

    Raises:
        BitableResolveError: If field not found
    """
    base_url = get_feishu_base_url()
    url = f"{base_url}{API_BITABLE_LIST_FIELDS.format(app_token=app_token, table_id=table_id)}"

    response = make_authenticated_request("GET", url, app_id, app_secret)

    fields = response.get("data", {}).get("items", [])
    if not fields:
        raise BitableResolveError(f"No fields found in table {table_id}")

    # Debug: Log first few fields to understand structure
    log.info(f"API returned {len(fields)} fields")
    for i, field in enumerate(fields[:3]):
        log.info(f"Field {i}: {field}")

    # Try multiple possible keys for field name
    # Feishu API may use "name" or "title" depending on version
    def get_field_name(field: Dict) -> str:
        """Get field name from field object, trying multiple possible keys."""
        # Try "name" first (standard key)
        name = field.get("name")
        if name:
            return name
        # Try "title" (some API versions)
        title = field.get("title")
        if title:
            return title
        # Try "field_name" (rare)
        field_name_key = field.get("field_name")
        if field_name_key:
            return field_name_key
        # Fallback to empty string
        return ""

    # Try exact match first
    for field in fields:
        fname = get_field_name(field)
        fid = field.get("field_id")
        ftype = field.get("type")
        log.debug(f"Checking field: name={fname}, id={fid}, type={ftype}")
        if fname == field_name:
            log.info(f"Exact match found: '{field_name}' -> field_id={fid}, type={ftype}")
            return fid

    # Try case-insensitive match
    field_name_lower = field_name.lower()
    for field in fields:
        fname = get_field_name(field)
        fid = field.get("field_id")
        ftype = field.get("type")
        if fname and fname.lower() == field_name_lower:
            log.info(f"Case-insensitive match found: '{field_name}' -> field_id={fid}, type={ftype}")
            return fid

    # Try partial match (contains)
    for field in fields:
        fname = get_field_name(field)
        fid = field.get("field_id")
        ftype = field.get("type")
        if fname and field_name_lower in fname.lower():
            log.warning(f"Partial match found: '{field_name}' -> '{fname}' (field_id={fid}, type={ftype})")
            return fid

    # Build available fields list with names
    available_fields = []
    for f in fields:
        fname = get_field_name(f)
        ftype = f.get("type")
        available_fields.append((fname if fname else "(no name)", ftype))

    raise BitableResolveError(
        f"Field '{field_name}' not found in table {table_id}. "
        f"Available fields: {available_fields}"
    )


def _get_field_name(
    app_token: str,
    table_id: str,
    field_id: str,
    app_id: str,
    app_secret: str
) -> str:
    """
    Get field name from field_id.

    Returns empty string if not found (used for logging only).
    """
    base_url = get_feishu_base_url()
    url = f"{base_url}{API_BITABLE_LIST_FIELDS.format(app_token=app_token, table_id=table_id)}"

    try:
        response = make_authenticated_request("GET", url, app_id, app_secret)
        fields = response.get("data", {}).get("items", [])
        for field in fields:
            if field.get("field_id") == field_id:
                # Try multiple possible keys for field name
                name = field.get("name")
                if name:
                    return name
                title = field.get("title")
                if title:
                    return title
                return ""
    except Exception:
        pass

    return ""


# ============================================================================
# Record Lookup
# ============================================================================

def _lookup_record(
    app_token: str,
    table_id: str,
    field_id: str,
    value: str,
    app_id: str,
    app_secret: str
) -> Optional[str]:
    """
    Lookup record by field value.

    Uses the Bitable search_records API.

    Args:
        app_token: Bitable app token
        table_id: Table ID
        field_id: Field ID to search
        value: Value to match
        app_id: Feishu app ID
        app_secret: Feishu app secret

    Returns:
        record_id if found, None otherwise
    """
    base_url = get_feishu_base_url()
    url = f"{base_url}{API_BITABLE_SEARCH_RECORDS.format(app_token=app_token, table_id=table_id)}"

    # Build filter
    # Filter format: {"filter": [{"field_id": "xxx", "operator": "is", "value": "xxx"}]}
    filter_config = {
        "filter": [
            {
                "field_id": field_id,
                "operator": "is",
                "value": value
            }
        ]
    }

    try:
        response = make_authenticated_request(
            "POST",
            url,
            app_id,
            app_secret,
            json_body=filter_config
        )
    except Exception as e:
        log.warning(f"Lookup failed: {e}")
        return None

    records = response.get("data", {}).get("items", [])
    if not records:
        return None

    # Return first matching record
    return records[0].get("record_id")


def resolve_field_type(
    app_token: str,
    table_id: str,
    field_id: str,
    app_id: str,
    app_secret: str
) -> str:
    """
    Get field type from field_id.

    Returns the field type string (e.g., 'attachment', 'text', 'single_select').
    """
    base_url = get_feishu_base_url()
    url = f"{base_url}{API_BITABLE_LIST_FIELDS.format(app_token=app_token, table_id=table_id)}"

    response = make_authenticated_request("GET", url, app_id, app_secret)

    fields = response.get("data", {}).get("items", [])
    for field in fields:
        if field.get("field_id") == field_id:
            return field.get("type", "")

    return ""
