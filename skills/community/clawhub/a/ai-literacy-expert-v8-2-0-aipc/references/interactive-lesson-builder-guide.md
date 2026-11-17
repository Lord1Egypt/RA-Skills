> **V7 兼容性说明**：本文件从 V6 完整继承。V7 保留所有 V6 能力，本文件内容完全有效。
> V7 新增 references 见 `references/edge-cloud-architecture.md` / `references/zero-upload-privacy.md` / `references/npu-scheduling-guide.md` / `references/edge-cloud-protocol.md` / `references/audit-report-v7.md`。
> 原始文件版本：V6 · 继承版本：V7 · 继承日期：2026-08-15

# 交互式问答备课生成指南（V4 新增）

> 本文是 V4 能力三「交互式问答生成完整备课文档」的设计与实现手册。V3 备课理念见 `references/lesson-prep-workflow.md`，本指南专注"问答流程 + 4 格式文档生成 + 单 HTML 交互界面"。

## 一、核心理念

- **AI 做 Executor（生成），人做 Architect（决策）**：与 V3 lesson-prep-workflow 的 P0–P3 约束衔接
- **5 阶段对话，逐步明确需求**：每阶段出口明确，避免"AI 跑偏"
- **一次生成 4 格式文档包**：Excel / Word / PPT / PDF 全部一并交付
- **单 HTML 文件**：老师在浏览器一键打开，填写表单 → 一键下载所有文档

## 二、5 阶段对话流程

### Phase 1 · 受众确认
- 提问：「请选择您的受众：① 中学生 ② 大学生 ③ 教师（备课用） ④ 专业应用场景」
- 必填，存为 `audience`

### Phase 2 · 模块选择
- 提问：「请选择要备课的模块（可多选）：A1 AI 进化历程 / A2 AI 是什么 / A3 协作哲学 / B1 TRAE IDE / B2 SOLO / C1 Prompt / C2 需求拆解 / C3 验证闭环 / C4 多 Agent / C5 飞轮 / D1 数据分析 / D2 Vibe Coding」
- 多选，存为 `modules[]`

### Phase 3 · 粒度确认
- 提问：「请选择备课粒度：① 单课（30 分钟） ② 单元（2–4 课） ③ 模块（整套 5–10 课） ④ 整套（20+ 课）」
- 单选，存为 `granularity`

### Phase 4 · 内容生成（AI 内部执行）
- 调阅 `references/module-<a-e>.md` 对应模块内容
- 用 V3 备课工作流：P0 约束文件 + P1 进度文件 + P2 分阶段 + P3 横评
- 生成教案结构、题目库、PPT 大纲
- 教师不需要介入，但 AI 内部走完

### Phase 5 · 文档生成 + 一键下载
- AI 把 Phase 4 内容渲染为 4 格式文档
- 单 HTML 文件提供 4 个下载按钮（Excel / Word / PPT / PDF）

## 二·附、教学模式选择（V7 新增）

> 在 Phase 3 粒度确认之后、Phase 4 内容生成之前，教师需选择一种教学模式。不同模式决定 Phase 4 生成内容的形态与侧重。

### 五种教学模式一览

| 教学模式 | 核心理念 | 教师角色 | 系统生成内容（Phase 4 差异化） |
|----------|----------|----------|-------------------------------|
| **讲授模式**（Lecture） | 教师主导，系统辅助 | 知识传授者 | PPT + 逐字稿 + 板书设计 + 课堂例题；按"导入→讲授→互动→总结"线性结构生成 |
| **探究模式**（Inquiry） | 问题驱动，学生自主探索 | 引导 facilitator | 探究任务链 + 引导问题集 + 假设验证工作单 + 结论归纳模板；PPT 以问题页为主轴，逐字稿改为引导话术 |
| **协作模式**（Collaborative） | 小组合作，同伴互学 | 组织协调者 | 分组任务卡 + 角色分工表 + 协作评价量规 + 小组汇报模板；PPT 含分组指令页，Excel 题库增加协作评分列 |
| **翻转模式**（Flipped） | 课前自学 + 课中实践 | 学习设计师 | 预习材料包（微课脚本 + 预习检测题）+ 课堂活动设计（讨论/实操/答疑）+ 课后巩固任务；Word 教案分"课前/课中/课后"三段 |
| **项目模式**（Project-based） | 长周期项目，真实问题解决 | 项目教练 | 项目 brief + 里程碑计划 + 阶段性评价标准 + 成果展示模板；PPT 改为项目启动演示，Excel 增加里程碑检查清单 |

