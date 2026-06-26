# Echo Seed 完全自动化设计方案

**儒家式开发 - 小爪&小小爪 共同设计**

---

## 📋 官家需求

1. **完全自动化** - 不需要手动 AI 分析按钮
2. **创建即分析** - Web 端/Bot 创建时自动触发 AI
3. **自动分类** - AI 分析后自动打标签
4. **Todo 自动同步** - 检测到待办自动同步 Google Calendar
5. **删除手动按钮** - 网页端删除 AI 分析面板

---

## 🔄 自动化流程

```
用户创建种子
    ↓
[Web 端 / Bot 端]
    ↓
1. 保存种子到数据库
    ↓
2. 自动触发 AI 分析（后台异步）
    ├─ 链接分析（如果有 URL）
    ├─ 点子扩张（如果是 idea 或短内容）
    └─ 智能关联（查找相关种子）
    ↓
3. AI 返回结果
    ├─ 自动标签 → 更新种子 tags 字段
    ├─ Todo 识别 → 同步到 Google Calendar
    └─ 分析结果 → 保存到 ai_analyses 表
    ↓
4. 返回用户
    ├─ Web 端：刷新列表（种子已带 AI 标签）
    └─ Bot 端：回复消息（含 AI 分析摘要）
```

---

## 📁 需要修改的文件

| 文件 | 修改内容 | 优先级 |
|------|---------|--------|
| **echo-web.py** | 创建种子后异步调用 AI 分析 | 🔴 P0 |
| **echo-telegram.py** | 修复 AI 导入路径，确保触发 | 🔴 P0 |
| **ai_service.py** | 添加 Todo 识别逻辑 | 🔴 P0 |
| **index.html** | 删除 AI 分析面板（手动按钮） | 🟡 P1 |
| **db_helper.py** | 已就绪 | ✅ |

---

## 🎯 AI 分析触发规则

| 条件 | 触发分析 | 说明 |
|------|---------|------|
| **有 URL** | 链接分析 | 提取网页内容 + 总结 + 标签 |
| **类型=idea** | 点子扩张 | 扩展想法成方案 |
| **内容<50 字** | 点子扩张 | 短内容自动扩展 |
| **所有种子** | 智能关联 | 查找相关种子 |
| **所有种子** | 自动标签 | AI 生成标签 |

---

## ✅ Todo 识别规则

**AI 分析后，判断是否需要同步到日历：**

### 规则 1：显式 Todo
- 类型 = `todo`
- 内容包含时间词（明天/下周/3 点后等）
- → 同步到 Google Calendar（定时事件）

### 规则 2：隐式 Todo
AI 分析检测到以下关键词：
- "记得"、"别忘了"、"要做"、"需要"
- "明天"、"下周"、"下午"、"晚上"
- "会议"、"面试"、"约会"、"截止"
- → 询问用户是否同步到日历（或直接同步）

### 规则 3：非 Todo
- 笔记、灵感、日记、链接等
- → 不同步到日历，仅存 Notion

---

## 🔧 技术实现

### 1. Web 端自动 AI（echo-web.py）

```python
@app.route('/api/capsules', methods=['POST'])
def create_capsule():
    # ... 创建种子 ...
    
    # 异步触发 AI 分析（不阻塞响应）
    import threading
    def auto_ai():
        time.sleep(0.5)  # 等数据库写入完成
        trigger_ai_analysis(capsule_id, capsule_type, content, url)
    
    threading.Thread(target=auto_ai).start()
    
    return jsonify({'success': True, 'id': capsule_id})
```

### 2. Bot 端自动 AI（echo-telegram.py）

```python
def create_capsule_from_message(text):
    # ... 创建种子 ...
    
    # 同步触发 AI 分析（Bot 可以等待）
    ai_reply = trigger_ai_analysis(capsule_id, capsule_type, content, url)
    
    # 回复用户
    reply = f"✅ 种子已创建\n{ai_reply}"
    return {'success': True, 'message': reply}
```

### 3. AI 分析核心（ai_service.py）

```python
def trigger_ai_analysis(capsule_id, capsule_type, content, url):
    """统一 AI 分析入口"""
    auto_tags = []
    is_todo = False
    calendar_info = None
    
    # 1. 链接分析
    if url:
        result = analyze_link(capsule_id, url)
        if result.get('success'):
            auto_tags.extend(result.get('suggested_tags', []))
    
    # 2. 点子扩张
    elif capsule_type == 'idea' or len(content) < 50:
        result = analyze_expansion(capsule_id, content)
        if result.get('success'):
            auto_tags.extend(result.get('suggested_tags', []))
            # 检查是否有待办建议
            if '行动建议' in result.get('expanded', {}):
                is_todo = True
    
    # 3. 智能关联
    find_relations(capsule_id)
    
    # 4. Todo 识别
    if capsule_type == 'todo' or is_todo:
        calendar_info = sync_to_calendar_if_needed(capsule_id, content)
    
    # 5. 更新种子标签
    if auto_tags:
        update_capsule_tags(capsule_id, auto_tags)
    
    return {
        'tags': auto_tags,
        'is_todo': is_todo,
        'calendar': calendar_info
    }
```

---

## 🎨 前端修改（index.html）

**删除 AI 分析面板，简化界面：**

```html
<!-- 删除整个右侧 AI 面板 -->
<!-- 删除 "🤖AI 面板" 按钮 -->
<!-- 删除 Vue AI App -->
```

**种子列表显示 AI 标签：**
```html
<!-- 种子卡片显示标签 -->
<span class="tags">{{ capsule.tags }}</span>
```

---

## 📊 数据库更新

```sql
-- 种子表增加 AI 相关字段
ALTER TABLE capsules ADD COLUMN ai_analyzed INTEGER DEFAULT 0;
ALTER TABLE capsules ADD COLUMN auto_tags TEXT;

-- 更新种子标签
UPDATE capsules SET tags = ? WHERE id = ?;
```

---

## ✅ 验收标准

| 功能 | 验收标准 | 状态 |
|------|---------|------|
| Web 创建 | 创建后自动 AI 分析，种子带标签 | ⏳ |
| Bot 创建 | 创建后回复 AI 分析摘要 | ⏳ |
| 自动标签 | AI 生成的标签显示在种子上 | ⏳ |
| Todo 同步 | Todo 类型自动同步到日历 | ⏳ |
| 无手动按钮 | 网页端无 AI 分析按钮 | ⏳ |

---

**请小爪审查此设计方案！**
