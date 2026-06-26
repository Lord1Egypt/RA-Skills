# Feishu Article Collector

OpenClaw Skill：从今日头条、微信公众号抓取文章，AI 自动生成总结和分类，存入飞书多维表格。

## 功能

- 支持今日头条（toutiao.com、snssdk.com 等）和微信公众号（mp.weixin.qq.com）
- 自动提取标题和正文
- DeepSeek AI 生成 200-300 字总结，自动分类（科技/财经/娱乐/健康/教育/体育/其他）
- 通过文章 ID 去重，避免重复收录
- 自动识别数据来源（今日头条/微信公众号）
- 多维表格自动发现或创建，无需手动配置

## 安装

```bash
npx clawhub install feishu-article-collector
```

## 配置

在 OpenClaw 的 `openclaw.json` 中配置环境变量：

```json
{
  "env": {
    "FEISHU_APP_ID": "飞书自建应用 App ID",
    "FEISHU_APP_SECRET": "飞书自建应用 App Secret",
    "DEEPSEEK_API_KEY": "DeepSeek API Key"
  }
}
```

飞书应用需开通 `bitable:app` 权限。

多维表格会在首次使用时自动创建（名为"今日头条文章收藏"），包含字段：文章标题、文章链接、文章ID、分享人、分享时间、分类标签、备注（AI总结）、已读。

## 依赖

- Python 3
- requests（通过 `uv` 自动安装）

## 使用方式

安装并配置后，向绑定的飞书机器人发送包含今日头条或微信公众号链接的消息，即可自动收录。
