# Flomo 自动同步到 Obsidian

使用浏览器自动化实现 flomo 到 Obsidian 的全自动增量同步。

## 🎯 功能特性

### ✅ 已实现
- **自动导出**：使用 Playwright 浏览器自动化，自动登录并导出 flomo 数据
- **增量同步**：只同步新增的笔记，避免重复处理
- **附件支持**：自动下载并复制图片和音频附件
- **状态记录**：记录同步状态，断点续传
- **自动清理**：自动清理旧的导出文件，节省空间
- **错误恢复**：出错时保存截图，便于调试

### 🔄 工作流程

```
1. 自动登录 flomo 网页版
     ↓
2. 触发数据导出功能
     ↓
3. 下载 ZIP 导出文件
     ↓
4. 解压并解析 HTML
     ↓
5. 检测新增笔记（增量）
     ↓
6. 转换为 Markdown 格式
     ↓
7. 复制附件到 Obsidian
     ↓
8. 更新同步状态
     ↓
9. 清理旧导出文件
```

## 📦 安装依赖

### 1. 安装 Python 依赖

```bash
pip install playwright beautifulsoup4 markdownify
```

### 2. 安装 Playwright 浏览器

```bash
playwright install chromium
```

这会下载 Chromium 浏览器（约 150MB），用于自动化操作。

## 🚀 快速开始

### 方式1：命令行直接使用（推荐初次测试）

```bash
python scripts/auto_sync.py \
  --email "your-email@example.com" \
  --password "your-password" \
  --output "/path/to/obsidian/vault/flomo" \
  --tag-prefix "flomo/" \
  --no-headless  # 首次运行建议显示浏览器，观察过程
```

**参数说明：**
- `--email`：你的 flomo 登录邮箱（必需）
- `--password`：你的 flomo 登录密码（必需）
- `--output`：Obsidian vault 中的目标目录（必需）
- `--tag-prefix`：标签前缀，默认 `flomo/`
- `--download-dir`：下载临时目录，默认 `./flomo_downloads`
- `--state-file`：同步状态文件，默认 `.flomo_sync_state.json`
- `--force-full`：强制完整同步（忽略增量检测）
- `--no-headless`：显示浏览器窗口（调试用）
- `--cleanup`：保留最近 N 次导出文件，默认 3
- `--verbose`：显示详细日志

### 方式2：使用配置文件（推荐日常使用）

1. **复制配置文件模板：**

```bash
cp config.example.json config.json
```

2. **编辑 `config.json`：**

```json
{
  "flomo": {
    "email": "your-email@example.com",
    "password": "your-password"
  },
  "obsidian": {
    "vault_path": "/Users/username/mynote/flomo",
    "tag_prefix": "flomo/"
  },
  "sync": {
    "download_dir": "./flomo_downloads",
    "state_file": ".flomo_sync_state.json",
    "keep_exports": 3,
    "headless": true
  }
}
```

3. **创建同步脚本 `sync.sh`：**

```bash
#!/bin/bash
cd /path/to/flomo-to-obsidian

CONFIG=$(cat config.json)
EMAIL=$(echo $CONFIG | jq -r '.flomo.email')
PASSWORD=$(echo $CONFIG | jq -r '.flomo.password')
VAULT=$(echo $CONFIG | jq -r '.obsidian.vault_path')
TAG_PREFIX=$(echo $CONFIG | jq -r '.obsidian.tag_prefix')

python scripts/auto_sync.py \
  --email "$EMAIL" \
  --password "$PASSWORD" \
  --output "$VAULT" \
  --tag-prefix "$TAG_PREFIX"
```

4. **添加执行权限：**

```bash
chmod +x sync.sh
```

5. **执行同步：**

```bash
./sync.sh
```

## ⏰ 设置定时自动同步

### macOS / Linux：使用 cron

1. **编辑 crontab：**

```bash
crontab -e
```

2. **添加定时任务：**

```bash
# 每天凌晨 2 点自动同步
0 2 * * * cd /path/to/flomo-to-obsidian && ./sync.sh >> /tmp/flomo_sync.log 2>&1

# 每 6 小时同步一次
0 */6 * * * cd /path/to/flomo-to-obsidian && ./sync.sh >> /tmp/flomo_sync.log 2>&1

# 每天 8:00、14:00、20:00 同步
0 8,14,20 * * * cd /path/to/flomo-to-obsidian && ./sync.sh >> /tmp/flomo_sync.log 2>&1
```

3. **查看日志：**

```bash
tail -f /tmp/flomo_sync.log
```

### 使用 OpenClaw 的定时任务功能（推荐）

你可以使用 OpenClaw 的 `scheduled_task` 来创建定时任务：

```bash
# 通过 OpenClaw 创建定时任务
use_skill("scheduled-task-creator")

# 然后告诉 AI：
# "帮我创建一个定时任务，每天晚上 10 点自动同步 flomo 到 Obsidian"
```

## 📊 同步状态文件

同步状态保存在 `.flomo_sync_state.json` 中：

```json
{
  "last_sync_time": "2024-03-11T16:30:00",
  "synced_notes": {
    "2024-03-11 16:20:15": "flomo-20240311-162015",
    "2024-03-11 16:25:30": "flomo-20240311-162530"
  },
  "last_export_file": "/path/to/flomo_export_20240311_163000.html",
  "sync_count": 15
}
```

- `last_sync_time`：最后同步时间
- `synced_notes`：已同步的笔记时间戳映射
- `last_export_file`：最后导出的文件路径
- `sync_count`：总同步次数

