// Judgments from JEV (atomic nouls), decisions in code (rules + priority).
// Each question names the narrowest observable fact and states both sides as concrete situations
// (TypeSafe: literal reading — put the boundary case in the criteria). The shared boundary for every
// structure question: a word, number, date or command that only APPEARS in the block is not how the
// block is ORGANIZED. Context every question shares lives once in the state (stateOf).
const N = (q, yes, no) => ({ type: 'noul', instructions: q, criteria: { true: yes, false: no } });
export const STATE_NOTE = 'block is one part of a longer written answer. A question about how block is organized asks about the whole block, not about a word, number, date or command it happens to mention.';
export const stateOf = text => ({ about: STATE_NOTE, block: text });
export const FACETS = {
  steps: N('Is `block` a series of actions done one after another in a set order, by the reader or by anyone else?',
    'Most of the block is actions in a fixed order, such as "unplug the router, wait 30 seconds, plug it back in, check the light" or "first we collect data, then we train, then we test".',
    'The block explains, describes or recommends, and any actions in it are separate pieces of advice or a single action.'),
  decision: N('Does `block` say that what to do next depends on which of two or more conditions holds?',
    'The block branches on a check, such as "if the light is green, continue; if it is red, call support".',
    'The block has no branch, or one condition appears inside a single sentence of advice or explanation.'),
  roles_handoff: N('Does `block` assign each step of a process to a named person, team or role?',
    'Each step has an owner, such as "sales signs the contract, legal reviews it, finance issues the invoice".',
    'Roles are mentioned, but the block does not walk through steps that pass from one owner to the next.'),
  agent_tools: N('Does `block` describe an AI agent deciding which named tools to call?',
    'The block walks through an agent calling tools, such as "the agent calls search, reads the page, then calls the calculator".',
    'The block talks about AI or tools in general without an agent calling them in turn.'),
  messages: N('Does `block` walk through, in order, messages that two or more named parties send to each other?',
    'Most of the block is who sends what to whom in turn, such as "the client asks for a token, the server returns it, the client sends the request with the token".',
    'The block explains why a protocol or system behaves as it does, naming a message or request only in passing.'),
  states: N('Does `block` name the states one object passes through over its life?',
    'The block names an object\'s states, such as "an order is pending, then paid, then shipped, then closed".',
    'The block describes things, steps or options rather than one object changing state.'),
  feelings: N('Does `block` say how a person feels at each stage of an experience?',
    'Each stage comes with a feeling, such as "booking is easy, waiting is anxious, arrival is a relief".',
    'Feelings are not given stage by stage.'),
  status_columns: N('Does `block` sort work items into status groups such as to do, doing and done?',
    'Items are grouped by status, such as "to do: design; doing: backend; done: login page".',
    'The block does not group items by work status.'),
  infra: N('Is `block` mainly about servers, databases, queues or other infrastructure and how they connect?',
    'The block lays out infrastructure pieces, such as "the load balancer sends traffic to two app servers that share one database".',
    'Infrastructure is named in passing in a block about something else.'),
  db_tables: N('Does `block` define database tables or entities with their fields?',
    'The block lists tables with fields, such as "users: id, email; orders: id, user_id, total".',
    'The block mentions data or a database without defining tables and fields.'),
  classes: N('Does `block` define programming classes or types with their fields or methods?',
    'The block lists types with members, such as "Shape has area(); Circle extends Shape with radius".',
    'The block mentions code or types without defining their members.'),
  modules_grid: N('Does `block` describe a software or hardware system built from modules arranged in layers or rows?',
    'The block names the layers of a system and the modules in each, such as "UI layer: web and app; service layer: orders and payments; data layer: database and cache".',
    'The word layer or level labels ideas, stages or management practices rather than parts of a built system.'),
  users: N('Does `block` name the kinds of people who use a system?',
    'The block names user groups of a system, such as "customers browse, staff fulfil orders, admins manage prices".',
    'People are mentioned but not as user groups of a system.'),
  external_systems: N('Does `block` name outside systems that the described system calls?',
    'The block names external services the system depends on, such as "it calls Stripe for payments and SendGrid for email".',
    'No outside system is named as something the system calls.'),
  role_actions: N('Does `block` list what each kind of user is allowed to do in a software system?',
    'The block maps users of a system to the features they may use, such as "viewers can read documents, editors can change them, admins can delete them".',
    'The block says what job or responsibility each person, model or component has, or does not describe permissions at all.'),
  requirements: N('Is `block` a list of numbered or named requirements that a system must meet?',
    'The block states requirements as such, such as "R1: the system must log every login; R2: it must lock after five failures".',
    'The block gives advice, explanation or tasks rather than requirements a system must meet.'),
  events_commands: N('Does `block` name events in a system that result from named commands?',
    'The block pairs commands with events, such as "PlaceOrder produces OrderPlaced, which triggers ReserveStock".',
    'The block does not pair commands with the events they produce.'),
  bit_layout: N('Does `block` give the bit or byte layout of a data format?',
    'The block gives field positions and widths, such as "bits 0-3 version, bits 4-7 header length".',
    'No bit or byte positions are given.'),
  subtopics: N('Is `block` mainly a map of one topic broken into named parts, where the names of the parts are what the reader should take away?',
    'The block exists to lay out the parts of a topic, each with its own sub-points, such as "Diet: less sugar, more fibre; Exercise: walk daily, lift twice a week; Sleep: same bedtime, no screens".',
    'The block makes a point, explains how something works, or gives steps or advice, and its lists are evidence, examples or details for that; or it is one flat list; or its parts are periods of time or priorities.'),
  file_tree: N('Does `block` show a directory or file tree?',
    'The block shows folders and files nested inside each other.',
    'Paths may be mentioned, but no tree of folders and files is shown.'),
  nested_parts: N('Does `block` break some of its parts into smaller sub-parts?',
    'Some parts of the block are divided further, such as a heading with a list under it.',
    'The block is flat: one paragraph or one list with no level below it.'),
  part_sizes: N('Does `block` give a size or amount for each part of one whole?',
    'Each part of a whole has its size, such as "the budget is 50% housing, 30% food, 20% savings".',
    'Numbers appear, but they are not the sizes of the parts of one whole.'),
  causes: N('Is `block` a list of several causes of one named problem?',
    'The block names one problem and lists its causes, such as "slow builds come from cold caches, large images and serial tests".',
    'The block explains, advises or lists effects rather than listing causes of one problem.'),
  dated_events: N('Is `block` a sequence of events ordered by their dates?',
    'Three or more events each have their own date and the dates order the block, such as "1969 first message, 1983 TCP/IP, 1991 the web".',
    'A date or year is background to an explanation, or only one or two dates appear.'),
  task_durations: N('Does `block` give how long each of several tasks takes?',
    'Several tasks each have a duration, such as "design takes two weeks, build four weeks, testing one week".',
    'A duration appears once or describes something other than tasks.'),
  git: N('Does `block` walk through, in order, the history of one set of git branches: where each branch starts, its commits and where it merges?',
    'The block follows one branch history step by step, such as "branch feature from main, commit twice, merge back into main".',
    'The block lists variants of a workflow, gives commands to choose from, or explains a branching policy without following one history.'),
  percentages: N('Is `block` built around several percentages that are shares of one whole?',
    'Three or more parts of one whole each get a percentage, such as "45% rent, 30% food, 25% savings".',
    'A percentage appears as a threshold, a change or a single figure inside a sentence.'),
  same_unit_numbers: N('Is `block` mainly a comparison of three or more items by one number in the same unit?',
    'The point of the block is how three or more items compare on one measure, such as "Paris 2.1 million, Rome 2.8 million, Madrid 3.3 million".',
    'Numbers are details inside separate points or rules, or they do not measure the same thing across three or more items.'),
  over_time: N('Does `block` give values of one measure at three or more points in time?',
    'One measure is tracked over time, such as "sales were 10 in 2021, 14 in 2022 and 19 in 2023".',
    'Times and numbers appear, but not as one measure tracked at several points in time.'),
  flows_amounts: N('Does `block` give amounts that move from sources to destinations?',
    'Amounts flow between named places, such as "of 100 visitors, 60 sign up and 40 leave; of the 60, 20 pay".',
    'No amounts move from one named place to another.'),
  scores_criteria: N('Does `block` give each item a numeric score on each of several criteria?',
    'Each item is scored on the same criteria, such as "A: speed 4, cost 2, quality 5; B: speed 3, cost 4, quality 3".',
    'Items are described in words, or have one number each.'),
  two_axes: N('Does `block` place each item as high or low on the same two named dimensions?',
    'Every item is rated on two axes, such as "task A: high impact, low effort; task B: low impact, high effort".',
    'Two dimensions are named, but items are not placed on both, or the block explains how to use such a grid.'),
  sets_overlap: N('Does `block` say which members belong to both of two named groups?',
    'The block names members in each group and in both, such as "mammals that fly: bats; birds that cannot fly: penguins".',
    'The block does not describe overlapping groups.'),
  evolution: N('Does `block` place components by how mature or commoditized they are?',
    'Components are placed from custom-built to commodity, such as "the model is custom, the database is a product, electricity is a commodity".',
    'Maturity of components is not described.'),
  domains: N('Does `block` sort problems by how predictable cause and effect are?',
    'Problems are sorted into clear, complicated, complex and chaotic kinds.',
    'Problems are not sorted by predictability.'),
  grammar: N('Does `block` give grammar or syntax rules for a language or format?',
    'The block gives rules for what can follow what, such as "an identifier is a letter followed by letters or digits".',
    'The block uses a language without stating its syntax rules.'),
  items_attrs: N('Does `block` compare two or more items on the same two or more attributes?',
    'Each item gets a value for the same attributes, such as "car: fast, expensive; bike: slow, cheap".',
    'Items are each described in their own way, or each item has only a name and a single explanation.'),
  warning: N('Does `block` warn the reader that something bad will happen if they do a specific thing?',
    'The block gives a caution tied to an action, such as "do not unplug the drive while it is writing, or you will lose data".',
    'The block gives advice, limits or risks in general without a caution tied to an action.'),
  alternatives: N('Does `block` present two or more alternative approaches the reader chooses between?',
    'The block names options the reader picks one of, each with its own details, such as "rent if you may move within two years; buy if you will stay longer".',
    'The block explains one method, or uses a word like plan or option once without offering a choice.'),
  parameter: N('Does `block` explain how a result changes when one setting grows or shrinks?',
    'One setting drives the result, such as "the higher the learning rate, the faster training starts but the less stable it is".',
    'Several separate actions or facts are listed rather than the effect of one setting.'),
  code: N('Does `block` give code or a command that the reader is meant to copy and run?',
    'The block contains code lines or a command line to type, such as "run pip install requests" or several lines of a program.',
    'A command or function name only labels something in a list or form, and the block is about something else.'),
  loop_back: N('Does `block` say that after some step the work goes back to an earlier step?',
    'The block loops, such as "if the test fails, fix the code and run the test again".',
    'The block moves forward only.'),
  paths_merge: N('Does `block` describe two different paths that later continue with the same step?',
    'Two branches rejoin, such as "pay by card or by bank transfer; either way, you then receive a receipt".',
    'The block has one path, or branches that never rejoin.'),
  multi_branch: N('Does `block` contain two or more separate checks that each decide what happens next?',
    'At least two decision points, such as "if the file exists, open it, else create it; if it is locked, wait".',
    'The block has at most one check, or conditions that are only part of advice.'),
  any_order: N('Could the items in `block` be done in any order without changing the result?',
    'The items are independent, such as a packing list or a set of tips.',
    'Later items need earlier ones to be done first.'),
  uses_previous: N('Does a later action in `block` need the result of an earlier action?',
    'An action uses what an earlier one produced, such as "download the file, then open the downloaded file".',
    'The items stand on their own, or the block contains no actions.'),
  back_and_forth: N('Does work in `block` pass between the same two roles more than once?',
    'The same two roles hand work back and forth, such as "the writer drafts, the editor comments, the writer revises, the editor approves".',
    'No work passes back and forth between two roles.'),
  transitions: N('Does `block` say which event moves one object from one named state to another?',
    'Events change an object\'s state, such as "paying moves the order from pending to paid".',
    'No event moves an object between named states.'),
  side_by_side: N('Does every item in `block` give its own value for the same two or more named attributes, so the items can be compared side by side?',
    'All items share the same attribute labels with a value each, such as "Plan A: price 10, storage 50 GB; Plan B: price 20, storage 200 GB".',
    'Items each get a different kind of explanation, or only a name and one description.'),
  one_task: N('Do the items in `block` together complete one specific task that the reader carries out step by step?',
    'The items are the steps of one task with one end result, such as "install the app, sign in, connect the printer, print a test page".',
    'The items are separate tips, checks, priorities or plan items that do not add up to one task done in one go.'),
  time_buckets: N('Are the items in `block` grouped by time period, phase or priority?',
    'Items sit under periods or priorities, such as "this week: …; this month: …; this year: …" or "first priority: …".',
    'Items are not grouped by time or priority.'),
  advice: N('Is `block` mainly a set of separate recommendations, rules or plan items?',
    'Most of the block is independent recommendations, such as "sleep eight hours; drink water; walk daily".',
    'The block mainly explains, describes, compares or walks through one procedure.'),
  system_parts: N('Does `block` name the components of a software or hardware system and which connects to which?',
    'Components and their connections are given, such as "the app calls the API, which reads from the database".',
    'The block does not describe how the parts of a system connect.'),
};
export const YES = 0.7;
// Forms with a narrow vocabulary need a clearer yes: JEV says "yes" readily on long text, and a wrong
// specialised diagram costs the reader more than a missed one.
export const STRICT = +(process.env.PE_STRICT || 0.85);
const NARROW = new Set(['subtopics','part_sizes','over_time','usecase','requirements','events_commands','bit_layout','causes','dated_events','task_durations','git','flows_amounts','scores_criteria','two_axes','sets_overlap','evolution','domains','grammar','parameter','agent_tools','modules_grid','external_systems','users','warning','role_actions']);
const Y = (s, k) => s[k] >= (NARROW.has(k) ? STRICT : YES);
// 每个组件 = 原子判断的布尔组合（代码里，可审、可测）
export const RULES = {
  // parts that feed each other also make a flow, but only when the text draws the links (two or more arrows)
  flowchart: s => (Y(s,'steps') && Y(s,'decision')) || (Y(s,'system_parts') && !Y(s,'infra') && s.__arrows >= 2),
  swimlane: s => Y(s,'steps') && Y(s,'roles_handoff'),
  agentflow: s => Y(s,'agent_tools'),
  sequenceDiagram: s => Y(s,'messages'),
  stateDiagram: s => Y(s,'states') && Y(s,'decision'),
  journey: s => Y(s,'feelings'),
  kanban: s => Y(s,'status_columns'),
  architecture: s => Y(s,'infra') && Y(s,'system_parts'),
  erDiagram: s => Y(s,'db_tables'),
  classDiagram: s => Y(s,'classes'),
  block: s => Y(s,'modules_grid'),
  c4: s => Y(s,'users') && Y(s,'external_systems'),
  usecase: s => Y(s,'role_actions'),
  requirement: s => Y(s,'requirements'),
  eventmodeling: s => Y(s,'events_commands'),
  packet: s => Y(s,'bit_layout'),
  mindmap: s => Y(s,'subtopics') && !Y(s,'steps') && !(s.time_buckets >= 0.85),
  treeView: s => Y(s,'file_tree'),
  treemap: s => Y(s,'nested_parts') && Y(s,'part_sizes') && !Y(s,'percentages'),
  ishikawa: s => Y(s,'causes'),
  timeline: s => Y(s,'dated_events'),
  gantt: s => Y(s,'task_durations'),
  gitGraph: s => Y(s,'git'),
  pie: s => Y(s,'percentages') && !Y(s,'parameter') && !Y(s,'over_time'),
  bar: s => Y(s,'same_unit_numbers') && !Y(s,'over_time') && !Y(s,'items_attrs'),
  line: s => Y(s,'over_time'),
  sankey: s => Y(s,'flows_amounts'),
  radar: s => Y(s,'scores_criteria'),
  quadrant: s => Y(s,'two_axes'),
  venn: s => Y(s,'sets_overlap'),
  wardley: s => Y(s,'evolution'),
  cynefin: s => Y(s,'domains'),
  railroad: s => Y(s,'grammar'),
  table: s => s.side_by_side >= 0.85 || (s.side_by_side >= 0.7 && s.__grid),
  callout: s => Y(s,'warning'),
  // conditions inside a step of one task stay in that step (DITA task / Horn procedure); only a plan with branches is blocked
  steps: s => Y(s,'steps') && s.uses_previous >= 0.8 && (!Y(s,'decision') || s.__list),
  tabs: s => Y(s,'alternatives'),
  slider: s => Y(s,'parameter'),
  code: s => Y(s,'code'),
};

