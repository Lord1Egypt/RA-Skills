const pptxgen = require("pptxgenjs");
const pres = new pptxgen();
pres.layout = "LAYOUT_16x9";
pres.title = "C++函数·素数计数（小学趣味版）";

// ─── 主题色 ───────────────────────────────────────────
const BG      = "FFFBF0";   // 暖白底
const DEEP    = "1A1A2E";   // 深蓝黑
const PURPLE  = "7C3AED";   // 紫
const BLUE    = "2563EB";   // 蓝
const TEAL    = "0891B2";   // 青
const GREEN   = "059669";   // 绿
const ORANGE  = "EA580C";   // 橙
const PINK    = "DB2777";   // 粉
const YELLOW  = "D97706";   // 黄
const RED     = "DC2626";   // 红
const WHITE   = "FFFFFF";
const GRAY    = "64748B";
const DARK    = "1E293B";
const CODBG   = "0D1117";   // 代码背景

// ─── 工具函数 ─────────────────────────────────────────
function rr(slide, x, y, w, h, color, radius) {
  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x, y, w, h, rectRadius: radius || 0.15,
    fill: { color }, line: { color }
  });
}
function rrBorder(slide, x, y, w, h, fillColor, borderColor, bw, radius) {
  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, {
    x, y, w, h, rectRadius: radius || 0.15,
    fill: { color: fillColor },
    line: { color: borderColor, width: bw || 2 }
  });
}
function txt(slide, text, x, y, w, h, opts) {
  slide.addText(text, { x, y, w, h, ...opts });
}
function oval(slide, x, y, w, h, color) {
  slide.addShape(pres.shapes.OVAL, { x, y, w, h, fill: { color }, line: { color } });
}
function codeBlock(slide, x, y, w, h, tokens, fs) {
  rrBorder(slide, x, y, w, h, CODBG, PURPLE, 1.5, 0.18);
  // 红黄绿三点
  [RED, YELLOW, GREEN].forEach((c, i) =>
    oval(slide, x + 0.2 + i * 0.28, y + 0.15, 0.16, 0.16, c)
  );
  slide.addText(tokens, {
    x: x + 0.15, y: y + 0.44, w: w - 0.3, h: h - 0.58,
    fontSize: fs || 12, fontFace: "Consolas"
  });
}

// ══════════════════════════════════════════════════════
// Slide 1  封面 —— 冒险开始！
// ══════════════════════════════════════════════════════
{
  const s = pres.addSlide();
  s.background = { color: DEEP };

  // 星星
  [[0.4,0.2],[1.5,0.6],[3,0.3],[6,0.4],[8,0.2],[9.2,0.7],[9.6,0.2],
   [0.2,3],[0.9,4.5],[9.5,3.5],[9,4.8],[5,0.1],[7,5.2]].forEach(([x,y]) => {
    oval(s, x, y, 0.07, 0.07, WHITE);
  });

  // 彩虹拱形装饰
  [PURPLE, BLUE, TEAL, GREEN, ORANGE, PINK].forEach((c, i) => {
    oval(s, 6.8 - i*0.35, -0.5 - i*0.3, 5+i*0.7, 5+i*0.7, c.length === 6 ? c : c);
    // 用透明度覆盖制造圆弧感
  });
  // 覆盖右侧
  s.addShape(pres.shapes.RECTANGLE, {
    x: 9.5, y: 0, w: 0.5, h: 5.63, fill: { color: DEEP }, line: { color: DEEP }
  });

  // 左侧主内容
  rr(s, 0.3, 0.28, 2.2, 0.42, PURPLE, 0.21);
  txt(s, "C++ 编程冒险", 0.3, 0.28, 2.2, 0.42, {
    fontSize: 12, bold: true, color: WHITE, align: "center", valign: "middle", margin: 0
  });

  txt(s, "函数的", 0.3, 0.9, 7, 0.75, {
    fontSize: 38, bold: true, color: "94A3B8"
  });
  txt(s, "魔法世界", 0.3, 1.6, 8, 1.3, {
    fontSize: 72, bold: true, color: WHITE, charSpacing: 4
  });

  txt(s, [
    { text: "素数猎人", options: { color: YELLOW, bold: true } },
    { text: " · 跟着程序一起抓素数！", options: { color: "94A3B8" } }
  ], 0.3, 2.95, 8, 0.55, { fontSize: 18 });

  // 底部
  s.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 5.28, w: 10, h: 0.35,
    fill: { color: PURPLE }, line: { color: PURPLE }
  });
  txt(s, "信息学启蒙  ·  C++ 基础  ·  函数专题  ·  小学高年级", 0, 5.28, 10, 0.35, {
    fontSize: 11, color: "C4B5FD", align: "center", valign: "middle"
  });

  // 右下角彩蛋
  rr(s, 7.8, 3.6, 1.85, 1.55, "1E1B4B", 0.2);
  txt(s, "🎮", 7.8, 3.68, 1.85, 0.6, { fontSize: 30, align: "center", valign: "middle" });
  txt(s, "准备好\n开始冒险了吗？", 7.8, 4.28, 1.85, 0.72, {
    fontSize: 10, color: "A78BFA", align: "center"
  });
}

