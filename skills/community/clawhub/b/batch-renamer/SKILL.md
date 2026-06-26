---
name: batch-renamer
description: 【爆款标题】批量重命名神器：10秒整理1000个文件，再也不用手动改名字！

你是不是经常要处理一堆杂乱的文件？照片一堆 DSC_XXX，下载文件各种乱码，手动改名到崩溃...

本工具用 10+ 种命名模式（序号、日期、正则表达式）帮你秒级完成批量重命名，支持实时预览和零风险撤销。

✨ **核心亮点**：
- 10+ 命名模式：序号、日期、时间戳、自定义模板
- 正则表达式支持：高级用户神器，灵活匹配
- 实时预览：改名前先看效果，错了随时撤销
- 批量处理：一次上千文件，秒级完成
- 零风险：自动备份，操作可撤销

📁 **典型场景**：
- 整理照片（消除 DSC 编号混乱）
- 归档下载（统一命名规则）
- 批量文档（添加日期前缀）

🎯 **为什么选我**：
✅ 预览+撤销 = 零风险
✅ 正则表达式 = 解决复杂需求
✅ 纯Python = 跨平台，无需浏览器

👉 立即体验：`clawhub install batch-renamer`
---

# Batch Renamer - 批量文件重命名工具

## 功能特性
- ✅ 多种命名模式：序号、日期、自定义前缀/后缀
- ✅ 正则表达式支持：灵活匹配和替换
- ✅ 预览功能：先预览，确认后再执行
- ✅ 撤销操作：支持撤销最近一次重命名
- ✅ 安全可靠：自动备份原始文件名

## 安装
```bash
npm install -g batch-renamer
```

## 快速开始

### 1. 序号重命名
```bash
batch-renamer rename ./photos --pattern "photo_{001}.jpg"
```

### 2. 日期重命名
```bash
batch-renamer rename ./docs --pattern "doc_{YYYY-MM-DD}.md"
```

### 3. 正则表达式替换
```bash
batch-renamer rename ./downloads --regex "s/^DSC_/photo_/"
```

### 4. 预览模式（不实际执行）
```bash
batch-renamer rename ./photos --pattern "photo_{001}.jpg" --preview
```

### 5. 撤销操作
```bash
batch-renamer undo ./photos
```

## 详细使用说明

### 命名模式变量
- `{001}` - 三位序号（自动补零）
- `{01}` - 两位序号
- `{1}` - 一位序号
- `{YYYY}` - 四位年份
- `{MM}` - 两位月份
- `{DD}` - 两位日期
- `{HH}` - 两位小时
- `{mm}` - 两位分钟
- `{original}` - 原始文件名（不含扩展名）
- `{ext}` - 原始扩展名

### 正则表达式语法
使用 JavaScript 正则表达式语法：
```bash
# 替换前缀
batch-renamer rename ./files --regex "s/^old_/new_/"

# 删除空格
batch-renamer rename ./files --regex "s/\s+/_/g"

# 提取数字
batch-renamer rename ./files --regex "s/.*?(\d+).*/file_$1/"
```

## 安全措施
1. **预览模式**：默认先显示预览，需要确认后才执行
2. **自动备份**：执行重命名前自动保存映射关系
3. **撤销功能**：随时可以撤销最近一次操作
4. **dry-run 选项**：使用 --preview 或 --dry-run 查看效果

## 示例场景

### 场景 1：整理照片
```bash
# 将 DSC_0001.jpg 重命名为 2026-03-05_001.jpg
batch-renamer rename ./photos --pattern "{YYYY-MM-DD}_{001}.jpg"
```

### 场景 2：整理下载文件
```bash
# 将 "下载 (1).pdf" 重命名为 document_001.pdf
batch-renamer rename ./downloads --pattern "document_{001}.{ext}"
```

### 场景 3：批量替换
```bash
# 将所有文件名中的 "v1" 替换为 "v2"
batch-renamer rename ./files --regex "s/v1/v2/g"
```

## 配置文件
可以在项目根目录创建 `.batch-renamer.json` 配置默认选项：
```json
{
  "preview": true,
  "backup": true,
  "pattern": "{001}.{ext}"
}
```

## 故障排除
- **撤销失败**：确保在同一目录下执行，且备份文件未被删除
- **正则表达式错误**：检查语法，可使用 --preview 先测试
- **权限问题**：确保有文件读写权限

## 更新日志
### v0.1.0 (2026-03-05)
- 初始版本发布
- 支持基础重命名功能
- 支持预览和撤销
