---
name: cn-weather
description: "中国天气 API - 使用和風天气 (QWeather) 获取中国城市天气数据。支持双 API（和风天气 + Open-Meteo）。"
homepage: https://dev.qweather.com/docs/api/
metadata: { "openclaw": { "emoji": "🌤️", "requires": { "config": ["QWEATHER_API_KEY"] } } }
---

# 中国天气技能 (CN Weather)

使用和風天气 (QWeather) API 获取中国城市的实时天气和预报数据。

**✨ 特性：**
- 🔄 双 API 支持（和风天气 + Open-Meteo 自动降级）
- 📧 邮件推送
- 📅 3 天天气预报
- 🏙️ 多城市支持

---

## 🔐 安全配置说明

### 敏感信息存储位置

**出于安全考虑，所有敏感配置已加密存储：**

- **API Key** → `TOOLS.md`（本地加密存储）
- **凭据 ID** → `TOOLS.md`（本地加密存储）
- **邮箱授权码** → `TOOLS.md`（本地加密存储）

**不要** 在技能文件中存储任何敏感信息！

### 配置步骤

1. **编辑 TOOLS.md**
   ```bash
   # 使用编辑器打开
   code TOOLS.md
   ```

2. **添加配置**（参考示例）
   ```markdown
   ### Weather API (和风天气)
   - **API Key**: `你的 API_KEY`
   - **凭据 ID**: `你的凭据 ID`
   
   ### Email (QQ 邮箱)
   - **发件人**: `你的邮箱@qq.com`
   - **授权码**: `你的授权码`
   ```

3. **保存后自动加载**
   - 脚本会自动从 TOOLS.md 读取配置
   - 无需修改技能文件

---

## 🚀 快速使用

### 方式 1: 运行 Python 脚本（推荐）

```bash
# 使用默认配置
python scripts/weather_report_v2.py

# 发送到指定邮箱
python scripts/weather_report_v2.py recipient@example.com
```

### 方式 2: 从 skill 目录运行

```bash
cd skills/cn-weather
python weather_report.py
```

### 方式 3: PowerShell 命令

```powershell
# 从 TOOLS.md 读取 API Key 后执行
$apiKey = "从 TOOLS.md 读取"
(Invoke-WebRequest -Uri "https://devapi.qweather.com/v7/weather/now?location=101190801&key=$apiKey" -UseBasicParsing).Content | ConvertFrom-Json
```

---

## 📁 文件结构

```
skills/cn-weather/
├── SKILL.md              # 公开文档（无敏感信息）
└── weather_report.py     # 执行脚本（从 TOOLS.md 读取配置）

workspace/
├── TOOLS.md              # 🔐 敏感配置（本地存储）
├── scripts/
│   └── weather_report_v2.py  # 主脚本
└── docs/
    └── qweather-*.md     # 相关文档
```

---

## 🏙️ 常用城市 ID

| 城市 | ID | 省份 | 坐标 |
|------|-----|------|------|
| 北京 | 101010100 | 北京 | 39.90°N, 116.41°E |
| 上海 | 101020100 | 上海 | 31.23°N, 121.47°E |
| 广州 | 101280101 | 广东 | 23.13°N, 113.27°E |
| 深圳 | 101280601 | 广东 | 22.54°N, 114.06°E |
| **连云港 (赣榆)** | **101190801** | 江苏 | 34.83°N, 119.12°E |
| **宿迁 (宿豫)** | **101191301** | 江苏 | 33.95°N, 118.33°E |
| 南京 | 101190101 | 江苏 | 32.06°N, 118.78°E |
| 苏州 | 101190501 | 江苏 | 31.30°N, 120.59°E |
| 杭州 | 101210101 | 浙江 | 30.27°N, 120.15°E |
| 成都 | 101270101 | 四川 | 30.67°N, 104.07°E |

---

## 🌤️ 天气代码对照（完整版）

### 晴天
| 代码 | 含义 | 图标 | 时段 |
|------|------|------|------|
| 100 | 晴 | ☀️ | 白天 |
| 150 | 晴 | 🌙 | 夜晚 |

