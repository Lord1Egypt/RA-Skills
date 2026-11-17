/**
 * verify_dashboard.js —— 通用看板交付前校验
 *
 * 用法:  node verify_dashboard.js ./看板.html
 * 退出码: 0 = 可交付；非 0 = 有错误，不得交付
 *
 * 四道门:
 *   1. 语法门禁        —— DATA / app JS 能被 vm 解析执行
 *   2. 桩化运行时冒烟   —— 最小 document + 桩 echarts，捕获运行时异常
 *   3. series 断言     —— series 存在、data 为数组、无 NaN/undefined
 *                        （显式 null = 「无数据」，仅告警不报错）
 *   4. 产出扫描        —— 空容器检测 + 全文 undefined/NaN 泄漏扫描
 */
const fs = require('fs');
const vm = require('vm');

const file = process.argv[2];
if (!file) { console.error('用法: node verify_dashboard.js <看板.html>'); process.exit(2); }
const html = fs.readFileSync(file, 'utf8');

// ---- 切分 script 块 ----
// 约定顺序: [0]=echarts  →  [DATA]  →  [app]  →  [可选面板/其他附加块]
// ⚠️ 不要用 blocks.length-2 / -1 定位：主生成器可能装配额外的 script 块
//    （如 gen_score_panel.py 的固化注入段），那样 DATA 会被误认成 app。
//    改为按**内容特征**定位，顺序变了也不受影响。
const blocks = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m => m[1]);
if (blocks.length < 3) {
  console.error('❌ script 块不足 3 个（需 echarts / DATA / app 三块分离），实际 ' + blocks.length);
  process.exit(1);
}
const dataIdx = blocks.findIndex((b, i) => i > 0 && /(^|[\s;])var\s+DATA\s*=/.test(b));
const appIdx = blocks.findIndex((b, i) => i > 0 && i !== dataIdx && /通用看板渲染器/.test(b));
if (dataIdx < 0) {
  console.error('❌ 未找到 DATA 块（期望含 "var DATA="）。实际块数 ' + blocks.length +
                '，各块开头: ' + blocks.map((b, i) => i + ':' + JSON.stringify(b.slice(0, 40))).join(' | '));
  process.exit(1);
}
const dataJs = blocks[dataIdx];
const appJs = appIdx >= 0 ? blocks[appIdx] : blocks[blocks.length - 1];
const nonEchartsJs = blocks.slice(1).join('\n');

const ids = new Set([...html.matchAll(/id="([A-Za-z0-9_]+)"/g)].map(m => m[1]));

// ---- 最小 DOM ----
function mkEl(id) {
  return {
    id, _html: '', _text: '', style: {}, className: '',
    get innerHTML() { return this._html; },
    set innerHTML(v) { this._html = String(v); },
    get textContent() { return this._text; },
    set textContent(v) { this._text = String(v); this._html = String(v); },
    querySelectorAll(sel) {
      const cls = (sel || '').replace(/^\./, '');
      const re = new RegExp('class="' + cls + '([^"]*)"', 'g');
      const out = [];
      let m;
      while ((m = re.exec(this._html))) {
        const tagHtml = m[0] + '" ' + (this._html.slice(m.index, m.index + 400));
        out.push(mkTab(tagHtml, cls));
      }
      return out;
    },
    setAttribute(k, v) { this['_' + k] = v; },
    getAttribute(k) { return this['_' + k]; },
    addEventListener() {},
    onclick: null,
  };
}
function mkTab(ctxHtml, cls) {
  const dv = (new RegExp('data-k="([^"]*)"').exec(ctxHtml) || [])[1];
  const on = new RegExp('class="' + cls + ' on"').test(ctxHtml);
  return {
    className: on ? cls + ' on' : cls,
    getAttribute: (k) => (k === 'data-k' ? dv : undefined),
    onclick: null,
  };
}

const elements = {};
ids.forEach(i => { elements[i] = mkEl(i); });

// 文档级 querySelectorAll：tab 多由生成器静态渲染，直接从原始 HTML 解析
function querySelectorAll(sel) {
  const cls = (sel || '').replace(/^\./, '');
  const re = new RegExp('<(\\w+)[^>]*class="' + cls + '([^"]*)"[^>]*>', 'g');
  const out = [];
  let m;
  while ((m = re.exec(html))) {
    const tagHtml = m[0];
    const dk = (new RegExp('data-k="([^"]*)"').exec(tagHtml) || [])[1];
    out.push({
      className: cls + (m[2] || ''),
      getAttribute: (k) => (k === 'data-k' ? dk : undefined),
      onclick: null,
    });
  }
  return out;
}

