name: checktruth
description: |
  验证内容是否属实。支持两种模式：
  【模式A：问答验证】验证AI回答是否正确
  【模式B：文章/论点验证】验证文章、帖子、论点是否属实
  触发词：英文 /checktruth，中文 /别瞎说
  触发后自动判断输入格式，选择模式A或模式B。
  核心功能：多视角交叉验证（零配置）
metadata:
  openclaw:
    emoji: '🔍'
    requires: {}
  security:
    credentials_usage: |
      ✅ CORE FUNCTIONALITY: ZERO CONFIG, NO EXTERNAL API KEYS REQUIRED.
      
      This skill's core fact-checking functionality is implemented entirely through
      the instructions in SKILL.md, using ONLY:
        - WorkBuddy's built-in LLM capabilities
        - WebSearch tool (for reference information retrieval)
      
      NO external API keys (OpenAI, Anthropic, Gemini, etc.) are needed
      for the core functionality.
      
      ⚠️ OPTIONAL REFERENCE CODE:
      
      The `reference/` folder contains optional Python scripts that DO require
      external LLM API keys (GLM, DeepSeek, Hunyuan, Kimi, MiniMax). These scripts are:
        - NOT required for core functionality
        - NOT loaded or executed by default
        - ONLY for developers who want to extend the skill
        - Clearly documented as requiring external API keys
      
      Normal users should IGNORE the `reference/` folder.
      
      🔒 DATA HANDLING:
      
      For core functionality:
        - User text is processed ONLY by WorkBuddy's built-in LLM
        - WebSearch queries may be sent to search engines (google.com, bing.com, etc.)
        - NO user text is sent to third-party LLM providers
      
      For reference/ code (optional, requires explicit key configuration):
        - User text MAY be sent to configured LLM providers
        - Users MUST provide their own API keys
        - Users are responsible for reviewing provider data policies
    allowed_domains:
      # These domains are for WebSearch reference retrieval ONLY
      # Core functionality does NOT send user text to these domains
      - google.com
      - bing.com
      - baidu.com
      - zhihu.com
      - wikipedia.org
      - gov.cn
      - xueqiu.com
      - caixin.com
    data_handling: |
      Core functionality:
        - User questions and text are processed locally by WorkBuddy's built-in LLM
        - Reference information is retrieved via WebSearch (search engine queries only)
        - NO user text is transmitted to third-party LLM providers
        - NO external API keys are required or used
      
      Optional reference/ code (requires user-provided API keys):
        - User text may be sent to third-party LLM providers (GLM, DeepSeek, Hunyuan, Kimi, MiniMax)
        - API keys are provided by the user, not stored or managed by this skill
        - Users must review each provider's data handling policies
        - This is OPTIONAL and NOT enabled by default
    external_dependencies: |
      Core functionality: NONE (zero external dependencies)
      
      Optional reference/ code:
        - openai (requires OPENAI_API_KEY or LLM_API_KEY)
        - anthropic (requires ANTHROPIC_API_KEY)
        - google.generativeai (requires GEMINI_API_KEY or GOOGLE_API_KEY)
        - zhipuai (requires ZHIPUAI_API_KEY)
        - dashscope (requires DASHSCOPE_API_KEY)
      
      These are NOT loaded or used unless the user explicitly configures them.
---
# checktruth（别瞎说）🔍

验证内容是否属实。**多视角交叉验证**，模拟多模型效果，给出可信度评分。

**核心特性：零配置 + 多视角验证**
- 无需任何外部 API Key
- 通过 3 轮不同视角验证，模拟多模型交叉验证效果
- 可选：通过 `reference/` 脚本调用真正的多模型 API（需自行配置 Key）

---

## 触发方式

本 Skill 通过以下触发词启动：

| 语言 | 触发词 | 说明 |
|------|--------|------|
| 英文 | `/checktruth <内容>` | 自动判断模式A或模式B |
| 中文 | `/别瞎说 <内容>` | 自动判断模式A或模式B |

