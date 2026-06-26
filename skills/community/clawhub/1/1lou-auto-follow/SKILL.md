---
name: 1lou-auto-follow
description: 管理追剧清单，自动检查并推送1lou网站的最新剧集更新。
---

# 1lou自动追剧

## 网站域名（按优先级）
1. https://1lou.me（首选）
2. https://1lou.one（备用）
3. https://1lou.icu（备用）
4. https://1lou.xyz（备用）
5. https://1lou.info（备用）
6. https://1lou.vip（备用）
7. https://1lou.pro（备用）

## 连接检测与重试
- 首次尝试连接首选域名 https://1lou.me
- 如果连接失败（超时/ERR_CONNECTION_TIMED_OUT），自动切换到下一个域名
- 切换顺序：1lou.me → 1lou.one → 1lou.icu → 1lou.xyz → 1lou.info → 1lou.vip → 1lou.pro
- 每个域名至少重试2次
- 选择第一个能够成功连接的域名进行搜索和下载

**重要：检测网站可用性时，只检测以下域名，不要自行尝试其他域名：**
- 1lou.me（首选）
- 1lou.one
- 1lou.icu
- 1lou.xyz
- 1lou.info
- 1lou.vip
- 1lou.pro
- 不要检测：1lou.com, 1lou.cc, 1lou.net（这些域名不存在！）

## 触发条件
- 定时任务触发（每天凌晨4点）
- 用户询问追剧相关功能

## 追剧清单文件
路径：`/Users/bluepop/.openclaw/scripts/drama_watchlist.json`

格式：
```json
{
  "drama_list": [
    {
      "name": "剧名",
      "downloaded_episodes": [1, 2, 3],
      "search_keyword": "搜索用的关键字"
    }
  ]
}
```

**重要**：search_keyword是成功下载时使用的搜索关键字，后续自动追剧时使用该关键字搜索。

## 工作流程（定时任务）

### 1. 检查清单
- 读取drama_watchlist.json
- 如果为空，回复"追剧清单为空，任务跳过"

### 2. 搜索更新
- 按以下顺序尝试连接：1lou.me → 1lou.one → 1lou.icu → 1lou.xyz → 1lou.info → 1lou.vip → 1lou.pro
- 使用第一个能够成功连接的域名
- 对清单中的每个剧进行搜索
- **使用search_keyword字段进行搜索**（不是用name）

### 3. 过滤规则（重要！必须先过滤再计数）
**先过滤，后计数！**

排除包含以下关键词的资源：
- 网盘
- 夸克
- 片源
- 无字

**过滤后再提取集数信息**，计算可下载的新集数。

### 4. 推送结果
- 格式：剧名 | 集数 | 大小 | 链接
- 无论是否有新资源，都要告知用户检查结果

### 5. 用户确认下载后，添加种子到qBittorrent

**第一步：先尝试curl命令下载**
```bash
curl -sL -o /tmp/xxx.torrent "https://1lou.one/attach-download-xxxxx.htm"
```
- 如果curl成功，直接用种子文件添加到qBittorrent
- 如果curl失败，尝试其他域名或用浏览器下载
- **重试：最多3次**

**第二步：使用浏览器下载**
1. 用浏览器打开种子下载链接
2. 检查以下位置（按顺序）：
   - 临时目录：`/var/folders/0g/tdp7p0zn7x3gbbtyysptxrvm0000gn/T/playwright-artifacts-*/`
   - 下载目录：`/Users/bluepop/Downloads/`
3. 找到最新的BitTorrent文件
4. 复制到Downloads目录（如在临时目录）
5. 用找到的文件添加到qBittorrent
- **重试：最多3次**

### 6. 更新追剧清单
下载完成后，更新drama_watchlist.json中的downloaded_episodes

## 加入追剧清单
1. 用户手动搜索并下载某剧集
2. 下载完成后，询问用户是否加入追剧
3. 用户确认后，更新drama_watchlist.json
   - 记录downloaded_episodes
   - **记录search_keyword**（本次搜索使用的关键字）

## 退出追剧清单
用户手动告诉退出某剧集，从drama_watchlist.json中移除

## 定时任务配置
- 任务名称：1lou追剧推送
- 执行时间：每天凌晨4:00
- 任务ID：bd2e8e58-2c7c-4cbc-879f-c7a546793efb

## 服务配置
- 1lou：https://1lou.me（首选）→ 1lou.one → 1lou.icu → 1lou.xyz → 1lou.info → 1lou.vip → 1lou.pro
- qBittorrent：192.168.1.38:8085
- n8n：192.168.1.38:5678
