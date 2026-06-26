---
name: ai-songwriter-renxu
description: AI歌曲创作核心技能 — 合辙押韵歌词创作 + MiniMax mmx-cli 正确调用 + 歌词验证 + 歌曲生成全流程。支持古诗词谱曲、主题歌曲创作、多渠道文件投递。
version: 3.3.0
category: utility
tags: [songwriting, rhyming, music-generation, minimax, mmx, lyrics, poetry, thematic, delivery, pronunciation-qa, epic-corporate]
author: renxu
license: MIT
platforms: [linux, macos, windows]
required_environment_variables:
  - MINIMAX_CN_API_KEY
required_commands:
  - mmx
triggers:
  - 写歌
  - 创作歌曲
  - 生成音乐
  - 帮我写首歌
  - AI songwriter
  - 作曲
  - 谱曲
  - 古诗词谱曲
  - 诗词改编
  - 企业歌曲
  - 客户歌曲
  - 景点歌曲
  - 品牌歌曲
  - 主题歌
---

# AI歌曲创作核心技能

## 八层门禁链路（GATED WORKFLOW）

所有歌曲创作必须严格按 8 层顺序执行。每层是一个**硬门禁（HARD GATE）**——失败/不通过不得进入下一层。

```
GATE 0: RESEARCH     → 调研背景信息
GATE 1: OUTLINE      → 分段主题大纲 + 韵脚预分配
GATE 2: RHYME_BANK  → 逐段韵脚字库 + 词语释义
GATE 3: WRITE       → 反推造句（受预分配尾字约束）
GATE 4: VERIFY      → pypinyin 全量验证 + 修复
GATE 5: PRONUNCIATION → 生僻字扫描 + 替换 + --extra 拼音
GATE 6: CONFIRM     → 用户确认歌词
GATE 7: GENERATE    → mmx music generate + 发送
GATE 8: QA          → 听审 + 迭代修复
```

> ⚠️ **核心原则：每层产出必须验证通过后才能进入下一层。在 GATE 3 写词前，GATE 2 的韵脚字库必须已经 100% 确定（44字全局唯一）。不能边写边改韵脚。**

---

## GATE 0：调研背景

**目标**：收集主题相关的历史、事件、特点、典故，输出调研笔记。

```bash
# 企业/公司
mmx search query --q "公司名称 成立 历史 里程碑 产品" --limit 10 --non-interactive --quiet --output json

# 景点/地点
mmx search query --q "景点名称 历史 典故 特色 名人" --limit 10 --non-interactive --quiet --output json

# 特定领域（如六代机）
mmx search query --q "关键词 最新进展 2024 2025" --limit 10 --non-interactive --quiet --output json
```

**产出**：调研笔记（关键时间节点、人物、事件、数据）

**门禁检查**：时间线是否完整？核心技术/事件是否覆盖？ □

---

## GATE 1：分段主题大纲 + 韵脚预分配

**目标**：将叙事线拆为 11 段，预分配每段的韵脚组和 44 个全局唯一定位字。

### 韵脚模式选择

| 模式 | 规则 | 适用 |
|------|------|------|
| **中东辙合韵（默认）** | ing/eng/ong/iong 通押为 'eng' 组 | 用户偏好，中文歌曲习惯 |
| 严格分韵 | ing/eng/ong 各自独立 | 学术验证 |
| AABA | L1=L2=L4 同韵，L3 白脚异韵 | 主题/企业歌曲 |
| 全韵统一 | 所有句同韵 | 短歌/儿歌 |

### AABA + 中东辙标准分配（11段 × 4句 = 44句）

```
段韵分配（不可变）：4ang + 5eng + 2ong = 11段
L3白脚分配（不可变）：全部 en 组 = 11个白脚字
尾字总量（不可变）：12ang + 15eng + 6ong + 11en = 44字全局唯一
```

**产出格式**：

| 段 | 标签 | 主题 | 段韵 | L1 | L2 | L4 | L3(en) | 核心内容 |
|----|------|------|------|----|----|----|--------|----------|
| 1 | Intro | xxx | ang | 航 | 光 | 翔 | 间 | xxx |
| ... | ... | ... | ... | ... | ... | ... | ... | ... |

**门禁检查**：
- 11段是否都有明确主题？ □
- 段韵分配是否为 4ang+5eng+2ong？ □
- 44个字是否互不相同（肉眼初查）？ □
- 叙事逻辑是否通顺？ □

