---
name: epic-free-games
description: >
  Auto-claim free games from Epic Games Store. 2026 latest page adaptation with 
  persistent login state, completes the full claim process (Get → Place Order → Confirm).
  自动领取 Epic Games Store 每周免费游戏。2026年最新页面适配，支持持久化登录状态，
  自动完成完整领取流程（获取 → 下订单 → 确认领取）。
metadata:
  openclaw:
    requires:
      commands: ["agent-browser"]
---

# Epic Free Games Auto Claimer / Epic 免费游戏自动领取

Auto-claim weekly free games from Epic Games Store.

自动领取 Epic Games Store 每周免费游戏。

## ⚠️ Risk Warning / 风险提示

**English:**
- **Account Risk**: Automated tools may violate Epic's Terms of Service. Use at your own risk. Account suspension is possible.
- **Human Verification**: hCaptcha/Cloudflare verification cannot be bypassed automatically. Manual intervention required when prompted.
- **Educational Purpose**: This tool is for learning purposes only. Do not abuse it.
- **No Warranty**: Use at your own risk. The author is not responsible for any consequences.

**中文：**
- **账号风险**：自动化工具可能违反 Epic 服务条款，使用风险自负。可能导致账号封禁。
- **人机验证**：无法自动绕过 hCaptcha/Cloudflare 验证，需要手动处理。
- **仅供学习**：本工具仅供学习研究使用，请勿滥用。
- **免责声明**：使用风险自负，作者不对任何后果负责。

## Features / 功能特点

- **2026 Latest Adaptation / 2026年最新适配** - Uses stable `data-testid` selectors / 使用稳定的 `data-testid` 选择器
- **Persistent Login / 持久化登录** - Login once, works forever (saves cookies) / 一次登录，永久生效（保存 Cookie）
- **Full Claim Process / 完整领取流程** - Get → Place Order → Confirm / 获取 → 0元下订单 → 确认领取
- **Cron Support / 定时任务支持** - Auto-claim every Thursday / 每周四自动领取

## Quick Start / 快速开始

```bash
# First time login (manual login required) / 首次登录（需要手动登录一次）
python scripts/claim.py --login

# Auto-claim free games / 自动领取免费游戏
python scripts/claim.py

# Show browser window (for captcha handling) / 显示浏览器窗口（用于处理验证码）
python scripts/claim.py --headed

# View help / 查看帮助
python scripts/claim.py --help
```

## Usage Steps / 使用步骤

### 1. First Login / 首次登录

```bash
python scripts/claim.py --login
```

Opens browser window for manual Epic login. After login, auth state is saved to `epic_auth.json`.

打开浏览器窗口，手动登录 Epic 账号。登录完成后，登录状态会保存到 `epic_auth.json`。

### 2. Auto Claim / 自动领取

```bash
python scripts/claim.py
```

Automatically:
1. Opens Epic free games page / 打开 Epic 免费游戏页面
2. Loads saved auth state / 加载保存的登录状态
3. Clicks "Get" button / 点击"获取"按钮
4. Clicks "Place Order" for $0 purchase / 点击"下订单"完成 0 元购买
5. Confirms success / 确认领取成功

### 3. Cron Task / 定时任务

Set up cron for weekly auto-claim:

设置定时任务，每周四自动领取：

```bash
# Every Thursday at 00:20 / 每周四 00:20 执行
20 0 * * 4 cd /path/to/epic-free-games && python scripts/claim.py
```

## CLI Arguments / 命令行参数

| Argument | Description |
|----------|-------------|
| `--login` | First-time login mode / 首次登录模式 |
| `--headed` | Show browser window / 显示浏览器窗口 |
| `--timeout N` | Wait timeout in seconds / 等待超时时间（秒） |
| `--auth-file FILE` | Auth state file path / 登录状态文件路径 |

## Files / 文件说明

```
epic-free-games/
├── SKILL.md           # This file / 本说明文件
├── scripts/
│   └── claim.py       # Main script / 主脚本
└── epic_auth.json     # Auth state (auto-generated) / 登录状态缓存（自动生成）
```

## Dependencies / 依赖

