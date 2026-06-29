---
name: ecommerce-image-diagnosis
description: "电商主图&详情页诊断助手。给它商品主图、详情页截图、搜索结果截图，或者商品链接，自动分析主图点击率潜力与详情页转化率，从视觉清晰度、信息传达、差异化、信任背书、平台合规等10个维度打分，生成结构化 HTML 可视化诊断报告，包含评级、核心发现和 P0/P1/P2 优先改进行动清单。适用于淘宝、拼多多、抖音电商、京东等平台。触发词：主图诊断、详情页诊断、商品图分析、主图优化、详情页分析、电商图片诊断、帮我看看主图、分析详情页、主图好不好、主图转化率、ecommerce image diagnosis。"
agent_created: true
---

# 电商主图&详情页诊断 Skill

## 核心用途

接受以下任意组合素材，输出结构化诊断报告 HTML：
- 商品主图（1-5张）
- 详情页截图（可多张，或一组连续截图）
- 搜索结果截图（主图在搜索列表中的呈现）
- 商品链接（自动抓取商品信息）

## 触发条件

用户提供任意以下素材时触发：
- 上传图片并提到"主图"、"详情页"、"商品图"、"诊断"、"分析"、"优化"等关键词
- 粘贴电商平台商品链接（淘宝、拼多多、抖音、京东等）
- 直接询问主图或详情页的问题（如"这个主图怎么样"、"详情页哪里有问题"）

## 诊断框架

诊断框架详见 `references/diagnosis_framework.md`，核心包含：

**主图10大评分维度（满分100分）：**
1. 视觉清晰度（20分）— 产品清晰度、背景干净度、色彩对比
2. 信息传达（25分）— 核心卖点可见性、文字简洁度、价值主张
3. 差异化竞争力（20分）— 竞品区分度、特色卖点突出度
4. 信任感建立（20分）— 权威认证、品牌识别、实物还原度
5. 平台合规性（15分）— 无违规文字、无虚假合成、移动端适配

**详情页5大评分维度（满分100分）：**
1. 首屏冲击力（25分）— 前3屏是否抓住核心痛点
2. 信息架构（25分）— 逻辑流畅性、模块化布局、参数可读性
3. 场景化呈现（20分）— 使用场景图质量、用户画像匹配
4. 信任背书（20分）— 用户评价、质检认证、品牌故事
5. 转化促进（10分）— 促销信息清晰度、售后保障说明

## 工作流程

### Step 1: 素材接收与分类

根据用户提供内容判断：
- 若提供图片：识别图片类型（主图/详情页截图/搜索结果截图）
- 若提供商品链接：提取商品名、平台、主图URL等基本信息（如可访问）
- 若素材不足：告知用户可以提供哪些素材，以及哪些素材会使报告更完整

**允许部分诊断**：未提供主图则跳过主图维度，未提供详情页则跳过详情页维度。

### Step 2: 视觉分析

仔细观察每张图片，按诊断框架逐项分析：

**主图分析要点：**
- 产品是否占据画面主要区域（理想：60-80%）
- 背景是否简洁（纯色/渐变/场景）
- 文字数量和位置是否合理（不超过3组文字）
- 是否有核心卖点标注或功能展示
- 与同类商品相比视觉差异化程度
- 是否有可见的信任元素（销量、评分、认证）
- 是否有疑似违规文字（最、第一、最优、极致等）
- 缩略图模式下产品是否依然清晰

**详情页分析要点：**
- 首屏内容类型（品牌Banner / 痛点共鸣 / 效果展示）
- 整体逻辑顺序是否符合"痛点→卖点→参数→场景→背书→促销"
- 文字段落vs图片比例
- 是否有使用场景图
- 规格参数是否有可视化处理
- 是否有真实买家好评截图
- 是否有质检/认证资质展示
- 移动端文字可读性

**搜索结果截图分析：**
- 主图在列表中的视觉跳出率
- 与周围竞品的对比优势/劣势

### Step 3: 评分与填充诊断数据

按框架评分，并为每个维度填充 `issues`（发现问题）和 `suggestions`（优化建议）。
用简短、具体的短语描述（5-15字），避免长段落。

示例：
```
issues: ["产品主体占比不足50%", "背景色与产品颜色对比度低"]
suggestions: ["扩大产品展示区域至画面70%", "换深色背景突出浅色产品"]
```

### Step 4: 生成核心发现与优先行动

