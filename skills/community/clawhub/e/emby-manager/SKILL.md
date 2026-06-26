---
name: emby-manager
description: 管理运行在 Linux NAS 上的 Emby 媒体服务器。当用户提到 Emby、媒体库、NAS 娱乐管理、刮削元数据、查看播放记录、管理用户权限、检查服务器状态等任何与 Emby 相关的操作时，必须使用此 Skill。即使用户只是问"帮我看看 Emby 状态"、"媒体库扫描一下"、"谁在看片"这类口语化表达，也应触发此 Skill。
---

# Emby 媒体服务器管理 Skill

## 首次使用：获取连接信息

如果对话中没有服务器地址和 API Key，**必须先向用户索取**：

```
请提供以下信息：
1. Emby 服务器地址（如 http://192.168.1.100:8096）
2. API Key（在 Emby 后台：Dashboard → Advanced → API Keys → 新建）
```

获取后，在整个对话中记住这两个值，不要重复询问。

---

## 标准 API 调用格式

```javascript
// 所有请求统一使用此格式
const BASE = "http://<server>:<port>"  // 用户提供
const API_KEY = "<api_key>"            // 用户提供

// GET 请求
fetch(`${BASE}/endpoint?api_key=${API_KEY}`)

// POST 请求
fetch(`${BASE}/endpoint?api_key=${API_KEY}`, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({...})
})
```

> 详细 API 端点速查 → 阅读 `references/api-guide.md`

---

## 四大功能模块

### 1. 媒体库管理
**触发词**：扫描、刷新、刮削、元数据、整理、媒体库

工作流程：
1. 先调用 `GET /Library/MediaFolders` 列出所有媒体库
2. 根据用户意图选择操作（全库扫描 / 单库刷新 / 刮削元数据）
3. 触发操作后，告知用户任务已提交，可通过计划任务接口查看进度

常用操作速查：
| 操作 | 方法 | 端点 |
|------|------|------|
| 全库扫描 | POST | `/Library/Refresh` |
| 查看媒体库列表 | GET | `/Library/MediaFolders` |
| 刷新单个条目元数据 | POST | `/Items/{itemId}/Refresh` |
| 查看计划任务状态 | GET | `/ScheduledTasks` |
| 运行指定计划任务 | POST | `/ScheduledTasks/Running/{taskId}` |

> 完整操作细节 → 阅读 `references/media-ops.md`

---

### 2. 用户与权限管理
**触发词**：用户、账号、权限、谁能看、新增用户、禁用

工作流程：
1. `GET /Users` 获取所有用户列表
2. 按需查看/修改单个用户：`GET /Users/{userId}`
3. 修改权限时使用 `POST /Users/{userId}/Policy`

展示用户信息时，重点呈现：用户名、是否管理员、是否禁用、最后活跃时间

---

### 3. 播放记录与统计查询
**触发词**：播放记录、谁在看、最近看了什么、观看历史、活跃会话

工作流程：
1. **实时会话**：`GET /Sessions` — 查看当前正在播放的内容
2. **播放活动**：`GET /user_usage_stats/user_activity`（需 Emby Stats 插件）
3. **最近播放**：`GET /Users/{userId}/Items/Latest`
4. **媒体统计**：`GET /Items/Counts`

展示会话信息时，重点呈现：用户名、正在播放的内容、播放进度、客户端类型、IP 地址

---

### 4. 服务器监控与健康检查
**触发词**：状态、健康、监控、性能、内存、CPU、转码、日志

工作流程：
1. `GET /System/Info` — 获取服务器基本信息（版本、操作系统、内存）
2. `GET /Sessions` — 查看活跃连接数和转码任务
3. `GET /ScheduledTasks` — 查看后台任务队列
4. `GET /System/Logs` — 获取最新日志列表

健康检查时，综合呈现：
- 服务器版本 & 运行时间
- 当前活跃会话数 / 转码流数量
- 系统内存使用情况
- 是否有失败的计划任务

> 排查问题时 → 阅读 `references/troubleshoot.md`

---

## 输出规范

- 数据以**表格或结构化列表**呈现，不要直接 dump JSON
- 操作完成后，说明**下一步可以做什么**
- 涉及破坏性操作（删除、修改权限）时，**先向用户确认**
- API 调用失败时，给出**具体错误原因**并引导排查

---

## 快速参考

```
媒体库相关  → references/api-guide.md#媒体库
用户相关    → references/api-guide.md#用户
统计相关    → references/api-guide.md#统计
排查问题    → references/troubleshoot.md
```