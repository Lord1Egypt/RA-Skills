"""
Update Bitable record module.

Responsibilities:
- Create new record with attachment field
- Update existing record with attachment field
- Support append mode (keep existing attachments + add new)
- Support replace mode (overwrite attachment field)

Key insight for append mode:
- Bitable attachment fields are arrays of {file_token: ...} objects
- To append, we must: GET record -> extract existing attachments -> add new -> PUT back
- Without reading first, we would overwrite and lose existing attachments
"""

from typing import Dict, Any, Optional, List
import json

from common import (
    log,
    make_authenticated_request,
    get_feishu_base_url,
    BitableUpdateError,
    BitableResolveError,
    FeishuAPIError,
    API_BITABLE_GET_RECORD,
    API_BITABLE_UPDATE_RECORD,
    API_BITABLE_CREATE_RECORD,
)


def update_bitable_record(
    app_token: str,
    table_id: str,
    field_id: str,
    file_token: str,
    app_id: str,
    app_secret: str,
    record_id: Optional[str] = None,
    append: bool = True,
    fields: Optional[Dict[str, Any]] = None,
    field_name: Optional[str] = None
) -> Dict[str, Any]:
    """
    Update or create Bitable record with attachment field.

    Args:
        app_token: Bitable app token
        table_id: Table ID
        field_id: Field ID (attachment field)
        file_token: File token from upload
        app_id: Feishu app ID
        app_secret: Feishu app secret
        record_id: Record ID (None for create new record)
        append: If True, append to existing attachments; if False, replace
        fields: Additional fields for new record creation
        field_name: Optional field name for fallback

    Returns:
        Dict with record_id, attachment_count, mode

    Raises:
        BitableUpdateError: If update/create fails
        BitableResolveError: If record not found
    """
    if record_id:
        # Update existing record
        log.info(f"Updating existing record: {record_id}")
        return _update_record(
            app_token, table_id, field_id, file_token,
            app_id, app_secret, record_id, append, field_name
        )
    else:
        # Create new record
        log.info("Creating new record")
        return _create_record(
            app_token, table_id, field_id, file_token,
            app_id, app_secret, fields
        )


# ============================================================================
# Update Existing Record
# ============================================================================

def _update_record(
    app_token: str,
    table_id: str,
    field_id: str,
    file_token: str,
    app_id: str,
    app_secret: str,
    record_id: str,
    append: bool,
    field_name: Optional[str] = None
) -> Dict[str, Any]:
    """
    Update existing record with attachment.

    Args:
        record_id: Existing record ID
        append: If True, keep existing attachments and add new one
        field_name: Optional field name for fallback

    Returns:
        Dict with record_id, attachment_count, mode

    Raises:
        BitableResolveError: If record not found
        BitableUpdateError: If update fails
    """
    base_url = get_feishu_base_url()

    if append:
        # Fetch existing record to get current attachments
        log.info("Fetching existing record for append mode")
        existing_attachments = _get_record_attachments(
            app_token, table_id, record_id, field_id, field_name, app_id, app_secret
        )
        log.info(f"Found {len(existing_attachments)} existing attachments")

        # Append new file_token
        attachments = existing_attachments + [{"file_token": file_token}]
        mode = "append"
    else:
        # Replace with new attachment only
        attachments = [{"file_token": file_token}]
        mode = "replace"

    # Build update payload - Use field_id as key (primary), field_name as fallback
    # Feishu Bitable API uses field_id as the key in fields object
    field_key = field_id  # Always prefer field_id
    log.info(f"Using field_id as key for update: {field_key}")

    fields_data = {field_key: attachments}

    url = f"{base_url}{API_BITABLE_UPDATE_RECORD.format(
        app_token=app_token,
        table_id=table_id,
        record_id=record_id
    )}"

    payload = {
        "fields": fields_data
    }

    # Log exactly what field key is being used for the update
    log.info(f"Final fields payload key: {field_key} (field_id)")
    log.info(f"Attachment count being written: {len(attachments)}")
    log.info(f"Full payload: {json.dumps({'fields': {field_key: f'[{len(attachments)} attachments]'}})}")

    try:
        response = make_authenticated_request("PUT", url, app_id, app_secret, json_body=payload)
    except FeishuAPIError as e:
        if e.status_code == 404:
            raise BitableResolveError(f"Record not found: {record_id}")
        # If FieldNameNotFound error and we have field_name fallback, try with field_name
        if field_name and "FieldNameNotFound" in str(e.message):
            log.warning(f"field_id '{field_id}' not recognized, trying field_name '{field_name}'")
            fields_data = {field_name: attachments}
            payload = {"fields": fields_data}
            log.info(f"Retrying with field_name as key: {field_name}")
            log.info(f"Retry payload: {json.dumps({'fields': {field_name: f'[{len(attachments)} attachments]'}})}")
            try:
                response = make_authenticated_request("PUT", url, app_id, app_secret, json_body=payload)
            except FeishuAPIError as e2:
                raise BitableUpdateError(f"Failed to update record with field_name: {e2.message}")
        else:
            raise BitableUpdateError(f"Failed to update record: {e.message}")

    # Parse response
    data = response.get("data", {})
    updated_record_id = data.get("record_id", record_id)

    log.info(f"Record updated successfully: {updated_record_id}")

    return {
        "record_id": updated_record_id,
        "attachment_count": len(attachments),
        "mode": mode
    }


