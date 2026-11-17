// Deterministic consistency rules. No model, no network. Same input → same output.
// 确定性一致性规则。不调模型、不联网，同一份输入跑十遍结果一模一样。
import { readFileSync } from 'node:fs';

const SEV = { high: 0, medium: 1, low: 2 };

// 每条 finding 同时带中英文。报告层按 --lang 选一套，规则层只写一次判定逻辑。
function add(out, base, zh, en) { out.push({ ...base, ...zh, en }); }

// ── helpers ──────────────────────────────────────────────────────────────────
const CN_NUM = { 零: 0, 〇: 0, 一: 1, 二: 2, 两: 2, 三: 3, 四: 4, 五: 5, 六: 6, 七: 7, 八: 8, 九: 9 };

function cnToInt(s) {
  const half = toHalf(s);
  if (/^\d+$/.test(half)) return +half;
  let section = 0, num = 0, seen = false;
  for (const ch of s) {
    if (ch in CN_NUM) { num = CN_NUM[ch]; seen = true; }
    else if (ch === '十') { section += (seen && num ? num : 1) * 10; num = 0; seen = true; }
    else if (ch === '百') { section += (seen && num ? num : 1) * 100; num = 0; seen = true; }
    else return NaN;
  }
  return seen ? section + num : NaN;
}

function toHalf(s) {
  return s.replace(/[！-～]/g, (c) => String.fromCharCode(c.charCodeAt(0) - 0xfee0));
}

// 一条 finding 命中多处时，若跨了文件，位置里必须带上文件名，否则没法定位。
function spread(hits) {
  const files = [...new Set(hits.map((h) => h.file))];
  const multi = files.length > 1;
  return {
    multi,
    file: multi ? `${files.length} 个文件` : files[0],
    loc: hits.map((h) => (multi ? `${h.file}:${h.loc}` : h.loc)).join(' / '),
  };
}

function snippet(text, at = 0, span = 46) {
  const start = Math.max(0, at - 12);
  const s = text.slice(start, start + span).replace(/\s+/g, ' ');
  return (start > 0 ? '…' : '') + s + (start + span < text.length ? '…' : '');
}

// ── label vocabulary ─────────────────────────────────────────────────────────
const TYPE_MAP = new Map(Object.entries({
  图: 'FIG', 插图: 'FIG', figure: 'FIG', fig: 'FIG', 'fig.': 'FIG',
  表: 'TAB', 附表: 'TAB', table: 'TAB', tab: 'TAB', 'tab.': 'TAB',
  式: 'EQ', 公式: 'EQ', equation: 'EQ', eq: 'EQ', 'eq.': 'EQ',
  附录: 'APP', appendix: 'APP',
  算法: 'ALG', algorithm: 'ALG',
  清单: 'LST', listing: 'LST',
}));
const TYPE_CN = { FIG: '图', TAB: '表', EQ: '公式', APP: '附录', ALG: '算法', LST: '清单' };
const TYPE_EN = { FIG: 'Figure', TAB: 'Table', EQ: 'Equation', APP: 'Appendix', ALG: 'Algorithm', LST: 'Listing' };

const LABEL_RE =
  /(插图|附表|附录|公式|算法|清单|图|表|式|Figures?|Figs?\.?|Tables?|Tabs?\.?|Equations?|Eqs?\.?|Appendix|Appendices|Algorithms?|Listings?)\s*([0-9０-９]+(?:\s*[-–—.·]\s*[0-9０-９]+)*|[A-Z](?![a-z]))/gi;

function normNum(raw) {
  return toHalf(raw).replace(/\s+/g, '').replace(/[–—.·]/g, '-');
}

function labelKey(type, num) { return `${type}#${num}`; }

