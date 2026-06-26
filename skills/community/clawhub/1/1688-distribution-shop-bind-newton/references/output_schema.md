# 输出格式规范

## JSON 输出结构

所有命令统一输出 JSON，通过 stdout 返回：

```json
{
  "success": true,
  "markdown": "展示给用户的内容（Markdown 格式）",
  "data": {
    "flow": {},
    "step": {},
    "stage": "in_progress",
    "channel": "douyin",
    "appKey": "xxx"
  },
  "browser_action": "open_url",
  "browser_params": {
    "url": "https://...",
    "wait_for_login": true,
    "timeout": 120
  },
  "flow_completed": false
}
```

## 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| success | bool | 操作是否成功 |
| markdown | string | 展示给用户的内容（Markdown 格式） |
| data | dict | 结构化数据，包含流程状态、步骤信息等 |
| browser_action | string | 浏览器操作指令（如有），牛顿客户端拦截执行 |
| browser_params | dict | 浏览器操作参数 |
| flow_completed | bool | 绑店流程是否已全部完成 |

## Exit Code 约定

| Exit Code | 含义 |
|-----------|------|
| 0 | 成功（success=true） |
| 1 | 参数错误或用法错误 |
| 2 | 认证失败（AK 未配置或签名无效） |
| 3 | 业务异常（服务端返回错误） |
| 4 | 网络异常（连接失败或超时） |

## browser_action 类型

| action | 说明 | 参数 |
|--------|------|------|
| open_url | 打开 URL | url, wait_for_login, timeout |
| wait_for_login | 等待登录完成 | timeout |
| get_page_info | 获取页面信息 | poll_interval, max_attempts |
| close_browser | 关闭浏览器 | — |

## 埋点日志

埋点数据通过 stderr 输出，格式为 JSON，包含 `_tracker: true` 标识字段。
牛顿客户端或 ClawHub 平台负责采集 stderr 中的埋点数据。
