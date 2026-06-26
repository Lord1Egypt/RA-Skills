# B站 API 调用备忘

## curl 降级方案

沙箱环境 Python 的 DNS 可能不稳定（`requests` 报 `NameResolutionError`），但 `curl` 通常能正常解析。

**模式：** 用 `subprocess.run(['curl', ...])` 替代 `requests.get()`。

```python
import subprocess, json

COOKIE = 'SESSDATA=...; bili_jct=...; buvid3=...'

def curl_get(url):
    r = subprocess.run(
        ['curl', '-s', '--connect-timeout', '10', url,
         '-H', 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
         '-H', 'Referer: https://www.bilibili.com',
         '-H', f'Cookie: {COOKIE}'],
        capture_output=True, text=True, timeout=20
    )
    return json.loads(r.stdout)
```

**注意：** Cookie 中包含 `%2C` 等 URL 编码字符，curl 的 `-b` 参数有时会出错，用 `-H 'Cookie: ...'` 更可靠。

## 常用 API 端点

| 用途 | 端点 | 关键参数 |
|------|------|----------|
| 获取用户UID | `/x/web-interface/nav` | 无 |
| 收藏夹列表 | `/x/v3/fav/folder/created/list-all` | `up_mid`（真实UID，不能为0） |
| 收藏夹内容 | `/x/v3/fav/resource/list` | `media_id`, `pn`, `ps`, `order=time` |
| 视频详情 | `/x/web-interface/view` | `bvid` |
| 字幕(view接口) | 视频详情返回的 `subtitle.list[].subtitle_url` | AI生成的CC字幕 |
| 字幕(player接口) | `/x/player/wbi/v2` | `aid`, `cid` — 含UP主上传字幕 |
| 高赞评论 | `/x/v2/reply/main` | `type=1`, `oid=aid`, `mode=3` |
| 弹幕 | `/x/v2/dm/web/seg.so` | `oid=cid`, `segment_index=1`（protobuf格式） |

## 字幕获取策略

1. 先查 `/x/web-interface/view` → `data.subtitle.list[]`
2. 如果为空，查 `/x/player/wbi/v2` → `data.subtitle.subtitles[]`
3. 优先选 `lan` 含 `zh` 的字幕
4. 两个接口都没有 → 视频确实无可用字幕，降级为基于简介+评论总结

## 总结质量要求

用户要求总结**具体详细**，不要泛泛而谈：
- 基于字幕逐段提取具体操作步骤和技术细节
- 评论区有价值的信息（扩展实践、反馈意见）要纳入
- 如果没有字幕，从简介和评论推断具体内容，而不是写通用模板话
- 用中文写总结，英文作为辅助