// ══════════════════════════════════════════════════════
// Slide 2  第0关：热身 —— 我们来猜一猜
// ══════════════════════════════════════════════════════
{
  const s = pres.addSlide();
  s.background = { color: BG };

  // 关卡标牌
  rr(s, 0, 0, 10, 0.78, PURPLE, 0);
  txt(s, "🌟 热身关 · 你认识这些数吗？", 0.4, 0, 9.2, 0.78, {
    fontSize: 22, bold: true, color: WHITE, valign: "middle"
  });

  // 问题
  rrBorder(s, 0.35, 0.9, 9.3, 1.05, "F5F3FF", PURPLE, 1.5, 0.2);
  txt(s, [
    { text: "哪些数只能被 ", options: { color: DARK, fontSize: 17 } },
    { text: "1", options: { color: PURPLE, bold: true, fontSize: 22 } },
    { text: " 和 ", options: { color: DARK, fontSize: 17 } },
    { text: "它自己", options: { color: PURPLE, bold: true, fontSize: 22 } },
    { text: " 整除？", options: { color: DARK, fontSize: 17 } }
  ], 0.6, 0.95, 8.8, 0.88, { valign: "middle" });

  // 数字格子
  const nums = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15];
  const isPrime = n => {
    if(n<=1) return false;
    for(let i=2;i*i<=n;i++) if(n%i===0) return false;
    return true;
  };
  nums.forEach((n, i) => {
    const col = i % 5;
    const row = Math.floor(i / 5);
    const x = 0.45 + col * 1.83;
    const y = 2.1 + row * 1.15;
    const prime = isPrime(n);
    rrBorder(s, x, y, 1.6, 0.95,
      prime ? "F0FDF4" : (n===1 ? "FFF7ED" : "F8FAFF"),
      prime ? GREEN : (n===1 ? ORANGE : "CBD5E1"), prime ? 2 : 1, 0.15);
    txt(s, String(n), x, y, 1.6, 0.55, {
      fontSize: 26, bold: prime, color: prime ? GREEN : (n===1 ? ORANGE : GRAY),
      align: "center", valign: "middle", margin: 0
    });
    if(prime) {
      rr(s, x+0.3, y+0.58, 1.0, 0.28, GREEN, 0.14);
      txt(s, "✓ 素数", x+0.3, y+0.58, 1.0, 0.28, {
        fontSize: 9.5, bold: true, color: WHITE, align: "center", valign: "middle", margin: 0
      });
    } else if(n===1) {
      rr(s, x+0.15, y+0.58, 1.3, 0.28, ORANGE, 0.14);
      txt(s, "特殊：1不是", x+0.15, y+0.58, 1.3, 0.28, {
        fontSize: 9, bold: true, color: WHITE, align: "center", valign: "middle", margin: 0
      });
    } else {
      rr(s, x+0.3, y+0.58, 1.0, 0.28, "94A3B8", 0.14);
      txt(s, "✗ 非素数", x+0.3, y+0.58, 1.0, 0.28, {
        fontSize: 9.5, bold: true, color: WHITE, align: "center", valign: "middle", margin: 0
      });
    }
  });

  // 底部提示
  rrBorder(s, 0.35, 5.12, 9.3, 0.38, "FFFBEB", YELLOW, 1, 0.1);
  txt(s, "💡 记住：像 2、3、5、7 这样的数，就叫做「素数」，也叫「质数」！", 0.55, 5.12, 9.0, 0.38, {
    fontSize: 12, color: YELLOW, valign: "middle", bold: true
  });
}