const document = {
  getElementById(id) {
    if (!elements[id]) { throw new Error('MISSING ELEMENT: #' + id + '（JS 引用了 HTML 中不存在的容器）'); }
    return elements[id];
  },
  querySelectorAll,
};

// ---- 桩 echarts（跟踪实例，真实检验 getInstanceByDom 复用逻辑）----
const optionLog = {};
const instances = new Map();
const echarts = {
  init(el) {
    if (instances.has(el.id)) return instances.get(el.id);
    const inst = {
      _el: el,
      setOption(o) {
        if (!o || typeof o !== 'object') throw new Error('setOption 非对象: ' + el.id);
        const ser = o.series;
        if (!ser) throw new Error('缺少 series: ' + el.id);
        const arr = Array.isArray(ser) ? ser : [ser];
        arr.forEach((s, i) => {
          if (!s.type) throw new Error('series[' + i + '] 缺 type @' + el.id);
          if (!Array.isArray(s.data)) throw new Error('series[' + i + '].data 非数组 @' + el.id);
          const val = d => (d && typeof d === 'object') ? d.value : d;
          const bad = s.data.filter(d => {
            const v = val(d);
            return v === undefined || (typeof v === 'number' && isNaN(v));
          });
          if (bad.length) throw new Error('series[' + i + '] 含 NaN/undefined 数据点 x' + bad.length + ' @' + el.id);
          const nulls = s.data.filter(d => val(d) === null);
          if (nulls.length) warnings.push('series[' + i + '] 含 ' + nulls.length + ' 个 null（无数据，不绘制）@' + el.id);
        });
        optionLog[el.id] = o;
        return inst;
      },
      resize() {},
    };
    instances.set(el.id, inst);
    return inst;
  },
  getInstanceByDom(el) { return el && instances.has(el.id) ? instances.get(el.id) : null; },
};

const warnings = [];
const errors = [];
const sandbox = {
  document, echarts, console,
  window: { addEventListener() {} },
  Number, Math, Array, Object, String, JSON, isNaN, parseFloat, parseInt, Date,
  setTimeout, clearTimeout,
};
sandbox.window.echarts = echarts;
sandbox.globalThis = sandbox;

const ctx = vm.createContext(sandbox);
try {
  vm.runInContext(dataJs, ctx, { filename: 'DATA.js' });
  vm.runInContext(appJs, ctx, { filename: 'app.js' });
} catch (e) {
  errors.push('运行时异常: ' + e.message + '\n' + (e.stack || '').split('\n').slice(0, 6).join('\n'));
}

// ---- 空容器检测（基于原始 HTML；图表容器由 canvas 绘制，豁免）----
const chartIds = new Set([...html.matchAll(/id="([A-Za-z0-9_]+)"[^>]*class="[^"]*chart/g)].map(m => m[1]));
const blank = [];
ids.forEach(id => {
  if (chartIds.has(id)) return;
  const re = new RegExp('<\\w+[^>]*\\bid="' + id + '"[^>]*>\\s*</');
  if (re.test(html)) blank.push(id);
});

// ---- undefined / NaN 泄漏扫描（排除 echarts 库块）----
const leakBody = nonEchartsJs + '\n' + html.replace(blocks[0], '');
const leaks = [];
['undefined', 'NaN'].forEach(tok => {
  const re = new RegExp('(>|[\\s"\'=:(])' + tok + '([<\\s"\'=:),;]|$)', 'g');
  const m = leakBody.match(re);
  if (m) leaks.push(tok + ' x' + m.length);
});

// ---- 报告 ----
const chartList = Object.keys(optionLog);
console.log('=== 看板交付前校验: ' + file + ' ===');
if (errors.length) { console.log('❌ 错误:'); errors.forEach(e => console.log('  ' + e)); }
else console.log('✅ JS 执行无异常');
if (warnings.length) { console.log('⚠️  告警（可接受）:'); warnings.forEach(w => console.log('  ' + w)); }
console.log('  script 块数: ' + blocks.length + '（echarts / DATA / app）');
console.log('  图表已 setOption (' + chartList.length + '): ' + JSON.stringify(chartList));
console.log('  空容器: ' + (blank.length ? '❌ ' + JSON.stringify(blank) : '无 (OK)'));
console.log('  undefined/NaN 泄漏: ' + (leaks.length ? '❌ ' + leaks.join(', ') : '无 (OK)'));

const bad = errors.length || blank.length || leaks.length;
console.log(bad ? '\n❌ 校验未通过，不得交付' : '\n✅ 校验通过');
process.exit(bad ? 1 : 0);
