# Emby API 速查手册

## 认证方式

Emby 支持两种认证方式，统一使用 **Query String** 方式最简单：

```
GET http://<host>:<port>/System/Info?api_key=<YOUR_API_KEY>
```

默认端口：`8096`（HTTP） / `8920`（HTTPS）

---

## 端点速查表

### 系统 & 健康

| 功能 | 方法 | 端点 | 关键返回字段 |
|------|------|------|-------------|
| 服务器信息 | GET | `/System/Info` | `Version`, `OperatingSystem`, `TotalPhysicalMemory` |
| 公开系统信息 | GET | `/System/Info/Public` | 无需认证 |
| 系统日志列表 | GET | `/System/Logs` | `Name`, `DateCreated`, `Size` |
| 获取日志内容 | GET | `/System/Logs/Log?name=<logname>` | 纯文本 |
| 重启服务器 | POST | `/System/Restart` | ⚠️ 谨慎操作 |

### 媒体库

| 功能 | 方法 | 端点 | 说明 |
|------|------|------|------|
| 列出所有媒体库 | GET | `/Library/MediaFolders` | 返回 Items 数组 |
| 全库刷新扫描 | POST | `/Library/Refresh` | 异步，立即返回 |
| 获取媒体数量统计 | GET | `/Items/Counts` | MovieCount, SeriesCount 等 |
| 搜索媒体 | GET | `/Items?SearchTerm=<keyword>&Limit=20` | 支持模糊搜索 |
| 获取最新入库 | GET | `/Items?SortBy=DateCreated&SortOrder=Descending&Limit=10` | |
| 刷新单项元数据 | POST | `/Items/{itemId}/Refresh?MetadataRefreshMode=FullRefresh&ImageRefreshMode=FullRefresh` | |
| 删除媒体条目 | DELETE | `/Items/{itemId}` | ⚠️ 会删除文件 |

### 用户管理

| 功能 | 方法 | 端点 | 说明 |
|------|------|------|------|
| 获取所有用户 | GET | `/Users` | 返回用户数组 |
| 获取指定用户 | GET | `/Users/{userId}` | |
| 创建用户 | POST | `/Users/New` | Body: `{"Name": "username"}` |
| 修改用户策略 | POST | `/Users/{userId}/Policy` | 权限控制 |
| 删除用户 | DELETE | `/Users/{userId}` | ⚠️ 不可恢复 |
| 获取当前用户 | GET | `/Users/Me` | |

**Policy 常用字段**：
```json
{
  "IsAdministrator": false,
  "IsDisabled": false,
  "EnableRemoteAccess": true,
  "EnableLiveTvAccess": true,
  "EnableMediaPlayback": true,
  "EnableAudioPlaybackTranscoding": true,
  "EnableVideoPlaybackTranscoding": true
}
```

### 会话 & 播放

| 功能 | 方法 | 端点 | 关键返回字段 |
|------|------|------|-------------|
| 所有活跃会话 | GET | `/Sessions` | `UserName`, `NowPlayingItem`, `PlayState` |
| 强制停止播放 | DELETE | `/Sessions/{sessionId}/Playing` | |
| 用户最近播放 | GET | `/Users/{userId}/Items/Latest?Limit=10` | |
| 用户播放进度 | GET | `/Users/{userId}/Items?IsPlayed=true` | |

**会话对象关键字段解析**：
```json
{
  "UserName": "用户名",
  "Client": "客户端类型（如 Emby Web）",
  "RemoteEndPoint": "客户端IP",
  "NowPlayingItem": {
    "Name": "正在播放的标题",
    "Type": "Movie/Episode",
    "SeriesName": "剧集名（如果是剧集）"
  },
  "PlayState": {
    "PositionTicks": "当前位置（需除以10000000得秒数）",
    "IsPaused": false
  },
  "TranscodingInfo": {
    "IsVideoDirect": true,
    "IsAudioDirect": false,
    "Framerate": 24.0
  }
}
```

### 计划任务

| 功能 | 方法 | 端点 | 说明 |
|------|------|------|------|
| 获取所有任务 | GET | `/ScheduledTasks` | |
| 运行指定任务 | POST | `/ScheduledTasks/Running/{taskId}` | |
| 停止指定任务 | DELETE | `/ScheduledTasks/Running/{taskId}` | |

**常见 taskId**（通过 GET /ScheduledTasks 查询 `Key` 字段获取）：
- `RefreshLibrary` — 扫描媒体库
- `CleanupCollectionAndPlaylistMedia` — 清理集合
- `CleanDatabase` — 清理数据库

---

## 常用查询参数

搜索/过滤 Items 时常用参数：

| 参数 | 说明 | 示例值 |
|------|------|--------|
| `IncludeItemTypes` | 限定媒体类型 | `Movie`, `Series`, `Episode` |
| `SortBy` | 排序字段 | `DateCreated`, `SortName`, `Runtime` |
| `SortOrder` | 排序方向 | `Ascending`, `Descending` |
| `Limit` | 返回数量 | `20` |
| `StartIndex` | 分页偏移 | `0` |
| `Fields` | 指定返回字段（减少数据量） | `Overview,Genres,Studios` |
| `Filters` | 过滤条件 | `IsPlayed`, `IsUnplayed`, `IsFavorite` |

---

## 时间单位说明

Emby API 中时间使用 **Ticks**（100纳秒单位）：
- `1秒 = 10,000,000 ticks`
- 转换：`秒数 = ticks / 10000000`
- 转换为 `mm:ss`：`Math.floor(seconds/60) + ':' + (seconds%60).toString().padStart(2,'0')`