// ══════════════════════════════════════════════════════
// Slide 3  第1关：认识「函数」—— 函数是什么
// ══════════════════════════════════════════════════════
{
  const s = pres.addSlide();
  s.background = { color: BG };

  rr(s, 0, 0, 10, 0.78, BLUE, 0);
  txt(s, "🔑 第1关 · 认识「函数」", 0.4, 0, 9.2, 0.78, {
    fontSize: 22, bold: true, color: WHITE, valign: "middle"
  });

  // 比喻：函数像榨汁机
  rrBorder(s, 0.35, 0.92, 9.3, 1.55, "EFF6FF", BLUE, 1.5, 0.2);
  txt(s, "🍊  函数，就像一台「榨汁机」！", 0.6, 1.0, 8.8, 0.52, {
    fontSize: 18, bold: true, color: BLUE
  });
  txt(s, [
    { text: "你把水果（", options: { color: DARK } },
    { text: "参数", options: { color: ORANGE, bold: true } },
    { text: "）放进去 → 机器处理 → 出来一杯果汁（", options: { color: DARK } },
    { text: "返回值", options: { color: GREEN, bold: true } },
    { text: "）", options: { color: DARK } },
  ], 0.6, 1.56, 8.8, 0.72, { fontSize: 14 });

  // 榨汁机图示（用形状模拟）
  // 输入箭头
  rr(s, 0.4, 2.7, 1.8, 0.72, "FEF3C7", 0.15);
  txt(s, "🍊 苹果\n（参数 n）", 0.4, 2.7, 1.8, 0.72, {
    fontSize: 11, color: ORANGE, align: "center", valign: "middle", bold: true
  });
  s.addShape(pres.shapes.RECTANGLE, { x: 2.22, y: 2.98, w: 0.5, h: 0.12, fill: {color: ORANGE}, line:{color:ORANGE} });
  txt(s, "→", 2.22, 2.82, 0.5, 0.44, { fontSize: 20, color: ORANGE, align: "center", bold: true });

  // 机器
  rr(s, 2.78, 2.52, 2.8, 1.1, BLUE, 0.2);
  txt(s, "⚙️ 函数\nisPrime(n)\n处理中...", 2.78, 2.52, 2.8, 1.1, {
    fontSize: 11.5, bold: true, color: WHITE, align: "center", valign: "middle"
  });

  // 输出箭头
  txt(s, "→", 5.6, 2.82, 0.5, 0.44, { fontSize: 20, color: GREEN, align: "center", bold: true });
  rr(s, 6.15, 2.7, 1.9, 0.72, "F0FDF4", 0.15);
  txt(s, "true/false\n（是/不是素数）", 6.15, 2.7, 1.9, 0.72, {
    fontSize: 11, color: GREEN, align: "center", valign: "middle", bold: true
  });

  // 函数语法
  rrBorder(s, 0.35, 3.82, 9.3, 1.68, "F8FAFF", PURPLE, 1.5, 0.18);
  txt(s, "C++ 函数的写法：", 0.6, 3.9, 5, 0.36, { fontSize: 13, bold: true, color: PURPLE });
  s.addText([
    { text: "bool", options: { color: YELLOW, bold: true } },
    { text: "  ", options: { color: WHITE } },
    { text: "isPrime", options: { color: TEAL, bold: true } },
    { text: " (", options: { color: WHITE } },
    { text: "int", options: { color: YELLOW } },
    { text: " n) {", options: { color: WHITE } },
    { text: "  ← 接受一个整数 n", options: { color: "6EE7B7", italic: true } },
    { text: "\n    ...处理逻辑...\n", options: { color: "94A3B8" } },
    { text: "    return", options: { color: PINK, bold: true } },
    { text: " true/false;", options: { color: WHITE } },
    { text: "  ← 告诉你结果\n}", options: { color: "6EE7B7", italic: true } },
  ], {
    x: 0.6, y: 4.3, w: 8.8, h: 1.1,
    fontSize: 13, fontFace: "Consolas",
    fill: { color: CODBG }, valign: "middle"
  });
}

