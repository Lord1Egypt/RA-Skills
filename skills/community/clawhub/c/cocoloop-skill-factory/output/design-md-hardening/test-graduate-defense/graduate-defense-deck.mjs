import pptxgen from "pptxgenjs";

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE";
pptx.author = "OpenAI Codex";
pptx.company = "OpenAI";
pptx.subject = "Graduate defense presentation";
pptx.title = "研究生毕业答辩示例稿";
pptx.lang = "zh-CN";
pptx.theme = {
  headFontFace: "PingFang SC",
  bodyFontFace: "PingFang SC",
  lang: "zh-CN",
};

const C = {
  black: "0B0C10",
  white: "F7F7F2",
  ink: "121417",
  muted: "67707C",
  blue: "2563EB",
  paleBlue: "EAF1FF",
  line: "D9DEE5",
  panel: "F2F4F7",
  darkPanel: "171A20",
  green: "0F9F6E",
  amber: "C88A12",
};

function pageNo(slide, n) {
  slide.addText(String(n), {
    x: 12.2,
    y: 6.72,
    w: 0.45,
    h: 0.18,
    fontFace: "PingFang SC",
    fontSize: 10,
    color: C.muted,
    align: "right",
  });
}

function topRule(slide, dark = false) {
  slide.addShape(pptx.ShapeType.rect, {
    x: 0.72,
    y: 0.58,
    w: 0.9,
    h: 0.05,
    line: { color: C.blue, transparency: 100 },
    fill: { color: C.blue },
  });
  slide.addText("硕士学位论文答辩", {
    x: 0.74,
    y: 0.8,
    w: 2.4,
    h: 0.18,
    fontFace: "PingFang SC",
    fontSize: 10,
    bold: true,
    color: dark ? "B8C0CC" : C.blue,
  });
}

function titleBlock(slide, title, summary, dark = false) {
  slide.addText(title, {
    x: 0.72,
    y: 1.08,
    w: 6.9,
    h: 0.72,
    fontFace: "PingFang SC",
    fontSize: 24,
    bold: true,
    color: dark ? C.white : C.ink,
  });
  slide.addText(summary, {
    x: 0.74,
    y: 1.74,
    w: 5.5,
    h: 0.28,
    fontFace: "PingFang SC",
    fontSize: 11,
    color: dark ? "B8C0CC" : C.muted,
  });
  slide.addShape(pptx.ShapeType.line, {
    x: 0.74,
    y: 2.16,
    w: 11.0,
    h: 0,
    line: { color: dark ? "313847" : C.line, width: 1 },
  });
}

function addCover() {
  const slide = pptx.addSlide();
  slide.background = { color: C.black };
  topRule(slide, true);
  slide.addText("研究生毕业答辩", {
    x: 0.72,
    y: 1.22,
    w: 4.4,
    h: 0.6,
    fontFace: "PingFang SC",
    fontSize: 28,
    bold: true,
    color: C.white,
  });
  slide.addText("面向复杂场景的多模态学习方法研究", {
    x: 0.72,
    y: 2.02,
    w: 7.2,
    h: 1.0,
    fontFace: "PingFang SC",
    fontSize: 23,
    color: C.white,
  });
  slide.addText("一句话结论：在复杂噪声和模态缺失条件下，方法仍能保持稳定提升。", {
    x: 0.74,
    y: 3.28,
    w: 6.1,
    h: 0.38,
    fontFace: "PingFang SC",
    fontSize: 12,
    color: "C4CAD4",
  });
  slide.addText("答辩人 张某某\n计算机科学与技术\n指导教师 李某某\n2026 年 4 月", {
    x: 0.76,
    y: 4.78,
    w: 2.1,
    h: 1.05,
    fontFace: "PingFang SC",
    fontSize: 14,
    color: C.white,
    breakLine: true,
  });

  slide.addShape(pptx.ShapeType.roundRect, {
    x: 8.9,
    y: 1.06,
    w: 3.2,
    h: 4.98,
    rectRadius: 0.16,
    line: { color: "2E3440", width: 1 },
    fill: { color: C.darkPanel },
  });
  const items = [
    ["研究背景", "问题为什么成立"],
    ["方法设计", "框架如何搭建"],
    ["实验结果", "效果是否真实"],
    ["总结展望", "价值与下一步"],
  ];
  items.forEach(([a, b], i) => {
    const y = 1.64 + i * 1.03;
    slide.addText(a, {
      x: 9.26,
      y,
      w: 1.4,
      h: 0.22,
      fontFace: "PingFang SC",
      fontSize: 15,
      bold: i === 2,
      color: C.white,
    });
    slide.addText(b, {
      x: 9.26,
      y: y + 0.28,
      w: 1.8,
      h: 0.16,
      fontFace: "PingFang SC",
      fontSize: 10,
      color: "98A1AE",
    });
    slide.addShape(pptx.ShapeType.line, {
      x: 9.24,
      y: y + 0.56,
      w: 2.2,
      h: 0,
      line: { color: i === 2 ? C.blue : "3B4351", width: i === 2 ? 2 : 1 },
    });
  });
}

