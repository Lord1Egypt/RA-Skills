# B站收藏夹API 参考

## 端点

```
GET https://api.bilibili.com/x/v3/fav/resource/list
```

## 参数

| 参数 | 类型 | 说明 | 限制 |
|------|------|------|------|
| `media_id` | int | 收藏夹ID（URL中 `fid=` 后的数字） | 必填 |
| `ps` | int | 每页数量 | **最大20**，超过返回 `code=-400`「请求错误」 |
| `pn` | int | 页码 | 默认1 |

## 认证

- **公开收藏夹**：无需Cookie，直接GET即可
- **私有收藏夹**：需要带B站登录态Cookie

## 响应结构

```json
{
  "code": 0,
  "message": "OK",
  "data": {
    "info": { ... },
    "medias": [
      {
        "id": 116366820508713,       // ← avid（用于去重追踪）
        "bvid": "BV1rPDkB7ESC",      // ← BV号（可直接用于转录）
        "bv_id": "BV1rPDkB7ESC",     // 部分响应用这个字段名
        "title": "视频标题",
        "duration": 298,             // 时长（秒）
        "upper": {
          "name": "UP主名"
        },
        "pubtime": 1775616958,       // 发布时间戳
        "fav_time": 1779933181       // 收藏时间戳
      }
    ],
    "has_more": false               // 是否有下一页
  }
}
```

## 注意点

### ps参数上限
`ps` 最大只支持 **20**。设 `ps=50` 会返回：
```json
{"code": -400, "message": "请求错误"}
```
如果收藏夹超过20个视频，需要分页请求（检查 `has_more` 字段）。

### avid vs bvid
- `id` = avid（数字ID），适合用于**去重追踪**
- `bvid` / `bv_id` = BV号（字符串），用于**构建转录URL**
- 部分API响应用 `bvid`，部分用 `bv_id`，建议同时检查两个字段

### 公开 vs 私有
公开收藏夹的API完全开放，无需Cookie。这个skill的扫描脚本使用公开访问。

### curl -L 陷阱
不要给B站API加 `-L`（跟随重定向）参数，会导致返回非JSON内容：
```
curl -s -L "https://api.bilibili.com/x/v3/fav/resource/list?media_id=xxx&ps=20"
# 返回：{"code":-400,"message":"请求错误"}
```

## curl 测试示例

```bash
# 获取收藏夹内容（公开）
curl -s "https://api.bilibili.com/x/v3/fav/resource/list?media_id=3972051046&ps=20&pn=1"

# 带Cookie访问（私有收藏夹）
curl -s -b /tmp/cookies.txt "https://api.bilibili.com/x/v3/fav/resource/list?media_id=xxx&ps=20&pn=1"
```

## Cookie 提取（私有收藏夹/会员视频用）

通过 yt-dlp 导出 Chromium Cookie：
```bash
CHROMIUM_PATH="$HOME/snap/chromium/common/chromium"
yt-dlp \
  --cookies-from-browser "chromium:$CHROMIUM_PATH" \
  --cookies /tmp/bili_cookies.txt \
  --skip-download \
  --print title \
  "https://www.bilibili.com/video/BV1rPDkB7ESC/"
```
⚠️ `--cookies` 参数读写双用，每次调用覆盖目标文件，不要在同一tick多次调用。

通过 yt-dlp 导出 Windows Edge Cookie：
```bash
WIN_USER=$(ls /mnt/c/Users/ | grep -v "Public\|Default\|All Users" | head -1)
yt-dlp \
  --cookies-from-browser "edge:C:/Users/$WIN_USER/AppData/Local/Microsoft/Edge/User Data" \
  --cookies /tmp/bili_cookies.txt \
  --skip-download \
  --print title \
  "https://www.bilibili.com/video/BV1rPDkB7ESC/"
```
