#!/usr/bin/env node
/**
 * ai_smell_scan.cjs
 *
 * Lightweight scanner for common "LLM fingerprints" in zh/en/ja text.
 * - Not a detector. This is a heuristic linter to guide rewriting.
 * - Treat results as "where it looks templated", not "proof it's AI".
 * - Outputs a compact, LLM-friendly report.
 */

const fs = require("fs");

function parseArgs(argv) {
  const out = { lang: "auto", file: null, logfile: null };
  for (let i = 2; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--lang") out.lang = argv[++i] || "auto";
    else if (a === "--logfile") out.logfile = argv[++i] || null;
    else if (!a.startsWith("--") && !out.file) out.file = a;
  }
  return out;
}

function readStdin() {
  return new Promise((resolve, reject) => {
    let data = "";
    process.stdin.setEncoding("utf8");
    process.stdin.on("data", (c) => (data += c));
    process.stdin.on("end", () => resolve(data));
    process.stdin.on("error", reject);
  });
}

function guessLang(text) {
  // Very rough: pick the dominant script.
  const hasJa = /[\u3040-\u30ff\u31f0-\u31ff]/.test(text); // Hiragana/Katakana
  const hasZh = /[\u4e00-\u9fff]/.test(text); // CJK Unified (also used by JA)
  const hasEn = /[A-Za-z]/.test(text);
  if (hasJa) return "ja";
  if (hasZh && !hasEn) return "zh";
  if (hasEn && !hasZh) return "en";
  if (hasZh && hasEn) return "zh";
  return "en";
}

function findMatches(text, regex, max = 6) {
  const re = new RegExp(regex.source, regex.flags.includes("g") ? regex.flags : `${regex.flags}g`);
  const out = [];
  let m;
  while ((m = re.exec(text)) && out.length < max) {
    const idx = m.index;
    const start = Math.max(0, idx - 24);
    const end = Math.min(text.length, idx + m[0].length + 24);
    out.push({
      match: m[0],
      context: text.slice(start, end).replace(/\s+/g, " ").trim(),
    });
  }
  return out;
}

function countRegex(text, regex) {
  const re = new RegExp(regex.source, regex.flags.includes("g") ? regex.flags : `${regex.flags}g`);
  const ms = text.match(re);
  return ms ? ms.length : 0;
}

