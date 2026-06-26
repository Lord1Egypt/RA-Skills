# 文生图提示词指南

本文档为 [`cartoon-video-creation-SKILL.md`](../cartoon-video-creation-SKILL.md) Phase 2（角色建档）与 Phase 4.1（首帧图提示词）的详细参考。Agent 在执行对应阶段时按需 Read。

---

## 1. 提示词总公式

分镜首帧图 `image_prompt` 按以下公式组装：

```text
image_prompt = 风格锚 + 画质锚 + 主题锚 + 一致性强化 + 角色身份卡 + 分镜变量 + 负向约束
```

其中：

- `风格锚 / 画质锚 / 主题锚 / 一致性强化 / 负向约束`：来自 `project.json`，**全集 12 镜保持不变**；**每一镜**的完整 `image_prompt` 都必须显式写出这些块（可与上一镜逐字相同，禁止省略或改用近义改写导致画风漂移）。
- `角色身份卡`：来自 `characters/{character_id}.json`，角色外观描述逐字固定。
- `分镜变量`：来自 `storyboard.json` 当前分镜字段（画面、情绪、镜头、场景）——**仅本块随镜变化**。

### 1.1 全片不变特征（`project.json` 建议字段）

在 Phase 2 写入 `project.json`，供 Phase 4 逐镜拼接；字段名可压缩为 JSON key，含义如下：

| 块 | 内容示例 | 作用 |
|----|----------|------|
| `风格锚` | 赛璐珞、平涂、线条粗细、是否 Q 版、参考流派/IP 气质 | 跨分镜画风统一 |
| `画质锚` | 分辨率感、细节密度、是否胶片颗粒 | 成片质感统一 |
| `主题锚` | 本集一句主题 + 世界观关键词（时代、地域、科技/魔法层级） | 叙事与视觉主题不跑偏 |
| `一致性强化` | 全局光照习惯、默认色调倾向、禁止元素提醒 | 减少镜间色差与设定冲突 |
| `负向约束` | 禁写实皮肤、禁水印、禁文字等 | 全集共用 negative |

**质检**：任意两镜若去掉「分镜变量」后，剩余前缀应与 `project.json` 中上述块一致（允许标点与空格差异，不允许语义改换画风）。

---

## 2. 角色身份卡结构

角色身份卡分为外观维度（固定）与表演维度（用于变量生成）：

### 2.1 外观维度（9 项，固定）

| 维度 | 说明 |
|------|------|
| 头身比 | 如 `7-head-tall slim bishounen` / `3-head-tall chibi` |
| 面容 | 面型、肤色、五官特征 |
| 眼睛 | 瞳色、瞳形、高光位置 |
| 发型 | 发色、长度、造型、发饰 |
| 体型 | 身高体态 |
| 服装 | 主服装描述（固定） |
| 配饰/武器 | 标志性道具 |
| 特征标记 | 疤痕、纹身、兽耳等 |
| 角色色板 | 主色 + 辅色 + 点缀色 HEX |

### 2.2 表演维度（3 项，可变）

| 维度 | 说明 | 示例 |
|------|------|------|
| 标志性表情 | 角色最具辨识度的默认表情 | 半闭眼冷淡、狡黠微笑 |
| 标志性姿态 | 角色常见肢体习惯 | 抱臂、单手插袋 |
| 情绪范围 | 本角色可覆盖的情绪区间 | 冷漠→惊讶→愤怒→释然 |

---

## 3. 一致性锚定栈（Anchor Stack）

角色一致性由四层共同保障：

1. Seed 锚（可选，最强）
2. 身份卡锚（固定文本）
3. 参考图锚（`ref_image_url`）
4. 风格锚（`project.json` 全局配置）

降级策略：

- API 不支持 seed 或 `ref-img-url` 时，自动回退到身份卡 + 风格锚
- 即使发生降级，也不得改写身份卡外观维度文本

---

## 4. 参考图策略

在动漫短剧场景，参考图来源按优先级执行：

1. **联网检索图（优先）**：通过 `web_search` 获取角色公开形象图，记录来源页与图片 URL。
2. **项目既有角色图**：`characters/{character_id}_ref*.png`。
3. **纯 prompt 生成**：仅在前两者不可用时使用。

> 知名 IP（如蜡笔小新）默认应先做联网检索，不建议直接跳过参考图阶段。

## 4.1 核心参考图（必须）

- 1 张正面半身、中性表情、白背景
- 用于后续首帧图调用的 `--ref-img-url`
- 若来自联网检索，需满足：人物清晰、无遮挡、无大面积文字水印、分辨率可用

## 4.2 辅助参考图（建议）

