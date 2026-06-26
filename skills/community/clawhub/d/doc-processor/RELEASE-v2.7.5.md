# doc-processor v2.7.5 发布说明

> **注意**: v2.7.11 起 AI 功能已移除。本文档中的 AI 相关描述已不再适用。

**发布日期**: 2026-03-27  
**版本**: 2.7.5  
**类型**: Bug 修复 + 代码质量提升

---

## 🐛 Bug 修复

### P0: convert() 路径解析错误

**问题**: `convert()` 方法未使用 `_resolve_path()` 解析目标路径，导致输出文件写入当前工作目录而非 workspace。

**修复**:
```python
def convert(self, src_path: str, dst_path: str) -> str:
    content = self.read(src_path)
    # v2.7.5 修复：解析目标路径到 workspace
    dst_path = self._resolve_path(dst_path)
    dst_path.parent.mkdir(parents=True, exist_ok=True)
    # ...
```

**影响**: 
- ✅ 转换操作现在正确输出到 workspace
- ✅ 支持相对路径和绝对路径
- ✅ 自动创建目标目录

---

## 🔒 安全改进

### P1: 修复裸 except 问题

**修复位置**:
- `doc_processor.py`: 5 处
- `ai_service.py`: 2 处
- `check_deps.py`: 1 处

**示例**:
```python
# 修复前
except:
    return 0.0

# 修复后
except (AttributeError, ValueError, TypeError):
    return 0.0
```

**影响**:
- ✅ 异常处理更精确
- ✅ 避免掩盖真实错误
- ✅ 便于问题诊断

---

## 🏗️ 代码质量提升

### P3: 完善异常体系

**新增异常类** (`error_handler.py`):
- `FileFormatError` - 不支持的文件格式
- `ReadError` - 读取失败
- `WriteError` - 写入失败
- `ConvertError` - 转换失败
- `TemplateError` - 模板错误
- `BatchError` - 批量处理错误
- `DependencyError` - 依赖缺失

**新增工厂函数**:
```python
format_error(format, supported)
read_error(path, reason)
write_error(path, reason)
convert_error(src, dst, reason)
template_error(template, reason)
batch_error(failed, total)
```

**影响**:
- ✅ 错误分类更清晰
- ✅ 错误消息带解决建议
- ✅ 便于调用方处理

---

## 📊 测试结果

| 测试文件 | 通过数 | 状态 |
|---------|--------|------|
| test_simple.py | 5/5 | ✅ |
| test_comprehensive.py | 22/22 | ✅ |
| test_v274.py | 5/5 | ✅ |
| 路径修复验证 | 3/3 | ✅ |

**总计**: 35/35 测试用例通过

---

## 🔄 向后兼容性

- ✅ **完全向后兼容**
- ✅ API 无变更
- ✅ 行为变更仅修复 Bug
- ✅ 现有代码无需修改

---

## 📦 升级方式

```bash
# 从 ClawHub 升级
clawhub install doc-processor --version 2.7.5 --force

# 或更新到最新版
clawhub update doc-processor
```

---

## 📝 变更文件清单

| 文件 | 变更类型 | 说明 |
|------|---------|------|
| `doc_processor.py` | 修改 | convert() 路径修复 + 裸 except 修复 |
| `ai_service.py` | 修改 | 裸 except 修复 |
| `check_deps.py` | 修改 | 裸 except 修复 |
| `error_handler.py` | 增强 | 新增 7 个异常类 + 工厂函数 |
| `SKILL.md` | 更新 | 版本号 2.7.3 → 2.7.5 |
| `_meta.json` | 更新 | 版本号 2.3.0 → 2.7.5 |
| `RELEASE-v2.7.5.md` | 新增 | 发布说明 |

---

## 🎯 推荐升级

- ✅ **强烈推荐**所有用户升级
- ✅ 修复关键路径 Bug
- ✅ 提升代码质量和可维护性
- ✅ 无升级风险

---

**上一版本**: v2.7.4  
**下一版本**: v2.8.0 (计划中)
