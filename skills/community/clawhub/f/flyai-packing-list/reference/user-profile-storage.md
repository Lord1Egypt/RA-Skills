# 用户画像存储规范（双模式）

本文档定义了 flyai-* 技能中用户旅行画像的**跨平台存储方案**，支持 Qoder Memory 和本地文件双模式。

---

## 存储模式优先级

```
1. 优先尝试 Qoder Memory（search_memory / update_memory）
2. 如果不可用或无结果，降级使用本地文件
3. 两种模式的数据格式保持一致
```

---

## 模式判断逻辑

### 如何判断是否是 Qoder 环境

**Qoder 环境特征：**
- 具有 `search_memory` 和 `update_memory` 内置工具
- 可以直接调用这些工具而不会报错

**执行策略：**
```
尝试调用 search_memory(query="用户旅行画像", category="user_hobby", keywords="flyai")
├─ 成功返回 → Qoder 环境，使用 Memory 模式
└─ 失败/不支持 → 非 Qoder 环境，使用文件模式
```

> 在 SKILL.md 中，我们通过**描述两种路径**来实现降级，AI 会根据实际环境选择可用的方式。

---

## 模式 A：Qoder Memory

### 读取

```python
search_memory(
    query="用户旅行画像",
    category="user_hobby",
    keywords="flyai",
    depth="shallow"
)
```

### 写入

```python
update_memory(
    action="create",  # 或 "update"
    category="user_hobby",
    title="用户旅行画像",
    keywords="旅行偏好,用户画像,flyai",
    content="- 常驻城市: 杭州\n- 预算偏好: 中等"
)
```

---

## 模式 B：本地文件

### 文件路径

```
~/.flyai/user-profile.md
```

如果 `~/.flyai/` 目录不存在，需要先创建：
```bash
mkdir -p ~/.flyai
```

### 文件格式

```markdown
# FlyAI 用户旅行画像

> 最后更新: 2026-04-03 15:30

## 基础信息
- 常驻城市: 杭州
- 出发机场: 萧山机场

## 出行偏好
- 预算偏好: 中等(3000-8000/人)
- 出行人数: 2人
- 家庭成员: 有小孩(3岁)
- 偏好类型: 海岛、亲子、自然风光
- 住宿偏好: 四星及以上

## 历史记录
- 去过城市: 三亚、厦门、大理

## 特殊需求
- 宠物友好: 否
- 无障碍: 否
```

### 读取文件

```bash
cat ~/.flyai/user-profile.md
```

或使用工具：
```
read_file(file_path="~/.flyai/user-profile.md")
```

### 写入/更新文件

使用文件写入工具更新内容，记得更新"最后更新"时间戳。

---

## 统一数据字段

无论使用哪种模式，数据字段保持一致：

| 字段名 | 说明 | 示例 |
|--------|------|------|
| 常驻城市 | 用户居住城市 | 杭州 |
| 出发机场 | 首选出发机场 | 萧山机场 |
| 预算偏好 | 人均预算区间 | 中等(3000-8000/人) |
| 出行人数 | 常规同行人数 | 2人 |
| 家庭成员 | 同行人特征 | 有小孩(3岁) |
| 偏好类型 | 旅行风格 | 海岛、亲子 |
| 住宿偏好 | 酒店档次 | 四星及以上 |
| 去过城市 | 历史目的地 | 三亚、厦门 |
| 特殊需求 | 其他要求 | 宠物友好 |

---

## SKILL.md 中的写法模板

```markdown
## 启动时读取用户画像（双模式）

### 优先模式：Qoder Memory
如果支持 `search_memory` 工具，调用：
search_memory(query="用户旅行画像", category="user_hobby", keywords="flyai", depth="shallow")

### 降级模式：本地文件
如果上述工具不可用，读取本地文件：
read_file(file_path="~/.flyai/user-profile.md")

### 无画像时
如果两种方式都无结果，直接询问用户关键信息。

---

## 发现新偏好时保存（双模式）

当用户表达新偏好（如"我住杭州"、"预算3000左右"）时：

1. 提示用户确认保存：
   💡 发现新偏好：「{字段}: {值}」
   [保存到画像] [仅本次使用]

2. 用户确认后：
   - Qoder 环境：调用 update_memory 更新
   - 非 Qoder：更新 ~/.flyai/user-profile.md 文件
```

---

## 平台兼容性

| 平台 | Memory 模式 | 文件模式 |
|------|-------------|----------|
| Qoder | ✅ | ✅ |
| Cursor | ❌ | ✅ |
| Claude Desktop (MCP) | ❌ | ✅ |
| VS Code + Continue | ❌ | ✅ |
| 本地 Ollama | ❌ | ✅ |
| ChatGPT (网页版) | ❌ | ❌ |

---

## 版本记录

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.0.0 | 2026-04-03 | 初始版本，定义双模式存储规范 |
