#!/usr/bin/env node

const english = {
  idea: {
    title: "Idea",
    question: "Is this worth building?",
    gate: "Problem-solution fit from direct evidence.",
    evidence: [
      "Target segment is specific.",
      "Pain has frequency, severity, and a current workaround.",
      "Customer discovery includes real conversations.",
      "Competitive map includes direct, indirect, adjacent, and incumbent threats.",
      "Disconfirming evidence has been actively sought."
    ],
    risks: [
      "Building before validating.",
      "Treating a prototype as proof.",
      "Using AI to confirm the founder's belief."
    ],
    next: [
      "Sharpen the hypothesis.",
      "Run adversarial research.",
      "Audit interview questions for bias.",
      "Synthesize evidence after every five interviews.",
      "Build only the smallest prototype for one core interaction."
    ]
  },
  mvp: {
    title: "MVP",
    question: "What exactly should we build first?",
    gate: "Evidence that a specific user group returns, pays, refers, or repeatedly uses the product.",
    evidence: [
      "MVP scope is written and excludes nonessential features.",
      "Architecture context exists for coding agents.",
      "Measurement framework is defined before launch.",
      "Security review happens before real user exposure.",
      "Feedback loop separates signal from enthusiasm."
    ],
    risks: [
      "Agentic technical debt.",
      "False PMF from launch spikes.",
      "Zero-friction scope creep.",
      "Functional but insecure code."
    ],
    next: [
      "Write MVP_SCOPE.md.",
      "Write architecture context.",
      "Build in short coding-agent sessions.",
      "Define activation, retention, revenue, referral, and false-positive metrics.",
      "Run a pivot diagnostic after three weak iteration cycles."
    ]
  },
  launch: {
    title: "Launch",
    question: "Does this business deserve to grow?",
    gate: "Repeatable growth, production readiness, and founder-independent operations.",
    evidence: [
      "Acquisition channels have known unit economics.",
      "Infrastructure handles production workloads.",
      "Security and compliance work is active.",
      "Support, triage, planning, and reporting do not depend on founder memory.",
      "Technical debt has been audited and sequenced."
    ],
    risks: [
      "MVP debt becomes structural.",
      "Founder remains in every loop.",
      "Security and compliance are deferred.",
      "Expansion hides the original PMF signal."
    ],
    next: [
      "Run architecture and test coverage audit.",
      "Inventory founder-owned workflows.",
      "Automate recurring operational loops.",
      "Stand up product management cadence.",
      "Track CAC, LTV, payback, reliability, support, and security metrics."
    ]
  },
  scale: {
    title: "Scale",
    question: "Can the company compound without the founder running daily operations?",
    gate: "Systematic growth, mature operations, enterprise trust, and defensible moat.",
    evidence: [
      "Governance and compliance are auditable.",
      "Enterprise documentation, SLAs, support, observability, and incident response exist.",
      "GTM function is repeatable beyond founder-led growth.",
      "Domain expertise is captured in product and agent context.",
      "Data loops and workflow integrations increase switching cost."
    ],
    risks: [
      "Founder cannot delegate because context is uncodified.",
      "Enterprise buyers find operational immaturity.",
      "GTM ceiling appears after organic growth stalls.",
      "Competitors can copy visible features without needing your accumulated context."
    ],
    next: [
      "Map founder bottlenecks.",
      "Test what breaks if the founder is unavailable for a week.",
      "Create enterprise readiness artifacts.",
      "Build GTM segmentation, messaging, playbooks, and reporting.",
      "Turn vertical edge cases into tests, validations, integrations, and workflows."
    ]
  }
};

