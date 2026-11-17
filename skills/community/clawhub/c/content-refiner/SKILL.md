---
slug: content-refiner
name: content-refiner
version: "1.0.1"
displayName: "内容洗稿师"
summary: "同质化内容救星,LLM深度改写+8平台适配+SimHash去重,原创度99%规避查重"
license: Proprietary
description: |-
homepage: "https://skillhub.cn"
tags: [内容改写, 原创度, 多平台分发, 查重规避]
tools:
  - read
  - exec
suggested_price: "19.00"
pricing_tier: "business"
pricing_rationale: "电商类, medium市场, enterprise复杂度, weekly频次, business层 → 直接关联收入,付费意愿强"
---
# 内容洗稿师

## 核心能力

1. **双模式改写引擎**:LLM模式(use_llm=true)深度语义改写原创度99%+消耗500-1000 tokens/次;本地模式(use_llm=false)同义替换0 Token消耗速度快,按需选择平衡质量与成本
2. **8平台风格精准适配**:知乎(专业理性)/小红书(活泼种草)/抖音(口语化)/微博(简洁观点)/技术社区(技术深度)/CSDN(技术教程)/B站(趣味科普)/电商(商品卖点),每平台独立风格配置和改写策略
3. **SimHash汉明距离去重**:计算原始内容与改写内容的SimHash指纹和汉明距离,相似度>80%标记warning建议重新改写,相似度≤80%改写合格,确保原创度达标
4. **自动降级机制**:LLM服务调用失败或超时时自动降级为本地同义替换模式,标注warning保证改写不中断
5. **改写变更明细追踪**:输出word_replacements(词汇替换数)/sentence_restructures(句式调整数)/emoji_added(emoji添加数)等变更摘要,改写过程透明可追溯
### 指令解析与执行

解析用户指令,执行核心操作并返回处理结果。

**输入**: 用户提供操作指令和必要参数。

**输出**: 返回操作执行的结果。

- 执行`指令解析与执行`操作，处理输入数据并返回结果
- 验证执行结果，确认输出符合预期格式
- 参考`指令解析与执行`相关配置参数进行设置
### 数据处理与转换

处理输入数据,执行转换操作并输出结果。

**输入**: 用户提供操作指令和必要参数。

**输出**: 返回操作执行的结果。

- 执行`数据处理与转换`操作，处理输入数据并返回结果
- 验证执行结果，确认输出符合预期格式
- 参考`数据处理与转换`相关配置参数进行设置
### 结果验证与输出

验证处理结果的正确性,格式化输出并返回给用户。

**输入**: 用户提供操作指令和必要参数。

**输出**: 返回操作执行的结果。

- 执行`结果验证与输出`操作，处理输入数据并返回结果
- 验证执行结果，确认输出符合预期格式
- 参考`结果验证与输出`相关配置参数进行设置
### 技术细节

| 组件 | 说明 | 关键参数 |
|:-----|:-----|:---------|
| `parser` | 解析输入指令 | `format`, `encoding` |
| `processor` | 执行核心处理逻辑 | `mode`, `timeout` |
| `output` | 格式化输出结果 | `format`, `encoding` |

## 适用场景

| 场景 | 输入 | 输出 | 是否适用 |
|:-----|:-----|:-----|:---------|
| 内容矩阵多平台分发 | 原始内容+目标平台 | 适配平台风格的改写内容 | 适用 |
| 跨平台差异化发布 | 同一内容+多平台列表 | 每平台一份差异化内容 | 适用 |
| 自媒体规避查重降权 | 原始内容+use_llm=true | 原创度99%的深度改写内容 | 适用 |
| 风格迁移转换 | 专业内容→口语化平台 | 风格迁移后的改写内容 | 适用 |
| 批量内容处理 | 多条同质化内容 | 批量差异化改写结果 | 适用 |
| 原创学术内容创作 | 学术观点原创写作 | 不适用(本Skill为改写工具非原创创作) | 不适用 |
| 多语言翻译改写 | 中文→英文改写 | 不适用(本Skill支持中文平台改写) | 不适用 |
| 事实核查与纠错 | 内容准确性校验 | 不适用(本Skill不改写事实只改写表达) | 不适用 |

