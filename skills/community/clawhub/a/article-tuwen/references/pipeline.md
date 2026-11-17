# Article Tuwen — 完整执行流程

详细4 Phase执行规范。SKILL.md只保留规则和格式，本文件是执行引擎。

---

## Phase 1: 素材摄入 & 长文撰写（调用transcript-crafter）

### 1.0 判断是否需要转写
- 用户说"转写成图文"（含"转写"）→ 需要Phase 1，调用transcript-crafter
- 用户说"转换成图文"且提供了已有MD文件 → 跳过Phase 1，直接进入Phase 2
- 用户说"不用转写" → 跳过Phase 1

### 1.1 调用transcript-crafter（必须完整8步）
- 技能路径: <transcript-crafter技能安装目录>
- 以auto模式执行完整8步流程：
  1. 输入获取+预处理
  2. 10维度提取→素材稿（认知层/传播层/情绪层/实操层）
  3. 行业适配+人设选择
  4. 框架生成
  5. **5工具搜索补充+事实核查**（关键！这是增量信息的来源）
  6. 文章撰写+内容审核
  7. 质量验证+交付
  8. 桌面保存
- 产出: `<slug>-article.md`（2500-4000字，增量密度≥70%）
- 关键要求：
  - 每段必须有实录外增量（背景/数据/对比/注释），增量信息标注来源
  - 观点必须归属发言者，Agent自身分析与实录观点明确区分
  - 5工具搜索补充确保零空缺，搜不到用[AI推断]标记

---

## Phase 2: 去重多样性检查

### 2.1 读取历史
- 读取 `history.json`（同目录下）
- 不存在或损坏则从空状态开始

### 2.2 轮换池

| 维度 | 池 |
|------|-----|
| 封面搜索词 | server room, data center, abstract blue, technology hands, neural network, code screen, circuit board, city skyline night |
| 封底搜索词 | abstract dark, night city, deep space, dark ocean, sunset silhouette, mountain fog, rain window, dark forest |
| Editorial主题 | indigo-porcelain, ink-classic, kraft-paper, arctic-dawn, moss-stone |
| Swiss主题 | copper-oxide, slate-storm, sage-garden, wine-dark-sea, desert-rose |

### 2.3 约束规则
- 封面/封底/主题按索引轮换，与最近3次不同
- 布局序列首尾固定(M01/M02开头，M15/M16结尾)，中间不与上次前3个重复
- 有数据场景时使用C01-C10图表，与上次不同

---

## Phase 3: 排版渲染

### 3.1 品类推断
- 商业/科技/分析 → Editorial
- 职场/干货/教程 → Swiss

### 3.2 内容规划
- 3500-4500字 → 8-9页
- 至少5种不同版式形态
- 标注明暗/氛围/版式节奏

### 3.3 组装HTML
- 拷贝种子模板（xhs-crafter的assets/目录）
- 注入Phase 2多样性约束
- 从图片源下载封面/封底图片到本地assets/（网络请求，见数据处理声明）
- 遵循字号铁律、密度铁律、关键词铁律

### 3.4 自检自修复
- 字号：搜索inline font-size，发现即替换为class
- 密度：每页≥78%，不足追加内容
- 关键词：核心词每页至少1处
- 图片：无broken image
- 节奏：暗色页不相邻，版式不重复

### 3.5 截图
- 调用xhs-crafter执行HTML页面截图
- 截图后验证文件大小与上次不同，确保内容正确

### 3.6 文字稿
- 模板：标题(1句)→场景开场(2句)→核心论点(2句)→关键原话(2条「」)→数据(5个)→结尾原话(1条)
- 字数：≥800且≤1000字
- 保存为 `<slug>-文字稿.txt`

---

## Phase 4: 交付 & 记录

### 4.1 本地交付
> 本步骤会在桌面创建输出文件夹并写入PNG/MD/TXT文件

- 复制输出文件到 `<桌面目录>\<slug>公众号配图\`
- 告知用户输出路径，不自动打开文件管理器

### 4.2 飞书云盘（需用户确认）
- **确认门**：执行前必须询问用户"是否同步到飞书云盘？"
- 用户同意后执行：
  - `lark-cli drive +create-folder --name "<slug>公众号配图"`
  - cd到output目录后逐个上传（lark-cli要求相对路径）
  - 返回飞书URL
- 用户拒绝则跳过，仅本地交付
- **隐私提醒**：如果素材包含敏感/机密内容，应在询问时额外提醒风险

### 4.3 更新history.json
- 追加本次运行记录
- 更新轮换索引
- 保存

---

## 异常处理

| 异常 | 处理 |
|------|------|
| URL抓取失败 | 重试1次，仍失败提示用户提供文本 |
| 素材<500字 | 提示"素材过少"但继续执行 |
| 图片下载失败 | 重试3次，失败切换图源 |
| 桌面路径权限 | 使用替代复制方法 |
| 飞书token过期 | 重新创建文件夹 |
| history.json损坏 | 从空状态开始 |
| 截图内容错误 | 重新调用xhs-crafter截图，验证文件大小 |
