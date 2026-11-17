# p5.js 互动课件生成指南

> 本文件是「AI 通识课专家 V3」技能的核心规范——指导如何为 AI 通识课各单元生成 p5.js 动态多媒体互动课件。课件目标：将抽象 AI 概念转化为可交互的 2D/3D 可视化演示，让学生在看、点、拖、调中理解 AI 原理。
>
> **版本策略（生产级基线）**：课件统一使用 **p5.js 2.x 稳定版**（如当前 `2.0.3`；以官方 https://p5js.org 最新 2.x 稳定版为准）。技能顶层标注「p5.js 2.x 专家」即指此基线——不得交付锁定旧版（如 1.11.0）的代码。若某环境仅支持 1.x，需在门控声明中暴露并降级说明（见第七章）。

---

## 一、课件标准结构

每个 p5.js 课件 = **一个完整 HTML 网页**（单文件 `index.html`，所有 JS/CSS 内嵌），用以下统一模板：

```text
┌──────────────────────────────────────────┐
│ [标题] AI 通识课 · 单元号 · 主题          │
├──────────────────────────────────────────┤
│                                          │
│        p5.js Canvas 核心可视化区          │
│        (动画 / 图表 / 对比演示)            │
│        ← 交互式，可点击拖拽调节 →          │
├──────────────────────────────────────────┤
│ [文字说明] 当前展示的关键概念 + 观察提示    │
├──────────────────────────────────────────┤
│ [控制面板] 按钮 / 滑块 / 下拉菜单 (可选)   │
├──────────────────────────────────────────┤
│ [教学要点] 本课件核心结论 (1-2 句话)       │
└──────────────────────────────────────────┘
```

### 代码引入标准

```html
<!-- 主用 cdnjs，备用 jsdelivr（onerror 自动回退，避免单一 CDN 不可达导致白屏） -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/2.0.3/p5.min.js"></script>
<script>
  if (typeof p5 === 'undefined') {
    document.write('<script src="https://cdn.jsdelivr.net/npm/p5@2.0.3/lib/p5.min.js"><\/script>');
  }
</script>
```

### 课件交付物

输出课件时，必须一并交付：
1. **完整 HTML 代码**（单文件，围栏标明 `html`，包含 `<style>` + `<script>`，CDN 引入 p5.js 2.x）
2. **使用说明**（Markdown 格式：怎么打开、怎么操作、核心概念映射）
3. **参数实验指南**（哪些值可调、调节后观察什么现象、推荐参数范围）
4. **学生探索任务**（基础/应用/挑战三层，对应原 system-prompt 八步流程的第七步）
5. **强制测试门控结果块**（见第七章 7.5，逐条 ✅/⏳ 勾选 + 说明，随交付物一并给出）

---

## 二、各模块课件适配方案

### 模块 A · 认知基础

#### A1 AI 的进化历程
- **方案**：交互式时间轴（水平滚动/缩放），里程碑节点可点击弹窗展示详情
- **核心元素**：年份刻度 + 事件气泡（大小与影响度成正比）+ 颜色渐变（从早期到现代）
- **交互**：拖拽平移时间轴、滚轮缩放、点击气泡弹出详情卡片
- **关键概念呈现**：Transformer (2017) → GPT 系列 → Scaling Laws → 涌现能力 → 多模态

#### A2 AI 是什么、不是什么
- **方案**：双列对比卡片，左侧"AI 能做到"（绿色）vs 右侧"AI 不能做到"（红色），中间用动画展示边界
- **核心元素**：卡片翻转动画、Jagged Frontier 边界曲线、Hallucination 示例弹出
- **交互**：点击卡片翻转查看详情、拖拽边界点改变锯齿形状
- **关键概念呈现**：符尧能力分层、Hallucination 结构性、Jagged Frontier

