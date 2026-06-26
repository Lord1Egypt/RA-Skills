---
name: baidu-scholar-helper
version: 1.1.0
author: 史婉媱
description: 一键搜索学术论文，自动下载PDF，智能总结核心工作与创新点。支持百度学术+arXiv，按引用量排序，科研必备工具。
tags:
  - 论文搜索
  - 学术研究
  - PDF下载
  - arXiv
  - 百度学术
  - 科研工具
  - Paper Search
  - Academic
highlights:
  - 🔍 一键搜索百度学术和arXiv
  - 📊 自动按引用量排序
  - 📥 PDF自动下载并分类保存
  - 🧠 AI智能提取核心工作和创新点
  - 🖼️ 自动识别并显示论文模型图
triggers:
  - 百度学术搜索
  - 百度学术查论文
  - 百度学术 {关键词}
  - 百度学术 {关键词} {年份}
  - arXiv搜索
  - arXiv {关键词}
  - 搜论文
  - 搜arxiv
when: 用户需要检索论文、下载PDF、总结工作创新点、按引用量排序时
how: |
  ⚠️ 重要：一次性完成所有操作，不要分步骤！
  
  百度学术模式：
  1. 解析关键词、年份
  2. 爬取百度学术，按引用量从高到低排序
  3. 解析标题、作者、来源、年份、引用量、PDF链接
  4. 进入详情页提取摘要，分析核心工作与创新点
  5. 显示模型图（如有）
  6. 自动下载PDF到 ~/Desktop/papers/<关键词>/ 文件夹
  7. 最后统一呈现完整报告（搜索结果+下载状态）
  
  arXiv模式：
  1. 使用arXiv官方API搜索
  2. 使用本地引用量数据库匹配（包含经典论文）
  3. 提供引用量手动查询链接（Google Scholar、Semantic Scholar）
  4. 按引用量排序（从高到低）
  5. 解析标题、作者、发布日期、分类、摘要
  6. 分析核心工作与创新点
  7. 自动下载PDF到 ~/Desktop/papers/<关键词>/ 文件夹
  8. 最后统一呈现完整报告（搜索结果+下载状态）
limits: 仅用于学术用途，不破解付费内容；arXiv API有速率限制；百度学术可能触发验证码；引用量数据来自本地数据库或需手动查询

# ============================================
# 安全声明 (Security Spec)
# ============================================
security:
  # 外部进程声明
  externalProcesses:
    - command: pdftotext
      purpose: 提取PDF文本内容，用于识别论文模型图位置
      safe: true
      reason: 系统工具，只读取本地PDF文件，不执行任何危险操作
    - command: pdfimages
      purpose: 从PDF中提取图片，用于识别模型架构图
      safe: true
      reason: 系统工具，只提取图片到临时目录，不执行任何危险操作
  
  # 文件操作声明
  fileOperations:
    read:
      - ~/Desktop/papers/  # 读取已下载的PDF
    write:
      - ~/Desktop/papers/  # 创建目录和保存PDF
    temp:
      - /tmp/  # 临时文件处理（模型图提取）
  
  # 网络访问声明
  networkAccess:
    - domain: xueshu.baidu.com
      purpose: 搜索学术论文
      dataType: 只读，获取搜索结果和论文元数据
    - domain: arxiv.org
      purpose: 搜索arXiv论文
      dataType: 只读，通过官方API获取论文信息
    - domain: *.pdf
      purpose: 下载论文PDF文件
      dataType: 二进制文件下载
  
  # 安全保证
  guarantees:
    - 不收集用户数据
    - 不上传任何信息到第三方服务器
    - 不执行任意代码
    - 不修改系统文件
    - 网络请求仅用于论文搜索和下载

# ============================================
# 依赖声明
# ============================================
dependencies:
  python:
    - requests>=2.28.0
    - beautifulsoup4>=4.11.0
    - Pillow>=9.0.0
  system:
    - poppler-utils  # 提供 pdfimages 和 pdftotext 工具，用于提取PDF中的模型图

# ============================================
# 权限声明
# ============================================
permissions:
  - network        # 访问百度学术和arXiv网络资源
  - file-write     # 创建目录和下载PDF文件到 ~/Desktop/papers/