### 教学模式对 Phase 4 的具体影响

#### 讲授模式（默认）
- Phase 4 生成标准教案结构：教学目标 → 学情分析 → 教学过程（导入/讲授/互动/总结）→ 板书设计 → 作业布置
- PPT 按内容页线性排列，备注栏含完整逐字稿
- Excel 题目表覆盖记忆→理解→应用三个认知层次

#### 探究模式
- Phase 4 生成探究任务链：核心问题 → 子问题序列 → 探究活动 → 数据收集表 → 结论归纳
- PPT 以"问题页"为主轴，每页含一个驱动问题 + 探究提示
- Word 教案改为"探究工作单"格式，含假设记录区、实验步骤区、发现总结区
- Excel 题目表侧重分析→创造层次，增加开放性题目比例

#### 协作模式
- Phase 4 生成分组任务体系：任务描述 → 角色定义（组长/记录员/汇报员/时间管理员）→ 协作流程 → 互评量规
- PPT 含分组指令页、角色说明页、汇报模板页
- Excel 题目表增加"协作贡献"评分列，支持组内互评
- Word 教案含小组活动指导语、巡视要点、汇报引导问题

#### 翻转模式
- Phase 4 分三段生成：
  - **课前**：预习材料清单 + 微课视频脚本（5-8 分钟）+ 预习检测题（5-10 题客观题）
  - **课中**：基于预习数据的针对性教学活动（答疑/讨论/实操）+ 分层任务卡
  - **课后**：巩固练习 + 拓展任务
- PPT 仅用于课中环节，课前材料以独立 PDF 交付
- Word 教案三段独立，课前段含预习数据统计指引

#### 项目模式
- Phase 4 生成项目全流程文档：
  - **项目 brief**：背景、目标、约束、交付物要求
  - **里程碑计划**：3-5 个阶段节点，每阶段含任务、资源、评价标准
  - **过程指导**：每阶段的学生工作单 + 教师检查清单
  - **成果评价**：多维度评价量规（过程 + 成果 + 反思）
- PPT 改为项目启动演示（含项目背景、要求、时间线）
- Excel 增加里程碑检查清单 + 阶段性评价表

### 教学模式选择界面（HTML 表单增量）

在 §4.2 界面骨架的 Phase 3 之后新增：

```html
<fieldset id="phase3b">
  <legend>教学模式选择</legend>
  <label><input type="radio" name="teaching_mode" value="讲授模式" checked> 讲授模式（教师主导）</label>
  <label><input type="radio" name="teaching_mode" value="探究模式"> 探究模式（问题驱动）</label>
  <label><input type="radio" name="teaching_mode" value="协作模式"> 协作模式（小组合作）</label>
  <label><input type="radio" name="teaching_mode" value="翻转模式"> 翻转模式（课前自学+课中实践）</label>
  <label><input type="radio" name="teaching_mode" value="项目模式"> 项目模式（长周期项目）</label>
</fieldset>
```

## 二·附2、流程阶段映射表（V7 新增）

> 本系统中存在三套流程阶段划分：备课工作流（3 阶段）、交互式问答备课（5 阶段）、评估流程（5 阶段）。以下映射表统一对齐，便于跨模块引用与协作。