function addAgenda() {
  const slide = pptx.addSlide();
  slide.background = { color: C.white };
  topRule(slide);
  titleBlock(slide, "答辩结构", "先给结论，再展开方法、实验与价值。");
  const rows = [
    ["01", "研究背景与问题", "场景难点、问题边界、研究目标"],
    ["02", "方法设计", "框架、模块、核心机制"],
    ["03", "实验与结果", "设置、指标、对比、消融"],
    ["04", "总结与展望", "结论、价值、后续工作"],
  ];
  rows.forEach(([num, title, desc], i) => {
    const y = 2.56 + i * 0.96;
    slide.addText(num, {
      x: 0.86,
      y,
      w: 0.56,
      h: 0.2,
      fontFace: "PingFang SC",
      fontSize: 12,
      bold: true,
      color: C.blue,
    });
    slide.addText(title, {
      x: 1.5,
      y: y - 0.02,
      w: 3.0,
      h: 0.22,
      fontFace: "PingFang SC",
      fontSize: 17,
      bold: true,
      color: C.ink,
    });
    slide.addText(desc, {
      x: 4.84,
      y: y - 0.01,
      w: 3.8,
      h: 0.22,
      fontFace: "PingFang SC",
      fontSize: 11,
      color: C.muted,
    });
    slide.addShape(pptx.ShapeType.line, {
      x: 0.86,
      y: y + 0.38,
      w: 10.7,
      h: 0,
      line: { color: C.line, width: 1 },
    });
  });
  slide.addShape(pptx.ShapeType.roundRect, {
    x: 9.36,
    y: 2.52,
    w: 2.32,
    h: 2.82,
    rectRadius: 0.14,
    line: { color: C.line, width: 1 },
    fill: { color: C.panel },
  });
  slide.addText("答辩节奏", {
    x: 9.68,
    y: 2.82,
    w: 1.0,
    h: 0.18,
    fontFace: "PingFang SC",
    fontSize: 11,
    color: C.muted,
  });
  slide.addText("问题\n→ 方法\n→ 结果\n→ 价值", {
    x: 9.66,
    y: 3.26,
    w: 1.2,
    h: 1.36,
    fontFace: "PingFang SC",
    fontSize: 18,
    bold: true,
    color: C.ink,
    breakLine: true,
    align: "center",
  });
  pageNo(slide, 2);
}

