# App Tools

Application information and system details

## get_app_info

Retrieves Eagle application information including version, build number, and system details. Provides comprehensive application metadata for debugging and compatibility checks. Supports both full information retrieval and specific property queries.

### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| property | string | No | Optional application property to retrieve (e.g., version, build, locale, arch, platform, theme) |

### Example

```bash
node scripts/eagle-api-cli.js call get_app_info
```
