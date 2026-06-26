# API 集成实现模式

## 类型化 Fetch 客户端

```ts
export class ApiError extends Error {
  constructor(
    public readonly status: number,
    public readonly body: unknown,
  ) {
    super(`API 请求失败，状态码 ${status}`);
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

## 用户端错误映射

```ts
export function getApiMessage(error: unknown): string {
  if (!(error instanceof ApiError)) return "操作失败，请稍后重试。";

  if (error.status === 401) return "请重新登录。";
  if (error.status === 403) return "您没有权限执行此操作。";
  if (error.status === 404) return "请求的资源已不存在。";
  if (error.status === 409) return "此变更与最新数据冲突。";
  if (error.status === 422) return "请检查标红字段。";
  if (error.status === 429) return "请求过于频繁，请稍后再试。";

  return "服务暂不可用，请稍后重试。";
}
```

## 上传选型

| 需求             | 推荐方案                      |
| ---------------- | ----------------------------- |
| 小头像或 CSV     | Multipart 请求                |
| 大视频或归档文件 | 预签名直传                    |
| 弱网环境大文件   | 分片断点续传                  |
| 入库前合规扫描   | 经 API 中介上传（含大小限制） |

## 实时通信选型

| 需求                 | 推荐方案                  |
| -------------------- | ------------------------- |
| 任务进度或通知       | SSE（Server-Sent Events） |
| 聊天、在线状态、协作 | WebSocket                 |
| 数秒一次的状态轮询   | 定时轮询（Polling）       |
| 服务端 AI Token 流   | SSE 或 fetch 流式响应     |

## 审查清单

- API 地址和凭证集中管理。
- 客户端需处理 204、非 JSON 错误、取消和离线状态。
- Token 刷新机制不能引发请求风暴。
- 组件应消费 hooks/领域函数，而非直接调用原始 fetch。
- 上传和实时流需暴露进度、取消、失败和重试状态。
