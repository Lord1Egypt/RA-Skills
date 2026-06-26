---
name: bee
description: 视频全流程自动化：下载 → 截封面 → OSS上传 → 蚁小二多平台分发 → 飞书多维表格记录。发一个视频链接就能跑完全程。
metadata:
  openclaw:
    emoji: 🐝
    requires:
      bins: [ffmpeg, ffprobe]
      env: [OSS_ACCESS_KEY_ID, OSS_ACCESS_KEY_SECRET, OSS_BUCKET_NAME, OSS_ENDPOINT]
---

# 🐝 Bee — 视频全流程自动化

一条链接，全自动搞定：下载 → 封面 → OSS → 多平台发布 → 飞书记录。

## 环境变量

| 变量 | 说明 | 必填 |
|------|------|------|
| `OSS_ACCESS_KEY_ID` | 阿里云 AccessKey ID | ✅ |
| `OSS_ACCESS_KEY_SECRET` | 阿里云 AccessKey Secret | ✅ |
| `OSS_BUCKET_NAME` | OSS Bucket 名称 | ✅ |
| `OSS_ENDPOINT` | OSS Endpoint（如 oss-cn-hangzhou.aliyuncs.com） | ✅ |
| `OSS_PREFIX` | OSS 路径前缀（默认 `bee/`） | |
| `YIXIAOER_TOKEN` | 蚁小二 API Token（发布用） | 发布时需要 |

## 飞书多维表格

默认配置在脚本头部：
- App Token: `Lv3fbmpWGacqhosSRtXct9EnnVd`
- Table ID: `tblWsUQPqlAYsnV3`

## 使用方式

### 自然语言（推荐）

直接跟 Agent 说：
- "帮我处理这个视频：https://v.douyin.com/xxxxx"
- "把这个视频发到所有平台"
- "下载这个视频存到OSS"

### 命令行

```bash
# 完整流程：下载 → OSS → 蚁小二 → 飞书
python3 scripts/bee.py run "视频链接或本地路径" --title "标题" --publish 小桃犟 --tags '["标签1"]'

# 只下载 + OSS
python3 scripts/bee.py run "视频链接或本地路径" --title "标题"

# 只上传本地视频到 OSS + 记录
python3 scripts/bee.py run /path/to/video.mp4 --title "我的视频"

# 查看蚁小二账号
python3 scripts/bee.py accounts

# 查看发布状态
python3 scripts/bee.py status <taskSetId>
```

### 参数

| 参数 | 说明 |
|------|------|
| `--title` | 视频标题（不填则用原始标题） |
| `--desc` | 视频描述 |
| `--tags` | 标签 JSON 数组，如 `'["搞笑","动画"]'` |
| `--publish` | 蚁小二发布目标（账号名/分组名），不填则跳过发布 |
| `--platform` | 指定平台（抖音/小红书/视频号），不填则发到目标下所有平台 |
| `--draft` | 存草稿不发布 |
| `--no-feishu` | 跳过飞书记录 |
| `--no-oss` | 跳过 OSS 上传 |
| `--cover` | 自定义封面图路径（不填则自动从视频截取） |

## 流程图

```
输入（链接/文件）
    │
    ▼
[1] 下载视频（支持抖音/本地文件/URL）
    │
    ▼
[2] 视频处理（ffprobe 获取信息 + ffmpeg 截封面）
    │
    ▼
[3] 上传到阿里云 OSS
    │
    ▼
[4] 蚁小二多平台发布（可选）
    │
    ▼
[5] 飞书多维表格记录
    │
    ▼
输出 JSON 结果
```