| 备课工作流（3 阶段） | 交互式问答备课（5 阶段） | 评估流程（5 阶段） | 说明 |
|----------------------|--------------------------|---------------------|------|
| **阶段一 · 探索与对齐**（锁方向） | Phase 1 · 受众确认 | Phase 1 · 模块确认 | 明确"为谁、学什么" |
| | Phase 2 · 模块选择 | Phase 2 · 难度确认 | 明确"学哪些、什么深度" |
| | Phase 3 · 粒度确认 + 教学模式选择 | Phase 3 · 题量确认 | 明确"范围多大、多少量" |
| **阶段二 · 内容创作**（产内容） | Phase 4 · 内容生成 | Phase 4 · 测评执行 | 核心生产/执行环节 |
| **阶段三 · PPT + 逐字稿**（授课材） | Phase 5 · 文档生成 + 一键下载 | Phase 5 · 评分与报告 | 最终产物交付 |

### 映射说明

1. **备课工作流的"阶段一"对应问答备课的 Phase 1-3**：三者都是"对齐需求"的过程——受众、模块、粒度/模式逐步明确，锁定方向后才进入生产。
2. **备课工作流的"阶段二"对应问答备课的 Phase 4**：均为 AI 内部执行的内容生成环节，教师不直接介入但可 Review。
3. **备课工作流的"阶段三"对应问答备课的 Phase 5**：均为最终产物交付——备课流产出 PPT+逐字稿，问答流产出 4 格式文档包。
4. **评估流程独立但可衔接**：Phase 1-3 对齐需求，Phase 4 执行测评，Phase 5 输出报告。评估结果可反馈至备课工作流的"阶段一"，形成"评估→诊断→调整备课方向"的闭环。

## 三、4 格式文档内容设计

### 3.1 Excel 题目表（SheetJS）

| 列 | 说明 |
|----|------|
| 题型 | 单选 / 多选 / 填空 / 简答 / 编程 |
| 知识点 | 关联到 V3 模块的 §n.m |
| 难度 | 1–5 星 |
| 题目 | 题干 |
| 答案 | 正确答案 |
| 解析 | 答题要点 |
| 关联课件 | 可选的 p5.js 课件 / 游戏链接 |

### 3.2 Word 教案（docx.js 或服务端 docx）

- 章节：教学目标 / 学情分析 / 教学过程（导入 / 讲授 / 互动 / 总结）/ 板书设计 / 作业布置 / 教学反思
- 附录：完整逐字稿（与 PPT 同步）

### 3.3 PPT 页面稿（pptxgenjs）

- 首页：课程标题 + 副标题
- 章节页：每章首页
- 内容页：文字 + 配图占位 + 关键概念
- 互动页：提问 + 选项
- 总结页：知识图谱
- 备注栏：教师口播稿

### 3.4 PDF 合并包（jsPDF + 前三份嵌入）

- 封面：课程标题 + 教师姓名 + 日期
- 目录：4 份文档索引
- 合并内容：题目表 + 教案 + PPT 截图
- 评估量规（可选）

## 四、单 HTML 交互式问答界面设计

### 4.1 技术栈
- HTML5 + 原生表单（5 阶段对话）
- CSS：响应式 + 移动端友好
- JS 库（CDN）：
  - `xlsx.js`（SheetJS）→ 生成 Excel
  - `docx` + `file-saver` → 生成 Word
  - `pptxgenjs` → 生成 PPT
  - `jsPDF` + `html2canvas` → 生成 PDF

### 4.2 界面骨架

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <title>V4 交互式备课生成器</title>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.18.5/xlsx.full.min.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/docx@8.5.0/build/index.umd.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/pptxgenjs@3.12.0/dist/pptxgen.bundle.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>
  <style>/* 响应式 + 表单样式 */</style>
