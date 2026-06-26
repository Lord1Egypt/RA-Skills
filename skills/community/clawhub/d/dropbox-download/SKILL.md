# Dropbox Download

Download files from Dropbox using the `/2/files/download` endpoint.

## Description

This skill downloads a file from a user's Dropbox account. It accepts a file path and an optional revision identifier.

## IO

| Field | Type | Description |
|-------|------|-------------|
| path | string | The path of the file to download (required) |
| rev | string | Optional revision identifier (deprecated, specify in path instead) |
| result | binary | The downloaded file content |

## Configuration

- **Integration**: `dropbox` (OAuth2)
- **HTTP Method**: POST
- **Endpoint**: `/2/files/download`

## Usage

```python
from typing import Annotated

def run(
    pipedream: Annotated[PipedreamAuth, Integration("dropbox")],
    path: Annotated[str, "The path of the file to download."],
    rev: Annotated[str | None, "Please specify revision in path instead."] = None,
):

    # Track initial props for reload comparison
    initial_props = {
          "dropbox", "path", "rev",
    }

    state_manager = PipedreamStateManager(pipedream, "Download File", initial_props, {})
    state_manager.add_prop("dropbox", {"authProvisionId": pipedream.auth_provision_id})

    state_manager.add_prop("path", path)

    rev_config = state_manager.resolve_prop("rev", rev, use_query=False, use_lv=False)
    state_manager.add_prop("rev", rev_config)

    return state_manager.run()
```

## Notes

- The `rev` parameter is deprecated; specify revision in the path instead.
- The file content is returned as binary data.
- Ensure the Dropbox integration has `files.content.read` scope.

## License

MIT