#### A3 协作哲学
- **方案**：Architect vs Executor 角色扮演流水线动画，展示任务从人→AI→人 的流转
- **核心元素**：左侧"Architect（人）"节点 → 箭头（携带任务卡片）→ 右侧"Executor（AI）"节点 → 返回箭头（携带结果卡片）→ 人审核节点
- **交互**：点击节点放大查看角色职责、拖拽调整任务复杂度（影响 AI 处理时间/质量）、切换场景（写代码/写报告/分析数据）
- **关键概念呈现**：Architect/Executor 分工、BCG 758 实验数据、Centaur Chess

---

### 模块 B · 工具操作

> B 模块是工具实操类，p5.js 互动课件定位为「操作引导 / 流程模拟」，而非替代真实软件实操；真实 TRAE IDE / SOLO 仍需学生在原环境练习。B 模块的 p5.js 可视化方案见本指南第二章 B1/B2；更细的工具实操指引见 `references/module-b-tools.md`。

#### B1 TRAE IDE（计算机 / 软件工程方向）
- **方案**：交互式功能导览——在 p5.js Canvas 上画出 IDE 界面骨架（侧边文件树 / 编辑区 / AI 对话面板），用高亮气泡逐步引导"代码生成→补全→调试"流程
- **核心元素**：IDE 界面线框图 + 步骤高亮气泡 + 每步对应的 C1/C2/C3 招式标注
- **交互**：点击步骤气泡播放该步动画、切换"用 AI / 不用 AI"对比同一任务耗时
- **关键概念呈现**：B1 作为 C/D 的计算机方向工具路径、Executor 角色在 IDE 中的体现

#### B2 TRAE Work·SOLO（全专业通用）
- **方案**：对话式协作模拟器——左侧 SOLO 对话框（可输入自然语言任务），右侧实时生成"任务卡片→拆解→执行→结果"的动画流转
- **核心元素**：对话框 + 任务流转管线（承接 C2 拆解、C3 验证节点高亮）+ 进度指示器
- **交互**：点击对话轮次查看 SOLO 内部如何调用 C1 Prompt / C2 拆解 / C3 验证
- **关键概念呈现**：SOLO 是"对话式 Architect/Executor 协作"的载体、全专业通用工具路径

---

### 模块 C · 方法论

#### C1 Prompt 工程基础
- **方案**：双栏输入输出对比器——左侧输入 Prompt（含五要素标注），右侧展示 AI 输出，可切换好/差 Prompt 对比
- **核心元素**：输入框 + 输出区 + 要素标注标签（Role/Task/Constraints/Examples/Format）+ 质量评分条
- **交互**：修改 Prompt 元素切换开关（开/关各要素），实时看到输出变化（用预设的输出映射模拟）
- **关键概念呈现**：五要素、CoT 效果、约束≠100% 遵守

#### C2 需求拆解与任务规划
- **方案**：树状分解图——根节点"总任务"逐级展开为子任务（可折叠/展开），每层显示验收标准
- **核心元素**：节点（任务描述 + 验收标准）+ 连线（依赖关系）+ 展开/折叠按钮
- **交互**：点击节点展开/折叠子任务、拖拽调整节点位置、点击验收标准高亮
- **关键概念呈现**：迭代式拆解、中间产物自包含、领域范式

#### C3 验证与闭环
- **方案**：四层纵深流程图——从"事前约束"→"事中审查"→"自动化验证"→"事后审计"，每层有具体动作卡片
- **核心元素**：流程图（从上到下四层）+ 每层可展开的"具体动作"子项 + 风险等级指示灯
- **交互**：点击每层展开/折叠子动作、拖拽风险滑块调整验证力度
- **关键概念呈现**：四层验证纵深、交叉审查、四大认知偏差警示

