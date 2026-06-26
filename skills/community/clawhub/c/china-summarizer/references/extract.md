# 内容提取技术说明

## 网页正文提取

### 各平台测试状态

```
✅ 稳定可用（静态HTML）：
  微信公众号   mp.weixin.qq.com
  知乎专栏     zhuanlan.zhihu.com
  博客园       cnblogs.com
  CSDN         blog.csdn.net
  简书         jianshu.com
  少数派       sspai.com
  36氪         36kr.com
  虎嗅         huxiu.com
  澎湃新闻     thepaper.cn
  新华网       xinhuanet.com
  人民网       people.com.cn

⚠️ 可能失败（JS渲染）：
  今日头条     toutiao.com
  微博         weibo.com
  部分知乎回答 zhihu.com/question/...
```

### 微信公众号正文提取

```
公众号文章正文位于：<div id="js_content">
文章标题位于：<h1 class="rich_media_title">
作者/来源位于：<span class="rich_media_meta">

提取优先级：
1. 先找 id="js_content" 的 div
2. 提取其中所有 <p> 标签内的文本
3. 过滤空段落
```

### 通用正文提取规则

```
HTML 清洗顺序：
1. 删除 <script>...</script> 全部内容
2. 删除 <style>...</style> 全部内容
3. 删除 <nav>、<header>、<footer>、<aside> 区块
4. 删除 HTML 注释 <!-- -->
5. 删除所有剩余 HTML 标签（保留文字）
6. 合并连续空白行
7. 去除行首行尾空格
```

---

## PDF 文件处理

### 工具选择建议

```
优先推荐：pdftotext（poppler）
  - 对中文PDF支持最好
  - 保留段落结构
  - 速度最快
  安装：
    macOS:  brew install poppler
    Ubuntu: sudo apt install poppler-utils

备选：pypdf（Python）
  - 无需系统工具，纯Python
  - 对复杂排版PDF可能有缺失
  安装：pip install pypdf

备选：pdfminer.six（Python）
  - 对复杂PDF提取更完整
  - 速度较慢
  安装：pip install pdfminer.six
```

### 判断是否为扫描版PDF

```
扫描版（图片型）PDF 特征：
- pdftotext 输出为空或只有少量乱码
- 文件很大但提取文字很少

处理建议：
- 告知用户该PDF是扫描版，文本提取无效
- 如需处理，建议安装 tesseract-ocr：
    brew install tesseract tesseract-lang  # macOS
    apt install tesseract-ocr tesseract-ocr-chi-sim  # Ubuntu
```

---

## Word 文件处理

```
python-docx 说明：
  安装：pip install python-docx
  
  提取内容包括：
  - 正文段落（doc.paragraphs）
  - 表格内容（doc.tables，如需要）
  
  注意：
  - 页眉页脚内容默认不提取
  - 图片内文字无法提取
  - 仅支持 .docx 格式，不支持老版 .doc
  
  .doc 格式处理：
  - 建议先用 Word/WPS 另存为 .docx
  - 或使用 LibreOffice 转换：
    libreoffice --convert-to docx file.doc
```
