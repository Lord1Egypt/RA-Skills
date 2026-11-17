const SIGNALS = {
  deliverable: {
    label: "最终交付物",
    pattern: /输出|生成|创建|制作|写成|整理成|交付|文档|报告|页面|表格|脚本|代码|原型|图片|文件|create|build|generate|produce|deliver|report|document|page|file/i,
  },
  scope: {
    label: "范围和排除项",
    pattern: /范围|只改|仅|不要|不改|排除|限定|以内|之外|scope|only|do not|don't|without|exclude/i,
  },
  inputs: {
    label: "输入材料",
    pattern: /输入|附件|文件|路径|链接|参考|数据|源码|现有|基于|input|attachment|file|path|link|source|based on/i,
  },
  constraints: {
    label: "约束和边界",
    pattern: /必须|需要|限制|格式|尺寸|语言|边界|权限|默认|保持|constraint|must|required|limit|format|permission/i,
  },
  acceptance: {
    label: "验收标准",
    pattern: /验收|完成标准|成功标准|做到|期望结果|判断标准|acceptance|done when|success criteria|expected result/i,
  },
  verification: {
    label: "验证方式",
    pattern: /验证|测试|检查|截图|日志|确认|试跑|对比|test|verify|check|screenshot|log|validate/i,
  },
};

const CORRECTION_PATTERN = /不对|不是|改成|换成|还是|不要|遗漏|漏了|重新|其实|应该|之前|刚才|wrong|instead|change to|redo|missing/i;

const CATEGORY_TEMPLATES = {
  "代码开发": "请在{项目或目录}完成{功能或修复}。输入材料：{源码、报错或接口信息}。范围：{允许修改的模块}；不要修改：{排除范围}。必须满足：{行为约束}。完成后运行{测试命令}，并说明改动文件、验证结果和剩余风险。",
  "文档与内容": "请基于{输入材料}输出{文档或内容类型}。读者是{目标读者}，用途是{使用场景}。必须包含{核心章节}，不要包含{排除内容}。验收标准：{结构、长度、格式和准确性要求}。",
  "产品与设计": "请围绕{页面、流程或功能}完成{PRD、原型或设计方案}。目标用户：{用户}。范围：{本次处理部分}；不要改：{排除范围}。覆盖{核心路径、状态和边界场景}，最终以{文件或页面形式}交付，并按{验收方式}验证。",
  "数据与表格": "请基于{数据文件或口径}完成{分析或表格产物}。先确认{字段、计算和去重规则}，再输出{目标格式}。异常值和缺失值按{规则}处理。完成后校验{总数、重复、格式和关键计算}。",
  "研究与分析": "请围绕{研究问题}进行分析。优先使用{资料范围}，区分事实、推断和建议。输出{结构和格式}，对关键结论给出{证据或来源}，并说明不确定性和不能下结论的部分。",
  "系统自动化": "请把{任务或脚本}设置为{频率或触发条件}自动执行。先检查现有任务是否重复，保留原文件不动。日志写到{位置}，失败时输出{告警或状态}。最后通过系统触发方式试跑，并验证退出码、日志和产物。涉及系统配置或权限扩大前先询问。",
  "Skill 与工具": "请把{能力}整理成可复用 skill 或工具。明确触发场景、输入、输出、依赖、失败处理、权限边界和验证方式。SKILL.md 只保留核心流程，详细规则放 references，稳定执行放 scripts。完成后运行校验和真实试用。",
  "视觉素材": "请生成{素材类型}，用于{使用场景}。画幅和尺寸：{要求}；必须出现：{元素}；禁止出现：{元素}；风格参考：{参考}。输出{数量和格式}，并检查文字、构图和可用性。",
  "其他任务": "请完成{目标}，最终交付{产物}。输入材料是{材料}，范围是{范围}，约束是{约束}，不要做{排除项}。完成标准是{验收标准}，请在交付前执行{验证方式}。",
};

