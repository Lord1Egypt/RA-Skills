// 临时冒烟：用最小 DOM 桩执行 web/index.html 的内联脚本，确认渲染管线不报错。
const fs = require("fs");
const path = require("path");

const html = fs.readFileSync(path.join(__dirname, "..", "web", "index.html"), "utf8");
const m = html.match(/<script>([\s\S]*?)<\/script>/g);
const code = m[m.length - 1].replace(/^<script>/, "").replace(/<\/script>$/, "");

const mockItems = [
  { id: "T-20261002-010", text: "推进 tdx-linker", status: "进行中", importance: "重要",
    urgent: "不紧急", is_urgent: false, note: "", blocker: "晚上刷手机", counter: "拿起手机前先做 10 分钟",
    workspace: "G:\\Projects\\Stock\\tdx\\tdx_warn", docs: [], links: [], tags: ["学习"],
    depends_on: [], parent: "", due: "2026-09-20", created: "2026-10-02 22:11", updated: null,
    from: null, date: "2026-10-02", archived: false, blocked: false,
    overdue_days: 16, due_in_days: -16, stall_days: null, projected_finish: null,
    pin: 0, pin_reason: "Overdue 16 day(s), moved to today" },
  { id: "T-20261002-004", text: "持续维护 vibe-astock", status: "进行中", importance: "不重要",
    urgent: "不紧急", is_urgent: false, note: "", blocker: "", counter: "",
    workspace: "G:\\Projects\\Stock\\vibe-astock", docs: [], links: [], tags: [],
    depends_on: [], parent: "", due: null, created: "2026-10-02 21:31", updated: null,
    from: null, date: "2026-10-02", archived: false, blocked: false,
    overdue_days: null, due_in_days: null, stall_days: 4, projected_finish: null,
    pin: 1, pin_reason: "No progress for 4 day(s), moved to today" },
  { id: "T-20261002-006", text: "收尾 TGDown", status: "结束", importance: "不重要",
    urgent: "不紧急", is_urgent: false, note: "", blocker: "", counter: "", workspace: "",
    docs: [], links: [], tags: [], depends_on: [], parent: "", due: null,
    created: "2026-10-02 21:31", updated: null, from: null, date: "2026-10-02",
    archived: false, blocked: false, overdue_days: null, due_in_days: null,
    stall_days: null, projected_finish: null, pin: null, pin_reason: "" },
];

