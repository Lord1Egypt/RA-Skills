---
name: dan-koe-writer
description: Dan Koe 写作方法论工具箱。基于 OpenClaw Agent 模型，把爆款内容拆解成「创意积木」，再组装成新文章。触发场景：(1) 用户要拆解爆款文章并提取写作要素；(2) 用户需要写作方向或创意灵感；(3) 用户要生成完整的公众号/小红书/推特文章；(4) 用户想学习 Dan Koe 的 APAG 框架、POV 写作或创意积木系统。
---

> ⚠️ **免责声明**：本技能基于 Dan Koe 公开分享的写作方法论整理，用于帮助用户学习并应用这些方法论创作原创内容。所有示例积木仅供学习参考，用户应使用自己的原创文章进行拆解和写作。
>
> - Dan Koe 官网：https://www.dankoe.com
> - Newsletter 订阅：https://thedankoe.com/letters
> - 书：The Art of Focus（亚马逊）
> - 本技能与 Dan Koe 本人及其商业产品无官方关联

# Dan Koe Writer

基于 Dan Koe 写作方法论的多智能体写作工具，把爆款内容拆解成「创意积木」，再组装成新内容。

**注意：本工具调用 OpenClaw Agent 的模型（minimax-m2.7），不需要额外配置 API Key。**

## 核心流程

```
爆款内容
    ↓ [goldmine.py]
积木库（7类积木）
    ↓ [spark.py]
创意方向（供 Agent 使用）
    ↓ [Agent 调用自己的模型]
完整文章
```

## 工作目录

```
dan-koe-writer/
├── scripts/
│   ├── goldmine.py   # 拆解爆款 → 提取积木（输出 prompt 供 Agent 调用）
│   ├── spark.py      # 从积木库生成创意方向（支持 JSON 输出）
│   └── write.py      # 从积木库构建写作 context（输出 prompt 供 Agent）
└── references/
    └── knowledge/    # 积木库（7类 Markdown 文件）
```

积木库初始有 Dan Koe 方法论示例积木，可直接使用。

## 积木库说明

| 文件 | 内容 | 使用场景 |
|------|------|---------|
| `hooks.md` | Attention 钩子 | 标题/开头抓住注意力 |
| `paradoxes.md` | 悖论 | 引发认知冲突 |
| `arcs.md` | 转化弧 | 故事线：Before→顿悟→After |
| `core_problems.md` | 核心问题 | 引发读者共鸣 |
| `golden_phrases.md` | 金句 | 收尾、被转发引用 |
| `structures.md` | 结构模式 | APAG/PAS/Before-After |
| `perspectives.md` | 观点 | POV（独特视角）|

## 使用方式

### 1. 拆解爆款内容

```bash
cd <skill>/scripts

# 抓取微信文章
python goldmine.py "https://mp.weixin.qq.com/s/xxxxx"

# 从本地文件拆解
python goldmine.py --file article.txt --source "文章标题"

# 直接输入文本
python goldmine.py --text "文章内容..." --source "手动输入"
```

**输出**：告诉 Agent 需要调用自己的模型提取积木。

### 2. 从积木库生成创意方向

```bash
# 生成3个创意方向（Markdown）
python spark.py

# 生成5个方向
python spark.py --count 5

# 指定话题过滤
python spark.py --topic "写作"

# 输出 JSON 格式（供 Agent 解析）
python spark.py --json

# 只用钩子生成
python spark.py --hook

# 固定种子（可复现）
python spark.py --seed 42
```

### 3. 生成完整文章

```bash
# 公众号长文
python write.py --topic "写作" --platform wechat --length 2000

# 小红书笔记
python write.py --topic "AI" --platform xhs --length 800

# 推文
python write.py --topic "自律" --platform twitter

# 输出 JSON 格式（包含 prompt）
python write.py --topic "个人品牌" --json
```

### 4. Agent 使用方式

Agent 读取脚本输出后，自行调用模型处理：

```python
# 示例：Agent 读取 spark.py 的 JSON 输出
result = subprocess.run(["python", "spark.py", "--json"], capture_output=True)
ideas = json.loads(result.stdout)

# 然后用 Agent 的模型生成文章
for idea in ideas:
    article = await agent.generate(idea)
```

## Dan Koe 方法论速查

### APAG 框架

| 维度 | 作用 | 关键问题 |
|------|------|---------|
| **Attention** | 钩子，抓住注意力 | 如何让人停下来？ |
| **Perspective** | 描绘敌人，指出错误观念 | 读者现在的错误想法是什么？ |
| **Advantage** | 描绘英雄，提出正确视角 | 如何让他们看到新的可能？ |
| **Gamify** | 给出可操作步骤 | 清晰、具体、下一步是什么？ |

### POV > Niche

- **Niche 陷阱**：选垂直领域 → AI 更快更好 → 被替代
- **POV 本质**：你是 lens（透镜），不是垂直领域专家
- **为什么不可复制**：你的经历 + 目标 + 价值观的独特折射，AI 无法复制

### 积木类型使用指南

- **钩子**：用在标题、第一行，制造停顿
- **悖论**：放在开头或转折处，引发"这不对啊"的反应
- **转化弧**：规划文章整体故事线
- **核心问题**：戳中读者痛点引发共鸣
- **金句**：收尾或关键转折，制造记忆点
- **结构**：选择适合内容类型的框架
- **观点**：贯穿全文的独特视角，差异化核心

### 写作事业 6 步

1. 选一个你无法停止谈论的话题
2. 头脑风暴，提出独特观点
3. 每周写 500-1000 字（短+长结合）
4. 把长文拆解为每日短帖
5. 学会让作品被分享（流量 > 写作）
6. 用经验变现

### 短内容写作关键

- **不是消费者，是研究者**：看到好帖子试着用自己的观点重写
- **结构训练**：模仿句式 → 转化为自己的声音
- **积木组合**：同一金句/悖论可用于不同话题的写作

## 技术说明

- **模型**：使用 OpenClaw Agent 配置的模型（`openrouter/minimax/minimax-m2.7`）
- **无需额外 API Key**：脚本只做数据处理，LLM 调用由 Agent 完成
- **JSON 输出**：所有脚本支持 `--json` 参数，方便 Agent 解析