// ══════════════════════════════════════════════════════
// Slide 4  第2关：写出判断素数的函数
// ══════════════════════════════════════════════════════
{
  const s = pres.addSlide();
  s.background = { color: BG };

  rr(s, 0, 0, 10, 0.78, TEAL, 0);
  txt(s, "🕵️ 第2关 · 侦探函数：isPrime() 是怎么工作的？", 0.4, 0, 9.2, 0.78, {
    fontSize: 20, bold: true, color: WHITE, valign: "middle"
  });

  // 左：步骤漫画
  rrBorder(s, 0.3, 0.9, 4.55, 4.62, "F0FDFA", TEAL, 1.5, 0.2);
  txt(s, "侦探的破案步骤：", 0.55, 0.98, 4.0, 0.4, { fontSize: 13, bold: true, color: TEAL });

  const steps = [
    { num:"①", emoji:"🚦", text:"n≤1？直接说「不是」，回家！", color: RED },
    { num:"②", emoji:"🔢", text:"从 2 开始，逐个试除", color: BLUE },
    { num:"③", emoji:"⚡", text:"只试到 √n（i×i≤n），聪明省力！", color: YELLOW },
    { num:"④", emoji:"❌", text:"被整除了？立刻说「不是」！", color: ORANGE },
    { num:"⑤", emoji:"🏆", text:"全试完没问题？「是素数！」", color: GREEN },
  ];
  steps.forEach((st, i) => {
    const y = 1.46 + i * 0.75;
    rrBorder(s, 0.48, y, 4.2, 0.62, WHITE, st.color, 1, 0.1);
    rr(s, 0.48, y, 0.7, 0.62, st.color, 0.1);
    txt(s, st.emoji, 0.48, y, 0.7, 0.62, { fontSize: 16, align: "center", valign: "middle", margin: 0 });
    txt(s, st.num + " " + st.text, 1.26, y + 0.1, 3.3, 0.42, { fontSize: 11.5, color: DARK });
  });

  // 右：代码
  codeBlock(s, 5.1, 0.9, 4.6, 4.62, [
    { text: "bool", options: { color: YELLOW, bold: true } },
    { text: " isPrime(", options: { color: WHITE } },
    { text: "int", options: { color: YELLOW } },
    { text: " n) {\n\n", options: { color: WHITE } },
    { text: "  // ① 不是素数：n≤1\n", options: { color: "6EE7B7", italic: true } },
    { text: "  if", options: { color: PINK, bold: true } },
    { text: " (n <= 1)\n", options: { color: WHITE } },
    { text: "    return", options: { color: PINK, bold: true } },
    { text: " false;\n\n", options: { color: WHITE } },
    { text: "  // ②③ 从2试到√n\n", options: { color: "6EE7B7", italic: true } },
    { text: "  for", options: { color: PINK, bold: true } },
    { text: " (", options: { color: WHITE } },
    { text: "int", options: { color: YELLOW } },
    { text: " i=2; i*i<=n; i++) {\n", options: { color: WHITE } },
    { text: "    // ④ 能整除？不是素数\n", options: { color: "6EE7B7", italic: true } },
    { text: "    if", options: { color: PINK, bold: true } },
    { text: " (n % i == 0)\n", options: { color: WHITE } },
    { text: "      return", options: { color: PINK, bold: true } },
    { text: " false;\n  }\n\n", options: { color: WHITE } },
    { text: "  // ⑤ 全部通过！\n", options: { color: "6EE7B7", italic: true } },
    { text: "  return", options: { color: PINK, bold: true } },
    { text: " true;\n}", options: { color: WHITE } },
  ], 11.5);
}

// ══════════════════════════════════════════════════════
// Slide 5  第3关：主函数 —— 派出侦探去查案
// ══════════════════════════════════════════════════════
{
  const s = pres.addSlide();
  s.background = { color: BG };

  rr(s, 0, 0, 10, 0.78, GREEN, 0);
  txt(s, "🚀 第3关 · 主函数：派侦探逐个排查 2~N", 0.4, 0, 9.2, 0.78, {
    fontSize: 20, bold: true, color: WHITE, valign: "middle"
  });

  // 流程图（横向）
  const flow = [
    { icon:"📥", text:"读入\nN", color: TEAL },
    { icon:"🔢", text:"count=0\ni 从 2 开始", color: BLUE },
    { icon:"🕵️", text:"调用\nisPrime(i)", color: PURPLE },
    { icon:"❓", text:"返回\ntrue?", color: ORANGE },
    { icon:"➕", text:"count\n+1", color: GREEN },
    { icon:"📤", text:"输出\ncount", color: PINK },
  ];

  flow.forEach((f, i) => {
    const x = 0.25 + i * 1.62;
    rr(s, x, 0.92, 1.42, 1.32, f.color, 0.18);
    txt(s, f.icon, x, 0.96, 1.42, 0.6, { fontSize: 22, align: "center", valign: "middle", margin: 0 });
    txt(s, f.text, x, 1.55, 1.42, 0.62, { fontSize: 10.5, bold: true, color: WHITE, align: "center", valign: "middle", margin: 0 });
    if(i < flow.length - 1) {
      txt(s, "→", 1.67 + i * 1.62, 1.38, 0.22, 0.44, { fontSize: 18, color: "94A3B8", bold: true, align: "center" });
    }
  });

  // 完整代码
  codeBlock(s, 0.3, 2.4, 5.5, 3.12, [
    { text: "#include", options: { color: YELLOW } },
    { text: " <iostream>\n", options: { color: TEAL } },
    { text: "using namespace", options: { color: PINK, bold: true } },
    { text: " std;\n\n", options: { color: WHITE } },
    { text: "bool", options: { color: YELLOW, bold: true } },
    { text: " isPrime(", options: { color: WHITE } },
    { text: "int", options: { color: YELLOW } },
    { text: " n) { ...函数在这里... }\n\n", options: { color: "6EE7B7" } },
    { text: "int", options: { color: YELLOW, bold: true } },
    { text: " main() {\n", options: { color: WHITE } },
    { text: "  int", options: { color: YELLOW } },
    { text: " N, count = 0;\n", options: { color: WHITE } },
    { text: "  cin", options: { color: GREEN } },
    { text: " >> N;\n", options: { color: WHITE } },
    { text: "  for", options: { color: PINK, bold: true } },
    { text: " (", options: { color: WHITE } },
    { text: "int", options: { color: YELLOW } },
    { text: " i=2; i<=N; i++)\n", options: { color: WHITE } },
    { text: "    if", options: { color: PINK, bold: true } },
    { text: " (isPrime(i))\n", options: { color: WHITE } },
    { text: "      count++;\n", options: { color: WHITE } },
    { text: "  cout", options: { color: GREEN } },
    { text: " << count;\n", options: { color: WHITE } },
    { text: "  return", options: { color: PINK, bold: true } },
    { text: " 0;\n}", options: { color: WHITE } },
  ], 11.5);

  // 右侧说明卡片
  rrBorder(s, 6.05, 2.4, 3.65, 3.12, WHITE, GREEN, 1.5, 0.18);
  txt(s, "✏️ 读懂代码", 6.25, 2.5, 3.2, 0.4, { fontSize: 13, bold: true, color: GREEN });
  const notes = [
    { color: TEAL,   text: "count=0：计数器清零" },
    { color: BLUE,   text: "i 从 2 开始，不从 1 开始" },
    { color: PURPLE, text: "isPrime(i)：调用侦探函数" },
    { color: ORANGE, text: "返回 true → count++" },
    { color: PINK,   text: "最后输出 count 就是答案" },
  ];
  notes.forEach((n, i) => {
    rrBorder(s, 6.22, 2.98 + i * 0.46, 3.3, 0.38, n.color + "15", n.color, 0.8, 0.08);
    txt(s, "• " + n.text, 6.32, 3.0 + i * 0.46, 3.1, 0.34, { fontSize: 11, color: DARK });
  });
}