function buildRules(lang) {
  const common = [
    {
      id: "format.bold_excess",
      label: "Excessive bold markers (format fingerprint)",
      re: /\*\*[^*]+\*\*/g,
      scoreHint: (t) => (countRegex(t, /\*\*[^*]+\*\*/g) >= 8 ? 2 : 0),
    },
    {
      id: "format.list_excess",
      label: "List-heavy formatting (many bullet lines)",
      re: /^(?:\s*[-*•]\s+.+)$/gm,
      scoreHint: (t) => (countRegex(t, /^(?:\s*[-*•]\s+.+)$/gm) >= 10 ? 2 : 0),
    },
    {
      id: "format.headings",
      label: "Markdown headings (## / ### ...)",
      re: /^\s*#{1,6}\s+\S.+$/gm,
      scoreHint: (t) => (countRegex(t, /^\s*#{1,6}\s+\S.+$/gm) >= 4 ? 2 : 0),
    },
    {
      id: "format.hr",
      label: "Markdown horizontal rules (---)",
      re: /^\s*-{3,}\s*$/gm,
      scoreHint: (t) => (countRegex(t, /^\s*-{3,}\s*$/gm) >= 3 ? 2 : 0),
    },
    {
      id: "format.emoji_dense",
      label: "Emoji/Unicode decorative density",
      // Heuristic: many pictographic chars often comes from template-based "pretty layout"
      re: /\p{Extended_Pictographic}/gu,
      scoreHint: (t) => (countRegex(t, /\p{Extended_Pictographic}/gu) >= 12 ? 2 : 0),
    },
  ];

  if (lang === "zh") {
    return common.concat([
      { id: "zh.signpost", label: "Template signposting", re: /(首先|其次|最后|综上所述|总而言之|总的来说|值得注意的是|不可忽视的是)/g },
      { id: "zh.buzzwords", label: "Buzzwords / big empty nouns", re: /(赋能|闭环|抓手|底层逻辑|赛道|生态|矩阵|方法论|降维|重塑|范式|加持|破圈|全链路|系统性|高质量发展)/g },
      {
        id: "zh.promo",
        label: "Promotional / inflated significance tone",
        re: /(里程碑|标志着|见证(了)?|引领|重磅|史诗级|划时代|颠覆|重塑格局|开启(了)?新(的)?时代|具有(重大|重要)意义|必将)/g,
      },
      {
        id: "zh.weasel",
        label: "Weasel attribution (vague authority)",
        re: /(有观点认为|有人认为|业内人士|有研究(表明|指出)|研究表明|数据显示|据(统计|报道)|权威机构(指出|认为)|专家(表示|指出)|大量实践证明)/g,
      },
      {
        id: "zh.negation_parallel",
        label: "Overuse: 不是…而是 / 不仅…(更/而且)… / 不再…而是…",
        re: /(不是[^。！？\n]{0,40}而是|不仅[^。！？\n]{0,40}(更|而且)|不再[^。！？\n]{0,40}而是)/g,
      },
      { id: "zh.core_key", label: "Overuse: 核心/关键/本质", re: /(核心|关键|本质|要点|重点)/g },
      { id: "zh.over_empathy", label: "Over-soft empathy / customer-service tone", re: /(我(懂你|理解你)|稳稳地接住你|辛苦了|不容易)/g },
      { id: "zh.helpful_close", label: "Over-helpful closing", re: /(希望对你有帮助|如果你愿意我也可以|如有需要我可以继续)/g },
      { id: "zh.dash", label: "Overuse of em dash", re: /——/g },
      { id: "zh.quote_marks", label: "Dense quote marks", re: /[“”‘’]/g },
    ]);
  }

  if (lang === "ja") {
    return common.concat([
      { id: "ja.signpost", label: "Template signposting", re: /(まず|次に|最後に|結論として|まとめると|重要なのは|ポイントは)/g },
      { id: "ja.core_key", label: "Overuse: 重要/本質/鍵/ポイント", re: /(重要|本質|鍵|ポイント)/g },
      { id: "ja.desumasu", label: "Many です。/ます。 endings (monotone)", re: /(です。|ます。)/g },
      { id: "ja.can_do", label: "Overuse: 〜することができます", re: /することができます/g },
      { id: "ja.passive", label: "Passive/impersonal templates", re: /(求められ(る|ます)|必要がある|推奨され(る|ます)|と言えるでしょう|と考えられ(る|ます))/g },
      { id: "ja.abstract", label: "Vague quantifiers / abstract words", re: /(様々な|多くの|いくつか|一定の|適切な|効果的な|このような|そのような)/g },
      { id: "ja.preface", label: "Long prefaces / empty openers", re: /(現代社会において|近年|周知の通り)/g },
      { id: "ja.hearsay", label: "Hearsay / vague evidence", re: /(研究によると|データによれば|と言われています)/g },
    ]);
  }

  // en
  return common.concat([
    { id: "en.transitions", label: "Stock transitions", re: /\b(Moreover|Additionally|Furthermore|Therefore|Thus|Hence|Nevertheless|Nonetheless)\b/g },
    { id: "en.signpost", label: "Template signposting", re: /\b(In conclusion|In summary|Overall|Firstly|Secondly|Lastly)\b/g },
    { id: "en.preface", label: "Over-prefacing", re: /\b(It is important to note that|It's important to note that|This is not an exhaustive list)\b/g },
    { id: "en.corp", label: "Corporate filler", re: /\b(robust|comprehensive|leverage|synergy|optimi[sz]e|streamline)\b/g },
    {
      id: "en.inflated",
      label: "Inflated significance / promo tone",
      re: /\b(testament|underscores? (its )?importance|plays? a vital role|watershed moment|pivotal|must-?see|breathtaking|captivating|rich (cultural )?(heritage|tapestry))\b/gi,
    },
    {
      id: "en.weasel",
      label: "Weasel attribution",
      re: /\b(studies show|research suggests|experts say|industry reports suggest|observers note|many believe)\b/gi,
    },
    {
      id: "en.negation_parallel",
      label: "Parallel negation / contrast templates",
      re: /\b(it'?s not .*?, it'?s .*?|not only .*? but also)\b/gi,
    },
    {
      id: "en.ing_tail",
      label: "Present-participle pseudo-analysis tails",
      re: /\b(ensuring|highlighting|emphasizing|reflecting|improving|enabling)\b/gi,
    },
    { id: "en.helpful", label: "Over-helpful closing", re: /\b(I hope this helps|Hope this helps)\b/g },
    { id: "en.polite_open", label: "Template polite opening", re: /\b(Certainly|Of course|Absolutely|I'd be happy to)\b/g },
  ]);
}

function score(rule, text) {
  if (typeof rule.scoreHint === "function") return rule.scoreHint(text);
  const c = countRegex(text, rule.re);
  if (c >= 8) return 2;
  if (c >= 3) return 1;
  return 0;
}

async function main() {
  try {
    const args = parseArgs(process.argv);
    const text = args.file ? fs.readFileSync(args.file, "utf8") : await readStdin();
    const lang = args.lang === "auto" ? guessLang(text) : args.lang;
    const rules = buildRules(lang);

    const findings = [];
    for (const r of rules) {
      const cnt = countRegex(text, r.re);
      if (!cnt) continue;
      findings.push({
        id: r.id,
        label: r.label,
        count: cnt,
        score: score(r, text),
        samples: findMatches(text, r.re, 3),
      });
    }

    findings.sort((a, b) => (b.score - a.score) || (b.count - a.count));

    const top = findings.slice(0, 10);
    const scoreTotal = top.reduce((s, f) => s + f.score, 0);

    const report = {
      lang,
      length: text.length,
      disclaimer:
        "This is a heuristic linter for templated style/fingerprints, not an AI detector. Treat findings as edit hints, not proof of authorship or factuality.",
      how_to_use: [
        "Look for clusters (multiple patterns) rather than any single match.",
        "In structured genres (PRDs, reports, FAQs), formatting matches may be expected; judge by context.",
        "Use Hallucination Gate separately for sources, numbers, and claims.",
      ],
      // Lightweight log of detected "AI flavor" points for easy downstream review.
      // Note: this is intentionally derived from the top findings only to keep output compact.
      log: top.map((f) => ({
        id: f.id,
        label: f.label,
        count: f.count,
        examples: (f.samples || []).map((s) => s.context),
      })),
      log_truncated: findings.length > top.length,
      findings: top,
      hint:
        scoreTotal >= 10
          ? "High template/LLM fingerprint density. Consider re-structuring + adding concrete specifics."
          : scoreTotal >= 5
            ? "Medium fingerprint density. Target the top 2-3 patterns and improve specificity/voice."
            : "Low fingerprint density. Focus on clarity and factual accuracy, not 'de-AI-ing'.",
    };

    // Optional persistent logging (JSONL). Disabled by default to avoid privacy surprises.
    if (args.logfile) {
      const entry = {
        ts: new Date().toISOString(),
        lang: report.lang,
        length: report.length,
        hint: report.hint,
        top: report.findings.map((f) => ({ id: f.id, count: f.count, score: f.score })),
      };
      try {
        fs.appendFileSync(args.logfile, JSON.stringify(entry) + "\n", "utf8");
        report.log_written_to = args.logfile;
      } catch (e) {
        // Never fail the scan because logging failed.
        process.stderr.write(
          `Warning: failed to write logfile "${args.logfile}": ${e && e.message ? e.message : String(e)}\n`,
        );
      }
    }

    process.stdout.write(JSON.stringify(report, null, 2) + "\n");
  } catch (err) {
    process.stderr.write(`Failure: ${err && err.message ? err.message : String(err)}\n`);
    process.exit(1);
  }
}

main();
