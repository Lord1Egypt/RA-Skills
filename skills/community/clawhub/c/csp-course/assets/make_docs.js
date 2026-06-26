const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  HeadingLevel, AlignmentType, WidthType, BorderStyle,
  ShadingType, TableLayoutType, VerticalAlign,
  PageOrientation
} = require("docx");
const fs = require("fs");

// ─────────────────────────────────────────────
// 工具函数
// ─────────────────────────────────────────────
const H1 = (text, color) => new Paragraph({
  heading: HeadingLevel.HEADING_1,
  spacing: { before: 320, after: 160 },
  children: [new TextRun({ text, bold: true, size: 32, color: color || "2563EB" })]
});
const H2 = (text, color) => new Paragraph({
  heading: HeadingLevel.HEADING_2,
  spacing: { before: 240, after: 120 },
  children: [new TextRun({ text, bold: true, size: 28, color: color || "7C3AED" })]
});
const H3 = (text, color) => new Paragraph({
  spacing: { before: 160, after: 80 },
  children: [new TextRun({ text, bold: true, size: 24, color: color || "059669" })]
});
const p = (runs, opts) => new Paragraph({
  spacing: { before: 80, after: 80 },
  ...opts,
  children: Array.isArray(runs) ? runs : [new TextRun({ text: runs, size: 22 })]
});
const li = (text, color) => new Paragraph({
  spacing: { before: 60, after: 60 },
  bullet: { level: 0 },
  children: [new TextRun({ text, size: 22, color: color || "1E293B" })]
});
const li2 = (text) => new Paragraph({
  spacing: { before: 40, after: 40 },
  bullet: { level: 1 },
  children: [new TextRun({ text, size: 20, color: "475569" })]
});
const br = () => new Paragraph({ children: [new TextRun({ text: "" })] });

const colorCell = (text, bgColor, textColor, bold) => new TableCell({
  shading: { fill: bgColor, type: ShadingType.CLEAR },
  verticalAlign: VerticalAlign.CENTER,
  margins: { top: 80, bottom: 80, left: 120, right: 120 },
  children: [new Paragraph({
    alignment: AlignmentType.CENTER,
    children: [new TextRun({ text, bold: bold !== false, color: textColor || "1E293B", size: 20 })]
  })]
});

