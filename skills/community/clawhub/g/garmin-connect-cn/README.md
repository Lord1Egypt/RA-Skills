# Garmin Connect 数据查询

读取 Garmin Connect 手表/设备的健康数据（步数、睡眠、心率、运动记录等），支持中国区 Garmin Connect（garmin.cn）。

![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Linux-blue)
![Python](https://img.shields.io/badge/Python-3.8+-green)

## 功能

- 📊 **今日数据** - 步数、距离、卡路里、爬楼
- 😴 **睡眠分析** - 睡眠时长、睡眠分数
- ❤️ **心率血氧** - 静息心率、血氧饱和度、压力指数
- 🏃 **运动记录** - 跑步/骑行/游泳等活动详情
- ⚖️ **体重体脂** - 配套体重秤数据

## 安装

### 方法一：ClawHub（一键安装）

```bash
openclaw skills install garmin-connect
```

### 方法二：手动安装

```bash
# 克隆仓库
git clone https://github.com/YOUR_USERNAME/garmin-connect.git ~/.qclaw/skills/garmin-connect

# 安装依赖
pip3 install requests
```

## 配置

### 获取 JWT Token

1. 浏览器打开 https://connect.garmin.cn 并登录
2. 按 **F12** 打开开发者工具 → **Application** 标签
3. 左侧选择 **Cookies** → `https://connect.garmin.cn`
4. 找到 `JWT_WEB` 这一行，复制 **Value** 列的值

> ⚠️ Token 有效期约 1 个月，过期后需重新获取。

### 配置 Token

将 Token 写入环境变量或配置文件：

```bash
export GARMIN_JWT="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

或在代码中直接传入。

## 使用

### 命令行

```bash
# 查询今日数据
python3 scripts/query.py "$GARMIN_JWT"

# 查询指定日期
python3 scripts/query.py "$GARMIN_JWT" 2026-03-24

# 查询最近活动
python3 scripts/activities.py "$GARMIN_JWT"
```

### OpenClaw AI 对话

```
"今天走了多少步？"
"昨晚睡眠质量怎么样？"
"这周有氧运动了几次？"
"上个月跑了多少公里？"
```

## API 端点

| 端点 | 说明 |
|------|------|
| `/userprofile-service/userprofile/user-settings` | 用户信息 |
| `/daily-summary-api/summary/daily/{date}` | 每日摘要 |
| `/activitylist-service/activities/{userId}` | 活动列表 |
| `/sleepservice/daily-sleep/{userId}` | 睡眠数据 |

完整文档见 `references/api.md`

## 文件结构

```
garmin-connect/
├── SKILL.md           # OpenClaw 技能定义
├── README.md          # 本文档
├── scripts/
│   ├── query.py       # 主查询脚本
│   └── activities.py  # 活动查询
└── references/
    ├── api.md         # API 文档
    └── setup.md       # 详细配置指南
```

## 依赖

- Python 3.8+
- `requests` 库

## 常见问题

**Q: API 返回 404？**  
A: JWT 可能已过期，重新获取 Token。

**Q: 支持 Garmin.com 国际站吗？**  
A: 本技能针对 garmin.cn 中国区，garmin.com 需修改 API base URL。

**Q: 支持哪些设备？**  
A: 所有同步到 Garmin Connect 的设备（手表/体重秤/踏步机等）。

## License

MIT
