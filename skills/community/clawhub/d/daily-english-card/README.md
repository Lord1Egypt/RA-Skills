# 每日英语场景对话卡片推送 Skill — README

## 一、功能概述

每天早上 8:30（Asia/Shanghai）自动推送一张英语口语学习卡片图片到微信：
- **440 个真实场景**（44 主题 × 10 变体），5 轮 A-B-A-B-A 对话
- **11 种视觉风格**按日期轮换（4 种风景 + 7 种色卡）
- **遗忘曲线复习**：工作日学新、周末自动复习
- **IMA 知识库存档**：每张卡片自动上传到腾讯 IMA 知识库
- **万能公式 + 英式音标**：每个公式至少 3 个例句，词汇附带 IPA

---

## 二、系统架构

```
cron (08:30) → isolated agent session → agent 执行以下步骤：
  1. exec: python3.9 push_english_daily.py（生成卡片 + 上传IMA）
  2. 从脚本输出 JSON 提取 image_path
  3. message 工具发送图片到微信（只发图，不加文字）
  → delivery (announce) 也会推送，但 agent 自己用 message 发图更可靠
```

**关键点**：与天气推送不同，英语卡片依赖 Python 脚本做全部重活（卡片生成、进度管理、IMA 上传），agent 只负责调用脚本 + 发送图片。

---

## 三、核心脚本详解

### 3.1 push_english_daily.py — 主推送脚本

**路径**：`~/workspace/scripts/push_english_daily.py`
**运行命令**：`python3 ~/workspace/scripts/push_english_daily.py`

> ⚠️ **确保 Python 环境已安装 Pillow**（部分系统 Python 缺少 PIL，需指定正确路径）。

**输出格式**（JSON 到 stdout）：
```json
{
  "image_path": "~/workspace/cards/card_2026-04-25.png",
  "style": "blush",
  "style_name": "蜜桃绒纱",
  "title_zh": "日常问候",
  "title_en": "Daily Greetings",
  "progress": "0/440",
  "is_weekend": true,
  "tencent_doc_url": ""
}
```

**核心流程**：

```
1. 读取 english_learning.json
2. 判断工作日/周末：
   - 工作日：学习新场景 → current_index + 1 → add_learned_scenario()
   - 周末：按遗忘曲线找复习场景 → 不推进进度
3. match_scene_title() 匹配场景中文标题
4. build_card_content() 构建 JSON 内容：
   - extract_key_phrases(): 从对话提取重点句型
   - build_formulas(): 构建万能公式（3+例句）
   - extract_vocabulary(): 提取关键词汇 + IPA音标
5. get_style_for_date(): 按日期选风格（11天一轮）
6. 调用 generate_english_card.py 生成 PNG
7. upload_card_to_ima() 上传到 IMA 知识库
8. 输出 JSON 结果
```

### 3.2 generate_english_card.py — 卡片图片生成器 v4

**路径**：`~/workspace/scripts/generate_english_card.py`

**画布**：1080 × 1776 像素（手机竖版 9:14.8）

**CLI 参数**：
```bash
python3 generate_english_card.py \
  --content-file content_2026-04-25.json \
  --output card_2026-04-25.png \
  --style blush \
  --seed 20260425
```

**卡片布局**（从上到下）：

```
┌──────────────────────────────┐
│  [emoji] [中文场景标题]       │ ← 32pt bold 居中
│  ─────────────────────       │ ← accent 色分割线
│                              │
│  💬 对话练习                  │
│    [Speaker A] 圆角标签       │
│    英文句子                   │
│    中文翻译                   │
│    [Speaker B] 圆角标签       │
│    ...                       │
│                              │
│  📝 重点句型                  │
│    ● 英文句型                 │
│      中文翻译                 │
│                              │
│  ⚡ 万能公式                  │
│    [❓ 提问公式] 圆角标签      │
│    → 例句1                   │
│    → 例句2                   │
│    → 例句3                   │
│    [✅ 回答公式]              │
│    ...                       │
│                              │
│  🔑 词汇                     │
│    word  /IPA/      中文释义  │
│    ...                       │
│                              │
│     Daily English · 每日英语  │ ← 底部水印 13pt
└──────────────────────────────┘
```

**11 种风格完整定义**：

