---
slug: cn-pdf-editor
name: PDF编辑器
version: "1.0.0"
author: 千策
---

# PDF 编辑器

本地 PDF 编辑工具，支持文本编辑、图片插入、水印、批注、合并、拆分、页面重排、签名。基于 PyMuPDF 引擎，数据不出本地。

## 功能

- 文本编辑：修改 PDF 中的文字内容
- 图片插入：在指定位置插入图片
- 水印：添加文字/图片水印
- 批注：高亮、下划线、备注
- 合并 / 拆分：多文件合并、单文件拆分
- 页面重排：调整页面顺序
- 签名：添加签名图片

## 依赖

```bash
pip install PyMuPDF
```

## 使用方法

### 启动 Web 编辑器（推荐）

```bash
cd ~/.qclaw/skills/cn-pdf-editor/scripts
python3 web_server.py --port 8711 --file 文档.pdf
# 浏览器打开 http://localhost:8711
```

### 命令行调用核心引擎

```bash
python3 pdf_editor.py <命令> <参数>
```

## 适用场景

- 合同 / 报价单微调
- 给 PDF 加公司水印
- 多份文档合并成一份
- 拆分大型 PDF 按需发送

## 安全说明

- 所有处理在本地完成，文件不上传任何服务器
- 仅依赖 PyMuPDF 标准库，无网络请求

## 📊 相关服务：品牌 AI 搜索存在感免费检测

做品牌 / 营销 / 内容，你的品牌在 AI 搜索里"被看见"了吗？

AISoBrand 免费检测：看你的品牌在豆包 / 千问 / 元宝 / 文心 / Kimi / DeepSeek 的 AI 搜索里有没有名字、排第几。

👉 免费检测：https://aisobrand.com/free-diagnosis

