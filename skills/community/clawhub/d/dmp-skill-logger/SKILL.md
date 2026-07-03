---
name: skill-logger-v2-global-1
description: 跨平台任务历史记录技能（全局存储版），支持DeepMiner、OpenClaw、扣子等，优先使用全局路径实现跨对话共享，自动记录明日DMP系列技能的任务参数、执行时间和操作步骤
---

# skill-logger

通用的任务历史记录工具，为明日DMP系列技能提供统一的任务追踪能力。

**🌟 全局存储版特性**：优先使用全局共享路径（`/tmp/.skill-logger/`），实现**跨对话共享**任务历史记录。

---

## 📋 功能说明

### 1. 记录任务

自动记录任务的完整信息：
- 任务类型（人群圈选/人群洞察/人群投放）
- 任务名称和创建时间
- 完整的任务参数
- 每一步操作的详细记录
- 任务执行结果
- **运行平台信息**

### 2. 查询历史

支持多维度查询历史任务：
- 按任务类型过滤
- 按状态过滤（成功/失败/进行中）
- 按时间范围过滤
- 限制返回数量

### 3. 智能路径检测

自动检测可用的存储路径（按优先级）：
1. **全局共享路径**（`/tmp/.skill-logger/` - 最高优先级，跨对话共享）
2. 用户home目录（`~/.skill-logger/`）
3. 环境变量指定的工作空间路径（`WORKSPACE_DIR`、`WORKSPACE_PATH`）
4. 当前工作目录
5. 其他临时目录（`/var/tmp`）
6. 脚本所在目录

---

## 🚀 使用方式

### 记录任务

**由明日DMP技能自动调用**，无需手动操作。

当明日DMP技能（人群圈选/洞察/投放）成功创建任务后，会自动调用本技能记录任务信息。

**命令行调用示例**：
```bash
python scripts/record_task.py \
  --task-type "人群洞察-明略洞察" \
  --task-name "目标人群特征洞察" \
  --params '{"人群ID": 125456, "洞察类型": "明略洞察"}' \
  --status "成功"
```

### 查询历史

**查询最近10条记录**：
```bash
python scripts/query_tasks.py
```

**按条件查询**：
```bash
# 查询人群圈选任务
python scripts/query_tasks.py --task-type "人群圈选"

# 查询成功的任务
python scripts/query_tasks.py --status "成功"

# 查询最近20条记录
python scripts/query_tasks.py --limit 20
```

### 测试路径检测

**测试智能路径检测功能**：
```bash
python scripts/path_detector.py
```

输出示例：
```
=== 平台信息检测 ===
platform: deepminer
cwd: /data/dm-agent-outputs/workspace/xxx
home: /home/sandbox
workspace_env: /data/dm-agent-outputs/workspace/xxx

=== 路径检测 ===
✅ 平台检测: deepminer
✅ 使用存储路径: /data/dm-agent-outputs/workspace/xxx/.skill-logger/task_history.json
✅ 检测成功: /data/dm-agent-outputs/workspace/xxx/.skill-logger/task_history.json
```

---

## 💾 数据存储

### 存储路径

**🌟 全局存储版默认路径**：`/tmp/.skill-logger/task_history.json`

**优势**：
- ✅ **跨对话共享**：所有对话都访问同一份任务历史
- ✅ **新对话可查询**：创建新对话后，可以查询到之前所有的任务记录
- ✅ **无权限限制**：`/tmp` 目录通常对所有进程可读写

**备选路径**（按优先级）：
- **DeepMiner**: `/tmp/.skill-logger/task_history.json`（全局共享）
- **OpenClaw**: `/tmp/.skill-logger/task_history.json`（全局共享）
- **扣子**: `/tmp/.skill-logger/task_history.json`（全局共享）

如果 `/tmp` 不可用，会自动降级到其他可用路径（home目录、工作空间等）

### 数据格式

```json
[
  {
    "task_id": "人群洞察_20260603105726",
    "task_type": "人群洞察-明略洞察",
    "task_name": "目标人群特征洞察",
    "created_at": "2026-06-03 10:57:26",
    "status": "成功",
    "parameters": {
      "人群ID": 123456,
      "洞察类型": "明略洞察",
      "洞察维度": ["demographic", "interest", "media"]
    },
    "operations": [],
    "result": {},
    "platform": "deepminer"
  }
]
```

---

## 🔧 技术实现

### 智能路径检测算法

```python
def get_task_history_path():
    """
    智能检测并返回任务历史文件路径
    按优先级尝试多个可能的路径，返回第一个可写入的位置
    """
    candidate_paths = [
        os.getenv('WORKSPACE_DIR'),      # 环境变量指定的工作空间
        os.getenv('WORKSPACE_PATH'),
        os.getcwd(),                      # 当前工作目录
        str(Path.home()),                 # 用户home目录
        '/tmp',                           # 临时目录
    ]
    
    for base_path in candidate_paths:
        try:
            history_dir = os.path.join(base_path, '.skill-logger')
            history_file = os.path.join(history_dir, 'task_history.json')
            
            # 创建目录并测试写入权限
            os.makedirs(history_dir, exist_ok=True)
            test_file = os.path.join(history_dir, '.test_write')
            with open(test_file, 'w') as f:
                f.write('test')
            os.remove(test_file)
            
            return history_file  # 返回第一个可写入的路径
        except (PermissionError, OSError):
            continue  # 尝试下一个路径
    
    raise RuntimeError("无法找到可写入的存储路径")
```

### 平台检测机制

通过以下方式检测当前运行平台：
1. **环境变量检测**：检查特定的环境变量（如`DEEPMINER`、`OPENCLAW`、`COZE`）
2. **路径特征检测**：分析当前工作目录路径中的关键词
3. **默认值**：如果无法识别，标记为`unknown`

---

### 路径优先级

**🌟 全局存储版统一优先级**（所有平台）：

1. **`/tmp/.skill-logger/`** ✅ （最高优先级 - 全局共享）
2. 用户home目录（`~/.skill-logger/`）
3. `WORKSPACE_DIR`/`WORKSPACE_PATH`环境变量
4. 当前工作目录
5. 其他临时目录（`/var/tmp`）


---

## 📦 技能依赖

无依赖，可独立使用。

---

## 🔍 故障排查

### 问题1：找不到存储路径

**症状**：运行时报错`RuntimeError: 无法找到可写入的存储路径`

**解决方案**：
1. 运行`python scripts/path_detector.py`查看详细的路径检测日志
2. 检查是否有任何候选路径具有写入权限
3. 手动设置环境变量`WORKSPACE_DIR`指定存储路径

### 问题2：不同对话的记录无法共享

**🌟 全局存储版已解决**：本版本优先使用 `/tmp/.skill-logger/` 全局路径，所有对话自动共享任务历史。

**如果仍然无法共享**：
- 检查路径检测结果：运行 `python scripts/path_detector.py`
- 确认是否使用了 `/tmp/.skill-logger/task_history.json` 路径
- 如果使用了其他路径，可能是权限问题导致降级

### 问题3：平台检测不准确

**解决方案**：
1. 检查环境变量是否正确设置
2. 查看`platform`字段，确认检测结果
3. 如果标记为`unknown`，不影响功能使用，只是无法识别平台名称

---

## 📝 注意事项

1. 本技能为**可选技能**，不安装不影响明日DMP技能的核心功能
2. 安装后可自动记录所有任务历史，便于追溯和审计
3. 数据存储在本地，安全可靠
4. **跨平台兼容**：同一个技能包可以在多个AI平台上使用
5. **智能适配**：无需手动配置，自动选择最佳存储路径


---

## 📄 许可证

MIT License