#### C4 多 Agent 协作
- **方案**：可编排的 Agent 协作图——拖拽创建 Agent 节点，连线定义串行/并行/交叉审查关系，预设场景模板
- **核心元素**：Agent 节点（可拖拽+连线）+ 编排模式切换（串行/并行/交叉审查）+ token 消耗计数器
- **交互**：拖拽排列 Agent、切换编排模式观察 token 变化、点击节点查看该 Agent 的任务
- **关键概念呈现**：Subagents/Teams/Dynamic、串行 vs 并行、契约先行

#### C5 复盘、沉淀与自动化
- **方案**：四级阶梯飞轮动画——从 Rules → Skills → Agents → Plugin 逐级上升，每一级有触发条件说明
- **核心元素**：循环飞轮（底部 Rules 最大、顶部 Plugin 最小，表示沉淀难度递增）+ 每级的触发条件弹窗
- **交互**：点击每级查看详情、点击飞轮触发一次循环动画、拖拽时间轴看沉淀历程
- **关键概念呈现**：四级阶梯、触发式沉淀、自动化生效、Jim Collins 飞轮

---

### 模块 D · 通用场景实练

#### D1 数据分析与可视化
- **方案**：交互式散点图/柱状图——内置示例数据集，可切换数据集、调整图表类型、拖拽数据点
- **核心元素**：Canvas 上的图表（轴标签 + 数据点/柱）+ 数据集选择器 + 图表类型切换按钮
- **交互**：鼠标悬停数据点显示值、拖拽改变数据点位置（观察回归线变化）、切换数据集
- **关键概念呈现**：六步分析流程、相关≠因果（关键强调）

#### D2 应用开发（Vibe Coding）
- **方案**：角色扮演进度条 + 对话气泡——产品经理（人）↔ AI 设计师/工程师的迭代对话可视化
- **核心元素**：左右对话气泡 + 中间迭代进度条 + 每个阶段标注角色和任务
- **交互**：点击阶段查看该阶段的典型对话示例、拖拽进度条回退到某阶段
- **关键概念呈现**：Vibe Coding 角色分工、5000 行魔咒、安全陷阱

---

### 模块 E · 专业应用层（跨学科适配）

> E 模块各专业的深度案例/数据/行业模板由院系教师主导；p5.js 课件定位为「专业场景可视化 + 方法论映射」，帮助用户直观看到"通识招式如何落到本专业"。以下按 E1-E5 给出适配方案骨架。

#### E1 计算机 / 软件工程
- **方案**：代码质量可视化——用 p5.js 画出"人工 Review vs AI 辅助"对同一段代码的 Bug 检出率对比条形图，或 CI/CD 流水线动画
- **关键概念呈现**：E1 工具路径=B1；C3 高强度验证（lint/单测自动化）；专业飞轮（团队规范沉淀为 Rules）

#### E2 经管 / 社科
- **方案**：竞品分析看板——交互式矩阵图（横轴"增速"、纵轴"壁垒"），拖拽企业气泡定位，点击查看 AI 辅助生成的剖析卡片
- **关键概念呈现**：E2 工具路径=B2；C2 金字塔原理拆解行业；C3 交叉核对数据口径、区分相关≠因果

#### E3 人文社科
- **方案**：文献关系网络——p5.js 力导向图展示文献引用/流派关系，点击节点弹出 AI 生成的综述要点（并标注"需人工核实引用"）
- **关键概念呈现**：E3 工具路径=B2；C3 重灾区（AI 编造文献）→ 逐条核对；学术诚信红线

#### E4 理工科
- **方案**：实验数据探索器——上传/内置 CSV 后，p5.js 实时绘制分布图、散点图，滑动控制置信区间/显著性水平，直观看到"相关≠因果"
- **关键概念呈现**：E4 工具路径=B2（+IDE 写计算脚本）；C3 单位/有效数字/统计方法验证；公式推导人工核对

#### E5 艺术与设计
- **方案**：创意发散画板——p5.js 生成式图案（用噪声/参数化图形），滑块控制"风格强度/随机性/约束度"，演示"AI 给 3 个差异化方向、人做审美终审"
- **关键概念呈现**：E5 工具路径=B2；C1 Role="资深设计师"约束；C3 验证原创性/可落地，审美终审在人

