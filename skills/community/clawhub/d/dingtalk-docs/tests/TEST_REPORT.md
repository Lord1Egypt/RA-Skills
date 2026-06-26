# 钉钉文档技能测试报告

## 测试概述

| 项目 | 说明 |
|------|------|
| 测试日期 | 2026-03-04 |
| 版本 | 0.2.1 |
| 测试范围 | 安全功能、JSON 传参、响应解析、脚本签名一致性 |
| 测试环境 | macOS, Python 3.x, mcporter >=0.7.0 |
| 测试结果 | **18/18 通过** |

---

## 测试用例清单

### 1. 路径安全 (TestResolveSafePath) — 3 个

| 用例 | 说明 | 结果 |
|------|------|------|
| 目录遍历攻击 | `../etc/passwd` → 应拒绝 | ✅ |
| 绝对路径越界 | `/etc/passwd` → 应拒绝 | ✅ |
| 合法相对路径 | 工作目录内文件 → 应通过 | ✅ |

### 2. 文件扩展名 (TestFileExtensionValidation) — 3 个

| 用例 | 说明 | 结果 |
|------|------|------|
| 允许扩展名 | `.md`, `.txt`, `.markdown` | ✅ |
| 大小写不敏感 | `.MD`, `.TXT` | ✅ |
| 禁止扩展名 | `.exe`, `.sh`, `.py`, `.pdf` | ✅ |

### 3. 文件大小 (TestFileSizeValidation) — 2 个

| 用例 | 说明 | 结果 |
|------|------|------|
| 小文件 | < 10MB → 通过 | ✅ |
| 大文件 | > 10MB → 拒绝 | ✅ |

### 4. URL 验证 (TestDocUrlValidation) — 2 个

| 用例 | 说明 | 结果 |
|------|------|------|
| 有效 URL | 正确提取 dentryUuid | ✅ |
| 无效 URL | http / 空 ID / 含空格 / 错误域名 → None | ✅ |

### 5. 响应解析 (TestParseResponse) — 3 个

| 用例 | 说明 | 结果 |
|------|------|------|
| 扁平 JSON | 顶层直接返回 | ✅ |
| 嵌套 result | `{success, result: {dentryUuid, pcUrl}}` | ✅ |
| 非法 JSON | 返回 None | ✅ |

### 6. run_mcporter 签名 (TestRunMcporter) — 2 个

| 用例 | 说明 | 结果 |
|------|------|------|
| 函数签名 | 参数为 `(tool, args, timeout)` | ✅ |
| 三脚本一致 | create/import/export 签名相同 | ✅ |

### 7. 内容长度常量 (TestContentLimits) — 3 个

| 用例 | 说明 | 结果 |
|------|------|------|
| create_doc | MAX_CONTENT_LENGTH = 50000 | ✅ |
| import_docs | MAX_CONTENT_LENGTH = 50000 | ✅ |
| export_docs | MAX_CONTENT_LENGTH = 100000 | ✅ |

---

## API 方法端到端测试

| 方法 | 状态 | 备注 |
|------|------|------|
| `get_my_docs_root_dentry_uuid()` | ✅ 成功 | JSON 传参，返回根目录 ID |
| `list_accessible_documents()` | ✅ 成功 | `--args '{"keyword": "..."}'` 格式 |
| `create_doc_under_node()` | ✅ 成功 | 创建文档 + 正确解析嵌套 result |
| `write_content_to_document()` | ✅ 成功 | 覆盖写入验证通过 |
| `get_document_content_by_url()` | ✅ 成功 | 导出内容与写入一致 |
| `create_dentry_under_node()` | ⚠️ 受限 | 企业账号权限限制（错误码 52600007） |

---

## 测试命令

```bash
cd ~/Skills/dingtalk-docs
python3 tests/test_security.py -v
```

---

**测试状态：** ✅ 18/18 通过
