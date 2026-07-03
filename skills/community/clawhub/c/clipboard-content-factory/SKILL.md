---
name: clipboard-content-factory
description: 剪贴板内容工厂。监控剪贴板，检测到文章/链接时自动改写成抖音、小红书、B站三个平台的版本，配合定时任务可实现"复制=发布"。当用户说"监控剪贴板"、"复制内容自动改写"、"一复制就生成多平台版本"时触发此技能。
---

# clipboard-content-factory — 剪贴板内容工厂

## 核心理念

**复制 = 自动改写 = 一鱼三吃**

把任意文章/链接复制到剪贴板 → 自动改写成三个平台版本 → 保存到桌面待发布文件夹

## 工作模式

### 模式1：一次性处理
```bash
python scripts/clipboard_watcher.py --once
# 读取当前剪贴板内容 → 改写 → 保存
```

### 模式2：持续监控（后台运行）
```bash
python scripts/clipboard_watcher.py --watch --interval 3
# 每3秒检查剪贴板，发现新内容立即改写
```

### 模式3：定时触发（推荐）
通过 Cron 定时触发，每次读取剪贴板并改写最新内容

## 输出目录

```
Desktop/clipboard_content_factory/
├── 2026-06-29/
│   ├── douyin_v1.md    # 抖音版本
│   ├── xhs_v1.md       # 小红书版本
│   ├── bilibili_v1.md  # B站版本
│   └── summary.json    # 总览
```

## 使用场景

1. **看到好文章**：复制链接 → 脚本自动抓取内容并改写
2. **热点跟进**：复制热点标题 → 自动生成各平台版本
3. **定时发布**：每天9点自动改写剪贴板内容并保存

## 配置

编辑 `scripts/config.json`：

```json
{
  "watch_interval": 3,
  "output_dir": "Desktop/clipboard_content_factory",
  "platforms": ["douyin", "xhs", "bilibili"],
  "auto_copy_to_clipboard": true
}
```

## 依赖

- Python 3.8+
- social-content-converter（内容改写）
- requests（抓取链接内容）
- pyperclip 或 Tkinter（剪贴板访问）

---
## 💰 付费增值服务

想要更省事？我还提供：

| 服务 | 价格 | 内容 |
|------|------|------|
| 🚗 代安装调试 | ¥68/次 | 帮你安装配置，解决环境问题 |
| 🛠️ 定制技能开发 | ¥200起 | 根据需求开发专属技能 |
| 🚀 视频自动化陪跑 | ¥999/月 | 从0到1搭建完整视频自动化 |
| 📦 技能全家桶 | ¥199 | 11个AI技能永久用 + 代安装 |

**微信咨询**：[微信号待填写]

---
