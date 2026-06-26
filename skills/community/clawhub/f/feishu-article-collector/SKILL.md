---
name: feishu-article-collector
version: 1.2.0
description: |
  自动收集今日头条、微信公众号文章。抓取正文，AI 生成总结和分类，存入飞书多维表格。支持去重。
metadata:
  openclaw:
    emoji: "📰"
    requires:
      bins:
        - python3
      env:
        - FEISHU_APP_ID
        - FEISHU_APP_SECRET
        - DEEPSEEK_API_KEY
    primaryEnv: FEISHU_APP_ID
    install:
      - kind: uv
        package: requests
---

# 飞书文章收集器

收到包含今日头条或微信公众号链接的消息时，自动抓取文章、AI 总结、分类并存入飞书多维表格。

## 触发条件

当消息中包含以下域名的链接时，立即执行本技能：

- `toutiao.com`、`toutiaocdn.com`、`toutiao.io`、`snssdk.com`（今日头条）
- `mp.weixin.qq.com`（微信公众号）

## 处理方式

使用 exec 工具调用脚本，一步完成所有处理：

```bash
python3 {baseDir}/scripts/collect.py '完整的消息文本'
```

参数说明：
- 第一个参数：用户发送的完整消息文本（包含链接和其他文字）

脚本返回 JSON 结果：

成功：
```json
{"success": true, "title": "文章标题", "category": "分类", "summary": "总结", "record_id": "xxx"}
```

重复：
```json
{"success": false, "error": "该文章已收录，跳过重复链接", "url": "..."}
```

## 回复格式

根据脚本返回结果回复用户：

成功时：
> 已收录：《文章标题》
> 分类：xxx
> 总结：xxx

重复时：
> 该文章已收录，无需重复保存

失败时：
> 收录失败：错误原因

## 重要：必须调用脚本

- **严禁使用 web_fetch 抓取文章**，必须调用上面的 Python 脚本
- 脚本已内置抓取、总结、分类、写入的全部逻辑，不需要自己做任何处理
- 消息文本原样传入第一个参数，不需要自己提取 URL
- 如果脚本执行失败，将错误信息返回给用户即可

## 安装后配置

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

飞书应用需开通 `bitable:app` 权限。多维表格会在首次使用时自动创建。
