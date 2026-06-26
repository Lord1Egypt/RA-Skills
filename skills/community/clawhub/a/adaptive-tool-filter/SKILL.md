# 自适应工具过滤 Skill

智能过滤工具列表，减少 token 消耗，提高响应效率。

## 功能

1. **意图识别** - 根据用户输入识别任务意图
2. **工具匹配** - 筛选与意图相关的工具
3. **优先级排序** - 按相关性排序工具列表
4. **动态调整** - 根据对话进展调整工具集

## 设计原理

参考 LightAgent 的自适应工具机制：
- 不是所有工具都需要在每次请求中加载
- 根据任务类型动态过滤
- 减少不必要的 token 消耗

## 意图分类

| 意图类型 | 相关工具 | 触发信号 |
|----------|----------|----------|
| **文件操作** | read, write, edit, exec | "读取"、"写入"、"文件"、"保存" |
| **网络搜索** | web_search, web_fetch, browser | "搜索"、"查找"、"网页"、"链接" |
| **消息发送** | message, sessions_send | "发送"、"通知"、"消息"、"飞书" |
| **飞书操作** | feishu_doc, feishu_bitable_* | "飞书"、"文档"、"表格"、"知识库" |
| **Agent 管理** | sessions_spawn, subagents | "子Agent"、"协作"、"并行" |
| **节点操作** | nodes | "节点"、"手机"、"设备" |
| **系统命令** | exec, process | "运行"、"执行"、"命令"、"安装" |

## 过滤规则

### 规则 1：关键词匹配

```python
INTENT_TOOLS = {
    'file': ['read', 'write', 'edit'],
    'web': ['web_search', 'web_fetch', 'browser'],
    'feishu': ['feishu_doc', 'feishu_bitable_*', 'feishu_wiki'],
    'message': ['message', 'sessions_send'],
    'agent': ['sessions_spawn', 'subagents', 'sessions_list'],
    'system': ['exec', 'process'],
}

def filter_tools(user_input: str, all_tools: list) -> list:
    # 检测意图
    detected_intents = detect_intent(user_input)
    
    # 筛选相关工具
    relevant_tools = []
    for intent in detected_intents:
        relevant_tools.extend(INTENT_TOOLS.get(intent, []))
    
    # 添加通用工具（始终需要）
    core_tools = ['memory_search', 'memory_get', 'read', 'write']
    
    return core_tools + relevant_tools
```

### 规则 2：上下文继承

对话进行中，保留之前使用的工具：
- 如果上一步用了 `feishu_doc`，下一步可能还需要
- 但可以移除不再需要的工具（如已完成的 `web_search`）

### 规则 3：安全边界

某些工具需要特别处理：
- `exec` - 需要用户明确允许
- `edit` - 检查文件是否在工作区

## System Prompt 集成

```
## 工具管理

每次请求前，智能筛选工具：

1. 分析用户输入关键词
2. 识别任务意图类型
3. 筛选相关工具集
4. 排序：核心工具 → 相关工具 → 可选工具
5. 控制工具数量（建议 ≤ 20 个）

意图检测信号：
- 文件相关："读取"、"写入"、"文件"、"保存"、"创建"
- 网络相关："搜索"、"查找"、"网页"、"链接"、"在线"
- 飞书相关："飞书"、"文档"、"表格"、"多维表格"、"知识库"
- 消息相关："发送"、"通知"、"消息"、"回复"
- Agent相关："子Agent"、"协作"、"并行"、"启动"
```

## 效果对比

### 无过滤

```
可用工具：50+ 个
Token 消耗：每次请求 ~5000 tokens（工具定义）
响应时间：较长（模型需要评估所有工具）
```

### 有过滤

```
可用工具：10-20 个
Token 消耗：每次请求 ~1500 tokens
响应时间：更快（模型只评估相关工具）
```

## 实现建议

OpenClaw 可以在以下层面实现：

### 1. 配置层面

在 `openclaw.json` 中配置意图-工具映射：

```json
{
  "toolFilter": {
    "intents": {
      "file": ["read", "write", "edit"],
      "web": ["web_search", "web_fetch"],
      "feishu": ["feishu_*"]
    }
  }
}
```

### 2. Skill 层面

创建 `tool-filter` Skill，在请求前自动过滤。

### 3. 运行时层面

在 Agent 运行时动态调整工具集。

---

*参考 LightAgent 自适应工具机制设计*