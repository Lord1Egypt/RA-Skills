const TRIGRAMS = {
  "111": { name: "乾", symbol: "☰", nature: "天", image: "健", counsel: "主动、开创、守正，不以强势替代判断。" },
  "110": { name: "兑", symbol: "☱", nature: "澤", image: "悦", counsel: "沟通、交换、悦纳，但承诺要有边界。" },
  "101": { name: "离", symbol: "☲", nature: "火", image: "丽", counsel: "看见事实，辨明依附关系，不被表象带走。" },
  "100": { name: "震", symbol: "☳", nature: "雷", image: "动", counsel: "启动、警醒，先稳住第一步。" },
  "011": { name: "巽", symbol: "☴", nature: "風", image: "入", counsel: "渐入、顺势，用连续的小动作推进。" },
  "010": { name: "坎", symbol: "☵", nature: "水", image: "险", counsel: "面对风险，先建承载与退路。" },
  "001": { name: "艮", symbol: "☶", nature: "山", image: "止", counsel: "止步、界限，在停顿中重新定位。" },
  "000": { name: "坤", symbol: "☷", nature: "地", image: "顺", counsel: "承接、养成，以耐心和秩序承载变化。" }
};

// Key is lower trigram | upper trigram, because lines are stored from bottom to top.
const HEXAGRAM_LOOKUP = {
  "乾|乾": 1, "乾|兑": 43, "乾|离": 14, "乾|震": 34, "乾|巽": 9, "乾|坎": 5, "乾|艮": 26, "乾|坤": 11,
  "兑|乾": 10, "兑|兑": 58, "兑|离": 38, "兑|震": 54, "兑|巽": 61, "兑|坎": 60, "兑|艮": 41, "兑|坤": 19,
  "离|乾": 13, "离|兑": 49, "离|离": 30, "离|震": 55, "离|巽": 37, "离|坎": 63, "离|艮": 22, "离|坤": 36,
  "震|乾": 25, "震|兑": 17, "震|离": 21, "震|震": 51, "震|巽": 42, "震|坎": 3, "震|艮": 27, "震|坤": 24,
  "巽|乾": 44, "巽|兑": 28, "巽|离": 50, "巽|震": 32, "巽|巽": 57, "巽|坎": 48, "巽|艮": 18, "巽|坤": 46,
  "坎|乾": 6, "坎|兑": 47, "坎|离": 64, "坎|震": 40, "坎|巽": 59, "坎|坎": 29, "坎|艮": 4, "坎|坤": 7,
  "艮|乾": 33, "艮|兑": 31, "艮|离": 56, "艮|震": 62, "艮|巽": 53, "艮|坎": 39, "艮|艮": 52, "艮|坤": 15,
  "坤|乾": 12, "坤|兑": 45, "坤|离": 35, "坤|震": 16, "坤|巽": 20, "坤|坎": 8, "坤|艮": 23, "坤|坤": 2
};

const LINE_POSITIONS = ["初爻", "二爻", "三爻", "四爻", "五爻", "上爻"];
const JOURNAL_KEY = "zhouyi-benjing-journal-v1";

const LINE_GUIDANCE = [
  "事在初起，宜先试探根基，不急于定局。",
  "渐入关系或结构，重在取得中位的支撑。",
  "内外交界，最容易躁进，宜复核风险。",
  "开始外显，适合调整表达、位置与策略。",
  "居于核心，重在正当性、责任和判断。",
  "一事将极，宜收束、转化，不恋旧势。"
];

const QUESTION_GUIDANCE = {
  relationship: "感情与关系之问，重点看互信、位置是否相称，以及是否有可持续的回应。",
  work: "事业与项目之问，重点看时机、角色、资源和下一步是否可验证。",
  money: "财务之问，重点先分清事实、假设与欲望；重大投入必须保留缓冲和退出条件。",
  wellbeing: "身心之问，卦象只能提示节奏和边界；涉及疾病、持续痛苦或风险时，应优先求助专业人士。",
  timing: "时机之问，重点看动爻多少、变卦方向，以及当下是否宜动、宜守或宜缓。",
  general: "一般问题，先把卦象当成镜子：找出你真正能负责的一步，再观察现实反馈。"
};

