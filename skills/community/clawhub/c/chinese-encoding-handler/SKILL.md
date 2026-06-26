# Chinese-Encoding-Handler

## 描述

中文编码处理工具包，解决 PowerShell 环境下中文文件读写乱码问题。提供自动编码检测、安全文件读写和终端显示修复功能。

## 触发场景

- 读取中文文件时出现乱码
- 写入中文内容后无法正常显示
- PowerShell 终端中文显示异常
- 需要自动检测文件编码
- 处理包含中文的配置文件或数据文件

## 使用方法

### 检测文件编码

```powershell
.\scripts\encoding-detector.ps1 -Path "C:\path\to\file.txt"
```

**输出示例**：
```
文件路径：C:\path\to\file.txt
检测编码：UTF-8-BOM
置信度：100%
```

### 安全读取中文文件

```powershell
.\scripts\safe-read.ps1 -Path "C:\path\to\file.txt"
```

**带编码参数读取**：
```powershell
.\scripts\safe-read.ps1 -Path "C:\path\to\file.txt" -Encoding "UTF-8"
```

### 安全写入中文文件

```powershell
.\scripts\safe-write.ps1 -Path "C:\path\to\file.txt" -Content "中文内容"
```

**指定编码写入**：
```powershell
.\scripts\safe-write.ps1 -Path "C:\path\to\file.txt" -Content "中文内容" -Encoding "UTF-8-BOM"
```

### 修复终端显示

```powershell
.\scripts\terminal-fix.ps1
```

**永久修复（需要管理员权限）**：
```powershell
.\scripts\terminal-fix.ps1 -Permanent
```

## 技术细节

### 编码检测原理

1. **BOM 检测**：优先检查文件开头的字节顺序标记（BOM）
   - UTF-8-BOM: `EF BB BF`
   - UTF-16-LE: `FF FE`
   - UTF-16-BE: `FE FF`

2. **内容分析**：无 BOM 时，通过字节分布和常见中文字符编码特征判断
   - GBK/GB2312：双字节字符特征
   - UTF-8：多字节序列特征

3. **置信度评分**：根据匹配程度给出 0-100% 置信度

### UTF-8-BOM 优势

- ✅ **兼容性好**：Windows 程序（记事本、Excel）识别准确
- ✅ **跨平台**：Linux/macOS 正常读取
- ✅ **无乱码风险**：明确标识编码格式
- ⚠️ **注意**：某些 Unix 工具可能不兼容 BOM

### 兼容性说明

| 系统 | 支持程度 | 备注 |
|------|---------|------|
| Windows PowerShell 5.1 | ✅ 完全支持 | 推荐 UTF-8-BOM |
| Windows PowerShell 7+ | ✅ 完全支持 | 默认 UTF-8 |
| Linux/macOS | ✅ 支持 | 建议无 BOM UTF-8 |
| CI/CD 环境 | ✅ 支持 | 需确保终端 UTF-8 |

## 故障排除

### 常见问题 Q&A

**Q1: 为什么读取文件还是乱码？**
- 检查文件编码是否被正确识别
- 尝试手动指定 `-Encoding` 参数
- 使用 `encoding-detector.ps1` 重新检测

**Q2: 写入的文件在记事本打开乱码？**
- 使用 `-Encoding "UTF-8-BOM"` 参数
- 避免使用纯 UTF-8（无 BOM）

**Q3: PowerShell 终端显示中文为方框？**
- 运行 `terminal-fix.ps1`
- 检查终端字体是否支持中文
- 使用 `-Permanent` 参数永久修复

**Q4: 批量处理文件时部分失败？**
- 检查文件权限
- 确认文件未被其他程序占用
- 查看错误日志定位具体文件

### 错误代码说明

| 错误码 | 含义 | 解决方案 |
|--------|------|---------|
| ERR-001 | 文件不存在 | 检查路径是否正确 |
| ERR-002 | 权限不足 | 以管理员身份运行 |
| ERR-003 | 编码检测失败 | 手动指定编码参数 |
| ERR-004 | 文件被占用 | 关闭占用程序后重试 |
| ERR-005 | 终端设置失败 | 检查注册表权限 |

## 相关资源

- [PowerShell 编码官方文档](https://learn.microsoft.com/powershell/module/microsoft.powershell.core/about/about_character_encoding)
- [UTF-8 BOM 规范](https://www.unicode.org/faq/utf_bom.html)
- [GitHub 仓库](https://github.com/openclaw/chinese-encoding-handler)