// ══════════════════════════════════════════════════════
// Slide 6  第4关：追踪侦探（N=10 动画模拟）
// ══════════════════════════════════════════════════════
{
  const s = pres.addSlide();
  s.background = { color: DEEP };

  rr(s, 0, 0, 10, 0.78, ORANGE, 0);
  txt(s, "🎯 第4关 · 追踪侦探工作过程（N = 10）", 0.4, 0, 9.2, 0.78, {
    fontSize: 20, bold: true, color: WHITE, valign: "middle"
  });

  // 数字行
  const ns = [2,3,4,5,6,7,8,9,10];
  const primes10 = new Set([2,3,5,7]);
  ns.forEach((n, i) => {
    const x = 0.3 + i * 1.04;
    const isPrime = primes10.has(n);
    rrBorder(s, x, 0.88, 0.88, 0.88, isPrime ? "064E3B" : "1E293B",
      isPrime ? GREEN : "475569", isPrime ? 2 : 0.8, 0.12);
    txt(s, String(n), x, 0.88, 0.88, 0.88, {
      fontSize: 22, bold: isPrime, color: isPrime ? GREEN : "64748B",
      align: "center", valign: "middle", margin: 0
    });
  });

  // 每个数的侦探报告卡
  const reports = [
    { n:2,  ok:true,  short:"i*i>n\n直接通过", reason:"2是最小素数" },
    { n:3,  ok:true,  short:"i=2,4>3\n直接通过", reason:"无因数" },
    { n:4,  ok:false, short:"4÷2=2\n整除!", reason:"2×2=4" },
    { n:5,  ok:true,  short:"i=2,4≤5\n2不整除\ni=3,9>5过", reason:"无因数" },
    { n:6,  ok:false, short:"6÷2=3\n整除!", reason:"2×3=6" },
    { n:7,  ok:true,  short:"i=2,3\n均不整除", reason:"无因数" },
    { n:8,  ok:false, short:"8÷2=4\n整除!", reason:"2×4=8" },
    { n:9,  ok:false, short:"9÷3=3\n整除!", reason:"3×3=9" },
    { n:10, ok:false, short:"10÷2=5\n整除!", reason:"2×5=10" },
  ];

  reports.forEach((r, i) => {
    const x = 0.3 + i * 1.04;
    rrBorder(s, x, 1.88, 0.88, 3.5, r.ok ? "0A2520" : "200A0A",
      r.ok ? GREEN : RED, 1, 0.1);
    rr(s, x + 0.08, 1.96, 0.72, 0.3, r.ok ? GREEN : RED, 0.1);
    txt(s, r.ok ? "✓素数" : "✗非素", x + 0.08, 1.96, 0.72, 0.3, {
      fontSize: 8.5, bold: true, color: WHITE, align: "center", valign: "middle", margin: 0
    });
    txt(s, r.short, x + 0.04, 2.3, 0.8, 1.4, {
      fontSize: 8, color: r.ok ? "6EE7B7" : "FCA5A5", fontFace: "Consolas"
    });
    rrBorder(s, x + 0.06, 3.72, 0.76, 0.5, r.ok ? "0A2520" : "200A0A",
      r.ok ? GREEN : RED, 0.6, 0.06);
    txt(s, r.reason, x + 0.06, 3.75, 0.76, 0.44, {
      fontSize: 8, color: r.ok ? "A7F3D0" : "FCA5A5", align: "center"
    });
  });

  // count 变化
  txt(s, "count 变化：", 0.3, 5.4, 2, 0.2, { fontSize: 11, color: "94A3B8" });
  let c = 0;
  ns.forEach((n, i) => {
    if(primes10.has(n)) c++;
    const x = 0.3 + i * 1.04;
    rr(s, x, 5.35, 0.88, 0.25, primes10.has(n) ? PURPLE : "1E293B", 0.06);
    txt(s, String(c), x, 5.35, 0.88, 0.25, {
      fontSize: 11, bold: primes10.has(n), color: primes10.has(n) ? YELLOW : "64748B",
      align: "center", valign: "middle", margin: 0
    });
  });

  // 最终答案
  rrBorder(s, 0.3, 5.24, 9.4, 0.3, "1E1B4B", PURPLE, 0.8, 0.1);
  txt(s, "🏁 最终结果：2~10 中共有 4 个素数（2, 3, 5, 7）→ count = 4", 0.5, 5.24, 9.0, 0.3, {
    fontSize: 11, color: YELLOW, bold: true, valign: "middle"
  });
}

