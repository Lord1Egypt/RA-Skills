# 文件管理大师

强大的文件批量处理工具，让文件管理变得简单高效。

## 功能特性

### 批量重命名
- 智能编号重命名（001, 002, ...）
- 正则表达式替换
- 添加前缀后缀
- 日期时间变量

### 智能整理
- 按文件类型分类
- 按日期整理
- 按大小分组
- 自动创建文件夹

### 高级搜索
- 文件内容搜索
- 元数据搜索
- 重复文件查找
- 快速文件定位

### 快速操作
- 批量复制移动
- 格式转换
- 文件压缩
- 自动备份

## 快速开始

### 安装
```bash
# 运行安装脚本
python install.py install
```

### 基本使用
```bash
# 批量重命名
file-master rename "~/photos" --pattern "vacation_{num:03d}.jpg"

# 按类型整理
file-master organize "~/Downloads" --recursive

# 搜索文件
file-master search "~/projects" --content "TODO:"

# 查找重复文件
file-master find-duplicates "~/backup"
```

## 详细文档

### 重命名模式
支持以下变量：
- `{num}` 或 `{num:03d}`: 序号（001, 002, ...）
- `{date:YYYYMMDD}`: 文件修改日期
- `{date:YYYY-MM-DD}`: 带分隔符的日期

示例：
```bash
# 添加前缀
file-master rename "." --prefix "backup_"

# 使用正则表达式
file-master rename "." --regex "^(.*)\.old$" --replace "$1.new"

# 按日期重命名
file-master rename "~/photos" --pattern "{date:YYYYMMDD}_{num:03d}.jpg"
```

### 整理选项
```bash
# 按类型整理（默认）
file-master organize "~/Downloads"

# 递归整理子文件夹
file-master organize "~/Downloads" --recursive

# 按日期整理
file-master organize "~/photos" --by date --format "YYYY/MM"

# 按大小整理
file-master organize "~/files" --by size --groups "small:<1MB,medium:1MB-10MB,large:>10MB"
```

## 配置说明

配置文件位置：`~/.file-master/config.yaml`

主要配置项：
- `confirm_deletion`: 删除前确认（默认：true）
- `backup_before_rename`: 重命名前备份（默认：true）
- `log_level`: 日志级别（debug/info/warning/error）
- `default_paths`: 默认路径配置
- `rules`: 自动化规则
- `file_types`: 文件类型分类
- `exclude`: 排除列表

## 安全特性

- 重要操作前确认
- 自动备份机制
- 完整操作日志
- 操作撤销功能
- 权限检查保护

## 系统要求

- **操作系统**: Windows 10+, macOS 10.15+, Linux
- **Python**: 3.8 或更高版本
- **内存**: 512MB RAM（推荐2GB）
- **磁盘空间**: 50MB

## 技术支持

- 文档：运行 `file-master --help`
- 社区：https://github.com/file-master-pro/community
- 问题反馈：https://github.com/file-master-pro/issues
- 邮箱支持：support@file-master.pro

## 许可证

MIT License - 详见 LICENSE 文件

## 更新日志

### v1.0.0 (2026-04-01)
- 首次发布
- 批量重命名功能
- 智能文件整理
- 高级搜索功能
- 重复文件查找

---

**让文件管理变得简单高效！**