- [agent-browser](https://github.com/vercel-labs/agent-browser) - Browser automation CLI / 浏览器自动化 CLI

Install / 安装：
```bash
npm install -g agent-browser
agent-browser install
```

## Limitations / 限制

1. **Cloudflare/hCaptcha** - Cannot bypass automatically, use `--headed` for manual handling / 无法自动绕过，使用 `--headed` 手动处理
2. **Login Expiry** - Re-run `--login` if session expires / 登录过期时重新运行 `--login`
3. **Already Owned** - Script detects and skips owned games / 脚本会检测并跳过已拥有游戏

## 🔒 Security Best Practices / 安全最佳实践

**IMPORTANT: This skill does NOT contain any pre-filled authentication files.**

**重要：本技能不包含任何预填充的认证文件。**

### For Users / 用户须知

1. **Generate Your Own Auth File / 自行生成认证文件**
   - Run `python scripts/claim.py --login` to create your own `epic_auth.json`
   - Never share your auth file with others / 不要分享你的认证文件
   - The auth file contains sensitive credentials / 认证文件包含敏感凭证

2. **Keep Auth File Private / 保护认证文件**
   - Add `epic_auth.json` to `.gitignore` if using git
   - Do not upload to public repositories / 不要上传到公开仓库

3. **Isolated Environment / 隔离环境**
   - Consider running in a sandbox or VM / 建议在沙箱或虚拟机中运行
   - Review the source code before running / 运行前请审查源代码

### For Developers / 开发者须知

1. **Never Commit Sensitive Files / 不要提交敏感文件**
   ```
   # These files should NEVER be in the distribution:
   # 以下文件绝对不应出现在分发包中：
   - epic_auth.json
   - browser-profile/
   - browser_profile/
   - *.png (screenshots may contain sensitive info)
   ```

2. **Use .gitignore / 使用 .gitignore**
   - The skill includes a `.gitignore` file to prevent accidental commits
   - 本技能包含 `.gitignore` 文件，防止意外提交

3. **Security First / 安全第一**
   - User credentials are private / 用户凭证是私密的
   - Never bundle auth files in distributions / 分发时绝不要打包认证文件

## Usage Tips / 使用技巧

### Cloudflare 验证绕过

Epic 网站使用 Cloudflare 验证检测自动化访问。使用 `--headed` 显示浏览器窗口手动处理验证：

```bash
# 显示浏览器窗口 + 禁用自动化检测标志
agent-browser --headed --session epic \
  --args "--disable-blink-features=AutomationControlled" \
  open "https://store.epicgames.com/zh-CN/free-games"
```

### 推荐的手动 + 自动混合流程

1. **打开浏览器窗口** (自动)
2. **用户手动完成验证和登录** (手动)
3. **自动领取游戏** (自动)

### agent-browser 常用命令

```bash
agent-browser --session epic snapshot -i  # 查看页面快照
agent-browser --session epic click "ref=e55"  # 点击元素
agent-browser --session epic close  # 关闭浏览器
```

## 领取流程中的常见问题 (2026-03-27 更新)

### 1. 获取按钮不在可视区域

**问题描述**：游戏页面的"获取"按钮可能不在首屏可视区域内，需要向下滚动才能看到。

**解决方案**：
```bash
# 先滚动页面，再查找获取按钮
agent-browser --session epic scroll down 300
agent-browser --session epic snapshot -i --json
# 查找 "获取" 按钮的 ref 值，然后点击
agent-browser --session epic click "ref=e50"
```

**最佳实践**：每次打开游戏页面后，先截图确认"获取"按钮是否可见，如不可见则滚动页面。

### 2. 登录状态未持久化

**问题描述**：每次运行都需要重新登录，因为登录状态没有保存到文件。

**解决方案**：
```bash
# 登录成功后，保存登录状态到文件
agent-browser --session epic state save "epic_auth.json"

# 下次运行时加载登录状态
agent-browser --session epic state load "epic_auth.json"
```

### 3. Cloudflare 验证拦截

**问题描述**：默认的自动化浏览器会被 Cloudflare 检测并拦截。

**解决方案**：使用 `--args` 参数禁用自动化检测标志：
```bash
agent-browser --session epic --headed \
  --args "--disable-blink-features=AutomationControlled" \
  open "https://store.epicgames.com/zh-CN/free-games"
```

### 4. 结账弹窗处理

**问题描述**：点击"获取"按钮后会弹出结账窗口，需要勾选协议复选框。

**解决方案**：
```bash
# 等待结账弹窗出现
agent-browser --session epic wait 3000
# 勾选协议复选框（checkbox 类型元素）
agent-browser --session epic check "ref=e134"
# 点击"下订单"按钮
agent-browser --session epic click "ref=e132"
```

### 完整领取流程示例

```bash
# 1. 打开浏览器（带反自动化检测）
agent-browser --session epic --headed \
  --args "--disable-blink-features=AutomationControlled" \
  open "https://store.epicgames.com/zh-CN/free-games"

# 2. 等待页面加载
agent-browser --session epic wait 3000

# 3. 截图确认页面状态
agent-browser --session epic screenshot

# 4. 获取游戏链接
agent-browser --session epic eval "document.querySelector('a[href*=\"游戏名\"]')?.href"

# 5. 打开游戏页面
agent-browser --session epic open "游戏链接"

# 6. 滚动到获取按钮位置
agent-browser --session epic scroll down 300

# 7. 点击获取按钮
agent-browser --session epic click "ref=获取按钮ref"

# 8. 处理结账弹窗
agent-browser --session epic wait 3000
agent-browser --session epic check "协议复选框ref"
agent-browser --session epic click "下订单按钮ref"

# 9. 保存登录状态
agent-browser --session epic state save "epic_auth.json"
```

## License / 许可证

MIT License - Use at your own risk / 使用风险自负