const els = {};
function makeEl(id) {
  return els[id] || (els[id] = {
    id, innerHTML: "", textContent: "", value: "", style: {},
    classList: { add(){}, remove(){}, toggle(){}, contains(){ return false; } },
    addEventListener(){}, focus(){}, appendChild(){}, querySelector(){ return null; },
    closest(){ return null; }, getAttribute(){ return null; }, setAttribute(){},
    offsetWidth: 160, offsetHeight: 118,
  });
}
// === 悬浮菜单定位用的可控替身（document/window 均为最小实现） ===
const wsWraps = [];
function makeWrap(name, rect, opts) {
  opts = opts || {};
  const wrap = {
    _name: name, _hover: false, _rect: rect,
    getBoundingClientRect() { return this._rect; },
    closest(sel) { return sel === ".ws-wrap" ? this : null; },
    querySelector(sel) { return sel === ".ws-menu" ? menu : null; },
    getAttribute() { return null; },
  };
  const menu = {
    _wrap: wrap, _path: opts.path || ("D:\\proj\\" + name),
    offsetWidth: opts.w == null ? 160 : opts.w,
    offsetHeight: opts.h == null ? 118 : opts.h,
    style: { left: "-9999px", top: "-9999px" },
    dataset: {},
    _contains: [],
    // 命中 :before 桥接带时事件目标就是菜单本身
    contains(n) { return n === this || this._contains.indexOf(n) >= 0; },
    getAttribute(sel) { return sel === "data-path" ? this._path : null; },
    classList: { _s: new Set(), add(c) { this._s.add(c); }, remove(c) { this._s.delete(c); },
                 contains(c) { return this._s.has(c); } },
    closest(sel) { return sel === ".ws-wrap" ? wrap : null; },
  };
  // 路径文本节点：hover 链的下端
  const ws = { closest(sel) { return sel === ".ws-wrap" ? wrap : null; }, getAttribute() { return null; } };
  wrap._menu = menu; wrap._ws = ws;
  wsWraps.push(wrap);
  return wrap;
}
// 菜单项节点：closest(".ws-item") 命中自己，closest(".ws-menu") 命中所属菜单
function makeWsItem(menu, act) {
  const item = {
    getAttribute(sel) { return sel === "data-ws-act" ? act : null; },
    closest(sel) {
      if (sel === ".ws-item") return item;
      if (sel === ".ws-menu") return menu;
      return null;
    },
  };
  menu._contains.push(item);
  return item;
}
// ---- 事件记录与派发：让「事件委托 / scroll / resize」这类真实交互可测 ----
const listeners = { doc: {}, win: {} };
function addL(bucket, type, fn) { (bucket[type] || (bucket[type] = [])).push(fn); }
function dispatch(bucket, type, ev) {
  const arr = bucket[type] || [];
  for (const fn of arr) fn(ev);
  return arr.length;
}
function fakeEv(target, x, y) {
  return { target, clientX: x == null ? 0 : x, clientY: y == null ? 0 : y,
           stopPropagation() {}, preventDefault() {} };
}
// ---- 可控 rAF：能推进帧队列并计数，用来验证不会自调用成死循环 ----
const rafQueue = [];
let rafSeq = 0;
global.requestAnimationFrame = function (cb) { rafQueue.push(cb); return ++rafSeq; };
function flushRaf(maxFrames) {
  let executed = 0, frames = 0;
  const cap = maxFrames || 50;
  while (rafQueue.length && frames < cap) {
    const batch = rafQueue.splice(0, rafQueue.length);
    frames++;
    for (const cb of batch) { cb(); executed++; }
  }
  return { executed: executed, frames: frames, pending: rafQueue.length };
}
const wsStubs = [];
global.document = {
  getElementById: makeEl,
  querySelectorAll: (sel) => (sel === ".ws-menu" ? wsWraps.map((w) => w._menu) : []),
  // 只放行悬浮菜单用的选择器，其余一律 null，避免影响页面原有逻辑
  querySelector: (sel) => {
    if (sel === ".ws-wrap:hover .ws-menu") {
      for (const w of wsWraps) { if (w._hover) return w._menu; }
      return null;
    }
    // 忠实还原真实 DOM：不加 :hover 限定时拿到的是「文档里第一个」菜单。
    // 少了这条，就无法复现「定位到别的卡片菜单」这个原始 BUG。
    if (sel === ".ws-menu") return wsWraps.length ? wsWraps[0]._menu : null;
    return null;
  },
  addEventListener: (type, fn) => addL(listeners.doc, type, fn),
  createElement: () => ({ style:{}, select(){}, value:"" }),
  body: { appendChild(){}, removeChild(){} },
};
global.window = {
  addEventListener: (type, fn) => addL(listeners.win, type, fn),
  innerWidth: 1440, innerHeight: 900,
};
global.localStorage = { getItem: () => null, setItem(){}, removeItem(){} };
const clipCalls = [];
// Node 22 的 globalThis.navigator 是只读 accessor，直接赋值会静默失效 —— 必须 defineProperty
Object.defineProperty(global, "navigator", {
  configurable: true, writable: true,
  value: { sendBeacon(){}, clipboard: { writeText: async (s) => { clipCalls.push(s); } } },
});
global.Blob = function(){};
const fetchCalls = [];
global.fetch = async (url, opts) => {
  fetchCalls.push({ url: url, opts: opts || {} });
  if (String(url).indexOf("/api/workspace/") >= 0) {
    return { ok: true, status: 200, json: async () => ({ ok: true, message: "Opened" }) };
  }
  return {
    ok: true, status: 200,
    json: async () => ({
      schema_version: 2,
      summary: { today: 2, overdue: 1 },
      week: { start: "2026-10-05", end: "2026-10-11", created: 0, done: 1 },
      defaults: { status: "进行中", importance: "不重要", urgent: "不紧急" },
      // 编辑器可用性由后端给；前端据此决定是否渲染「用编辑器打开」
      editor: { configured: true, available: true, label: "Cursor", path: "C:\\...\\Cursor.exe", error: null },
      storage_dir: "G:\\Projects\\19AI\\skills\\awam-todo\\storage",
      items: mockItems, revision: "abc",
    }),
  };
};
// 菜单显隐由 CSS :hover 决定，桩里按 wrap 的 hover 态还原 display
global.getComputedStyle = (el) => {
  const wrap = el && el._wrap;
  return { display: wrap && wrap._hover ? "flex" : "none" };
};

let failed = false;
function check(name, cond, extra) {
  console.log((cond ? "  PASS  " : "  FAIL  ") + name + (cond ? "" : "  | " + (extra || "")));
  if (!cond) failed = true;
}