const state = {
  method: "coin",
  currentReading: null,
  catalogGrade: "all"
};

const els = {
  question: document.querySelector("#question"),
  castButton: document.querySelector("#castButton"),
  modeButtons: document.querySelectorAll(".mode-button"),
  resultLayout: document.querySelector("#resultLayout"),
  detailGrid: document.querySelector("#detailGrid"),
  primaryHexagram: document.querySelector("#primaryHexagram"),
  changedHexagram: document.querySelector("#changedHexagram"),
  primaryTitle: document.querySelector("#primaryTitle"),
  changedTitle: document.querySelector("#changedTitle"),
  primaryTrigrams: document.querySelector("#primaryTrigrams"),
  changedTrigrams: document.querySelector("#changedTrigrams"),
  changedBlock: document.querySelector("#changedBlock"),
  changeArrow: document.querySelector("#changeArrow"),
  readingText: document.querySelector("#readingText"),
  lineList: document.querySelector("#lineList"),
  symbolList: document.querySelector("#symbolList"),
  journalList: document.querySelector("#journalList"),
  copyButton: document.querySelector("#copyButton"),
  clearJournalButton: document.querySelector("#clearJournalButton"),
  catalogSearch: document.querySelector("#catalogSearch"),
  catalogFilters: document.querySelector("#catalogFilters"),
  catalogGrid: document.querySelector("#catalogGrid"),
  hexagramSearch: document.querySelector("#hexagramSearch"),
  hexagramLibrary: document.querySelector("#hexagramLibrary")
};

function tossLine(method) {
  if (method === "yarrow") {
    return createLine(weightedPick([
      { value: 6, weight: 1 },
      { value: 7, weight: 5 },
      { value: 8, weight: 7 },
      { value: 9, weight: 3 }
    ]));
  }

  const coins = Array.from({ length: 3 }, () => (Math.random() < 0.5 ? 2 : 3));
  return createLine(coins.reduce((sum, coin) => sum + coin, 0), coins);
}

function weightedPick(items) {
  const total = items.reduce((sum, item) => sum + item.weight, 0);
  let cursor = Math.random() * total;
  for (const item of items) {
    cursor -= item.weight;
    if (cursor < 0) return item.value;
  }
  return items[items.length - 1].value;
}

function createLine(value, coins = []) {
  return {
    value,
    coins,
    yang: value === 7 || value === 9,
    moving: value === 6 || value === 9,
    label: value === 6 ? "老阴" : value === 7 ? "少阳" : value === 8 ? "少阴" : "老阳"
  };
}

function castHexagram() {
  const lines = Array.from({ length: 6 }, () => tossLine(state.method));
  const changedLines = lines.map((line) => ({
    ...line,
    yang: line.moving ? !line.yang : line.yang,
    moving: false
  }));

  return enrichReading({
    id: createId(),
    createdAt: new Date().toISOString(),
    question: els.question.value.trim(),
    method: state.method,
    lines,
    changedLines
  });
}

function enrichReading(reading) {
  const primary = resolveHexagram(reading.lines);
  const changed = resolveHexagram(reading.changedLines);
  const moving = reading.lines
    .map((line, index) => ({ line, index }))
    .filter(({ line }) => line.moving);

  return {
    ...reading,
    primary,
    changed,
    moving,
    decision: decideTextSource(primary, changed, moving)
  };
}

function createId() {
  if (window.crypto?.randomUUID) return window.crypto.randomUUID();
  return `reading-${Date.now()}-${Math.random().toString(16).slice(2)}`;
}

function resolveHexagram(lines) {
  const lowerBits = lines.slice(0, 3).map((line) => (line.yang ? "1" : "0")).join("");
  const upperBits = lines.slice(3, 6).map((line) => (line.yang ? "1" : "0")).join("");
  const lower = TRIGRAMS[lowerBits];
  const upper = TRIGRAMS[upperBits];
  const number = HEXAGRAM_LOOKUP[`${lower.name}|${upper.name}`];
  const benjing = ZHOUYI_BENJING[number - 1];

  return {
    number,
    name: benjing.name,
    fullName: fullHexagramName(benjing.name, upper, lower),
    judgment: benjing.judgment,
    lines: benjing.lines,
    extras: benjing.extras,
    lower,
    upper
  };
}

