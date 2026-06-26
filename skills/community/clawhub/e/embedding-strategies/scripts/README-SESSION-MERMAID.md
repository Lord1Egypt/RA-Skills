# 方案 C：子任务自动 Mermaid 生成

## 📚 概述

创建子任务时自动生成 Mermaid 流程图，并发送到飞书。

## 📁 脚本文件

| 文件 | 说明 |
|------|------|
| `invoke-session-with-mermaid.ps1` | 主脚本（完整功能） |
| `test-session-mermaid.ps1` | 测试脚本 |
| `send-mermaid-to-feishu.ps1` | Mermaid 发送到飞书脚本 |

## 🚀 使用方法

### 方法 1：使用完整脚本

```powershell
# 切换到脚本目录
cd C:\Users\Xiabi\.openclaw\workspace\scripts

# 运行脚本
.\invoke-session-with-mermaid.ps1 -Task "分析数据" -Label "data-analysis"
```

**参数说明：**
- `-Task`：子任务描述（必填）
- `-Label`：子任务标签（可选，默认 "auto-mermaid"）

**执行流程：**
1. 创建子任务
2. 等待子任务完成
3. 检测回复中的 Mermaid 代码
4. 生成 PNG
5. Chrome 打开
6. 发送到飞书
7. 清理临时文件（可选）

---

### 方法 2：使用测试脚本

```powershell
# 运行测试脚本
.\test-session-mermaid.ps1
```

**测试内容：**
- 创建测试子任务
- 检测 Mermaid 代码
- 生成 PNG
- 发送到飞书

---

### 方法 3：手动调用

```powershell
# 1. 创建子任务
$result = sessions_spawn -Task "分析数据"

# 2. 等待完成
while ($result.Status -ne 'Completed') {
    Start-Sleep -Seconds 2
    $result = Get-SessionResult -SessionId $result.SessionId
}

# 3. 获取回复
$response = $result.Response

# 4. 检测 Mermaid 代码
if ($response -match '```mermaid\s*([\s\S]*?)```') {
    $mermaidCode = $matches[1].Trim()
    
    # 5. 生成 PNG
    $tempDir = Join-Path $env:TEMP "mermaid-$(Get-Date -Format 'yyyyMMdd-HHmmss')"
    New-Item -ItemType Directory -Path $tempDir | Out-Null
    
    $mmdFile = Join-Path $tempDir "diagram.mmd"
    $pngFile = Join-Path $tempDir "diagram.png"
    
    $mermaidCode | Out-File -FilePath $mmdFile -Encoding UTF8
    mmdc -i $mmdFile -o $pngFile -w 1000 -H 800
    
    # 6. Chrome 打开
    Start-Process "chrome" -ArgumentList $pngFile
    
    # 7. 发送到飞书
    message --action send --channel feishu --filePath $pngFile
}
```

---

## 📊 功能特性

### ✅ 自动检测 Mermaid 代码

- 检测回复中的 ```mermaid 代码块
- 提取并生成 PNG

### ✅ 自动生成执行流程图

- 如果回复中没有 Mermaid 代码
- 自动生成执行流程图
- 展示任务执行步骤

### ✅ Chrome 自动打开

- 生成 PNG 后立即用 Chrome 打开
- 方便预览和检查

### ✅ 飞书自动发送

- 自动发送到飞书
- 文字 + 图片一起发送
- 方便事后搜索

---

## 🔧 配置

### 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `TEMP` | 临时文件目录 | 系统临时目录 |

### mmdc 配置

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `-w` | PNG 宽度 | 1000 |
| `-H` | PNG 高度 | 800 |

---

## 📝 示例

### 示例 1：包含 Mermaid 代码的任务

```powershell
.\invoke-session-with-mermaid.ps1 -Task "生成 Mermaid 流程图，展示 OpenClaw 架构"
```

**预期结果：**
- ✅ 检测到 Mermaid 代码
- ✅ 提取并生成 PNG
- ✅ Chrome 打开
- ✅ 发送到飞书

---

### 示例 2：不包含 Mermaid 代码的任务

```powershell
.\invoke-session-with-mermaid.ps1 -Task "分析数据并生成报告"
```

**预期结果：**
- ⚠️ 未检测到 Mermaid 代码
- ✅ 自动生成执行流程图
- ✅ 生成 PNG
- ✅ Chrome 打开
- ✅ 发送到飞书

---

## ⚠️ 注意事项

### 1. 依赖项

- ✅ PowerShell 5.1+
- ✅ Node.js（mmdc 命令）
- ✅ Mermaid CLI（@mermaid-js/mermaid-cli）
- ✅ Chrome 浏览器
- ✅ OpenClaw sessions_spawn 命令

### 2. 权限

- ✅ 需要执行 PowerShell 脚本权限
- ✅ 需要访问临时目录权限
- ✅ 需要启动 Chrome 权限

### 3. 性能

- ⏱️ 子任务执行时间：取决于任务复杂度
- ⏱️ Mermaid 生成时间：约 2-5 秒
- ⏱️ Chrome 打开时间：约 1-2 秒
- ⏱️ 飞书发送时间：约 1-2 秒

**总延迟：约 5-10 秒**

---

## 🐛 故障排查

### 问题 1：sessions_spawn 命令不存在

**解决：**
```powershell
# 检查 OpenClaw 是否安装
openclaw --version

# 检查 sessions_spawn 是否可用
Get-Command sessions_spawn
```

### 问题 2：mmdc 命令不存在

**解决：**
```powershell
# 安装 Mermaid CLI
npm install -g @mermaid-js/mermaid-cli
```

### 问题 3：Chrome 无法打开

**解决：**
```powershell
# 检查 Chrome 是否安装
Get-Process chrome -ErrorAction SilentlyContinue

# 或者手动指定 Chrome 路径
Start-Process "C:\Program Files\Google\Chrome\Application\chrome.exe" -ArgumentList $pngFile
```

### 问题 4：飞书发送失败

**解决：**
```powershell
# 检查飞书是否登录
# 检查 message 命令是否可用
message --help
```

---

## 📞 支持

如有问题，请联系：
- 📧 飞书：@阿香
- 🐛 GitHub Issue: https://github.com/openclaw/openclaw/issues

---

## 🎯 下一步

**长期目标：**
1. ✅ 集成到 OpenClaw 核心
2. ✅ 添加配置选项
3. ✅ 支持更多图表类型
4. ✅ 支持批量生成

**当前方案：**
- ✅ 方案 C-1：PowerShell 包装脚本（已实施）
- ⏳ 方案 C-2：修改 sessions_spawn 函数（不推荐）
- ⏳ 方案 C-3：创建 OpenClaw 插件（可选）

---

**方案 C 实施完成！** 🦞✨
