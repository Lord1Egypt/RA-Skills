// catalog.mjs — the routing label set. Stage 1 picks a form family; stage 2 picks a diagram type
// inside the family. Each diagram type carries a description (used as the classifier instruction) and a
// minimal skeleton which the model fills in.
export const FAMILIES = {
  prose:     'a plain fact, definition, conclusion or recommendation; one idea that needs no picture',
  steps:     'an ordered list of actions or a process, possibly with branches or decisions',
  sequence:  'messages or requests passed back and forth between two or more actors over time',
  state:     'states of one thing and the transitions between them; a lifecycle; or work items grouped on a board by status',
  structure: 'parts of a system and how they connect: architecture, components, dependencies, data model, who can use it, its requirements, events, or the byte layout of a message',
  hierarchy: 'a hierarchy, taxonomy, directory or folder tree, or a breakdown of a topic into parts',
  timeline:  'dated or ordered events, history, versions or a schedule',
  table:     'several options or items compared across several attributes',
  chart:     'numbers to compare: amounts, shares, trends over time, flows between quantities, scores',
  slider:    'how a result changes when one parameter value is made larger or smaller',
  tabs:      'two to five alternative answers or approaches, each described in detail',
  landscape: 'placing things on a strategy map: a value chain by how evolved each part is, or problems by how predictable they are',
  grammar:   'the syntax or grammar of a language, command, file format, identifier or pattern',
};

export const FAMILY_INSTRUCTION = 'Pick the visual form that best explains this block of an answer: ' +
  Object.entries(FAMILIES).map(([k, v]) => `${k} = ${v}`).join('; ') + '.';