**触发后自动判断模式**：
- 如果输入包含 `问题：` + `回答：` 结构 → 模式A（问答验证）
- 如果输入是连续文本，无明确 Q&A 结构 → 模式B（文章/论点验证）

---

## 模式A：问答验证

验证「问题 + 回答」中的回答是否正确。

### 输入格式
```
问题：<question>
回答：<answer>
```

（触发词后直接粘贴以上内容，无需单独声明模式A）

---

## 模式B：文章/论点验证

验证一段文章、帖子、论点中的事实陈述是否属实。

### 输入格式
直接粘贴文章内容或论点文本，无需 question/answer 结构。

（触发词后直接粘贴文本内容，无需单独声明模式B）

---

## 执行流程（两种模式通用）

按以下步骤执行验证，**每一步都用中文输出进度**。

### Step 1：获取参考信息

使用 WebSearch 或 WebFetch 搜索相关内容，获取 2-3 个权威参考来源。
记录参考来源的核心信息作为验证依据。

> **优先搜索的方向**：涉及人物/公司/事件时，优先搜索官方资料、政府网站(gov.cn)、权威媒体。

---

### Step 2：原子事实分解

将待验证内容分解为独立的原子事实列表。每个事实必须是一个可以被独立验证的陈述句。

输出格式：
```
【原子事实分解】
1. <事实1>
2. <事实2>
...
```

---

### Step 3：多视角交叉验证（核心）

**这是本 Skill 的核心创新**：通过 3 轮不同视角的验证，模拟多模型交叉验证的效果。

#### 视角 1：严谨核查员（模拟 GLM 风格）

以「严谨事实核查员」的视角，对照 Step 1 获取的参考信息，对每个原子事实进行验证。

**角色设定**：
- 严谨、保守，只认有来源支撑的事实
- 对数字、日期、名称格外敏感
- 无来源支撑的陈述一律判「无法验证」

输出格式：
```
【视角 1：严谨核查员】
事实 1：<事实内容>
判定：✅ 正确 / ❌ 错误 / ⚠️ 无法验证
置信度：<0-100%>
依据：<简短说明，引用具体来源>
```

#### 视角 2：质疑者（模拟 DeepSeek 风格）

以「主动质疑者」的视角，重新审视每个事实，**主动寻找反例或矛盾**。

**角色设定**：
- 质疑精神，主动寻找反例
- 关注事实之间的逻辑一致性
- 如果发现视角 1 的判定有问题，明确指出

输出格式：
```
【视角 2：质疑者】
事实 1：<事实内容>
对视角1判定的质疑：<同意/不同意，理由>
补充验证：<新的发现或反例>
置信度调整：<上调/下调/维持> 至 <X%>
```

#### 视角 3：综合裁判（模拟混元风格）

综合视角 1 和视角 2 的结果，**给出最终判定**。

**角色设定**：
- 综合双方意见，给出平衡的最终判断
- 如果有分歧，说明采纳哪方及理由
- 输出最终的可信度评分

输出格式：
```
【视角 3：综合裁判】
事实 1：<事实内容>
最终判定：✅ 正确 / ❌ 错误 / ⚠️ 无法验证
最终置信度：<0-100%>
判定理由：<综合视角1和视角2的理由>
```

---

### Step 4：内部一致性检测

检查待验证内容本身是否存在自相矛盾（前后说法冲突、数字不一致等）。

---

### Step 5：综合评分

根据视角 3 的最终判定结果计算总分：

- 正确事实：+100分 × 最终置信度
- 错误事实：+0分
- 无法验证：+50分 × 最终置信度
- 内部矛盾：总分 × 0.8 扣分

最终输出格式：

```
🔍 验证结果：<正确/部分正确/错误/无法判断>（<总分>分）

✅ 正确的事实：
  • <事实>（置信度：XX%）
    依据：<来源>

❌ 错误的事实：
  • <事实>（置信度：XX%）
    正确应为：<更正>
    依据：<来源>

⚠️ 无法验证：
  • <事实>（原因：<原因>）

📊 多视角验证摘要：
  • 视角1（严谨核查员）：<简要点评>
  • 视角2（质疑者）：<简要点评>
  • 视角3（综合裁判）：<简要点评>

📊 一致性检测：<通过/发现矛盾>
📚 参考来源：<来源列表>
```

