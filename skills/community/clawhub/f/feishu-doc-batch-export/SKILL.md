---
name: feishu-doc-batch-export
description: 批量导出飞书文档（docx）到本地Markdown格式，支持保留文档格式、图片、链接，支持指定文件夹/文档链接批量导出。触发场景：当用户需要导出飞书文档、批量下载飞书文档、飞书文档转Markdown时使用。
---
# 飞书文档批量导出技能

## 核心功能
1. 支持单个文档导出：输入飞书文档链接，直接导出为Markdown文件
2. 支持文件夹批量导出：输入飞书文件夹链接，导出文件夹下所有docx文档
3. 自动保留格式：标题、列表、表格、粗体、斜体、链接格式完全保留
4. 自动下载图片：文档内图片自动下载到本地assets目录，Markdown内路径自动替换
5. 错误重试：导出失败自动重试3次，支持导出日志输出

## 使用方法
### 基本命令
```bash
# 导出单个文档
python scripts/export.py --url <飞书文档链接> --output <本地输出目录>

# 导出文件夹下所有文档
python scripts/export.py --url <飞书文件夹链接> --output <本地输出目录> --recursive
```

### 参数说明
- `--url`: 飞书文档/文件夹的公开链接或有权限访问的链接
- `--output`: 本地导出目录，默认当前目录下的feishu_export文件夹
- `--recursive`: 是否递归导出子文件夹内容，默认false
- `--keep-html`: 是否同时保留原始HTML文件，默认false

## 依赖要求
提前配置飞书应用权限：
1. 飞书自建应用需要开通`docx:readonly`、`drive:readonly`权限
2. 环境变量配置`FEISHU_APP_ID`和`FEISHU_APP_SECRET`

## 注意事项
- 仅支持docx格式的飞书文档，不支持表格、思维笔记、幻灯片等其他格式
- 导出速度受飞书API限制，每分钟最多导出10个文档
- 大文档导出时间较长，请耐心等待
