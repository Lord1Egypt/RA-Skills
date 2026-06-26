---
name: contextStable
description: 长小说文章上下文稳定输出续写
author: YBs
version: 0.0.1
tags:
  - 长文本处理
  - 上下文一致性
  - 小说续写
  - 多轮对话
  - 智能提示词生成
requires:
  - sentence-transformers
  - numpy
  - scikit-learn
  - python>=3.8
usage:
  - 小说/故事续写
  - 长文档生成
  - 多轮对话场景
  - 角色设定保持
  - 世界观一致性维护
---
# Context Stabilizer Skill

## 技能名称
Context Stabilizer（长文本上下文稳定器）

## 技能描述
用于稳定长文本生成的上下文一致性，自动提取核心设定并确保生成内容符合设定。

## 功能特点
- **自动锚点提取**：从文本中自动提取人设、世界观、核心剧情、文风等核心设定
- **增强提示词生成**：智能组合相关上下文和锚点，生成更准确的提示词
- **一致性检查**：分维度检查生成内容的一致性（人设/剧情/文风/世界观）
- **历史记录管理**：追踪多轮对话历史，支持角色状态和剧情时间线管理
- **滑动窗口管理**：智能处理超长文本，支持重要片段标记
- **缓存机制**：提高嵌入向量计算效率

## 适用场景
- 小说/故事续写
- 长文档生成
- 多轮对话场景
- 角色设定保持
- 世界观一致性维护

## 安装依赖
```bash
pip install -r requirements.txt
```

## 基本使用
```python
from context_stabilizer import LongTextContextStabilizer

# 初始化
stabilizer = LongTextContextStabilizer()

# 添加长文本（自动提取锚点）
long_text = "你的长文本内容..."
stabilizer.init_long_text(long_text, auto_extract=True)

# 生成增强提示词
user_prompt = "你的续写需求..."
enhanced_prompt = stabilizer.get_enhanced_prompt(user_prompt)

# 检查一致性
llm_output = "LLM生成的内容..."
check_result = stabilizer.check_consistency(llm_output, detailed=True)

# 记录历史
stabilizer.record_generation(user_prompt, enhanced_prompt, llm_output, check_result)
```

## 高级用法
### 自定义配置
```python
from context_stabilizer.config import ContextConfig, ConsistencyConfig

custom_config = ContextConfig(
    consistency=ConsistencyConfig(threshold=0.75),
    history=ContextConfig.__annotations__['history'].__args__[0](
        max_history=200, auto_save=True
    )
)
stabilizer = LongTextContextStabilizer(custom_config)
```

### 手动设置锚点
```python
manual_anchors = {
    "人设": "角色设定...",
    "世界观": "世界观设定...",
    "核心剧情": "剧情设定...",
    "文风": "文风设定..."
}
stabilizer.init_long_text(long_text, manual_anchors=manual_anchors, auto_extract=False)
```

### 标记重要片段
```python
stabilizer.mark_important_segment(
    content="重要内容...",
    reason="重要原因...",
    importance=2.0
)
```

### 保存和加载会话
```python
stabilizer.save_session("session_name")
stabilizer.load_session("session_name")
```

## 输出示例
### 增强提示词
```
请根据以下需求和上下文，续写/创作文本，严格遵守核心设定，保持文风一致：

【用户需求】
续写第三章，李逍遥和赵灵儿在破庙休息时遭遇拜月教小喽啰袭击

【相关上下文】
第一章 初入江湖
李逍遥，18岁，性格洒脱，嫉恶如仇，手持一把生锈的铁剑，从小在余杭镇长大。
这天，他离开家乡，准备前往苏州城，寻找失散多年的婶婶。

第二章 偶遇灵儿
在去苏州的路上，李逍遥遇到了一位名叫赵灵儿的少女，她温柔善良，身负女娲族的血脉，正被拜月教追杀。
李逍遥出手相救，两人结伴同行。

【核心设定】
人设：李逍遥：18岁，洒脱，嫉恶如仇；赵灵儿：温柔善良，女娲族血脉
世界观：古风武侠仙侠世界
核心剧情：李逍遥寻找婶婶，偶遇赵灵儿，结伴前往苏州城
文风：古风武侠，语言简洁，情感细腻

要求：1. 剧情连贯，不偏离核心设定；2. 人设统一，无矛盾；3. 文风与前文一致。
```

### 一致性检查结果
```
总体一致性: ✓ 通过
发现问题数: 0

各维度评分:
  character: 1.00
  plot: 1.00
  style: 0.90
  world: 1.00

改进建议:
无
```

## 技术原理
1. **文本分块**：将长文本分割成适当大小的块
2. **锚点提取**：自动识别和提取核心设定
3. **上下文检索**：基于关键词匹配或向量相似度检索相关上下文
4. **一致性检查**：分维度评估生成内容与设定的一致性
5. **历史管理**：追踪生成历史，支持多轮对话

## 注意事项
- 首次运行时会自动下载 sentence-transformers 模型（需要网络连接）
- 对于超长文本，滑动窗口会自动管理上下文大小
- 可通过配置调整分块大小、一致性阈值等参数
- 支持导出故事为 txt 或 json 格式