---

## 规则

1. **不知道就说不知道**：无法验证的内容判「无法验证」，不随意打分
2. **引用来源**：每个判定必须有依据，尽量引用具体来源URL或名称
3. **中文输出**：所有输出使用中文
4. **先搜索再判断**：优先通过 WebSearch/WebFetch 获取参考信息，不要只依赖自身知识
5. **标注置信度**：每个判定标注置信度（0-100%），表示判断的可靠程度
6. **区分事实与观点**：观点/主观判断（如"好不好"、"值不值"）标注为「观点，无法验证」，不参与评分
7. **多视角必须执行**：Step 3 的 3 个视角（核查员 → 质疑者 → 综合裁判）必须全部执行，不能跳过

---

## 示例

### 示例1：问答验证（模式A）

**用户输入（中文）：**
```
/别瞎说
问题：魏建军是谁？
回答：魏建军是长城汽车创始人，1964年出生，现任董事长，持有公司56%股份。
```

**输出：**
```
【原子事实分解】
1. 魏建军是长城汽车创始人
2. 魏建军1964年出生
3. 魏建军现任董事长
4. 魏建军持有公司56%股份

【视角 1：严谨核查员】
事实 1：魏建军是长城汽车创始人
判定：✅ 正确
置信度：90%
依据：长城汽车官网及公开资料一致确认

事实 2：魏建军1964年出生
判定：✅ 正确
置信度：85%
依据：公开履历信息

事实 3：魏建军现任董事长
判定：✅ 正确
置信度：95%
依据：长城汽车2023年报

事实 4：魏建军持有公司56%股份
判定：❌ 错误
置信度：88%
依据：长城汽车2023年报显示魏建军持股比例约30%，非56%

【视角 2：质疑者】
事实 1：魏建军是长城汽车创始人
对视角1判定的质疑：同意。补充：魏建军是1986年接手长城工业公司，1990年正式担任厂长，后发展为长城汽车。
补充验证：无反例。
置信度调整：维持 90%

事实 4：魏建军持有公司56%股份
对视角1判定的质疑：同意。实际持股比例约30%（2023年报），56%可能是混淆了投票权与持股比例。
补充验证：无反例。
置信度调整：维持 88%

【视角 3：综合裁判】
事实 1：魏建军是长城汽车创始人
最终判定：✅ 正确
最终置信度：90%
判定理由：视角1和视角2均确认，来源可靠。

事实 4：魏建军持有公司56%股份
最终判定：❌ 错误
最终置信度：88%
判定理由：视角1和视角2均确认错误，正确持股比例约30%。

🔍 验证结果：部分正确（70分）

✅ 正确的事实：
  • 魏建军是长城汽车创始人（置信度：90%）
  • 魏建军1964年出生（置信度：85%）
  • 魏建军现任董事长（置信度：95%）

❌ 错误的事实：
  • 魏建军持有公司56%股份（置信度：88%）
    正确应为：约30%（2023年财报数据）

📊 多视角验证摘要：
  • 视角1（严谨核查员）：发现持股比例错误
  • 视角2（质疑者）：确认错误，补充了投票权与持股比例的区分
  • 视角3（综合裁判）：综合双方意见，维持错误判定

📊 一致性检测：通过
📚 参考来源：Wikipedia、长城汽车2023年报、新浪财经
```

### 示例2：文章/论点验证（模式B）

**用户输入（中文）：**
```
/别瞎说
比亚迪2024年销量400万辆，已经超过特斯拉成为全球第一，
王传福是比亚迪创始人，公司成立于1995年，总部在深圳。
```

