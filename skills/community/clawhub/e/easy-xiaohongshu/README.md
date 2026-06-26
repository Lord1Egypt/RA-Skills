# Easy-xiaohongshu

一个用于生成和发布小红书图文内容的技能。

## 改进后的能力

- 统一配置加载：`config/default-config.json` + `config/local-config.json` + 环境变量覆盖
- 公共错误类型：`EasyXHSError` / `ConfigError` / `APIError` / `MCPError`
- 统一 CLI 入口：`scripts/cli.py`
- 保留原有脚本入口：`optimize_prompt.py` / `generate_content.py` / `generate_image.py` / `publish_to_xhs.py`

## CLI 用法

```bash
cd scripts
python3 cli.py optimize \
  --account-type "科技博主" \
  --content-direction "AI效率" \
  --target-audience "职场新人" \
  --topic "AI工具清单"

python3 cli.py generate \
  --account-type "科技博主" \
  --content-direction "AI效率" \
  --target-audience "职场新人" \
  --topic "AI工具清单"

python3 cli.py images \
  --content-file ../generated_content.json \
  --style '{"style":"极简科技风","colors":"蓝白"}' \
  --negative-prompt "低质量，模糊，变形"

python3 cli.py publish \
  --title "AI工具清单" \
  --content "正文内容" \
  --images ../generated_images/image_01.png ../generated_images/image_02.png \
  --tags AI 工具 效率
```

## 环境变量

- `EASY_XHS_CONFIG`：JSON 字符串，用于覆盖配置文件中的任意字段
- `XHS_MCP_URL`：覆盖发布 MCP 地址

✨ **从创意到发布，全自动完成** — 提示词优化 → 图文生成 → 一键发布

---

## 📖 简介

Easy-xiaohongshu 是一个专为小红书创作者设计的 AI 图文自动发布工具。只需输入主题，即可自动生成完整的 8 页图文笔记，并一键发布到小红书。

### 核心流程

```
用户输入主题
     ↓
【Step 1】智能匹配风格预设（13 种账号类型）
     ↓
【Step 2】生成 8 页图文方案（文案 + 画面描述）
     ↓
【Step 3】用户确认文案
     ↓
【Step 4】调用 Gemini API 生成 8 张成品图
     ↓
【Step 5】用户确认图片
     ↓
【Step 6】通过 MCP 服务自动发布到小红书
```

---

## 🚀 快速开始

### 环境要求

- Python 3.8+
- macOS（发布功能需要）
- xhs-mac-mcp 服务（可选，仅发布时需要）

### 安装步骤

#### 1. 获取 API Key