# ============================================
# 安装规范 (Install Spec)
# ============================================
install:
  # Python依赖安装
  pip:
    - requests>=2.28.0
    - beautifulsoup4>=4.11.0
    - Pillow>=9.0.0
  
  # 系统依赖安装（根据操作系统选择）
  system:
    ubuntu:
      - sudo apt-get install -y poppler-utils
    debian:
      - sudo apt-get install -y poppler-utils
    macos:
      - brew install poppler
    fedora:
      - sudo dnf install -y poppler-utils
    centos:
      - sudo yum install -y poppler-utils
---

# 百度学术助手 (Baidu Scholar Helper) V1.0.0

一键搜索学术论文，自动下载PDF，智能总结核心工作与创新点。

## 功能清单

### 百度学术
- ✅ 关键词搜索 + 年份筛选
- ✅ **按引用量排序（高引用在前）**
- ✅ **每次显示5-10篇论文**
- ✅ 自动提取核心工作
- ✅ 自动提取创新点
- ✅ 显示模型图（如有）
- ✅ 显示论文链接
- ✅ 自动下载PDF

### arXiv
- ✅ 关键词搜索（官方API）
- ✅ 按相关度排序
- ✅ 自动提取核心工作
- ✅ 自动提取创新点
- ✅ 显示arXiv分类
- ✅ 显示论文链接
- ✅ 自动下载PDF

---

## 安装指南

### 1. 安装 Python 依赖

```bash
pip install requests beautifulsoup4 Pillow
```

### 2. 安装系统依赖（用于提取PDF模型图）

**Ubuntu/Debian:**
```bash
sudo apt-get install -y poppler-utils
```

**macOS:**
```bash
brew install poppler
```

**Fedora/CentOS:**
```bash
sudo dnf install -y poppler-utils
# 或
sudo yum install -y poppler-utils
```

### 3. 验证安装

```bash
# 检查 poppler-utils 是否安装成功
which pdftotext pdfimages
```

---

## PDF保存规则

### 保存位置
```
~/Desktop/papers/<论文方向>/
```

每次搜索会自动创建以关键词命名的文件夹，方便分类管理。

### 命名格式
```
标题_年份_J.pdf   # 期刊论文
标题_年份_C.pdf   # 会议论文
```

arXiv预印本也按此格式命名（根据分类自动判断J/C）。

---

## 使用方法

### 命令行
```bash
# 百度学术
python scripts/search.py baidu 大模型
python scripts/search.py baidu 人工智能 2024

# arXiv
python scripts/search.py arxiv transformer
python scripts/search.py arxiv "deep learning" 5
```

### 对话方式
```
用户：百度学术搜索 大模型
AI：运行脚本，返回论文列表 + 核心工作 + 创新点 + PDF下载

用户：arXiv GPT 5
AI：搜索arXiv并下载前5篇论文
```

---

## 输出示例

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📄 【1】引用量：⭐1523
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📌 标题：Attention Is All You Need
👥 作者：Vaswani A, Shazeer N, Parmar N
📚 来源：NeurIPS 2017
🔗 链接：https://...

🧠 【核心工作】
   本文提出了一种新的简单网络架构——Transformer，完全基于注意力机制，
   彻底摒弃了循环和卷积。

💡 【创新点】
   提出多头注意力机制，在机器翻译任务上取得了最优性能，同时训练速度大幅提升。

🖼️ 【模型图】
   https://...

⬇️  下载PDF...
✅ 已下载：Attention Is All You Need_2017_C.pdf
```

---

## 脚本说明

| 脚本 | 说明 |
|------|------|
| `main.py` | 百度学术搜索脚本 |
| `arxiv_search_v2.py` | arXiv API搜索脚本 |
| `search.py` | 统一入口脚本 |
| `extract_model_figure.py` | PDF模型图提取脚本 |

---

## 注意事项

1. **百度学术**可能触发验证码拦截
2. **arXiv API**有速率限制，脚本已内置重试机制
3. 下载的PDF请用于学术研究，尊重版权
4. 引用量数据来自百度学术，仅供参考
5. **模型图提取功能**需要安装 `poppler-utils`

---

## 系统要求

- Python 3.7+
- 网络连接（访问百度学术/arXiv）
- 磁盘空间（存储下载的PDF）