function addChallengeCards() {
  const slide = pptx.addSlide();
  slide.background = { color: C.white };
  topRule(slide);
  titleBlock(slide, "研究背景与问题", "问题页不再堆条目，而是先把难点拆成可见结构。");
  const cards = [
    ["场景复杂", "多源异构输入同时存在", "文本、图像、结构化特征共同决定结果。"],
    ["噪声显著", "模态缺失与标签稀缺", "真实场景中存在模态不完整与标注不足。"],
    ["对齐困难", "共享语义空间不稳定", "模态之间很难在噪声条件下保持一致表达。"],
  ];
  cards.forEach(([title, key, body], i) => {
    const x = 0.8 + i * 4.02;
    slide.addShape(pptx.ShapeType.roundRect, {
      x,
      y: 2.56,
      w: 3.48,
      h: 2.82,
      rectRadius: 0.12,
      line: { color: C.line, width: 1 },
      fill: { color: i === 1 ? C.paleBlue : C.panel },
    });
    slide.addText(title, {
      x: x + 0.28,
      y: 2.84,
      w: 1.3,
      h: 0.2,
      fontFace: "PingFang SC",
      fontSize: 16,
      bold: true,
      color: C.ink,
    });
    slide.addText(key, {
      x: x + 0.28,
      y: 3.24,
      w: 2.6,
      h: 0.35,
      fontFace: "PingFang SC",
      fontSize: 13,
      color: i === 1 ? C.blue : C.muted,
      bold: i === 1,
    });
    slide.addText(body, {
      x: x + 0.28,
      y: 3.86,
      w: 2.82,
      h: 0.78,
      fontFace: "PingFang SC",
      fontSize: 11,
      color: C.muted,
      valign: "mid",
    });
  });
  slide.addText("核心研究目标：在复杂场景和有限监督下，提升多模态学习的稳定性与泛化能力。", {
    x: 0.86,
    y: 5.92,
    w: 8.4,
    h: 0.28,
    fontFace: "PingFang SC",
    fontSize: 14,
    bold: true,
    color: C.ink,
  });
  pageNo(slide, 3);
}

function addContributionSlide() {
  const slide = pptx.addSlide();
  slide.background = { color: C.white };
  topRule(slide);
  titleBlock(slide, "研究目标与论文贡献", "先给结论，再把贡献拆成三块独立可见的内容。");
  const cols = [
    ["贡献一", "动态对齐机制", "根据样本质量自适应调整模态权重。"],
    ["贡献二", "一致性约束", "降低噪声扰动带来的语义漂移。"],
    ["贡献三", "完整实验验证", "在公开数据集和自建数据集上验证有效性。"],
  ];
  cols.forEach(([title, big, body], i) => {
    const x = 0.82 + i * 4.0;
    slide.addText(title, {
      x,
      y: 2.6,
      w: 0.9,
      h: 0.18,
      fontFace: "PingFang SC",
      fontSize: 10,
      bold: true,
      color: C.blue,
    });
    slide.addText(big, {
      x,
      y: 3.0,
      w: 2.5,
      h: 0.48,
      fontFace: "PingFang SC",
      fontSize: 20,
      bold: true,
      color: C.ink,
    });
    slide.addText(body, {
      x,
      y: 3.72,
      w: 2.88,
      h: 0.72,
      fontFace: "PingFang SC",
      fontSize: 12,
      color: C.muted,
    });
    slide.addShape(pptx.ShapeType.line, {
      x,
      y: 4.72,
      w: 2.92,
      h: 0,
      line: { color: C.line, width: 1 },
    });
  });
  slide.addText("这三项贡献共同回答了论文的核心问题：为什么方法有效，为什么结果可信。", {
    x: 0.84,
    y: 5.46,
    w: 6.2,
    h: 0.24,
    fontFace: "PingFang SC",
    fontSize: 12,
    color: C.muted,
  });
  pageNo(slide, 4);
}