1. 访问 [z.3i0.cn](https://z.3i0.cn) 注册账号
2. 在钱包管理中充值（生图成本最低 0.2 元/张）
3. 在令牌管理中创建新令牌
4. 复制生成的 API Key

#### 2. 运行安装脚本

```bash
cd ~/clawd/skills/Easy-xiaohongshu
bash install.sh
```

安装脚本会自动：
- ✅ 检查 Python 环境
- ✅ 安装 Python 依赖
- ✅ 引导配置 API Key
- ✅ 检查 MCP 服务状态
- ✅ 创建输出目录

#### 3. 开始创作

发送消息：
```
我想发一篇主题为【xxxxxx】的小红书，帮我制作内容
```

---

## 🎨 支持的账号风格

| 编号 | 账号类型 | 风格名称 | 色调 | 适合场景 |
|------|----------|----------|------|----------|
| 1 | 科技博主 | 极简科技感 | 蓝/白/灰 | AI 工具、数码测评 |
| 2 | 亲子博主 | 温馨插画风 | 暖黄/粉 | 育儿经验、亲子互动 |
| 3 | 美妆博主 | 高级 ins 风 | 莫兰迪色 | 护肤教程、彩妆分享 |
| 4 | 健身博主 | 活力运动风 | 橙/黑 | 健身计划、减脂塑形 |
| 5 | 美食博主 | 治愈系 | 暖色调 | 家常菜、美食探店 |
| 6 | 学习博主 | 清新简约 | 蓝/绿 | 学习方法、考试经验 |
| 7 | 旅行博主 | 电影感 | 胶片色 | 旅行攻略、风景摄影 |
| 8 | 职场博主 | 商务简约 | 深蓝/灰 | 职场技能、时间管理 |
| 9 | 漫画博主 | 热血漫画风 | 鲜明对比 | 动漫解析、漫画推荐 |
| 10 | 摄影博主 | 胶片质感 | 复古色 | 摄影教程、作品分享 |
| 11 | 穿搭博主 | 时尚杂志风 | 高级灰 | 穿搭分享、OOTD |
| 12 | 游戏博主 | 电竞科技风 | 霓虹色 | 游戏攻略、测评 |
| 13 | 音乐博主 | 唱片封面风 | 艺术色 | 歌单推荐、音乐分享 |

---

## 📁 文件结构

```
Easy-xiaohongshu/
├── SKILL.md                    # 技能说明
├── README.md                   # 详细文档（本文件）
├── install.sh                  # 一键安装脚本
├── requirements.txt            # Python 依赖清单
│
├── config/
│   ├── default-config.json     # 默认配置模板
│   └── local-config.json       # 本地配置（API Key、偏好）
│
├── scripts/
│   ├── optimize_prompt.py      # 提示词优化器（匹配风格预设）
│   ├── generate_content.py     # 文案生成器（调用 API）
│   ├── generate_image.py       # 图片生成器（调用 Gemini）
│   └── publish_to_xhs.py       # 小红书发布（MCP 服务）
│
├── references/
│   ├── style-presets.json      # 13 种风格预设定义
│   ├── hashtag-library.json    # 标签库（按分类）
│   ├── prompt-template.md      # 图文生成提示词模板
│   └── caption-template.md     # 发布文案模板
│
└── generated_images/           # 生成的图片输出目录
    ├── image_1.png
    ├── image_2.png
    └── ...
```

---

## ⚙️ 配置说明

### 本地配置文件

先复制示例配置再填写密钥：

```bash
cp config/local-config.example.json config/local-config.json
```

`config/local-config.json` 示例：

```json
{
  "api": {
    "key": "your-api-key-here",
    "base_url": "https://z.3i0.cn/v1beta",
    "model": "gemini-3.1-flash-image-preview",
    "timeout_seconds": 120,
    "max_retries": 3
  },
  "user_preferences": {
    "account_type": "漫画博主",
    "content_direction": "动漫解析",
    "target_audience": "二次元爱好者"
  },
  "mcp": {
    "url": "http://localhost:18060/mcp",
    "timeout_seconds": 30
  },
  "style_matching": {
    "enabled": true,
    "fallback_to": "清新简约",
    "auto_detect_keywords": true
  }
}
```

推荐统一使用 `api.key` 与 `mcp.url`，旧字段 `api.api_key` 和 `xhs_mcp.url` 仅用于兼容历史配置。

### 配置项说明

| 字段 | 说明 | 默认值 |
|------|------|--------|
| `api.key` | Z3i0 API Key | 必填 |
| `api.base_url` | API 基础 URL | https://z.3i0.cn/v1beta |
| `api.model` | 生成模型 | gemini-3.1-flash-image-preview |
| `user_preferences.account_type` | 账号类型 | 科技博主 |
| `user_preferences.content_direction` | 内容方向 | - |
| `user_preferences.target_audience` | 目标用户 | - |
| `mcp.url` | MCP 服务地址 | http://localhost:18060/mcp |

---

## 💰 成本说明

| 项目 | 成本 | 说明 |
|------|------|------|
| 技能使用 | 免费 | 开源技能 |
| API 调用 | 最低 0.2 元/张 | Z3i0 生图成本 |
| 8 页图文 | 最低约 1.6 元/次 | 按 8 张起算 |
| MCP 服务 | 免费 | 本地运行 |

---

## 🔌 MCP 服务集成

### 安装 xhs-mac-mcp

```bash
# 参考 xhs-mac-mcp 技能文档
cd ~/clawd/skills/xhs-mac-mcp
# 按照 SKILL.md 安装
```

### 启动 MCP 服务

```bash
# 启动后默认监听 http://localhost:18060/mcp
```

### 首次发布流程

1. 技能检测到 MCP 服务可用
2. 触发扫码登录（小红书官方二维码）
3. 登录成功后保存会话
4. 后续发布无需重复登录

---

## 📊 输出示例

### generated_content.json

```json
{
  "raw_text": "【第1页】...\n成品图生成提示词：...",
  "page_prompts": [
    "一张教育类封面图，包含中文文字...",
    "..."
  ]
}
```

### generated_caption.json

```json
{
  "title": "定语从句，3 步就搞定！英语老师亲授",
  "content": "你是不是也这样？看到定语从句就头大？😫\n分不清 which 和 that？...",
  "tags": ["英语教学", "定语从句", "英语语法", ...]
}
```

---

## ❓ 常见问题

### Q: API Key 在哪里获取？
**A:** 在 [z.3i0.cn](https://z.3i0.cn) 注册后，进入控制台 → 令牌管理 → 添加令牌。

### Q: 生成失败怎么办？
**A:** 
1. 检查 API Key 是否正确
2. 检查网络连接
3. 查看 `generated_images/` 目录是否有错误日志

### Q: 发布失败怎么办？
**A:**
1. 检查 MCP 服务是否运行：`curl http://localhost:18060/mcp`
2. 检查是否已完成扫码登录
3. 查看 MCP 服务日志

### Q: 可以自定义风格吗？
**A:** 可以，编辑 `references/style-presets.json` 添加或修改风格预设。

### Q: 可以修改图片数量吗？
**A:** 可以，在 `config/local-config.json` 中修改 `pages` 字段（建议 6-10 页）。

### Q: 支持批量创作吗？
**A:** 当前版本支持单次创作，批量功能开发中。

---

## 🛠️ 开发相关

### 添加新的风格预设

编辑 `references/style-presets.json`：

```json
{
  "新博主类型": {
    "style": "风格名称",
    "colors": ["#颜色 1", "#颜色 2"],
    "fonts": ["字体 1", "字体 2"],
    "elements": ["元素 1", "元素 2"],
    "tone": "语气描述",
    "emoji": ["😀", "😊"],
    "content_length": {"min": 300, "max": 600},
    "cover_style": "封面风格描述"
  }
}
```

### 调试模式

设置环境变量启用调试输出：

```bash
export EASY_XHS_DEBUG=1
python scripts/generate_content.py
```

---

## 📝 更新日志

### v1.1.0 (2026-03-23)
- ✅ 添加 install.sh 一键安装脚本
- ✅ 完善 13 种风格预设（新增漫画博主、学习博主）
- ✅ 集成提示词优化器到主流程
- ✅ 添加用户偏好配置支持
- ✅ 完善 SKILL.md 和 README.md 文档

### v1.0.0 (2026-03-20)
- ✅ 初始版本发布
- ✅ 基础图文生成功能
- ✅ MCP 发布集成

---

## 📄 许可证

MIT License

---

## 🙏 致谢

- [Z3i0 API](https://z.3i0.cn) - 图像生成服务
- [xhs-mac-mcp](https://github.com/...) - 小红书 MCP 服务
- [Gemini](https://ai.google.dev/) - AI 模型支持