function fullHexagramName(name, upper, lower) {
  if (upper.name === lower.name && sameTrigramName(name, upper.name)) return `${name}為${upper.nature}`;
  return `${upper.nature}${lower.nature}${name}`;
}

function sameTrigramName(sourceName, trigramName) {
  const aliases = { 兑: "兌", 离: "離" };
  return sourceName === trigramName || sourceName === aliases[trigramName];
}

function decideTextSource(primary, changed, moving) {
  const count = moving.length;

  if (count === 0) {
    return {
      rule: "六爻不变：以本卦卦辞为主。",
      focus: "本卦卦辞",
      entries: [{ title: `${primary.name}卦辞`, text: primary.judgment, priority: true }]
    };
  }

  if (count === 1) {
    const item = moving[0];
    return {
      rule: "一爻变：以该动爻爻辞为主。",
      focus: primary.lines[item.index].label,
      entries: [lineEntry(primary, item.index, true)]
    };
  }

  if (count === 2) {
    const indexes = moving.map(({ index }) => index).sort((a, b) => a - b);
    const upperIndex = indexes[indexes.length - 1];
    return {
      rule: "二爻变：取两条动爻爻辞，以上爻为主。",
      focus: primary.lines[upperIndex].label,
      entries: indexes.map((index) => lineEntry(primary, index, index === upperIndex))
    };
  }

  if (count === 3) {
    return {
      rule: "三爻变：以本卦卦辞与变卦卦辞合看。",
      focus: "本卦与变卦卦辞",
      entries: [
        { title: `${primary.name}卦辞`, text: primary.judgment, priority: true },
        { title: `${changed.name}卦辞`, text: changed.judgment, priority: false }
      ]
    };
  }

  if (count === 4) {
    const staticIndexes = [0, 1, 2, 3, 4, 5].filter((index) => !moving.some((item) => item.index === index));
    const lowerIndex = staticIndexes[0];
    return {
      rule: "四爻变：取两条静爻爻辞，以下爻为主。",
      focus: primary.lines[lowerIndex].label,
      entries: staticIndexes.map((index) => lineEntry(primary, index, index === lowerIndex))
    };
  }

  if (count === 5) {
    const staticIndex = [0, 1, 2, 3, 4, 5].find((index) => !moving.some((item) => item.index === index));
    return {
      rule: "五爻变：取变卦中唯一静爻所对应的爻辞。",
      focus: changed.lines[staticIndex].label,
      entries: [lineEntry(changed, staticIndex, true)]
    };
  }

  const special = primary.number === 1 ? primary.extras.find((item) => item.label === "用九")
    : primary.number === 2 ? primary.extras.find((item) => item.label === "用六")
      : null;

  if (special) {
    return {
      rule: "六爻皆变：乾用用九，坤用用六。",
      focus: special.label,
      entries: [{ title: special.label, text: special.text, priority: true }]
    };
  }

  return {
    rule: "六爻皆变：乾坤之外，以变卦卦辞为主。",
    focus: `${changed.name}卦辞`,
    entries: [{ title: `${changed.name}卦辞`, text: changed.judgment, priority: true }]
  };
}

function lineEntry(hexagram, index, priority) {
  const source = hexagram.lines[index];
  return {
    title: `${hexagram.name}${source.label}`,
    text: source.text,
    priority
  };
}

function renderReading(reading) {
  state.currentReading = reading;
  els.resultLayout.hidden = false;
  els.detailGrid.hidden = false;

  renderHexagram(els.primaryHexagram, reading.lines);
  renderHexagram(els.changedHexagram, reading.changedLines);

  const hasMoving = reading.moving.length > 0;
  els.changedBlock.style.opacity = hasMoving ? "1" : "0.45";
  els.changeArrow.textContent = hasMoving ? "→" : "•";

  els.primaryTitle.textContent = `${reading.primary.number}. ${reading.primary.fullName}`;
  els.changedTitle.textContent = hasMoving ? `${reading.changed.number}. ${reading.changed.fullName}` : "无变卦";
  els.primaryTrigrams.textContent = trigramText(reading.primary);
  els.changedTrigrams.textContent = hasMoving ? trigramText(reading.changed) : "六爻皆静，重在本卦卦辞。";

  els.readingText.innerHTML = buildReadingSections(reading);
  els.lineList.innerHTML = buildLineList(reading);
  els.symbolList.innerHTML = buildSymbolList(reading);

  saveJournal(reading);
  renderJournal();
  els.resultLayout.scrollIntoView({ behavior: "smooth", block: "start" });
}