## 🔧 常见问题

### 1. 登录失败

**问题**：浏览器自动化无法登录 flomo

**解决方案**：
- 使用 `--no-headless` 参数查看浏览器实际操作
- 检查邮箱和密码是否正确
- 确认 flomo 网站是否有验证码或其他安全措施
- 查看错误截图：`flomo_downloads/error_screenshot.png`

### 2. 找不到导出按钮

**问题**：脚本无法找到"导出数据"按钮

**解决方案**：
- flomo 网页版可能更新了界面
- 使用 `--no-headless` 手动观察页面结构
- 查看调试截图：`flomo_downloads/debug_screenshot.png`
- 联系作者更新选择器

### 3. 下载超时

**问题**：导出文件下载超时

**解决方案**：
- 检查网络连接
- 增加超时时间（需修改代码中的 `timeout` 参数）
- 手动导出一次，确认 flomo 服务正常

### 4. 增量同步不工作

**问题**：每次都进行完整同步

**解决方案**：
- 检查 `.flomo_sync_state.json` 文件是否存在
- 确认状态文件没有被删除
- 使用 `--force-full` 可以强制完整同步

### 5. 附件缺失

**问题**：图片或音频没有同步

**解决方案**：
- 确认 flomo 导出的 ZIP 包含 `file/` 目录
- 检查解压后的目录结构
- 查看详细日志：`auto_sync.log`

## 🔐 安全建议

### 密码安全

**方式1：使用环境变量**

```bash
export FLOMO_EMAIL="your-email@example.com"
export FLOMO_PASSWORD="your-password"

python scripts/auto_sync.py \
  --email "$FLOMO_EMAIL" \
  --password "$FLOMO_PASSWORD" \
  --output "/path/to/obsidian/vault/flomo"
```

**方式2：使用密码文件**

创建 `.env` 文件（添加到 `.gitignore`）：

```bash
FLOMO_EMAIL=your-email@example.com
FLOMO_PASSWORD=your-password
```

修改 `sync.sh` 读取环境变量：

```bash
#!/bin/bash
source .env

python scripts/auto_sync.py \
  --email "$FLOMO_EMAIL" \
  --password "$FLOMO_PASSWORD" \
  --output "/path/to/obsidian/vault/flomo"
```

⚠️ **重要**：不要将包含密码的文件提交到 Git！

## 📝 使用示例

### 示例1：首次完整同步

```bash
python scripts/auto_sync.py \
  --email "ryan@example.com" \
  --password "mypassword" \
  --output "/Users/ryan/mynote/flomo" \
  --force-full \
  --no-headless \
  --verbose
```

**说明**：
- `--force-full`：忽略增量，同步所有笔记
- `--no-headless`：显示浏览器，方便观察
- `--verbose`：显示详细日志

### 示例2：日常增量同步

```bash
python scripts/auto_sync.py \
  --email "ryan@example.com" \
  --password "mypassword" \
  --output "/Users/ryan/mynote/flomo"
```

**说明**：自动检测新笔记，只同步增量数据

### 示例3：清理旧文件

```bash
python scripts/auto_sync.py \
  --email "ryan@example.com" \
  --password "mypassword" \
  --output "/Users/ryan/mynote/flomo" \
  --cleanup 1
```

**说明**：`--cleanup 1` 只保留最近 1 次导出文件

## 📈 性能优化

### 减少网络流量

- 使用增量同步（默认行为）
- 定期清理旧导出文件
- 只在笔记较多时同步

### 提升同步速度

- 使用 `--headless` 模式（默认）
- 在网络良好的环境下运行
- 避免在高峰时段同步

## 🐛 调试技巧

### 查看详细日志

```bash
python scripts/auto_sync.py \
  --email "..." \
  --password "..." \
  --output "..." \
  --verbose
```

### 显示浏览器操作

```bash
python scripts/auto_sync.py \
  --email "..." \
  --password "..." \
  --output "..." \
  --no-headless
```

### 查看错误截图

出错时会自动保存截图：
- `flomo_downloads/error_screenshot.png` - 错误时的截图
- `flomo_downloads/debug_screenshot.png` - 调试截图

### 查看同步日志

```bash
tail -f auto_sync.log
```

## 📚 高级用法

### 自定义下载目录

```bash
python scripts/auto_sync.py \
  --email "..." \
  --password "..." \
  --output "/path/to/obsidian/vault/flomo" \
  --download-dir "/tmp/flomo_downloads"
```

### 自定义状态文件位置

```bash
python scripts/auto_sync.py \
  --email "..." \
  --password "..." \
  --output "/path/to/obsidian/vault/flomo" \
  --state-file "/path/to/.flomo_sync_state.json"
```

### 不使用标签前缀

```bash
python scripts/auto_sync.py \
  --email "..." \
  --password "..." \
  --output "/path/to/obsidian/vault/flomo" \
  --tag-prefix ""
```

## 🔄 版本更新

### V3.0.0 (2024-03-11)
- ✅ 新增：浏览器自动化导出
- ✅ 新增：增量同步机制
- ✅ 新增：自动清理旧文件
- ✅ 新增：错误截图调试
- ✅ 改进：更稳定的登录流程
- ✅ 改进：更完善的错误处理

## 🤝 贡献

如果你发现 flomo 网页版更新导致脚本失效，欢迎：
1. 提交 Issue 说明问题
2. 提供错误截图
3. Fork 并提交 PR 修复

## 📄 许可证

MIT License
