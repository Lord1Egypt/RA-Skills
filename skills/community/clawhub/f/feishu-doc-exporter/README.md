# Feishu Document Exporter 📄

批量导出飞书文档为 Markdown 格式的工具，支持导出单个文档或整个文件夹。

## 功能特点
- ✅ 批量导出整个文件夹的文档
- ✅ 支持递归导出子文件夹
- ✅ 保留原始文档的 Markdown 格式
- ✅ 自动处理文件名中的特殊字符
- ✅ 保留文件夹层级结构
- ✅ 增量导出支持（后续版本）
- ✅ PDF 导出支持（后续版本）

## 安装
```bash
clawhub install feishu-doc-exporter
```

## 使用方法

### 导出单个文档
```bash
feishu-doc-exporter export \
  --url "https://example.feishu.cn/docx/xxxxxxxxxxxxxxxxxxxx" \
  --format markdown \
  --output ./export
```

### 导出整个文件夹
```bash
feishu-doc-exporter export \
  --folder "folder_token_here" \
  --output ./export \
  --recursive
```

### 列出文件夹内容
先查看文件夹中有哪些文档，再选择性导出：
```bash
feishu-doc-exporter list \
  --folder "folder_token_here" \
  --recursive
```

## 参数说明
| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--url` | 单个文档的URL | - |
| `--folder` | 文件夹的token | - |
| `--format` | 导出格式，目前支持 `markdown` | `markdown` |
| `--output` | 输出目录路径 | `./export` |
| `--recursive` | 是否递归导出子文件夹 | false |

## 权限要求
使用前需要确保飞书应用有以下权限：
- `doc:document:read` - 读取文档内容
- `drive:folder:read` - 读取文件夹信息
- `drive:file:read` - 读取文件信息

## 使用场景
1. 批量备份飞书文档到本地
2. 文档迁移到其他平台
3. 生成静态网站内容
4. 文档离线查阅
5. 批量文档格式转换

## 注意事项
- PDF 导出功能将在后续版本中支持
- 大文档导出可能需要较长时间，请耐心等待
- 导出的图片会在后续版本中支持自动下载保存
- 建议先导出少量文档测试，确认格式符合预期后再批量导出

## 许可证
MIT
