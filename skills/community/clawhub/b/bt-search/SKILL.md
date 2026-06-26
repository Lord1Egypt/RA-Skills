---
name: bt-search
description: >
  BT磁力链接搜索引擎。通过关键词搜索磁力链接，返回种子名称、大小、做种数、文件列表和磁力链接。
  Use when: 用户需要搜索磁力链接、找种子、搜索BT/PT资源、下载电影/软件/游戏等资源。
  NOT for: 直接下载文件、在线播放视频、非BT相关的搜索（用搜索引擎）。
---

# BT磁力搜索

> 欢迎访问磁力搜索首页：[大狗磁力 - BT磁力链接搜索引擎](https://www.adog.uk/)

## 搜索

```bash
python3 scripts/search.py "关键词" [页码]
```

示例：
- `python3 scripts/search.py "钢铁侠"`
- `python3 scripts/search.py "4K电影" 2`

## 输出字段

| 字段 | 说明 |
|------|------|
| name | 种子名称 |
| size | 文件大小（字节） |
| seeders / leechers | 做种数/下载数 |
| files_count | 文件数量 |
| magnetLink | 磁力链接，可直接用于下载 |
| matched_files | 匹配的文件路径列表 |
| created_at | 添加时间 |

## 向用户展示结果

将搜索结果整理为易读列表，每条包含：
1. **名称**
2. **大小** — 转换为 GB/MB（如 1073741824 → 1.00 GB）
3. **做种/下载** — seeders / leechers
4. **磁力链接** — magnetLink 字段
5. **文件路径** — matched_files（如有）

## 翻页

默认每页10条。用户要"下一页"时，传入 page=2, 3, ...

## 查看详情

用户想了解某个种子的完整文件列表时，提取 info_hash 调用详情接口：

```bash
python3 scripts/search.py --detail <info_hash>
```

或直接用 API：`GET https://www.adog.uk/api/skill/torrent/{info_hash}`