| # | 风格ID | 中文名 | 类型 | 主色调 | 文字色 |
|---|--------|--------|------|--------|--------|
| 0 | forest | 雾境森林 | 风景 | 冷绿渐变 | #233732 |
| 1 | sunrise | 山野晨昏 | 风景 | 暖橘大地 | #2F2B27 |
| 2 | lake | 清冷湖海 | 风景 | 蓝灰倒影 | #1F2C37 |
| 3 | twilight | 荒原暮色 | 风景 | 深色星夜 | #F0EBE3 |
| 4 | periwinkle | 梦幻薰衣 | 色卡 | 薰衣草→蜜桃 | #2D2755 |
| 5 | blush | 蜜桃绒纱 | 色卡 | 粉→紫→蓝 | #4A2040 |
| 6 | candy | 糖果彩虹 | 色卡 | 粉→黄→蓝→紫 | #2A3050 |
| 7 | nautical | 海军蓝调 | 色卡 | 深蓝→白→蓝 | #E8F0F5 |
| 8 | lavender | 薰衣草梦 | 色卡 | 紫→粉→蓝 | #352850 |
| 9 | ocean | 深海幽蓝 | 色卡 | 深蓝→青→白 | #E0F5FA |
| 10 | warmth | 暖阳绒毯 | 色卡 | 粉→暖棕→桃 | #3A2820 |

**风格轮换**：`STYLES[day_of_year % 11]`，同一天风格固定。

**4 种风景背景生成器**：

| 风格 | 生成函数 | 技术要素 |
|------|----------|----------|
| forest | `create_forest_bg()` | 多层渐变天空 + 3层山峦剪影(中点位移法) + 松树剪影 + 雾带 + 丁达尔光束 |
| sunrise | `create_sunrise_bg()` | 暖橘渐变 + 朝阳光晕(径向渐变) + 4层山峦 + 云雾 |
| lake | `create_lake_bg()` | 蓝灰天空 + 远山 + 水面倒影(翻转+模糊+变暗) + 波纹 |
| twilight | `create_twilight_bg()` | 深色渐变 + 200颗星空 + 月亮光晕 + 荒原剪影 + 月光光束 |

**7 种色卡背景**：统一用 `create_palette_bg(style_name)` 生成
- 垂直渐变 + 大型抽象色斑 + 白色光斑 + 散景光点 + 顶部/底部柔光 + 噪点 + 暗角 + 高斯模糊

**所有风格都叠加半透明蒙版**（`overlay_rgb` + `overlay_alpha`）保证文字可读性。

### 3.3 learning_manager.py — 学习进度管理器

**路径**：`~/workspace/scripts/learning_manager.py`

**掌握程度**：
- `new` → 生疏
- `familiar` → 熟悉（复习 ≥ 3 次自动升级）
- `mastered` → 掌握（复习 ≥ 5 次自动升级）

**遗忘曲线复习间隔**：`[1, 2, 4, 7, 15]` 天

**CLI 命令**：
```bash
python3 learning_manager.py reviews          # 今日需复习的场景
python3 learning_manager.py stats            # 本周学习统计
python3 learning_manager.py cards            # 本周卡片列表
python3 learning_manager.py mastery <idx> <level>  # 更新掌握程度
python3 learning_manager.py reviewed <idx>   # 标记已复习
```

---

## 四、数据文件

### 4.1 english_learning.json

**路径**：`~/workspace/english_learning.json`

```json
{
  "progress": {
    "current_index": 0,
    "total_scenarios": 440,
    "last_updated": "2026-04-25",
    "learned_scenarios": [
      {
        "index": 0,
        "learn_date": "2026-04-25",
        "mastery": "new",
        "review_count": 0,
        "last_review_date": null,
        "next_review_date": "2026-04-26",
        "card_path": "~/workspace/cards/card_2026-04-25.png"
      }
    ]
  },
  "forgetting_curve": {
    "intervals": [1, 3, 7, 14, 30],
    "weights": [1.0, 0.8, 0.6, 0.4, 0.2],
    "review_intervals_days": [1, 2, 4, 7, 15]
  },
  "scenarios": [
    {
      "id": "daily_greetings_01",
      "title": "日常问候",
      "scene": "greeting",
      "dialogues": [
        {"speaker": "A", "speaker_en": "Tom", "en": "Hey, how's it going?", "cn": "嘿，最近怎么样？"},
        {"speaker": "B", "speaker_en": "Lisa", "en": "Pretty good! How about you?", "cn": "挺好的！你呢？"},
        ...
      ]
    }
  ]
}
```

