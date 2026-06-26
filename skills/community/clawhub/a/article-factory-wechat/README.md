# article-factory-wechat 使用指南

## 简介

article-factory-wechat 是一个用于生成和发布微信公众号文章的专业技能，支持 HTML 格式文章生成、图片处理和自动提交到微信公众号平台的完整 7 步 SOP。

## 目录结构

```
article-factory-wechat/
├── scripts/
│   ├── submit-draft.js       # 提交草稿到微信公众号
│   └── temp-convert.js       # HTML 转图片工具
├── steps/                   # 7 步操作指南
│   ├── step-01-information-gathering.md
│   ├── step-02-research.md
│   ├── step-03-writing.md
│   ├── step-04-de-ai.md
│   ├── step-05-html-image-generation.md
│   ├── step-06-html-layout.md
│   └── step-07-submit-draft.md
├── templates/                # HTML 模板
├── references/              # 参考文档
├── SKILL.md                  # 技能核心定义（Agent 使用）
├── package.json
└── README.md                 # 本使用指南
```

***

## 前置准备

### 1. 获取微信开发者密钥

1. **登录微信公众平台**：访问 <https://mp.weixin.qq.com/> 并登录你的公众号账号
2. **进入开发者工具**：左侧菜单 → 开发 → 基本配置
3. **获取 AppID 和 AppSecret**：
   - AppID：应用 ID，公开信息
   - AppSecret：应用密钥，**注意保密**
4. **记录密钥**：将获取到的 AppID 和 AppSecret 保存好

### 2. 配置服务器 IP 白名单

将运行此技能的服务器 IP 添加到微信公众平台 IP 白名单：

> 添加方式：微信公众平台 → 开发 → 基本配置 → IP 白名单 → 添加 IP

### 3. 配置环境变量

创建或编辑 `~/.openclaw/env` 文件，添加以下内容：

```
WECHAT_APPID=你的微信公众号AppID
WECHAT_APPSECRET=你的微信公众号AppSecret
```

### 4. 安装依赖

```bash
cd skills/article-factory-wechat && npm install
```

***

## 凭证汇总

| 凭证                 | 用途         | 配置位置              |
| ------------------ | ---------- | ----------------- |
| `WECHAT_APPID`     | 微信公众号应用 ID | `~/.openclaw/env` |
| `WECHAT_APPSECRET` | 微信公众号应用密钥  | `~/.openclaw/env` |
| 飞书机器人              | 文章审阅分享     | OpenClaw 飞书插件（自动） |

***

## 7 步流程

| 步骤     | 操作      | 说明                               |
| ------ | ------- | -------------------------------- |
| Step 1 | 信息搜集    | 使用 multi-search-engine 搜索热点，提炼选题 |
| Step 2 | 深度调研    | 收集素材，验证数据真实性                     |
| Step 3 | 撰写文章    | 按公众号风格写作                         |
| Step 4 | 去 AI 味  | 使用 humanize-chinese 技能优化         |
| Step 5 | 生成配图    | HTML 模板 + Puppeteer 生成封面和配图      |
| Step 6 | HTML 排版 | 美化 HTML，适配微信                     |
| Step 7 | 提交草稿    | 自动提交到微信公众号草稿箱                    |

***

## 脚本用法

### 生成配图

```bash
node scripts/temp-convert.js --html=article.html --output=output/dir --width=1400 --height=1200
```

### 提交草稿

```bash
node scripts/submit-draft.js --html=article.html --title="文章标题" --author="虾看虾说" --digest="摘要"
```

***

## 注意事项

1. **AppSecret 保密**：不要将 AppSecret 提交到代码仓库或分享给他人
2. **IP 白名单**：服务器 IP 变更后需及时更新白名单设置
3. **去 AI 味不可跳过**：每次发布前必须运行 humanize-chinese 检测
4. **用户审阅后再提交**：若为飞书渠道，通过飞书文档发送链接给用户确认
5. **图片尺寸**：微信公众号对图片大小有限制，建议单张控制在 1MB 以内

***

## 故障排除

| 错误信息               | 原因            | 解决方案             |
| ------------------ | ------------- | ---------------- |
| `401 unauthorized` | IP 未在白名单或凭证错误 | 检查白名单和 env 配置    |
| `invalid media_id` | 图片上传失败        | 检查网络连接           |
| 图片不显示              | HTML 中图片路径错误  | 确保路径相对于 HTML 文件  |
| Puppeteer 启动失败     | 依赖未安装或网络问题    | 运行 `npm install` |

