# 钩子系统参考

## 核心约束

**本技能的所有关键约束由 Python 端强制执行，不依赖 LLM 自觉。**
备份、版本管理初始化、版本上限清理均由钩子直接在脚本层完成，
LLM 无权跳过这些操作。

## 设计目标

在 drawiodo 的 Think -> Confirm -> Iterate -> Version Control 四阶段工作流中
嵌入可插拔的钩子扩展点，实现：

1. **强制约束**：备份/版本管理等关键操作由 Python 端自动执行
2. **安全拦截**：在关键节点自动校验状态，防止错误的输入/输出通过
3. **自动补全**：缺省上下文字段和输出目录自动补全/创建
4. **快捷跳转**：满足条件时自动跳过不必要的确认环节
5. **后处理自动化**：生成后自动初始化版本管理、自动校验、自动预览

## Hook Point 定义

| Hook Point | 阶段 | 触发时机 | 标准上下文 |
|---|---|---|---|
| `pre_think` | 思考前 | 收到用户输入后、分析前 | `user_input`, `workspace` |
| `post_think` | 思考后 | 分析完成后、展示方案前 | `analysis_output` |
| `pre_confirm` | 确认前 | 展示选项前 | `confirm_options`, `analysis_output` |
| `post_confirm` | 确认后 | 用户选择后 | `user_choice`, `analysis_output` |
| `pre_iterate` | 迭代前 | 生成/更新文件前 | `output_path`, `is_update` |
| `post_iterate` | 迭代后 | 文件生成完成后 | `output_path` |
| `pre_vc` | 版本操作前 | 保存/恢复版本前 | `version_count`, `max_versions` |
| `post_vc` | 版本操作后 | 版本操作完成后 | `vc_result` |

## 内置钩子清单

### pre_think (2 个)

1. **input_validator** (强制阻断)
   - 校验 `user_input` 非空
   - abort=True -> 输入为空时阻断，LLM 无法继续

2. **context_enricher** (自动补全)
   - 补全 `workspace`（默认 `.`）
   - 补全 `timestamp`（当前时间）

### post_think (1 个)

1. **output_validator**
   - 校验 `analysis_output` 包含 `diagram_type` 和 `complexity`
   - abort=False -> 仅警告，不阻断

### pre_confirm (2 个)

1. **option_validator** (强制阻断)
   - 校验 `confirm_options` 非空且 >= 2 项
   - abort=True -> 选项不足时直接阻断

2. **shortcut_detector** (强制清除选项)
   - 检测是否满足快捷模式条件
   - 满足条件时：直接清除 `confirm_options` 为空列表，LLM 无法展示 AskUserQuestion
   - 条件：简单流程图、JSON spec 模式、已确认方案

### post_confirm (1 个)

1. **choice_parser**
   - 将 `user_choice` 写入 `ctx['execution_params']`

### pre_iterate (2 个)

1. **file_checker** (自动创建)
   - 输出目录不存在时自动 `os.makedirs()` 创建
   - 不 abort，LLM 无需关心目录问题

2. **auto_backup** (【强制】Python 端自动执行备份)
   - **非首次迭代时，直接调用 `VersionManager.save_version()` 执行备份**
   - **不需要 LLM 读取任何 flag，不需要 LLM 调用任何脚本**
   - 备份结果写入 `ctx['backup_result']`
   - 更新 `ctx['version_count']` 和 `ctx['current_version']`
   - abort=True -> 备份失败时阻断（确保不丢数据）

### post_iterate (2 个)

1. **output_validator** (【强制】Python 端自动初始化版本管理)
   - 校验文件存在性、文件大小 >= 200 字节
   - **首次生成时，直接调用 `VersionManager.init()` 自动注册版本管理**
   - **不需要 LLM 读取任何 flag，不需要 LLM 调用任何脚本**
   - abort=True -> 文件不存在时阻断

2. **preview_trigger** (【强制】Python 端自动打开预览)
   - 直接调用 `subprocess.Popen([drawio_exe, output_path])` 打开 draw.io
   - draw.io 未安装时仅警告，不阻断
   - LLM 无权跳过预览

### pre_vc (1 个)

1. **limit_checker** (【强制】Python 端自动清理)
   - 检查 `version_count >= max_versions`
   - **超限时，直接删除最旧版本的目录和日志**
   - **不需要 LLM 读取任何 flag，不需要 LLM 执行任何清理操作**
   - 清理结果写入 `ctx['pruned']`

### post_vc (1 个)

1. **status_reporter**
   - 报告版本操作结果（version + description）

## 强制约束清单

以下操作由钩子在 Python 端**自动执行**，LLM 无权干预：

| # | 操作 | 执行钩子 | 触发点 |
|---|---|---|---|
| 1 | 校验输入非空 | input_validator | pre_think |
| 2 | 自动创建输出目录 | file_checker | pre_iterate |
| 3 | 自动备份当前版本 | auto_backup | pre_iterate |
| 4 | 自动初始化版本管理 | output_validator | post_iterate |
| 5 | 自动清理超限版本 | limit_checker | pre_vc |

## API 参考

### `hooks(point, context) -> list[HookResult]`

一键触发钩子，最常用的入口。

```python
from drawio_hooks import hooks

results = hooks('pre_think', {'user_input': '画一个流程图'})
for r in results:
    if r.abort:
        return  # 钩子已阻止流程，直接返回
    if not r.success:
        print(f'Warning: {r.message}')
```

### `register(point, name=None, description='') -> decorator`

注册一个钩子函数到指定 Hook Point。

```python
from drawio_hooks import register

@register('pre_think', name='my_audit', description='自定义审计')
def audit_hook(ctx):
    if 'user_input' not in ctx:
        return {'success': False, 'message': 'missing input', 'abort': True}
    return {'success': True, 'message': 'ok'}
```

### `unregister(point, name) -> bool`

注销指定钩子。返回 True 表示成功。谨慎使用。

```python
from drawio_hooks import unregister
unregister('post_iterate', 'preview_trigger')  # 禁用自动预览
```

### `registry() -> dict`

返回所有注册的钩子（按 Hook Point 分组）。

### `history(limit=20) -> list[dict]`

返回最近 N 次钩子执行历史。

### `clear()`

清空所有注册（测试/重置用）。

## HookResult 结构

| 字段 | 类型 | 说明 |
|---|---|---|
| `success` | bool | 执行是否成功 |
| `message` | str | 结果描述 |
| `abort` | bool | 是否阻断流程 |
| `data` | dict | 额外数据 |
| `name` | str | 钩子名称 |
| `point` | str | 所属 Hook Point |
| `timestamp` | str | 执行时间 ISO8601 |

## CLI

```bash
python scripts/drawio_hooks.py list     # 查看注册表
python scripts/drawio_hooks.py check    # 全流程自检
python scripts/drawio_hooks.py history  # 执行历史
```

## 自定义钩子最佳实践

1. **保持幂等**：同一输入多次执行应产生相同结果
2. **单一职责**：一个钩子只做一件事
3. **提供清晰 message**：abort 时 message 应指出问题和修复方向
4. **非必要不 abort**：可恢复的问题只 warning，不可恢复才 abort
5. **用 register 而非改源码**：新增逻辑用装饰器，不更新 drawio_hooks.py