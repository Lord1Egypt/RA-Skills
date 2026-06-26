# 🔧 OpenClaw 内置浏览器切换工具

> 一键启用/禁用内置浏览器，无需手动修改配置文件

---

## 🚀 快速开始

### 1. 安装

```bash
cd /home/ereala/.openclaw/workspace/skills/browser-toggle
chmod +x browser_toggle.py
```

### 2. 使用

**启用内置浏览器：**
```bash
python3 browser_toggle.py --enable
```

**禁用（恢复默认）：**
```bash
python3 browser_toggle.py --disable
```

**查看状态：**
```bash
python3 browser_toggle.py --status
```

---

## 📋 完整命令

| 命令 | 说明 |
|------|------|
| `--enable` | 启用内置浏览器 |
| `--disable` | 禁用内置浏览器 |
| `--status` | 查看当前状态 |
| `--headless` | 切换到无头模式 |
| `--visible` | 切换到可视化模式 |
| `--restore <文件>` | 从备份恢复 |

---

## 💡 使用场景

### 场景 1：访问需要登录的网站

```bash
# 1. 启用内置浏览器（可视化模式）
python3 browser_toggle.py --enable

# 2. 重启 OpenClaw
openclaw gateway restart

# 3. 让 AI 打开网站，手动登录
# 例如：打开百度网盘，手动登录

# 4. 后续可以切换到无头模式
python3 browser_toggle.py --visible
openclaw gateway restart
```

### 场景 2：日常自动化（无头模式）

```bash
# 启用无头模式（后台运行，不显示浏览器）
python3 browser_toggle.py --enable --headless
openclaw gateway restart
```

### 场景 3：恢复默认

```bash
# 禁用内置浏览器，使用 Chrome 扩展
python3 browser_toggle.py --disable
openclaw gateway restart
```

---

## 🔧 配置说明

### 内置浏览器模式
- **Profile:** `openclaw`
- **数据位置:** `~/.openclaw/browser/`
- **特点:** 独立空间，不访问个人浏览器数据

### Chrome 扩展模式（默认）
- **Profile:** `chrome`
- **需要:** Chrome 扩展
- **特点:** 使用个人 Chrome 浏览器

---

## 📁 备份管理

**自动备份位置：**
```
~/.openclaw/workspace/backups/
```

**备份文件名：**
```
openclaw-YYYYMMDD-HHMMSS-before-browser-toggle.json
```

**手动恢复：**
```bash
python3 browser_toggle.py --restore ~/.openclaw/workspace/backups/openclaw-20260228-220000-before-browser-toggle.json
```

---

## ⚠️ 注意事项

1. **修改配置后需要重启 OpenClaw**
   ```bash
   openclaw gateway restart
   ```

2. **首次使用需要手动登录**
   - 启用内置浏览器后，用 AI 打开网站
   - 手动输入账号密码登录
   - 登录状态会保存

3. **切换模式需要重新登录**
   - 从 `chrome` 切换到 `openclaw` 需要重新登录网站
   - 因为是两个独立的浏览器空间

4. **无头模式 vs 可视化**
   - **无头模式 (`headless: true`)**: 后台运行，不显示浏览器窗口
   - **可视化 (`headless: false`)**: 显示浏览器窗口，可以看到操作过程

---

## 🐛 故障排除

### 问题 1：Chrome 路径不正确

**错误：** `Chrome executable not found`

**解决：**
```bash
# 找到 Chrome 路径
which google-chrome
# 或
which chromium

# 编辑 openclaw.json，修改 executablePath
nano ~/.openclaw/openclaw.json
```

### 问题 2：配置失败

**解决：**
```bash
# 从备份恢复
python3 browser_toggle.py --restore <备份文件>

# 或手动恢复
cp ~/.openclaw/workspace/backups/openclaw-*.json ~/.openclaw/openclaw.json
```

### 问题 3：浏览器无法启动

**解决：**
```bash
# 检查 Chrome 是否安装
google-chrome --version

# 如未安装
sudo apt-get install google-chrome-stable
```

---

## 📖 更多文档

- [SKILL.md](SKILL.md) - Skill 说明
- [browser_toggle.py](browser_toggle.py) - 源代码

---

## 🎯 最佳实践

### 推荐配置

**日常使用（无头模式）：**
```json
{
  "browser": {
    "enabled": true,
    "defaultProfile": "openclaw",
    "headless": true
  }
}
```

**需要登录时（可视化）：**
```json
{
  "browser": {
    "enabled": true,
    "defaultProfile": "openclaw",
    "headless": false
  }
}
```

**恢复默认：**
```json
// 删除 browser 配置即可
```

---

## 🆘 获取帮助

```bash
python3 browser_toggle.py --help
```

---

*版本：v1.0*  
*最后更新：2026-02-28*
