---
name: humanize-chinese
description: 检测并去除中文文本中的AI写作痕迹。当用户说"去AI味"、"改得自然一点"、"太机器了"、"帮我润色"、"去掉AI感"时使用。支持文件输入或直接粘贴文本，输出改写后文本和对比报告。适用于论文、文案、公众号、社交媒体等场景。
allowed-tools:
  - Read
  - Write
  - Edit
  - exec
---

# Humanize Chinese v2.1

中文 AI 文本人性化改写工具。检测 AI 写作特征，去除机器腔调，保留原意。

## 工作流

用户给我文本 → 我运行脚本 → 输出改写后文本

### 方式一：直接粘贴（最常用）

用户直接把文字发给我，我调用脚本处理：

```bash
# 对比 + 改写（激进模式，适合明显AI味的内容）
python3 ~/.openclaw/skills/humanize-chinese-2-0-0/scripts/compare_cn.py --scene social -a

# 纯检测，不改写（想先看看AI味有多重）
python3 ~/.openclaw/skills/humanize-chinese-2-0-0/scripts/detect_cn.py -v

# 指定场景改写
# --scene general  通用（默认）
# --scene social   社交媒体、短文
# --scene tech     科技文章
# --scene formal   正式文章/报告
# --scene chat     对话/聊天
```

### 方式二：文件处理

```bash
# 改写并保存到新文件
python3 ~/.openclaw/skills/humanize-chinese-2-0-0/scripts/humanize_cn.py 输入.txt -o 输出.txt --scene social -a

# 检测AI分数
python3 ~/.openclaw/skills/humanize-chinese-2-0-0/scripts/detect_cn.py 输入.txt -v
```

### 方式三：批量处理

```bash
# 批量改写所有 markdown 文件
for f in *.md; do
  python3 ~/.openclaw/skills/humanize-chinese-2-0-0/scripts/humanize_cn.py "$f" --scene tech -a -o "${f%.md}_clean.md"
done
```

## 检测评分体系

| 分数 | 等级 | 含义 |
|------|------|------|
| 0-24 | 🟢 低 | 读起来像真人 |
| 25-49 | 🟡 中 | 有一些AI特征 |
| 50-74 | 🟠 高 | 大概率AI写的 |
| 75-100 | 🔴 很高 | 基本确定是AI |

## 核心检测类别

| 类别 | 权重 | 示例 |
|------|------|------|
| 🔴 三段式套路 | 高 | 首先…其次…最后 |
| 🔴 机械连接词 | 高 | 值得注意的是、综上所述 |
| 🔴 空洞宏大词 | 高 | 赋能、闭环、新质生产力 |
| 🟠 引流开场白 | 高 | 让我们一起、揭秘、划重点 |
| 🟠 模糊概括 | 高 | 有研究表明、专家认为 |
| 🟠 AI高频词 | 中 | 助力、彰显、底层逻辑 |
| 🟠 套话废话 | 中 | 值得一提的是、毫无疑问 |
| 🟡 节奏单一 | 低 | 句子长度高度一致 |

## 改写原则（基于研究）

1. **打破固定句式** — AI 喜欢"首先/其次/最后"，改成自然过渡
2. **增加具体细节** — "有研究表明" → "XX团队在2025年发表的数据"
3. **隐藏中心句** — AI 开头就给结论，改写到段中或段尾
4. **注入个人视角** — 加"我觉得"、"查了资料后发现"
5. **句式变化** — 长短句交替，主动被动互换

## 规则配置

所有检测词和替换规则在：
```
~/.openclaw/skills/humanize-chinese-2-0-0/scripts/patterns_cn.json
```

可自行添加新的 AI 特征词或调整替换映射。
