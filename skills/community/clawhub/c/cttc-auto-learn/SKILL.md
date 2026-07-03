---
name: cttc-auto-learn
description: >-
  烟草网络学院 (mooc.ctt.cn) 自动学习脚本，支持刷学时、刷专题、刷课程、刷任务四种模式。
  用户说"帮我刷学时"即可自动完成登录、播放视频、累计学时全流程。
  触发词：烟草、网络学院、mooc、cttc、自动学习、学时。
license: MIT
compatibility: Requires Python 3.11+, uv, Playwright, and access to mooc.ctt.cn
metadata:
  author: gandli
  version: "1.0.0"
  project_url: https://github.com/gandli/cttc-auto-learn
  platform: mooc.ctt.cn
  categories: automation, education, browser-automation
  topics: video-learning, china-tobacco, mooc, playwright, study-hours, qr-login
  tags: playwright, automation, china-tobacco, video, agent-workflow
  changelog: |
    v1.0.0 (2026-06-18) - 初始发布
    - 支持刷学时、刷专题、刷课程、刷任务四种模式
    - QR 码登录（APP + 微信双二维码）
    - 事件驱动登录检测（framenavigated）
    - 自动凭证管理（保存/恢复/定期更新）
    - 实时状态监控（status.json）
    - AES-128-ECB 加密的 video-progress API
    - 单实例文件锁 + 标签页管理
    - 崩溃自动恢复（最多 5 次）
allowed-tools: Bash(uv:*) Bash(git:*) Bash(taskkill:*) Read Write
---

# 烟草网络学院自动学习

> 用户只需安装此 SKILL，说"帮我刷学时"即可。Agent 自动完成环境搭建、登录、学习。

## 支持模式

| 模式 | 命令 | 说明 |
|------|------|------|
| 刷学时 | `uv run python main.py --mode hours` | 播放视频累计学时（默认） |
| 刷专题 | `uv run python main.py --mode topics` | 完成专题课程 |
| 刷课程 | `uv run python main.py --mode courses` | 完成所有未完成课程 |
| 刷任务 | `uv run python main.py --mode tasks` | 完成指定任务 |

**触发词对应模式：**
- "帮我刷学时" / "累计学时" → `--mode hours`
- "帮我刷专题" / "完成专题" → `--mode topics`
- "帮我刷课程" / "完成课程" → `--mode courses`
- "帮我刷任务" / "完成任务" → `--mode tasks`

## Agent 执行流程（按顺序执行）

### Step 1: 克隆项目（如果还没有）

```bash
# 检查项目是否存在
if [ ! -d ~/Desktop/cttc-auto-learn ]; then
  git clone https://github.com/gandli/cttc-auto-learn.git ~/Desktop/cttc-auto-learn
fi
cd ~/Desktop/cttc-auto-learn
```

### Step 2: 安装依赖

```bash
cd ~/Desktop/cttc-auto-learn
uv sync
```

### Step 3: 清理环境

```bash
# 杀掉残留 Chrome 进程（注意：不要误杀其他 Chrome）
taskkill //F //IM chrome.exe 2>/dev/null || true
# 清除 Python 缓存
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
```

### Step 4: 首次登录（需要用户扫码）

检查凭证文件是否存在且有效：

```bash
ls output/auth-state.json 2>/dev/null
```

**如果不存在或已过期**，需要用户扫码登录：

```bash
cd ~/Desktop/cttc-auto-learn
uv run python main.py
```

**登录流程特性：**
- **事件驱动**：监听页面跳转 (`framenavigated`)，扫码后立即检测成功
- **双二维码**：同时提供 APP 和微信两种扫码方式
- **自动刷新**：二维码过期时自动刷新并重新保存图片
- **即时响应**：无需轮询，登录成功后立即开始学习

**二维码图片位置：**
- `output/qrcode-app.png` — APP 扫码
- `output/qrcode-wechat.png` — 微信扫码

**Agent 操作步骤：**
1. 启动脚本后，等待二维码生成（约 5 秒）
2. 监控日志获取二维码路径：
   ```bash
   tail -20 ~/Desktop/cttc-auto-learn/logs/cttc.log | grep "QR_PATHS"
   ```