---

## GATE 2：逐段韵脚字库 + 词语释义

**目标**：为每个预分配的韵脚字提供常用词语和释义，供 GATE 3 造句参考。

**产出格式**（每段一组）：

```
### 段1【主题】韵母 ang — 航/光/翔/间(白脚)

| 韵脚字 | 常用词语（供造句参考） | 释义 |
|--------|---------------------|------|
| 航 | 启航、远航、领航、航空 | 出发；引领方向 |
| 光 | 荣光、曙光、光芒、追光 | 光辉；荣耀 |
| 翔 | 翱翔、飞翔 | 展翅高飞 |
| 间 | 瞬间、天地间、弹指间 | (白脚) 时段、空间 |
```

**门禁检查**：
- 每个字是否都有 ≥3 个可造句的词语？ □
- 白脚字（en组）是否标注了用途？ □
- 是否有生僻字混入词库？（如「筚」「缕」「旌」→ 提前踢出） □

---

## GATE 3：反推造句

**目标**：用 GATE 2 的预分配尾字反向造句。每段 AABA，L1/L2/L4 尾字必须是指定的段韵字，L3 尾字必须是指定的白脚字。

**硬约束**：
- ❌ 不得使用非分配的尾字
- ❌ 不得在段内换韵
- ❌ 「客户名/品牌名」只能出现一次，且在 Intro 低调位置
- ❌ 主线是业务/历史叙事，不是个人颂歌

**产出**：44 句完整歌词（无结构标签 — 纯文本，一行一句）

**门禁检查**：44 句是否写完？尾字是否与 GATE 2 分配一致（肉眼核对）？ □

---

## GATE 4：pypinyin 全量验证

**目标**：用 Python 脚本逐句验证韵母归属 + AABA 结构 + 尾字全局唯一性。

**必须用 pypinyin 而不能用硬编码集合**：

| 字 | 硬编码判断 | pypinyin 正确结果 |
|----|----------|-----------------|
| 穷 | ong | eng (iong) |
| 穹 | ong | eng (iong) |
| 雄 | ong | eng (iong) |
| 逢 | ong | eng (ong→介音u，归eng) |
| 崧 | eng | ong |

```python
import re
from pypinyin import pinyin
from collections import Counter

def get_rhyme_group(ch):
    """返回 'ang'|'eng'|'ong'|'en' 韵母组"""
    py = pinyin(ch, style=0)[0][0].lower()
    m = re.findall(r'[bpmfdtnlgkhjqxzcsryw]+', py)
    initial = m[0] if m else ''
    final = py[len(initial):]
    if final in ['ang','iang','uang']: return 'ang'
    if final in ['eng','ing','ueng','iong']: return 'eng'
    if final in ['ong']: return 'ong'
    if final in ['en','in','un','ün','uen','ian','an','uan']: return 'en'
    return f'other({final})'

# AABA 验证
def validate_aaba(lines, seg_rhymes):
    """lines: 44个字符串, seg_rhymes: 11个段韵列表"""
    errors = []
    tails = []
    for si in range(11):
        s = si * 4
        g1,g2,g3,g4 = [get_rhyme_group(lines[s+j][-1]) for j in range(4)]
        sr = seg_rhymes[si]
        tails.extend([lines[s+j][-1] for j in range(4)])
        if not (g1==g2==g4==sr and g3=='en'):
            errors.append(f"S{si+1}: {g1}/{g2}/{g3}/{g4} (期望 {sr}/{sr}/en/{sr})")
    dups = {k:v for k,v in Counter(tails).items() if v>1}
    return errors, dups
```

**验收标准**：
- 韵脚错误 = 0 □
- 尾字重复 = 0（全局唯一） □
- AABA 结构 = 100% 正确 □

**修复原则**：发现重复尾字→优先替换高频字；发现韵脚错误→换尾字（必须同组且全局唯一）。

**门禁检查**：以上三项是否全部通过？ □

---

## GATE 5：发音质量控制

**目标**：扫描生僻字，替换高危字，为保留字准备 --extra 拼音提示。

### 生僻字风险分级

| 字级 | 定义 | 策略 | 示例 |
|------|------|------|------|
| 乙级（超纲） | HSK词汇表外 | 强制替换，不保留 | 筚、缕、旌 |
| 丙级（低频） | HSK丙级 | 优先替换；不可替换时加 --extra | 峥、嵘、霆、铭、铸 |
| 多音字 | 有多个读音 | --extra 标注正确读音 | 藏(cáng/zàng)、行(xíng/háng) |

