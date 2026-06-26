# 媒体库操作详细指南

## 扫描 vs 刷新 vs 刮削 — 区别说明

向用户说明操作差异，避免误操作：

| 操作 | 说明 | 耗时 | 端点 |
|------|------|------|------|
| **快速扫描** | 仅检测新增/删除的文件 | 快（秒级） | `POST /Library/Refresh` |
| **元数据刷新** | 重新从网络抓取海报、简介等 | 慢（分钟~小时） | `POST /Items/{id}/Refresh?MetadataRefreshMode=FullRefresh` |
| **强制覆盖刷新** | 覆盖已有元数据，完全重新抓取 | 最慢 | 同上，加 `&ReplaceAllMetadata=true` |

**推荐流程**：新增文件后 → 先快速扫描 → 如果元数据不对再单独刷新该条目

---

## 媒体库扫描操作

### 触发全库扫描
```
POST /Library/Refresh?api_key=<KEY>
```
- 异步执行，接口立即返回 `204 No Content`
- 通过 `GET /ScheduledTasks` 查看 `RefreshLibrary` 任务状态

### 查看扫描进度
```
GET /ScheduledTasks?api_key=<KEY>
```
找到 `Key = "RefreshLibrary"` 的任务，查看：
- `State`: `Running` / `Idle`
- `CurrentProgressPercentage`: 进度百分比
- `LastExecutionResult.Status`: `Completed` / `Failed`

---

## 单条目元数据操作

### 先搜索找到 ItemId
```
GET /Items?SearchTerm=<关键词>&api_key=<KEY>
```
返回的每个 Item 包含 `Id` 字段，即 itemId。

### 刷新单条目元数据
```
POST /Items/{itemId}/Refresh
  ?MetadataRefreshMode=FullRefresh
  &ImageRefreshMode=FullRefresh
  &api_key=<KEY>
```

### 强制覆盖元数据（慎用）
```
POST /Items/{itemId}/Refresh
  ?MetadataRefreshMode=FullRefresh
  &ImageRefreshMode=FullRefresh
  &ReplaceAllMetadata=true
  &ReplaceAllImages=true
  &api_key=<KEY>
```

---

## 媒体库统计信息

```
GET /Items/Counts?api_key=<KEY>
```

返回示例：
```json
{
  "MovieCount": 245,
  "SeriesCount": 32,
  "EpisodeCount": 1204,
  "MusicAlbumCount": 0,
  "SongCount": 0,
  "BookCount": 0
}
```

---

## 查找"问题媒体"

### 找没有元数据的电影
```
GET /Items
  ?IncludeItemTypes=Movie
  &Fields=Overview,Genres
  &Recursive=true
  &api_key=<KEY>
```
遍历结果，找 `Overview` 为空或 `Genres` 为空的条目。

### 找没有海报的媒体
```
GET /Items
  ?IncludeItemTypes=Movie,Series
  &Recursive=true
  &ImageTypes=Primary
  &api_key=<KEY>
```
对比未返回图片的条目。

---

## 集合与播放列表管理

### 获取所有集合
```
GET /Items?IncludeItemTypes=BoxSet&Recursive=true&api_key=<KEY>
```

### 创建集合
```
POST /Collections?Name=<集合名>&api_key=<KEY>
```

### 向集合添加媒体
```
POST /Collections/{collectionId}/Items?Ids=<itemId1,itemId2>&api_key=<KEY>
```

---

## Linux 系统层面的辅助操作

如果用户需要在系统层面操作（需 SSH 权限），可以配合以下命令：

```bash
# 查看 Emby 服务状态
systemctl status emby-server

# 重启 Emby 服务
sudo systemctl restart emby-server

# 查看 Emby 实时日志
journalctl -u emby-server -f

# 查看 Emby 数据目录大小
du -sh /var/lib/emby/

# 查看媒体目录权限
ls -la /path/to/media/
```

Emby 数据目录通常在：
- Debian/Ubuntu: `/var/lib/emby/` 或 `~/.local/share/emby/`
- 配置文件: `/etc/emby-server/`