3. 读取二维码图片并发送给用户
4. 用户扫码后，脚本自动检测登录成功
5. 凭证自动保存到 `output/auth-state.json`

**如果已存在**，跳到 Step 5。

### Step 5: 运行自动学习

```bash
cd ~/Desktop/cttc-auto-learn
uv run python main.py
```

脚本会自动：
1. 恢复登录状态（使用 `output/auth-state.json`）
2. 通过 API 获取课程列表
3. 逐个播放未完成的视频
4. 监控学时进度
5. 达到目标后自动退出

### Step 6: 监控运行

脚本运行后，Agent **必须**主动监控状态并定期向用户汇报进展。

#### 6.1 检查脚本是否在运行

```bash
# 检查 Python 进程
tasklist 2>/dev/null | grep -i python || echo "脚本未运行"

# 或检查状态文件是否存在
ls ~/Desktop/cttc-auto-learn/output/status.json 2>/dev/null && echo "脚本已启动" || echo "脚本未运行"
```

#### 6.2 读取实时状态（推荐）

状态文件 `output/status.json` 每 30 秒自动更新，Agent 可直接读取：

```bash
cat ~/Desktop/cttc-auto-learn/output/status.json
```

状态字段说明：

| 字段 | 类型 | 说明 |
|------|------|------|
| `status` | string | `playing` / `completed` / `error` |
| `current_video` | string | 当前播放的课程名称 |
| `video_progress` | float | DOM 进度百分比 (0-100) |
| `api_completed_rate` | int | API 返回的完成率 |
| `study_hours_current` | float | 当前学时 |
| `study_hours_target` | float | 目标学时 |
| `courses_completed` | int | 已完成课程数 |
| `courses_pending` | int | 待学课程数 |
| `courses_total` | int | 总课程数 |
| `errors_count` | int | 累计错误次数 |
| `stall_recoveries` | int | 停滞恢复次数 |
| `uptime_seconds` | int | 运行时长（秒） |
| `last_update` | string | 最后更新时间 |

#### 6.3 终端监控面板

在另一个终端运行实时监控（有进度条和颜色）：

```bash
cd ~/Desktop/cttc-auto-learn
uv run python scripts/monitor.py
```

#### 6.4 查看日志

```bash
tail -50 ~/Desktop/cttc-auto-learn/logs/cttc.log
```

#### 6.5 Agent 主动汇报模板

Agent 应定期（每 5-10 分钟或用户询问时）读取状态并向用户汇报：

```
📊 当前状态
- 状态: playing
- 视频: 全链路数智化转型 (48.1%)
- 学时: 28.1/50.0h (56.2%)
- 课程: 0 完成 / 76 待学
- 运行: 25 分钟
- 错误: 0 次
```

**关键事件必须立即通知用户：**
- ✅ 视频完成（`status` 变为 `completed` 或新视频开始）
- 📈 学时增长（`study_hours_current` 变化）
- ❌ 错误发生（`errors_count` 增加）
- 🎯 达到目标（`study_hours_current` >= `study_hours_target`）

## 运行参数

在 `main.py` 中可调整：

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `target_hours` | 50 | 目标学时（小时） |
| `headless` | False | 无头模式（不显示浏览器窗口） |

## 常见问题

| 问题 | 原因 | 解决 |
|------|------|------|
| `40909` 多开限制 | localStorage 残留旧会话 | 脚本已自动处理（启动时清除） |
| `40904` 错误 | studyTime 不正确 | 脚本已自动修正为增量值 |
| 浏览器崩溃 | GPU 进程异常 | 脚本已加 `--disable-gpu` 参数 |
| 学时不增长 | 服务器异步结算 | 持续运行，隔天检查 |
| 二维码过期 | 超过 2 分钟未扫码 | 脚本会自动刷新二维码 |

## 技术细节（供参考）

- **加密**：video-progress API 使用 AES-128-ECB，密钥 `d8cg8gVakEq9Agup`
- **防挂机**：每 25 分钟自动触发 mousemove 事件
- **单实例**：文件锁防止多个脚本同时运行
- **标签页管理**：自动关闭多余标签页，确保只播放一个视频
- **弹窗处理**：自动关闭弹窗，但排除视频播放器区域
