# emoTwin 改进版本 - 打包信息

## 打包时间
2026-03-12 06:13 GMT+8

## 改进内容

### 1. 用户可选择情绪同步频率
- 启动时交互式选择：30秒 / 60秒 / 5分钟 / 自定义
- 配置自动保存到 `~/.emotwin/sync_interval.txt`
- 支持 10-3600 秒的任意间隔

### 2. Cron任务静默模式
- 使用 `delivery.mode: "none"`
- 不发送系统消息到用户聊天窗口
- 后台静默执行社交周期

## 文件清单

| 文件 | 说明 |
|------|------|
| `SKILL.md` | 技能文档（已更新） |
| `README.md` | GitHub文档（已更新） |
| `start_emotwin.sh` | 启动脚本（主要改进） |
| `stop_emotwin.sh` | 停止脚本（显示上次频率） |
| `scripts/` | 核心脚本目录 |
| `test_cron_silent.py` | 静默模式测试脚本 |

## 安装方法

```bash
# 解压到OpenClaw skills目录
cd ~/.openclaw/skills
tar -xzf emotwin-improved-20260312_061357.tar.gz

# 确保脚本可执行
chmod +x emotwin/start_emotwin.sh emotwin/stop_emotwin.sh
```

## 使用

```bash
# 启动（会提示选择频率）
~/.openclaw/skills/emotwin/start_emotwin.sh

# 停止
~/.openclaw/skills/emotwin/stop_emotwin.sh
```

## 备份位置
`~/.openclaw/skills/emotwin/emotwin-improved-20260312_061357.tar.gz`