### 替换规则

- **中间位字词**（不在句尾）→ 直接替换为常用同义词，不影响韵脚
- **尾字**（影响韵脚）→ 替换为同韵母组常用字，且必须验证全局唯一性
- **保留字**→ 必须加入 `--extra` 拼音提示

**产出**：修复版歌词 + `--extra` 拼音提示字符串

**门禁检查**：
- 乙级字是否全部替换？ □
- 保留字是否都加了 --extra 拼音？ □
- 替换后韵脚是否重新通过 GATE 4 验证？ □

---

## GATE 6：用户确认歌词

**目标**：将歌词提交用户确认，未经确认不得生成音频。**这是硬规则。**

**产出**：
- 纯文本歌词（无结构标签）
- 预计时长（44句×3.2秒≈2.3分钟，repeat≈4.7分钟）
- 韵脚验证结果（0错误）

**门禁检查**：用户是否明确确认？ □

---

## GATE 7：音乐生成 + 发送

**目标**：用正确参数调用 mmx music-2.6，生成后发送文件。

### 歌词双轨制

| 场景 | 是否含结构标签 | 原因 |
|------|-------------|------|
| 用户确认 | ❌ 纯文本 | 阅读体验 |
| mmx API | ✅ [Intro][Verse][Chorus]等 | 帮助AI理解结构，提升生成质量 |

### 音乐风格匹配表

| 歌曲类型 | --prompt 关键词 | --vocals | --bpm | --key |
|---------|---------------|----------|-------|-------|
| 航空/军工/史诗 | Epic cinematic orchestral, Chinese national style, military grandeur, soaring brass, timpani, building from solemn to triumphant | Powerful male choir, heroic baritone solo | 105-115 | D/G major |
| 企业/品牌 | Warm positive corporate, steady rhythmic, modern, hopeful, choir climax | Choir, uplifting chorus | 100-110 | C major |
| 古诗词 | Traditional Chinese, slow tempo, guqin, xiao flute, sparse and elegant | Sweet child/古风女声 | 60-80 | E minor |
| 景点/山水 | Cinematic ancient style, dizi flute, guzheng, flowing water imagery | 古风女声, sweet and ethereal | 70-90 | D minor |
| 温馨/亲情 | Gentle acoustic, piano-driven, warm and intimate | Warm male baritone | 80-95 | F major |

### 生成命令模板

调用 mmx 前确保 PATH 包含 mmx 所在目录（安装位置取决于环境，常见于 `~/.hermes/node/bin/` 或 `~/.local/bin/`）。用 `which mmx` 或查找确认路径后 export。

```bash
# 确保 mmx 在 PATH 中（根据实际安装位置调整）
export PATH="<mmx安装目录>:$PATH"

mmx music generate \
  --prompt "风格描述" \
  --lyrics-file <歌词文件路径> \
  --vocals "人声描述" \
  --genre "流派" \
  --mood "情绪" \
  --instruments "乐器" \
  --tempo "速度" \
  --bpm 110 \
  --key "D major" \
  --use-case "使用场景" \
  --extra "Pronunciation: 生僻字=拼音, ..." \
  --model music-2.6 \
  --out <输出路径>.mp3 \
  --non-interactive --quiet
```

> ⚠️ `--async` 不能用于 music generate。
> ⚠️ `--lyrics-file` 比 `--lyrics` 更稳定（避免命令行字符串过长）。
> ⚠️ 不要硬编码绝对路径到技能中——让 agent 在运行时动态确认 mmx 位置。

### 文件发送

```python
send_message(
    action="send",
    target="<platform>:<chat_id>",
    message="🎵 歌曲描述 MEDIA:/tmp/song.mp3"
)
```

**门禁检查**：
- 结构标签是否在 API 调用中保留？ □
- 音乐参数是否与歌曲类型匹配？ □
- --extra 是否包含发音提示？ □
- 文件是否成功发送？ □

---

## GATE 8：听审 + 迭代

**目标**：听取生成结果，发现发音错误→回到 GATE 5 替换→GATE 4 重新验证→GATE 7 重新生成。

**常见问题**：

