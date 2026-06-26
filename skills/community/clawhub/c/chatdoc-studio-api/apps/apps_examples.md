# Apps API - Code Examples

This page contains code examples for the Apps API in Python, TypeScript (server-side), and cURL.

## Environment Setup

Set up your environment variables:

```bash
export CHATDOC_STUDIO_BASE_URL="https://api.chatdoc.studio/v1"
export CHATDOC_STUDIO_API_KEY="your-api-key-here"
```

## Get Apps

### Python

```python
import os
import requests

BASE_URL = os.getenv("CHATDOC_STUDIO_BASE_URL", "https://api.chatdoc.studio/v1")
API_KEY = os.getenv("CHATDOC_STUDIO_API_KEY")

def get_apps(current_page: int = 1, page_size: int = 20) -> dict:
    """Get a paginated list of all apps in your team."""
    url = f"{BASE_URL}/apps/"
    headers = {"Authorization": f"Bearer {API_KEY}"}

    params = {
        "currentPage": current_page,
        "pageSize": page_size
    }

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()["data"]

# Usage
result = get_apps(current_page=1, page_size=20)
print(f"Total apps: {result['total']}")
print(f"Current page: {result['page']}")
print(f"Page size: {result['size']}")

# Print each app
for app in result["items"]:
    app_type_name = {
        1: "ChatApp",
        2: "ExtractApp",
        5: "RAG App",
        7: "Agent App"
    }.get(app["app_type"], "Unknown")
    print(f"  - {app['name']} ({app_type_name}) - ID: {app['id']}")

# Pagination example
def get_all_apps():
    """Get all apps by handling pagination."""
    all_apps = []
    page = 1
    page_size = 20

    while True:
        result = get_apps(current_page=page, page_size=page_size)
        all_apps.extend(result["items"])

        # Check if there are more pages
        if len(result["items"]) < page_size:
            break

        page += 1

    return all_apps

all_apps = get_all_apps()
print(f"Retrieved {len(all_apps)} apps total")
```

### TypeScript (Server-side)

```typescript
import axios from 'axios';

const BASE_URL = process.env.CHATDOC_STUDIO_BASE_URL || 'https://api.chatdoc.studio/v1';
const API_KEY = process.env.CHATDOC_STUDIO_API_KEY || '';

interface AppItem {
  id: string;
  name: string;
  app_type: number;
  created_at: number;
  updated_at: number;
}

interface GetAppsResponse {
  items: AppItem[];
  page: number;
  size: number;
  total: number;
}

interface ApiErrorResponse {
  code: string;
  detail?: string;
}

async function getApps(
  currentPage: number = 1,
  pageSize: number = 20
): Promise<GetAppsResponse> {
  const response = await axios.get<{ data: GetAppsResponse }>(
    `${BASE_URL}/apps/`,
    {
      headers: {
        Authorization: `Bearer ${API_KEY}`,
      },
      params: {
        currentPage,
        pageSize,
      },
    }
  );
  return response.data.data;
}

// Usage
const result = await getApps(1, 20);
console.log(`Total apps: ${result.total}`);
console.log(`Current page: ${result.page}`);
console.log(`Page size: ${result.size}`);

// Print each app
for (const app of result.items) {
  const appTypeName = {
    1: 'ChatApp',
    2: 'ExtractApp',
    5: 'RAG App',
    7: 'Agent App',
  }[app.app_type] || 'Unknown';
  console.log(`  - ${app.name} (${appTypeName}) - ID: ${app.id}`);
}

// Pagination example
async function getAllApps(): Promise<AppItem[]> {
  const allApps: AppItem[] = [];
  let page = 1;
  const pageSize = 20;

  while (true) {
    const result = await getApps(page, pageSize);
    allApps.push(...result.items);

    // Check if there are more pages
    if (result.items.length < pageSize) {
      break;
    }

    page++;
  }

  return allApps;
}

const allApps = await getAllApps();
console.log(`Retrieved ${allApps.length} apps total`);
```

### cURL