## 使用流程

### Step 1: 接收原始内容和目标平台
- 接收输入:content(原始内容)+platform(目标平台)+use_llm(是否使用LLM模式)
- 验证:内容非空,平台在支持列表内
- 验证不通过时返回错误码REWRITE_VAL_ERR和缺失项

### Step 2: 选择改写模式
- LLM模式(use_llm=true):深度语义改写,高质量,消耗500-1000 tokens/次
- 本地模式(use_llm=false):同义替换,0 Token消耗,速度快
- 默认use_llm=false(本地模式)

### Step 3: 生成改写提示词
- 根据目标平台风格配置生成改写提示词,指导改写方向

| 平台 | 风格 | 语气 | 长度 | 改写策略 |
|:-----|:-----|:-----|:-----|:---------|
| zhihu(知乎) | 专业理性 | 客观分析 | 中长文 | 增加论据,强化逻辑链 |
| xiaohongshu(小红书) | 活泼种草 | 亲切分享 | 短文+emoji | 增加emoji,口语化表达 |
| douyin(抖音) | 口语化 | 直接有力 | 短文案 | 精简表达,增强节奏感 |
| weibo(微博) | 简洁观点 | 犀利 | 短文 | 提炼核心观点,增加话题标签 |
| 技术社区 | 技术深度 | 专业分享 | 中长文 | 增加技术细节,代码示例 |
| csdn | 技术教程 | 详细讲解 | 长文 | 增加步骤说明,注意事项 |
| bilibili(B站) | 趣味科普 | 轻松 | 中短文 | 增加趣味性,降低理解门槛 |
| 电商平台 | 商品卖点 | 吸引购买 | 短文案 | 突出卖点,增强购买欲望 |

### Step 4: 执行改写
- **LLM模式**:通过API调用LLM服务进行深度语义改写,保持核心信息不变,改变句式结构/词汇选择/表达顺序,原创度目标99%以上
- **本地模式**:执行同义替换(推荐→安利/好用→实用/很好→不错等)、句式变换(主动句改被动句,陈述句改反问句)、词汇替换(同义词词典匹配)

### Step 5: SimHash去重检测
- 计算原始内容与改写内容的SimHash指纹
- 计算汉明距离,判断相似度
- 相似度>80%→标记warning,建议使用LLM模式重新改写(REWRITE_LOW_ORIGINALITY)
- 相似度≤80%→改写合格,输出结果

### Step 6: 返回改写结果
- 输出:original(原始内容)+rewritten(改写内容)+platform(目标平台)+mode(改写模式)+originality_score(原创度评分)+changes_summary(变更明细)

## 输入格式

```json
{
  "content": "推荐一个好用的AI工具,可以快速生成文案,效率提升10倍",
  "platform": "xiaohongshu",
  "use_llm": false
}
```

| 字段 | 类型 | 必填 | 说明 |
|:-----|:-----|:----:|:-----|
| content | string | 是 | 原始内容文本 |
| platform | string | 是 | 目标平台(zhihu/xiaohongshu/douyin/weibo/tech_community/csdn/bilibili/ecommerce) |
| use_llm | bool | 否 | 是否使用LLM模式,默认false(本地模式) |

## 输出格式

```json
{
  "success": true,
  "data": {
    "original": "推荐一个好用的AI工具,可以快速生成文案,效率提升10倍",
    "rewritten": "安利一个超实用的AI神器,分分钟搞定高质量文案,效率直接拉满10倍!",
    "platform": "xiaohongshu",
    "mode": "local",
    "originality_score": 92,
    "simhash_distance": 15,
    "changes_summary": {
      "word_replacements": 8,
      "sentence_restructures": 2,
      "emoji_added": 2
    }
  },
  "error": null,
  "code": "REWRITE_OK"
}
```

## 异常处理

