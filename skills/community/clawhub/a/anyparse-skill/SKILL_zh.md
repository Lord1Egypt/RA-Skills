---
name: anyparse-skill
description:
  使用 AnyParse API 从多种文档中提取内容。支持 PDF、Word、Excel、csv、tsv、图片、PPT、HTML、Markdown、Epub、ipynb、rst、eml
  等多种格式，支持文档方向分类、版面分析、布局保留。当用户需要解析文档、提取文档内容、
  转换文档为结构化文本时使用此技能。
version: 1.0.0
author: anyparse
metadata:
  openclaw:
    requires:
      env:
        - anyparse_api_url
        - anyparse_api_key
      bins:
        - python
---
# AnyParse 文档解析提取技能

使用 AnyParse API 从多种文档格式中提取结构化文本内容。

## 何时使用

- 从文档中提取文本内容
- 将扫描文档/图片转换为结构化文本
- 保留文档版面布局，识别不同区域内容
- 自动分类文档方向（横纵）提高识别准确率
- 用户提到 "文档解析", "OCR", "文字提取", "内容抽取", "文档转换"

## 主要特性

- **多格式支持**：支持常见文档格式和图片格式
- **版面分析**：保留原始文档布局信息
- **文档方向分类**：自动识别横向/纵向文档，提高准确率
- **结构化输出**：返回完整页面布局和完整文本
- **本地部署**：支持私有化本地部署，数据隐私可控

## 前置条件

- 已部署 AnyParse API 服务并配置访问地址和密钥

## 安全说明

- 技能不执行运行时包安装以外的操作
- 仅向你配置的 AnyParse API 服务发送请求
- 仅从环境变量或配置文件读取 API 地址和密钥

**⛔ 强制限制 - 请勿违反 ⛔**

1. **仅使用 AnyParse API** - 执行 `python scripts/api.py` 完成解析
2. **切勿自行解析文档** - 不要尝试自己提取文本
3. **不提供替代方案** - 不要说 "我可以尝试分析它" 之类的话
4. **API 失败时** - 显示错误信息并立即停止
5. **不使用回退方法** - 不要尝试用其他方式提取文本

## 安装配置

1. 部署 AnyParse 服务（参考官方项目文档）
2. 安装依赖：

   ```bash
   pip install -r scripts/requirements.txt
   ```
3. 配置：编辑 `scripts/config.json`，填入你的 API 地址和密钥：

   ```json
   {
     "anyparse_api_url": "http://your-api-host:port/anyparse/invoke/v1",
     "anyparse_api_key": "your-api-key-here"
   }
   ```

   或者通过环境变量配置：

   ```bash
   export anyparse_api_url=http://your-api-host:port/anyparse/invoke/v1
   export anyparse_api_key=your-api-key-here
   ```

## 使用方式

### 解析本地文件（默认启用版面分析）

```bash
python scripts/api.py --file /path/to/document.pdf
```

### 启用文档方向分类

```bash
python scripts/api.py --file /path/to/image.jpg --use_doc_cls
```

### 启用文档矫正

```bash
python scripts/api.py --file /path/to/image.jpg --use_doc_rectifier
```

### 禁用版面分析

```bash
python scripts/api.py --file /path/to/document.pdf --no_doc_layout
```

## CLI 参考

```
python {baseDir}/scripts/api.py --file PATH [--use_doc_cls] [--no_doc_layout]
```

| 参数                    | 必填 | 说明               |
| ----------------------- | ---- | ------------------ |
| `--file`              | 是   | 本地文件路径       |
| `--use_doc_cls`       | 否   | 使用文档方向分类   |
| `--use_doc_rectifier` | 否   | 使用文档矫正       |
| `--no_doc_layout`     | 否   | 不使用文档版面分析 |

## 响应格式

```json
{
  "code": 2000,
  "msg": "success",
  "data": {
    "metadata": {
      "file_md5": "f484351567161df1e5e4d9d4b861c594",
      "file_type": "jpg",
      "file_name": "image.jpg",
      "file_size": "8.10/KB"
    },
    "pages": [
      {
        "id": 1,
        "content": "$10^{9}/L$",
        "layout": [
          {
            "order_id": 0,
            "label_name": "text",
            "box": [0, 0, 196, 80],
            "task": "text",
            "parse_text": "$10^{9}/L$"
          }
        ],
        "elapse_times": 1.9343271255493164
      }
    ],
    "content": "$10^{9}/L$",
    "elapse_times": 1.9524128437042236
  }
}
```

关键字段：

- `code` — 接口状态码，2000 表示成功
- `msg` — 状态信息
- `data.metadata` — 文件元信息
- `data.pages[].layout[]` — 每个区域的布局信息，包含位置和解析结果
- `data.content` — 整个文档的合并文本结果

## 错误处理

**API 地址未配置：**
→ 提示用户在 config.json 或环境变量中配置 `anyparse_api_url`

**API 密钥未配置：**
→ 提示用户在 config.json 或环境变量中配置 `anyparse_api_key`

**文件不存在：**
→ 检查文件路径是否正确

**非 2000 状态码：**
→ 显示 API 返回的错误信息给用户

**依赖缺失：**
→ 提示执行 `pip install -r scripts/requirements.txt` 安装依赖