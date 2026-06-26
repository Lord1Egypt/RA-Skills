# Easy-xiaohongshu - 小红书 AI 图文自动发布

✨ **从创意到发布，全自动完成** — 提示词优化 → 图文生成 → 一键发布

---

## 核心能力

| 能力 | 描述 |
|------|------|
| 🤖 **智能提示词优化** | 根据账号定位自动匹配最佳风格（13 种预设） |
| 📝 **图文生成** | 文案 + 排版 + AI 成品图，一站式完成 |
| 📱 **自动发布** | 通过 MCP 服务一键发布到小红书 |
| 📋 **发布文案生成** | 自动生成标题 + 正文 + 标签 |

---

## 快速开始

### Step 1：获取 API Key

1. 在 [z.3i0.cn](https://z.3i0.cn) 注册账号
2. 在钱包管理中按需充值（生图有成本，最低 0.2 元/张）
3. 在令牌管理中点击【添加令牌】
4. 输入名称等信息后保存
5. 复制生成的 API Key

### Step 2：安装技能

```bash
cd ~/clawd/skills/Easy-xiaohongshu
bash install.sh
```

安装脚本会：
- ✅ 检查 Python 环境
- ✅ 安装依赖
- ✅ 引导 API Key 配置
- ✅ 检查 MCP 服务状态

### Step 3：发送创作主题

```
我想发一篇主题为【xxxxxx】的小红书，帮我制作内容
```

### Step 4：确认文案

技能会同时生成：
- 📄 **图文方案**（8 页图文内容）
- 📝 **发布文案**（标题 + 正文 + 标签）

确认没问题后进入下一步。

### Step 5：确认图片

8 张成品图会逐张生成并发给你预览，确认效果后进入下一步。

### Step 6：发布到小红书

技能会通过 MCP 服务自动发布。首次使用需要扫码登录，之后无需重复登录。发布前会再次确认。

---

## 支持的风格预设

| 账号类型 | 风格 | 适合场景 |
|----------|------|----------|
| 科技博主 | 极简科技感 | AI 工具、数码测评 |
| 亲子博主 | 温馨插画风 | 育儿经验、亲子互动 |
| 美妆博主 | 高级 ins 风 | 护肤教程、彩妆分享 |
| 健身博主 | 活力运动风 | 健身计划、减脂塑形 |
| 美食博主 | 治愈系 | 家常菜、美食探店 |
| 学习博主 | 清新简约 | 学习方法、考试经验 |
| 旅行博主 | 电影感 | 旅行攻略、风景摄影 |
| 职场博主 | 商务简约 | 职场技能、时间管理 |
| 漫画博主 | 热血漫画风 | 动漫解析、漫画推荐 |
| 摄影博主 | 胶片质感 | 摄影教程、作品分享 |
| 穿搭博主 | 时尚杂志风 | 穿搭分享、OOTD |
| 游戏博主 | 电竞科技风 | 游戏攻略、测评 |
| 音乐博主 | 唱片封面风 | 歌单推荐、音乐分享 |

---

## 自动发布（可选）

发布功能需要 `xiaohongshu-mcp` 服务，参考 `xhs-mac-mcp` 技能安装。

### MCP 配置

在 `config/local-config.json` 中配置：

```json
{
  "mcp": {
    "url": "http://localhost:18060/mcp",
    "timeout_seconds": 30
  }
}
```

---

## 文件结构

```
Easy-xiaohongshu/
├── SKILL.md                    # 技能说明（本文件）
├── README.md                   # 详细文档
├── install.sh                  # 一键安装脚本
├── requirements.txt            # Python 依赖
├── config/
│   ├── default-config.json     # 默认配置
│   └── local-config.json       # 本地配置（API Key 等）
├── scripts/
│   ├── optimize_prompt.py      # 提示词优化器
│   ├── generate_content.py     # 文案生成器
│   ├── generate_image.py       # 图片生成器
│   └── publish_to_xhs.py       # 小红书发布
├── references/
│   ├── style-presets.json      # 13 种风格预设
│   ├── hashtag-library.json    # 标签库
│   ├── prompt-template.md      # 提示词模板
│   └── caption-template.md     # 文案模板
└── generated_images/           # 生成的图片输出目录
```

---

## 依赖

| 依赖 | 用途 | 必需 |
|------|------|------|
| Python 3.8+ | 脚本运行 | ✅ |
| requests | HTTP 请求 | ✅ |
| Z3i0 API | 图像生成 | ✅ |
| xiaohongshu-mcp | 自动发布 | 发布时必需 |

---

## 配置说明

### API 配置

建议先复制示例文件：

```bash
cp config/local-config.example.json config/local-config.json
```

在 `config/local-config.json` 中配置：

```json
{
  "api": {
    "key": "你的 API Key",
    "base_url": "https://z.3i0.cn/v1beta",
    "model": "gemini-3.1-flash-image-preview"
  },
  "user_preferences": {
    "account_type": "漫画博主",
    "content_direction": "动漫解析",
    "target_audience": "二次元爱好者"
  }
}
```

### 用户偏好

技能会记住你的账号类型偏好，下次使用时自动应用。如需修改，重新运行 `install.sh` 或手动编辑 `local-config.json`。

---

## 输出内容

| 文件 | 描述 |
|------|------|
| `generated_content.json` | 生图原始文本 + `page_prompts` 结构化提示词 |
| `generated_caption.json` | 发布文案（标题 + 正文 + 标签） |
| `generated_images/*.png` | 生成的 8 张成品图 |

---

## 常见问题

### Q: API Key 在哪里获取？
A: 在 [z.3i0.cn](https://z.3i0.cn) 注册后，在令牌管理中创建。

### Q: 发布失败怎么办？
A: 检查 MCP 服务是否运行，首次发布需要扫码登录。

### Q: 可以修改风格预设吗？
A: 可以，编辑 `references/style-presets.json`。

---

## 许可证

MIT License

---

## 更新日志

- **2026-03-23**: 添加 install.sh 安装脚本、完善 13 种风格预设、集成提示词优化器
