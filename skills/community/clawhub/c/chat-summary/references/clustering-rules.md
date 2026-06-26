# 话题聚类规则

## 切换话题的信号

### 明确切换
- "换个话题"
- "对了，..."
- "另外，..."
- "回到之前说的..."

### 隐式切换
- 关键词相似度 <30%
- 时间间隔 >5 分钟
- 问题类型变化（如 技术→生活）

## 聚类算法

```python
def calculate_similarity(msg1, msg2):
    """计算两条消息的语义相似度"""
    # 1. 提取关键词
    # 2. 计算 Jaccard 相似度
    # 3. 考虑时间因素
    pass

def detect_topic_boundary(messages, threshold=0.3):
    """检测话题边界"""
    boundaries = []
    for i in range(1, len(messages)):
        sim = calculate_similarity(messages[i-1], messages[i])
        if sim < threshold:
            boundaries.append(i)
    return boundaries
```

## 话题命名规则

- 长度：<20 字
- 格式：`【主题】+ 核心内容`
- 示例：
  - 【技术】Whisper.cpp 配置
  - 【生活】埃及旅行计划
  - 【工作】每日笔记自动化

## 摘要生成规则

| 元素 | 要求 |
|------|------|
| 标题 | <20 字，包含关键词 |
| 摘要 | <200 字，包含结论/数据 |
| 关键数据 | 数字/日期/决定 |
| 相关链接 | URL/文件路径 |

## 特殊情况处理

### 多话题混合
当一条消息涉及多个话题时：
1. 归入主要话题
2. 或在两个话题中都引用

### 无明确结论
标记为"待讨论"或"进行中"

### 敏感内容
跳过或标记为"[已省略]"