**440 场景结构**：44 主题 × 10 变体，每个场景 5 轮对话（A-B-A-B-A）

### 4.2 cards/ 目录

**路径**：`~/workspace/cards/`

- `card_YYYY-MM-DD.png` — 当天卡片图片
- `content_YYYY-MM-DD.json` — 当天卡片 JSON 内容

### 4.3 weekly_doc_state.json

**路径**：`~/workspace/weekly_doc_state.json`

腾讯文档存档状态（**已弃用**，但文件仍存在）。

---

## 五、IMA 知识库存档

卡片自动上传到腾讯 IMA 知识库，替代已弃用的腾讯文档存档。

| 参数 | 值 |
|------|------|
| KB_ID | `YOUR_IMA_KB_ID` |
| 主文件夹 | `YOUR_IMA_FOLDER_ID` |
| 凭证获取 | `~/Library/Application Support/QClaw/openclaw/config/skills/ima/get-token.sh` |

**上传流程（5步）**：

```
1. preflight-check.cjs — 文件类型+大小前置检查
2. check_repeated_names — 重名检查（同名文件跳过）
3. create_media — 获取 media_id + COS 临时凭证
4. cos-upload.cjs — Node.js 脚本上传文件到 COS（Python 有 403 问题，所以用 Node）
5. add_knowledge — 注册到知识库
```

**关键文件**：
- 前置检查：`.../ima/knowledge-base/scripts/preflight-check.cjs`
- COS上传：`.../ima/knowledge-base/scripts/cos-upload.cjs`
- 凭证获取：`.../ima/get-token.sh`

---

## 六、完整 Cron Payload 提示词

```
你是一个英语学习助手。请完成以下任务：

1. 生成今日英语口语卡片：
```bash
python3 ~/workspace/scripts/push_english_daily.py
```

2. 脚本会输出 JSON，提取 image_path 字段的图片路径。

3. 使用 message 工具发送图片卡片给用户：
   - channel: openclaw-weixin
   - target: o9cq800qdEr8F9W0A_BulcOhDiCk@im.wechat
   - accountId: e7aef5bc05d2-im-bot
   - media: 图片路径（从脚本输出中提取）

4. 图片发送成功后，输出简短确认信息。

要求：
(1) 不要回复 HEARTBEAT_OK
(2) 必须调用 message 工具发送图片
(3) 直接发送图片，不要输出文字内容
```

> **注意**：payload 中写的是 `python3`，但实际应该用 `/usr/local/opt/python@3.9/bin/python3.9`。如果 agent 用了错误的 python 导致报错，需要在 payload 中修正路径。

---

## 七、微信推送配置

| 参数 | 值 |
|------|------|
| channel | `openclaw-weixin` |
| target | `o9cq800qdEr8F9W0A_BulcOhDiCk@im.wechat` |
| accountId | `e7aef5bc05d2-im-bot` |
| delivery.mode | `announce` |
| delivery.bestEffort | `true` |

### Gateway API（手动调试用）

- Base URL: `http://localhost:{GATEWAY_PORT}/api/v1`
- Token: `bash ~/.qclaw/scripts/get-token.sh`

手动推送卡片：
```bash
# 1. 生成卡片
python3 ~/workspace/scripts/push_english_daily.py

# 2. 发送到微信
TOKEN=$(bash ~/.qclaw/scripts/get-token.sh)
curl -X POST "http://localhost:{GATEWAY_PORT}/api/v1/messages/send" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "channel": "openclaw-weixin",
    "target": "o9cq800qdEr8F9W0A_BulcOhDiCk@im.wechat",
    "accountId": "e7aef5bc05d2-im-bot",
    "media": "~/workspace/cards/card_2026-04-25.png"
  }'
```

---

## 八、Cron 配置详情

| 字段 | 值 |
|------|------|
| Job ID | `YOUR_CRON_JOB_ID` |
| 名称 | 英语场景对话每日推送 |
| 表达式 | `30 8 * * *` |
| 时区 | Asia/Shanghai |
| sessionTarget | isolated |
| wakeMode | now |
| enabled | true |

---

## 九、重要代码逻辑详解

### 9.1 场景标题匹配