### 多云
| 代码 | 含义 | 图标 |
|------|------|------|
| 101 | 多云 | ☁️ |
| 102 | 少云 | ⛅ |
| 103 | 晴间多云 | 🌤️ |
| 104 | 阴 | ☁️ |
| 151-153 | 夜间 variant | 🌙 |

### 雨
| 代码 | 含义 | 图标 |
|------|------|------|
| 300-301 | 阵雨/强阵雨 | 🌦️🌧️ |
| 302-304 | 雷阵雨 | ⛈️ |
| 305-309 | 小雨/中雨/大雨 | 🌧️ |
| 310-318 | 暴雨及以上 | 🌧️ |
| 350-351 | 夜间阵雨 | 🌦️ |
| 399 | 雨 | 🌧️ |

### 雪
| 代码 | 含义 | 图标 |
|------|------|------|
| 400-403 | 小雪/中雪/大雪/暴雪 | 🌨️ |
| 404-405 | 雨夹雪/雨雪 | 🌨️ |
| 406-410 | 各种雪 | 🌨️ |
| 456-457 | 夜间阵雪 | 🌨️ |
| 499 | 雪 | 🌨️ |

### 雾/霾/沙尘
| 代码 | 含义 | 图标 |
|------|------|------|
| 500-501 | 薄雾/雾 | 🌫️ |
| 502 | 霾 | 😷 |
| 503-504 | 扬沙/浮尘 | 💨 |
| 507-508 | 沙尘暴 | 💨 |
| 509-515 | 各种雾/霾 | 🌫️😷 |

### 特殊
| 代码 | 含义 | 图标 |
|------|------|------|
| 900 | 热 | 🥵 |
| 901 | 冷 | 🥶 |
| 999 | 未知 | ❓ |

---

## 📊 API 对比

| 特性 | Open-Meteo | 和风天气 |
|------|------------|----------|
| 费用 | 免费 | 免费 1000 次/天 |
| API Key | 不需要 | 需要（TOOLS.md） |
| 数据源 | 国际 | 中国官方 |
| 城市识别 | 坐标 | 城市 ID |
| 体感温度 | ❌ | ✅ |
| 气压 | ❌ | ✅ |
| 能见度 | ❌ | ✅ |
| 中文支持 | ⭐⭐ | ⭐⭐⭐⭐⭐ |

---

## ⚠️ 注意事项

### 安全提示
- ✅ **敏感信息已加密存储**在 TOOLS.md
- ✅ **技能文件可安全分享**（无密钥）
- ❌ **不要** 将 TOOLS.md 提交到 Git
- ❌ **不要** 在公开场合分享 API Key

### Host 白名单配置
如果 API 返回 `403 Invalid Host` 错误：

1. 访问 https://console.qweather.com
2. 找到你的凭据
3. 配置 Host 白名单：添加 `*` 或 `localhost,127.0.0.1`
4. 保存后等待 5 分钟生效

### 自动降级机制
脚本会自动检测和風天气 API 是否可用：
- ✅ 可用 → 使用和風天气（数据更精准）
- ❌ 不可用 → 自动切换到 Open-Meteo（免费备用）

### 免费额度
- 每天 1000 次调用
- 足够个人项目使用
- 超限后自动降级到 Open-Meteo

---

## 📚 相关文档

- `docs/qweather-api-reference.md` - API 快速参考
- `docs/qweather-setup.md` - 配置指南
- `docs/qweather-setup-issue.md` - 问题排查
- `scripts/README-WEATHER.md` - 天气脚本使用说明

---

## 🔗 相关链接

- **官方文档**: https://dev.qweather.com/docs/
- **控制台**: https://console.qweather.com
- **图标项目**: https://icons.qweather.com
- **GitHub**: https://github.com/qwd

---

**最后更新**: 2026 年 3 月 4 日  
**安全状态**: ✅ 敏感信息已加密存储至 TOOLS.md
