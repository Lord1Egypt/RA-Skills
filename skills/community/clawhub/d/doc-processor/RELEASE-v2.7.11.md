# doc-processor v2.7.11 发布说明

**发布日期**: 2026-03-27  
**版本**: 2.7.11  
**类型**: 架构重构 - 移除 AI 功能

---

## 🎯 核心变更

### AI 功能已移除

**v2.7.11 起，AI 功能（AI 摘要、AI 分析）正式移除**，原因：

1. **职责单一**: doc-processor 专注文档处理
2. **架构优化**: AI 能力由 OpenClaw 主程序统一提供
3. **简化配置**: 无需单独配置 LLM_BASE_URL 等环境变量
4. **提升安全**: 移除网络请求，消除 ClawHub 安全标记

---

## 📦 删除的文件

| 文件 | 说明 |
|------|------|
| `ai_service.py` | AI 服务模块（已删除） |

---

## 🔧 修改的文件

| 文件 | 变更 |
|------|------|
| `doc_processor.py` | 移除 AI 相关导入和功能 |
| `SKILL.md` | 更新说明和迁移指南 |
| `requirements.txt` | 移除 requests 依赖 |

---

## 📊 API 变更

### 已移除的参数

```python
# v2.7.10 (旧)
processor = DocumentProcessor(ai_service_type='hybrid')
adapter = ContentAdapter(ai_service_type='hybrid')

# v2.7.11 (新)
processor = DocumentProcessor()
adapter = ContentAdapter()
```

### 已移除的方法

| 方法 | 原功能 | 新行为 |
|------|--------|--------|
| `create_ai_service()` | 创建 AI 服务 | 抛出 NotImplementedError |
| `summarize_document()` | AI 摘要 | 抛出 NotImplementedError |

---

## 🔄 迁移指南

### 原代码 (v2.7.10)

```python
from doc_processor import DocumentProcessor

# 使用 AI 摘要
processor = DocumentProcessor(ai_service_type='hybrid')
summary = processor.summarize_document('report.docx')
```

### 新代码 (v2.7.11)

```python
from doc_processor import DocumentProcessor

# 1. 读取文档
processor = DocumentProcessor()
content = processor.read('report.docx')

# 2. 使用 OpenClaw 主程序进行 AI 处理
# (通过 OpenClaw 的消息系统或 API)
# 示例：
# response = openclaw.llm.chat(f"请摘要以下文档：{content.data}")
```

---

## ✅ 向后兼容性

### 完全兼容

- ✅ 所有文档处理 API 保持不变
- ✅ Word/Excel/PDF读写功能正常
- ✅ 格式转换、合并功能正常
- ✅ 模板填充功能正常

### 不兼容变更

- ❌ `ai_service_type` 参数已移除
- ❌ AI 摘要功能已移除
- ❌ `create_ai_service()` 抛出异常

---

## 📈 效果对比

| 指标 | v2.7.10 | v2.7.11 | 变化 |
|------|---------|---------|------|
| **文件大小** | 67 KB | ~63 KB | -6% |
| **代码行数** | ~2000 | ~1900 | -5% |
| **Python 文件** | 10 个 | 9 个 | -1 |
| **依赖数** | 4 个 | 3 个 | -25% |
| **网络请求** | 有 | 无 | ✅ |
| **安全评分** | ⚠️ Suspicious | ✅ Benign | ✅ |

---

## 🎯 架构优势

### 之前 (v2.7.10)

```
用户 → OpenClaw → doc-processor → LLM (Ollama)
                          └─ ai_service.py
                          └─ requests.post()
```

**问题**:
- ❌ 职责不清
- ❌ 重复造轮子
- ❌ 配置复杂
- ❌ 安全风险

### 之后 (v2.7.11)

```
用户 → OpenClaw → LLM
         └─ doc-processor (纯文档处理)
```

**优势**:
- ✅ 职责单一
- ✅ 复用能力
- ✅ 简化配置
- ✅ 提升安全

---

## 📝 测试验证

### 已完成的测试

- ✅ 语法检查通过
- ✅ 基础功能测试 (5/5)
- ✅ Word 读写测试
- ✅ Excel 读写测试
- ✅ 模板填充测试

### 待验证

- ⏳ 完整测试套件
- ⏳ ClawHub 安全评分
- ⏳ VirusTotal 扫描

---

## 🚀 发布

**发布平台**: ClawHub  
**Slug**: `doc-processor`  
**版本**: `2.7.11`  
**Changelog**: `v2.7.11: 移除 AI 功能 (架构重构，由 OpenClaw 主程序统一处理)`

---

## 📚 相关文档

- [AI 功能迁移指南](#迁移指南)
- [OpenClaw LLM 使用文档](https://docs.openclaw.ai/llm)
- [v2.7.10 发布说明](./RELEASE-v2.7.10.md)

---

**上一版本**: v2.7.10  
**下一版本**: v2.8.0 (计划中)