// ══════════════════════════════════════════════
// 教案文档
// ══════════════════════════════════════════════
async function makeJiaoAn() {
  const doc = new Document({
    styles: {
      default: {
        document: { run: { font: "微软雅黑", size: 22 } }
      }
    },
    sections: [{
      children: [
        // 封面信息
        new Paragraph({
          alignment: AlignmentType.CENTER,
          spacing: { before: 200, after: 200 },
          children: [new TextRun({ text: "信息学 C++ 教学教案", bold: true, size: 44, color: "2563EB" })]
        }),
        new Paragraph({
          alignment: AlignmentType.CENTER,
          spacing: { after: 400 },
          children: [new TextRun({ text: "——函数专题：素数猎人（小学高年级版）", size: 28, color: "7C3AED" })]
        }),

        // 基本信息表
        H1("一、基本信息"),
        new Table({
          width: { size: 100, type: WidthType.PERCENTAGE },
          rows: [
            new TableRow({ children: [
              colorCell("课程名称", "DBEAFE", "1E40AF"),
              colorCell("C++ 函数专题：素数猎人", "EFF6FF", "1E293B", false),
              colorCell("授课年级", "DBEAFE", "1E40AF"),
              colorCell("小学高年级（4-6年级）", "EFF6FF", "1E293B", false),
            ]}),
            new TableRow({ children: [
              colorCell("课时时长", "DBEAFE", "1E40AF"),
              colorCell("40 分钟", "EFF6FF", "1E293B", false),
              colorCell("授课方式", "DBEAFE", "1E40AF"),
              colorCell("讲授 + 互动 + 上机", "EFF6FF", "1E293B", false),
            ]}),
            new TableRow({ children: [
              colorCell("知识前提", "DBEAFE", "1E40AF"),
              colorCell("了解变量、if语句、for循环", "EFF6FF", "1E293B", false),
              colorCell("教材资源", "DBEAFE", "1E40AF"),
              colorCell("配套课件 + 任务单", "EFF6FF", "1E293B", false),
            ]}),
          ]
        }),
        br(),

        // 教学目标
        H1("二、教学目标"),
        H2("知识与技能目标", "2563EB"),
        li("理解函数的概念：会定义、调用、传参、接收返回值"),
        li("掌握 bool 返回类型和 return 语句的使用方法"),
        li("能独立编写 isPrime() 函数判断一个数是否为素数"),
        li("能在主函数中枚举 2~N 并调用函数统计素数个数"),
        H2("过程与方法目标", "059669"),
        li("经历「问题拆解 → 函数设计 → 组合调用」的模块化编程过程"),
        li("理解 i*i<=n（√n 优化）背后的算法思维，体会效率差异"),
        li("通过追踪程序执行过程，建立「程序运行」的心智模型"),
        H2("情感态度与价值观", "7C3AED"),
        li("在游戏化闯关情境中激发编程兴趣"),
        li("体会「让机器帮我们解决枚举问题」的效率感和成就感"),
        br(),

        // 教学重难点
        H1("三、教学重难点"),
        new Table({
          width: { size: 100, type: WidthType.PERCENTAGE },
          rows: [
            new TableRow({ children: [
              colorCell("类别", "FEF3C7", "92400E"),
              colorCell("内容", "FEF3C7", "92400E"),
              colorCell("突破策略", "FEF3C7", "92400E"),
            ]}),
            new TableRow({ children: [
              colorCell("重点", "FFF7ED", "EA580C"),
              colorCell("bool 函数的定义与调用；函数与主程序的协作", "FFFBF0", "1E293B", false),
              colorCell("榨汁机比喻 + 代码同步演示 + 跟做练习", "FFFBF0", "1E293B", false),
            ]}),
            new TableRow({ children: [
              colorCell("难点①", "FFF5F5", "DC2626"),
              colorCell("i*i<=n 的含义和优化原理", "FFF8F8", "1E293B", false),
              colorCell("数字对比（试98次 vs 试9次）直观演示", "FFF8F8", "1E293B", false),
            ]}),
            new TableRow({ children: [
              colorCell("难点②", "F0FDF4", "059669"),
              colorCell("形参与实参的对应关系", "F7FFF9", "1E293B", false),
              colorCell("调用时「传值过程」图示+追踪表", "F7FFF9", "1E293B", false),
            ]}),
          ]
        }),
        br(),

        // 教学过程
        H1("四、教学过程（共 40 分钟）"),

        // 环节1
        H2("环节1：热身导入「猜猜看」（5分钟）"),
        p([
          new TextRun({ text: "教师活动：", bold: true, color: "2563EB", size: 22 }),
          new TextRun({ text: "展示 PPT 第2页，让学生观察 1~15 的数字格子，判断哪些是素数。", size: 22 }),
        ]),
        li("提问：「谁只能被 1 和自己整除？举手回答！」"),
        li("引导学生发现规律：2、3、5、7、11、13……"),
        li("强调：1 不是素数！2 是最小的素数！"),
        p([
          new TextRun({ text: "学生活动：", bold: true, color: "059669", size: 22 }),
          new TextRun({ text: "观察格子，举手抢答，记住素数的定义。", size: 22 }),
        ]),
        p([
          new TextRun({ text: "过渡语：", bold: true, color: "7C3AED", size: 22 }),
          new TextRun({ text: "「如果 N=10000，我们要数出有多少素数，手动数得数到什么时候？这节课我们就用 C++ 写一个「素数猎人」程序来帮我们做这件事！」", size: 22 }),
        ]),
        br(),

        // 环节2
        H2("环节2：认识函数「榨汁机」（8分钟）"),
        p([
          new TextRun({ text: "教师活动：", bold: true, color: "2563EB", size: 22 }),
          new TextRun({ text: "展示 PPT 第3页，用榨汁机类比讲解函数概念。", size: 22 }),
        ]),
        li("比喻：函数就像榨汁机——放进去水果（参数），出来果汁（返回值）"),
        li("展示函数语法结构，逐部分解释："),
        li2("bool = 返回的是「真/假」"),
        li2("isPrime = 函数名字（可以自己取）"),
        li2("int n = 接收一个整数叫做 n"),
        li2("return = 告诉调用者结果"),
        li("提问互动：「这个函数的输入是什么？输出是什么？」"),
        p([
          new TextRun({ text: "学生活动：", bold: true, color: "059669", size: 22 }),
          new TextRun({ text: "观察榨汁机图示，回答提问，在任务单上填写函数各部分名称。", size: 22 }),
        ]),
        br(),

        // 环节3
        H2("环节3：侦探破案「isPrime 函数设计」（10分钟）"),
        p([
          new TextRun({ text: "教师活动：", bold: true, color: "2563EB", size: 22 }),
          new TextRun({ text: "展示 PPT 第4页，用「侦探破案」故事线讲解判断素数的逻辑。", size: 22 }),
        ]),
        li("情境导入：「isPrime 是一个侦探，每次接受一个嫌疑数 n，用5步查出它是不是素数」"),
        li("逐步展示5个侦探步骤，对应代码行："),
        li2("① n≤1？不是，回家 → if(n<=1) return false;"),
        li2("② 从 2 开始问 → for(int i=2; ...)"),
        li2("③ 只问到 √n → i*i<=n"),
        li2("④ 能整除？不是素数 → if(n%i==0) return false;"),
        li2("⑤ 全部通过！是素数 → return true;"),
        li("重点讲解「i*i<=n」：用 n=100 为例，对比试98次 vs 试9次的差距"),
        p([
          new TextRun({ text: "学生活动：", bold: true, color: "059669", size: 22 }),
          new TextRun({ text: "对照步骤图，在任务单上补全 isPrime 函数的空缺代码。", size: 22 }),
        ]),
        br(),

        // 环节4
        H2("环节4：主函数组装「派侦探去查案」（8分钟）"),
        p([
          new TextRun({ text: "教师活动：", bold: true, color: "2563EB", size: 22 }),
          new TextRun({ text: "展示 PPT 第5页，展示完整程序结构和执行流程图。", size: 22 }),
        ]),
        li("引导语：「侦探写好了，怎么派它出去？主函数就是指挥官！」"),
        li("讲解主函数流程：读入 N → 初始化 count → 循环 i=2~N → 调用 isPrime(i) → 若真则 count++ → 输出 count"),
        li("特别强调：i 从 2 开始，因为 1 不是素数"),
        li("演示完整代码，分析每一行的作用"),
        p([
          new TextRun({ text: "学生活动：", bold: true, color: "059669", size: 22 }),
          new TextRun({ text: "对照流程图，在任务单上补全主函数代码框架。", size: 22 }),
        ]),
        br(),

        // 环节5
        H2("环节5：程序追踪「看侦探工作」（5分钟）"),
        p([
          new TextRun({ text: "教师活动：", bold: true, color: "2563EB", size: 22 }),
          new TextRun({ text: "展示 PPT 第6页，带领学生逐步追踪 N=10 时程序的执行过程。", size: 22 }),
        ]),
        li("让学生逐个预测每个数的结果，再看卡片揭晓"),
        li("重点追踪 count 的变化过程：0 → 1 → 2 → 2 → 3 → 3 → 4 → 4 → 4 → 4"),
        li("强调：每次调用 isPrime 就像派侦探出去一趟"),
        p([
          new TextRun({ text: "学生活动：", bold: true, color: "059669", size: 22 }),
          new TextRun({ text: "填写任务单追踪表，记录每个数的 isPrime 结果和 count 变化。", size: 22 }),
        ]),
        br(),

        // 环节6
        H2("环节6：上机实践 + 挑战升级（4分钟）"),
        p([
          new TextRun({ text: "上机任务：", bold: true, color: "EA580C", size: 22 }),
        ]),
        li("基础任务：输入 N，输出 2~N 中素数的个数"),
        li("进阶任务：输出所有素数（不只是个数）"),
        li("挑战任务：计算 2~N 中所有素数的和"),
        br(),

        // 板书设计
        H1("五、板书设计"),
        H3("函数的魔法世界 · 素数猎人"),
        p("左侧板书："),
        li("函数 = 榨汁机（输入→处理→输出）"),
        li("bool isPrime(int n)：侦探函数"),
        li("isPrime 的 5 个侦探步骤"),
        p("右侧板书："),
        li("主函数：指挥官派侦探去查"),
        li("i 从 2 枚举到 N"),
        li("isPrime(i) 为 true → count++"),
        li("关键优化：i*i<=n（只试到√n）"),
        br(),

        // 作业
        H1("六、课后作业"),
        H2("必做题", "2563EB"),
        li("整理笔记：写出函数的四要素（名称、参数、函数体、返回值）"),
        li("完成任务单最后一栏「挑战题」：修改程序输出所有素数"),
        H2("选做题", "7C3AED"),
        li("思考：如何判断一个数既是偶数又是素数？（答案：只有2）"),
        li("编程：计算 2~100 中素数的总和"),
        br(),

        // 评价
        H1("七、教学评价"),
        new Table({
          width: { size: 100, type: WidthType.PERCENTAGE },
          rows: [
            new TableRow({ children: [
              colorCell("评价维度", "E0E7FF", "3730A3"),
              colorCell("评价标准", "E0E7FF", "3730A3"),
              colorCell("评价方式", "E0E7FF", "3730A3"),
            ]}),
            new TableRow({ children: [
              colorCell("函数理解", "F5F3FF", "5B21B6", false),
              colorCell("能说出函数的输入、处理、输出三部分", "FAFAFA", "1E293B", false),
              colorCell("课堂提问+任务单填写", "FAFAFA", "1E293B", false),
            ]}),
            new TableRow({ children: [
              colorCell("代码编写", "F5F3FF", "5B21B6", false),
              colorCell("能独立补全 isPrime 函数和主函数框架", "FAFAFA", "1E293B", false),
              colorCell("任务单检查+上机结果", "FAFAFA", "1E293B", false),
            ]}),
            new TableRow({ children: [
              colorCell("追踪能力", "F5F3FF", "5B21B6", false),
              colorCell("能正确填写 N=10 的追踪表", "FAFAFA", "1E293B", false),
              colorCell("任务单追踪表批改", "FAFAFA", "1E293B", false),
            ]}),
          ]
        }),
      ]
    }]
  });

  const buf = await Packer.toBuffer(doc);
  fs.writeFileSync("C:/Users/ning/WorkBuddy/Claw/信息学C++函数_素数计数_教案_v2.docx", buf);
  console.log("教案生成成功！");
}

