---
name: 1lou-search
description: 在1lou网站搜索影视资源并下载到群晖qBittorrent。用于手动搜索电影或电视剧。触发关键词：影视搜索
---

# 1lou影视搜索

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
用户发送以"影视搜索"开头的指令，格式：
- "影视搜索 电影 xxx" - 电影分类，保存到movie目录
- "影视搜索 电视剧集 xxx" - 电视剧分类，保存到tv目录

**示例**：
- "影视搜索 电影 疯狂动物城2"
- "影视搜索 电视剧集 不良医生"
- "影视搜索 电影 日本沉没"

**注意**：必须包含"电影"或"电视剧集"分类词。

## 工作流程

### 1. 解析搜索词
- 格式："影视搜索 [分类] [关键词]"
- 分类：电影 → 保存到movie目录；电视剧集 → 保存到tv目录

### 2. 搜索资源
- 按照域名优先级顺序尝试连接（见上方域名列表）
- 每个域名连接失败时自动切换到下一个
- 输入关键词搜索
- 选择电视剧集分类（forum-2）或电影分类

### 3. 过滤规则（重要！）
排除包含以下关键词的资源：
- 网盘
- 夸克
- 片源
- 无字

**必须在提取集数信息之前先过滤**，确保统计的集数来自有效资源。

### 4. 展示结果
格式：剧名 | 集数 | 大小 | 链接

### 5. 用户确认
等待用户确认下载哪个资源

### 6. 获取种子

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

### 7. 添加到qBittorrent
- qBittorrent地址：192.168.1.38:8085
- 账号：boring737
- 密码：Conan2015
- 电影保存路径：/volume1/EMBY/downloads/movie
- 电视剧保存路径：/volume1/EMBY/downloads/tv

### 8. 询问追剧
下载完成后，询问用户是否加入追剧清单
- 如果是电视剧集，询问时记录本次搜索使用的**关键字**
- 后续自动追剧时使用该关键字搜索

## 配置文件
- 追剧清单：/Users/bluepop/.openclaw/scripts/drama_watchlist.json

## API调用示例
```bash
# 登录qBittorrent
curl -s -c cookies.txt -X POST "http://192.168.1.38:8085/api/v2/auth/login" \
  -d "username=boring737&password=Conan2015"

# 添加种子
curl -s -b cookies.txt -X POST "http://192.168.1.38:8085/api/v2/torrents/add" \
  -F "torrent_file=@/tmp/xxx.torrent" \
  -F "savepath=/volume1/EMBY/downloads/tv"
```