// Specific forms outrank generic ones; first match is the primary.
export const PRIORITY = ['packet','gitGraph','treeView','erDiagram','classDiagram','railroad','wardley','cynefin','eventmodeling','requirement','c4','usecase','journey','kanban','agentflow','ishikawa','gantt','timeline','sankey','treemap','pie','radar','quadrant','venn','line','bar','swimlane','sequenceDiagram','stateDiagram','architecture','block','slider','table','tabs','flowchart','mindmap','code','steps','callout'];
// Lexical facts code can check exactly; JEV is not asked to count or parse.
// Parents that carry two or more sub-items: an indented list under a list item, or a list under a heading or a
// "label：" line. A hierarchy is what a mindmap or tree shows that a flat list cannot.
export function branchingParents(t) {
  const lines = t.split('\n'); let n = 0;
  for (let i = 0; i < lines.length; i++) {
    const l = lines[i], ind = l.match(/^\s*/)[0].length;
    const item = /^\s*([-*]|\d+[.)])\s/.test(l);
    if (!(/^\s*#{2,6}\s/.test(l) || /[:：]\s*$/.test(l) || item)) continue;
    let kids = 0;
    for (let j = i + 1; j < lines.length; j++) {
      const m = lines[j], mi = m.match(/^\s*/)[0].length;
      if (/^\s*#{2,6}\s/.test(m)) break;
      if (/^\s*([-*]|\d+[.)])\s/.test(m) && (mi > ind || !item)) kids++;
      else if (m.trim()) break;
    }
    if (kids >= 2) n++;
  }
  // inline: "所有权（借用、生命周期）、类型系统（trait、泛型）" — a part followed by its sub-parts in brackets
  n += (t.match(/[^，。；、\s（(]{1,20}[（(](?!如|例如|比如|e\.g)[^）)]*[、,，][^）)]*[）)]/g) || []).length;
  return n;
}
// The text is already a list of three or more items that make up most of it.
export const listShaped = t => { const ls = t.split('\n').filter(l => l.trim()); const it = ls.filter(l => /^\s*([-*]|\d+[.)])\s/.test(l)).length; return it >= 2 && it >= ls.length * 0.6; };
// An item points at another item: a jump or a loop that a list cannot draw.
export const crossRef = t => /(回到|返回|退回|跳到|跳回|重复)(第\s*\d+\s*步|步骤|上一步|前一步|开头|起点|[A-Z①-⑨]\b)?|再走一遍|go back to|return to step|repeat from/i.test(t);
// the most numbers that share one unit ("72 美元 … 68 美元 … 65 美元" → 3)
// Counting words (块、个、项…) count things, they are not a measure to compare on a bar.
const COUNTERS = new Set('块个项页次题条处份张名人轮步种类位件段行列组批篇章节号年根台'.split(''));
// thresholds (≥90 cm) and range ends (18.5–23.9) are limits, not magnitudes to compare
const sameUnit = t => { const c = {}; for (const m of t.matchAll(/(?<![≥≤<>＜＞~–\-\d.])\d+(?:\.\d+)?\s*(%|[a-zA-Z]+|[\u4e00-\u9fa5])/g)) if (!COUNTERS.has(m[1]) && !/^\s*[–~-]/.test(t.slice(m.index + m[0].length - m[1].length - 1, m.index + m[0].length))) c[m[1]] = (c[m[1]] || 0) + 1; return Math.max(0, ...Object.values(c)); };
// sentences or list items: the nodes a diagram would have
const units = t => t.split(/[。！？!?；;\n]+/).filter(x => x.replace(/[>*\s#-]/g, '').length >= 4).length;
const nums = t => (t.match(/\d+(?:\.\d+)?/g) || []).length;
export const HARD = {
  // a timeline needs three or more distinct dates, each carrying its own event
  // ...and each date opens its own clause or item, so the dates order the events rather than decorate them
  timeline: t => new Set([...t.matchAll(/(?:^|[\n；;。，,])\s*(?:[-*]|\d+[.)])?\s*\**\s*((?:1[5-9]|20)\d{2})(?=\s*年|-\d{2}|\s*[–-]|\s*[)）:：])/g)].map(m => m[1])).size >= 3,
  gantt: t => /\d+\s*(天|周|个?月|小时|days?|weeks?)/.test(t),
  // a pie shows shares of one whole: three or more single percentages (not ranges) adding up to about 100
  pie: t => { const v = [...t.matchAll(/(?<![\d.–~-])(\d+(?:\.\d+)?)\s*%(?!\s*[–~-])/g)].map(m => +m[1]); const sum = v.reduce((a, b) => a + b, 0); return v.length >= 3 && sum >= 90 && sum <= 110; },
  radar: t => nums(t) >= 6,
  sankey: t => nums(t) >= 3, bar: t => sameUnit(t) >= 3,
  // a line needs at least three points on a time axis written out in the text
  line: t => new Set(t.match(/(1[5-9]|20)\d{2}\s*年?|\d{1,2}\s*月|第\s*\d+\s*(天|周|月|轮|季度?)|Q[1-4]\b|\b\d{1,2}:\d{2}\b|周[一二三四五六日]|(day|week|month)\s*\d+/gi) || []).size >= 3, quadrant: t => true,
  packet: t => /\d+\s*(位|字节|bits?|bytes?)/i.test(t),
  // a parameter sweep says how far it moves: "越 X 越 Y" or "从 A 调到 B" with the numbers
  // a slider shows one parameter's effect; a list of several actions is not one parameter
  slider: t => !listShaped(t) && /(越.{1,8}越|从\s*\S+\s*(调|升|降|涨|增|减)到|the (larger|higher|more|smaller|lower)|as .{1,20} (increases|grows|shrinks))/i.test(t) && nums(t) >= 2,
  // alternatives are named as such: 方案 A / 可以选 X，也可以选 Y / option
  // tabs need two or more named alternatives, not one mention of the word 方案
  tabs: t => /(方案|选项|做法|路线|option|plan)\s*[A-DＡ-Ｄ一二三1-3①-③]|可以选.{1,30}也可以|二选一|either\b.{1,40}\bor\b/i.test(t) || (t.match(/(方案|选项|做法|路线|option|alternative|approach)/gi) || []).length >= 2,
  // a list whose branches stay inside its own items is still a list: draw a flow only when items jump or loop
  // ...and a flow has three or more nodes: one sentence with one condition is a sentence
  // in prose the order must be written: arrows or ordering / branching words
  flowchart: t => listShaped(t) ? crossRef(t) && units(t) >= 3 : (t.match(/→|->|⟶|先|再|然后|接着|随后|最后|才|就|则|如果|若|否则|一旦|是否|失败时|成功后|之后|then|if\b|otherwise/gi) || []).length >= 3,
  swimlane: t => !listShaped(t) || crossRef(t),
  stateDiagram: t => !listShaped(t) || crossRef(t),
  // a checklist is ticked in any order, and a ranked list ("按优先级") orders by importance, not by time
  // steps need three or more actions written in order: a list, or ordering words in prose
  steps: t => !/^\s*[-*]\s*\[[ xX]\]/m.test(t) && !/(按|依)?优先级[)）]?\s*[:：]|按重要性|Top\s*\d/i.test(t) && ((t.match(/^\s*([-*]|\d+[.)])\s/gm) || []).length >= 3 || (t.match(/(先|再|然后|接着|随后|最后|第[一二三四五六]步|first|then|next|finally)/gi) || []).length >= 2 || /分\s*[\d一二三四五六七八九十]+\s*步/.test(t)),
  // a sequence diagram needs three or more messages passed between parties, written as arrows or exchange verbs
  sequenceDiagram: t => (t.match(/→|->|⟶|发(?![生现展布表明挥])|回(?=\s*[A-Za-z])|发送|发给|发出|回复|回传|返回|请求|响应|应答|reply|send|request|respond/gi) || []).length >= 3,
  // code is code: a fenced block or two or more lines of statements, not a command named inline
  code: t => /```/.test(t) || (!listShaped(t) && /\b(npm|pnpm|yarn|pip3?|git|docker|curl|node|python3?|cargo|go)\s+[\w-]|&&|\b[A-Z_]{3,}=\S/.test(t)) || t.split('\n').filter(l => /^\s*[\w.\[\]]+\s*(=|\(|\{)|;\s*$|^\s*(def|function|import|from|class|return|const|let|var)\b/.test(l) && !/^\s*([-*]|\d+[.)])\s/.test(l)).length >= 2 || /^\s*[\w.]+\s*=\s*.*("""|'''|\(\s*$)/m.test(t),
  // a mindmap shows a hierarchy: two or more parts that each have their own sub-points
  mindmap: t => branchingParents(t) >= 2,
  treemap: t => branchingParents(t) >= 1 && sameUnit(t) >= 3,
  // a journey needs three or more stages, each with how the person feels
  journey: t => new Set(t.match(/(兴奋|烦躁|焦虑|开心|高兴|不错|烦|放松|失望|满意|沮丧|紧张|期待|愉快|生气|困惑|舒服|难受|惊喜|担心|安心|无聊|frustrat\w*|happy|anxious|relieved|annoyed|delighted)/gi) || []).size >= 3,
  // a callout is a caution the text itself flags (⚠️, 注意：, 切勿…); a list of caveats is a list
  callout: t => /(⚠️|❗|(^|\n)\s*>?\s*\**\s*(注意|重要|警告|风险提示|小心|warning|caution|important)\**\s*[:：]|^\s*>?\s*\**callout\b|绝对不要|切勿|务必)/i.test(t),
  kanban: t => new Set(t.match(/(待办|进行中|已完成|阻塞|待验收|todo|doing|done|in progress|backlog)/gi) || []).size >= 2,
  // forms bound to a domain vocabulary: the text must use that vocabulary
  // a requirement diagram needs numbered requirements or binding wording, not just the word 需求
  requirement: t => /(REQ-\d|\bR\d+\b|requirement|shall\b)/i.test(t) || (/(需求|验收)/.test(t) && (t.match(/(必须|应当|不得|须)/g) || []).length >= 2),
  railroad: t => /(语法|文法|BNF|正则|产生式|开头|后面跟|分隔|可以是|syntax|grammar|token)/i.test(t),
  // use cases: the vocabulary, or two or more clauses that each open with a role and what it can do
  usecase: t => /(用例|权限|use case|actor|permission)/i.test(t) || (t.match(/(?:^|[；;，,。：:])\s*[^，。；;：:\s]{1,10}?(只能|可以|能|还能|\bcan\b)/g) || []).length >= 2,
  c4: t => /(外部|第三方|C4|系统上下文|external|third-party)/i.test(t),
  // a fishbone groups causes under named categories
  ishikawa: t => /(原因|导致|为什么|根因|cause|because)/i.test(t) && (branchingParents(t) >= 2 || t.split(/[；;]/).filter(x => x.trim()).length >= 3),
  eventmodeling: t => /(事件|命令|event|command)/i.test(t),
  wardley: t => /(演进|成熟度|商品化|定制|Wardley|commodit|evolution)/i.test(t),
  cynefin: t => /(Cynefin|混沌|繁杂|复杂域|清晰域|可预测|chaotic|complicated)/i.test(t),
  erDiagram: t => /(表|字段|主键|外键|实体|table|column|entity|primary key)/i.test(t),
  classDiagram: t => /(类|方法|属性|接口|继承|class|method|interface|inherit)/i.test(t),
  gitGraph: t => /(git|分支|合并|branch|merge|commit)/i.test(t),
};
// A generic form drawing the same content as a more specific primary is redundant.
const GENERIC = { flowchart: 'process', steps: 'process', table: 'compare', tabs: 'compare', bar: 'numbers', mindmap: 'parts' };
const COVERS = {
  process: ['swimlane','sequenceDiagram','stateDiagram','agentflow','gantt','gitGraph','timeline','journey','eventmodeling','requirement','erDiagram','classDiagram','block','c4','usecase','architecture','wardley','packet','code'],
  compare: ['radar','quadrant','sankey','venn','cynefin','slider','bar','pie'],
  numbers: ['pie','treemap','radar','sankey','line','gantt','packet'],
  parts: ['treemap','ishikawa','treeView','table','tabs'],
};
// Three or more list items that each carry two or more values under the same attribute labels
// ("- A：价格 3，耗时 5" / "- B：价格 4，耗时 2"): the text already has a grid's shape. Sentences in a list
// rarely start their clauses with the same words, so a repeated label is the tell.
export function gridShape(t, { whole = true } = {}) {
  const items = (t.match(/^\s*([-*]|\d+[.)])\s+.+$/gm) || []).map(l => new Set([...l.matchAll(/[：:，,]\s*([^\s，,：:；;]{1,24})\s/g)].map(m => m[1])));
  if (items.length < 2) return false;
  // a table rewritten as a list ("- 行名：列 A 值，列 B 值") repeats the same column words across its rows;
  // grid = 3+ rows sharing 2+ column words, or 2 rows sharing 3+
  const count = new Map(); items.forEach(s => s.forEach(k => count.set(k, (count.get(k) || 0) + 1)));
  const cols = [...count].filter(([, v]) => v >= 2).sort((x, y) => y[1] - x[1]).map(([k]) => k);
  for (let c = Math.min(cols.length, 6); c >= 2; c--) {
    const rows = items.filter(s => cols.slice(0, c).every(k => s.has(k))).length;
    // ...and those rows are most of the list: a small grid inside a longer section does not make the block a table
    if (((rows >= 3 && c >= 2) || (rows >= 2 && c >= 3)) && (!whole || rows >= items.length * 0.6)) return true;
  }
  return false;
}

// A comparison written in a sentence: three or more items split by "；", each giving two or more attributes.
export const proseGrid = t => { const segs = t.split(/[；;]/).map(x => x.trim()).filter(Boolean); return segs.length >= 3 && segs.every(x => (x.match(/[、，,]/g) || []).length >= 1); };
export function decide(s, text = '') {
  s = { ...s, __list: listShaped(text), __grid: gridShape(text) || proseGrid(text), __arrows: (text.match(/→|->|⟶/g) || []).length };
  let cands = PRIORITY.filter(c => RULES[c](s) && (!HARD[c] || HARD[c](text)));
  // the grid shape is lexical; it leads only when JEV also reads the items as compared side by side
  // a grid that is most of the list leads; a grid inside a longer section leads only when JEV reads the block as comparing items
  if (gridShape(text) || (gridShape(text, { whole: false }) && s.items_attrs >= 0.85)) cands = ['table', ...cands.filter(c => c !== 'table')];
  // a block that is itself code is shown as code: redrawing a program as a flowchart hides the code it is
  const lines = text.split('\n').filter(l => l.trim());
  if (cands.includes('code') && lines.length >= 2 && lines.filter(l => /^\s*[\w.\[\]]+\s*(=|\(|\{)|[:;{]\s*$|^\s*(#|\/\/|def|for|if|else|elif|while|return|import|from|class|const|let|var|function)\b/.test(l) && !/^\s*([-*]|\d+[.)])\s/.test(l)).length >= lines.length * 0.6) cands = ['code', ...cands.filter(c => c !== 'code')];
  const primary = cands[0] || 'prose';
  cands = cands.filter(c => c === primary || !GENERIC[c] || !COVERS[GENERIC[c]].includes(primary));
  return { primary, cands };
}

// Where each component renders: the family and diagram type the scaffold and derivers understand.
const FORM = { table: ['table', null], tabs: ['tabs', null], slider: ['slider', null], steps: ['steps', 'numbered'], callout: ['prose', null], code: ['prose', null] };
export function formOf(name, TYPES, s = {}) {
  if (FORM[name]) return FORM[name];
  if (name === 'flowchart') return [Y(s, 'steps') ? 'steps' : 'structure', 'flowchart'];
  for (const [fam, types] of Object.entries(TYPES)) if (types[name]) return [fam, name];
  return ['prose', null];
}
