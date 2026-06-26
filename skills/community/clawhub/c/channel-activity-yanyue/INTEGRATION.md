# 短期记忆集成指南

## 🔍 问题定位

**功能状态**：
- ✅ 记录功能：正常
- ✅ 读取功能：正常
- ✅ 跨通道：正常
- ❌ **会话集成**：缺失 ← 这是问题！

## 🎯 解决方案

### 方案 1：手动调用（立即使用）

**在炎月回复前**，执行：
```python
from session_hook import get_session_context

# 飞书会话
context = get_session_context("feishu")
# 输出：[其他通道最近 30 分钟活动] - [qq] 15:00: xxx

# QQ 会话
context = get_session_context("qq")
# 输出：[其他通道最近 30 分钟活动] - [feishu] 15:00: xxx
```

### 方案 2：自动 Hook（推荐）

**集成到 OpenClaw**：
1. 在 `openclaw.json` 中添加 hook
2. 每次会话前自动调用 `session_hook.py`
3. 将结果注入到上下文

### 方案 3：炎月主动调用

**炎月在每次回复前**：
```python
# 判断当前通道
current_channel = get_current_channel()  # feishu or qq

# 获取临时记忆
temp_context = get_session_context(current_channel)

# 整合到回复
final_context = session_history + MEMORY.md + temp_context
```

## 📋 使用流程

### 1. 星之君在飞书发消息
```
飞书："帮我记住要买牛奶"
```

**炎月自动记录**：
```python
ca.record("feishu", "星之君要求买牛奶")
```

### 2. 星之君在 QQ 问
```
QQ："我刚才说了什么？"
```

**炎月自动获取上下文**：
```python
context = get_session_context("qq")
# 输出：[其他通道最近 30 分钟活动] - [feishu] 15:00: 星之君要求买牛奶
```

**炎月回复**：
```
"星之君刚才在飞书说：要买牛奶"
```

## ⚙️ 技术实现

**session_hook.py**：
```python
def get_session_context(current_channel: str) -> str:
    ca = ChannelActivity()
    summary = ca.get_context_summary(channel=current_channel)
    return summary if summary else ""
```

**输出格式**：
```
[其他通道最近 30 分钟活动]
- [qq] 15:00: 测试 QQ 通道活动
- [feishu] 15:05: 星之君要求买牛奶
```

## 🧪 验证结果

**测试 1：飞书会话**
```
输入：get_session_context("feishu")
输出：[其他通道最近 30 分钟活动] - [qq] 15:00: xxx
✅ 正确：显示 QQ 活动，排除飞书
```

**测试 2：QQ 会话**
```
输入：get_session_context("qq")
输出：[其他通道最近 30 分钟活动] - [feishu] 15:00: xxx
✅ 正确：显示飞书活动，排除 QQ
```

## 📝 下一步

**需要集成到 OpenClaw 会话流程**：
1. 在 Gateway 层添加 hook
2. 或在炎月回复前自动调用
3. 将临时记忆注入到 prompt

**星之君选择哪种方案？**
- 方案 1：手动调用（简单，但需要手动）
- 方案 2：自动 Hook（推荐，需要配置）
- 方案 3：炎月主动（灵活，需要修改回复逻辑）

---

**创建时间**：2026-03-08 15:15  
**状态**：✅ 功能验证通过，等待集成方案选择