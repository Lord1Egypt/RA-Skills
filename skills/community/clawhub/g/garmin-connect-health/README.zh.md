# garmin-connect-health -- OpenClaw Skill

<div align="right">
  <img src="https://img.shields.io/badge/语言-中文-red?style=for-the-badge&logo=googletranslate&logoColor=white" alt="中文">
  &nbsp;
  <a href="README.md"><img src="https://img.shields.io/badge/Language-English-blue?style=for-the-badge&logo=googletranslate&logoColor=white" alt="English"></a>
</div>

一个面向 [OpenClaw](https://github.com/openclaw/openclaw) 的 Garmin Connect 全量健康数据 Skill，可获取 40+ 项健康指标并让 AI 助手直接查询。

## 功能亮点

- **40+ 健康指标** -- 睡眠、HRV、压力、Body Battery、血氧、VO2 Max、训练状态、比赛预测等
- **结构化 JSON + SQLite 输出** -- 每日快照 + 可查询数据表，便于趋势和运动分析
- **多种认证方式** -- 环境变量、命令行参数、macOS 钥匙串、配置文件四选一
- **自动缓存每日数据** -- 无需重复调用 API，秒级响应
- **运动详情表** -- 活动记录和力量训练组写入 SQLite，方便深度分析
- **跨平台** -- macOS、Linux、Windows 均支持

## 效果截图

> 接入 OpenClaw 后，AI 助手可直接分析你的 Garmin 健康数据 💪

<div align="center">
  <img src="docs/screenshot-1.jpg" width="380" alt="Garmin 健康数据总览 -- 步数、睡眠、HRV、Body Battery、血氧">
  &nbsp;&nbsp;
  <img src="docs/screenshot-2.jpg" width="380" alt="训练分析与恢复建议">
</div>

*左图：完整健康数据快照，包含睡眠、心率、Body Battery、血氧、HRV 等核心指标。*
*右图：今日训练回顾（有氧/无氧效果量化）+ 个性化恢复建议。*

## 快速开始

```bash
# 安装依赖
pip install garminconnect

# 设置账号（推荐用环境变量，避免暴露在 shell 历史中）
export GARMIN_EMAIL="你的邮箱@example.com"
export GARMIN_PASSWORD="你的密码"

# 拉取今天的数据
python3 garmin_health.py

# 查看缓存的最新数据
python3 garmin_health.py --show
```

## 安装方式

### 手动安装
1. 复制 `garmin_health.py` 和 `SKILL.md` 到 OpenClaw skills 目录
2. 安装 Python 依赖：`pip install garminconnect`
3. 配置认证（见下方）

## 认证配置

认证优先级从高到低：

**1. 命令行参数（不推荐，会留在 shell 历史中）**
```bash
python3 garmin_health.py --email 你的邮箱 --password 你的密码
```

**2. 环境变量（推荐）**
```bash
export GARMIN_EMAIL="你的邮箱@example.com"
export GARMIN_PASSWORD="你的密码"
```

**3. macOS 钥匙串（最安全）**
```bash
security add-generic-password -a "你的邮箱@example.com" -s "garmin_connect" -w "你的密码"
```

**4. 本地配置文件**
```bash
# 创建配置文件
cat > ~/.garmin_credentials << EOF
email=你的邮箱@example.com
password=你的密码
EOF

# 必须设置为仅自己可读（重要！）
chmod 600 ~/.garmin_credentials
```

## 国内账号 / 大陆 IP 用户

默认连接 **国际版** Garmin Connect（`connect.garmin.com`）。  
如果你的佳明账号是在国内注册的，或在大陆 IP 运行，建议切换到 **国内端点**（`connect.garmin.com.cn`），稳定性更好、不容易触发 429。

### 一次性配置（推荐）

在 shell 配置文件（`~/.zshrc` 或 `~/.bashrc`）里加一行，以后每次都自动生效：

```bash
export GARMIN_IS_CN=true
```

然后重新加载：

```bash
source ~/.zshrc   # 或 source ~/.bashrc
```

**设置一次，永久生效** -- 包括 AI 助手通过 Skill 调用时，也会自动使用国内端点，无需额外传参。

### 临时指定（单次运行）

```bash
python3 garmin_health.py --cn
```

> **怎么判断用哪个端点？**  
> 如果你是在国内佳明官网/App 注册的账号，选国内（`--cn`）。如果是在 garmin.com 国际官网注册的，用默认即可。

### 首次登录与双重验证（MFA）
首次运行时 Garmin 会触发 MFA 验证，你的账号注册邮箱会收到验证码，按提示输入即可。授权成功后 token 会缓存在 `~/.garminconnect/`，后续无需再次验证。

## 使用方法

```bash
# 拉取今天的数据（默认）
python3 garmin_health.py

# 拉取指定日期
python3 garmin_health.py --date 2026-03-16

# 显示最新缓存数据
python3 garmin_health.py --show
```

## 数据覆盖

| 类别 | 指标 |
|------|------|
| **日常活动** | 步数、距离、卡路里（活动+基础代谢）、楼层、运动强度分钟 |
| **心率** | 最低/最高/静息心率 |
| **睡眠** | 时长、评分、深睡/浅睡/REM/清醒分布 |
| **HRV** | 昨晚均值、5min峰值、周均、状态、个人基线 |
| **Body Battery** | 当前值、今日最高/最低 |
| **血氧 SpO2** | 平均值、最低值 |
| **呼吸频率** | 清醒均值、睡眠均值 |
| **压力** | 平均/最高、休息/低/中/高压力时长 |
| **训练状态** | 恢复/超负荷/维持等 + 急慢性负荷比 |
| **训练准备度** | 0-100 评分 |
| **体能指标** | VO2 Max、体能年龄、耐力评分 |
| **比赛预测** | 5K/10K/半马/全马预测成绩 |
| **体重/体成分** | 体重、体脂率、BMI（需 Garmin Index 秤） |
| **饮水** | 摄入量与目标 |
| **活动记录** | 每次锻炼的心率、时长、卡路里、海拔、训练效果 |
| **周汇总** | 本周总步数、日均步数 |

## 数据存储

此 skill 会同时写入本地 JSON 快照和本地 SQLite 数据库：

```
~/.garmin_health/
  ├── 2026-05-07.json   # 每日 JSON 快照
  ├── latest.json       # 最新 JSON 快照
  └── garmin.db         # SQLite：daily_summary / activities / activity_sets
```

此 skill 不会上传你的健康数据；除非你主动分享，否则数据只保存在本机。

可通过环境变量覆盖路径：
- `GARMIN_DATA_DIR` -- 数据目录
- `GARMIN_TOKENSTORE` -- token 缓存目录

## 隐私与安全说明

- ✅ **数据本地存储** -- 所有数据保存在你自己的机器上，不上传任何第三方
- ✅ **仅与 Garmin 官方 API 通信** -- 无额外网络请求
- ✅ **支持 macOS 钥匙串** -- 密码可加密存储，无需明文
- ⚠️ **避免 --password 参数** -- 命令行密码会留在 shell 历史和进程列表中，建议用环境变量或钥匙串
- ⚠️ **保护配置文件** -- 使用 `~/.garmin_credentials` 时务必 `chmod 600`

## 常见问题

**Q: 支持哪些设备？**
A: 所有能同步到 Garmin Connect 的 Garmin 手表/运动追踪器。Body Battery、血氧等功能取决于设备型号。

**Q: 体成分数据为空？**
A: 需要 Garmin Index 系列智能体重秤与账号关联。

**Q: 不用 OpenClaw 能单独使用吗？**
A: 完全可以，这是一个独立的 Python 脚本，输出标准 JSON，并额外写入本地 SQLite。

**Q: 数据会上传到任何地方吗？**
A: 不会。数据只存储在本地 JSON/SQLite 文件中。

## 配合 OpenClaw 使用示例

配置好 Skill 后，可以直接问 AI：
- "我今天走了多少步？"
- "昨晚睡眠质量怎么样？"
- "我的 HRV 状态如何？"
- "我最近训练是否过度？"
- "帮我分析这周的运动数据"

## 依赖

- Python 3.10+
- [python-garminconnect](https://github.com/cyberjunky/python-garminconnect)（感谢这个优秀的开源封装库）

## License

MIT-0