export const CATEGORY_PATTERNS = [
  ["产品与设计", /PRD|需求|原型|Figma|流程|交互|页面设计|产品方案|wireframe|prototype|user flow/i],
  ["系统自动化", /自动化|定时|launchd|launchctl|cron|脚本执行|后台任务|schedule|automation|systemd/i],
  ["Skill 与工具", /SKILL\.md|skill|插件|plugin|MCP|工具|CLI|workflow|agent tool/i],
  ["数据与表格", /表格|Excel|CSV|数据|统计|字段|口径|报表|公式|透视|xlsx|spreadsheet|dataset/i],
  ["视觉素材", /图片|海报|主视觉|KV|插画|照片|图标|image|poster|visual|illustration/i],
  ["研究与分析", /调研|分析|研究|对比|评估|审查|证据|来源|research|analysis|compare|review/i],
  ["文档与内容", /文档|README|说明|总结|文案|文章|邮件|方案书|markdown|copywriting|documentation/i],
  ["代码开发", /代码|开发|修复|bug|报错|测试|接口|API|数据库|前端|后端|组件|函数|class|typescript|javascript|python|java|git|commit|code|debug|fix|test/i],
];

export function classifyCategory(text, artifacts = []) {
  const haystack = `${text || ""}\n${artifacts.map((item) => item.relative || item).join("\n")}`;
  for (const [category, pattern] of CATEGORY_PATTERNS) {
    if (pattern.test(haystack)) return category;
  }
  return "其他任务";
}

export function analyzePrompt(messages = [], category = "其他任务") {
  const cleanMessages = messages.map((item) => String(item || "").trim()).filter(Boolean);
  const first = cleanMessages[0] || "";
  const signals = Object.fromEntries(
    Object.entries(SIGNALS).map(([key, item]) => [key, item.pattern.test(first)]),
  );
  const missing = Object.entries(signals)
    .filter(([, present]) => !present)
    .map(([key]) => SIGNALS[key].label);
  const correctionCount = cleanMessages.slice(1).filter((message) => CORRECTION_PATTERN.test(message)).length;
  const presentCount = Object.values(signals).filter(Boolean).length;
  const level = presentCount >= 5 && correctionCount <= 1
    ? "green"
    : presentCount <= 1 || correctionCount >= 3
      ? "red"
      : "yellow";
  const summary = missing.length
    ? `第一条请求缺少${missing.slice(0, 3).join("、")}，后续更容易通过多轮补充规则。`
    : "第一条请求已经覆盖主要目标、边界和验收信息。";
  const correctionNote = correctionCount
    ? ` 后续检测到 ${correctionCount} 次方向或约束修正。`
    : "";
  return {
    promptAssessment: {
      signals,
      missing,
      correctionCount,
      summary: `${summary}${correctionNote}`.trim(),
    },
    level,
    nextPrompt: CATEGORY_TEMPLATES[category] || CATEGORY_TEMPLATES["其他任务"],
  };
}

export function summarizeActions({ sessionCount = 0, artifacts = [], category = "其他任务" }) {
  const actions = [];
  if (sessionCount) actions.push(`围绕“${category}”完成 ${sessionCount} 次主要会话。`);
  if (artifacts.length) {
    const types = [...new Set(artifacts.map((item) => extensionLabel(item.relative)))].filter(Boolean).slice(0, 4);
    actions.push(`形成 ${artifacts.length} 个可识别产物${types.length ? `，主要包括${types.join("、")}` : ""}。`);
  } else {
    actions.push("主要成果保留在对话结论中，本周没有识别到对应文件产物。");
  }
  return actions;
}

function extensionLabel(file) {
  const ext = String(file || "").toLowerCase().match(/\.[a-z0-9]+$/)?.[0] || "";
  return ({
    ".md": "Markdown 文档",
    ".html": "HTML 页面",
    ".json": "JSON 数据",
    ".csv": "CSV 表格",
    ".xlsx": "Excel 表格",
    ".xls": "Excel 表格",
    ".png": "PNG 图片",
    ".jpg": "JPG 图片",
    ".jpeg": "JPG 图片",
    ".webp": "WebP 图片",
    ".pdf": "PDF 文件",
    ".docx": "Word 文档",
    ".pptx": "演示文稿",
    ".zip": "压缩包",
  })[ext] || "";
}