</head>
<body>
  <h1>V4 交互式备课生成器</h1>
  <form id="builder">
    <fieldset id="phase1">
      <legend>Phase 1 · 受众</legend>
      <label><input type="radio" name="audience" value="中学生"> 中学生</label>
      <label><input type="radio" name="audience" value="大学生"> 大学生</label>
      <label><input type="radio" name="audience" value="教师"> 教师</label>
      <label><input type="radio" name="audience" value="专业"> 专业应用</label>
    </fieldset>
    <fieldset id="phase2">
      <legend>Phase 2 · 模块（可多选）</legend>
      <label><input type="checkbox" name="modules" value="A1"> A1 AI 进化历程</label>
      <label><input type="checkbox" name="modules" value="A2"> A2 AI 是什么</label>
      <label><input type="checkbox" name="modules" value="C1"> C1 Prompt</label>
      <!-- 全部 A/B/C/D/E 模块 -->
    </fieldset>
    <fieldset id="phase3">
      <legend>Phase 3 · 粒度</legend>
      <select name="granularity">
        <option>单课</option>
        <option>单元</option>
        <option>模块</option>
        <option>整套</option>
      </select>
    </fieldset>
    <button type="submit">生成备课包</button>
  </form>
  <div id="download">
    <button id="dl-xlsx" disabled>📊 下载 Excel 题目表</button>
    <button id="dl-docx" disabled>📄 下载 Word 教案</button>
    <button id="dl-pptx" disabled>📽️ 下载 PPT 页面稿</button>
    <button id="dl-pdf" disabled>📕 下载 PDF 合并包</button>
  </div>
  <script>
    // 表单提交 → 调 AI 接口 / 加载本地内容 → 4 库生成 Blob → 触发下载
  </script>
