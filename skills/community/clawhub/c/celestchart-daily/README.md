# 🌟 CelestChart Daily Forecast Skill

> 为 AI Agent（Claude、OpenClaw 等）提供个性化每日星盘运势能力。  
> A daily astrology transit skill for AI agents, powered by the [CelestChart](https://xp.broad-intelli.com) API.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![ClaWhub](https://img.shields.io/badge/ClaWhub-install-blueviolet)](https://clawhub.ai/maye08/celestchart-daily)

---

## ✨ 功能介绍

安装后，你可以直接在 AI 对话中问：

- "今日运势"、"今天运势怎么样"
- "今天星象如何"、"今天适合做什么"

AI 会自动调用 CelestChart API，返回基于你个人本命盘的当天运势，包括：

| 模块 | 内容 |
|------|------|
| 🌙 月亮行运 | 月亮今日星座与所在宫位 |
| 😊 情绪基调 | 今日整体情绪倾向 |
| 📊 情绪稳定指数 | 今日情绪稳定程度及建议 |
| 🎯 今日重点 | 月亮宫位对应的人生领域 |
| ⏰ 最佳时机 | 今日最佳行动时间窗口 |
| 🌙 月亮相位 | 月亮与本命盘的行星相位及解读 |
| ✨ 内行星相位 | 金星、火星等内行星与本命盘的相位 |

---

## 📋 前置条件

使用本 Skill 需要：

1. **CelestChart 账号** — 前往 [xp.broad-intelli.com](https://xp.broad-intelli.com) 注册或快速登录
2. **VIP 会员** — 登录即免费送 VIP（1个月）
3. **API Key** — 登录后在「用户中心 → API Key 管理」生成

---

## 🚀 安装方式

### 方式一：通过 ClaWhub 安装（推荐）

访问 Skill 页面：[clawhub.ai/maye08/celestchart-daily](https://clawhub.ai/maye08/celestchart-daily)

```bash
npx clawhub@latest install celestchart-daily
```

### 方式二：手动复制到 OpenClaw

```bash
# 克隆仓库
git clone https://github.com/maye08/celestchart-astrology-skills.git

# 复制 skill 到 OpenClaw 目录
cp -r celestchart-astrology-skills/celestchart-daily ~/.openclaw/skills/
```

---

## ⚙️ 配置环境变量

安装后，需要配置以下环境变量（在 `~/.zshrc` 或 `~/.bashrc` 中添加并重新加载）：

```bash
# ── 必填 ─────────────────────────────────────────
export CELESTCHART_API_KEY="<在用户中心生成的 API Key>"

export CELESTCHART_BIRTH_YEAR="1990"            # 出生年
export CELESTCHART_BIRTH_MONTH="1"              # 出生月（1-12）
export CELESTCHART_BIRTH_DAY="1"                # 出生日（1-31）

# ── 选填（有默认值）────────────────────────────────
export CELESTCHART_BIRTH_HOUR="12"              # 出生时（默认 12）
export CELESTCHART_BIRTH_MINUTE="0"             # 出生分（默认 0）
export CELESTCHART_BIRTH_LON="116.4"            # 出生地经度（默认北京）
export CELESTCHART_BIRTH_LAT="39.9"             # 出生地纬度（默认北京）
export CELESTCHART_BIRTH_TZ="8"                 # 时区（默认 +8，北京/上海）
```

添加后执行：

```bash
source ~/.zshrc   # 或 source ~/.bashrc
```

### 📍 常用城市经纬度参考

| 城市 | 经度 | 纬度 | 时区 |
|------|------|------|------|
| 北京 | 116.4 | 39.9 | 8 |
| 上海 | 121.5 | 31.2 | 8 |
| 广州 | 113.3 | 23.1 | 8 |
| 成都 | 104.1 | 30.6 | 8 |
| 香港 | 114.2 | 22.3 | 8 |
| 台北 | 121.5 | 25.0 | 8 |
| 东京 | 139.7 | 35.7 | 9 |
| 新加坡 | 103.8 | 1.3 | 8 |
| 伦敦 | -0.13 | 51.5 | 0 |
| 纽约 | -74.0 | 40.7 | -5 |
| 洛杉矶 | -118.2 | 34.1 | -8 |
| 悉尼 | 151.2 | -33.9 | 10 |

> 其他城市可前往 [latlong.net](https://www.latlong.net) 查询精确经纬度。

---

## 🔒 安全说明

- **保护 API Key**：`CELESTCHART_API_KEY` 存储在 shell 配置文件中，请勿将含有真实 Key 的 `.zshrc` / `.bashrc` 提交到公开仓库或分享给他人。
- **密钥泄露处理**：若 API Key 可能已暴露，请立即前往 [CelestChart 用户中心](https://xp.broad-intelli.com/usercenter) 撤销并重新生成。
- **固定服务地址**：本 Skill 仅向 CelestChart 官方地址 `https://xp.broad-intelli.com` 发送请求，不支持自定义服务地址，确保你的 API Key 和出生信息不会被发送到第三方服务。
- **最小权限**：建议为本 Skill 单独申请一个 API Key，与其他用途的 Key 隔离，便于独立管理和撤销。

---

## 🧪 验证安装

配置完环境变量后，运行以下命令验证 API 是否正常：

```bash
bash ~/.openclaw/skills/celestchart-daily/run.sh
```

成功时会返回包含 `moon_transit`、`emotional_tone`、`emotional_stability_index`、`daily_focus` 等字段的 JSON 数据。

---

## 💬 使用示例

在 AI 对话中输入以下任意语句：

```
今日运势
今天运势怎么样？
我今天的星象如何？
今天适合做重要决策吗？
```

AI 会解读并输出包含月亮行运、情绪基调、相位分析等完整运势内容。

---

## ❗ 错误排查

| 错误提示 | 原因 | 解决方法 |
|---------|------|---------|
| `未配置 CELESTCHART_API_KEY` | 环境变量未设置 | 检查 `~/.zshrc` 并执行 `source ~/.zshrc` |
| `API Key 无效或已失效` (401) | API Key 错误或已删除 | 前往[用户中心](https://xp.broad-intelli.com/usercenter)重新生成 |
| `VIP 已过期` (403) | VIP 订阅到期 | 前往[用户中心](https://xp.broad-intelli.com/usercenter)续费 VIP |
| `未配置出生信息` | 出生年月日环境变量缺失 | 确认 `BIRTH_YEAR`、`BIRTH_MONTH`、`BIRTH_DAY` 均已设置 |

---

## 📁 文件说明

```
celestchart-daily/
├── SKILL.md      # Skill 核心配置：定义触发词、AI 解读规则
├── run.sh        # API 调用脚本：请求 CelestChart 并返回 JSON
└── README.md     # 本文档
```

---

## 📄 许可证

[MIT License](LICENSE) — 免费使用，欢迎 Fork 和贡献。

---

## 🔗 相关链接

- 🌐 **CelestChart 官网**：[xp.broad-intelli.com](https://xp.broad-intelli.com)
- 🔧 **ClaWhub Skill 页面**：[clawhub.ai/maye08/celestchart-daily](https://clawhub.ai/maye08/celestchart-daily)
- 🐙 **本仓库**：[github.com/maye08/celestchart-astrology-skills](https://github.com/maye08/celestchart-astrology-skills)