function renderHexagram(container, lines) {
  container.innerHTML = "";
  [...lines].reverse().forEach((line) => {
    const div = document.createElement("div");
    div.className = `yao ${line.yang ? "yang" : "yin"} ${line.moving ? "moving" : ""}`;
    div.setAttribute("aria-label", `${line.label}${line.moving ? "，动爻" : ""}`);
    if (line.moving) {
      const dot = document.createElement("span");
      dot.className = "move-dot";
      div.appendChild(dot);
    }
    container.appendChild(div);
  });
}

function trigramText(hexagram) {
  return `上${hexagram.upper.name}${hexagram.upper.symbol}${hexagram.upper.nature} · 下${hexagram.lower.name}${hexagram.lower.symbol}${hexagram.lower.nature}`;
}

function buildReadingSections(reading) {
  const questionType = classifyQuestion(reading.question);
  const question = reading.question || "未写下具体问题";
  const entries = reading.decision.entries
    .map((entry) => `<blockquote class="${entry.priority ? "primary-source" : ""}"><strong>${escapeHtml(entry.title)}</strong>${escapeHtml(entry.text)}</blockquote>`)
    .join("");

  return `
    <section>
      <h3>所问</h3>
      <p>${escapeHtml(question)}</p>
    </section>
    <section>
      <h3>卦辞</h3>
      <blockquote><strong>${escapeHtml(reading.primary.name)}卦辞</strong>${escapeHtml(reading.primary.judgment)}</blockquote>
      ${reading.moving.length ? `<p>变卦为「${escapeHtml(reading.changed.fullName)}」，其卦辞为：${escapeHtml(reading.changed.judgment)}</p>` : ""}
    </section>
    <section>
      <h3>取辞</h3>
      <p><span class="rule-badge">${reading.moving.length} 动爻</span>${escapeHtml(reading.decision.rule)} 本次重点：${escapeHtml(reading.decision.focus)}。</p>
      <div class="source-stack">${entries}</div>
    </section>
    <section>
      <h3>解读</h3>
      <p>${buildInterpretation(reading, questionType)}</p>
    </section>
    <section>
      <h3>体系路由</h3>
      <p>${buildRouteNote(reading, questionType)}</p>
    </section>
    <section>
      <h3>行动</h3>
      <p>${buildActionAdvice(reading, questionType)}</p>
    </section>
    <section>
      <h3>追问</h3>
      <p>${buildReflectionQuestion(reading, questionType)}</p>
    </section>
  `;
}

function buildRouteNote(reading, questionType) {
  const enabled = DIVINATION_SYSTEMS.find((item) => item.id === "zhouyi-benjing");
  const related = recommendSystems(questionType)
    .map((id) => DIVINATION_SYSTEMS.find((item) => item.id === id))
    .filter(Boolean);
  const names = related.map((item) => `${item.name}（${item.status}，${item.grade}级）`).join("；");
  return `本次采用 ${enabled.name}（${enabled.grade}级，${enabled.status}）作为主体系，因为它能直接引用本经并按动爻取辞。可参考的旁支体系：${names || "暂无"}。旁支只作百科线索，不参与本次断语。`;
}

function recommendSystems(questionType) {
  const map = {
    relationship: ["liuyao", "meihua", "ziwei", "tarot"],
    work: ["meihua", "liuyao", "qimen", "bazi"],
    money: ["liuyao", "qimen", "bazi"],
    wellbeing: ["meihua", "fengshui", "bazi"],
    timing: ["qimen", "liuyao", "meihua"],
    general: ["meihua", "liuyao", "routing"]
  };
  return map[questionType] || map.general;
}

