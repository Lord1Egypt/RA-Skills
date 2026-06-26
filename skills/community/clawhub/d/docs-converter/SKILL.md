---
name: wdangz-doc-converter
description: 调用文档转换全能王(https://www.wdangz.com)API进行文档格式转换。支持PDF/Word/Excel/PPT/图片等格式互转，OCR识别，PDF合并拆分加密等。转换完成后自动下载到原文件目录。
env_vars:
  WDANGZ_API_KEY:
    description: 文档转换全能王 API Key，从 https://www.wdangz.com 获取
    required: true
endpoints:
  - https://www.wdangz.com/api/v1/convert
  - https://www.wdangz.com/api/v1/checkState
  - https://www.wdangz.com/file/{docId}
security_warning: 此技能会将本地文件上传到第三方服务进行转换，请勿用于敏感文档
---

# 📄 文档转换全能王

调用 [文档转换全能王](https://www.wdangz.com) API 实现专业文档格式转换。

## ⚠️ 重要安全须知

**使用此工具前，请务必了解以下风险：**

| 风险类型 | 说明 |
|---------|------|
| 📤 **数据上传** | 文件将上传到 `https://www.wdangz.com` 进行转换 |
| 🔒 **隐私风险** | 请勿上传包含敏感信息、机密数据或受监管文档 |
| 💼 **商业机密** | 涉及商业秘密的文档请使用本地转换工具 |
| 🏥 **个人隐私** | 包含个人身份信息(PII)的文档请谨慎处理 |

**建议在以下情况下使用：**
- ✅ 公开文档、普通办公文档
- ✅ 已脱敏的处理后文档
- ✅ 非敏感的格式转换需求

**不建议用于：**
- ❌ 财务报表、合同文件
- ❌ 身份证件、银行卡照片
- ❌ 公司内部机密文档
- ❌ 包含个人隐私的文件

---

## ✨ 支持的转换

| 转换类型 | 示例 |
|----------|------|
| Word → PDF | "docx转PDF" |
| Excel → PDF | "xlsx转PDF" |
| PPT → PDF | "ppt转PDF" |
| PDF → Word | "PDF转Word" |
| PDF → Excel | "PDF转Excel" |
| PDF → 图片 | "PDF转图片" |
| 图片 → Word (OCR) | "图片转Word" |
| 图片 → Excel (OCR) | "图片转Excel" |
| PDF合并 | "合并PDF" |
| PDF拆分 | "拆分PDF" |
| PDF水印 | "添加水印" |
| PDF加密/解密 | "加密PDF" / "解密PDF" |

---

## 🚀 使用方式

直接告诉我：
1. **文件路径** - 例如 `E:\doc\report.docx`
2. **目标格式** - 例如 "转成PDF"、"转为Word"

**示例：**
- "把 E:\doc\报告.docx 转换成 PDF"
- "将 report.pdf 转成 Word"
- "帮我把这个Excel转成PDF"
- "PDF文件添加水印"

---

## 📥 输出

转换后的文件自动保存到 **原文件同一目录**。

---

## ⚙️ 配置 API Key（必需）

**首次使用必须配置 API Key！**

### 获取 API Key 步骤
1. 访问 [文档转换全能王](https://www.wdangz.com) 注册账号
2. 在官网菜单中找到 **「API服务」** 菜单并点击进入
3. 按照页面提示开通 API 服务
4. 获取 API Key 后设置环境变量

### 配置方式：环境变量（唯一支持方式）

**Windows:**
```powershell
# 临时设置（当前终端会话）
$env:WDANGZ_API_KEY = "你的API密钥"

# 永久设置（用户级别）
[Environment]::SetEnvironmentVariable("WDANGZ_API_KEY", "你的API密钥", "User")
```

**Linux/Mac:**
```bash
# 临时设置
export WDANGZ_API_KEY="你的API密钥"

# 永久设置（添加到 ~/.bashrc 或 ~/.zshrc）
echo 'export WDANGZ_API_KEY="你的API密钥"' >> ~/.bashrc
source ~/.bashrc
```

---

## 📋 技术细节

| 项目 | 说明 |
|-----|------|
| API端点 | `https://www.wdangz.com/api/v1/convert` |
| 文件限制 | 单文件最大 50MB |
| 支持格式 | doc, docx, xls, xlsx, ppt, pptx, pdf, jpg, png, bmp, gif, webp |
| 依赖 | Python 3.x + requests 库 |

---

💡 **Tip:** 只需用自然语言描述你要做什么，我会自动识别转换类型！