// ══════════════════════════════════════════════════════
// Slide 7  第5关：超级比较 —— 慢方法 vs 快方法
// ══════════════════════════════════════════════════════
{
  const s = pres.addSlide();
  s.background = { color: BG };

  rr(s, 0, 0, 10, 0.78, PINK, 0);
  txt(s, "⚡ 第5关 · 超级对比：慢方法 vs 聪明方法", 0.4, 0, 9.2, 0.78, {
    fontSize: 20, bold: true, color: WHITE, valign: "middle"
  });

  // 左：慢方法
  rrBorder(s, 0.3, 0.92, 4.4, 4.55, "FFF5F5", RED, 2, 0.2);
  rr(s, 0.3, 0.92, 4.4, 0.52, RED, 0.2);
  txt(s, "🐌 慢方法（不推荐）", 0.4, 0.92, 4.2, 0.52, {
    fontSize: 14, bold: true, color: WHITE, valign: "middle"
  });
  s.addText([
    { text: "for", options: { color: PINK, bold: true } },
    { text: " (i=2; i<n; i++)\n", options: { color: DARK } },
    { text: "  if", options: { color: PINK, bold: true } },
    { text: "(n%i==0)", options: { color: DARK } },
    { text: " return", options: { color: PINK, bold: true } },
    { text: " false;\n", options: { color: DARK } },
    { text: "return", options: { color: PINK, bold: true } },
    { text: " true;", options: { color: DARK } },
  ], {
    x: 0.5, y: 1.55, w: 4.0, h: 0.85,
    fontSize: 12, fontFace: "Consolas",
    fill: { color: "FEE2E2" }
  });
  txt(s, "判断 100 是不是素数：", 0.5, 2.52, 4.0, 0.38, { fontSize: 12, color: DARK, bold: true });
  const slowSteps = ["试除 2,3,4,5,...,99","要试 98 次！","才发现 100=2×50"];
  slowSteps.forEach((st, i) => {
    rrBorder(s, 0.5, 2.95+i*0.48, 3.9, 0.4, "FFF5F5", RED, 0.8, 0.08);
    txt(s, "😓 " + st, 0.65, 2.97+i*0.48, 3.6, 0.34, { fontSize: 11.5, color: RED });
  });
  txt(s, "🐢 要试 n-2 次，太慢！", 0.5, 4.44, 4.0, 0.45, {
    fontSize: 12, bold: true, color: RED,
    fill: { color: "FEE2E2" }
  });

  // 中间箭头
  txt(s, "VS", 4.75, 2.55, 0.5, 0.55, { fontSize: 20, bold: true, color: GRAY, align: "center" });
  txt(s, "→\n优化！", 4.65, 3.18, 0.7, 0.72, { fontSize: 11, color: PURPLE, align: "center", bold: true });

  // 右：快方法
  rrBorder(s, 5.3, 0.92, 4.4, 4.55, "F0FDF4", GREEN, 2, 0.2);
  rr(s, 5.3, 0.92, 4.4, 0.52, GREEN, 0.2);
  txt(s, "🚀 聪明方法（推荐）", 5.4, 0.92, 4.2, 0.52, {
    fontSize: 14, bold: true, color: WHITE, valign: "middle"
  });
  s.addText([
    { text: "for", options: { color: PINK, bold: true } },
    { text: " (i=2; ", options: { color: DARK } },
    { text: "i*i<=n", options: { color: GREEN, bold: true } },
    { text: "; i++)\n", options: { color: DARK } },
    { text: "  if", options: { color: PINK, bold: true } },
    { text: "(n%i==0)", options: { color: DARK } },
    { text: " return", options: { color: PINK, bold: true } },
    { text: " false;\n", options: { color: DARK } },
    { text: "return", options: { color: PINK, bold: true } },
    { text: " true;", options: { color: DARK } },
  ], {
    x: 5.48, y: 1.55, w: 4.0, h: 0.85,
    fontSize: 12, fontFace: "Consolas",
    fill: { color: "DCFCE7" }
  });
  txt(s, "判断 100 是不是素数：", 5.48, 2.52, 4.0, 0.38, { fontSize: 12, color: DARK, bold: true });
  const fastSteps = ["√100 = 10","只试 2,3,4,...,10","试 9 次就知道了！"];
  fastSteps.forEach((st, i) => {
    rrBorder(s, 5.48, 2.95+i*0.48, 3.9, 0.4, "F0FDF4", GREEN, 0.8, 0.08);
    txt(s, "😎 " + st, 5.62, 2.97+i*0.48, 3.6, 0.34, { fontSize: 11.5, color: GREEN });
  });
  txt(s, "🚀 只试 √n 次，快 10 倍！", 5.48, 4.44, 4.0, 0.45, {
    fontSize: 12, bold: true, color: GREEN,
    fill: { color: "DCFCE7" }
  });
}

