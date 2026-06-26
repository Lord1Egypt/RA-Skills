---
name: douyin-user-videos
version: 1.0.0
author: xueai-portal
description: 获取抖音博主的视频列表
triggers:
  - douyin
  - 抖音
  - 抖音视频
  - douyin videos
  - 抖音博主
dependencies: []
tools:
  - douyin_get_user_videos
---

# 抖音用户视频查询 Skill

获取指定抖音用户主页的视频列表。

## Features

- 根据抖音用户主页 URL 获取视频列表
- 返回视频描述和发布时间
- 支持配置环境变量自动获取 apikey 和 cookie

## Setup

### 配置环境变量

在 OpenClaw 配置中添加环境变量（`~/.openclaw/openclaw.json`）：

```json
{
  "skills": {
    "douyin-user-videos": {
      "env": {
        "DOUYIN_API_KEY": "用户的GUID-apiKey",
        "DOUYIN_COOKIE": "抖音Cookie"
      }
    }
  }
}
```

或者通过命令行设置：
```bash
export DOUYIN_API_KEY="用户的GUID-apiKey"
export DOUYIN_COOKIE="抖音Cookie"
```

### apikey 说明

- apikey 是用户在学AI门户注册后获得的 GUID
- 每个用户有唯一的 apikey，用于计费和身份验证

## Usage Examples

### 查询抖音用户视频

User: "获取 https://www.douyin.com/user/MS4wLjABAAAAxxx 的视频列表"
User: "这个抖音博主发了哪些视频"

Action:
1. 从用户消息中解析抖音主页 URL
2. 调用 douyin_get_user_videos 工具（自动使用环境变量中的 apikey 和 cookie）
3. 格式化返回视频列表

## Tools

### douyin_get_user_videos

获取抖音用户的视频列表。

**Parameters:**
- `url` (string, required): 抖音用户主页 URL，格式如 https://www.douyin.com/user/MS4wLjABAAAAxxx

**环境变量（自动使用）：**
- `DOUYIN_API_KEY`: 用户的 API Key (GUID)
- `DOUYIN_COOKIE`: 抖音登录 Cookie

**Returns:**
```json
{
  "success": true,
  "message": "获取视频列表成功",
  "data": [
    {
      "desc": "视频描述内容",
      "createTime": 1774504047,
      "beijingTime": "2026/3/26 13:47:27"
    }
  ]
}
```

## Error Handling

- **无效 URL**: 提示用户检查抖音链接格式
- **API Key 无效**: 提示用户检查 DOUYIN_API_KEY 配置
- **Cookie 无效**: 提示用户更新 DOUYIN_COOKIE
- **积分不足**: 提示用户充值积分

## Notes

- Cookie 来自抖音网页登录状态，需要定期更新，获取方式：https://my.feishu.cn/wiki/HbTpwSDMMiu4mUkCsjwcXgCWn7Z
- API Key 是用户的唯一标识，获取方式：https://my.feishu.cn/wiki/HbTpwSDMMiu4mUkCsjwcXgCWn7Z