**核心发现**（3-5条）：指出最影响转化的关键问题，每条以具体数据或现象描述。
**P0（立即修复）**：影响合规性或点击率的硬伤，1-3条。
**P1（本周优化）**：明显影响转化但可快速改进的问题，2-4条。
**P2（下次迭代）**：中长期优化方向，2-3条。

### Step 5: 生成诊断 JSON

将分析结果整理成以下 JSON 结构（仅包含有诊断数据的部分）：

```json
{
  "product_name": "商品名称",
  "platform": "平台名称",
  "product_url": "链接（可选）",
  "diagnosis_date": "YYYY-MM-DD",
  "main_image": {
    "score": 整体主图分（0-100）,
    "clarity": {"score": 分, "max": 20, "issues": [], "suggestions": []},
    "info_delivery": {"score": 分, "max": 25, "issues": [], "suggestions": []},
    "differentiation": {"score": 分, "max": 20, "issues": [], "suggestions": []},
    "trust": {"score": 分, "max": 20, "issues": [], "suggestions": []},
    "compliance": {"score": 分, "max": 15, "issues": [], "suggestions": []}
  },
  "detail_page": {
    "score": 整体详情页分（0-100）,
    "first_screen": {"score": 分, "max": 25, "issues": [], "suggestions": []},
    "info_structure": {"score": 分, "max": 25, "issues": [], "suggestions": []},
    "scene": {"score": 分, "max": 20, "issues": [], "suggestions": []},
    "trust_proof": {"score": 分, "max": 20, "issues": [], "suggestions": []},
    "conversion": {"score": 分, "max": 10, "issues": [], "suggestions": []}
  },
  "search_competition": {
    "visual_standout": "强/中等/弱",
    "thumbnail_clarity": "优/良好/一般/差",
    "title_image_coherence": "强/一般/弱",
    "notes": "补充说明"
  },
  "overall_grade": "S/A/B/C/D",
  "overall_score": 综合分,
  "key_findings": ["发现1", "发现2", "发现3"],
  "priority_actions": {
    "P0": ["行动1", "行动2"],
    "P1": ["行动1", "行动2", "行动3"],
    "P2": ["行动1", "行动2"]
  }
}
```

整体分计算：若同时有主图和详情页，`overall_score = round(main_image.score * 0.45 + detail_page.score * 0.55)`；
若只有主图，`overall_score = main_image.score`；若只有详情页，`overall_score = detail_page.score`。

`overall_grade` 按如下规则判定：
- 85-100 → S；70-84 → A；55-69 → B；40-54 → C；<40 → D

### Step 6: 调用脚本生成 HTML 报告

将 Step 5 的 JSON 写入临时文件，调用生成脚本：

```bash
# 写入 JSON
python_path="C:\Users\PC\.workbuddy\binaries\python\versions\3.13.12\python.exe"
script_path="{baseDir}/scripts/generate_report.py"
json_file="<工作目录>/diagnosis_temp.json"
output_file="<工作目录>/电商诊断报告_<商品名>.html"

# 运行脚本
"$python_path" "$script_path" "$json_file" "$output_file"
```

其中 `{baseDir}` 是本 Skill 所在目录：`~/.workbuddy/skills/ecommerce-image-diagnosis`

输出路径使用当前会话工作目录（`C:\Users\PC\WorkBuddy\当前session目录\`）。

### Step 7: 呈现报告

调用 `present_files` 展示生成的 HTML 文件，同时在文字回复中给出：
- 一句话总结（评级 + 核心问题）
- P0 优先行动列表

## 素材不足时的处理策略

| 素材情况 | 处理方式 |
|---------|---------|
| 只有主图 | 仅诊断主图，详情页维度跳过 |
| 只有详情页截图 | 仅诊断详情页，主图维度跳过 |
| 只有商品链接 | 提取商品名称和平台，尝试获取主图，无法获取时告知用户 |
| 只有搜索截图 | 诊断搜索竞争力，其余维度标注"素材缺失" |
| 无任何素材 | 引导用户上传图片或粘贴链接 |

## 注意事项

- 评分保持客观公正，有问题明说，避免过度宽松或过度严苛
- issues 和 suggestions 使用短语（5-15字），不写长段落
- P0 问题必须是真实硬伤，不能为凑数而强行列出
- 若为抖音平台，额外关注：封面图在竖版短视频feed流中的表现
- 若为拼多多平台，额外关注：主图是否有明显的低价促销感知
- 若商品URL为天猫/淘宝，额外关注：主图视频+多图轮播策略

## 参考资源

- `references/diagnosis_framework.md` — 完整诊断框架和评分标准
- `scripts/generate_report.py` — HTML 诊断报告生成脚本