// ══════════════════════════════════════════════════════
// Slide 8  知识星图：今天学了什么
// ══════════════════════════════════════════════════════
{
  const s = pres.addSlide();
  s.background = { color: DEEP };

  rr(s, 0, 0, 10, 0.08, YELLOW, 0);
  txt(s, "🌟 今天的收获星图", 0, 0.12, 10, 0.72, {
    fontSize: 26, bold: true, color: WHITE, align: "center"
  });

  const stars = [
    { icon:"🏷️", title:"函数定义",   desc:"bool isPrime(int n)",       color: PURPLE, x:0.3,  y:1.0 },
    { icon:"📦", title:"参数传递",   desc:"形参 n 接收 i 的值",          color: BLUE,   x:3.55, y:1.0 },
    { icon:"↩️", title:"return",    desc:"提前返回或最后返回",           color: PINK,   x:6.8,  y:1.0 },
    { icon:"📞", title:"函数调用",   desc:"isPrime(i)",                 color: TEAL,   x:0.3,  y:3.15 },
    { icon:"⚡", title:"√n 优化",   desc:"i*i≤n  只试这么多",           color: YELLOW, x:3.55, y:3.15 },
    { icon:"🧩", title:"模块化思想", desc:"判断和计数分开写",             color: GREEN,  x:6.8,  y:3.15 },
  ];

  stars.forEach(sk => {
    rrBorder(s, sk.x, sk.y, 2.95, 1.92, "0F172A", sk.color, 2, 0.2);
    rr(s, sk.x, sk.y, 2.95, 0.55, sk.color, 0.2);
    txt(s, sk.icon + "  " + sk.title, sk.x, sk.y, 2.95, 0.55, {
      fontSize: 14, bold: true, color: WHITE, align: "center", valign: "middle", margin: 0
    });
    txt(s, sk.desc, sk.x + 0.12, sk.y + 0.65, 2.71, 0.95, {
      fontSize: 12.5, color: sk.color, fontFace: "Consolas", align: "center", valign: "middle"
    });
    rr(s, sk.x + 0.72, sk.y + 1.55, 1.5, 0.28, sk.color, 0.1);
    txt(s, "✓ 已掌握", sk.x + 0.72, sk.y + 1.55, 1.5, 0.28, {
      fontSize: 10, bold: true, color: WHITE, align: "center", valign: "middle", margin: 0
    });
  });
}

