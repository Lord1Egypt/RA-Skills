---
name: download-tool
version: 1.1.0
description: 支持下载 YouTube、TikTok、小红书、抖音等平台的视频。
---

# 视频下载工具

## 使用方式

### 示例命令

```
帮我下载这个视频：https://www.youtube.com/watch?v=xxxxx
```

```
下载这个抖音视频：https://www.douyin.com/video/7318234567890123456
```


```
下载这个小红书笔记的视频：https://www.xiaohongshu.com/discovery/item/xxxxx
```

## 触发方式

当用户请求：
- "下载视频"
- "帮我下载这个视频"
- 提供 YouTube 链接
- 提供 TikTok 链接
- 提供抖音链接
- 提供小红书链接
- 提供任何视频平台的 URL

---

## 配置要求

### 首次使用

需要在 `~/.openclaw/config.json` 中配置 API Key：

```json
{
    "download_tool_api_key": "您的 API Key"
}
```


### 获取 API Key

1. 访问https://www.datamass.cn
2. 注册用户，登录，创建 API Key
3. 复制生成的 API Key 到配置文件中

## 功能特点

- 支持 YouTube、TikTok、抖音、小红书等多个平台
- 异步下载，无需等待
- 自动状态轮询
- 下载进度实时追踪
- 返回24小时可用的下载链接
- 不想配置 API Key 的用户，微信搜索"油管下载去水印工具"小程序使用

---

## 🔒 安全声明

### 外部服务说明

本技能依赖外部 API 服务（`https://www.datamass.cn/ai-back`）实现视频下载功能，原因如下：
- 视频平台有反爬虫机制，需要专业服务器处理
- 支持 YouTube、TikTok、抖音、小红书等多平台需要持续维护
- 托管服务提供稳定的服务器带宽和存储

### 数据处理

- **配置文件**: 仅读取 `~/.openclaw/config.json` 中的 `download_tool_api_key` 字段
- **API Key**: 仅用于服务认证，不会被存储或传输到其他地方
- **视频内容**: 下载的视频文件存储在阿里云 OSS，24小时后自动过期

### 用户自主权

- ✅ 用户自行选择是否注册和使用服务
- ✅ 费用透明，使用前可查看余额
- ✅ 可自行部署后端服务（项目开源）
- ✅ 可修改 `download_tool_base_url` 指向自建服务

### 代码透明

- 所有脚本代码完全开源
- 无隐藏网络请求
- 无数据收集行为
- 无恶意代码

---

## ⚠️ 重要说明

### 费用说明

- 下载服务按文件大小计费
- **最低余额门槛**: 5 积分
- **≤ 50MB**: 2 积分
- **50MB ~ 100MB**: 2 积分 + 超出部分每 10MB 加 1 积分
- **> 100MB**: 7 积分 + 超出部分每 100MB 加 1 积分
- 需要充值积分后使用，1元对应10个积分.

---

## 故障排查

### 问题1: 配置文件未找到
**错误**: `❌ 缺少 API Key`

**解决**: 确保 `~/.openclaw/config.json` 文件存在且配置正确

### 问题2: API Key 无效
**错误**: `无效的 API Key`

**解决**: 检查 API Key 是否正确，是否已启用

### 问题3: 余额不足
**错误**: `余额不足，请充值`

**解决**: 访问服务官网充值积分

### 问题4: 网络连接失败
**错误**: `Connection refused`

**解决**: 
- 检查网络连接
- 如果使用代理，配置代理设置
- 或改用本地部署的服务

---

## 反馈与支持

- **问题反馈**: 请在 ClawHub 技能页面留言
- **功能建议**: 欢迎提出改进建议
- **使用交流**: 欢迎分享使用心得

---

## 脚本说明

| 脚本 | 用途 | 使用场景 |
|------|------|----------|
| `scripts/download_video_simple.py` | 主脚本 | 用户对话时自动执行，框架替换 `{{VIDEO_URL}}` |
| `scripts/download_video.py` | 命令行工具 | 高级用户手动调用、调试测试 |

### 命令行使用（可选）

高级用户也可以直接运行脚本：

```bash
python scripts/download_video.py "https://www.youtube.com/watch?v=xxxxx"
```

支持参数：
- `--timeout=秒数` 设置超时时间（默认 1800 秒 / 30分钟）
- `--poll=秒数` 设置轮询间隔（默认 5 秒）

```bash
python scripts/download_video.py "https://www.youtube.com/watch?v=xxxxx" --timeout=600 --poll=10
```