function buildInterpretation(reading, questionType) {
  const movement = reading.moving.length === 0
    ? "此卦无动爻，说明问题的关键不在立刻改变，而在看清本卦所呈现的结构。"
    : reading.moving.length >= 4
      ? "动爻很多，表示局面已经接近整体翻转，判断时要少抓单点，多看变卦给出的方向。"
      : "有动爻，说明现状中已经出现转折点；爻位提示变化发生的层次。";

  const lineLayer = reading.moving.length
    ? reading.moving.map(({ index }) => `${LINE_POSITIONS[index]}：${LINE_GUIDANCE[index]}`).join(" ")
    : "六爻皆静，以本卦卦辞为主，不宜把问题解释成马上会变。";

  return `${movement}${lineLayer}${QUESTION_GUIDANCE[questionType]} 本系统只以《周易》本经卦辞、爻辞为底，不把结果说成确定命令。`;
}

function buildActionAdvice(reading, questionType) {
  const count = reading.moving.length;
  const typeAdvice = {
    relationship: "先校正关系中的位置与边界，再谈推进；如果对方回应不稳定，不要用催促替代确认。",
    work: "把下一步拆成可验证的小行动，先确认角色、资源、时间表，再扩大承诺。",
    money: "不要只看收益叙事，先列出最大损失、退出条件和等待成本。",
    wellbeing: "先恢复秩序和支持系统；若涉及疾病或持续痛苦，请优先找专业帮助。",
    timing: "若动爻少，先抓关键动作；若动爻多，缩短承诺周期，等待新局面落定。",
    general: "把卦象落回现实：今天能负责的一步是什么，做完后用什么信号复盘。"
  };

  const rhythm = count === 0
    ? "宜守中观察，少做剧烈转向。"
    : count <= 2
      ? "宜抓住一个关键点，小步推进。"
      : count === 3
        ? "宜同时看现状与去向，先做过渡安排。"
        : "宜降低赌注，给变化留出缓冲。";

  return `${rhythm}${typeAdvice[questionType]}`;
}

function buildReflectionQuestion(reading, questionType) {
  const base = {
    relationship: "这段关系里，我真正能负责的是表达、边界，还是等待？",
    work: "如果只推进一步，哪一步最能验证这件事值得继续？",
    money: "我现在看到的是价值、价格，还是被波动放大的欲望与恐惧？",
    wellbeing: "我最需要先恢复的是体力、秩序、支持，还是边界？",
    timing: "我是在等合适时机，还是在用等待回避行动？",
    general: "这件事里，我真正能负责的部分是什么？"
  };
  return `${base[questionType]}以「${reading.primary.fullName}」为镜，再看「${reading.changed.fullName}」是否指出下一阶段。`;
}

function buildLineList(reading) {
  return reading.lines
    .map((line, index) => {
      const source = reading.primary.lines[index];
      const selected = reading.decision.entries.some((entry) => entry.title === `${reading.primary.name}${source.label}`);
      const coinText = line.coins.length ? `三钱：${line.coins.join(" + ")} = ${line.value}` : `蓍草概率数：${line.value}`;
      return `
        <div class="line-item ${line.moving ? "moving" : ""} ${selected ? "selected" : ""}">
          <strong>${source.label} · ${line.label}${line.moving ? " · 动" : ""}</strong>
          <p>${coinText}</p>
          <p class="source-text">${escapeHtml(source.text)}</p>
        </div>
      `;
    })
    .reverse()
    .join("");
}

function buildSymbolList(reading) {
  const items = [
    {
      title: "本经底座",
      text: "本页数据由 sources/zhouyi/zhouyi_benjing.txt 生成，仅含六十四卦卦辞、爻辞、用九、用六。"
    },
    {
      title: `上卦 ${reading.primary.upper.name}${reading.primary.upper.symbol}`,
      text: `${reading.primary.upper.nature}象为${reading.primary.upper.image}：${reading.primary.upper.counsel}`
    },
    {
      title: `下卦 ${reading.primary.lower.name}${reading.primary.lower.symbol}`,
      text: `${reading.primary.lower.nature}象为${reading.primary.lower.image}：${reading.primary.lower.counsel}`
    },
    {
      title: "取辞规则",
      text: reading.decision.rule
    }
  ];

  if (reading.moving.length) {
    items.push({
      title: `变化 ${reading.changed.fullName}`,
      text: `由 ${reading.primary.fullName} 变为 ${reading.changed.fullName}，解释时先按动爻数量取辞，再参考变卦方向。`
    });
  }

  return items
    .map(
      (item) => `
        <div class="symbol-item">
          <strong>${escapeHtml(item.title)}</strong>
          <p>${escapeHtml(item.text)}</p>
        </div>
      `
    )
    .join("");
}