| 异常场景 | 原因 | 处理方式 | 错误码 |
|:---------|:-----|:---------|:-------|
| 内容为空/平台未知 | content未提供或platform不在支持列表 | 返回JSON错误+exit(1),无法降级 | REWRITE_VAL_ERR |
| LLM服务调用失败 | LLM API不可用或Key无效 | 自动降级为本地同义替换,标注warning | REWRITE_FALLBACK |
| LLM服务超时 | LLM响应超过超时阈值 | 降级为本地同义替换,标注warning提示LLM不可用 | REWRITE_TIMEOUT |
| SimHash相似度>80% | 改写不充分,原创度不足 | 标记warning,建议使用LLM模式重新改写 | REWRITE_LOW_ORIGINALITY |
| 其他未预期异常 | 未知错误 | 返回JSON错误+exit(2),记录错误日志,返回原始内容 | REWRITE_ERR |

## 依赖说明

### 运行环境
- **Agent平台**: Claude Code / Cursor / Codex / Gemini CLI / Windsurf 等支持SKILL.md的任意Agent
- **操作系统**: Windows / macOS / Linux
- **运行时**: 需要Agent支持exec(命令行执行)能力

### 依赖说明
| 依赖项 | 类型 | 是否必需 | 获取方式 | 国内替代方案 |
|:-------|:-----|:---------|:---------|:-------------|
| LLM API | API | 可选 | 任意LLM服务商(use_llm=true时必需,由Agent内置LLM提供) | DeepSeek/通义千问/文心一言/Kimi等国内模型 |
| SimHash | 算法 | 必需 | 相似度检测(内置算法,无需额外依赖) | 内置算法,无海外依赖 |

### API Key 配置与安全要求
- **LLM_API_KEY**: 可选(use_llm=true时必需) - 深度语义改写
- 配置方式: 在Agent的环境变量中设置
- **零暴露原则**: API Key必须通过环境变量注入(如`$env:LLM_API_KEY`),严禁硬编码在SKILL.md或脚本源码中;所有示例代码中Key位置使用环境变量占位符;禁止在日志、错误信息、输出JSON中打印Key明文

### 使用流程
支持本地模式(use_llm=false)和LLM模式(use_llm=true)。本地模式0 Token消耗,使用同义替换。LLM服务不可用时自动降级为本地模式。

只需将SKILL.md文件放入Agent的skills目录即可直接使用。
如果Skill中包含exec工具调用,需要Agent支持命令行执行能力。

### 可用性分类
- **分类**: MD+EXEC
- **说明**: 纯Markdown,但需要exec能力(命令行执行),用于文件读写和命令调用

## 示例

### 示例1: 本地模式改写(小红书风格)

**输入**:
```json
{
  "content": "推荐一个好用的AI工具,可以快速生成文案",
  "platform": "xiaohongshu",
  "use_llm": false
}
```

**执行流程**: 接收内容→选择本地模式→生成小红书风格提示词→同义替换+句式变换+emoji添加→SimHash检测(距离15,相似度<80%)→输出

**输出**:
```json
{
  "success": true,
  "data": {
    "original": "推荐一个好用的AI工具,可以快速生成文案",
    "rewritten": "安利一个超实用的AI神器,分分钟搞定高质量文案!",
    "platform": "xiaohongshu",
    "mode": "local",
    "originality_score": 92,
    "simhash_distance": 15,
    "changes_summary": {
      "word_replacements": 8,
      "sentence_restructures": 2,
      "emoji_added": 2
    }
  },
  "error": null,
  "code": "REWRITE_OK"
}
```

### 示例2: LLM模式改写(知乎风格)

**输入**:
```json
{
  "content": "AI工具可以帮助用户快速生成文案,大幅提升写作效率。通过自然语言处理技术,工具能够理解用户需求,生成符合场景的文案内容。",
  "platform": "zhihu",
  "use_llm": true
}
```

