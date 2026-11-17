# PowerShell 命令对照

SKILL.md 正文命令的 PowerShell 版本，按步骤一一对应。Windows 无 Git Bash 环境时使用。

> `openspec`、`npm`、`opencode` 等 CLI 本身跨平台一致，需要转换的只有 shell 内建语法：检测、循环、建目录、复制。

## Step 0 — 检查并安装 OpenSpec

```powershell
# 检测，未安装则全局安装
if (-not (Get-Command openspec -ErrorAction SilentlyContinue)) {
  npm install -g @fission-ai/openspec@latest
}

# 验证，预期输出 x.y.z 形式的版本号
openspec --version
```

注意：bash 的 `&>/dev/null` 在 PowerShell 中没有直接等价物，用 `Get-Command -ErrorAction SilentlyContinue` 做存在性检测。

## Step 0 — 获取原生支持的工具列表

```powershell
openspec init --help
```

## Step 0 — 交叉检查本机可用的 Agent CLI

```powershell
foreach ($tool in 'opencode','codebuddy','atomcode','zcode') {
  if (Get-Command $tool -ErrorAction SilentlyContinue) {
    Write-Output "$tool: ✅ 可用"
  } else {
    Write-Output "$tool: ❌ 未安装"
  }
}
```

## Step 1 — 初始化 OpenSpec

```powershell
cd C:\path\to\project
openspec init --tools opencode
```

## Step 3 — 原生工具：直接使用

```powershell
opencode run '/opsx:propose "your change idea"'
```

注意：参数务必用**单引号**包裹——PowerShell 双引号内 `$` 会触发变量展开，斜杠命令参数若含 `$` 会被改写。

## Step 4b — 用选定的桥接工具初始化

```powershell
openspec init --tools opencode
# 若用户选择 codebuddy：
# openspec init --tools codebuddy
```

## Step 4d — 为目标工具创建对应文件

```powershell
New-Item -ItemType Directory -Force .<target-tool>/skills, .<target-tool>/commands

# 示例：从 opencode 桥梁适配到 atomcode
Copy-Item .opencode/skills/opsx-*.md .atomcode/skills/
Copy-Item .opencode/commands/opsx-*.md .atomcode/commands/
```

`New-Item -Force` 等价于 bash 的 `mkdir -p`（目录已存在时不报错）。

## 验证

```powershell
ls openspec/config.yaml
ls .opencode/skills/
opencode run '/opsx:propose "verify SDD is working"'
```

`ls` 在 PowerShell 中是 `Get-ChildItem` 的别名，可直接使用。