function renderCatalog() {
  if (!els.catalogGrid) return;
  const query = normalize(els.catalogSearch?.value || "");
  const systems = DIVINATION_SYSTEMS.filter((item) => {
    const gradeOk = state.catalogGrade === "all" || item.grade === state.catalogGrade;
    const haystack = normalize([
      item.name,
      item.family,
      item.grade,
      item.status,
      item.basis,
      item.capability,
      item.guardrail,
      item.bestFor.join(" "),
      item.inputs.join(" ")
    ].join(" "));
    return gradeOk && (!query || haystack.includes(query));
  });

  els.catalogGrid.innerHTML = systems.map(renderSystemCard).join("") ||
    `<div class="system-card"><p>没有匹配的体系。</p></div>`;
}

function renderSystemCard(item) {
  return `
    <article class="system-card">
      <header>
        <div>
          <h3>${escapeHtml(item.name)}</h3>
          <p>${escapeHtml(item.family)} · ${escapeHtml(item.basis)}</p>
        </div>
        <span class="grade-badge grade-${item.grade.toLowerCase()}">${item.grade}</span>
      </header>
      <span class="status-badge">${escapeHtml(item.status)}</span>
      <p>${escapeHtml(item.capability)}</p>
      <div class="tag-list">${item.bestFor.slice(0, 4).map((tag) => `<span>${escapeHtml(tag)}</span>`).join("")}</div>
      <p><strong>资料：</strong>${escapeHtml(item.inputs.join("、"))}</p>
      <p><strong>边界：</strong>${escapeHtml(item.guardrail)}</p>
    </article>
  `;
}

function renderHexagramLibrary() {
  if (!els.hexagramLibrary) return;
  const query = normalize(els.hexagramSearch?.value || "");
  const items = ZHOUYI_BENJING.filter((hex) => {
    const haystack = normalize([
      hex.number,
      hex.name,
      hex.judgment,
      hex.lines.map((line) => `${line.label}${line.text}`).join(" "),
      hex.extras.map((line) => `${line.label}${line.text}`).join(" ")
    ].join(" "));
    return !query || haystack.includes(query);
  });

  els.hexagramLibrary.innerHTML = items.map(renderHexCard).join("") ||
    `<div class="hex-card"><p>没有匹配的卦。</p></div>`;
}

function renderHexCard(hex) {
  const firstMovingLine = hex.lines.find((line) => /吉|凶|悔|咎|厲|利/.test(line.text)) || hex.lines[0];
  return `
    <article class="hex-card">
      <header>
        <h3>${hex.number}. ${escapeHtml(hex.name)}</h3>
        <span class="grade-badge grade-s">本经</span>
      </header>
      <p class="source-line">${escapeHtml(hex.name)}：${escapeHtml(hex.judgment)}</p>
      <p>${escapeHtml(firstMovingLine.label)}：${escapeHtml(firstMovingLine.text)}</p>
    </article>
  `;
}

function normalize(value) {
  return String(value).toLowerCase().replace(/\s+/g, "");
}

function classifyQuestion(question) {
  const q = question.toLowerCase();
  if (/感情|关系|恋|婚|伴侣|喜欢|复合|分手/.test(q)) return "relationship";
  if (/工作|事业|合作|项目|公司|创业|offer|职位|老板|面试|跳槽/.test(q)) return "work";
  if (/钱|投资|买|卖|收入|财|价格|交易|理财|资产/.test(q)) return "money";
  if (/健康|身体|病|睡眠|焦虑|压力|治疗|医院/.test(q)) return "wellbeing";
  if (/何时|什么时候|时机|现在适合|是否适合|能不能|该不该/.test(q)) return "timing";
  return "general";
}