export const TYPES = {
  steps: {
    flowchart: { desc: 'steps with decisions or branches, one actor', skel: 'flowchart LR\n  A[第一步] --> B{判断?}\n  B -- 是 --> C[结果一]\n  B -- 否 --> D[结果二]' },
    swimlane: { desc: 'steps handed off between several people, teams or roles', skel: 'swimlane-beta LR\n  subgraph 角色甲\n    a[动作一]\n  end\n  subgraph 角色乙\n    b[动作二]\n  end\n  a --> b' },
    agentflow: { desc: 'an AI agent or tool-calling workflow with inputs, tools and outputs', skel: 'agentflow-beta TB\n  flow main["流程"]\n    inp["输入"]@{ shape: input }\n    tool["工具"]@{ shape: tool }\n    inp --> tool\n  end' },
    numbered: { desc: 'a short linear list of actions with no branches', skel: null },
  },
  sequence: {
    sequenceDiagram: { desc: 'messages between actors in time order', skel: 'sequenceDiagram\n  autonumber\n  participant A as 甲\n  participant B as 乙\n  A->>B: 请求\n  B-->>A: 响应' },
  },
  state: {
    stateDiagram: { desc: 'states and transitions', skel: 'stateDiagram-v2\n  [*] --> 状态一\n  状态一 --> 状态二 : 事件\n  状态二 --> [*]' },
    journey: { desc: 'a person moving through stages with a feeling or score at each', skel: 'journey\n  title 用户旅程\n  section 阶段一\n    动作: 5: 用户' },
    kanban: { desc: 'work items or tasks grouped into columns by status, like a board', skel: 'kanban\n  todo[待办]\n    t1[任务一]\n  doing[进行中]\n    t2[任务二]@{ assigned: \'负责人\' }\n  done[已完成]\n    t3[任务三]' },
  },
  structure: {
    flowchart: { desc: 'a small set of connected components or services', skel: 'flowchart LR\n  subgraph 前端\n    UI[界面]\n  end\n  subgraph 后端\n    API[接口] --> DB[(数据库)]\n  end\n  UI --> API' },
    architecture: { desc: 'cloud or infrastructure services grouped into boundaries', skel: 'architecture-beta\n  group app(cloud)[应用]\n  service api(server)[接口] in app\n  service db(database)[数据库] in app\n  api:R --> L:db' },
    erDiagram: { desc: 'database tables or entities with fields and relationships', skel: 'erDiagram\n  USER ||--o{ ORDER : places\n  USER {\n    string id PK\n  }' },
    classDiagram: { desc: 'classes or types with members and inheritance', skel: 'classDiagram\n  Animal <|-- Dog\n  Animal : +name\n  Dog : +bark()' },
    block: { desc: 'a layout of blocks or modules in rows and columns', skel: 'block\n  columns 3\n  a["模块一"] b["模块二"] c["模块三"]' },
    c4: { desc: 'one system in its context: the people who use it and the external systems it talks to', skel: 'C4Context\n  title 系统上下文\n  Person(user, "用户", "做什么")\n  System(app, "本系统", "负责什么")\n  System_Ext(ext, "外部系统")\n  Rel(user, app, "使用")\n  Rel(app, ext, "调用", "HTTPS")' },
    usecase: { desc: 'which actors or roles can do which actions with a system', skel: 'usecase-beta\n  direction LR\n  actor u("角色甲")\n  actor v("角色乙")\n  systemBoundary sys("系统")\n    a("功能一")\n    b("功能二")\n  end\n  u --> a\n  v --> b' },
    requirement: { desc: 'requirements and which parts satisfy or verify them', skel: 'requirementDiagram\n  requirement req1 {\n    id: 1\n    text: "需求描述"\n    risk: medium\n    verifymethod: test\n  }\n  element part1 {\n    type: "模块"\n  }\n  part1 - satisfies -> req1' },
    eventmodeling: { desc: 'commands, events and read models of a system over time (event sourcing, CQRS)', skel: 'eventmodeling\n  timeframe 01 ui OrderPage\n  timeframe 02 command PlaceOrder\n  timeframe 03 event OrderPlaced\n  timeframe 04 readmodel OrderList' },
    packet: { desc: 'the bit or byte layout of a message, header or binary format', skel: 'packet-beta\n  0-15: "字段一"\n  16-31: "字段二"\n  32-63: "字段三"' },
  },
  hierarchy: {
    mindmap: { desc: 'a topic broken into ideas and sub-ideas', skel: 'mindmap\n  root((主题))\n    分支一\n      要点\n    分支二' },
    treeView: { desc: 'a directory or file tree', skel: 'treeView-beta\n  project/\n    src/\n      index.js ## 入口\n    README.md' },
    treemap: { desc: 'a hierarchy where each part has a size or amount', skel: 'treemap-beta\n"总计"\n  "部分一": 60\n  "部分二": 40' },
    ishikawa: { desc: 'causes of one problem grouped by category', skel: 'ishikawa-beta\n  问题\n  人员\n    原因一\n  流程\n    原因二' },
  },
  timeline: {
    timeline: { desc: 'historical events or milestones by date', skel: 'timeline\n  title 发展历程\n  2014 : 事件一\n  2018 : 事件二' },
    gantt: { desc: 'a schedule of tasks with durations and dependencies', skel: 'gantt\n  dateFormat YYYY-MM-DD\n  section 阶段\n  任务一 :a1, 2026-01-01, 10d\n  任务二 :after a1, 5d' },
    gitGraph: { desc: 'git branches, commits and merges', skel: 'gitGraph\n  commit\n  branch dev\n  commit\n  checkout main\n  merge dev' },
  },
  chart: {
    pie: { desc: 'shares or percentages of one whole', skel: 'pie title 占比（来源：…）\n  "甲" : 40\n  "乙" : 60' },
    bar: { desc: 'amounts compared across categories', skel: 'xychart\n  title "对比（来源：…）"\n  x-axis ["甲", "乙", "丙"]\n  y-axis "单位" 0 --> 100\n  bar [30, 60, 90]' },
    line: { desc: 'values changing over time', skel: 'xychart\n  title "趋势（来源：…）"\n  x-axis ["1月", "2月", "3月"]\n  y-axis "单位" 0 --> 100\n  line [20, 50, 80]' },
    sankey: { desc: 'quantities flowing from sources to destinations', skel: 'sankey\n\n来源甲,去向乙,10\n来源甲,去向丙,5' },
    radar: { desc: 'several items scored on several criteria', skel: 'radar-beta\n  axis a["维度一"], b["维度二"], c["维度三"]\n  curve x["选项甲"]{4, 3, 5}\n  max 5' },
    quadrant: { desc: 'items placed on two axes to show a trade-off', skel: 'quadrantChart\n  x-axis 低成本 --> 高成本\n  y-axis 低收益 --> 高收益\n  选项甲: [0.3, 0.7]' },
    venn: { desc: 'overlap between sets', skel: 'venn-beta\n  set A["集合一"]\n  set B["集合二"]\n  union A,B["共同部分"]' },
  },
  landscape: {
    wardley: { desc: 'a value chain from user need down to components, placed by how evolved each one is (genesis to commodity)', skel: 'wardley-beta\n  title 价值链\n  anchor "用户" [0.95, 0.6]\n  component "能力一" [0.7, 0.4]\n  component "基础设施" [0.2, 0.9]\n  "用户" -> "能力一"\n  "能力一" -> "基础设施"' },
    cynefin: { desc: 'problems sorted into clear, complicated, complex and chaotic domains', skel: 'cynefin-beta\n  title 问题分类\n  clear\n    "有标准做法的事"\n  complicated\n    "需要专家分析的事"\n  complex\n    "只能试了才知道的事"\n  chaotic\n    "先止血的事"' },
  },
  grammar: {
    railroad: { desc: 'grammar rules drawn as railroad (syntax) diagrams', skel: 'railroad-ebnf-beta\n  title "语法"\n  rule = part , { "," , part } ;\n  part = "a" | "b" ;' },
  },
};

export const typeInstruction = fam => `Pick the diagram type for this block: ` +
  Object.entries(TYPES[fam]).map(([k, v]) => `${k} = ${v.desc}`).join('; ') + '.';