const chinese = {
  idea: {
    title: "Idea",
    question: "这件事值得做吗？",
    gate: "来自直接证据的 problem-solution fit。",
    evidence: [
      "Target segment 足够具体。",
      "Pain 有 frequency、severity 和 current workaround。",
      "Customer discovery 包含真实访谈。",
      "Competitive map 覆盖 direct、indirect、adjacent 和 incumbent threats。",
      "已经主动寻找 disconfirming evidence。"
    ],
    risks: [
      "未验证就 build。",
      "把 prototype 当成 proof。",
      "用 AI 证明 founder 原本就相信的东西。"
    ],
    next: [
      "收紧 hypothesis。",
      "做 adversarial research。",
      "审查 interview questions 是否有 bias。",
      "每五次访谈后综合证据。",
      "只 build 一个用于测试 core interaction 的最小 prototype。"
    ]
  },
  mvp: {
    title: "MVP",
    question: "第一版到底该做什么？",
    gate: "特定用户群体愿意 return、pay、refer 或 repeat use 的证据。",
    evidence: [
      "MVP scope 已写清楚，并排除非核心 feature。",
      "Coding agents 有 architecture context。",
      "Launch 前已定义 measurement framework。",
      "真实用户接触前已做 security review。",
      "Feedback loop 能区分 signal 和 enthusiasm。"
    ],
    risks: [
      "Agentic technical debt。",
      "把 launch spike 误判成 PMF。",
      "Zero-friction scope creep。",
      "代码可运行但不安全。"
    ],
    next: [
      "写 MVP_SCOPE.md。",
      "写 architecture context。",
      "用短 coding-agent sessions build。",
      "定义 activation、retention、revenue、referral 和 false-positive metrics。",
      "三轮弱迭代后做 pivot diagnostic。"
    ]
  },
  launch: {
    title: "Launch",
    question: "这个业务值得扩大吗？",
    gate: "Repeatable growth、production readiness 和 founder-independent operations。",
    evidence: [
      "Acquisition channels 有可解释 unit economics。",
      "Infrastructure 能承受 production workloads。",
      "Security 和 compliance 已成为 active workstream。",
      "Support、triage、planning、reporting 不依赖 founder 记忆。",
      "Technical debt 已审计并排序。"
    ],
    risks: [
      "MVP debt 变成 structural liability。",
      "Founder 仍在每个 loop 里。",
      "Security 和 compliance 被推迟。",
      "过早 expansion 掩盖原始 PMF signal。"
    ],
    next: [
      "做 architecture 与 test coverage audit。",
      "盘点 founder-owned workflows。",
      "自动化 recurring operational loops。",
      "建立 product management cadence。",
      "跟踪 CAC、LTV、payback、reliability、support 和 security metrics。"
    ]
  },
  scale: {
    title: "Scale",
    question: "公司能否在不依赖 founder 日常运营的情况下复利？",
    gate: "Systematic growth、mature operations、enterprise trust 和 defensible moat。",
    evidence: [
      "Governance 和 compliance 可被审计。",
      "Enterprise documentation、SLAs、support、observability、incident response 已存在。",
      "GTM function 不再只靠 founder-led growth。",
      "Domain expertise 已进入 product 和 agent context。",
      "Data loops 与 workflow integrations 正在提高 switching cost。"
    ],
    risks: [
      "Context 没有 codify，founder 无法交接。",
      "Enterprise buyers 发现 operational immaturity。",
      "Organic growth 到顶但 GTM engine 未建立。",
      "Competitors 能复制 visible features，却不需要你的 accumulated context。"
    ],
    next: [
      "绘制 founder bottleneck map。",
      "测试 founder 离开一周哪些 workflow 会停。",
      "创建 enterprise readiness artifacts。",
      "建立 GTM segmentation、messaging、playbooks 和 reporting。",
      "把 vertical edge cases 转成 tests、validations、integrations 和 workflows。"
    ]
  }
};

function renderList(items) {
  return items.map((item) => `- [ ] ${item}`).join("\n");
}

function wantsChinese(args) {
  return args.some((arg) => ["zh", "zh-cn", "cn", "chinese", "中文"].includes(arg.toLowerCase()));
}

const args = process.argv.slice(2);
const stageName = (args[0] || "").toLowerCase();
const data = wantsChinese(args.slice(1)) ? chinese : english;

if (!stageName || !data[stageName]) {
  console.error("Usage: node scripts/stage-checklist.mjs <idea|mvp|launch|scale> [zh]");
  process.exit(1);
}

const stage = data[stageName];
const labels = data === chinese
  ? {
      mainQuestion: "核心问题",
      stageGate: "阶段门",
      evidence: "证据检查",
      risks: "风险检查",
      next: "下一步动作"
    }
  : {
      mainQuestion: "Main Question",
      stageGate: "Stage Gate",
      evidence: "Evidence Checklist",
      risks: "Risk Checklist",
      next: "Next Moves"
    };

console.log(`# ${stage.title} Stage Checklist

## ${labels.mainQuestion}
${stage.question}

## ${labels.stageGate}
${stage.gate}

## ${labels.evidence}
${renderList(stage.evidence)}

## ${labels.risks}
${renderList(stage.risks)}

## ${labels.next}
${renderList(stage.next)}
`);