**输出：**
```
【原子事实分解】
1. 比亚迪2024年销量400万辆
2. 比亚迪已经超过特斯拉成为全球第一
3. 王传福是比亚迪创始人
4. 比亚迪公司成立于1995年
5. 比亚迪总部在深圳

【视角 1：严谨核查员】
事实 1：比亚迪2024年销量400万辆
判定：✅ 正确
置信度：92%
依据：比亚迪2024年年报披露销量约395万辆，400万为近似值

事实 2：比亚迪已经超过特斯拉成为全球第一
判定：⚠️ 无法验证
置信度：—%
依据：需明确比较维度（销量/市值/净利润），不同维度结果不同

事实 3：王传福是比亚迪创始人
判定：✅ 正确
置信度：98%
依据：比亚迪官网及公开资料一致确认

事实 4：比亚迪公司成立于1995年
判定：✅ 正确
置信度：95%
依据：比亚迪官方公司简介

事实 5：比亚迪总部在深圳
判定：✅ 正确
置信度：99%
依据：公开资料一致确认

【视角 2：质疑者】
事实 2：比亚迪已经超过特斯拉成为全球第一
对视角1判定的质疑：同意「无法验证」的判定。
补充验证：若按销量维度，比亚迪2024年销量确实超过特斯拉；但若按市值或净利润，结果可能不同。原陈述未明确维度，应判「无法验证」。
置信度调整：维持「无法验证」

【视角 3：综合裁判】
事实 1：比亚迪2024年销量400万辆
最终判定：✅ 正确
最终置信度：92%
判定理由：视角1和视角2均确认，年报数据支撑。

事实 2：比亚迪已经超过特斯拉成为全球第一
最终判定：⚠️ 无法验证
最终置信度：—%
判定理由：原陈述未明确比较维度，无法给出单一判断。

事实 3：王传福是比亚迪创始人
最终判定：✅ 正确
最终置信度：98%

事实 4：比亚迪公司成立于1995年
最终判定：✅ 正确
最终置信度：95%

事实 5：比亚迪总部在深圳
最终判定：✅ 正确
最终置信度：99%

🔍 验证结果：部分正确（82分）

✅ 正确的事实：
  • 比亚迪2024年销量400万辆（置信度：92%）
  • 王传福是比亚迪创始人（置信度：98%）
  • 比亚迪公司成立于1995年（置信度：95%）
  • 比亚迪总部在深圳（置信度：99%）

⚠️ 无法验证：
  • 比亚迪已经超过特斯拉成为全球第一（原因：比较维度不明确）

📊 多视角验证摘要：
  • 视角1（严谨核查员）：大部分事实正确，发现"全球第一"表述不明确
  • 视角2（质疑者）：确认"全球第一"无法验证，补充了多维度比较的说明
  • 视角3（综合裁判）：综合双方意见，维持大部分判定

📊 一致性检测：通过
📚 参考来源：比亚迪官网、2024年年报、新浪财经、雪球
```

---

## 文件结构

```
checktruth/
├── SKILL.md          # 本文件（核心，零配置）
├── prompts/          # 提示词模板（可选，供参考）
├── tests/            # 测试用例（可选）
├── docs/             # 设计文档（可选）
└── reference/        # 参考代码（可选，需外部API Key，非核心功能）
```

**核心功能零配置**：本 Skill 的所有核心验证逻辑均通过 `SKILL.md` 中的指令、
WorkBuddy 内置 LLM 能力和 WebSearch 完成，**无需任何外部 API Key**。

`reference/` 文件夹包含基于外部 LLM API 的参考实现（需自行配置 Key），
**不是核心功能**，仅供开发者参考。普通用户无需理会此文件夹。

### 关于多视角验证的说明

本 Skill 的「多视角交叉验证」是通过 **LLM 角色扮演** 实现的：
- 视角 1（严谨核查员）→ 模拟 GLM 的严谨风格
- 视角 2（质疑者）→ 模拟 DeepSeek 的质疑风格
- 视角 3（综合裁判）→ 模拟混元的综合平衡风格

这是**零配置方案**，无需任何外部 API Key。
如果需要**真正的多模型交叉验证**（调用 GLM/DeepSeek/混元/Kimi/MiniMax 等外部 API），
请参考 `reference/` 文件夹中的脚本（需自行配置各模型 API Key）。

---

_版本：0.4 | 多视角交叉验证（零配置）| 触发词：英文 /checktruth，中文 /别瞎说_