---

### 第一部分 · 核心理念演示（跨模块通用课件）

> 以下课件可用于课前导入或跨单元串讲，不绑定特定模块。

- **四大核心理念轮播**：Architect/Executor → Trust but Verify → 飞轮 → Jagged Frontier，每个理念一个卡片（自动轮播+手动翻页）
- **统一隐喻展示**：实习生/施工图纸/作品集——3 个隐喻卡片并列展示，点击展开详细解释
- **"锯齿状能力边界"体验器**：交互式绘图——画出你认为"AI 能/不能"的边界，与已知能力图对比，单击打点标记翻车位置

---

## 三、课件交付前测试清单（⚠️ 强制门控）

> **本清单是课件交付红线**：生成课件后、交付给用户前，**必须逐项完成以下检查且全部通过**。任一项未通过或无法确认，课件不得交付；无法在浏览器实测时，须明确声明已完成项与需用户实测项（见第七章）。
>
> **运行模式约定**：本技能所有 p5.js 课件统一采用**实例模式**（`new p5((p) => { ... })`），所有 p5 API 调用均带 `p.` 前缀（如 `p.createCanvas` / `p.background` / `p.mousePressed`），**禁止在实例模式 sketch 内混用全局式调用**（如裸写 `background()` / `createCanvas()`），这是 p5.js 最经典的静默运行失败陷阱。

- [ ] 使用 **p5.js 2.x** 稳定版 CDN 引入（cdnjs 主 + jsdelivr 备用，含 `typeof p5 === 'undefined'` 回退判断）
- [ ] Canvas 放在 `<div id="p5-container">` 中，且 `cnv.parent('p5-container')` 已挂接
- [ ] CSS 定义了页面布局（标题区 / Canvas 区 / 说明区 / 控制区 / 结论区）
- [ ] 采用**实例模式**：sketch 内所有 p5 调用均带 `p.` 前缀，无裸写全局式 API
- [ ] `p.setup` 中 `p.createCanvas()` 使用 `p.windowWidth/Height` 或父容器尺寸（响应式，非硬编码 700×420）
- [ ] 响应式：`p.windowResized` 已定义且实际调用 `p.resizeCanvas(...)`（非空函数）
- [ ] 交互事件回调（如用到 `mousePressed/keyPressed/mouseDragged`）在实例模式下显式绑定为 `p.mousePressed = ...` 等，且逻辑正确
- [ ] 交互控件使用 p5.js DOM 元素（`p.createButton/p.createSlider/p.createSelect`）或原生 HTML + 事件监听
- [ ] **中文渲染**：Canvas 上 `p.text()` 的中文正常显示（2D 模式依赖浏览器默认字体；若用 `WEBGL` 模式，`text()` 前必须 `p.loadFont('xxx.ttf/.otf')` 加载字体，默认字体在 WEBGL 下不显示中文/会报错）
- [ ] 所有函数名、常量名、URL 都确认为 p5.js 2.x 真实 API（不凭记忆编造；不确定时查官方文档）
- [ ] ⚠️ **禁用已移除 API（黑名单）**：`screenX/screenY/screenZ`、`modelX/modelY/modelZ` 等在 p5 2.x 中已被移除（1.x 可用），**禁止用于点击拾取 / 屏幕↔模型坐标互转**；3D 节点拾取改用「下拉列表选择」或「局部坐标近似法」，详见文末「附录：p5 2.x 常见 API 陷阱速查」
- [ ] 配色方案有足够对比度（可访问性：避免仅靠颜色传递信息）
- [ ] 代码注释：变量名英文（清晰表意）、注释中文（解释概念而非复述代码）
- [ ] 页面加载时无控制台错误；`setup()` 仅执行一次、`draw()` 正常循环、无 `draw()` 内阻塞/死循环
- [ ] 默认参数下可被非技术人员顺利操作

