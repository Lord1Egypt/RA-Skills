# 抖音下载 API 参考

## 关键端点

| 端点 | 用途 | 水印 |
|------|------|------|
| `https://www.iesdouyin.com/share/video/<ID>/` | 移动端页面，提取 video_id | 无 |
| `https://aweme.snssdk.com/aweme/v1/playwm/?video_id=...` | 720p 视频下载 | 有 |
| `https://aweme.snssdk.com/aweme/v1/play/?video_id=...` | 无水印下载（需签名） | 无 |

## URL 解析规则

抖音短链接 `https://v.douyin.com/xxx/` 会 302 重定向到：

```
https://www.iesdouyin.com/share/video/<video_id_str>/?region=CN&mid=...&...
```

其中 URL 路径里的 `<video_id_str>`（纯数字，19位）是视频的公开 ID。

## video_id 提取位置

在 iesdouyin 页面 HTML 中，`video_id` 出现在 `<script>` 标签的 JSON 数据中：

```html
<script id="RENDER_DATA" type="application/json">
  {"aweme":{"detail":{"video_id":"v0d00fg10000d7pc7dvog65j2bpvg940",...
```

提取正则：
```bash
grep -o '"video_id":"[^"]*"' /tmp/dy_page.html
# 或
grep -o 'video_id=[^&"]*' /tmp/dy_page.html
```

## 请求头说明

```bash
-H "User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15"
-H "Referer: https://www.douyin.com/"
```

这两个头是必需的，否则请求会被抖音服务器拒绝（403）。

## 已知失败场景及备选方案

| 场景 | 原因 | 备选 |
|------|------|------|
| iesdouyin 页面返回空/403 | IP 被限流 | 等几秒重试或换 User-Agent |
| snssdk 返回 HTML 错误页 | video_id 过期或错误 | 重新抓取页面确认 video_id |
| 第三方 API 全部不可用 | 网络封锁/接口下线 | 使用本方案（iesdouyin + snssdk） |