function addMethodFlow() {
  const slide = pptx.addSlide();
  slide.background = { color: C.white };
  topRule(slide);
  titleBlock(slide, "方法总览", "方法页用流程图承接逻辑，不再只用段落描述模块关系。");
  const stages = [
    ["输入层", "文本 / 图像 / 结构化特征"],
    ["编码层", "独立提取多模态表示"],
    ["融合层", "动态对齐与权重聚合"],
    ["约束层", "一致性损失与鲁棒训练"],
    ["输出层", "分类结果与解释分析"],
  ];
  stages.forEach(([title, sub], i) => {
    const x = 0.84 + i * 2.34;
    slide.addShape(pptx.ShapeType.roundRect, {
      x,
      y: 3.0,
      w: 1.88,
      h: 1.16,
      rectRadius: 0.1,
      line: { color: C.line, width: 1 },
      fill: { color: i === 2 ? C.paleBlue : C.panel },
    });
    slide.addText(title, {
      x: x + 0.16,
      y: 3.28,
      w: 1.2,
      h: 0.2,
      fontFace: "PingFang SC",
      fontSize: 14,
      bold: true,
      color: C.ink,
      align: "center",
    });
    slide.addText(sub, {
      x: x + 0.14,
      y: 3.62,
      w: 1.56,
      h: 0.3,
      fontFace: "PingFang SC",
      fontSize: 10,
      color: C.muted,
      align: "center",
    });
    if (i < stages.length - 1) {
      slide.addShape(pptx.ShapeType.line, {
        x: x + 1.88,
        y: 3.58,
        w: 0.46,
        h: 0,
        line: { color: C.blue, width: 2, beginArrowType: "none", endArrowType: "triangle" },
      });
    }
  });
  slide.addText("方法主线：先分模态建模，再在融合层解决对齐问题，最后通过约束层稳住表示空间。", {
    x: 0.84,
    y: 5.2,
    w: 7.0,
    h: 0.24,
    fontFace: "PingFang SC",
    fontSize: 12,
    color: C.muted,
  });
  pageNo(slide, 5);
}

function addModuleDeepDive() {
  const slide = pptx.addSlide();
  slide.background = { color: C.white };
  topRule(slide);
  titleBlock(slide, "核心模块解析", "把重点模块拆成主结论、机制图和补充说明三层。");
  slide.addShape(pptx.ShapeType.roundRect, {
    x: 0.9,
    y: 2.72,
    w: 5.5,
    h: 2.88,
    rectRadius: 0.12,
    line: { color: C.line, width: 1 },
    fill: { color: C.panel },
  });
  const nodes = [
    { x: 1.3, y: 3.24, t: "样本质量评估" },
    { x: 3.0, y: 3.24, t: "模态权重更新" },
    { x: 4.72, y: 3.24, t: "融合结果输出" },
  ];
  nodes.forEach((node) => {
    slide.addShape(pptx.ShapeType.roundRect, {
      x: node.x,
      y: node.y,
      w: 1.22,
      h: 0.72,
      rectRadius: 0.08,
      line: { color: C.blue, width: 1.2 },
      fill: { color: "FFFFFF" },
    });
    slide.addText(node.t, {
      x: node.x + 0.08,
      y: node.y + 0.18,
      w: 1.06,
      h: 0.24,
      fontFace: "PingFang SC",
      fontSize: 10,
      color: C.ink,
      align: "center",
    });
  });
  slide.addShape(pptx.ShapeType.line, {
    x: 2.52,
    y: 3.6,
    w: 0.48,
    h: 0,
    line: { color: C.blue, width: 2, endArrowType: "triangle" },
  });
  slide.addShape(pptx.ShapeType.line, {
    x: 4.22,
    y: 3.6,
    w: 0.5,
    h: 0,
    line: { color: C.blue, width: 2, endArrowType: "triangle" },
  });
  slide.addText("主结论", {
    x: 6.94,
    y: 2.88,
    w: 0.9,
    h: 0.18,
    fontFace: "PingFang SC",
    fontSize: 10,
    bold: true,
    color: C.blue,
  });
  slide.addText("动态对齐模块能够根据输入质量，自动降低低价值模态对结果的干扰。", {
    x: 6.94,
    y: 3.28,
    w: 4.2,
    h: 0.78,
    fontFace: "PingFang SC",
    fontSize: 19,
    bold: true,
    color: C.ink,
  });
  slide.addText(
    [
      { text: "机制一：", options: { bold: true } },
      { text: "根据样本质量动态调整模态权重。", options: {} },
      { text: "机制二：", options: { breakLine: true, bold: true } },
      { text: "在模态缺失条件下保留主要判别信息。", options: {} },
      { text: "机制三：", options: { breakLine: true, bold: true } },
      { text: "降低固定融合策略导致的性能波动。", options: {} },
    ],
    {
      x: 6.96,
      y: 4.44,
      w: 4.1,
      h: 1.18,
      fontFace: "PingFang SC",
      fontSize: 12,
      color: C.muted,
    },
  );
  pageNo(slide, 6);
}