| 辅助图 | 目的 | 文件示例 |
|--------|------|----------|
| 3/4 侧面像 | 侧脸一致性校验 | `{id}_ref_side.png` |
| 全身立绘 | 体型与服装比例校验 | `{id}_ref_full.png` |
| 标志性表情 | 表演风格校验 | `{id}_ref_expr.png` |

辅助参考图不要求全部传给 API；主要用于 Agent 质检和 Prompt 修正。

---

## 5. 分镜变量生成规则

`分镜变量` 推荐覆盖以下子维度：

- 表情：眉眼、嘴部、脸部张力
- 姿态：重心、肩颈、手势
- 衣物与发丝动态
- 场景层次：前景/中景/远景
- 镜头角度：平视/俯视/仰视
- 光照：主光方向、硬软光
- 色调：冷暖、对比、饱和度
- 特效粒子：雨雪、烟尘、魔法粒子
- 氛围词：压迫、轻松、悬疑等
- 主体构图：主角色居中、主体占比、背景角色远景化

### 5.1 主体构图硬约束（动漫短剧）

每镜 `image_prompt` 必须显式加入以下约束：

1. 仅 1 名主角色作为视觉主体（`primary_subject`）
2. 主角色位于画面中央区域（center composition）
3. 主角色面积占画幅 >= 1/3（可写 `subject occupies at least one-third of frame`）
4. 其他角色仅允许远景或背景轮廓（`secondary characters in far background only`）

推荐补充语句：

```text
single primary character centered, occupying at least one-third of the frame; all secondary characters remain small in distant background
```

---

## 6. 表情描述规范（必须具体化）

禁止使用纯情绪词（如 `happy`, `angry`）；必须拆成可视化细节。

| 模糊写法 | 推荐写法 |
|---------|----------|
| happy | `corners of mouth curving upward, eyes narrowing into crescents` |
| angry | `brows deeply furrowed, jaw clenched, nostrils slightly flared` |
| sad | `inner brows raised, lower lip trembling, gaze dropping downward` |
| surprised | `eyebrows raised high, eyes widened, mouth forming a small O` |
| cold | `half-lidded eyes, lips in a thin neutral line, chin slightly raised` |

---

## 7. 多角色画面规则

多角色场景中，`image_prompt` 需补充：

1. 角色空间关系（前后左右与距离）
2. 视线关系（谁看向谁）
3. 互动动作（递物、对峙、追逐）
4. 主次关系（主角占画面比例 >= 1/3，其它角色仅远景）

推荐表达：

```text
Character A stands half-step in front-left of Character B, side-facing B, eye contact maintained.
```

动漫短剧场景建议追加：

```text
Character A remains the sole dominant subject in center frame; Character B and others appear only in distant background with small scale.
```

---

## 8. 题材适配参考

| 题材类型 | 风格锚方向 | 身份卡侧重 | 负向约束侧重 |
|----------|-----------|-----------|-------------|
| 玄幻/仙侠 | 国漫古风、水墨、动态构图 | 服装纹饰、法宝、光效 | 现代服饰、写实人像 |
| 热血少年漫 | 赛璐珞、高饱和、速度线 | 发型、招牌动作、战斗姿态 | 照片质感、真实皮肤纹理 |
| 日常喜剧 | Q 版、粗轮廓、平涂 | 头身比、夸张表情 | 写实比例、复杂阴影 |
| 科幻/赛博 | 霓虹、硬表面、未来光效 | 机械配件、制服、HUD | 古风元素、Q 版变形 |
| 少女漫 | 柔光、细线条、装饰粒子 | 眼部高光、发丝层次 | 粗重线条、高噪点 |
| 武侠/历史 | 写实美型+水墨点缀 | 兵器形制、时代服饰 | 现代元素、过度卡通化 |

---

## 9. 质检清单（首帧图）

生成完成后，逐镜检查：

- [ ] **本镜 `image_prompt` 是否含 `project.json` 中的风格锚、画质锚、主题锚、一致性强化与负向约束（全集不变块完整，未省略）**
- [ ] 与相邻分镜相比，除「分镜变量」外是否与全片锚定一致（无画风突变）
- [ ] 主角脸型与发型是否与参考图一致
- [ ] 服装主色和标志性配饰是否保留
- [ ] 手部、眼睛、耳饰等细节是否畸形
- [ ] 表情是否与 `emotion` 和台词语义一致
- [ ] 镜头景别与 `camera_shot` 是否匹配
- [ ] 场景元素是否符合 `scene_environment`
- [ ] 主角色是否居中且占画幅 >= 1/3
- [ ] 其它角色是否仅为远景陪衬（无抢主体）

不通过的分镜仅重生该镜，不影响其它镜头。

