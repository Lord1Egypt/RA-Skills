# 中文编码处理工具集

PowerShell 中文文件编码处理工具，解决中文乱码问题。

## 📦 组件清单

| 脚本 | 功能 | 说明 |
|------|------|------|
| `encoding-detector.ps1` | 编码检测 | 自动检测文件编码（UTF-8/UTF-8-BOM/GBK/GB2312/UTF-16） |
| `safe-read.ps1` | 安全读取 | 自动识别编码并读取中文文件 |
| `safe-write.ps1` | 安全写入 | 以 UTF-8-BOM 格式写入中文文件 |
| `terminal-fix.ps1` | 终端修复 | 配置 PowerShell 终端 UTF-8 显示 |

## 🚀 快速开始

### 1. 修复终端显示（首先执行）

```powershell
cd C:\OpenClaw-Instances\gateway-instance-4\workspace\skills\chinese-encoding-handler\scripts

# 配置 UTF-8 终端
.\terminal-fix.ps1

# 永久保存设置（可选）
.\terminal-fix.ps1 -Permanent

# 检查当前设置
.\terminal-fix.ps1 -Check

# 恢复原始设置
.\terminal-fix.ps1 -Reset
```

### 2. 检测文件编码

```powershell
# 检测单个文件
.\encoding-detector.ps1 -Path "C:\path\to\file.txt"

# 输出 JSON 格式
.\encoding-detector.ps1 -Path "C:\path\to\file.txt" | ConvertFrom-Json

# 运行自检
.\encoding-detector.ps1 -Test
```

### 3. 读取中文文件

```powershell
# 自动检测编码读取
$content = .\safe-read.ps1 -Path "C:\path\to\file.txt"
Write-Host $content

# 指定编码读取
$content = .\safe-read.ps1 -Path "C:\path\to\file.txt" -Encoding "UTF-8"

# 支持管道
Get-ChildItem "C:\path\*.txt" | ForEach-Object { .\safe-read.ps1 -Path $_.FullName }

# 运行自检
.\safe-read.ps1 -Test
```

### 4. 写入中文文件

```powershell
# 默认 UTF-8-BOM 写入
.\safe-write.ps1 -Path "C:\path\to\file.txt" -Content "中文内容"

# 管道方式写入
"中文内容" | .\safe-write.ps1 -Path "C:\path\to\file.txt"

# 追加模式
.\safe-write.ps1 -Path "C:\path\to\file.txt" -Content "追加内容" -Append

# 指定编码
.\safe-write.ps1 -Path "C:\path\to\file.txt" -Content "内容" -Encoding "GBK"

# 跳过验证（提高性能）
.\safe-write.ps1 -Path "C:\path\to\file.txt" -Content "内容" -NoVerify

# 运行自检
.\safe-write.ps1 -Test
```

## 📋 详细参数说明

### encoding-detector.ps1

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `-Path` | string | ✓ | 要检测的文件路径 |
| `-Test` | switch | ✗ | 运行自检测试 |

**输出格式：**
```json
{
  "Encoding": "UTF-8-BOM",
  "Confidence": 100,
  "Message": "检测到 UTF-8 BOM 标记"
}
```

### safe-read.ps1

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `-Path` | string | ✓ | 要读取的文件路径 |
| `-Encoding` | string | ✗ | 指定编码（Auto/UTF-8-BOM/UTF-8/GBK/GB2312/UTF-16） |
| `-Test` | switch | ✗ | 运行自检测试 |

**默认行为：** 自动检测编码，按 UTF-8-BOM → UTF-8 → GBK → GB2312 顺序尝试

### safe-write.ps1

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `-Path` | string | ✓ | 要写入的文件路径 |
| `-Content` | string | ✓ | 要写入的内容 |
| `-Encoding` | string | ✗ | 编码格式（默认 UTF-8-BOM） |
| `-Append` | switch | ✗ | 追加模式 |
| `-NoVerify` | switch | ✗ | 跳过写入验证 |
| `-Test` | switch | ✗ | 运行自检测试 |

**特性：**
- 自动创建不存在的父目录
- 写入后自动验证可读性
- 默认使用 UTF-8-BOM（Windows 兼容性最好）