// ══════════════════════════════════════════════════════
// Slide 9  闯关挑战题（互动）
// ══════════════════════════════════════════════════════
{
  const s = pres.addSlide();
  s.background = { color: BG };

  rr(s, 0, 0, 10, 0.78, PURPLE, 0);
  txt(s, "🎮 课堂挑战：看代码找问题！", 0.4, 0, 9.2, 0.78, {
    fontSize: 22, bold: true, color: WHITE, valign: "middle"
  });

  const bugs = [
    {
      q: "Bug 1  —  下面代码会把 1 也算成素数！为什么？",
      code: "bool isPrime(int n) {\n  for(int i=2; i*i<=n; i++)\n    if(n%i==0) return false;\n  return true; // n=1时循环不执行\n}",
      fix: "在开头加上：if(n<=1) return false;",
      color: RED,
    },
    {
      q: "Bug 2  —  这个主函数会少算素数，找出原因！",
      code: "for(int i=1; i<=N; i++)\n  if(isPrime(i)) count++;",
      fix: "从 i=2 开始，因为1不是素数",
      color: ORANGE,
    },
    {
      q: "Bug 3  —  循环条件写的是 i<n，有什么问题？",
      code: "for(int i=2; i<n; i++)\n  if(n%i==0) return false;\nreturn true;",
      fix: "改为 i*i<=n 更高效（只需试到√n）",
      color: BLUE,
    },
  ];

  bugs.forEach((b, i) => {
    const y = 0.9 + i * 1.5;
    rrBorder(s, 0.3, y, 9.4, 1.38, WHITE, b.color, 1.5, 0.15);
    rr(s, 0.3, y, 9.4, 0.35, b.color, 0.15);
    txt(s, b.q, 0.5, y + 0.02, 9.0, 0.3, { fontSize: 12, bold: true, color: WHITE, valign: "middle" });
    s.addText(b.code, {
      x: 0.5, y: y + 0.38, w: 5.2, h: 0.85,
      fontSize: 10.5, fontFace: "Consolas", color: DARK, fill: { color: "F8FAFF" }
    });
    rrBorder(s, 5.85, y + 0.38, 3.7, 0.85, "F0FDF4", GREEN, 1, 0.1);
    txt(s, "✅ 修正：", 6.0, y + 0.42, 3.4, 0.3, { fontSize: 11, color: GREEN, bold: true });
    txt(s, b.fix, 6.0, y + 0.72, 3.4, 0.45, { fontSize: 10.5, color: DARK, fontFace: "Consolas" });
  });
}

// ══════════════════════════════════════════════════════
// Slide 10  结语：冒险结束！下次挑战
// ══════════════════════════════════════════════════════
{
  const s = pres.addSlide();
  s.background = { color: DEEP };

  // 顶部彩虹条
  [PURPLE, BLUE, TEAL, GREEN, ORANGE, PINK, YELLOW].forEach((c, i) => {
    s.addShape(pres.shapes.RECTANGLE, {
      x: i*(10/7), y:0, w:10/7-0.02, h:0.14,
      fill:{color:c}, line:{color:c}
    });
  });

  // 主标题
  txt(s, "🎉 冒险成功！", 0, 0.25, 10, 0.72, {
    fontSize: 28, bold: true, color: YELLOW, align: "center"
  });
  txt(s, "你已掌握了「素数猎人」的全部技能！", 0, 0.95, 10, 0.55, {
    fontSize: 18, color: "CBD5E1", align: "center"
  });

  // 技能总结徽章
  const badges = [
    { text:"函数定义", color: PURPLE },
    { text:"参数传递", color: BLUE },
    { text:"return语句", color: PINK },
    { text:"函数调用", color: TEAL },
    { text:"√n优化", color: YELLOW },
    { text:"模块化", color: GREEN },
  ];
  badges.forEach((b, i) => {
    const x = 0.5 + (i%3) * 3.02;
    const y = 1.65 + Math.floor(i/3) * 0.72;
    rr(s, x, y, 2.7, 0.55, b.color, 0.28);
    oval(s, x + 0.12, y + 0.12, 0.32, 0.32, WHITE);
    txt(s, "★", x + 0.12, y + 0.12, 0.32, 0.32, {
      fontSize: 12, color: b.color, align: "center", valign: "middle", margin: 0
    });
    txt(s, b.text, x + 0.52, y, 2.06, 0.55, {
      fontSize: 13, bold: true, color: WHITE, valign: "middle"
    });
  });

  // 下一步挑战
  rrBorder(s, 0.4, 3.2, 9.2, 1.62, "0F172A", YELLOW, 1.5, 0.2);
  txt(s, "🚀 下次挑战预告", 0.65, 3.28, 4, 0.4, { fontSize: 14, bold: true, color: YELLOW });
  const nexts = [
    "① 输出所有素数（不只是个数）",
    "② 计算素数之和",
    "③ 判断两个数之间有多少素数",
  ];
  nexts.forEach((n, i) =>
    txt(s, n, 0.65, 3.72 + i*0.34, 8.5, 0.3, { fontSize: 12, color: "CBD5E1" })
  );

  // 底部
  rr(s, 0, 5.28, 10, 0.35, "0A0A1A", 0);
  txt(s, "编程就是把想法变成现实的魔法  🌟  继续加油！", 0, 5.28, 10, 0.35, {
    fontSize: 12, color: "7C3AED", align: "center", valign: "middle"
  });
}

// ─── 保存 ─────────────────────────────────────────────
pres.writeFile({ fileName: "C:/Users/ning/WorkBuddy/Claw/信息学C++函数_素数计数_v2.pptx" })
  .then(() => console.log("PPT 小学趣味版生成成功！"))
  .catch(e => console.error(e));
