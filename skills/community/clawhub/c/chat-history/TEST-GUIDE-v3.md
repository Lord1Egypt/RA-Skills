# Chat History v3.0 测试指南

## 📋 测试前准备

1. **备份现有数据**
```bash
cp -r ~/.openclaw/workspace/conversation-archives ~/.openclaw/workspace/conversation-archives-backup
```

2. **检查环境**
```bash
# 确认 OpenClaw CLI 可用
openclaw --version

# 确认 Python 3
python3 --version
```

---

## ✅ 功能测试

### 1. 基础功能测试

```bash
cd ~/.openclaw/workspace/skills/chat_history

# 测试帮助信息
python3 main_v3.py --help

# 测试状态查询
python3 main_v3.py --status

# 测试归档功能
python3 main_v3.py --archive
```

**预期结果**：
- ✅ 显示完整帮助信息
- ✅ 显示当前状态
- ✅ 成功执行归档（无错误）

---

### 2. Cron 功能测试

```bash
# 设置定时任务
python3 main_v3.py --setup-cron

# 检查任务是否存在
openclaw cron list | grep chat-history

# 测试修改归档时间
python3 main_v3.py --set-time "22:00"

# 验证时间已更新
openclaw cron list | grep chat-history

# 移除定时任务
python3 main_v3.py --remove-cron

# 验证已移除
openclaw cron list | grep chat-history
# 应该无输出
```

**预期结果**：
- ✅ 成功添加 cron 任务
- ✅ 任务显示在 `openclaw cron list` 中
- ✅ 成功修改归档时间
- ✅ 成功移除任务

---

### 3. 跨平台测试

#### macOS 测试：
```bash
# 所有命令应该正常执行
python3 main_v3.py --setup-cron
python3 main_v3.py --status
```

#### Windows 测试（PowerShell）：
```powershell
# 进入 skill 目录
cd "$env:USERPROFILE\.openclaw\workspace\skills\chat_history"

# 执行测试
python main_v3.py --help
python main_v3.py --status
python main_v3.py --setup-cron
```

**预期结果**：
- ✅ macOS 正常运行
- ✅ Windows 正常运行（无 crontab 错误）

---

### 4. 安全性验证

```bash
# 检查是否还有系统命令
grep -n "os.popen\|os.system" main_v3.py
# 应该无输出

# 检查是否还有 crontab 调用
grep -n "crontab" main_v3.py
# 应该只在注释或 OpenClaw CLI 调用中出现

# 检查硬编码路径
grep -n "/Users/tanghao" main_v3.py
# 应该无输出
```

**预期结果**：
- ✅ 无系统命令调用
- ✅ 无硬编码路径
- ✅ 所有路径使用动态检测

---

## 🔍 问题排查

### 问题1：OpenClaw CLI 不可用
```
错误：openclaw: command not found
解决：确认 OpenClaw 已安装并添加到 PATH
```

### 问题2：Python 版本不兼容
```
错误：SyntaxError: invalid syntax
解决：确保 Python 3.6+
python3 --version
```

### 问题3：权限问题
```
错误：Permission denied
解决：检查文件权限
chmod +x main_v3.py
```

---

## 📊 测试检查清单

| 测试项 | 状态 | 说明 |
|--------|------|------|
| --help | ⬜ | 显示帮助信息 |
| --status | ⬜ | 显示当前状态 |
| --archive | ⬜ | 执行归档 |
| --setup-cron | ⬜ | 设置定时任务 |
| --remove-cron | ⬜ | 移除定时任务 |
| --set-time | ⬜ | 修改归档时间 |
| macOS 兼容 | ⬜ | macOS 正常运行 |
| Windows 兼容 | ⬜ | Windows 正常运行 |
| 无系统命令 | ⬜ | 安全扫描通过 |
| 无硬编码路径 | ⬜ | 路径动态检测 |

---

## ✅ 测试通过标准

- ✅ 所有基础功能正常
- ✅ Cron 功能正常
- ✅ macOS/Windows 兼容
- ✅ 无系统命令调用
- ✅ 无硬编码路径
- ✅ 安全扫描通过

---

*测试指南版本：v3.0*
*最后更新：2026-03-10*
