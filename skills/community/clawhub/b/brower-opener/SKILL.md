---
name: brower-opener
description: Chrome浏览器调试环境启动工具。支持自动检测系统并启动带有远程调试端口的Chrome浏览器，提供cookie/session复用功能。使用场景包括："打开浏览器"、"打开测试浏览器"、"复用cookie打开浏览器"、"启动浏览器 复用cookie"、"启动浏览器"、"启动无痕浏览器"。当用户需要无痕模式或明确指定不复用cookie时使用独立profile模式，否则默认使用复用cookie模式。
---

# Browser Opener - Chrome调试浏览器启动工具

## 概述

本技能用于启动带有远程调试端口的Chrome浏览器，支持两种模式：

1. **复用Cookie模式（默认）** - 复用主profile的登录状态和cookie
2. **无痕/独立模式** - 使用独立profile，不保留任何会话信息

## 触发条件

当用户提到以下关键词时触发本技能：

| 触发词 | 行为模式 |
|--------|----------|
| 打开浏览器 | 默认复用cookie |
| 打开测试浏览器 | 默认复用cookie |
| 复用cookie打开浏览器 | 复用cookie |
| 启动浏览器 复用cookie | 复用cookie |
| 启动浏览器 | 默认复用cookie |
| 启动无痕浏览器 | **独立profile模式** |

### 模式自动判断

系统根据触发词自动选择模式，**无需询问用户**：

- **使用独立模式的情况**（以下任一）：
  - 用户明确提到"无痕浏览器"
  - 用户明确提到"独立profile"
  - 用户明确提到"不复用cookie"

- **其他所有情况默认使用复用cookie模式**

## 核心功能

1. **自动环境检测**
   - 检测操作系统类型（Windows/macOS/Linux）
   - 自动查找 Chrome 安装路径
   - 自动处理端口冲突

2. **双模式支持**
   - 复用模式: 复用主profile（会关闭现有Chrome窗口）
   - 独立模式: 使用独立profile（无痕，不干扰现有窗口）

3. **非阻塞启动**
   - 使用 `subprocess.Popen` 后台启动 Chrome
   - 命令立即返回，不卡住智能体
   - 启动完成后可直接连接 DevTools

## 脚本说明

本技能位于 `scripts/` 目录：

| 脚本 | 说明 | 是否必需 |
|------|------|----------|
| `launcher.py` | **主脚本**，跨平台统一入口，自动检测系统并启动 Chrome | **是** |
| `health.py` | 健康检查脚本，验证 Chrome 是否在 9222 端口正常运行 | **否**（手动运行） |

**重要说明：**
- `launcher.py` 只负责启动 Chrome，不会自动运行健康检查
- `health.py` 需要**手动运行**来验证 Chrome 是否已就绪
- 建议在 `launcher.py` 启动后等待 2-3 秒，然后手动运行 `health.py` 确认状态

## 工作流程

### 推荐用法：使用 launcher.py + health.py（可选）

**完整工作流程：**

```
1. 解析用户请求，检测触发关键词
   ↓
2. 判断是否使用独立模式
   ├─ 触发词包含"无痕"/"独立profile"/"不复用" → 使用 --mode independent
   └─ 其他情况 → 使用 --mode reuse（默认）
   ↓
3. 运行 launcher.py 启动 Chrome
   ├─ 自动检测操作系统类型
   ├─ 查找 Chrome 安装路径
   ├─ 关闭占用 9222 端口的进程
   ├─ 后台启动 Chrome（非阻塞）
   └─ 立即返回成功状态
   ↓
4. 【可选】等待 2-3 秒后运行 health.py 验证状态
   └─ 确认 Chrome 是否在 9222 端口正常运行
   ↓
5. 浏览器就绪，可以连接到 Chrome DevTools (http://127.0.0.1:9222)
```

### 命令示例

**1. 启动 Chrome（必需）：**

```bash
# 复用主profile（默认）
python scripts/launcher.py

# 或明确指定
python scripts/launcher.py --mode reuse

# 独立profile（无痕模式）
python scripts/launcher.py --mode independent
```

**2. 验证 Chrome 状态（可选但推荐）：**

```bash
# 在 launcher.py 启动后运行（等待 2-3 秒）
python scripts/health.py
```

**输出示例：**
```
Checking Chrome health on port 9222...
[OK] Chrome is healthy and responding on port 9222
```