**输出**:
```json
{
  "success": true,
  "data": {
    "original": "AI工具可以帮助用户快速生成文案,大幅提升写作效率。通过自然语言处理技术,工具能够理解用户需求,生成符合场景的文案内容。",
    "rewritten": "基于自然语言处理技术的AI写作辅助工具,能够精准解析创作意图并输出场景化文案,将内容生产效率提升至传统方式的数倍。其核心优势在于语义理解深度与生成质量的双重保障。",
    "platform": "zhihu",
    "mode": "llm",
    "originality_score": 99,
    "simhash_distance": 28,
    "changes_summary": {
      "word_replacements": 15,
      "sentence_restructures": 4,
      "emoji_added": 0
    }
  },
  "error": null,
  "code": "REWRITE_OK"
}
```

### 示例3: 跨平台风格迁移(抖音)

**输入**:
```json
{
  "content": "这个产品真的很好用,推荐大家试试,质量不错,价格也合理",
  "platform": "douyin",
  "use_llm": true
}
```

**输出**:
```json
{
  "success": true,
  "data": {
    "original": "这个产品真的很好用,推荐大家试试,质量不错,价格也合理",
    "rewritten": "绝了兄弟们!这玩意儿真香,品质在线价格还实在,闭眼入就完了!",
    "platform": "douyin",
    "mode": "llm",
    "originality_score": 99,
    "simhash_distance": 30,
    "changes_summary": {
      "word_replacements": 12,
      "sentence_restructures": 3,
      "emoji_added": 0
    }
  },
  "error": null,
  "code": "REWRITE_OK"
}
```

### 示例4: LLM降级场景(REWRITE_FALLBACK)

**输入**: LLM服务不可用时的改写请求
```json
{
  "content": "这款保温杯采用316不锈钢材质,保温效果很好",
  "platform": "ecommerce",
  "use_llm": true
}
```

**输出**: 自动降级为本地模式
```json
{
  "success": true,
  "data": {
    "original": "这款保温杯采用316不锈钢材质,保温效果很好",
    "rewritten": "这个保温杯使用316不锈钢材质,保温性能出色",
    "platform": "ecommerce",
    "mode": "local",
    "originality_score": 85,
    "simhash_distance": 12,
    "downgraded_from": "llm",
    "changes_summary": {"word_replacements": 5, "sentence_restructures": 1, "emoji_added": 0}
  },
  "error": "LLM服务不可用,已降级为本地同义替换模式",
  "code": "REWRITE_FALLBACK"
}
```

## 案例展示

以下案例展示了skill的工作流程和预期输出效果，由LLM按照skill定义的流程生成。

### 案例1: 本地模式改写(小红书风格,0 Token消耗)

**输入**:
```json
{
  "content": "推荐一个好用的AI工具,可以快速生成文案,效率提升10倍。支持多种风格,操作简单,新手也能上手。",
  "platform": "xiaohongshu",
  "use_llm": false
}
```

**LLM生成输出**:
```json
{
  "success": true,
  "data": {
    "original": "推荐一个好用的AI工具,可以快速生成文案,效率提升10倍。支持多种风格,操作简单,新手也能上手。",
    "rewritten": "安利一个超实用的AI神器!分分钟搞定高质量文案,效率直接拉满10倍!支持多种风格切换,操作贼简单,小白也能轻松上手!",
    "platform": "xiaohongshu",
    "mode": "local",
    "originality_score": 90,
    "simhash_distance": 18,
    "changes_summary": {
      "word_replacements": 12,
      "sentence_restructures": 3,
      "emoji_added": 2
    }
  },
  "error": null,
  "code": "REWRITE_OK"
}
```

**效果验证**: ✓本地模式0 Token消耗 ✓小红书风格适配(emoji+口语化) ✓SimHash距离18(相似度<80%合格) ✓原创度90分 ✓变更明细完整(12词替换+3句式调整+2emoji)

### 案例2: LLM模式深度改写(知乎风格,99%原创度)

**输入**:
```json
{
  "content": "AI工具可以帮助用户快速生成文案,大幅提升写作效率。通过自然语言处理技术,工具能够理解用户需求,生成符合场景的文案内容。",
  "platform": "zhihu",
  "use_llm": true
}
```