function addExperimentDesign() {
  const slide = pptx.addSlide();
  slide.background = { color: C.white };
  topRule(slide);
  titleBlock(slide, "实验设计", "实验页用卡片和结构图说明数据、对比方法与指标。");
  const cards = [
    ["数据集", "公开数据集 A\n自建数据集 B"],
    ["对比方法", "单模态基线\n早期融合\n后期融合"],
    ["评估指标", "Accuracy\nF1\nAUC"],
  ];
  cards.forEach(([t, body], i) => {
    const x = 0.86 + i * 3.66;
    slide.addShape(pptx.ShapeType.roundRect, {
      x,
      y: 2.72,
      w: 3.18,
      h: 1.5,
      rectRadius: 0.1,
      line: { color: C.line, width: 1 },
      fill: { color: i === 2 ? C.paleBlue : C.panel },
    });
    slide.addText(t, {
      x: x + 0.24,
      y: 3.0,
      w: 1.0,
      h: 0.18,
      fontFace: "PingFang SC",
      fontSize: 14,
      bold: true,
      color: C.ink,
    });
    slide.addText(body, {
      x: x + 0.24,
      y: 3.34,
      w: 1.8,
      h: 0.48,
      fontFace: "PingFang SC",
      fontSize: 11,
      color: C.muted,
      breakLine: true,
    });
  });
  slide.addText("评估逻辑", {
    x: 0.88,
    y: 4.9,
    w: 1.0,
    h: 0.18,
    fontFace: "PingFang SC",
    fontSize: 10,
    bold: true,
    color: C.blue,
  });
  const flow = [
    ["训练集", 0.96],
    ["验证集", 3.4],
    ["测试集", 5.84],
    ["对比分析", 8.28],
  ];
  flow.forEach(([label, x]) => {
    slide.addShape(pptx.ShapeType.roundRect, {
      x,
      y: 5.26,
      w: 1.6,
      h: 0.78,
      rectRadius: 0.08,
      line: { color: C.line, width: 1 },
      fill: { color: "FFFFFF" },
    });
    slide.addText(label, {
      x: x + 0.16,
      y: 5.54,
      w: 1.2,
      h: 0.2,
      fontFace: "PingFang SC",
      fontSize: 12,
      bold: true,
      color: C.ink,
      align: "center",
    });
  });
  [2.56, 5.0, 7.44].forEach((x) => {
    slide.addShape(pptx.ShapeType.line, {
      x,
      y: 5.64,
      w: 0.42,
      h: 0,
      line: { color: C.blue, width: 2, endArrowType: "triangle" },
    });
  });
  pageNo(slide, 7);
}