function methodText(method) {
  if (method === "yarrow") return "蓍草概率";
  return "三枚铜钱";
}

function saveJournal(reading) {
  const journal = getJournal().filter((item) => item.id !== reading.id);
  journal.unshift({
    id: reading.id,
    createdAt: reading.createdAt,
    question: reading.question,
    method: reading.method,
    lines: reading.lines,
    changedLines: reading.changedLines
  });
  localStorage.setItem(JOURNAL_KEY, JSON.stringify(journal.slice(0, 8)));
}

function getJournal() {
  try {
    return JSON.parse(localStorage.getItem(JOURNAL_KEY) || "[]");
  } catch {
    return [];
  }
}

function renderJournal() {
  const journal = getJournal();
  if (!journal.length) {
    els.journalList.innerHTML = `<div class="journal-item"><p>暂无记录</p></div>`;
    return;
  }

  els.journalList.innerHTML = journal
    .map((item) => {
      const reading = enrichReading(item);
      const date = new Intl.DateTimeFormat("zh-CN", {
        month: "2-digit",
        day: "2-digit",
        hour: "2-digit",
        minute: "2-digit"
      }).format(new Date(item.createdAt));
      return `
        <button class="journal-item" type="button" data-id="${item.id}">
          <strong>${reading.primary.number}. ${escapeHtml(reading.primary.fullName)}</strong>
          <p>${date} · ${methodText(item.method)} · ${escapeHtml(item.question || "未写问题")}</p>
        </button>
      `;
    })
    .join("");
}

function escapeHtml(value = "") {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function plainTextReading() {
  if (!state.currentReading) return "";
  const container = document.createElement("div");
  container.innerHTML = buildReadingSections(state.currentReading);
  return container.innerText.trim();
}

function bootstrap() {
  if (!Array.isArray(window.ZHOUYI_BENJING) || window.ZHOUYI_BENJING.length !== 64) {
    els.readingText.innerHTML = `<section><h3>数据错误</h3><p>未能加载完整《周易》本经数据。</p></section>`;
    return;
  }
  if (!Array.isArray(window.DIVINATION_SYSTEMS) || window.DIVINATION_SYSTEMS.length < 8) {
    els.readingText.innerHTML = `<section><h3>数据错误</h3><p>未能加载完整术数百科数据。</p></section>`;
    return;
  }

  els.modeButtons.forEach((button) => {
    button.addEventListener("click", () => {
      state.method = button.dataset.method;
      els.modeButtons.forEach((item) => item.classList.toggle("active", item === button));
    });
  });

  els.castButton.addEventListener("click", () => {
    renderReading(castHexagram());
  });

  els.copyButton.addEventListener("click", async () => {
    const text = plainTextReading();
    if (!text) return;
    try {
      await navigator.clipboard.writeText(text);
      els.copyButton.textContent = "✓";
    } catch {
      els.copyButton.textContent = "!";
    }
    window.setTimeout(() => {
      els.copyButton.textContent = "⧉";
    }, 1200);
  });

  els.clearJournalButton.addEventListener("click", () => {
    localStorage.removeItem(JOURNAL_KEY);
    renderJournal();
  });

  els.catalogSearch?.addEventListener("input", renderCatalog);
  els.hexagramSearch?.addEventListener("input", renderHexagramLibrary);
  els.catalogFilters?.addEventListener("click", (event) => {
    const button = event.target.closest("[data-grade]");
    if (!button) return;
    state.catalogGrade = button.dataset.grade;
    els.catalogFilters.querySelectorAll(".filter-button").forEach((item) => {
      item.classList.toggle("active", item === button);
    });
    renderCatalog();
  });

  els.journalList.addEventListener("click", (event) => {
    const button = event.target.closest("[data-id]");
    if (!button) return;
    const record = getJournal().find((item) => item.id === button.dataset.id);
    if (record) renderReading(enrichReading(record));
  });

  renderJournal();
  renderCatalog();
  renderHexagramLibrary();
}

bootstrap();