// ══════════════════════════════════════════════
// 学生任务单
// ══════════════════════════════════════════════
async function makeRenwuDan() {
  const doc = new Document({
    styles: {
      default: {
        document: { run: { font: "微软雅黑", size: 22 } }
      }
    },
    sections: [{
      children: [
        // 标题
        new Paragraph({
          alignment: AlignmentType.CENTER,
          spacing: { before: 100, after: 100 },
          children: [new TextRun({ text: "🎮  素数猎人任务单", bold: true, size: 48, color: "7C3AED" })]
        }),
        new Paragraph({
          alignment: AlignmentType.CENTER,
          spacing: { after: 80 },
          children: [new TextRun({ text: "C++ 函数专题  ·  小学高年级", size: 22, color: "94A3B8" })]
        }),

        // 姓名栏
        new Table({
          width: { size: 100, type: WidthType.PERCENTAGE },
          rows: [new TableRow({ children: [
            colorCell("姓名：___________", "F5F3FF", "7C3AED"),
            colorCell("班级：___________", "F5F3FF", "7C3AED"),
            colorCell("日期：___________", "F5F3FF", "7C3AED"),
            colorCell("得分：___________", "FEF3C7", "D97706"),
          ]})]
        }),
        br(),

        // 任务0：热身
        H1("☀️ 任务0：热身（连一连）", "059669"),
        p("在下面的数中，圈出所有的素数："),
        new Paragraph({
          spacing: { before: 120, after: 120 },
          alignment: AlignmentType.CENTER,
          children: [new TextRun({
            text: "1    2    3    4    5    6    7    8    9    10    11    12    13",
            size: 28, bold: true, color: "1E293B"
          })]
        }),
        p([
          new TextRun({ text: "答案：共圈出 ", size: 22 }),
          new TextRun({ text: "_____ ", size: 22, color: "7C3AED", bold: true }),
          new TextRun({ text: "个素数，分别是：", size: 22 }),
          new TextRun({ text: "________________________________", size: 22, color: "2563EB" }),
        ]),
        br(),

        // 任务1：函数认知
        H1("🔑 任务1：认识函数（填一填）", "2563EB"),
        p("读下面的代码，回答问题："),
        new Paragraph({
          spacing: { before: 80, after: 80 },
          children: [new TextRun({ text: "bool  isPrime ( int  n )  {  ...  }", size: 24, bold: true, color: "1E1B4B", font: "Consolas" })]
        }),
        new Table({
          width: { size: 100, type: WidthType.PERCENTAGE },
          rows: [
            new TableRow({ children: [
              colorCell("函数名称是？", "DBEAFE", "1E40AF"),
              colorCell("___________________________", "F8FAFF", "1E293B", false),
            ]}),
            new TableRow({ children: [
              colorCell("参数（输入）是什么？", "DBEAFE", "1E40AF"),
              colorCell("___________________________", "F8FAFF", "1E293B", false),
            ]}),
            new TableRow({ children: [
              colorCell("返回类型是什么？", "DBEAFE", "1E40AF"),
              colorCell("___________________________", "F8FAFF", "1E293B", false),
            ]}),
            new TableRow({ children: [
              colorCell("这个函数用来干什么？", "DBEAFE", "1E40AF"),
              colorCell("___________________________", "F8FAFF", "1E293B", false),
            ]}),
          ]
        }),
        br(),

        // 任务2：补全函数
        H1("🕵️ 任务2：补全侦探函数（填代码）", "7C3AED"),
        p("根据侦探的5个步骤，在 ___ 处填入正确的内容："),
        new Paragraph({
          spacing: { before: 80, after: 80 },
          shading: { fill: "0D1117", type: ShadingType.CLEAR },
          children: [
            new TextRun({ text: "bool isPrime(int n) {\n", color: "FFFFFF", size: 22, font: "Consolas" }),
            new TextRun({ text: "  if (n _____ 1) return false;    // ① 排除特殊情况\n", color: "FCD34D", size: 22, font: "Consolas" }),
            new TextRun({ text: "  for (int i=2; i*i _____ n; i++) {  // ② 枚举到√n\n", color: "FCD34D", size: 22, font: "Consolas" }),
            new TextRun({ text: "    if (n _____ i == 0)          // ③ 能整除？\n", color: "FCD34D", size: 22, font: "Consolas" }),
            new TextRun({ text: "      ________________;          // ④ 返回不是素数\n", color: "FCD34D", size: 22, font: "Consolas" }),
            new TextRun({ text: "  }\n", color: "FFFFFF", size: 22, font: "Consolas" }),
            new TextRun({ text: "  ________________;              // ⑤ 通过全部检验！\n", color: "FCD34D", size: 22, font: "Consolas" }),
            new TextRun({ text: "}", color: "FFFFFF", size: 22, font: "Consolas" }),
          ]
        }),
        br(),

        // 任务3：追踪表
        H1("🎯 任务3：程序追踪（N = 10）", "EA580C"),
        p("填写下表，追踪程序的执行过程："),
        new Table({
          width: { size: 100, type: WidthType.PERCENTAGE },
          rows: [
            new TableRow({ children: [
              colorCell("i 的值", "FEF3C7", "92400E"),
              colorCell("isPrime(i) 结果", "FEF3C7", "92400E"),
              colorCell("count 变化", "FEF3C7", "92400E"),
              colorCell("原因（如果不是素数）", "FEF3C7", "92400E"),
            ]}),
            ...[
              ["2", "true ✓", "0→1", "—"],
              ["3", "true ✓", "1→2", "—"],
              ["4", "______", "______", "______"],
              ["5", "______", "______", "______"],
              ["6", "______", "______", "______"],
              ["7", "______", "______", "______"],
              ["8", "______", "______", "______"],
              ["9", "______", "______", "______"],
              ["10","______", "______", "______"],
            ].map((row, i) => new TableRow({
              children: row.map((cell, ci) => colorCell(
                cell,
                i < 2 ? "F0FDF4" : (ci === 0 ? "F8FAFF" : "FFFFFF"),
                i < 2 ? "059669" : "1E293B",
                i < 2 && ci < 2
              ))
            })),
            new TableRow({ children: [
              colorCell("最终结果", "DBEAFE", "1E40AF"),
              new TableCell({
                columnSpan: 3,
                shading: { fill: "EFF6FF", type: ShadingType.CLEAR },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({
                  children: [new TextRun({ text: "2~10 中共有 _____ 个素数，分别是：_________________________", size: 22, color: "1E293B" })]
                })]
              }),
            ]}),
          ]
        }),
        br(),

        // 任务4：主函数
        H1("🚀 任务4：补全主函数（填代码）", "059669"),
        p("在空白处填入正确内容，完成主函数："),
        new Paragraph({
          spacing: { before: 80, after: 80 },
          shading: { fill: "0D1117", type: ShadingType.CLEAR },
          children: [
            new TextRun({ text: "int main() {\n", color: "FFFFFF", size: 22, font: "Consolas" }),
            new TextRun({ text: "  int N, count = _____;\n", color: "FCD34D", size: 22, font: "Consolas" }),
            new TextRun({ text: "  cin >> N;\n", color: "6EE7B7", size: 22, font: "Consolas" }),
            new TextRun({ text: "  for (int i=_____; i<=N; i++) {  // 从 2 开始枚举\n", color: "FCD34D", size: 22, font: "Consolas" }),
            new TextRun({ text: "    if (isPrime(_____))           // 调用函数\n", color: "FCD34D", size: 22, font: "Consolas" }),
            new TextRun({ text: "      _____++;                    // 计数加1\n", color: "FCD34D", size: 22, font: "Consolas" }),
            new TextRun({ text: "  }\n", color: "FFFFFF", size: 22, font: "Consolas" }),
            new TextRun({ text: "  cout << _____;\n", color: "FCD34D", size: 22, font: "Consolas" }),
            new TextRun({ text: "  return 0;\n}", color: "FFFFFF", size: 22, font: "Consolas" }),
          ]
        }),
        br(),

        // 任务5：慢快对比
        H1("⚡ 任务5：思考题（连线题）", "DB2777"),
        p("将左边的描述和右边的代码连线："),
        new Table({
          width: { size: 90, type: WidthType.PERCENTAGE },
          rows: [
            new TableRow({ children: [
              colorCell("描述", "FCE7F3", "9D174D"),
              colorCell("", "FFFFFF", "FFFFFF"),
              colorCell("代码片段", "FCE7F3", "9D174D"),
            ]}),
            ...[
              ["只枚举到 √n（优化版本）", "", "for(i=2; i<n; i++)"],
              ["枚举到 n-1（慢速版本）", "", "for(i=2; i*i<=n; i++)"],
              ["排除 1 和负数", "", "return true;"],
              ["所有试除都通过", "", "if(n<=1) return false;"],
            ].map(row => new TableRow({
              children: row.map((cell, ci) => colorCell(
                cell,
                ci === 0 ? "FFF5F5" : (ci === 2 ? "F0FDF4" : "FFFFFF"),
                ci === 0 ? "DC2626" : (ci === 2 ? "059669" : "1E293B"),
                false
              ))
            }))
          ]
        }),
        br(),

        // 任务6：挑战题
        H1("🏆 任务6：挑战题（选做）", "D97706"),
        p("修改程序，使它能输出 2~N 中所有的素数（不只是个数）。"),
        p("提示：在主函数的 count++ 前面加一句 ___________________"),
        br(),
        p("答案代码：（写在下面的空白处）"),
        new Paragraph({
          spacing: { before: 80, after: 80 },
          shading: { fill: "F8FAFF", type: ShadingType.CLEAR },
          children: [new TextRun({ text: "\n\n\n\n\n\n\n\n", size: 22 })]
        }),
        br(),

        // 自我评价
        H1("⭐ 自我评价", "7C3AED"),
        p("勾选你今天学会的内容："),
        new Table({
          width: { size: 100, type: WidthType.PERCENTAGE },
          rows: [
            new TableRow({ children: [
              colorCell("技能", "E0E7FF", "3730A3"),
              colorCell("完全掌握 ⭐⭐⭐", "E0E7FF", "3730A3"),
              colorCell("基本掌握 ⭐⭐", "E0E7FF", "3730A3"),
              colorCell("还需练习 ⭐", "E0E7FF", "3730A3"),
            ]}),
            ...[
              "能说出函数的作用和结构",
              "能看懂 isPrime 函数的代码",
              "能补全函数代码（填空）",
              "能填写程序追踪表",
              "能说出 i*i<=n 的意思",
            ].map(skill => new TableRow({
              children: [
                colorCell(skill, "F5F3FF", "5B21B6", false),
                colorCell("□", "FAFAFA", "1E293B"),
                colorCell("□", "FAFAFA", "1E293B"),
                colorCell("□", "FAFAFA", "1E293B"),
              ]
            }))
          ]
        }),
        br(),
        p([
          new TextRun({ text: "今天最大的收获：", bold: true, color: "7C3AED", size: 22 }),
          new TextRun({ text: "________________________________________________", size: 22 }),
        ]),
        p([
          new TextRun({ text: "还有什么不明白：", bold: true, color: "DC2626", size: 22 }),
          new TextRun({ text: "________________________________________________", size: 22 }),
        ]),
      ]
    }]
  });

  const buf = await Packer.toBuffer(doc);
  fs.writeFileSync("C:/Users/ning/WorkBuddy/Claw/信息学C++函数_素数计数_学生任务单_v2.docx", buf);
  console.log("学生任务单生成成功！");
}

makeJiaoAn().then(() => makeRenwuDan()).catch(e => console.error(e));
