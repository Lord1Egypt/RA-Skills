# 版本管理审计教训（v0.8.9）

## 问题发现

VERSION_RULE.md格式：
```
**当前版本：v0.8.8**
**下一个版本：v0.8.9**
```

version_sync.py的regex（错误）：
```python
r'\*\*当前版本：\*\*v\d+\.\d+\.\d+'  # 期望：**版本：**v
```

实际文本是`**当前版本：v`**（单个`**`包住整句）

## 修复

正确regex：
```python
r'\*\*当前版本：v\d+\.\d+\.\d+\*\*'
```

教训：先读取实际文本格式，再写regex。

## 验证命令

```bash
# 查看版本
python scripts/version_sync.py

# 升级并验证
python scripts/version_sync.py 0.9.0
```

## 三处验证

1. `cat VERSION` → 新版本
2. `grep "^version:" SKILL.md` → 新版本
3. `grep "当前版本" VERSION_RULE.md` → 新版本