(async () => {
  try {
    eval(code + "\n;global.__render = render; global.__setState = function(s){ currentState = s; };" +
      "\n;global.__store = store;" +
      "\n;global.__ws = { positionWsMenu: positionWsMenu, followWsMenuX: followWsMenuX," +
      " activeWsMenu: activeWsMenu, GAP: WS_GAP, OVERLAP: WS_OVERLAP, MARGIN: WS_MARGIN," +
      " computeWsTop: computeWsTop, computeWsLeft: computeWsLeft, wsMenuSize: wsMenuSize," +
      " wsMenuShown: wsMenuShown, scheduleWsReposition: scheduleWsReposition," +
      " repositionActiveWsMenu: repositionActiveWsMenu," +
      " setViewport: function(w, h){ window.innerWidth = w; window.innerHeight = h; }," +
      " setMouse: function(x, y){ lastMouse.x = x; lastMouse.y = y; } };" +
      "\n;global.__setLang = setLang;");
  } catch (e) {
    console.log("  FAIL  脚本执行抛错 | " + e.message);
    process.exit(1);
  }
  await new Promise(r => setTimeout(r, 300));

  const list = els["list"] ? els["list"].innerHTML : "";
  const nav = els["navSide"] ? els["navSide"].innerHTML : "";
  check("列表渲染出卡片", (list.match(/class="card/g) || []).length === 3, list.slice(0, 200));
  check("逾期卡有红色置顶说明", /pin red/.test(list) && /Overdue 16 day\(s\)/.test(list));
  check("停滞卡有琥珀置顶说明", /pin grace/.test(list) && /No progress for 4 day\(s\)/.test(list));
  check("逾期卡给出两个出口", /Advance now/.test(list) && /Reschedule/.test(list));
  check("卡片展示预案", /Blocker/.test(list) && /拿起手机前先做 10 分钟/.test(list));
  check("无推算时显示 N/A", /N\/A/.test(list));
  check("导航渲染含今日视图", /data-k="today"/.test(nav));
  check("导航含设置入口", /data-k="settings"/.test(nav), nav.slice(0, 200));
  check("默认视图是全部(active)", /class="navitem active" data-k="all"/.test(nav), nav.slice(0, 160));
  check("默认视图不是今日入口", !/navitem active" data-k="today"/.test(nav));
  check("默认语言为英文", /Advance now/.test(list) && !/立即推进/.test(list));
  check("周口径条已渲染(英文)", /starts Monday/.test(els["weekbar"].innerHTML || ""));
  check("底部新建入口文案(英文)", /New todo \(click here too\)/.test(els["newEntryBottom"].innerHTML || ""));
  check("图标为内联 svg", /<svg class="ic/.test(list));
  check("无 emoji 输出", !/[\u{1F300}-\u{1FAFF}]/u.test(list));

  // ---------- 设置页：捕获服务（快捷键 / 分诊类型 / 试用分诊） ----------
  global.__setState("settings"); global.__render();
  const setHtml = els["list"].innerHTML || "";
  check("设置页渲染捕获服务卡片", /Capture service/.test(setHtml), setHtml.slice(0, 200));
  check("设置页含快捷键输入框", /id="set_cap_hotkey"/.test(setHtml));
  check("设置页含启用开关", /id="set_cap_enabled"/.test(setHtml));
  check("设置页含分诊类型开关", /id="set_type_add"/.test(setHtml) && /id="set_type_delete"/.test(setHtml));
  check("设置页含试用分诊", /id="triageTryText"/.test(setHtml));
  global.__setState("all"); global.__render();
  check("从设置页切回列表正常", (els["list"].innerHTML.match(/class="card/g) || []).length === 3);

  // 切到「今日」视图
  global.__setState("today"); global.__render();
  const todayList = els["list"].innerHTML || "";
  check("今日视图只剩置顶项", (todayList.match(/class="card/g) || []).length === 2, todayList.slice(0, 120));
  check("今日视图有口径说明(英文)", /Today: 2 todo\(s\) to handle/.test(todayList));

  // ---------- 国际化：默认英文，可切换中文并持久化，切回英文恢复 ----------
  global.__setLang("zh"); global.__render();
  const zhList = els["list"].innerHTML || "";
  check("切中文后出口显示中文", /立即推进/.test(zhList) && /调整计划/.test(zhList));
  check("切中文后预案显示中文", /障碍/.test(zhList) && /对策/.test(zhList));
  check("切中文后无推算显示中文", /暂无推算/.test(zhList));
  check("切中文后导航含进行中", /进行中/.test(els["navSide"].innerHTML || ""));
  check("切中文后底部新建入口为中文", /新增待办（也可以点这里）/.test(els["newEntryBottom"].innerHTML || ""));
  global.__setLang("en"); global.__render();
  const enBack = els["list"].innerHTML || "";
  check("切回英文恢复英文", /Advance now/.test(enBack) && !/立即推进/.test(enBack));

  console.log("\n== 工作空间悬浮菜单定位 ==");
  const WS = global.__ws;
  const GAP = WS.GAP;                    // JS 与 CSS 里必须同一套间隙，别各写各的
  const MW = 160, MH = 118;
  const wrapA = makeWrap("A", { top:100, bottom:118, left:200, right:320, width:120, height:18 });
  const wrapB = makeWrap("B", { top:400, bottom:418, left:200, right:320, width:120, height:18 });
  const menuA = wrapA._menu, menuB = wrapB._menu;

  // 鼠标放在屏幕中间（远离两个路径元素），验证纵向不吃鼠标的 y
  WS.setMouse(600, 300);
  WS.positionWsMenu(menuA);
  const topA = parseInt(menuA.style.top, 10);
  check("纵向锚点取路径元素底边(+间隙)，不是鼠标位置", topA === wrapA._rect.bottom + GAP,
    "top=" + topA + "，期望 " + (wrapA._rect.bottom + GAP));
  WS.setMouse(600, 700);
  WS.positionWsMenu(menuA);
  check("鼠标纵向移动不改变 top", parseInt(menuA.style.top, 10) === topA, menuA.style.top);
  check("纵向锚点已缓存到菜单上", menuA.dataset.anchorTop === String(topA), menuA.dataset.anchorTop);

  // 只跟横向：left 变、top 不动
  WS.setMouse(260, 260);
  WS.positionWsMenu(menuA);
  const leftBefore = menuA.style.left;
  WS.setMouse(340, 100);      // 横向移动 + 纵向移动，只有横向应该起作用
  WS.followWsMenuX(menuA);
  check("mousemove 只改横向：top 不变", parseInt(menuA.style.top, 10) === topA, menuA.style.top);
  check("mousemove 只改横向：left 变化", menuA.style.left !== leftBefore,
    "before=" + leftBefore + " after=" + menuA.style.left);
  check("横向不越视口右边界", parseInt(menuA.style.left, 10) + MW <= window.innerWidth - 8);
  check("横向与路径元素仍重叠", parseInt(menuA.style.left, 10) < wrapA._rect.right &&
    parseInt(menuA.style.left, 10) + MW > wrapA._rect.left, menuA.style.left);

  // 多张卡片时，定位的必须是「当前 hover 的那个」菜单
  wrapA._hover = true;  wrapB._hover = false;
  check("多菜单时取到当前 hover 的菜单", WS.activeWsMenu() === menuA);
  wrapA._hover = false; wrapB._hover = true;
  const active = WS.activeWsMenu();
  check("hover 切换后跟着切换到另一个菜单", active === menuB);
  WS.positionWsMenu(active);
  check("当前菜单已锚定到自己的路径元素", parseInt(menuB.style.top, 10) === wrapB._rect.bottom + GAP, menuB.style.top);
  check("另一个菜单没被顺手移动", parseInt(menuA.style.top, 10) === topA, menuA.style.top);

  // 贴底时翻转到路径元素上方
  const wrapC = makeWrap("C", { top:880, bottom:898, left:100, right:220, width:120, height:18 });
  wrapA._hover = false; wrapB._hover = false; wrapC._hover = true;
  WS.setMouse(150, 890);
  WS.positionWsMenu(wrapC._menu);
  check("下方空间不足时翻转到上方", parseInt(wrapC._menu.style.top, 10) === wrapC._rect.top - GAP - MH,
    wrapC._menu.style.top);
  check("翻转时打上 upward 标记（桥接带改到下方）", wrapC._menu.classList.contains("upward"));
  wrapC._hover = false;

  // 静态校验：桥接带必须存在且高于间隙，否则中间有断带，鼠标永远过不去
  check("菜单带透明桥接带 CSS", /\.ws-menu::before\{[^}]*background:transparent/.test(html));
  check("翻转时桥接带改到下方", /\.ws-menu\.upward::before\{[^}]*top:100%/.test(html));
  const bridge = (html.match(/\.ws-menu::before\{[^}]*height:(\d+)px/) || [])[1];
  check("桥接带高度覆盖菜单间隙", Number(bridge) >= GAP, "bridge=" + bridge + " gap=" + GAP);

  console.log("\n== QA 独立边界验证（悬浮菜单）==");
  const M = WS.MARGIN, GAP2 = WS.GAP;
  const topOf = (m) => parseInt(m.style.top, 10);
  const leftOf = (m) => parseInt(m.style.left, 10);
  const overlapOf = (m, r) => Math.min(leftOf(m) + m.offsetWidth, r.right) - Math.max(leftOf(m), r.left);
  const clearHover = () => wsWraps.forEach((w) => { w._hover = false; });
  // 「鼠标能不能从路径元素走到菜单」的硬指标：菜单与路径元素的垂直间隙。
  // 0 表示菜单直接压住路径元素（也算连通）；>0 则必须 <= 桥接带高度。
  const BRIDGE_H = Number((html.match(/\.ws-menu::before\{[^}]*height:(\d+)px/) || [])[1]);
  const vGapOf = (m, r) => {
    const top = parseInt(m.style.top, 10), bottom = top + (m.offsetHeight || 118);
    if (bottom >= r.top && top <= r.bottom) return 0;
    return top > r.bottom ? top - r.bottom : r.top - bottom;
  };

  // ---- 边界1：列表重渲染后，菜单节点是新节点（dataset 被清空）还能否正确锚定 ----
  // render() 重建 innerHTML 会造出全新的 .ws-menu，dataset.anchorTop 为空。
  // 场景：保存完任务 / 切换筛选后指针恰好停在原路径元素上。
  const wrapR = makeWrap("R", { top:300, bottom:318, left:200, right:320, width:120, height:18 });
  clearHover(); wrapR._hover = true;
  dispatch(listeners.doc, "mouseover", fakeEv(wrapR._ws, 260, 309));
  check("重渲染后 mouseover 能重新算出纵向锚点", topOf(wrapR._menu) === wrapR._rect.bottom + GAP2,
    "top=" + wrapR._menu.style.top + " 期望 " + (wrapR._rect.bottom + GAP2));
  check("重渲染后菜单不再停在 -9999", leftOf(wrapR._menu) > -1000, wrapR._menu.style.left);

  // 更苛刻：新节点没锚定过，直接来一次 mousemove（不是 mouseover），必须自愈成完整定位
  const wrapR2 = makeWrap("R2", { top:500, bottom:518, left:200, right:320, width:120, height:18 });
  wrapR._menu.dataset.anchorTop = undefined; delete wrapR._menu.dataset.anchorTop;
  wrapR._hover = false; wrapR2._hover = true;
  wrapR2._menu.style.top = "-9999px"; wrapR2._menu.style.left = "-9999px";
  dispatch(listeners.doc, "mousemove", fakeEv(wrapR2._ws, 260, 509));
  check("未锚定节点收到 mousemove 时自愈为完整定位", topOf(wrapR2._menu) === wrapR2._rect.bottom + GAP2,
    "top=" + wrapR2._menu.style.top);
  check("自愈后横向也一并定位", leftOf(wrapR2._menu) > -1000, wrapR2._menu.style.left);
  clearHover();

  // ---- 边界2：rAF 必须收敛，不能自调用成死循环 ----
  const wrapQ = makeWrap("Q", { top:200, bottom:218, left:200, right:320, width:120, height:18 }, { w: 0, h: 0 });
  rafQueue.length = 0;
  WS.positionWsMenu(wrapQ._menu);                 // 首显前量不到尺寸 -> 排一次 rAF
  check("尺寸未知时排入 rAF 校正", rafQueue.length === 1, "queued=" + rafQueue.length);
  wrapQ._menu.offsetWidth = 160; wrapQ._menu.offsetHeight = 118;   // 下一帧可见
  const r1 = flushRaf(20);
  check("rAF 校正后队列清空（无自调用死循环）", r1.pending === 0, JSON.stringify(r1));
  check("rAF 回调次数收敛（<=2）", r1.executed <= 2, JSON.stringify(r1));
  check("校正后锚点按真实尺寸重算", topOf(wrapQ._menu) === wrapQ._rect.bottom + GAP2, wrapQ._menu.style.top);

  // 极端：菜单一直量不到尺寸（始终 display:none）也不许反复排队
  const wrapQ2 = makeWrap("Q2", { top:200, bottom:218, left:200, right:320, width:120, height:18 }, { w: 0, h: 0 });
  rafQueue.length = 0;
  WS.positionWsMenu(wrapQ2._menu);
  const r2 = flushRaf(20);
  check("始终不可见时 rAF 也只跑一次", r2.executed === 1 && r2.pending === 0, JSON.stringify(r2));
  check("anchorPending 已复位", wrapQ2._menu.dataset.anchorPending === "0", wrapQ2._menu.dataset.anchorPending);

  // ---- 边界3：菜单比视口还高 / 路径元素贴视口底 ----
  WS.setViewport(1440, 200);
  const tall = makeWrap("tall", { top:50, bottom:68, left:200, right:320, width:120, height:18 }, { w:160, h:180 });
  WS.positionWsMenu(tall._menu);
  const tTall = topOf(tall._menu);
  check("菜单高于视口时 top 仍为有限非负数", Number.isFinite(tTall) && tTall >= 0, "top=" + tTall);
  check("菜单高于视口时不越出视口上边界", tTall >= M, "top=" + tTall + " margin=" + M);
  const gapTall = vGapOf(tall._menu, tall._rect);
  check("菜单高于视口时与路径元素仍连通（间隙<=桥接带）", gapTall <= BRIDGE_H, "gap=" + gapTall);

  WS.setViewport(1440, 300);
  const bottomish = makeWrap("bot", { top:280, bottom:298, left:200, right:320, width:120, height:18 }, { w:160, h:118 });
  WS.positionWsMenu(bottomish._menu);
  const tBot = topOf(bottomish._menu);
  check("贴底且上方放不下时 top 非负数", Number.isFinite(tBot) && tBot >= 0, "top=" + tBot);
  const gapBot = vGapOf(bottomish._menu, bottomish._rect);
  check("贴底极端情形与路径元素仍连通（间隙<=桥接带）", gapBot <= BRIDGE_H, "gap=" + gapBot);

  // 常规：贴底但上方放得下 -> 必须翻转
  WS.setViewport(1440, 900);
  const flipW = makeWrap("flip", { top:860, bottom:878, left:200, right:320, width:120, height:18 }, { w:160, h:118 });
  WS.positionWsMenu(flipW._menu);
  check("贴底且上方放得下时翻转到上方", topOf(flipW._menu) === flipW._rect.top - GAP2 - 118, flipW._menu.style.top);
  check("翻转后菜单不遮挡路径元素", topOf(flipW._menu) + 118 <= flipW._rect.top, flipW._menu.style.top);
  check("翻转后不越出视口上边界", topOf(flipW._menu) >= M, flipW._menu.style.top);

  // ---- 边界4：窄视口 + 路径元素贴右边缘，「视口 clamp」与「水平重叠」打架 ----
  const narrowCases = [
    { vw: 480, rect: { left:400, right:470, width:70 }, mouse: 430 },
    { vw: 360, rect: { left:150, right:190, width:40 }, mouse: 170 },
    { vw: 200, rect: { left:150, right:190, width:40 }, mouse: 190 },
    { vw: 480, rect: { left:462, right:478, width:16 }, mouse: 470 },
  ];
  let allOverlap = true, allInView = true, worst = 999;
  narrowCases.forEach((c, i) => {
    WS.setViewport(c.vw, 900);
    const w = makeWrap("n" + i,
      { top:300, bottom:318, left:c.rect.left, right:c.rect.right, width:c.rect.width, height:18 },
      { w:160, h:118 });
    WS.setMouse(c.mouse, 309);
    WS.positionWsMenu(w._menu);
    const ov = overlapOf(w._menu, w._rect);
    const inView = leftOf(w._menu) >= 0 && leftOf(w._menu) + 160 <= c.vw + 1;
    worst = Math.min(worst, ov);
    if (ov <= 0) allOverlap = false;
    if (!inView) allInView = false;
    console.log("    case vw=" + c.vw + " rect=[" + c.rect.left + "," + c.rect.right + "] mouse=" +
      c.mouse + " -> left=" + leftOf(w._menu) + " overlap=" + ov + "px");
  });
  check("窄视口各用例菜单均与路径元素水平重叠（可垂直移入）", allOverlap, "最小重叠=" + worst);
  check("窄视口各用例菜单未溢出视口", allInView);
  WS.setViewport(1440, 900);

  // ---- 边界5：多卡片快速切换 ----
  const wrapX = makeWrap("X", { top:100, bottom:118, left:200, right:320, width:120, height:18 });
  const wrapY = makeWrap("Y", { top:400, bottom:418, left:600, right:720, width:120, height:18 });
  clearHover(); wrapX._hover = true;
  dispatch(listeners.doc, "mouseover", fakeEv(wrapX._ws, 260, 109));
  const xTop0 = topOf(wrapX._menu), xLeft0 = leftOf(wrapX._menu);
  check("切换到卡片B前，A 的菜单可见", WS.wsMenuShown(wrapX._menu) === true);
  clearHover(); wrapY._hover = true;                 // 指针直接跳到 B 的路径
  check("切到B后，A 的菜单不再显示（无残留可见）", WS.wsMenuShown(wrapX._menu) === false);
  dispatch(listeners.doc, "mouseover", fakeEv(wrapY._ws, 660, 409));
  check("B 的菜单锚定到 B 自己的路径元素", topOf(wrapY._menu) === wrapY._rect.bottom + GAP2,
    wrapY._menu.style.top);
  check("切换时 A 的菜单没被顺手改动", topOf(wrapX._menu) === xTop0 && leftOf(wrapX._menu) === xLeft0,
    wrapX._menu.style.top + "," + wrapX._menu.style.left);
  check("activeWsMenu 取到的是 B", WS.activeWsMenu() === wrapY._menu);
  // 直接复现用户报的原始 BUG：不按 hover 过滤就会拿到文档里第一张卡片的菜单
  check("activeWsMenu 不会拿到第一张卡片的菜单（原始 BUG 回归）",
    WS.activeWsMenu() !== wsWraps[0]._menu || wrapY === wsWraps[0],
    "first=" + (wsWraps[0] && wsWraps[0]._name));
  // 鼠标停在菜单内部时不应继续横向漂移（否则菜单会追着鼠标跑）
  wrapY._menu._contains.push(wrapY._ws);
  const yLeft0 = leftOf(wrapY._menu);
  dispatch(listeners.doc, "mousemove", fakeEv(wrapY._menu, 900, 500));
  check("鼠标进入菜单后不再横向跟随（避免抖动）", leftOf(wrapY._menu) === yLeft0, wrapY._menu.style.left);
  wrapY._menu._contains.pop();
  clearHover();

  // ---- 边界6：滚动 / 缩放后纵向锚点重算 ----
  const wrapS = makeWrap("S", { top:300, bottom:318, left:200, right:320, width:120, height:18 });
  clearHover(); wrapS._hover = true;
  WS.setMouse(260, 309);
  WS.positionWsMenu(wrapS._menu);
  check("滚动前锚点正确", topOf(wrapS._menu) === 318 + GAP2, wrapS._menu.style.top);
  wrapS._rect = { top:120, bottom:138, left:200, right:320, width:120, height:18 };  // 页面滚动了
  dispatch(listeners.win, "scroll", fakeEv(null, 260, 129));
  check("滚动后纵向锚点跟着路径元素重算", topOf(wrapS._menu) === 138 + GAP2, wrapS._menu.style.top);
  wrapS._rect = { top:520, bottom:538, left:200, right:320, width:120, height:18 };
  dispatch(listeners.win, "resize", fakeEv(null, 260, 529));
  check("resize 后纵向锚点跟着重算", topOf(wrapS._menu) === 538 + GAP2, wrapS._menu.style.top);
  clearHover();

  // ---- 边界7：桥接带与间隙的数值关系（断带 = 鼠标永远进不去）----
  const bridgeH = Number((html.match(/\.ws-menu::before\{[^}]*height:(\d+)px/) || [])[1]);
  const bridgeTop = Number((html.match(/\.ws-menu::before\{[^}]*top:(-?\d+)px/) || [])[1]);
  const wrapB2 = makeWrap("B2", { top:300, bottom:318, left:200, right:320, width:120, height:18 });
  clearHover(); wrapB2._hover = true;
  WS.positionWsMenu(wrapB2._menu);
  const menuTop = topOf(wrapB2._menu);
  const bandTop = menuTop + bridgeTop, bandBottom = menuTop + bridgeTop + bridgeH;
  check("向下展开时桥接带完整盖住间隙",
    bandTop <= wrapB2._rect.bottom && bandBottom >= menuTop,
    "带=[" + bandTop + "," + bandBottom + "] 路径底=" + wrapB2._rect.bottom + " 菜单顶=" + menuTop);
  check("向下展开时桥接带还压住路径元素本身", bandTop <= wrapB2._rect.bottom && bandBottom >= wrapB2._rect.bottom,
    "带=[" + bandTop + "," + bandBottom + "]");
  // 翻转到上方：桥接带改到菜单下方（top:100%）
  const wrapU = makeWrap("U", { top:200, bottom:218, left:200, right:320, width:120, height:18 });
  clearHover(); wrapU._hover = true;
  WS.setViewport(1440, 260);                       // 逼它翻转
  WS.positionWsMenu(wrapU._menu);
  check("构造用例确实翻转了", wrapU._menu.classList.contains("upward"), wrapU._menu.classList._s.toString());
  const uTop = topOf(wrapU._menu), uBottom = uTop + 118;
  check("向上翻转时桥接带盖住间隙（top:100% + 14px）",
    uBottom <= wrapU._rect.top && uBottom + bridgeH >= wrapU._rect.top,
    "菜单底=" + uBottom + " 路径顶=" + wrapU._rect.top + " 带宽=" + bridgeH);
  check("桥接带高度 >= 间隙 + 余量", bridgeH >= GAP2 + 4, "bridge=" + bridgeH + " gap=" + GAP2);
  WS.setViewport(1440, 900);
  clearHover();

  // ---- 边界8：三个菜单项的点击回归（事件委托在 document 上）----
  const wrapC2 = makeWrap("C2", { top:300, bottom:318, left:200, right:320, width:120, height:18 },
    { path: "G:\\Projects\\Stock\\tdx-linker" });
  const itemCopy = makeWsItem(wrapC2._menu, "copy");
  const itemOpen = makeWsItem(wrapC2._menu, "open");
  const itemCur = makeWsItem(wrapC2._menu, "cursor");
  clipCalls.length = 0; fetchCalls.length = 0;
  dispatch(listeners.doc, "click", fakeEv(itemCopy, 260, 309));
  dispatch(listeners.doc, "click", fakeEv(itemOpen, 260, 309));
  dispatch(listeners.doc, "click", fakeEv(itemCur, 260, 309));
  await new Promise((r) => setTimeout(r, 50));
  check("复制路径写入剪贴板", clipCalls.length === 1 && clipCalls[0] === "G:\\Projects\\Stock\\tdx-linker",
    JSON.stringify(clipCalls));
  const wsUrls = fetchCalls.filter((f) => String(f.url).indexOf("/api/workspace/") >= 0).map((f) => String(f.url));
  check("打开目录命中 /api/workspace/open", wsUrls.indexOf("/api/workspace/open") >= 0, JSON.stringify(wsUrls));
  check("用编辑器打开命中 /api/workspace/editor", wsUrls.indexOf("/api/workspace/editor") >= 0, JSON.stringify(wsUrls));
  check("不再请求历史接口 /api/workspace/cursor", wsUrls.indexOf("/api/workspace/cursor") < 0, JSON.stringify(wsUrls));
  const openBody = JSON.parse((fetchCalls.find((f) => String(f.url).indexOf("/api/workspace/open") >= 0) || {}).opts
    ? (fetchCalls.find((f) => String(f.url).indexOf("/api/workspace/open") >= 0).opts.body || "{}") : "{}");
  check("打开目录带上了正确的 path", openBody.path === "G:\\Projects\\Stock\\tdx-linker", JSON.stringify(openBody));

  global.__setState("overdue"); global.__render();
  check("逾期视图只剩逾期项", (els["list"].innerHTML.match(/class="card/g) || []).length === 1);

  // ---------- 编辑器可配置：可用性决定菜单项是否渲染 ----------
  global.__setState("all"); global.__render();
  let cardHtml = els["list"].innerHTML;
  check("编辑器可用时渲染「用编辑器打开」", /data-ws-act="editor"/.test(cardHtml), cardHtml.slice(0, 120));
  check("菜单项显示配置的编辑器名", /Open with Cursor/.test(cardHtml), cardHtml.slice(0, 120));
  check("编辑器可用时不再渲染旧 cursor 动作", !/data-ws-act="cursor"/.test(cardHtml));

  // 只配了 path、没配 label 时必须回落到通用文案「用编辑器打开」，不能拼出「用打开」
  global.__store.editor = { configured: true, available: true, label: null,
                            path: "C:\\Apps\\Code.exe", error: null };
  global.__render();
  const genericHtml = els["list"].innerHTML;
  check("label 未配置时回落为「用编辑器打开」", /Open with editor/.test(genericHtml), genericHtml.slice(0, 120));
  check("回落时菜单项照常渲染", /data-ws-act="editor"/.test(genericHtml));
  check("回落时不会拼出「用打开」", !/Open with\s*$/.test(genericHtml), genericHtml.slice(0, 120));

  global.__store.editor = { configured: false, available: false, label: null, path: null,
                            error: "editor not configured (env.json lacks editor.path)" };
  global.__render();
  cardHtml = els["list"].innerHTML;
  check("编辑器不可用时不渲染「用编辑器打开」", !/data-ws-act="editor"/.test(cardHtml),
    cardHtml.match(/data-ws-act="[a-z]+"/g));
  check("编辑器不可用时仍保留复制路径与打开目录", /data-ws-act="copy"/.test(cardHtml) && /data-ws-act="open"/.test(cardHtml));

  global.__store.editor = { configured: true, available: false, label: "Cursor", path: "D:\\gone\\Cursor.exe",
                            error: "editor path invalid (file missing)" };
  global.__render();
  check("配置了但路径失效时同样不渲染该菜单项", !/data-ws-act="editor"/.test(els["list"].innerHTML));

  // 复原，避免影响后续断言
  global.__store.editor = { configured: true, available: true, label: "Cursor", path: "C:\\...\\Cursor.exe", error: null };
  global.__render();

  console.log(failed ? "\n结果：存在失败项" : "\n结果：全部通过");
  process.exit(failed ? 1 : 0);
})();