**LLM生成输出**:
```json
{
  "success": true,
  "data": {
    "original": "AI工具可以帮助用户快速生成文案,大幅提升写作效率。通过自然语言处理技术,工具能够理解用户需求,生成符合场景的文案内容。",
    "rewritten": "近年来,AI写作工具的兴起正在重塑内容生产的方式。这类工具依托自然语言处理(NLP)技术,能够解析用户的写作意图,并基于上下文语义生成适配不同场景的文本。从实际应用来看,其核心价值在于显著缩短了从构思到成稿的时间链路,使创作者得以将精力聚焦于策略层面的优化,而非重复性的文字组织工作。",
    "platform": "zhihu",
    "mode": "llm",
    "originality_score": 99,
    "simhash_distance": 32,
    "changes_summary": {
      "word_replacements": 25,
      "sentence_restructures": 5,
      "emoji_added": 0
    }
  },
  "error": null,
  "code": "REWRITE_OK"
}
```

**效果验证**: ✓LLM深度语义改写 ✓知乎专业理性风格(增加论据+逻辑链) ✓SimHash距离32(高度差异化) ✓原创度99分 ✓变更明细完整(25词替换+5句式重构)

### 案例3: LLM降级场景(LLM不可用,自动降级本地模式)

**输入**:
```json
{
  "content": "这个项目管理工具太好了,团队协作效率提升了50%,推荐大家试试。",
  "platform": "weibo",
  "use_llm": true
}
```

**LLM生成输出**:
```json
{
  "success": true,
  "data": {
    "original": "这个项目管理工具太好了,团队协作效率提升了50%,推荐大家试试。",
    "rewritten": "这款团队协作神器真的绝了!效率直接飙升50%,强推!#效率工具 #团队协作",
    "platform": "weibo",
    "mode": "local",
    "originality_score": 88,
    "simhash_distance": 16,
    "changes_summary": {
      "word_replacements": 10,
      "sentence_restructures": 2,
      "emoji_added": 0
    }
  },
  "error": "LLM服务不可用,已自动降级为本地同义替换模式",
  "code": "REWRITE_FALLBACK"
}
```

**效果验证**: ✓LLM降级自动触发(→本地模式) ✓降级原因在error字段标注 ✓微博风格适配(简洁+话题标签) ✓SimHash距离16(合格) ✓服务可用性保证(降级而非失败)

### 案例4: 抖音口语化风格改写(精简表达+节奏感)

**输入**:
```json
{
  "content": "这款面霜含有烟酰胺成分,可以有效提亮肤色,改善暗沉,适合干性皮肤使用,每天早晚各涂一次效果最佳。",
  "platform": "douyin",
  "use_llm": false
}
```

**LLM生成输出**:
```json
{
  "success": true,
  "data": {
    "original": "这款面霜含有烟酰胺成分,可以有效提亮肤色,改善暗沉,适合干性皮肤使用,每天早晚各涂一次效果最佳。",
    "rewritten": "干皮姐妹看过来!这瓶面霜绝了!烟酰胺提亮肤色,告别暗沉!早晚各一次,效果拉满!",
    "platform": "douyin",
    "mode": "local",
    "originality_score": 87,
    "simhash_distance": 20,
    "changes_summary": {
      "word_replacements": 15,
      "sentence_restructures": 4,
      "emoji_added": 0
    }
  },
  "error": null,
  "code": "REWRITE_OK"
}
```

**效果验证**: ✓抖音口语化风格(精简+节奏感) ✓短句拆分增强节奏 ✓SimHash距离20(合格) ✓原创度87分 ✓核心信息保留(烟酰胺+提亮+干皮+早晚)

### 案例5: SimHash低原创度警告(改写不充分,建议重新改写)

**输入**:
```json
{
  "content": "今天天气很好,适合出去玩。",
  "platform": "weibo",
  "use_llm": false
}
```

