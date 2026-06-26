# sync.py 详细行为说明与边界情况

## 核心机制

### Hash 与 History

- 文件每次内容变化时，新 MD5 hash 追加到 history 尾部
- history 长度上限为 10（`HISTORY_LIMIT`）
- 同步时，双方 history 会合并去重，保留最近 10 个版本

### 共同祖先检测

`sync.py` 通过 `find_common_ancestor(h1, h2)` 在双方 history 中寻找最近的共同版本：
- 从最新的 hash 向前遍历 local history，在 remote history 中查找匹配
- 找到的第一个匹配即为共同祖先

### 冲突判定逻辑

```
if l and r (文件在双方都存在):
    if lh == rh:  # hash 相同
        continue  # 无需操作
    base = find_common_ancestor(l["history"], r["history"])
    if base is None or (lh != base and rh != base):
        → 冲突（双方都偏离祖先，或无共同祖先）
    elif lh == base:
        → remote 胜出，复制到 local
    elif rh == base:
        → local 胜出，复制到 remote
```

### 删除 vs 修改的冲突

- `l_deleted = (not l) and lo` — local 文件消失但 old state 有记录
- `r_deleted = (not r) and ro` — remote 文件消失但 old state 有记录

当一边删除、另一边修改时，`handle_conflict` 被调用（而非 move_to_trash）。
这是因为：对方修改的内容若直接覆盖删除方的空位，会导致数据丢失。

**预期场景**：A 删除文件，B 同时修改文件 → 冲突保存，B 的修改不会覆盖 A 的删除意图。

### move_to_trash 的触发条件

只有当**双方同时删除**（l_deleted and r_deleted 都不满足，但 lo/ro 有记录而 l/r 不存在）时，才会调用 `move_to_trash`。实际上代码中：

```python
if l_deleted:  # local 删除，remote 未动
    move_to_trash(remote_root, f, log_file)  # remote 端文件移入 trash
if r_deleted:  # remote 删除，local 未动
    move_to_trash(local_root, f, log_file)  # local 端文件移入 trash
```

注意：`l_deleted and r` 分支会冲突，而不是走删除流程。

## 边界情况

1. **文件仅在一方的 .trash/.conflict/.sync_logs 中存在**：这些目录本身被 `os.walk` 忽略（`dirnames[:] = [d for d in dirnames if d not in IGNORE_DIRS]`），因此不会参与同步。

2. **同名子目录 vs 文件冲突**：例如一方是文件 `foo`，另一方是目录 `foo/`。同步会尝试 `shutil.copy2` 一个文件到已存在的目录路径，导致异常，被 `try/except` 捕获并记录 ERROR。

3. **state 文件损坏/非 JSON**：load_state 返回空字典 `{}`，文件被当作新文件处理。

4. **同步链（PC1 → PC2 → USB）**：每次 sync 是两方之间进行，多跳同步时需注意中间状态可能不一致。

5. **并发使用**：不支持多个进程同时对同一目录执行 sync，可能导致状态文件损坏。

6. **Windows 路径分隔符**：代码使用 `os.sep`，路径比较时用 `rel_path.replace(os.sep, '_')` 生成冲突文件名，Windows 上会替换 `\` 为 `_`。

7. **历史断裂**：如果文件在某次同步后被手动复制到另一端（未通过 sync.py），两端的 history 会各自独立，后续冲突检测可能失效。