</body>
</html>
```

### 4.3 内容来源

- **AI API 模式**：表单提交后调用 AI 接口（如 `/api/lesson-builder`），传入 `audience / modules / granularity`，服务端读 V3 references + 生成内容 → 返回 JSON → 前端 4 库生成 Blob → 触发下载
- **本地模式**（无后端）：AI 在 V4 技能下一次性生成完整 HTML + 内嵌内容（教师离开 AI 也能用）

## 五、强制测试门控（问答备课专项）

- 5 阶段对话流程分支覆盖（每个 Phase 都有明确出口）
- 4 格式文档均能正确生成并下载（Excel / Word / PPT / PDF）
- 文档库 CDN 加载成功（提供 jsdelivr 备选）
- 文档内容与 V3 references 一致（不凭空编造知识点）
- 表单校验：必填项缺失时给出友好提示
- 跨浏览器兼容（Chrome / Edge / Safari / Firefox）
- 移动端表单可用（响应式）

## 六、与 V3 lesson-prep-workflow 衔接

| V3 备课 | V4 问答备课 |
|---------|-------------|
| P0 约束文件 | Phase 1 + Phase 2 自动生成受众 / 模块约束 |
| P1 进度文件 | Phase 3 粒度确认 = 进度阶段 |
| P2 分阶段 | 5 阶段对话 = 强制的"先对齐后写作" |
| P3 横评 | Phase 5 生成 PDF 中自动含横评表 |
| 三层治理 | 交互式表单自动建立三层结构 |

## 七、30 分钟出活清单

1. V4 技能加载后，AI 主动问 5 阶段问题
2. 用户依次回答（每阶段 1–2 分钟）
3. Phase 4 内部生成内容（AI 一次性产出）
4. 输出：单 HTML 文件（交互式表单 + 4 文档生成按钮）
5. 用户打开 HTML → 在线微调 → 一键下载 4 格式
6. 老师用 Word 教案 + PPT 备课，用 Excel 题库出题，用 PDF 备份

## 八、典型用例

- 例 1：中学信息老师备课 C1 Prompt 单元
  - 答：受众「中学生」 / 模块 C1 / 粒度「单元」
  - 输出：Excel 30 题 + Word 2 课教案 + PPT 30 页 + PDF 合并包
- 例 2：大学新教师备课整套 A 模块
  - 答：受众「大学生」 / 模块 A1+A2+A3 / 粒度「整套」
  - 输出：Excel 100 题 + Word 10 课教案 + PPT 150 页 + PDF 合并包
- 例 3：企业培训备课 B1 TRAE IDE
  - 答：受众「专业」 / 模块 B1 / 粒度「单课」
  - 输出：Excel 20 题 + Word 1 课教案 + PPT 20 页 + PDF 合并包

## 九、常见坑与解法

| 坑 | 解法 |
|----|------|
| 文档库 CDN 加载失败 | 提供 jsdelivr 备选 + try/catch 降级提示 |
| Word 排版乱 | 用 docx 模板（标题 / 正文 / 列表样式） |
| PPT 字号不一致 | 强制主题字号 + 排版规则 |
| PDF 体积过大 | 压缩图片（webp / quality 70%） |
| 表单数据丢失 | 用 `localStorage` 自动保存草稿 |
| AI 跑偏到无关模块 | 严格用 V3 references 内容，不自由发挥 |
| 一次性生成内容太多超时 | 拆 Phase 4 为"先 outline → 确认 → 再生成 4 文档" |

## 十、扩展方向

- 接入 LMS（学习管理系统）直接发布
- 与 V3 p5.js 课件 / 游戏联动（一键生成"课件 + 游戏 + 备课包"三位一体）
- 题目难度自适应（根据学生答题反馈调整）
- 多语言（中英双语）
- 协作备课（多人同时填写，教师合并）
- 历史版本管理（每次生成留档，可回滚）

## 十一、交付物升级（V4.3 新增）：单 HTML + 4 格式 zip 一键打包下载

V4.3 在 V4「单 HTML + 4 文档分别下载」的基础上，新增**一键 zip 打包**：把 4 个文档 + 单 HTML 自身 一起打包为 zip 文件，教师一次下载即可。

### 11.1 技术栈增量

新增两个库（CDN）：
- `jszip@3.10.1` → 把多个文件打包为 zip
- `file-saver@2.0.5` → 触发浏览器下载

CDN 引用：

```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/file-saver@2.0.5/dist/FileSaver.min.js"></script>
```

### 11.2 一键打包下载范式

```javascript
async function downloadAllAsZip() {
  const zip = new JSZip();
  // 1) 把 4 个文档（Excel/Word/PPT/PDF）的 Blob 加入 zip
  zip.file('题目表.xlsx', xlsxBlob);
  zip.file('教案.docx', docxBlob);
  zip.file('页面稿.pptx', pptxBlob);
  zip.file('备课包.pdf', pdfBlob);
  // 2) 把当前单 HTML 也加入 zip（保留交互界面供离线使用）
  const htmlBlob = new Blob([document.documentElement.outerHTML], { type: 'text/html' });
  zip.file('备课生成器.html', htmlBlob);
  // 3) 生成 zip Blob 并触发下载
  const zipBlob = await zip.generateAsync({ type: 'blob' });
  saveAs(zipBlob, '备课包.zip');
}

// 触发：一键下载按钮
document.getElementById('dl-all').addEventListener('click', downloadAllAsZip);
```

### 11.3 UI 增量

在 §4.2 界面骨架的 `#download` 区域加一个按钮：

```html
<button id="dl-all">📦 一键打包下载（zip）</button>
```

### 11.4 降级与容错

- JSZip 加载失败：仅保留 4 文档分别下载（V4 行为），并提示用户
- 4 文档中某个生成失败：zip 跳过该文件 + 在 README.md 标注缺失原因

### 11.5 强制测试门控

- CDN 链完整（cdnjs → jsdelivr → 本地）
- 5 文件全部成功加入 zip（4 文档 + HTML）
- 浏览器实测下载 zip 并解压
- 跨浏览器兼容