function collectLabels(docs) {
  const captions = [];   // 题注（定义）
  const refs = [];       // 正文引用
  const tocLabels = [];  // 目录里列出的条目
  for (const doc of docs) {
    for (const b of doc.blocks) {
      if (b.toc) {
        LABEL_RE.lastIndex = 0;
        let tm;
        while ((tm = LABEL_RE.exec(b.text))) {
          const w = tm[1].toLowerCase().replace(/s$/, '');
          const ty = TYPE_MAP.get(w) || TYPE_MAP.get(w.replace(/\.$/, ''));
          if (ty) tocLabels.push({ type: ty, num: normNum(tm[2]), key: labelKey(ty, normNum(tm[2])), raw: tm[0], file: doc.file, loc: b.loc });
        }
        continue;
      }
      const bare = b.text.replace(/^[\s*_>#`\[（(【]+/, '');
      const lead = b.text.length - bare.length;
      const isCaptionStyle = /^(Caption|caption|题注|图题|表题)$/.test(b.style || '');
      LABEL_RE.lastIndex = 0;
      let m;
      while ((m = LABEL_RE.exec(b.text))) {
        const word = m[1].toLowerCase().replace(/s$/, '');
        const type = TYPE_MAP.get(word) || TYPE_MAP.get(word.replace(/\.$/, ''));
        if (!type) continue;
        const num = normNum(m[2]);
        const hit = {
          type, num, key: labelKey(type, num), raw: m[0],
          file: doc.file, loc: b.loc, block: b, at: m.index,
          snippet: snippet(b.text, m.index),
        };
        const atStart = m.index === lead;
        const cued = /^\s*(?:所示|中|所述|可见|列出)/.test(b.text.slice(m.index + m[0].length));
        const isCaption =
          !b.heading && (isCaptionStyle || (atStart && b.text.length <= 120 && !cued));
        (isCaption ? captions : refs).push(hit);
      }
    }
  }
  return { captions, refs, tocLabels };
}

// ── R1 编号连续性：跳号 / 重号 / 起始异常 ────────────────────────────────────
function ruleNumbering(captions, out) {
  const groups = new Map();
  for (const c of captions) {
    const parts = c.num.split('-');
    const last = parts[parts.length - 1];
    const val = /^\d+$/.test(last) ? +last : (/^[A-Z]$/.test(last) ? last.charCodeAt(0) - 64 : NaN);
    if (!Number.isFinite(val)) continue;
    const gk = `${c.type}|${parts.slice(0, -1).join('-')}`;
    if (!groups.has(gk)) groups.set(gk, []);
    groups.get(gk).push({ ...c, val });
  }

  for (const [gk, items] of groups) {
    const [type, prefix] = gk.split('|');
    const label = TYPE_CN[type] + (prefix ? ` ${prefix}-*` : '');
    const labelEn = TYPE_EN[type] + (prefix ? ` ${prefix}-*` : '');

    // 重号
    const byVal = new Map();
    for (const it of items) {
      if (!byVal.has(it.val)) byVal.set(it.val, []);
      byVal.get(it.val).push(it);
    }
    for (const [val, dupes] of byVal) {
      if (dupes.length < 2) continue;
      const disp = `${TYPE_CN[type]} ${dupes[0].num}`;
      const dispEn = `${TYPE_EN[type]} ${dupes[0].num}`;
      const { file, loc, multi } = spread(dupes);
      add(out, {
        severity: 'high', rule: 'numbering', file, loc, snippet: dupes[0].snippet,
      }, {
        type: '编号重号',
        message: `${disp} 出现了 ${dupes.length} 次题注${multi ? '（分布在多个文件里）' : ''}`,
        fix: multi
          ? `如果这几份是同一章的不同版本，请只传一份再跑；否则确认哪一处该改号 —— 重号会让所有指向 ${disp} 的引用变成歧义。`
          : `确认哪一处该改号；重号会让正文里所有指向 ${disp} 的引用变成歧义。`,
      }, {
        type: 'Duplicate number',
        message: `${dispEn} is used as a caption ${dupes.length} times${multi ? ' (across several files)' : ''}`,
        fix: multi
          ? `If these are different revisions of the same chapter, run against one of them only. Otherwise decide which one gets renumbered — every reference to ${dispEn} is ambiguous until then.`
          : `Decide which one gets renumbered — every reference to ${dispEn} is ambiguous until then.`,
      });
    }

    if (items.length < 2) continue;
    const vals = [...byVal.keys()].sort((a, b) => a - b);

    // 跳号
    const missing = [];
    for (let v = vals[0]; v <= vals[vals.length - 1]; v++) if (!byVal.has(v)) missing.push(v);
    if (missing.length) {
      const near = byVal.get(vals.find((v) => v > missing[0])) || items;
      const gaps = missing.map((v) => (prefix ? `${prefix}-${v}` : v)).join('、');
      add(out, {
        severity: 'medium', rule: 'numbering',
        file: near[0].file, loc: near[0].loc, snippet: near[0].snippet,
      }, {
        type: '编号跳号',
        message: `${label} 序列缺 ${gaps}（现有 ${vals[0]}–${vals[vals.length - 1]}）`,
        fix: '要么补上缺的那一个，要么把后面的整体前移重排；两种都行，但正文引用要跟着改。',
      }, {
        type: 'Numbering gap',
        message: `${labelEn} sequence is missing ${gaps} (present: ${vals[0]}–${vals[vals.length - 1]})`,
        fix: 'Either add the missing item or renumber everything after it — references must follow either way.',
      });
    }

    // 起始异常
    if (vals[0] !== 1) {
      add(out, {
        severity: 'low', rule: 'numbering',
        file: items[0].file, loc: items[0].loc, snippet: items[0].snippet,
      }, {
        type: '编号起始异常',
        message: `${label} 从 ${vals[0]} 开始，不是 1`,
        fix: '若前面那几个是合稿时丢的，按跳号处理；若本就从这里起编，忽略即可。',
      }, {
        type: 'Numbering does not start at 1',
        message: `${labelEn} starts at ${vals[0]}, not 1`,
        fix: 'If the earlier ones were lost in a merge, treat it as a gap; if the series legitimately starts here, ignore.',
      });
    }
  }
}

// ── R2 引用 / 题注 / 目录 三方对账 ────────────────────────────────────────────
// 三份清单要放在一起判，否则真实书稿会刷屏：很多教材的图题是嵌在图片里或用
// Word 自动题注域，文字层压根没有题注 —— 那是「这一项查不了」，不是「N 条悬空」。
function ruleLabelIntegrity(captions, refs, tocLabels, out) {
  const byType = (list) => {
    const m = new Map();
    for (const x of list) {
      if (!m.has(x.type)) m.set(x.type, []);
      m.get(x.type).push(x);
    }
    return m;
  };
  const capT = byType(captions), refT = byType(refs), tocT = byType(tocLabels);
  const types = new Set([...capT.keys(), ...refT.keys(), ...tocT.keys()]);

  for (const type of types) {
    const caps = capT.get(type) || [], rfs = refT.get(type) || [], tocs = tocT.get(type) || [];
    const capKeys = new Set(caps.map((c) => c.key));
    const tocKeys = new Set(tocs.map((t) => t.key));
    const known = new Set([...capKeys, ...tocKeys]);
    const expected = new Set([...tocKeys, ...rfs.map((r) => r.key)]);
    const cn = TYPE_CN[type], en = TYPE_EN[type];

    // 先判题注是否落在文字层。覆盖率过低 = 系统性缺失，此时逐条报「悬空」是错的：
    // 那不是「N 条引用错了」，而是「这一项根本查不了」。必须说清楚，而不是刷屏。
    const coverage = expected.size ? capKeys.size / expected.size : 1;
    if (expected.size >= 6 && coverage < 0.35) {
      const anchor = rfs[0] || tocs[0] || caps[0];
      add(out, {
        severity: 'medium', rule: 'xref',
        file: anchor.file, loc: `${rfs.length} refs`, snippet: anchor.snippet || '',
      }, {
        type: '题注不在文字层',
        message: `正文引用了 ${expected.size} 个不同的「${cn}」，但文字层只找到 ${capKeys.size} 条${cn}题注${tocKeys.size ? `（目录里列了 ${tocKeys.size} 条）` : ''}`,
        fix: '题注多半嵌在图片里，或用了 Word 自动题注域（域不落在正文文字里，本工具读不到）。**这一项本工具查不了，不代表没问题** —— 需要把题注落到文字层后重跑，或走人工核对。',
      }, {
        type: 'Captions not in text layer',
        message: `${expected.size} distinct ${en}s are referenced, but only ${capKeys.size} ${en} caption(s) exist in the text layer${tocKeys.size ? ` (${tocKeys.size} listed in the TOC)` : ''}`,
        fix: `Captions are most likely baked into the images or generated by Word SEQ fields — field results are not stored as body text, so this tool cannot read them. **This check could not be performed; that is not the same as passing it.** Move captions into the text layer and re-run, or verify by hand.`,
      });
      continue;
    }

    // 真·悬空：既没有题注，目录里也没有 —— 读者无论如何都找不到
    for (const r of rfs) {
      if (known.has(r.key)) continue;
      const disp = `${cn} ${r.num}`, dispEn = `${en} ${r.num}`;
      add(out, {
        severity: 'high', rule: 'xref', file: r.file, loc: r.loc, snippet: r.snippet,
      }, {
        type: '交叉引用悬空',
        message: `正文引用了 ${disp}，但既没有对应题注，目录里也没有`,
        fix: `确认 ${disp} 是被删了、改号了、还是合稿时丢了；这类错评审一翻就现。`,
      }, {
        type: 'Dangling cross-reference',
        message: `The text refers to ${dispEn}, but there is no such caption and no TOC entry either`,
        fix: `Check whether ${dispEn} was deleted, renumbered, or lost in a merge. A reviewer will hit this on the first read-through.`,
      });
    }

    // 目录列了但正文没有 —— 读者按目录翻会翻空
    const missingInBody = tocs.filter((t) => !capKeys.has(t.key));
    const uniq = [...new Map(missingInBody.map((t) => [t.key, t])).values()];
    for (const t of uniq.slice(0, 15)) {
      add(out, {
        severity: 'high', rule: 'toc', file: t.file, loc: t.loc, snippet: t.raw,
      }, {
        type: '目录有、正文无',
        message: `目录列了 ${cn} ${t.num}，但正文里找不到这条题注`,
        fix: '多半是合稿时整段被删或改了号，目录没跟着更新 —— 读者按目录翻会翻空。',
      }, {
        type: 'In TOC, missing in body',
        message: `The TOC lists ${en} ${t.num}, but no such caption exists in the body`,
        fix: 'Usually a section was deleted or renumbered and the TOC was never regenerated — readers following the TOC land on nothing.',
      });
    }
    if (uniq.length > 15) {
      add(out, {
        severity: 'high', rule: 'toc', file: uniq[0].file, loc: '—', snippet: '',
      }, {
        type: '目录有、正文无',
        message: `另有 ${uniq.length - 15} 条${cn}目录条目在正文中找不到`,
        fix: '用 --json 拿完整清单。',
      }, {
        type: 'In TOC, missing in body',
        message: `${uniq.length - 15} more ${en} TOC entries have no counterpart in the body`,
        fix: 'Use --json for the complete list.',
      });
    }

    // 正文有但目录漏了
    if (tocKeys.size >= 4) {
      const missingInToc = [...new Map(caps.filter((c) => !tocKeys.has(c.key)).map((c) => [c.key, c])).values()];
      for (const c of missingInToc.slice(0, 15)) {
        add(out, {
          severity: 'medium', rule: 'toc', file: c.file, loc: c.loc, snippet: c.snippet,
        }, {
          type: '正文有、目录无',
          message: `正文有 ${cn} ${c.num} 的题注，但目录里没列`,
          fix: '目录该重新生成/更新了。',
        }, {
          type: 'In body, missing from TOC',
          message: `${en} ${c.num} is captioned in the body but absent from the TOC`,
          fix: 'The TOC needs to be regenerated.',
        });
      }
    }
  }
}

// ── R3 章节引用悬空 ──────────────────────────────────────────────────────────
const SEC_REF_RE = /第\s*([0-9０-９一二三四五六七八九十百零]+)\s*([章节])|(?:Chapter|Section)\s+([0-9]+(?:\.[0-9]+)*)/gi;

function headingNumbers(docs) {
  const nums = new Set();
  for (const doc of docs) {
    for (const b of doc.blocks) {
      if (!b.heading) continue;
      const t = b.text.replace(/^#+\s*/, '');
      let m;
      if ((m = /^第\s*([0-9０-９一二三四五六七八九十百零]+)\s*[章篇部]/.exec(t))) {
        const v = cnToInt(m[1]); if (Number.isFinite(v)) nums.add(String(v));
      } else if ((m = /^第\s*([0-9０-９一二三四五六七八九十百零]+)\s*节/.exec(t))) {
        const v = cnToInt(m[1]); if (Number.isFinite(v)) nums.add(String(v));
      } else if ((m = /^(\d+(?:\.\d+)*)[\s.、]/.exec(t))) {
        nums.add(m[1]);
        nums.add(m[1].split('.')[0]);
      } else if ((m = /^(?:Chapter|Section|Part)\s+(\d+(?:\.\d+)*)/i.exec(t))) {
        nums.add(m[1]);
      }
    }
  }
  return nums;
}

function ruleSectionXref(docs, out) {
  const nums = headingNumbers(docs);
  if (nums.size < 2) return;   // 没识别出章节体系就不查，免得刷假红点
  for (const doc of docs) {
    for (const b of doc.blocks) {
      if (b.heading) continue;
      SEC_REF_RE.lastIndex = 0;
      let m;
      while ((m = SEC_REF_RE.exec(b.text))) {
        let val;
        if (m[1]) { const v = cnToInt(m[1]); val = Number.isFinite(v) ? String(v) : null; }
        else if (m[3]) val = m[3];
        if (!val || nums.has(val)) continue;
        const unit = m[2] === '节' ? '节' : '章';
        add(out, {
          severity: 'high', rule: 'xref',
          file: doc.file, loc: b.loc, snippet: snippet(b.text, m.index),
        }, {
          type: '章节引用悬空',
          message: `正文提到「${m[0].trim()}」，但没有编号为 ${val} 的${unit}`,
          fix: '合稿后章节顺序变了最常见；把引用改到实际章号，或补回被删的那一章。',
        }, {
          type: 'Dangling section reference',
          message: `The text refers to "${m[0].trim()}", but no ${unit === '节' ? 'section' : 'chapter'} numbered ${val} exists`,
          fix: 'Most often the chapter order changed during a merge. Point the reference at the real number, or restore the missing chapter.',
        });
      }
    }
  }
}

// ── R4 章节骨架对账 ──────────────────────────────────────────────────────────
function normTitle(t) {
  return toHalf(t)
    .replace(/^#+\s*/, '')
    .replace(/^第\s*[0-9一二三四五六七八九十百零]+\s*[章节篇部]\s*/, '')
    .replace(/^\d+(?:\.\d+)*[\s.、)]*/, '')
    .replace(/[\s:：.。、,，]/g, '')
    .toLowerCase();
}

function plainTitle(t) { return t.replace(/^#+\s*/, '').trim(); }

// 章级标题不一定是 level 1：markdown 里书名占了 #，章就落在 ##。
// 取「最浅的、出现 ≥3 次的层级」当章级，子栏目就是它下一级。
function chapterLevels(docs) {
  const counts = new Map();
  for (const doc of docs) for (const b of doc.blocks) if (b.heading) counts.set(b.level, (counts.get(b.level) || 0) + 1);
  if (!counts.size) return null;
  const levels = [...counts.keys()].sort((a, b) => a - b);
  const chap = levels.find((l) => counts.get(l) >= 3) ?? levels[0];
  return { chap, sub: chap + 1 };
}

// 返回「标准栏目」集合 —— 这些标题在多数章里重复出现是模板，不是重复错误。
function ruleSkeleton(docs, out) {
  const lv = chapterLevels(docs);
  if (!lv) return new Set();

  const chapters = [];
  for (const doc of docs) {
    let cur = null;
    for (const b of doc.blocks) {
      if (b.heading && b.level === lv.chap) {
        cur = { title: plainTitle(b.text), file: doc.file, loc: b.loc, subs: new Map() };
        chapters.push(cur);
      } else if (b.heading && b.level === lv.sub && cur) {
        const k = normTitle(b.text);
        // 展示用的栏目名去掉前导编号：「2.2 Security」→「Security」
        if (k) cur.subs.set(k, plainTitle(b.text).replace(/^\d+(?:\.\d+)*[\s.、)]*/, ''));
      }
    }
  }
  const usable = chapters.filter((c) => c.subs.size > 0);
  if (usable.length < 3) return new Set();

  const freq = new Map();
  for (const c of usable) for (const k of c.subs.keys()) freq.set(k, (freq.get(k) || 0) + 1);

  const threshold = Math.ceil(usable.length * 0.6);
  const standard = new Set();
  for (const [k, n] of freq) {
    if (n < threshold) continue;
    standard.add(k);
    if (n >= usable.length) continue;
    const label = usable.find((c) => c.subs.has(k)).subs.get(k);
    for (const c of usable) {
      if (c.subs.has(k)) continue;
      add(out, {
        severity: 'medium', rule: 'skeleton',
        file: c.file, loc: c.loc, snippet: c.title.slice(0, 46),
      }, {
        type: '章节骨架缺项',
        message: `「${c.title.slice(0, 30)}」缺栏目「${label}」（${usable.length} 章里有 ${n} 章都有）`,
        fix: '要么补这一节，要么确认本章确实不适用 —— 多人分头写的稿子这里最容易漏。',
      }, {
        type: 'Missing standard section',
        message: `"${c.title.slice(0, 30)}" has no "${label}" section (${n} of ${usable.length} chapters have one)`,
        fix: 'Either add it or confirm it genuinely does not apply here — this is the classic gap when chapters are written by different people.',
      });
    }
  }
  return standard;
}

// ── R5 术语一致性 ────────────────────────────────────────────────────────────
const STOP = new Set(['the', 'and', 'for', 'with', 'this', 'that', 'from', 'are', 'was', 'not', 'but', 'you', 'all', 'can', 'has', 'have', 'its', 'our', 'use', 'used', 'using', 'one', 'two', 'may', 'will', 'shall', 'must', 'each', 'any', 'more', 'than', 'when', 'where', 'which', 'their', 'there', 'these', 'those', 'been', 'into', 'over', 'such', 'also', 'per']);
const TERM_RE = /[A-Za-z][A-Za-z0-9+#]*(?:[ _\-][A-Za-z0-9+#]+){0,2}/g;

function ruleTerminology(docs, glossary, out) {
  // (a) 大小写 / 连字符 / 空格变体
  const groups = new Map();
  for (const doc of docs) {
    for (const b of doc.blocks) {
      TERM_RE.lastIndex = 0;
      let m;
      while ((m = TERM_RE.exec(b.text))) {
        // 掐掉首尾的虚词，否则「The AI Agent」和「the ai-agent」会被当成两个不同的词组
        let words = m[0].trim().split(/([ _\-])/).filter((x) => x !== '');
        while (words.length && STOP.has(words[0].toLowerCase())) words.splice(0, 2);
        while (words.length && STOP.has(words[words.length - 1].toLowerCase())) words.splice(-2);
        const surf = words.join('');
        if (surf.length < 3 || surf.length > 40) continue;
        words = surf.split(/[ _\-]/);
        if (words.every((w) => STOP.has(w.toLowerCase()))) continue;
        const interesting =
          /[A-Z].*[A-Z]/.test(surf) || /[0-9]/.test(surf) || /[-_]/.test(surf) ||
          (words.length > 1 && /^[A-Z]/.test(words[0]));
        if (!interesting) continue;
        const key = surf.toLowerCase().replace(/[\s_\-]/g, '');
        if (!groups.has(key)) groups.set(key, new Map());
        const g = groups.get(key);
        if (!g.has(surf)) g.set(surf, { n: 0, first: { file: doc.file, loc: b.loc, snippet: snippet(b.text, m.index) } });
        g.get(surf).n++;
      }
    }
  }
  for (const [, g] of groups) {
    const forms = [...g.entries()];
    // 两种以上写法、且合计出现 ≥3 次才报 —— 术语漂移常常是每种写法各出现一两次
    if (forms.length < 2 || forms.reduce((n, [, v]) => n + v.n, 0) < 2) continue;
    // 只差首字母大小写、且没有一个形式含内部大写 → 句首大写造成的假阳性，跳过
    const onlyFirstCase =
      forms.every(([s]) => s.slice(1) === forms[0][0].slice(1)) &&
      !forms.some(([s]) => /[a-z][A-Z]/.test(s));
    if (onlyFirstCase) continue;
    forms.sort((a, b) => b[1].n - a[1].n);
    const [main] = forms[0];
    add(out, {
      severity: 'medium', rule: 'terminology',
      file: forms[0][1].first.file, loc: forms[0][1].first.loc, snippet: forms[1][1].first.snippet,
    }, {
      type: '术语写法不一致',
      message: `同一术语出现 ${forms.length} 种写法：${forms.map(([s, v]) => `「${s}」×${v.n}`).join('、')}`,
      fix: `统一成出现最多的「${main}」，或由主编拍一个正名后全局替换。`,
    }, {
      type: 'Inconsistent term spelling',
      message: `One term is spelled ${forms.length} different ways: ${forms.map(([s, v]) => `"${s}" ×${v.n}`).join(', ')}`,
      fix: `Standardise on the most frequent form "${main}", or have the editor pick one and replace globally.`,
    });
  }

  // (b) 术语表驱动
  if (!glossary) return;
  for (const { canonical, variants } of glossary) {
    for (const v of variants) {
      for (const doc of docs) {
        for (const b of doc.blocks) {
          const at = b.text.indexOf(v);
          if (at < 0) continue;
          add(out, {
            severity: 'medium', rule: 'terminology',
            file: doc.file, loc: b.loc, snippet: snippet(b.text, at),
          }, {
            type: '违反术语表',
            message: `用了「${v}」，术语表规定的正名是「${canonical}」`,
            fix: `替换为「${canonical}」。`,
          }, {
            type: 'Glossary violation',
            message: `Uses "${v}"; the glossary's approved term is "${canonical}"`,
            fix: `Replace with "${canonical}".`,
          });
          break;   // 每个变体每份文件只报一次，避免刷屏
        }
      }
    }
  }
}

export function parseGlossary(file) {
  const out = [];
  for (const line of readFileSync(file, 'utf8').split(/\r?\n/)) {
    const t = line.trim();
    if (!t || t.startsWith('#')) continue;
    const [left, right] = t.split(/\s*[=:：]\s*/);
    if (!right) continue;
    const variants = right.split(/\s*[,，、]\s*/).map((s) => s.trim()).filter(Boolean);
    if (variants.length) out.push({ canonical: left.trim(), variants });
  }
  return out;
}

// ── R6 占位符 / 旧版残留 ─────────────────────────────────────────────────────
const RESIDUE = [
  { re: /\b(TODO|TBD|FIXME|XXX)\b/g, label: '占位符残留', sev: 'high' },
  { re: /待填|待定|待补充|此处填写|请填写|待完善/g, label: '占位符残留', sev: 'high' },
  { re: /[×xX]{3,}(?:公司|集团|有限)/g, label: '占位符残留', sev: 'high' },
  { re: /Lorem ipsum/gi, label: '占位符残留', sev: 'high' },
  { re: /【[^】]{0,10}(?:待|填|TBD|TODO)[^】]{0,10}】/g, label: '占位符残留', sev: 'high' },
];

function ruleResidue(docs, out) {
  for (const doc of docs) {
    for (const b of doc.blocks) {
      for (const r of RESIDUE) {
        r.re.lastIndex = 0;
        let m;
        while ((m = r.re.exec(b.text))) {
          add(out, {
            severity: r.sev, rule: 'residue',
            file: doc.file, loc: b.loc, snippet: snippet(b.text, m.index),
          }, {
            type: r.label,
            message: `残留「${m[0]}」`,
            fix: '定稿前必须清掉；这类字样出现在交付件里，专业度直接扣分。',
          }, {
            type: 'Leftover placeholder',
            message: `Leftover "${m[0]}"`,
            fix: 'Must be cleared before delivery — placeholders in a shipped document read as carelessness.',
          });
        }
      }
    }
  }

  // 旧版年份残留：以全文出现最多的年份为基准
  const years = new Map();
  const hits = [];
  for (const doc of docs) {
    for (const b of doc.blocks) {
      const re = /(19|20)\d{2}/g;
      let m;
      while ((m = re.exec(b.text))) {
        const y = +m[0];
        if (y < 1990 || y > 2100) continue;
        years.set(y, (years.get(y) || 0) + 1);
        hits.push({ y, doc, b, at: m.index });
      }
    }
  }
  if (years.size < 2) return;
  const dominant = [...years.entries()].sort((a, b) => b[1] - a[1])[0][0];
  const seen = new Set();
  for (const h of hits) {
    if (h.y >= dominant) continue;
    const ctx = h.b.text.slice(Math.max(0, h.at - 16), h.at + 20);
    if (!/项目|合同|标书|投标|截止|有效期|日期|年度|版本|修订/.test(ctx)) continue;
    const k = `${h.doc.file}|${h.b.loc}|${h.y}`;
    if (seen.has(k)) continue;
    seen.add(k);
    add(out, {
      severity: 'low', rule: 'residue',
      file: h.doc.file, loc: h.b.loc, snippet: snippet(h.b.text, h.at),
    }, {
      type: '疑似旧版年份',
      message: `出现 ${h.y} 年，而全文主用年份是 ${dominant}`,
      fix: '确认是引用历史事实，还是从上一版复制过来忘了改 —— 后者在标书里是致命错。',
    }, {
      type: 'Suspected stale year',
      message: `Mentions ${h.y} while the document's dominant year is ${dominant}`,
      fix: 'Confirm this is a historical fact and not copy-paste from last year\'s version — in a bid, the latter is fatal.',
    });
  }
}

// ── R7 标题重复 ──────────────────────────────────────────────────────────────
function ruleDupHeading(docs, standard, out) {
  const seen = new Map();
  for (const doc of docs) {
    for (const b of doc.blocks) {
      if (!b.heading) continue;
      const norm = normTitle(b.text);
      if (!norm) continue;
      // 「学习目标 / 教学内容 / 课后作业」这类每章都有的模板栏目是对的，不是重复错误
      if (standard.has(norm)) continue;
      const k = `${b.level}|${norm}`;
      if (!seen.has(k)) seen.set(k, []);
      seen.get(k).push({ doc, b });
    }
  }
  for (const [, list] of seen) {
    if (list.length < 2) continue;
    const title = plainTitle(list[0].b.text);
    const { file, loc } = spread(list.map((x) => ({ file: x.doc.file, loc: x.b.loc })));
    add(out, {
      severity: 'low', rule: 'skeleton', file, loc, snippet: title.slice(0, 46),
    }, {
      type: '标题重复',
      message: `同级标题「${title.slice(0, 30)}」出现 ${list.length} 次`,
      fix: '目录里会并成两条一样的，评审翻不到想看的那节。加限定词区分。',
    }, {
      type: 'Duplicate heading',
      message: `Same-level heading "${title.slice(0, 30)}" appears ${list.length} times`,
      fix: 'The TOC will show two identical entries and reviewers cannot tell them apart. Add a qualifier.',
    });
  }
}

// ── R8 合稿丢段（需 --baseline）────────────────────────────────────────────────
function ruleMergeDiff(docs, baseDocs, out) {
  const cur = new Set();
  for (const d of docs) for (const b of d.blocks) if (b.text.length >= 20) cur.add(normTitle(b.text) || b.text);
  const lost = [];
  for (const d of baseDocs) {
    for (const b of d.blocks) {
      if (b.text.length < 20) continue;
      const k = normTitle(b.text) || b.text;
      if (!cur.has(k)) lost.push({ d, b });
    }
  }
  const shown = lost.slice(0, 50);
  for (const l of shown) {
    add(out, {
      severity: 'medium', rule: 'merge',
      file: l.d.file, loc: `base ${l.b.loc}`, snippet: l.b.text.slice(0, 46),
    }, {
      type: '合稿疑似丢段',
      message: '基准稿里有这一段，当前稿里找不到',
      fix: '确认是有意删除还是合稿漏了 —— 三个人各写一份合成一份时，这里最容易出事。',
    }, {
      type: 'Paragraph lost in merge',
      message: 'Present in the baseline, absent from the current draft',
      fix: 'Confirm it was deleted on purpose rather than dropped during the merge — this is where three-way merges go wrong.',
    });
  }
  if (lost.length > shown.length) {
    add(out, {
      severity: 'medium', rule: 'merge', file: baseDocs[0].file, loc: '—', snippet: '',
    }, {
      type: '合稿疑似丢段',
      message: `另有 ${lost.length - shown.length} 段同类问题未逐条列出`,
      fix: '用 --json 拿完整清单。',
    }, {
      type: 'Paragraph lost in merge',
      message: `${lost.length - shown.length} more paragraphs are missing but not listed individually`,
      fix: 'Use --json for the complete list.',
    });
  }
}

// ── entry ────────────────────────────────────────────────────────────────────
export function runRules(docs, { glossary = null, baseDocs = null } = {}) {
  const out = [];
  const { captions, refs, tocLabels } = collectLabels(docs);
  // 目录区不参与正文类检查（术语、占位符、标题、骨架都不该把目录算进去）
  const body = docs.map((d) => ({ ...d, blocks: d.blocks.filter((b) => !b.toc) }));

  ruleNumbering(captions, out);
  ruleLabelIntegrity(captions, refs, tocLabels, out);
  ruleSectionXref(body, out);
  const standard = ruleSkeleton(body, out);
  ruleTerminology(body, glossary, out);
  ruleResidue(body, out);
  ruleDupHeading(body, standard, out);
  if (baseDocs) ruleMergeDiff(body, baseDocs.map((d) => ({ ...d, blocks: d.blocks.filter((b) => !b.toc) })), out);

  out.sort((a, b) => SEV[a.severity] - SEV[b.severity] || a.file.localeCompare(b.file) || a.type.localeCompare(b.type));
  out.forEach((f, i) => { f.id = i + 1; });
  return {
    findings: out,
    stats: {
      captions: captions.length,
      refs: refs.length,
      tocEntries: tocLabels.length,
      tocBlocks: docs.reduce((n, d) => n + (d.tocBlocks || 0), 0),
    },
  };
}