function addResultsSlide() {
  const slide = pptx.addSlide();
  slide.background = { color: C.white };
  topRule(slide);
  titleBlock(slide, "实验结果", "结果页先看指标卡，再看对比条，最后补一句结论。");
  const metrics = [
    ["Accuracy", "+3.8%", C.ink],
    ["F1", "+4.5%", C.blue],
    ["AUC", "+2.9%", C.ink],
  ];
  metrics.forEach(([name, value, color], i) => {
    const x = 0.86 + i * 3.86;
    slide.addShape(pptx.ShapeType.roundRect, {
      x,
      y: 2.72,
      w: 3.34,
      h: 1.58,
      rectRadius: 0.1,
      line: { color: C.line, width: 1 },
      fill: { color: i === 1 ? C.paleBlue : C.panel },
    });
    slide.addText(name, {
      x: x + 0.22,
      y: 3.0,
      w: 0.9,
      h: 0.18,
      fontFace: "PingFang SC",
      fontSize: 11,
      color: C.muted,
    });
    slide.addText(value, {
      x: x + 0.2,
      y: 3.28,
      w: 1.4,
      h: 0.42,
      fontFace: "PingFang SC",
      fontSize: 25,
      bold: true,
      color,
    });
    slide.addText("相对最优基线", {
      x: x + 0.22,
      y: 3.74,
      w: 1.2,
      h: 0.16,
      fontFace: "PingFang SC",
      fontSize: 10,
      color: C.muted,
    });
  });
  const bars = [
    ["数据集 A", 0.81, 0.86, 4.9],
    ["数据集 B", 0.78, 0.84, 5.58],
  ];
  bars.forEach(([label, base, ours, y]) => {
    slide.addText(label, {
      x: 0.92,
      y,
      w: 0.9,
      h: 0.16,
      fontFace: "PingFang SC",
      fontSize: 11,
      color: C.muted,
    });
    slide.addShape(pptx.ShapeType.rect, {
      x: 1.86,
      y: y + 0.04,
      w: 4.8 * base,
      h: 0.18,
      line: { color: "B8C0CC", transparency: 100 },
      fill: { color: "B8C0CC" },
    });
    slide.addShape(pptx.ShapeType.rect, {
      x: 1.86,
      y: y + 0.34,
      w: 4.8 * ours,
      h: 0.18,
      line: { color: C.blue, transparency: 100 },
      fill: { color: C.blue },
    });
    slide.addText(`基线 ${Math.round(base * 100)}%`, {
      x: 6.9,
      y: y - 0.02,
      w: 1.0,
      h: 0.16,
      fontFace: "PingFang SC",
      fontSize: 10,
      color: C.muted,
    });
    slide.addText(`本文 ${Math.round(ours * 100)}%`, {
      x: 6.9,
      y: y + 0.28,
      w: 1.0,
      h: 0.16,
      fontFace: "PingFang SC",
      fontSize: 10,
      color: C.blue,
    });
  });
  slide.addText("结果结论：提出方法在两个数据集上的主指标都取得最优，且模态缺失时优势更明显。", {
    x: 8.2,
    y: 4.9,
    w: 3.4,
    h: 1.08,
    fontFace: "PingFang SC",
    fontSize: 16,
    bold: true,
    color: C.ink,
    valign: "mid",
  });
  pageNo(slide, 8);
}

function addAblationSlide() {
  const slide = pptx.addSlide();
  slide.background = { color: C.white };
  topRule(slide);
  titleBlock(slide, "消融与分析", "用矩阵表达模块作用，不再只列口头解释。");
  const left = 1.1;
  const top = 2.8;
  const cellW = 2.3;
  const cellH = 1.18;
  const headers = ["关闭动态对齐", "关闭一致性约束"];
  headers.forEach((h, i) => {
    slide.addShape(pptx.ShapeType.roundRect, {
      x: left + (i + 1) * cellW,
      y: top,
      w: cellW,
      h: cellH,
      rectRadius: 0.06,
      line: { color: C.line, width: 1 },
      fill: { color: C.panel },
    });
    slide.addText(h, {
      x: left + (i + 1) * cellW + 0.18,
      y: top + 0.4,
      w: 1.92,
      h: 0.24,
      fontFace: "PingFang SC",
      fontSize: 11,
      align: "center",
      color: C.ink,
    });
  });
  const rows = [
    ["性能变化", ["-2.8%", "-1.9%"]],
    ["鲁棒性变化", ["显著下降", "中度下降"]],
  ];
  rows.forEach(([label, values], r) => {
    slide.addShape(pptx.ShapeType.roundRect, {
      x: left,
      y: top + (r + 1) * cellH,
      w: cellW,
      h: cellH,
      rectRadius: 0.06,
      line: { color: C.line, width: 1 },
      fill: { color: C.panel },
    });
    slide.addText(label, {
      x: left + 0.2,
      y: top + (r + 1) * cellH + 0.42,
      w: 1.9,
      h: 0.22,
      fontFace: "PingFang SC",
      fontSize: 12,
      bold: true,
      align: "center",
      color: C.ink,
    });
    values.forEach((value, c) => {
      slide.addShape(pptx.ShapeType.roundRect, {
        x: left + (c + 1) * cellW,
        y: top + (r + 1) * cellH,
        w: cellW,
        h: cellH,
        rectRadius: 0.06,
        line: { color: C.line, width: 1 },
        fill: { color: c === 0 ? "FFF4F1" : "F7F9FC" },
      });
      slide.addText(value, {
        x: left + (c + 1) * cellW + 0.18,
        y: top + (r + 1) * cellH + 0.38,
        w: 1.92,
        h: 0.3,
        fontFace: "PingFang SC",
        fontSize: 18,
        bold: true,
        align: "center",
        color: c === 0 ? "D94827" : C.ink,
      });
    });
  });
  slide.addText("解释：动态对齐模块对总体性能的贡献最大，一致性约束对复杂场景的稳定性贡献更明显。", {
    x: 8.55,
    y: 3.28,
    w: 3.0,
    h: 1.24,
    fontFace: "PingFang SC",
    fontSize: 15,
    bold: true,
    color: C.ink,
    valign: "mid",
  });
  slide.addText("因此，方法有效性不是单点提升，而是结构层面的整体改善。", {
    x: 8.56,
    y: 4.86,
    w: 2.8,
    h: 0.56,
    fontFace: "PingFang SC",
    fontSize: 11,
    color: C.muted,
  });
  pageNo(slide, 9);
}

