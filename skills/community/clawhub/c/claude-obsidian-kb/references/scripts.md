# 脚本使用指南

---

## auto_link.py — 双向链接自动织网

```bash
python3 scripts/auto_link.py <vault_path> [--dry-run]
```

**功能**：
1. 扫描 vault 中所有 `.md` 文件
2. 检测 `[[笔记名]]` 双向链接的有效性
3. 生成死链列表（指向不存在的笔记）
4. 生成孤儿笔记列表（无任何笔记链接的笔记）
5. 输出可执行的修复建议

**输出格式**：
```
=== 死链报告 ===
[[不存在的笔记]] 在以下文件中被引用：
  - file1.md (line 23)
  - file2.md (line 7)

=== 孤儿笔记 ===
以下笔记未被任何笔记链接：
  - orphan_note.md
```

**--dry-run**：仅报告，不修改文件

---

## hot_cache.py — 热缓存管理

```bash
python3 scripts/hot_cache.py <vault_path> get <key>
python3 scripts/hot_cache.py <vault_path> set <key> <value>
python3 scripts/hot_cache.py <vault_path> list
python3 scripts/hot_cache.py <vault_path> clear
```

**功能**：在 vault 根目录维护 `.cache/hot_cache.json`，跨 session 存储关键状态：

- 最后整理时间
- 已处理过的 raw 文件列表
- 当前活跃项目/话题
- 用户偏好设置

**示例**：
```bash
# 获取上次整理的主题
python3 scripts/hot_cache.py ./vault get active_topic

# 设置当前活跃话题
python3 scripts/hot_cache.py ./vault set active_topic "FMT-肠菌移植"
```

---

## extract_entities.py — 实体提取

```bash
python3 scripts/extract_entities.py <input_file.md> [--vault <vault_path>]
```

**功能**：
1. 读取输入的 markdown 文件
2. 使用 AI（通过 API）提取实体列表
3. 检查 vault 中是否存在对应笔记
4. 生成创建建议

**--vault**：指定 vault 路径，生成创建建议时包含现有笔记对比