```bash
# Get first page of apps (default page size: 20)
curl -X GET "${CHATDOC_STUDIO_BASE_URL}/apps/" \
  -H "Authorization: Bearer ${CHATDOC_STUDIO_API_KEY}"

# Get second page with custom page size
curl -X GET "${CHATDOC_STUDIO_BASE_URL}/apps/?currentPage=2&pageSize=10" \
  -H "Authorization: Bearer ${CHATDOC_STUDIO_API_KEY}"

# Response example:
# {
#   "data": {
#     "items": [
#       {
#         "id": "abc123xyz",
#         "name": "Customer Support Bot",
#         "app_type": 1,
#         "created_at": 1757320181,
#         "updated_at": 1757320181
#       },
#       {
#         "id": "def456uvw",
#         "name": "Invoice Extractor",
#         "app_type": 2,
#         "created_at": 1757320181,
#         "updated_at": 1757320181
#       },
#       {
#         "id": "ghi789rst",
#         "name": "Contract Review Agent",
#         "app_type": 7,
#         "created_at": 1757320181,
#         "updated_at": 1757320181
#       }
#     ],
#     "page": 1,
#     "size": 20,
#     "total": 42
#   }
# }
```

## Delete App

### Python

```python
def delete_app(app_id: str) -> None:
    """Delete an app by ID.

    This operation is permanent and irreversible.
    """
    url = f"{BASE_URL}/apps/{app_id}"
    headers = {"Authorization": f"Bearer {API_KEY}"}

    response = requests.delete(url, headers=headers)
    response.raise_for_status()
    print(f"App {app_id} deleted successfully")

# Usage
delete_app("abc123xyz")
```

### TypeScript

```typescript
async function deleteApp(appId: string): Promise<void> {
  await axios.delete(
    `${BASE_URL}/apps/${appId}`,
    {
      headers: {
        Authorization: `Bearer ${API_KEY}`,
      },
    }
  );
  console.log(`App ${appId} deleted successfully`);
}

// Usage
await deleteApp('abc123xyz');
```

### cURL

```bash
# Delete an app
curl -X DELETE "${CHATDOC_STUDIO_BASE_URL}/apps/abc123xyz" \
  -H "Authorization: Bearer ${CHATDOC_STUDIO_API_KEY}"

# Response (success):
# {
#   "data": null,
#   "code": "success",
#   "type": "System",
#   "detail": null
# }

# Error response (app not found):
# {
#   "data": {},
#   "code": "not_found",
#   "type": "UserError",
#   "detail": "App not found"
# }
```

## Complete Workflow Example

### Python

```python
# Complete workflow for app management

# 1. List all apps
result = get_apps(current_page=1, page_size=50)
print(f"Found {result['total']} apps")

# 2. Filter apps by type
chat_apps = [app for app in result["items"] if app["app_type"] == 1]
extract_apps = [app for app in result["items"] if app["app_type"] == 2]
rag_apps = [app for app in result["items"] if app["app_type"] == 5]

print(f"Chat Apps: {len(chat_apps)}")
print(f"Extract Apps: {len(extract_apps)}")
print(f"RAG Apps: {len(rag_apps)}")

# 3. Delete old apps (example: delete apps created more than 90 days ago)
import time

current_time = int(time.time())
ninety_days_ago = current_time - (90 * 24 * 60 * 60)

for app in result["items"]:
    if app["created_at"] < ninety_days_ago:
        print(f"Deleting old app: {app['name']} (ID: {app['id']})")
        try:
            delete_app(app["id"])
        except Exception as e:
            print(f"Failed to delete {app['id']}: {e}")
```

### TypeScript

```typescript
// Complete workflow for app management

async function manageApps() {
  // 1. List all apps
  const result = await getApps(1, 50);
  console.log(`Found ${result.total} apps`);

  // 2. Filter apps by type
  const chatApps = result.items.filter(app => app.app_type === 1);
  const extractApps = result.items.filter(app => app.app_type === 2);
  const ragApps = result.items.filter(app => app.app_type === 5);

  console.log(`Chat Apps: ${chatApps.length}`);
  console.log(`Extract Apps: ${extractApps.length}`);
  console.log(`RAG Apps: ${ragApps.length}`);

  // 3. Delete old apps (example: delete apps created more than 90 days ago)
  const currentTime = Math.floor(Date.now() / 1000);
  const ninetyDaysAgo = currentTime - (90 * 24 * 60 * 60);

  for (const app of result.items) {
    if (app.created_at < ninetyDaysAgo) {
      console.log(`Deleting old app: ${app.name} (ID: ${app.id})`);
      try {
        await deleteApp(app.id);
      } catch (error) {
        console.error(`Failed to delete ${app.id}:`, error);
      }
    }
  }
}

manageApps();
```