`SCENE_TITLES` 字典按关键词匹配，如 "餐厅" → "餐厅点餐"，"咖啡" → "咖啡店点单"。
未匹配到则 fallback 为 `DEFAULT_SCENE`（"日常英语"）。

### 9.2 万能公式构建

1. 从 `FORMULA_EXAMPLES` 字典按场景关键词匹配预制例句
2. 提问公式：第一个例句来自实际对话 + 2个预制例句
3. 回答公式：同上
4. 未匹配场景用 `DEFAULT_FORMULA`

### 9.3 英式 IPA 音标

`ENG_TO_IPA` 字典约 80 个常用词的英式音标（如 `wrong → /rɒŋ/`）。
词汇提取时自动查询，未收录的词 phonetic 字段为空。

### 9.4 遗忘曲线复习

- 工作日：学习新场景，`current_index` 前进
- 周末：按 `REVIEW_INTERVALS = [1, 2, 4, 7, 15]` 找到期复习场景
- 复习不推进进度，不标记"复习日"
- 复习 3 次升级 familiar，5 次升级 mastered

### 9.5 腾讯文档（已弃用）

代码中仍保留 `get_week_doc_id()` / `save_week_doc_id()` / `upload_card_to_tencent_docs()` 等函数，但不再使用。腾讯文档因 OCR 扫描中文图片触发违规封禁，已改用 IMA 知识库。

---

## 十、已知问题

1. **Python 路径**：必须用 `/usr/local/opt/python@3.9/bin/python3.9`，Homebrew 3.14 无 PIL
2. **微信推送偶发丢失**：风控原因，无法根治
3. **腾讯文档已弃用**：代码残留待清理（get_week_doc_id 等函数）
4. **IMA COS 上传**：Python 直接调 COS SDK 有 403 问题，已用 Node 脚本绕过
5. **ENG_TO_IPA 不全**：仅约 80 词，生僻词无音标
6. **Cron payload 中 python 路径**：写的是 `python3`，可能触发错误 Python 版本

---

## 十一、重建指南

如果需要从零重建此 skill：

### 1. 准备数据文件

```bash
# english_learning.json 需要 440 场景数据
# 可从 regenerate_scenarios.py 重新生成（注意该脚本有语法错误，需修复）
```

### 2. 安装 Python 依赖

```bash
/usr/local/opt/python@3.9/bin/python3.9 -m pip install Pillow
```

### 3. 创建 cron job

```bash
openclaw cron add --name "英语场景对话每日推送" \
  --schedule '{"kind":"cron","expr":"30 8 * * *","tz":"Asia/Shanghai"}' \
  --payload '{"kind":"agentTurn","message":"<上面的完整提示词>"}' \
  --delivery '{"mode":"announce","channel":"openclaw-weixin","to":"o9cq800qdEr8F9W0A_BulcOhDiCk@im.wechat","accountId":"e7aef5bc05d2-im-bot"}'
```

### 4. 手动测试

```bash
python3 ~/workspace/scripts/push_english_daily.py
# 检查输出 JSON 中 image_path 是否有效
# 检查 cards/ 目录是否生成 PNG
```

### 5. 打包 skill

```bash
python3 ~/Library/Application\ Support/QClaw/openclaw/node_modules/openclaw/skills/skill-creator/scripts/package_skill.py ~/.qclaw/skills/daily-english-card
```

---

## 十二、文件清单

```
~/.qclaw/skills/daily-english-card/
├── SKILL.md          # skill 定义文件（触发描述 + 执行流程）
└── README.md         # 本文件（详细文档）

依赖的脚本文件：
~/workspace/scripts/push_english_daily.py     # 主推送脚本
~/workspace/scripts/generate_english_card.py   # 卡片图片生成器 v4
~/workspace/scripts/learning_manager.py        # 学习进度管理器

数据文件：
~/workspace/english_learning.json              # 440 场景数据
~/workspace/weekly_doc_state.json              # 腾讯文档状态（已弃用）

输出目录：
~/workspace/cards/                             # 卡片图片 + JSON 内容

IMA 知识库相关：
~/Library/Application Support/QClaw/openclaw/config/skills/ima/
├── get-token.sh                                    # IMA 凭证获取
└── knowledge-base/scripts/
    ├── preflight-check.cjs                         # 文件前置检查
    └── cos-upload.cjs                              # COS 上传脚本

Gateway API：
~/.qclaw/scripts/get-token.sh              # Gateway token 获取
```