## 使用场景示例

### 场景 1: 打开浏览器（默认复用cookie）

```
用户: "打开浏览器"

执行流程:
1. 检测到"打开浏览器"触发词（非无痕模式）
2. 选择复用cookie模式
3. 运行: python scripts/launcher.py --mode reuse
   - 检测系统（Windows/macOS/Linux）
   - 查找 Chrome 路径
   - 关闭现有 Chrome 窗口
   - 后台启动 Chrome
   - 立即返回
4. 【可选】等待 2-3 秒后运行: python scripts/health.py
   - 验证 Chrome 是否正常响应
5. 浏览器就绪（保持登录状态）
6. 智能体可连接 DevTools
```

### 场景 2: 启动无痕浏览器

```
用户: "启动无痕浏览器"

执行流程:
1. 检测到"无痕浏览器"触发词
2. 选择独立profile模式
3. 运行: python scripts/launcher.py --mode independent
   - 检测系统
   - 查找 Chrome 路径
   - 不关闭现有 Chrome 窗口
   - 后台启动 Chrome（使用独立profile）
   - 立即返回
4. 【可选】等待 2-3 秒后运行: python scripts/health.py
   - 验证 Chrome 是否正常响应
5. 浏览器就绪（干净的独立环境）
6. 智能体可连接 DevTools
```

## API 使用指南

### 使用 launcher.py 和 health.py

```python
import subprocess
import time

# 步骤 1: 启动 Chrome
# 复用主profile（默认）
subprocess.run(["python", "scripts/launcher.py"])

# 或独立profile模式
# subprocess.run(["python", "scripts/launcher.py", "--mode", "independent"])

# 步骤 2: 【推荐】等待 Chrome 启动完成
time.sleep(3)

# 步骤 3: 【可选】运行健康检查验证状态
result = subprocess.run(["python", "scripts/health.py"], capture_output=True, text=True)
print(result.stdout)
```

### 检测操作系统

```javascript
const isWindows = process.platform === 'win32';
const isMacOS = process.platform === 'darwin';
const isLinux = process.platform === 'linux';
```

### 判断启动模式

```javascript
function shouldUseIndependentMode(userInput) {
  const independentKeywords = ['无痕', '独立profile', '不复用', 'incognito'];
  return independentKeywords.some(keyword => 
    userInput.toLowerCase().includes(keyword.toLowerCase())
  );
}
```

### 连接到 Chrome DevTools

```javascript
await chrome-devtools_navigate_page({
  type: "url",
  url: "http://127.0.0.1:9222"
});
```

## 注意事项

1. **非阻塞启动**
   - `launcher.py` 使用 `subprocess.Popen` 后台启动 Chrome
   - 命令立即返回，不会卡住智能体
   - 启动成功后需等待 2-3 秒再连接 DevTools

2. **健康检查（health.py）**
   - `launcher.py` **不会自动运行** `health.py`
   - `health.py` 是一个独立的可选脚本，用于验证 Chrome 状态
   - 建议在 `launcher.py` 启动后手动运行 `health.py` 确认状态
   - 或者直接等待 2-3 秒后尝试连接 DevTools

3. **复用cookie模式的警告**
   - 会关闭所有现有Chrome窗口，请提醒用户保存工作
   - 复用主profile的登录状态和cookie

4. **独立模式的特点**
   - 不会关闭现有Chrome窗口
   - 使用全新的独立profile，无任何会话信息
   - 需要重新登录网站

5. **端口管理**
   - 脚本会自动处理9222端口冲突
   - 如有冲突会自动关闭占用进程

6. **安全提示**
   - 敏感信息应妥善处理，避免泄露
   - 某些网站可能使用 HttpOnly cookie

## 故障排查

1. 检查 Chrome 是否已正确启动：
   ```bash
   # Windows
   tasklist | findstr chrome
   
   # macOS/Linux
   ps aux | grep chrome
   ```

2. 检查端口占用：
   ```bash
   # Windows
   netstat -ano | findstr :9222
   
   # macOS/Linux
   lsof -i :9222
   ```

3. 手动验证 Chrome 调试端口：
   - 访问 http://127.0.0.1:9222/json/version
   - 应该返回 JSON 格式的浏览器信息

4. 常见解决方案：
   - 重启 Chrome 调试模式
   - 检查防火墙设置
   - 确保端口 9222 未被其他程序占用
