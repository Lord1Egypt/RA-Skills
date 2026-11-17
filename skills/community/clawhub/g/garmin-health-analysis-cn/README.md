# 佳明健康数据分析 - 技能（Skill）

> **用自然语言与你的佳明数据对话** —— "帮我分析一下上周的比赛数据"、"帮我分析一下最近的身体状况"、"我昨晚睡得怎么样？"

从你的佳明设备获取 20 余项健康指标：睡眠阶段、身体电量（Body Battery）、心率变异性（HRV）、最大摄氧量（VO2 Max）、训练准备度、身体成分、血氧（SPO2）等。支持下载 FIT/GPX 文件、查询任意位置的海拔与配速，并生成可交互的健康仪表盘。

> **🌍 账号区域说明：本 Skill 同时支持中国大陆版与国际版佳明账号**
>
> - 通过配置文件中的 `is_cn` 字段（或登录命令的 `--cn` 参数）选择要连接的服务器：`true` 连接**佳明中国**（[connect.garmin.cn](https://connect.garmin.cn)），`false` 连接**国际版**（[connect.garmin.com](https://connect.garmin.com)）；
> - 配置模板 `config.example.json` 默认 `is_cn: true`（面向中国大陆用户），**国际版用户请将其改为 `false`**；
> - 请务必使用与账号注册区域一致的服务器，区域不匹配会导致登录失败。

---

## 🚀 安装

```bash
# 方式一：使用安装脚本（推荐）
./install.sh

# 方式二：手动安装
pip3 install garminconnect fitparse gpxpy

# 配置账号并登录
python3 scripts/garmin_auth.py login
```

**[📖 完整安装与使用说明](SKILL.md)**

## ⚡ 功能特性

**适合场景**：自动化健康监测、定时报告、主动健康提醒

- **自然语言查询**："帮我分析一下最近的身体状况" → 即刻生成身体电量与恢复分析
- **睡眠分析**：睡眠时长、睡眠阶段（浅睡/深睡/快速眼动）、睡眠评分、趋势变化
- **恢复追踪**：身体电量、心率变异性、训练准备度、压力水平
- **运动数据**：按类型统计的活动、卡路里、时长、配速、海拔
- **健康指标**：静息心率、最大摄氧量、身体成分、血氧
- **活动文件**：下载 FIT/GPX 文件，进行详细的路线与运动表现分析
- **交互式图表**：基于 Chart.js 的精美 HTML 仪表盘
- **有科学依据的解读**：使用专业分析框架解读数据趋势

## 📊 查询示例

> "帮我分析一下上周的比赛数据"
>
> "帮我分析一下最近的身体状况"
>
> "我昨晚睡得怎么样？"
>
> "最近一个月我的配速有什么变化？"
>
> "这次比赛的心率区间分布合理吗？"
>
> "下载我周日长距离拉练的 GPX 文件"

## 🛠️ 核心指标

| 指标 | 数值范围 | 含义说明 |
|------|----------|----------|
| **身体电量** | 0-100 | 佳明的恢复程度评分（越高代表精力越充沛） |
| **睡眠评分** | 0-100 | 整体睡眠质量（90 分以上为优秀） |
| **心率变异性** | 20-200+ 毫秒 | 相邻心跳间隔的变化程度（越高通常代表恢复越好） |
| **静息心率** | 40-80 次/分 | 越低通常越好（运动员常见为 40-60） |
| **压力** | 低/中/高 | 基于全天心率变异性分析得出 |

## 📦 文件结构

```
garmin-health-analysis-cn/
├── SKILL.md                       # 技能安装与使用说明
├── README.md                      # 本文件
├── install.sh                     # 一键安装脚本
├── scripts/
│   ├── garmin_auth.py            # 登录认证脚本
│   ├── garmin_data.py            # 获取健康指标（JSON 格式）
│   ├── garmin_chart.py           # 生成 HTML 图表
│   ├── garmin_data_extended.py   # 扩展指标（最大摄氧量、训练准备度等）
│   ├── garmin_activity_files.py  # 下载并解析 FIT/GPX 文件
│   └── garmin_query.py           # 按时间点查询数据
├── references/
│   ├── health_analysis.md        # 指标解读指南
│   ├── api.md                    # 佳明 Connect 接口说明
│   └── extended_capabilities.md  # 进阶功能说明
└── config.example.json           # 账号配置模板
```

## 🔒 隐私与安全

- 账号信息仅保存在本地（绝不会发送给任何第三方）
- 会话令牌自动刷新（无需反复登录）
- 仅连接佳明官方服务器
- 不使用云存储、不向外部共享数据
- 开源项目，代码可自行审查

## 📚 相关文档与链接

**项目文档**

- **[SKILL.md](SKILL.md)** - 完整的安装、命令与故障排查说明
- **[references/health_analysis.md](references/health_analysis.md)** - 有科学依据的指标解读方法
- **[references/api.md](references/api.md)** - 佳明 Connect 接口详细说明
- **[references/extended_capabilities.md](references/extended_capabilities.md)** - 进阶功能说明

**官方链接**

- **佳明 Connect 中国大陆版**：[connect.garmin.cn](https://connect.garmin.cn)
- **佳明 Connect 国际版**：[connect.garmin.com](https://connect.garmin.com)

## 🐛 常见问题排查

**登录认证出现问题？**
- 重新运行 `python3 scripts/garmin_auth.py login` 刷新令牌
- 检查 config.json 或环境变量中的账号信息是否正确
- 尝试登录佳明 Connect 网页版，确认账号可用
- 请确认配置文件中的 `is_cn` 与你的账号注册区域一致（中国大陆 `true`，国际版 `false`），或使用 `--cn` 参数显式指定

**缺少数据？**
- 部分指标需要特定设备支持（身体电量需要支持心率变异性的手表）
- 检查对应时间段内是否佩戴了设备
- 新账号的历史数据可能较少

**请求频率受限？**
- 佳明会限制接口请求频率，请等待几分钟后再试
- 尽量批量查询（用 `summary` 命令代替多次单独调用）

## 📄 版本信息

- **作者**：Earthaveeman
- **版本**：1.0.1（2026-11-12 更新）
- **首次发布**：1.0.0（2026-11-11，中国大陆适配版）
- **更新日期**：2026-11-12
- **许可证**：MIT
- **依赖库**：garminconnect、fitparse、gpxpy（均通过 pip 安装）

---

**如有疑问？** 请在本项目提交 Issue，或查阅上方文档。
