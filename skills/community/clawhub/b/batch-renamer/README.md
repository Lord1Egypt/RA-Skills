# Batch Renamer - 批量文件重命名工具

一个简单但强大的批量文件重命名工具，支持多种命名模式、正则表达式、预览和撤销功能。

## 功能特性
- ✅ 多种命名模式：序号、日期、自定义前缀/后缀
- ✅ 正则表达式支持：灵活匹配和替换
- ✅ 预览功能：先预览，确认后再执行
- ✅ 撤销操作：支持撤销最近一次重命名
- ✅ 安全可靠：自动备份原始文件名

## 安装

### 方法一：作为脚本运行
```bash
git clone <repo-url>
cd batch-renamer
python3 batch_renamer.py --help
```

### 方法二：安装为命令行工具（计划中）
```bash
npm install -g batch-renamer
# 或
pip install batch-renamer
```

## 快速开始

### 1. 序号重命名
```bash
python3 batch_renamer.py rename ./photos --pattern "photo_{001}.jpg"
```

### 2. 日期重命名
```bash
python3 batch_renamer.py rename ./docs --pattern "doc_{YYYY-MM-DD}.md"
```

### 3. 正则表达式替换
```bash
python3 batch_renamer.py rename ./downloads --regex "s/^DSC_/photo_/"
```

### 4. 预览模式（不实际执行）
```bash
python3 batch_renamer.py rename ./photos --pattern "photo_{001}.jpg" --preview
```

### 5. 撤销操作
```bash
python3 batch_renamer.py undo ./photos
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
python3 batch_renamer.py rename ./files --regex "s/^old_/new_/"

# 删除空格
python3 batch_renamer.py rename ./files --regex "s/\s+/_/g"

# 提取数字
python3 batch_renamer.py rename ./files --regex "s/.*?(\d+).*/file_$1/"
```

## 安全措施
1. **预览模式**：默认先显示预览，需要确认后才执行
2. **自动备份**：执行重命名前自动保存映射关系
3. **撤销功能**：随时可以撤销最近一次操作
4. **dry-run 选项**：使用 --preview 查看效果

## 示例场景

### 场景 1：整理照片
```bash
# 将 DSC_0001.jpg 重命名为 2026-03-05_001.jpg
python3 batch_renamer.py rename ./photos --pattern "{YYYY-MM-DD}_{001}.jpg"
```

### 场景 2：整理下载文件
```bash
# 将 "下载 (1).pdf" 重命名为 document_001.pdf
python3 batch_renamer.py rename ./downloads --pattern "document_{001}.{ext}"
```

### 场景 3：批量替换
```bash
# 将所有文件名中的 "v1" 替换为 "v2"
python3 batch_renamer.py rename ./files --regex "s/v1/v2/g"
```

## 配置文件（计划中）
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

## 贡献
欢迎提交 Issue 和 Pull Request！

## 许可证
MIT License
