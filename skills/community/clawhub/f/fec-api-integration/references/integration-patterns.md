# API integration implementation mode

## Typed Fetch client

```ts
export class ApiError extends Error {
  constructor(
    public readonly status: number,
    public readonly body: unknown,
  ) {
    super(`API request failed, status code ${status}`);
  }
}

export async function requestJson<T>(
  path: string,
  init: RequestInit = {},
): Promise<T> {
  const response = await fetch(`${import.meta.env.VITE_API_URL}${path}`, {
    ...init,
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
      ...init.headers,
    },
    credentials: "include",
  });

  if (!response.ok) {
    const body = await response.json().catch(() => null);
    throw new ApiError(response.status, body);
  }

  if (response.status === 204) return undefined as T;
  return response.json() as Promise<T>;
}
```

## User side error mapping

```ts
export function getApiMessage(error: unknown): string {
  if (!(error instanceof ApiError)) return "The operation failed, please try again later.";

  if (error.status === 401) return "Please log in again.";
  if (error.status === 403) return "You do not have permission to perform this operation.";
  if (error.status === 404) return "The requested resource no longer exists.";
  if (error.status === 409) return "This change conflicts with the latest data.";
  if (error.status === 422) return "Please check the red fields.";
  if (error.status === 429) return "The request is too frequent, please try again later.";

  return "The service is temporarily unavailable, please try again later.";
}
```

## Upload selection

| Requirements | Recommended solutions |
| ---------------- | ----------------------------- |
| Avatar or CSV | Multipart request |
| Large video or archive file | Pre-signed direct transfer |
| Large files in weak network environment | Fragmented breakpoint resume download |
| Compliance scanning before warehousing | Uploading through API intermediary (including size limit) |

## Real-time communication selection

| Requirements | Recommended solutions |
| -------------------- | ------------------------- |
| Task progress or notification | SSE (Server-Sent Events) |
| Chat, Presence, Collaboration | WebSocket |
| Status polling every few seconds | Scheduled polling (Polling) |
| Server-side AI Token stream | SSE or fetch streaming response |

## Review Checklist

- Centralized management of API addresses and credentials.
- The client needs to handle 204, non-JSON errors, cancellation and offline status.
- The Token refresh mechanism cannot trigger request storms.
- Components should consume hooks/domain functions rather than calling raw fetch directly.
- Uploads and live streams need to expose progress, cancellation, failure and retry status.