---

## 四、代码框架模板（实例模式 · 响应式 · 2.x）

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AI 通识课 · [单元号] · [主题]</title>
  <!-- 主用 cdnjs，备用 jsdelivr（onerror 自动回退） -->
  <script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/2.0.3/p5.min.js"></script>
  <script>
    if (typeof p5 === 'undefined') {
      document.write('<script src="https://cdn.jsdelivr.net/npm/p5@2.0.3/lib/p5.min.js"><\/script>');
    }
  </script>
  <style>
    /* 页面布局 */
    body { font-family: 'Noto Sans SC', sans-serif; margin: 0; background: #f4f6f9; }
    #header { background: #1a1a2e; color: #fff; padding: 16px 24px; }
    #main { display: flex; flex-direction: column; align-items: center; padding: 20px; }
    #p5-container { border-radius: 12px; overflow: hidden; box-shadow: 0 4px 24px rgba(0,0,0,0.12); }
    #legend { max-width: 800px; margin: 16px auto; padding: 16px 20px; background: #fff; border-radius: 8px; font-size: 14px; line-height: 1.8; }
    #controls { margin: 12px 0; display: flex; gap: 12px; flex-wrap: wrap; justify-content: center; }
    #conclusion { max-width: 800px; margin: 12px auto; padding: 12px 20px; background: #e8f5e9; border-left: 4px solid #4caf50; border-radius: 4px; font-weight: 600; }
  </style>
</head>
<body>
  <div id="header">
    <h1>AI 通识课 · [单元号] · [主题]</h1>
  </div>
  <div id="main">
    <div id="p5-container"></div>
    <div id="legend">
      <!-- 关键概念说明 -->
    </div>
    <div id="controls">
      <!-- 交互控件 -->
    </div>
    <div id="conclusion">
      <!-- 教学要点总结 -->
    </div>
  </div>
  <script>
    // ===== p5.js Sketch（实例模式）=====
    const sketch = (p) => {
      // 参数配置区（学生可调）
      let param1 = 0.5;
      let cnv;

      p.setup = () => {
        // 响应式画布：取窗口 90% 宽、80% 高，并限制最大尺寸保证不溢出
        const w = p.min(p.windowWidth * 0.9, 900);
        const h = p.min(p.windowHeight * 0.8, 560);
        cnv = p.createCanvas(w, h);
        cnv.parent('p5-container');
        // 初始化
      };

      p.draw = () => {
        p.background(255);
        // 核心可视化逻辑（注意：draw 内避免阻塞/死循环）
      };

      // 响应式：窗口缩放时真正重算画布尺寸
      p.windowResized = () => {
        const w = p.min(p.windowWidth * 0.9, 900);
        const h = p.min(p.windowHeight * 0.8, 560);
        p.resizeCanvas(w, h);
      };

      // 示例：交互回调需在实例模式下显式绑定（如用到鼠标交互）
      // p.mousePressed = () => { /* 点击逻辑 */ };
      // p.mouseDragged = () => { /* 拖拽逻辑 */ };
    };

    new p5(sketch);
  </script>
</body>
</html>
```

---

## 五、课件标注规范

每个课件代码内部必须包含以下注释块（放在 `<script>` 顶部或 HTML 注释中）：

```html
<!--
  [课件名称] AI 通识课 · [单元号] · [主题]
  [教学目标] 本课件帮助学生理解……（1-2 句）
  [操作方式] 点击/拖拽/调节滑块……（简述交互方式）
  [可调参数] param1 → 改变……效果；param2 → 调整……速度/大小
  [推荐探索] 基础：观察……变化；应用：修改参数看……；挑战：尝试添加……
  [相关概念] C1 Prompt 工程 / C3 验证闭环 / ……
  [p5.js 版本] 2.x（如 2.0.3）
  [运行模式] 实例模式（new p5(sketch)，p. 前缀）
-->
```

---

## 六、常见问题与解决方案

| 问题 | 解决方案 |
|------|---------|
| Canvas 不居中 | 用 `cnv.parent('p5-container')` + CSS `#main { display: flex; justify-content: center; }` |
| 按钮无反应 | 确认使用 `p.createButton()` 或原生 `<button>` + 事件监听；实例模式下不要漏写 `p.` 前缀 |
| 动画太卡 | 降低 Canvas 尺寸（≤800×500）；减少 `draw()` 内复杂计算 |
| 移动端太小 | 使用 `p.windowWidth` 自适应；字体至少 12px |
| 缩放后画布变形 | `p.windowResized()` 中调用 `p.resizeCanvas(...)` 时保留宽高比 |
| 中文显示为方框/空白 | 2D 模式确保 `<meta charset="UTF-8">` 且字体含中文（如 Noto Sans SC）；**WEBGL 模式下 `text()` 必须先用 `p.loadFont()` 加载 `.ttf/.otf` 字体**，否则中文不显示 |
| 白屏（CDN 不可达） | 检查网络；确认已配置 jsdelivr 备用源回退；或提示用户本地放置 p5.min.js 并改 `<script src="p5.min.js">` |

---

> **使用方式**：在生成课件代码时，先查阅本指南中对应的模块适配方案，选择推荐的可视化策略，按标准结构和模板生成完整 HTML 文件。每次输出课件时，必须包含代码 + 使用说明 + 参数实验指南 + 学生探索任务 + **强制测试门控结果块**五部分。

---

## 七、课件测试验证流程（⚠️ 强制）

> 对应本技能 SKILL.md「强制测试门控（课件交付红线）」。课件不是"写完就发"，必须经过验证方可交付。

### 7.1 静态自检（必做，对照第三章清单逐项）
- 括号/引号是否匹配；`push()/pop()` 是否配对
- **实例模式一致性**：sketch 内所有 p5 调用是否都带 `p.` 前缀，无混用全局式
- 变量是否先定义后使用；函数名是否为 p5.js 2.x 真实 API（不凭记忆编造，不确定时查官方文档）
- **禁用已移除 API**：确认未使用 `screenX/screenY/screenZ`、`modelX/modelY/modelZ`（2.x 已移除）；3D 点击拾取不得依赖屏幕投影函数，改用下拉列表 / 局部坐标近似（见文末附录）
- 2D 与 WEBGL 坐标系是否混淆；是否存在 `draw()` 内重复创建大量对象
- 是否兼顾窗口大小变化（`p.windowResized` 且实际 `resizeCanvas`）；是否有键盘之外的交互替代方式
- **中文渲染**：Canvas `p.text()` 中文是否正常（2D 用默认字体；WEBGL 需 `loadFont`）
- **事件绑定**：用到的 `mousePressed/keyPressed/mouseDragged` 是否在实例模式下显式绑定为 `p.xxx = ...`
- 资源路径是否有效；数组是否可能越界；是否存在未定义对象；有无死循环/`draw()` 内阻塞

### 7.2 语法验证（硬性要求）
- 将 `<script>` 内的 sketch JS 提取为临时 `.js` 文件，运行 `node --check 文件名.js` 验证语法（p5 全局函数调用在语法层不报错，仅查语法）
- 若环境无 Node，可用 `npx -y acorn` 或浏览器控制台做等价语法检查
- **硬约束**：环境无 Node 时**必须记录"跳过语法验证"及原因**，并在 7.4 透明声明与 7.5 交付判定中显式暴露——不得默认视为通过

### 7.3 逻辑预演（必做）
- 在脑中按"点击/拖拽/调节"走查主交互路径：能否到达预期状态、有无死路、边界值（最小/最大参数）是否崩溃
- 对照该单元「关键概念呈现」确认可视化确实表达了目标概念

### 7.4 透明声明（交付时必附）
在交付课件时，必须明确告知用户：
- ✅ 已完成的检查：静态自检（具体项）/ 语法验证（node --check 通过 或 跳过原因）/ 逻辑预演结论
- ⏳ 需用户在浏览器实测的项：真实渲染效果、交互流畅度、跨浏览器兼容性、CDN 可达性
- **不得声称"已验证可运行"**，除非已在真实浏览器环境跑通

### 7.5 交付判定
- 7.1（全过）+ 7.2（通过或已声明跳过原因）+ 7.3（通过）+ 7.4（已声明）→ 可交付
- **交付物末尾必须附「强制测试门控结果」块**，逐条列出 7.1 勾选项（✅/⏳）+ 7.2 验证结论 + 7.4 透明声明，作为可审计证据
- 任一项未通过 → **不得交付**，先修复并重新走 7.1–7.4

---

## 附录：p5 2.x 常见 API 陷阱速查（⚠️ 防复发）

> 本附录由「AI 历史 3D 课件」实战踩坑沉淀：课件在 p5 2.0.3 下因调用 `p.screenX()` 触发 `TypeError: p.screenX is not a function`，导致 `draw()` 每帧崩溃、时间光标不绘制、点击/播放全失效。根因是**把 1.x 可用 API 当成 2.x 真实 API 凭记忆调用**。以下坑必须固化规避，生成任何 WEBGL/交互课件前强制对照本表。

### A. 已移除 / 改名 API（2.x 禁止使用）

| 1.x 写法（已失效） | 2.x 现状 | 正确替代 |
|------|------|------|
| `p.screenX(x,y,z)` / `screenY` / `screenZ` | **2.x 已移除** | 不要做屏幕投影；3D 拾取用下拉列表 / 原生 DOM 选择，或自实现射线投射 |
| `p.modelX(x,y,z)` / `modelY` / `modelZ` | **2.x 已移除** | 同上，避免模型↔屏幕坐标互转 |
| `createCanvas(w,h)` 硬编码旧版 | 语法保留但应统一 2.x | 用 2.0.3 CDN，实例模式，响应式尺寸 |

### B. 已知易错点

- **WEBGL 中文渲染**：默认字体在 WEBGL 下不显示中文，必须 `p.loadFont('xxx.ttf/.otf')` 后方可 `p.text()``；**稳妥做法（本技能推荐范式）：WEBGL 画布内不用中文 text，中文全部走 HTML DOM 信息层**。
- **DOM 控件**：优先用原生 `<button>/<input>/<select>` + `addEventListener`，比 `p.createButton().mousePressed()` 在实例模式 + 全局 `p.mousePressed` 共存时更可靠。
- **draw 前置崩溃**：任何在 `draw()` 中、时间光标/关键绘制**之前**的报错（如调用不存在的 API），都会让后续绘制被跳过——务必把关键可视化（如时间光标竖线）放在 `draw()` 末尾，或确保前置代码零崩溃。

### C. 正确范式：3D 节点「下拉列表」拾取（替代 screenX 投影）

```javascript
// setup 中：用原生 select 列出所有里程碑，change 时聚焦对应节点
const sel = document.getElementById('nodeSelect');
events.forEach((ev, i) => {
  const opt = document.createElement('option');
  opt.value = i; opt.textContent = ev.yr + ' · ' + ev.title;
  sel.appendChild(opt);
});
sel.addEventListener('change', (e) => {
  const v = parseInt(e.target.value, 10);
  if (v >= 0) { selectedIndex = v; updateInfo(); }  // 对应 3D 球高亮由 selectedIndex 驱动
});

// ❌ 错误范式（2.x 必崩，禁止）：
// const sx = p.screenX(n.x, n.y, n.z);  // TypeError: not a function
// 若需点击 3D 对象，用 selectedIndex 驱动的拾取/高亮，而非屏幕投影函数
```
