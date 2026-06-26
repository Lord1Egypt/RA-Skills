---
name: Bilibili-trending
description: 获取 Bilibili 全榜单热门数据并分析趋势。支持 21 个榜单，自动调用子 Agent 分析并生成 MD 报告持久化储存。安全无隐私风险，仅调用公开 API。
---

# Bilibili Trending

获取 B 站热门数据 → 自动调用子 Agent 分析 → 持久化储存 → 趋势预测

## 安全说明

- **仅调用公开 API**：使用 B 站公开排行榜 API，不涉及登录、Cookie、用户信息
- **无个人信息**：只获取热门视频数据，不采集任何用户身份信息
- **本地存储**：数据保存在本地工作区，不上传到任何外部服务器
- **标准请求头**：仅使用标准 User-Agent，无特殊权限
- **自动重试**：API 限流（-352）时自动等待并重试（最多 3 次）

## 环境要求

- Python 3.x
- `requests` 库
- **OpenClaw 环境**（用于自动调用子 Agent）

## 支持 21 个榜单

| 类型 | 榜单 |
|------|------|
| **普通视频** | 全站、动画、游戏、音乐、舞蹈、鬼畜、影视、娱乐、知识、科技数码、美食、汽车、时尚美妆、体育运动、动物 |
| **PGC 内容** | 番剧、国创、纪录片、电影、电视剧 |

---

## 使用方式

> 以下命令在 skill 目录下执行（脚本会根据相对于工作区的位置自动创建所需目录）

### 抓取并分析单个榜单

```bash
cd skills/Bilibili-trending/scripts
python bilibili_all.py --rank <榜单>
```

示例：
```bash
python bilibili_all.py --rank game    # 游戏榜
python bilibili_all.py --rank tv      # 电视剧榜
python bilibili_all.py --rank anime   # 番剧榜
python bilibili_all.py --rank all     # 全站榜
```

### 列出所有榜单

```bash
python bilibili_all.py --list
```

### 手动模式（输出 prompt 不调用子 Agent）

```bash
python bilibili_all.py --rank game --manual
```

### 抓取并检测异常

```bash
python bilibili_all.py --rank game --alert    # 抓取后自动运行异常检测
python bilibili_all.py --rank game -a -m      # 手动模式 + 异常检测
```

---

## 完整流程

### Step 1: 抓取数据

脚本自动完成：
1. 调用 B 站 API 抓取数据
2. 处理数据（计算互动率、提取关键词）
3. 保存 JSON 到 `{工作区}/json/output_{rank_type}.json`
4. 更新趋势数据到 `trend.json`

### Step 2: 自动分析

脚本自动 spawn 子 Agent，发送分析 prompt

### Step 3: 保存报告

分析完成后，报告自动保存到：
```
{工作区}/memory/bilibili-analysis/{榜单名称}_{时间}.md
```
例如：`游戏_2026-04-02-15-30-45.md`

---

## 趋势分析命令

> 在 `skills/Bilibili-trending/scripts` 目录下执行

### 查看趋势

```bash
python bili_trend.py trend          # 全局趋势
python bili_trend.py trend game     # 单榜单趋势
```

### 生成周总结

```bash
python bili_trend.py weekly         # 全站周总结
python bili_trend.py weekly game    # 单榜单周总结
```

### 生成月总结

```bash
python bili_trend.py monthly        # 全站月总结
python bili_trend.py monthly game   # 单榜单月总结
```

### 对已有数据重新分析

```bash
python bili_trend.py workflow game           # 自动调用子 Agent
python bili_trend.py workflow game --manual  # 仅输出 prompt
```

### 定时自动采集

```bash
python bili_trend.py daemon                      # 默认 2h 间隔，采集全部 21 个榜单
python bili_trend.py daemon --interval 30m       # 每 30 分钟采集一次
python bili_trend.py daemon -i 4h -r game,anime  # 每 4 小时采集游戏+番剧榜
python bili_trend.py daemon --no-alert           # 关闭异常检测
```

按 `Ctrl+C` 优雅停止。

---

## 非 OpenClaw 环境

如果没有 OpenClaw 环境：
- 脚本检测到无法导入 `sessions_spawn`
- 自动输出 prompt 供手动使用
- 用户可将 prompt 发送给子 Agent 手动分析

---

## 关键词提取逻辑

```python
# 1. 正则提取 2-4 字中文
words = re.findall(r'[\u4e00-\u9fa5]{2,4}', title)

# 2. 统计词频
kw_counter = Counter(words)

# 3. 取 Top 10
top_keywords = [kw for kw, _ in kw_counter.most_common(10)]
```

---

## 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `BILIBILI_WORKSPACE` | 工作区路径（JSON 和报告的输出目录） | 自动检测（scripts/ 往上 3 级） |

---

## 异常检测

当使用 `--alert` 或 daemon 模式时，自动检测以下 4 类异常：

| 类型 | 级别 | 检测规则 |
|------|------|----------|
| **互动率飙升** | HOT | 视频互动率 > 历史均值 × 2.5 |
| **新 UP 主上榜** | INFO | UP 主首次出现在该榜单 |
| **分区热度突变** | WARN | 分区占比 > 历史均值 × 2.0 |
| **关键词爆发** | INFO | 新关键词首次进入 Top 10 |

预警数据保存到 `memory/bilibili-analysis/alerts.json`（最近 200 条），UP 主历史记录保存到 `up_history_{rank_type}.json`。

> 需要至少 3 条历史趋势记录才会启动检测。

---

## 脚本结构

```
scripts/
├── config.py         # 21 个榜单配置
├── common.py         # 共享工具（路径、持久化、关键词、prompt、API 重试、抓取、Agent 调用）
├── alerts.py         # 异常检测（互动率、新UP主、分区突变、关键词爆发）
├── bilibili_all.py   # 主入口：抓取 → 处理 → 保存 → 分析（支持 --alert）
└── bili_trend.py     # 趋势分析：trend / weekly / monthly / workflow / daemon
```

---

## 输出文件

脚本会在工作区自动创建以下目录结构：

```
{工作区}/
├── json/                           # JSON 数据目录
│   └── output_{rank_type}.json      # 原始数据（含 owner 字段）
└── memory/bilibili-analysis/        # 分析结果目录
    ├── trend.json                    # 趋势累计数据（最近 60 条）
    ├── alerts.json                   # 预警记录（最近 200 条）
    ├── up_history_game.json          # 游戏榜历史 UP 主
    ├── 游戏_2026-04-02-15-30-45.md  # 分析报告
    ├── weekly-2026-W14.md           # 周总结
    └── monthly-2026-04.md           # 月总结
```

---

## 注意事项

- 频繁请求会触发 API 限流（-352 错误），脚本已内置自动重试 + 递增等待
- 趋势数据需长期积累（建议 30+ 次）才能形成可靠预测
- 子 Agent 分析完成后报告自动保存
- 普通视频数据包含 `owner` 字段，支持 UP 主生态分析
