---
name: douyin-download
description: |
  抖音无水印视频下载工具。当用户发送抖音视频链接时，自动解析并下载无水印版本，上传到云盘发给用户。
  Use cases:
  - 用户发送抖音链接
  - "下载这个视频"
  - "帮我保存抖音视频"
  - "解析抖音链接"
metadata:
  openclaw:
    emoji: "🎵"
---

# 抖音无水印视频下载 Skill

## Trigger

当用户发送抖音视频链接时激活。

## Workflow

```
用户发送抖音链接
  → Step 1: 调用 parse-douyin.py 解析视频
  → Step 2: 上传视频到云盘
  → Step 3: 返回下载链接给用户
```

## Commands

### Step 1: 解析并下载

```bash
source ~/.agent-reach-venv/bin/activate
python3 ~/.qclaw/workspace/skills/douyin-download/parse-douyin.py <抖音链接>
```

**支持格式：**
- `https://www.douyin.com/video/1234567890123456789`
- `https://v.douyin.com/xxxxx?modal_id=1234567890123456789`
- 任意包含 19 位数字视频 ID 的链接

### Step 2: 上传到云盘

```bash
PORT=${AUTH_GATEWAY_PORT:-19000}
curl -s -X POST http://localhost:$PORT/proxy/qclaw-cos/upload \
  -H 'Content-Type: application/json' \
  -d '{"localPath":"<视频路径>","conflictStrategy":"ask"}'
```

### Step 3: 返回结果

直接输出云盘返回的 `message` 字段内容。

## Example

**User Input:**
```
https://www.douyin.com/video/7611512807091178804
```

**AI Actions:**
1. 执行解析脚本
2. 上传到云盘
3. 输出云盘返回的链接

**Output:**
```
✅ 视频已保存！

📎 douyin_7611512807091178804.mp4 (104.2 MB)
🔗 下载链接: https://jsonproxy.3g.qq.com/urlmapper/xxxxx

云端保留 30 天，请及时保存~
```

## Notes

- 视频保存在 `/tmp/douyin_<video_id>.mp4`
- 云端保留 30 天后自动清理
- 无需 Cookie，已验证可直接解析公开视频