def _get_record_attachments(
    app_token: str,
    table_id: str,
    record_id: str,
    field_id: str,
    field_name: Optional[str] = None,
    app_id: str = None,
    app_secret: str = None
) -> List[Dict[str, str]]:
    """
    Get existing attachments from record.

    This is required for append mode - we need to preserve existing attachments.

    Args:
        app_token: Bitable app token
        table_id: Table ID
        record_id: Record ID
        field_id: Field ID (primary key to look for)
        field_name: Optional field name fallback
        app_id: Feishu app ID
        app_secret: Feishu app secret

    Returns:
        List of {"file_token": "..."} dicts

    Raises:
        BitableResolveError: If record not found
    """
    base_url = get_feishu_base_url()
    url = f"{base_url}{API_BITABLE_GET_RECORD.format(
        app_token=app_token,
        table_id=table_id,
        record_id=record_id
    )}"

    try:
        response = make_authenticated_request("GET", url, app_id, app_secret)
    except FeishuAPIError as e:
        if e.status_code == 404:
            raise BitableResolveError(f"Record not found: {record_id}")
        raise BitableResolveError(f"Failed to get record: {e.message}")

    # Parse response
    data = response.get("data", {})
    fields_data = data.get("fields", {})

    # Try field_id first (primary key)
    attachment_value = fields_data.get(field_id)
    used_key = field_id

    # Fallback to field_name if field_id not found
    if attachment_value is None and field_name:
        attachment_value = fields_data.get(field_name)
        if attachment_value is not None:
            log.info(f"Field ID '{field_id}' not found in record, using field_name '{field_name}' instead")
            used_key = field_name

    if attachment_value is None:
        # Field might not exist or be empty
        log.warning(f"Field '{field_id}' not found in record {record_id}, treating as empty")
        return []

    if not isinstance(attachment_value, list):
        log.warning(f"Field '{used_key}' is not a list (type: {type(attachment_value)}), treating as empty")
        return []

    # Extract file_tokens from existing attachments
    attachments = []
    for item in attachment_value:
        if isinstance(item, dict) and "file_token" in item:
            attachments.append({"file_token": item["file_token"]})

    return attachments


# ============================================================================
# Create New Record
# ============================================================================

def _create_record(
    app_token: str,
    table_id: str,
    field_id: str,
    file_token: str,
    app_id: str,
    app_secret: str,
    fields: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Create new record with attachment field.

    Args:
        fields: Additional fields to set (dict of field_id -> value)

    Returns:
        Dict with record_id, attachment_count, mode

    Raises:
        BitableUpdateError: If create fails
    """
    base_url = get_feishu_base_url()

    # Build fields with attachment
    # The attachment field format is: [{file_token: "vob..."}]
    fields_data = {field_id: [{"file_token": file_token}]}

    # Merge additional fields
    if fields:
        for fid, value in fields.items():
            fields_data[fid] = value

    url = f"{base_url}{API_BITABLE_CREATE_RECORD.format(app_token=app_token, table_id=table_id)}"

    payload = {
        "records": [
            {
                "fields": fields_data
            }
        ]
    }

    try:
        response = make_authenticated_request("POST", url, app_id, app_secret, json_body=payload)
    except FeishuAPIError as e:
        raise BitableUpdateError(f"Failed to create record: {e.message}")

    # Parse response
    data = response.get("data", {})
    records = data.get("items", [])

    if not records:
        raise BitableUpdateError("Create record succeeded but no record returned")

    new_record_id = records[0].get("record_id")

    if not new_record_id:
        raise BitableUpdateError("Create record succeeded but no record_id returned")

    log.info(f"New record created successfully: {new_record_id}")

    return {
        "record_id": new_record_id,
        "attachment_count": 1,
        "mode": "create"
    }


# ============================================================================
# Validation Helpers
# ============================================================================

def validate_field_exists(
    app_token: str,
    table_id: str,
    field_id: str,
    app_id: str,
    app_secret: str
) -> bool:
    """
    Validate that field exists in table.

    Returns True if field exists, False otherwise.
    """
    from common import API_BITABLE_LIST_FIELDS

    base_url = get_feishu_base_url()
    url = f"{base_url}{API_BITABLE_LIST_FIELDS.format(app_token=app_token, table_id=table_id)}"

    try:
        response = make_authenticated_request("GET", url, app_id, app_secret)
        fields = response.get("data", {}).get("items", [])
        for field in fields:
            if field.get("field_id") == field_id:
                return True
    except Exception:
        return False

    return False


def validate_record_exists(
    app_token: str,
    table_id: str,
    record_id: str,
    app_id: str,
    app_secret: str
) -> bool:
    """
    Validate that record exists in table.

    Returns True if record exists, False otherwise.
    """
    base_url = get_feishu_base_url()
    url = f"{base_url}{API_BITABLE_GET_RECORD.format(
        app_token=app_token,
        table_id=table_id,
        record_id=record_id
    )}"

    try:
        make_authenticated_request("GET", url, app_id, app_secret)
        return True
    except FeishuAPIError as e:
        if e.status_code == 404:
            return False
        raise