function addClosing() {
  const slide = pptx.addSlide();
  slide.background = { color: C.black };
  topRule(slide, true);
  slide.addText("总结与展望", {
    x: 0.74,
    y: 1.18,
    w: 3.2,
    h: 0.6,
    fontFace: "PingFang SC",
    fontSize: 26,
    bold: true,
    color: C.white,
  });
  const blocks = [
    ["结论", "方法在复杂场景下保持稳定提升。"],
    ["价值", "多模态动态对齐在真实任务中具有实践意义。"],
    ["展望", "继续扩展到更大规模和更低监督场景。"],
  ];
  blocks.forEach(([title, body], i) => {
    const x = 0.86 + i * 4.0;
    slide.addText(title, {
      x,
      y: 2.48,
      w: 0.8,
      h: 0.18,
      fontFace: "PingFang SC",
      fontSize: 10,
      bold: true,
      color: C.blue,
    });
    slide.addText(body, {
      x,
      y: 2.9,
      w: 2.9,
      h: 0.78,
      fontFace: "PingFang SC",
      fontSize: 18,
      bold: true,
      color: C.white,
    });
  });
  slide.addShape(pptx.ShapeType.line, {
    x: 0.86,
    y: 4.58,
    w: 10.8,
    h: 0,
    line: { color: "2D3440", width: 1 },
  });
  const roadmap = ["论文定稿", "答辩修改", "代码开源", "后续研究"];
  roadmap.forEach((label, i) => {
    const x = 1.1 + i * 2.85;
    slide.addShape(pptx.ShapeType.ellipse, {
      x,
      y: 5.12,
      w: 0.28,
      h: 0.28,
      line: { color: i === 3 ? C.blue : "556071", width: 1 },
      fill: { color: i === 3 ? C.blue : "556071" },
    });
    if (i < roadmap.length - 1) {
      slide.addShape(pptx.ShapeType.line, {
        x: x + 0.28,
        y: 5.26,
        w: 2.57,
        h: 0,
        line: { color: "556071", width: 1.2 },
      });
    }
    slide.addText(label, {
      x: x - 0.2,
      y: 5.54,
      w: 0.9,
      h: 0.2,
      fontFace: "PingFang SC",
      fontSize: 11,
      color: C.white,
      align: "center",
    });
  });
  slide.addText("感谢各位老师批评指正", {
    x: 0.86,
    y: 6.2,
    w: 3.0,
    h: 0.24,
    fontFace: "PingFang SC",
    fontSize: 12,
    color: "B8C0CC",
  });
  pageNo(slide, 10);
}

addCover();
addAgenda();
addChallengeCards();
addContributionSlide();
addMethodFlow();
addModuleDeepDive();
addExperimentDesign();
addResultsSlide();
addAblationSlide();
addClosing();

await pptx.writeFile({ fileName: "graduate-defense-demo.pptx" });