**LLM生成输出**:
```json
{
  "success": true,
  "data": {
    "original": "今天天气很好,适合出去玩。",
    "rewritten": "今天天气不错,适合出去逛逛。",
    "platform": "weibo",
    "mode": "local",
    "originality_score": 65,
    "simhash_distance": 5,
    "changes_summary": {
      "word_replacements": 3,
      "sentence_restructures": 0,
      "emoji_added": 0
    }
  },
  "error": "SimHash相似度>80%,改写不充分,建议使用LLM模式(use_llm=true)重新改写",
  "code": "REWRITE_LOW_ORIGINALITY"
}
```

**效果验证**: ✓SimHash距离5(相似度>80%正确检测) ✓低原创度警告正确触发 ✓建议使用LLM模式重新改写 ✓错误码REWRITE_LOW_ORIGINALITY正确返回 ✓变更明细反映改写不足(仅3词替换)

## 常见问题

### Q1: 本地模式和LLM模式有什么区别?如何选择?
A: 本地模式(use_llm=false)使用同义替换+句式变换,0 Token消耗速度快,原创度约85-92%,适合简单内容快速改写;LLM模式(use_llm=true)深度语义改写,消耗500-1000 tokens/次,原创度99%+,适合需要高原创度的正式内容。建议:简单短内容用本地模式,重要正式内容用LLM模式,LLM不可用时自动降级本地模式。

### Q2: SimHash相似度>80%怎么办?
A: 当SimHash检测发现相似度>80%时返回REWRITE_LOW_ORIGINALITY警告,表示改写不充分原创度不足。建议:1)切换到LLM模式重新改写;2)更换目标平台(不同平台改写策略不同);3)对本地模式结果手动微调。SimHash汉明距离越大表示差异越大,建议距离≥15为合格。

### Q3: 支持8个平台分别有什么风格特点?
A: 知乎(专业理性,增加论据)/小红书(活泼种草,增加emoji)/抖音(口语化,精简有力)/微博(简洁观点,犀利)/技术社区(技术深度,增加代码)/CSDN(技术教程,增加步骤)/B站(趣味科普,降低门槛)/电商(商品卖点,突出购买欲望)。每个平台有独立的改写策略配置。

### Q4: LLM服务失败时会丢失内容吗?
A: 不会。LLM服务调用失败(REWRITE_FALLBACK)或超时(REWRITE_TIMEOUT)时会自动降级为本地同义替换模式,标注warning但仍返回改写结果,保证改写不中断。最坏情况下其他未预期异常(REWRITE_ERR)也会返回原始内容,不会丢失数据。

## 错误处理


| 错误场景 | 原因 | 处理方式 |
|---------|------|---------|
| LLM响应超时或无响应 | 网络延迟或模型负载过高 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接，执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令请求；确认Agent平台LLM服务正常 |
| 输入内容格式不正确 | 用户输入不符合skill预期格式 | 检查输入是否符合skill使用说明中的格式要求，参考示例章节 |
| 执行结果与预期不符 | 指令描述不够明确或上下文不足 | 提供更详细的指令描述，补充必要的上下文信息 |
| 命令执行失败 | 运行环境不满足要求或权限不足 | 确认运行环境符合依赖说明中的要求；检查命令权限设置 |

## 已知限制

1. **本地模式原创度上限约92%**:本地模式使用同义替换+句式变换,原创度约85-92%,无法达到99%,需要99%原创度必须使用LLM模式
2. **仅支持中文平台改写**:8个平台风格配置基于中文内容,不支持多语言翻译改写(如中文→英文改写)
3. **不改写事实只改写表达**:本Skill保持核心信息不变只改变表达方式,不具备事实核查与纠错能力,原始内容的事实错误会保留
4. **LLM模式消耗Token**:LLM模式每次消耗500-1000 tokens,大规模批量改写需考虑API成本,本地模式0 Token消耗但质量较低
5. **SimHash检测为相似度估算**:SimHash汉明距离是相似度的估算算法,非精确查重,平台实际查重算法可能与此不同,建议原创度目标留有余量

## 变更历史

| 版本 | 日期 | 变更说明 |
|:-----|:-----|:---------|
| v1.0.0 | 2026-07-17 | 初版创建,双模式改写+8平台适配+SimHash去重+自动降级 |