| 问题 | 修复 | 迭代路径 |
|------|------|---------|
| 某字发音不准 | 替换为同韵脚常用字 | GATE 5 → 4 → 7 |
| 某段情绪不对 | 调整结构标签或 --prompt | GATE 7 |
| 整体气场不够 | 换 --genre/--mood/--bpm | GATE 7 |
| 时长太短 | 加 repeat 或扩展段落 | GATE 1 → ... → 7 |

**门禁检查**：用户是否满意？ □

---

## 时长控制

```
预估时长 ≈ 歌词总句数 × 3.2秒/句
24句 → 约77秒（不够）
44句 → 约141秒（单遍不够，repeat ≈ 4.7分钟 ✅）
56句 → 约179秒（边缘）
60~92句 → 推荐交付区间
```

**硬规则**：单遍不足 3 分钟必须 repeat 或扩写。
**补足优先级**：repeat 完整结构 > 增加 Verse > 增加 Bridge。

---

## 用户反馈处理优先级

| 用户反馈 | 信号级别 | 处理 |
|---------|---------|------|
| "尾字重复太多不好听" | FIRST-CLASS | 立即检查重复字 > 换韵脚分组 > 换不同意象字 |
| "发音不对，xx字读错了" | HIGH | GATE 5 替换该字 → GATE 4 → GATE 7 |
| "气场不够" | MEDIUM | 调 --prompt/--genre/--bpm → GATE 7 |
| "某段歌词改一下" | LOW | 局部替换 → GATE 4 验证 |

---

## mmx-cli 参考

### 模型路由

| 任务 | 模型 | 命令 |
|------|------|------|
| 歌曲生成 | music-2.6 | `mmx music generate --model music-2.6` |
| 歌词生成（备用） | MiniMax-M2.7 | `mmx text chat --model MiniMax-M2.7 --region cn` |
| 图片生成 | image-01 | `mmx image generate --model image-01` |
| 视频生成 | hailuo-2.3 | `mmx video generate --model hailuo-2.3` |

> ⚠️ `lyrics_generation` 不可靠（经常超时），用 MiniMax-M2.7 作为歌词生成的备用模型。
> ⚠️ `music-2.6-free` 需要付费计划，不用。

### 声线参数

| 期望声线 | --vocals |
|---------|----------|
| 男声合唱 | `Powerful male choir with heroic baritone solo` |
| 女声独唱 | `Bright female soprano` |
| 童声 | `Sweet innocent child vocal` |
| 合唱 | `Choir, uplifting chorus` |
| 男声独唱 | `Warm male baritone` |

### 结构标签（mmx API 支持）

`[Intro] [Verse] [Pre Chorus] [Chorus] [Interlude] [Bridge] [Outro] [Build Up] [Solo]`

---

## 审查清单

```
□ GATE 0: 调研笔记是否完整？
□ GATE 1: 11段大纲是否通过用户确认？
□ GATE 2: 44字韵脚库是否 100% 确定？
□ GATE 3: 44句是否严格用预分配尾字造句？
□ GATE 4: pypinyin 验证是否 0 错误 + 0 重复 + AABA 全对？
□ GATE 5: 乙级生僻字是否全部替换？保留字是否加了 --extra？
□ GATE 6: 歌词是否已发给用户确认？
□ GATE 7: --model music-2.6？结构标签是否保留在 API 调用中？
□ GATE 8: 用户是否满意最终音频？
```

---

## 已知问题与解法

| 问题 | 解法 |
|------|------|
| 尾字重复 | 替换韵脚分组（ang↔eng↔ong轮换）→ 替换不同意象字（航→长/途）|
| 生僻字发音不准 | 三层防线：扫描替换 → --extra 拼音 → 听审迭代 |
| 硬编码韵母集合不可靠 | 强制用 pypinyin 逐字验证 |
| lyrics_generation 返回空 | 换用 `MiniMax-M2.7` 作为备用 |
| 48句+ 长歌词超时 | Python subprocess 后台运行，等待约 160 秒 |
| 粤语不支持 | music-2.6 输出仍为普通话 |

---

## References

- MiniMax CLI: https://github.com/MiniMax-AI/cli
- Platform Docs: https://platform.minimaxi.com/docs
- ClawHub: https://clawhub.ai/andyrenxu7255/ai-songwriter-renxu
- **`references/rhyme-table-20260522.md`** — 实测押韵表
- **`references/session-20260522-chengfei.md`** — 成飞案例完整复盘