### terminal-fix.ps1

| 参数 | 类型 | 说明 |
|------|------|------|
| `-Reset` | switch | 恢复原始设置 |
| `-Check` | switch | 仅检查当前设置 |
| `-Permanent` | switch | 永久保存到配置文件 |
| `-Test` | switch | 运行自检测试 |

**配置内容：**
- 设置 `chcp 65001`（UTF-8 代码页）
- 设置 `[Console]::OutputEncoding = UTF8`
- 检查字体中文支持情况

## 🔧 使用场景

### 场景 1：批量转换文件为 UTF-8-BOM

```powershell
$files = Get-ChildItem "C:\docs\*.txt"
foreach ($file in $files) {
    $content = .\safe-read.ps1 -Path $file.FullName
    .\safe-write.ps1 -Path $file.FullName -Content $content
    Write-Host "已转换：$($file.Name)"
}
```

### 场景 2：读取并处理中文日志

```powershell
$logContent = .\safe-read.ps1 -Path "C:\logs\应用日志.txt"
$errors = $logContent | Select-String "错误"
foreach ($error in $errors) {
    Write-Host $error.Line
}
```

### 场景 3：创建中文配置文件

```powershell
$config = @"
{
  "名称": "配置文件",
  "版本": "1.0",
  "作者": "开发团队",
  "描述": "这是一个中文配置文件示例"
}
"@

.\safe-write.ps1 -Path "C:\config\设置.json" -Content $config
```

### 场景 4：CI/CD 自动化配置

```powershell
# 在构建脚本开头添加
& "C:\scripts\terminal-fix.ps1" -Permanent

# 确保所有输出文件使用 UTF-8-BOM
.\safe-write.ps1 -Path "build\output.txt" -Content $buildResult
```

## ⚠️ 注意事项

1. **脚本文件本身使用 UTF-8-BOM 编码保存**，确保中文注释正常显示
2. **首次使用建议先运行 `terminal-fix.ps1`**，确保终端能正确显示中文
3. **Windows 记事本兼容性**：使用 UTF-8-BOM 格式可确保记事本正确识别
4. **Git 版本控制**：建议在 `.gitattributes` 中设置 `*.ps1 working-tree-encoding=UTF-8`
5. **永久设置**：使用 `-Permanent` 参数会将配置写入 `$PROFILE.CurrentUserCurrentHost`

## 🧪 测试

每个脚本都包含 `-Test` 参数进行自检：

```powershell
.\encoding-detector.ps1 -Test
.\safe-read.ps1 -Test
.\safe-write.ps1 -Test
.\terminal-fix.ps1 -Test
```

测试内容包括：
- 编码检测准确性
- 文件读写正确性
- 目录自动创建
- 追加模式功能
- 错误处理机制

## 📝 编码标准

- 所有字符串使用双引号
- 路径使用 `Join-Path` 处理
- 包含完整的中文注释
- 包含参数说明和使用示例
- 包含错误处理和验证

## 🆘 故障排除

### 问题 1：中文仍然显示乱码

**解决：**
```powershell
# 1. 运行终端修复
.\terminal-fix.ps1

# 2. 检查字体设置
# 右键终端 → 属性 → 字体 → 选择 "Consolas" 或 "Lucida Console"

# 3. 验证设置
.\terminal-fix.ps1 -Check
```

### 问题 2：读取文件时报错

**解决：**
```powershell
# 1. 检查文件是否存在
Test-Path "文件路径"

# 2. 检测文件编码
.\encoding-detector.ps1 -Path "文件路径"

# 3. 尝试指定编码读取
.\safe-read.ps1 -Path "文件路径" -Encoding "GBK"
```

### 问题 3：写入后其他程序无法识别

**解决：**
```powershell
# 确保使用 UTF-8-BOM（兼容性最好）
.\safe-write.ps1 -Path "文件路径" -Content $content -Encoding "UTF-8-BOM"

# 不要使用 -NoVerify 参数，确保写入可验证
```

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交问题和改进建议。

---

**最后更新：** 2026-03-30  
**维护者：** OpenClaw Gateway
