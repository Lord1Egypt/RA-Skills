import { tokenize as _utilTokenize } from "./memory-utils.ts";
import { DATA_DIR, loadJson, debouncedSave } from "./persistence.ts";
import { resolve } from "path";
import { existsSync, readFileSync } from "fs";
const ASSOC_PATH = resolve(DATA_DIR, "aam_associations.json");
function detectLanguage(text) {
  const cjk = (text.match(/[\u4e00-\u9fff]/g) || []).length;
  const latin = (text.match(/[a-zA-Z]/g) || []).length;
  if (cjk > latin * 0.3) return "zh";
  return "en";
}
const networks = /* @__PURE__ */ new Map();
function cooccurPath(lang) {
  return resolve(DATA_DIR, `aam_cooccur_${lang}.json`);
}
function synonymsPath(lang) {
  return resolve(DATA_DIR, `aam_synonyms_${lang}.json`);
}
function getNetwork(lang) {
  if (!networks.has(lang)) {
    const p = cooccurPath(lang);
    networks.set(lang, loadJson(p, {
      cooccur: {},
      df: {},
      totalDocs: 0,
      lastRebuild: 0
    }));
    if (lang !== "zh" && lang !== "en") {
      const sp = synonymsPath(lang);
      if (!existsSync(sp)) {
        generateSynonymSeed(lang).catch(() => {
        });
      }
    }
  }
  return networks.get(lang);
}
function migrateOldAssociations() {
  if (!existsSync(ASSOC_PATH)) return;
  const zhPath = cooccurPath("zh");
  if (existsSync(zhPath)) return;
  try {
    const old = loadJson(ASSOC_PATH, { cooccur: {}, df: {}, totalDocs: 0, lastRebuild: 0 });
    if (old.totalDocs > 0) {
      networks.set("zh", old);
      debouncedSave(zhPath, old);
      console.log(`[cc-soul][aam] migrated legacy aam_associations.json \u2192 aam_cooccur_zh.json (${old.totalDocs} docs)`);
    }
  } catch {
  }
}
migrateOldAssociations();
let _currentLang = "zh";
function network() {
  return getNetwork(_currentLang);
}
const TEMPORAL_PATH = resolve(DATA_DIR, "aam_temporal.json");
const TEMPORAL_MAX_ENTRIES = 1e3;
let _temporalNet = loadJson(TEMPORAL_PATH, { directed: {} });
let _prevMessageWords = [];
const _TEMPORAL_EN_STOPS = /* @__PURE__ */ new Set([
  "the",
  "is",
  "are",
  "was",
  "were",
  "be",
  "been",
  "being",
  "have",
  "has",
  "had",
  "do",
  "does",
  "did",
  "will",
  "would",
  "could",
  "should",
  "can",
  "may",
  "might",
  "what",
  "when",
  "where",
  "which",
  "who",
  "whom",
  "how",
  "why",
  "that",
  "this",
  "these",
  "those",
  "it",
  "its",
  "and",
  "but",
  "or",
  "not",
  "no",
  "yes",
  "to",
  "of",
  "in",
  "on",
  "at",
  "by",
  "for",
  "with",
  "from",
  "about",
  "very",
  "just",
  "also",
  "too",
  "so",
  "then",
  "than",
  "now"
]);
function learnTemporalLink(currentContent) {
  const words = filterStopWords(tokenize(currentContent));
  const unique = [...new Set(words)].filter((w) => !isJunkToken(w) && !_TEMPORAL_EN_STOPS.has(w.toLowerCase()));
  if (_prevMessageWords.length > 0 && unique.length > 0) {
    for (const prev of _prevMessageWords) {
      if (!_temporalNet.directed[prev]) _temporalNet.directed[prev] = {};
      for (const curr of unique) {
        if (prev === curr) continue;
        _temporalNet.directed[prev][curr] = (_temporalNet.directed[prev][curr] || 0) + 1;
      }
    }
    const totalEntries = Object.keys(_temporalNet.directed).length;
    if (totalEntries > TEMPORAL_MAX_ENTRIES) {
      const entries = Object.entries(_temporalNet.directed).map(([w, succs]) => ({ word: w, total: Object.values(succs).reduce((a, b) => a + b, 0) })).sort((a, b) => a.total - b.total);
      const toRemove = totalEntries - TEMPORAL_MAX_ENTRIES + 100;
      for (let i = 0; i < toRemove && i < entries.length; i++) {
        delete _temporalNet.directed[entries[i].word];
      }
    }
    if (network().totalDocs % 20 === 0) {
      debouncedSave(TEMPORAL_PATH, _temporalNet);
    }
  }
  _prevMessageWords = unique.slice(0, 10);
}
function getTemporalSuccessors(word, topK = 5) {
  const succs = _temporalNet.directed[word];
  if (!succs) return [];
  return Object.entries(succs).sort(([, a], [, b]) => b - a).slice(0, topK).map(([w, c]) => ({ word: w, count: c }));
}
function decayTemporalLinks() {
  let pruned = 0;
  for (const [w, succs] of Object.entries(_temporalNet.directed)) {
    for (const [w2, count] of Object.entries(succs)) {
      const newCount = count * 0.98;
      if (newCount < 0.5) {
        delete succs[w2];
        pruned++;
      } else succs[w2] = newCount;
    }
    if (Object.keys(succs).length === 0) delete _temporalNet.directed[w];
  }
  if (pruned > 0) debouncedSave(TEMPORAL_PATH, _temporalNet);
}
const SYNONYMS_PATH = resolve(DATA_DIR, "aam_synonyms.json");
const _defaultSynonyms = {
  "\u5F00\u5FC3": ["\u9AD8\u5174", "\u5FEB\u4E50", "\u6109\u5FEB", "\u5FC3\u60C5\u597D", "happy"],
  "\u9AD8\u5174": ["\u5F00\u5FC3", "\u5FEB\u4E50", "\u6109\u5FEB"],
  "\u96BE\u8FC7": ["\u4F24\u5FC3", "\u96BE\u53D7", "\u4E0D\u5F00\u5FC3", "\u5FC3\u60C5\u5DEE", "sad"],
  "\u751F\u6C14": ["\u6124\u6012", "\u53D1\u706B", "\u607C\u706B", "angry"],
  "\u5BB3\u6015": ["\u6050\u60E7", "\u62C5\u5FC3", "\u7126\u8651", "\u7D27\u5F20"],
  "\u559C\u6B22": ["\u7231", "\u504F\u597D", "\u4E2D\u610F", "\u559C\u7231"],
  "\u8BA8\u538C": ["\u4E0D\u559C\u6B22", "\u70E6", "\u53D7\u4E0D\u4E86", "\u53CD\u611F"],
  "\u5403": ["\u996E\u98DF", "\u98DF\u7269", "\u9910", "\u83DC", "\u7F8E\u98DF", "\u96F6\u98DF"],
  "\u51CF\u80A5": ["\u7626\u8EAB", "\u5065\u8EAB", "\u4F53\u91CD", "\u5361\u8DEF\u91CC", "\u8282\u98DF"],
  "\u5DE5\u4F5C": ["\u4E0A\u73ED", "\u529E\u516C", "\u804C\u573A", "\u516C\u53F8", "\u52A0\u73ED"],
  "\u5B66\u4E60": ["\u8BFB\u4E66", "\u5B66", "\u8BFE\u7A0B", "\u6559\u7A0B", "\u77E5\u8BC6"],
  "\u4EE3\u7801": ["\u7F16\u7A0B", "\u5F00\u53D1", "\u5199\u4EE3\u7801", "\u7A0B\u5E8F"],
  "\u7761\u89C9": ["\u7761\u7720", "\u5931\u7720", "\u4F11\u606F", "\u65E9\u7761", "\u71AC\u591C"],
  "\u8FD0\u52A8": ["\u953B\u70BC", "\u5065\u8EAB", "\u8DD1\u6B65", "\u6E38\u6CF3", "\u7BEE\u7403", "\u8DB3\u7403", "\u7FBD\u6BDB\u7403", "\u4E52\u4E53\u7403", "\u7F51\u7403", "\u745C\u4F3D"],
  "\u65C5\u884C": ["\u65C5\u6E38", "\u51FA\u884C", "\u51FA\u5DEE", "\u5EA6\u5047"],
  "\u7535\u5F71": ["\u5F71\u7247", "\u770B\u7535\u5F71", "\u5F71\u9662"],
  "\u97F3\u4E50": ["\u6B4C", "\u542C\u6B4C", "\u5531\u6B4C"],
  "\u4E70": ["\u8D2D\u4E70", "\u9009\u8D2D", "\u5165\u624B", "\u4E0B\u5355"],
  "\u8D35": ["\u4EF7\u683C\u9AD8", "\u4E0D\u4FBF\u5B9C", "\u6602\u8D35"],
  "\u4FBF\u5B9C": ["\u5B9E\u60E0", "\u6027\u4EF7\u6BD4", "\u5212\u7B97"],
  "\u597D": ["\u4E0D\u9519", "\u68D2", "\u4F18\u79C0", "\u725B"],
  "\u5DEE": ["\u70C2", "\u5783\u573E", "\u4E0D\u884C", "\u7CDF\u7CD5"],
  "\u5FEB": ["\u8FC5\u901F", "\u6548\u7387\u9AD8", "\u901F\u5EA6\u5FEB"],
  "\u6162": ["\u7F13\u6162", "\u6548\u7387\u4F4E", "\u5361\u987F"],
  "\u5927": ["\u5E9E\u5927", "\u5DE8\u5927", "\u5F88\u591A"],
  "\u5C0F": ["\u5FAE\u5C0F", "\u5F88\u5C11", "\u4E0D\u591A"],
  "Python": ["python", "py", "pip"],
  "JavaScript": ["js", "node", "npm", "typescript", "ts"],
  "Docker": ["docker", "\u5BB9\u5668", "container", "k8s"],
  "Git": ["git", "github", "gitlab", "\u7248\u672C\u63A7\u5236"],
  "Linux": ["linux", "ubuntu", "centos", "shell", "bash"],
  "API": ["api", "\u63A5\u53E3", "\u8BF7\u6C42", "http", "rest"],
  "\u6570\u636E\u5E93": ["sql", "mysql", "postgres", "redis", "mongo", "sqlite"],
  "\u9762\u8BD5": ["interview", "\u7B80\u5386", "\u6C42\u804C", "offer"],
  "\u623F\u5B50": ["\u79DF\u623F", "\u4E70\u623F", "\u623F\u4EF7", "\u88C5\u4FEE"],
  "\u8F66": ["\u6C7D\u8F66", "\u8F7F\u8F66", "SUV", "\u7535\u52A8\u8F66", "\u4E70\u8F66", "\u5F00\u8F66"],
  "\u4E70\u8F66": ["\u8D2D\u8F66", "\u63D0\u8F66", "\u9009\u8F66", "\u8BD5\u9A7E", "4S\u5E97"],
  "\u5B69\u5B50": ["\u5C0F\u5B69", "\u5B9D\u5B9D", "\u80B2\u513F", "\u6559\u80B2"],
  "\u8001\u5A46": ["\u8001\u516C", "\u5BF9\u8C61", "\u4F34\u4FA3", "\u7231\u4EBA"],
  "\u94B1": ["\u6536\u5165", "\u5DE5\u8D44", "\u82B1\u8D39", "\u9884\u7B97", "\u5B58\u6B3E"],
  "\u8EAB\u4F53": ["\u5065\u5EB7", "\u4F53\u68C0", "\u751F\u75C5", "\u533B\u9662"],
  // ── 情感表达（50组）──────────────────────────────────────────────────
  "\u6109\u5FEB": ["\u6109\u60A6", "\u8212\u7545", "\u5FC3\u65F7\u795E\u6021", "pleasant"],
  "\u5E78\u798F": ["\u7F8E\u6EE1", "\u5E78\u8FD0", "\u6EE1\u8DB3", "\u751C\u871C", "happiness"],
  "\u5174\u594B": ["\u6FC0\u52A8", "\u4EA2\u594B", "\u70ED\u8840\u6CB8\u817E", "excited"],
  "\u60CA\u559C": ["\u610F\u5916", "\u60CA\u8BB6", "\u60CA\u8273", "surprise"],
  "\u611F\u52A8": ["\u52A8\u5BB9", "\u89E6\u52A8", "\u6696\u5FC3", "\u6CEA\u76EE"],
  "\u6EE1\u8DB3": ["\u6EE1\u610F", "\u77E5\u8DB3", "\u5FC3\u6EE1\u610F\u8DB3", "satisfied"],
  "\u81EA\u4FE1": ["\u5E95\u6C14", "\u6709\u628A\u63E1", "\u4FE1\u5FC3\u5341\u8DB3", "confident"],
  "\u9A84\u50B2": ["\u81EA\u8C6A", "\u5F97\u610F", "\u8363\u8000", "proud"],
  "\u671F\u5F85": ["\u76FC\u671B", "\u61A7\u61AC", "\u7FD8\u9996\u4EE5\u76FC", "\u671F\u671B"],
  "\u611F\u6069": ["\u611F\u8C22", "\u8C22\u8C22", "\u611F\u6FC0", "grateful"],
  "\u8F7B\u677E": ["\u653E\u677E", "\u8212\u9002", "\u81EA\u5728", "\u65E0\u538B\u529B"],
  "\u5E73\u9759": ["\u5B89\u5B81", "\u5B81\u9759", "\u6DE1\u5B9A", "\u5FC3\u5982\u6B62\u6C34"],
  "\u52C7\u6562": ["\u80C6\u5927", "\u65E0\u754F", "\u6709\u80C6\u91CF", "brave"],
  "\u6E29\u6696": ["\u6696", "\u6696\u5FC3", "\u6E29\u99A8", "warm"],
  "\u5584\u826F": ["\u597D\u5FC3", "\u5584\u610F", "\u5FC3\u5730\u597D", "kind"],
  "\u4F24\u5FC3": ["\u60B2\u4F24", "\u5FC3\u788E", "\u5FC3\u75DB", "\u96BE\u8FC7", "heartbroken"],
  "\u6124\u6012": ["\u66B4\u6012", "\u6C14\u70B8", "\u6012\u706B", "\u706B\u5927", "furious"],
  "\u6050\u60E7": ["\u5BB3\u6015", "\u80C6\u602F", "\u60CA\u6050", "fear"],
  "\u7126\u8651": ["\u7D27\u5F20", "\u4E0D\u5B89", "\u62C5\u5FE7", "\u5FC3\u614C", "anxiety"],
  "\u65E0\u804A": ["\u6CA1\u610F\u601D", "\u4E4F\u5473", "\u67AF\u71E5", "boring"],
  "\u75B2\u60EB": ["\u7D2F", "\u7CBE\u75B2\u529B\u5C3D", "\u7B4B\u75B2\u529B\u5C3D", "\u4F53\u529B\u4E0D\u652F"],
  "\u70E6\u8E81": ["\u70E6", "\u5FC3\u70E6", "\u4E0D\u8010\u70E6", "\u70E6\u6B7B\u4E86", "annoyed"],
  "\u5C34\u5C2C": ["\u96BE\u4E3A\u60C5", "\u7A98\u8FEB", "\u4E22\u8138", "embarrassed"],
  "\u5B64\u72EC": ["\u5BC2\u5BDE", "\u5F62\u5355\u5F71\u53EA", "\u4E00\u4E2A\u4EBA", "lonely"],
  "\u5931\u671B": ["\u5FC3\u7070\u610F\u51B7", "\u6CC4\u6C14", "\u7070\u5FC3", "disappointed"],
  "\u540E\u6094": ["\u61CA\u6094", "\u8FFD\u6094", "\u6094\u6068", "\u4E0D\u8BE5", "regret"],
  "\u5AC9\u5992": ["\u773C\u7EA2", "\u7FA1\u6155\u5AC9\u5992\u6068", "\u5992\u5FCC", "jealous"],
  "\u5185\u759A": ["\u6127\u759A", "\u81EA\u8D23", "\u8FC7\u610F\u4E0D\u53BB", "guilty"],
  "\u4E0D\u5B89": ["\u5FD0\u5FD1", "\u60F6\u6050", "\u5FC3\u795E\u4E0D\u5B81", "uneasy"],
  "\u60B2\u89C2": ["\u6D88\u6781", "\u7070\u5FC3", "\u770B\u4E0D\u5230\u5E0C\u671B", "pessimistic"],
  "\u7EDD\u671B": ["\u65E0\u671B", "\u8D70\u6295\u65E0\u8DEF", "\u4E07\u5FF5\u4FF1\u7070", "hopeless"],
  "\u59D4\u5C48": ["\u53D7\u59D4\u5C48", "\u51A4\u6789", "\u5FC3\u9178", "\u618B\u5C48"],
  "\u5D29\u6E83": ["\u53D7\u4E0D\u4E86", "\u7EF7\u4E0D\u4F4F", "\u7CBE\u795E\u5D29\u6E83", "breakdown"],
  "\u6291\u90C1": ["\u90C1\u95F7", "\u6D88\u6C89", "\u4F4E\u843D", "depression"],
  "\u8FF7\u832B": ["\u56F0\u60D1", "\u4E0D\u77E5\u6240\u63AA", "\u832B\u7136", "confused"],
  "\u7EA0\u7ED3": ["\u72B9\u8C6B", "\u4E3E\u68CB\u4E0D\u5B9A", "\u5DE6\u53F3\u4E3A\u96BE", "\u62FF\u4E0D\u5B9A\u4E3B\u610F"],
  "\u7FA1\u6155": ["\u773C\u7EA2", "\u5411\u5F80", "\u771F\u597D", "envy"],
  "\u91CA\u7136": ["\u653E\u4E0B", "\u60F3\u5F00\u4E86", "\u770B\u5F00\u4E86", "\u91CA\u6000"],
  "\u6000\u5FF5": ["\u60F3\u5FF5", "\u601D\u5FF5", "\u6302\u5FF5", "miss"],
  "\u62C5\u5FC3": ["\u64CD\u5FC3", "\u5FE7\u8651", "\u6302\u5FC3", "worry"],
  "\u60ED\u6127": ["\u7F9E\u6127", "\u65E0\u5730\u81EA\u5BB9", "\u6C57\u989C"],
  "\u6CAE\u4E27": ["\u9893\u5E9F", "\u6D88\u6C89", "\u4F4E\u843D", "dejected"],
  "\u538C\u5026": ["\u817B\u4E86", "\u53D7\u591F\u4E86", "\u538C\u70E6", "tired of"],
  "\u9707\u60CA": ["\u5403\u60CA", "\u76EE\u77AA\u53E3\u5446", "\u96BE\u4EE5\u7F6E\u4FE1", "shocked"],
  "\u7F9E\u803B": ["\u4E22\u4EBA", "\u53EF\u803B", "\u6CA1\u8138", "shame"],
  "\u6050\u614C": ["\u614C\u5F20", "\u516D\u795E\u65E0\u4E3B", "\u624B\u5FD9\u811A\u4E71", "panic"],
  "\u6B23\u6170": ["\u5B89\u6170", "\u5BBD\u6170", "\u653E\u5FC3"],
  "\u6FC0\u52A8": ["\u70ED\u6CEA\u76C8\u7736", "\u5FC3\u6F6E\u6F8E\u6E43", "\u60C5\u7EEA\u9AD8\u6DA8"],
  "\u5FC3\u75BC": ["\u5FC3\u75DB", "\u820D\u4E0D\u5F97", "\u601C\u60DC", "\u75BC\u60DC"],
  // ── 日常生活（80组）──────────────────────────────────────────────────
  "\u559D": ["\u996E", "\u559D\u6C34", "\u996E\u6599", "\u559D\u9152"],
  "\u7761": ["\u7761\u89C9", "\u5165\u7761", "\u8EBA\u4E0B", "\u4F11\u606F"],
  "\u8D70": ["\u6B65\u884C", "\u8D70\u8DEF", "\u6563\u6B65", "\u6E9C\u8FBE"],
  "\u8DD1": ["\u8DD1\u6B65", "\u6162\u8DD1", "\u51B2\u523A", "run", "jogging"],
  "\u5750": ["\u5750\u4E0B", "\u5C31\u5750", "\u843D\u5EA7"],
  "\u7AD9": ["\u7AD9\u7ACB", "\u7AD9\u8D77\u6765", "\u8D77\u7ACB"],
  "\u770B": ["\u89C2\u770B", "\u77A7", "\u7785", "\u6CE8\u89C6", "\u76EF"],
  "\u542C": ["\u503E\u542C", "\u542C\u5230", "\u8046\u542C"],
  "\u8BF4": ["\u8BB2", "\u544A\u8BC9", "\u8BF4\u8BDD", "\u804A"],
  "\u5199": ["\u4E66\u5199", "\u64B0\u5199", "\u5199\u4F5C", "\u7801\u5B57"],
  "\u8BFB": ["\u9605\u8BFB", "\u770B\u4E66", "\u6717\u8BFB", "\u8BFB\u4E66"],
  "\u6D17": ["\u6E05\u6D17", "\u6D17\u6DA4", "\u51B2\u6D17", "\u6D17\u6FA1"],
  "\u7A7F": ["\u7A7F\u8863", "\u642D\u914D", "\u7A7F\u642D", "\u8863\u670D"],
  "\u505A\u996D": ["\u70F9\u996A", "\u4E0B\u53A8", "\u7092\u83DC", "\u716E\u996D", "cook"],
  "\u6253\u626B": ["\u6E05\u6D01", "\u626B\u5730", "\u62D6\u5730", "\u641E\u536B\u751F"],
  "\u8D2D\u7269": ["\u4E70\u4E1C\u897F", "\u901B\u8857", "\u5241\u624B", "shopping"],
  "\u65C5\u6E38": ["\u65C5\u884C", "\u51FA\u6E38", "\u6E38\u73A9", "travel"],
  "\u805A\u4F1A": ["\u6D3E\u5BF9", "\u805A\u9910", "\u8F70\u8DB4", "party"],
  "\u7EA6\u4F1A": ["\u89C1\u9762", "\u7EA6\u89C1", "\u76F8\u4EB2", "date"],
  "\u52A0\u73ED": ["\u71AC\u591C\u5E72\u6D3B", "\u8D76\u5DE5", "\u8D85\u65F6\u5DE5\u4F5C", "overtime"],
  "\u8BF7\u5047": ["\u4F11\u5047", "\u544A\u5047", "\u653E\u5047", "\u6B47\u73ED"],
  "\u8FDF\u5230": ["\u665A\u4E86", "\u6765\u4E0D\u53CA", "\u8D76\u4E0D\u4E0A"],
  "\u51FA\u5DEE": ["\u5DEE\u65C5", "\u516C\u51FA", "\u5916\u6D3E"],
  "\u6D17\u6FA1": ["\u6DCB\u6D74", "\u6CE1\u6FA1", "\u51B2\u51C9", "shower"],
  "\u5237\u7259": ["\u6F31\u53E3", "\u53E3\u8154\u6E05\u6D01"],
  "\u5316\u5986": ["\u7F8E\u5986", "\u4E0A\u5986", "\u6253\u626E", "makeup"],
  "\u7406\u53D1": ["\u526A\u5934\u53D1", "\u7406\u53D1\u5E97", "\u53D1\u578B", "haircut"],
  "\u905B\u72D7": ["\u6E9C\u72D7", "\u5E26\u72D7\u6563\u6B65"],
  "\u5582\u732B": ["\u94F2\u5C4E", "\u64B8\u732B", "\u517B\u732B"],
  "\u4E0B\u5355": ["\u4E0B\u5355\u8D2D\u4E70", "\u7F51\u8D2D", "\u4E70\u4E70\u4E70"],
  "\u9000\u8D27": ["\u9000\u6B3E", "\u552E\u540E", "\u6362\u8D27"],
  "\u7B7E\u6536": ["\u53D6\u5FEB\u9012", "\u6536\u5305\u88F9", "\u6536\u8D27"],
  "\u5FEB\u9012": ["\u5305\u88F9", "\u7269\u6D41", "\u987A\u4E30", "\u83DC\u9E1F"],
  "\u5916\u5356": ["\u70B9\u5916\u5356", "\u7F8E\u56E2", "\u997F\u4E86\u4E48", "\u53EB\u5916\u5356"],
  "\u53EB\u8F66": ["\u6253\u8F66", "\u53EB\u6EF4\u6EF4", "\u7F51\u7EA6\u8F66", "\u51FA\u79DF\u8F66"],
  "\u6392\u961F": ["\u7B49\u4F4D", "\u7B49\u5019", "\u6392\u53F7"],
  "\u9884\u7EA6": ["\u6302\u53F7", "\u9884\u5B9A", "\u8BA2\u4F4D", "\u9884\u8BA2"],
  "\u5145\u503C": ["\u5145\u94B1", "\u7F34\u8D39", "\u7EED\u8D39", "\u4ED8\u8D39"],
  "\u63D0\u73B0": ["\u53D6\u94B1", "\u8F6C\u8D26", "\u6C47\u6B3E"],
  "\u626B\u7801": ["\u4E8C\u7EF4\u7801", "\u626B\u4E00\u626B", "\u4ED8\u6B3E\u7801"],
  "\u642C\u5BB6": ["\u642C\u8FC1", "\u4E54\u8FC1", "\u6362\u5730\u65B9", "\u6362\u623F\u5B50", "\u65B0\u5BB6"],
  "\u88C5\u4FEE": ["\u7FFB\u65B0", "\u6539\u9020", "\u88C5\u6F62", "\u65BD\u5DE5"],
  "\u5012\u5783\u573E": ["\u6254\u5783\u573E", "\u5783\u573E\u5206\u7C7B"],
  "\u505A\u5BB6\u52A1": ["\u5BB6\u52A1\u6D3B", "\u5E72\u6D3B", "\u6253\u626B\u536B\u751F"],
  "\u53EB\u9192": ["\u95F9\u949F", "\u8D77\u5E8A", "\u65E9\u8D77", "\u8D56\u5E8A"],
  "\u71AC\u591C": ["\u665A\u7761", "\u901A\u5BB5", "\u591C\u732B\u5B50", "\u5931\u7720"],
  "\u5348\u4F11": ["\u5348\u7761", "\u5C0F\u61A9", "\u6253\u4E2A\u76F9"],
  "\u6563\u6B65": ["\u6E9C\u8FBE", "\u8D70\u8D70", "\u901B\u901B"],
  "\u6668\u8DD1": ["\u6668\u7EC3", "\u65E9\u8D77\u8FD0\u52A8", "\u8DD1\u6B65"],
  "\u953B\u70BC": ["\u5065\u8EAB", "\u8FD0\u52A8", "\u7EC3", "workout", "\u8DD1\u6B65", "\u953B\u70BC\u4E60\u60EF"],
  "\u505A\u745C\u4F3D": ["\u745C\u4F3D", "\u62C9\u4F38", "\u51A5\u60F3", "yoga"],
  "\u6E38\u6CF3": ["\u6CE1\u6CF3\u6C60", "\u86D9\u6CF3", "\u81EA\u7531\u6CF3", "swim"],
  "\u9A91\u8F66": ["\u9A91\u81EA\u884C\u8F66", "\u5355\u8F66", "\u9A91\u884C", "cycling"],
  "\u722C\u5C71": ["\u767B\u5C71", "\u5F92\u6B65", "\u8FDC\u8DB3", "hiking"],
  "\u9493\u9C7C": ["\u5782\u9493", "\u9493", "\u9493\u9C7C\u4F6C", "fishing"],
  "\u5531\u6B4C": ["K\u6B4C", "\u5531K", "KTV", "karaoke"],
  "\u8DF3\u821E": ["\u821E\u8E48", "\u8E66\u8FEA", "\u8DF3", "dance"],
  "\u62CD\u7167": ["\u62CD\u6444", "\u6444\u5F71", "\u7167\u76F8", "photo"],
  "\u5237\u624B\u673A": ["\u5237\u6296\u97F3", "\u5237\u5FAE\u535A", "\u5237\u89C6\u9891", "\u6478\u9C7C"],
  "\u770B\u5267": ["\u8FFD\u5267", "\u5237\u5267", "\u770B\u7535\u89C6\u5267", "\u7172\u5267"],
  "\u6253\u6E38\u620F": ["\u73A9\u6E38\u620F", "\u5F00\u9ED1", "\u4E0A\u5206", "gaming"],
  "\u804A\u5929": ["\u804A", "\u4F83", "\u5439\u725B", "\u95F2\u804A"],
  "\u5435\u67B6": ["\u4E89\u5435", "\u5435", "\u95F9\u77DB\u76FE", "\u62CC\u5634"],
  "\u9053\u6B49": ["\u8BA4\u9519", "\u8BF4\u5BF9\u4E0D\u8D77", "\u8D54\u4E0D\u662F", "apologize"],
  "\u642C\u7816": ["\u5E72\u6D3B", "\u6253\u5DE5", "\u82E6\u529B"],
  "\u5E26\u5A03": ["\u5E26\u5B69\u5B50", "\u770B\u5B69\u5B50", "\u966A\u5A03"],
  "\u905B\u5F2F": ["\u6563\u6B65", "\u6E9C\u8FBE", "\u8D70\u8D70"],
  "\u8D76\u98DE\u673A": ["\u8D76\u822A\u73ED", "\u53BB\u673A\u573A", "\u767B\u673A"],
  "\u5835\u8F66": ["\u585E\u8F66", "\u4EA4\u901A\u62E5\u5835", "\u8DEF\u4E0A\u5835"],
  "\u505C\u8F66": ["\u627E\u8F66\u4F4D", "\u6CCA\u8F66", "\u505C\u8F66\u573A"],
  "\u52A0\u6CB9": ["\u5145\u7535", "\u52A0\u6EE1", "\u6CB9\u8D39", "\u7535\u8D39"],
  "\u4FEE\u8F66": ["\u6C7D\u8F66\u7EF4\u4FEE", "\u4FDD\u517B", "4S\u5E97"],
  "\u770B\u75C5": ["\u5C31\u533B", "\u53BB\u533B\u9662", "\u770B\u533B\u751F", "\u6302\u53F7"],
  "\u914D\u773C\u955C": ["\u9A8C\u5149", "\u8FD1\u89C6", "\u773C\u955C\u5E97"],
  "\u529E\u8BC1": ["\u529E\u624B\u7EED", "\u8BC1\u4EF6", "\u5BA1\u6279"],
  "\u7F34\u7A0E": ["\u62A5\u7A0E", "\u4E2A\u7A0E", "\u7A0E\u52A1"],
  // ── 冷启动种子扩展（自动生成，2000组目标）──────────────────────────
  "\u70E4\u9E2D": ["\u5317\u4EAC\u70E4\u9E2D", "\u7247\u76AE\u9E2D", "\u70E4\u9E2D\u5E97"],
  "\u9992\u5934": ["\u82B1\u5377", "\u53D1\u9762", "\u9762\u98DF"],
  "\u714E\u997C": ["\u714E\u997C\u679C\u5B50", "\u9E21\u86CB\u997C", "\u8584\u997C"],
  "\u5BFF\u53F8": ["\u751F\u9C7C\u7247", "\u523A\u8EAB", "\u65E5\u6599"],
  "\u62AB\u8428": ["pizza", "\u5916\u5356", "\u5FC5\u80DC\u5BA2"],
  "\u6C49\u5821": ["\u9EA6\u5F53\u52B3", "\u80AF\u5FB7\u57FA", "\u5FEB\u9910"],
  "\u6C99\u62C9": ["\u852C\u83DC\u6C99\u62C9", "\u8F7B\u98DF", "\u5065\u5EB7\u9910"],
  "\u725B\u6392": ["\u897F\u9910", "\u4E94\u5206\u719F", "\u4E03\u5206\u719F", "steak"],
  "\u610F\u9762": ["pasta", "\u610F\u5927\u5229\u9762", "\u901A\u5FC3\u7C89"],
  "\u84B8\u83DC": ["\u84B8\u9C7C", "\u84B8\u6392\u9AA8", "\u84B8\u86CB"],
  "\u7096\u6C64": ["\u8001\u706B\u6C64", "\u7172\u6C64", "\u9E21\u6C64"],
  "\u51C9\u62CC": ["\u62CC\u83DC", "\u51C9\u83DC", "\u51B7\u83DC"],
  "\u9171\u6CB9": ["\u751F\u62BD", "\u8001\u62BD", "\u8C03\u5473"],
  "\u8FA3\u6912": ["\u8FA3", "\u8FA3\u9171", "\u8FA3\u6CB9", "\u5241\u6912"],
  "\u82B1\u6912": ["\u9EBB", "\u85E4\u6912", "\u9EBB\u8FA3"],
  "\u516B\u89D2": ["\u4E94\u9999", "\u6842\u76AE", "\u9999\u6599"],
  "\u51B0\u6DC7\u6DCB": ["\u96EA\u7CD5", "\u51B0\u68CD", "\u751C\u7B52"],
  "\u86CB\u7CD5": ["\u751F\u65E5\u86CB\u7CD5", "\u751C\u54C1", "\u70D8\u7119"],
  "\u5DE7\u514B\u529B": ["\u53EF\u53EF", "\u751C\u98DF", "\u9ED1\u5DE7"],
  "\u679C\u6C41": ["\u9C9C\u69A8", "\u6A59\u6C41", "\u897F\u74DC\u6C41"],
  "\u53EF\u4E50": ["\u78B3\u9178\u996E\u6599", "\u96EA\u78A7", "\u6C7D\u6C34"],
  "\u8C46\u8150": ["\u8C46\u5E72", "\u8C46\u76AE", "\u8C46\u5236\u54C1"],
  "\u9E21\u8089": ["\u9E21\u80F8", "\u9E21\u817F", "\u9E21\u7FC5"],
  "\u732A\u8089": ["\u4E94\u82B1\u8089", "\u6392\u9AA8", "\u8089\u4E1D"],
  "\u725B\u8089": ["\u725B\u8169", "\u725B\u8171", "\u725B\u8089\u9762"],
  "\u7F8A\u8089": ["\u6DAE\u7F8A\u8089", "\u70E4\u5168\u7F8A", "\u624B\u6293"],
  "\u6D77\u9C9C": ["\u867E", "\u8783\u87F9", "\u9C7C", "\u8D1D\u7C7B"],
  "\u7D20\u98DF": ["\u7D20\u83DC", "\u5403\u7D20", "\u658B\u996D"],
  "\u8FA3\u5473": ["\u9EBB\u8FA3", "\u9999\u8FA3", "\u5FAE\u8FA3", "\u53D8\u6001\u8FA3"],
  "\u751C\u5473": ["\u751C\u70B9", "\u751C\u54C1", "\u7CD6"],
  "\u9178\u5473": ["\u9178\u83DC", "\u67E0\u6AAC", "\u918B"],
  "\u82E6\u5473": ["\u82E6\u74DC", "\u9ED1\u5496\u5561", "\u82E6"],
  "\u9999\u83DC": ["\u82AB\u837D", "\u4E0D\u5403\u9999\u83DC", "\u9999\u83DC\u515A"],
  "\u8471": ["\u5927\u8471", "\u5C0F\u8471", "\u8471\u82B1"],
  "\u59DC": ["\u8001\u59DC", "\u751F\u59DC", "\u59DC\u7247"],
  "\u849C": ["\u5927\u849C", "\u849C\u672B", "\u849C\u84C9"],
  "\u5473\u7CBE": ["\u9E21\u7CBE", "\u8C03\u5473\u6599", "\u63D0\u9C9C"],
  "\u8611\u83C7": ["\u9999\u83C7", "\u91D1\u9488\u83C7", "\u5E73\u83C7"],
  "\u571F\u8C46": ["\u9A6C\u94C3\u85AF", "\u85AF\u6761", "\u571F\u8C46\u4E1D"],
  "\u897F\u7EA2\u67FF": ["\u756A\u8304", "\u5723\u5973\u679C", "\u756A\u8304\u7092\u86CB"],
  "\u9EC4\u74DC": ["\u9752\u74DC", "\u51C9\u62CC\u9EC4\u74DC"],
  "\u8304\u5B50": ["\u7EA2\u70E7\u8304\u5B50", "\u9C7C\u9999\u8304\u5B50"],
  "\u767D\u83DC": ["\u5927\u767D\u83DC", "\u5C0F\u767D\u83DC", "\u5A03\u5A03\u83DC"],
  "\u83E0\u83DC": ["\u6CE2\u83DC", "\u7EFF\u53F6\u83DC"],
  "\u897F\u5170\u82B1": ["\u82B1\u83DC", "\u82B1\u6930\u83DC"],
  "\u7389\u7C73": ["\u751C\u7389\u7C73", "\u7206\u7C73\u82B1", "\u7389\u7C73\u68D2"],
  "\u82F9\u679C": ["\u7EA2\u5BCC\u58EB", "\u9752\u82F9\u679C", "\u6C34\u679C"],
  "\u9999\u8549": ["\u82AD\u8549", "\u70ED\u5E26\u6C34\u679C"],
  "\u8349\u8393": ["\u84DD\u8393", "\u8986\u76C6\u5B50", "\u6D46\u679C"],
  "\u897F\u74DC": ["\u54C8\u5BC6\u74DC", "\u751C\u74DC"],
  "\u8461\u8404": ["\u63D0\u5B50", "\u8461\u8404\u9152", "\u7EA2\u9152"],
  "\u6A58\u5B50": ["\u6A59\u5B50", "\u67D1\u6A58", "\u67DA\u5B50"],
  "\u8292\u679C": ["\u70ED\u5E26\u6C34\u679C", "\u8292\u679C\u6C41"],
  "\u69B4\u83B2": ["\u81ED", "\u6C34\u679C\u4E4B\u738B"],
  "\u83DC\u8C31": ["\u98DF\u8C31", "\u505A\u6CD5", "\u6559\u7A0B"],
  "\u62FF\u624B\u83DC": ["\u7279\u957F\u83DC", "\u62DB\u724C\u83DC", "\u7EDD\u6D3B"],
  "\u53E3\u5473": ["\u5473\u9053", "\u53E3\u611F", "\u98CE\u5473"],
  "\u5FCC\u53E3": ["\u4E0D\u5403", "\u8FC7\u654F\u98DF\u7269", "\u7981\u5FCC", "\u4E0D\u78B0"],
  "\u7D20\u98DF\u4E3B\u4E49": ["\u5403\u7D20", "\u7EAF\u7D20", "vegan"],
  "\u5C0F\u5403": ["\u96F6\u5634", "\u8DEF\u8FB9\u644A", "\u591C\u5E02\u5C0F\u5403"],
  "\u6296\u97F3": ["\u77ED\u89C6\u9891", "TikTok", "\u5237\u6296\u97F3", "\u6296\u97F3\u76F4\u64AD"],
  "\u5FAE\u535A": ["\u53D1\u5FAE\u535A", "\u70ED\u641C", "\u8F6C\u53D1", "\u8D85\u8BDD"],
  "\u5FAE\u4FE1": ["\u804A\u5929", "\u670B\u53CB\u5708", "\u516C\u4F17\u53F7", "\u5FAE\u4FE1\u7FA4"],
  "\u5C0F\u7EA2\u4E66": ["\u79CD\u8349", "\u7B14\u8BB0", "\u5206\u4EAB", "\u62D4\u8349"],
  "B\u7AD9": ["\u54D4\u54E9\u54D4\u54E9", "\u5F39\u5E55", "up\u4E3B", "\u756A\u5267"],
  "\u7F51\u7EA2": ["\u535A\u4E3B", "KOL", "\u8FBE\u4EBA", "\u7F51\u7EA2\u5E97"],
  "WiFi": ["\u7F51\u7EDC", "\u4FE1\u53F7", "\u65AD\u7F51", "\u7F51\u901F"],
  "\u516C\u4F17\u53F7": ["\u8BA2\u9605\u53F7", "\u63A8\u6587", "\u6587\u7AE0"],
  "\u670B\u53CB\u5708": ["\u53D1\u5708", "\u6652", "\u70B9\u8D5E", "\u8BC4\u8BBA"],
  "\u8868\u60C5\u5305": ["\u6597\u56FE", "emoji", "\u641E\u7B11\u56FE"],
  "\u70ED\u641C": ["\u4E0A\u70ED\u641C", "\u70ED\u95E8\u8BDD\u9898", "\u70ED\u8BAE"],
  "\u8F6C\u53D1": ["\u5206\u4EAB", "\u6269\u6563", "\u5B89\u5229"],
  "\u70B9\u8D5E": ["\u53CC\u51FB", "\u559C\u6B22", "like"],
  "\u8BC4\u8BBA": ["\u7559\u8A00", "\u56DE\u590D", "\u8BA8\u8BBA"],
  "\u7C89\u4E1D": ["\u5173\u6CE8\u8005", "\u8FFD\u968F\u8005", "fan"],
  "\u9ED1\u7C89": ["\u55B7\u5B50", "\u952E\u76D8\u4FA0", "\u6760\u7CBE"],
  "\u4FE1\u606F\u8327\u623F": ["\u540C\u6E29\u5C42", "\u63A8\u8350\u7B97\u6CD5"],
  "vlog": ["\u89C6\u9891\u65E5\u8BB0", "\u62CDvlog", "\u8BB0\u5F55\u751F\u6D3B"],
  "\u5F39\u5E55": ["\u8BC4\u8BBA\u533A", "\u4E92\u52A8", "\u5410\u69FD"],
  "\u79CD\u8349": ["\u63A8\u8350", "\u5B89\u5229", "\u597D\u7269"],
  "\u62D4\u8349": ["\u4E70\u5230\u624B", "\u5165\u624B", "\u4E0B\u5355"],
  "\u4EE3\u8D2D": ["\u6D77\u6DD8", "\u56FD\u5916\u4E70", "\u514D\u7A0E\u5E97"],
  "\u62FC\u56E2": ["\u62FC\u5355", "\u56E2\u8D2D", "\u62FC\u591A\u591A"],
  "\u79D2\u6740": ["\u9650\u65F6\u62A2\u8D2D", "\u95EA\u8D2D", "\u79D2\u6740\u4EF7"],
  "\u5BA2\u670D": ["\u552E\u540E", "\u6295\u8BC9", "\u9000\u6362"],
  "\u597D\u8BC4": ["\u4E94\u661F", "\u8BC4\u4EF7", "\u63A8\u8350"],
  "\u5DEE\u8BC4": ["\u4E00\u661F", "\u6295\u8BC9", "\u4E0D\u63A8\u8350"],
  "\u6253\u5361": ["\u7B7E\u5230", "\u6BCF\u65E5\u6253\u5361", "check-in"],
  "\u5728\u7EBF": ["\u7EBF\u4E0A", "\u8FDC\u7A0B", "\u4E91\u7AEF"],
  "\u5BC6\u7801": ["\u53E3\u4EE4", "\u9A8C\u8BC1\u7801", "\u6307\u7EB9"],
  "\u8D26\u53F7": ["\u6CE8\u518C", "\u767B\u5F55", "\u7528\u6237\u540D"],
  "\u9690\u79C1": ["\u4E2A\u4EBA\u4FE1\u606F", "\u6570\u636E\u4FDD\u62A4", "\u6CC4\u9732"],
  "\u5E7F\u544A": ["\u63A8\u5E7F", "\u5F39\u7A97", "\u690D\u5165"],
  "\u7EAA\u5F55\u7247": ["BBC", "\u820C\u5C16", "\u4EBA\u6587"],
  "\u53E4\u5178\u97F3\u4E50": ["\u4EA4\u54CD\u4E50", "\u94A2\u7434\u66F2", "\u534F\u594F\u66F2"],
  "\u6447\u6EDA": ["\u4E50\u961F", "\u6447\u6EDA\u4E50", "\u5409\u4ED6solo"],
  "\u8BF4\u5531": ["rap", "\u563B\u54C8", "hip-hop", "freestyle"],
  "\u6C11\u8C23": ["\u6C11\u8C23\u6B4C\u624B", "\u6728\u5409\u4ED6", "\u6587\u827A"],
  "\u7535\u5B50\u97F3\u4E50": ["EDM", "DJ", "\u8E66\u8FEA"],
  "\u7235\u58EB": ["jazz", "\u84DD\u8C03", "blues"],
  "\u6B4C\u5355": ["\u64AD\u653E\u5217\u8868", "\u6536\u85CF", "\u63A8\u8350\u6B4C\u66F2"],
  "\u8033\u673A": ["\u964D\u566A", "AirPods", "\u97F3\u8D28"],
  "\u5409\u4ED6": ["\u5F39\u5409\u4ED6", "guitar", "\u5F39\u5531", "\u548C\u5F26"],
  "\u94A2\u7434": ["\u5F39\u94A2\u7434", "piano", "\u952E\u76D8", "\u7434\u952E"],
  "\u5C0F\u63D0\u7434": ["violin", "\u5F26\u4E50", "\u62C9\u7434"],
  "\u67B6\u5B50\u9F13": ["\u6253\u9F13", "drums", "\u8282\u594F"],
  "\u4E50\u961F": ["\u7EC4\u4E50\u961F", "band", "\u6392\u7EC3"],
  "\u6B4C\u624B": ["\u5531\u6B4C", "\u6B4C\u66F2", "\u51FA\u9053"],
  "\u5076\u50CF": ["\u8FFD\u661F", "\u7C89\u4E1D", "\u5E94\u63F4"],
  "\u559C\u5267": ["\u641E\u7B11", "\u5E7D\u9ED8", "\u7B11\u8BDD"],
  "\u6050\u6016\u7247": ["\u60CA\u609A", "\u5413\u4EBA", "\u6050\u6016"],
  "\u7231\u60C5\u7247": ["\u6D6A\u6F2B", "\u8A00\u60C5", "\u751C\u871C"],
  "\u52A8\u4F5C\u7247": ["\u6B66\u6253", "\u7279\u6548", "\u5927\u7247"],
  "\u79D1\u5E7B\u7247": ["\u79D1\u5E7B", "\u672A\u6765", "\u592A\u7A7A"],
  "\u60AC\u7591": ["\u63A8\u7406", "\u70E7\u8111", "\u53CD\u8F6C"],
  "\u5BFC\u6F14": ["\u62CD\u7535\u5F71", "\u5F71\u7247", "\u4F5C\u54C1"],
  "\u6F14\u5458": ["\u660E\u661F", "\u89D2\u8272", "\u8868\u6F14"],
  "\u7968\u623F": ["\u4E0A\u6620", "\u9996\u6620", "\u9662\u7EBF"],
  "\u6E38\u620F\u4E3B\u673A": ["PS5", "Switch", "Xbox"],
  "\u624B\u6E38": ["\u624B\u673A\u6E38\u620F", "\u738B\u8005", "\u539F\u795E"],
  "steam": ["PC\u6E38\u620F", "\u7AEF\u6E38", "3A\u5927\u4F5C"],
  "\u5BC6\u5BA4\u9003\u8131": ["\u5BC6\u5BA4", "\u89E3\u8C1C", "\u6050\u6016\u5BC6\u5BA4"],
  "\u7F51\u8D2D": ["\u6DD8\u5B9D", "\u4EAC\u4E1C", "\u62FC\u591A\u591A", "\u5929\u732B"],
  "\u53CC\u5341\u4E00": ["\u53CC11", "\u6253\u6298", "\u5927\u4FC3", "\u6EE1\u51CF"],
  "\u4F18\u60E0\u5238": ["\u6298\u6263", "\u7EA2\u5305", "\u8FD4\u5229", "\u4F18\u60E0\u7801"],
  "\u76F2\u76D2": ["\u6F6E\u73A9", "\u624B\u529E", "\u6536\u85CF", "\u6CE1\u6CE1\u739B\u7279"],
  "\u6253\u6298": ["\u964D\u4EF7", "\u4FC3\u9500", "\u7279\u4EF7", "\u6E05\u4ED3"],
  "\u6EE1\u51CF": ["\u6EE1\u51CF\u5238", "\u51D1\u5355", "\u4F18\u60E0"],
  "\u9884\u552E": ["\u5B9A\u91D1", "\u5C3E\u6B3E", "\u9884\u8D2D"],
  "\u76F4\u64AD\u5E26\u8D27": ["\u76F4\u64AD\u95F4", "\u94FE\u63A5", "\u4E0A\u67B6"],
  "\u597D\u7269": ["\u63A8\u8350", "\u5FC5\u4E70", "\u503C\u5F97\u4E70"],
  "\u6027\u4EF7\u6BD4": ["\u5212\u7B97", "\u4FBF\u5B9C\u53C8\u597D", "\u7269\u7F8E\u4EF7\u5EC9"],
  "\u54C1\u724C": ["\u540D\u724C", "\u5927\u724C", "\u5962\u4F88\u54C1"],
  "\u5C71\u5BE8": ["\u4EFF\u54C1", "\u5047\u8D27", "\u9AD8\u4EFF"],
  "\u6B63\u54C1": ["\u6B63\u7248", "\u5B98\u65B9", "\u65D7\u8230\u5E97"],
  "\u4F1A\u5458": ["VIP", "\u5E74\u8D39", "\u6743\u76CA"],
  "\u79EF\u5206": ["\u5151\u6362", "\u6512\u79EF\u5206", "\u6298\u6263"],
  "\u7269\u6D41": ["\u5FEB\u9012", "\u53D1\u8D27", "\u5230\u8D27"],
  "\u552E\u540E": ["\u9000\u8D27", "\u6362\u8D27", "\u7EF4\u4FEE"],
  "\u5305\u90AE": ["\u514D\u8FD0\u8D39", "\u987A\u4E30\u5230\u4ED8"],
  "\u6279\u53D1": ["\u56E2\u8D2D", "\u91CF\u5927\u4F18\u60E0"],
  "\u52C7\u6C14": ["\u52C7\u6562", "\u80C6\u91CF", "\u6562", "brave"],
  "\u575A\u6301": ["\u6BC5\u529B", "\u575A\u5F3A", "\u4E0D\u653E\u5F03", "\u6301\u4E4B\u4EE5\u6052"],
  "\u653E\u5F03": ["\u534A\u9014\u800C\u5E9F", "\u7B97\u4E86", "\u4E0D\u5E72\u4E86"],
  "\u6210\u529F": ["\u80DC\u5229", "\u8FBE\u6210", "\u6210\u5C31", "\u8D62"],
  "\u5931\u8D25": ["\u8F93", "\u6CA1\u505A\u5230", "\u843D\u9009", "\u5931\u5229"],
  "\u673A\u4F1A": ["\u673A\u9047", "\u65F6\u673A", "\u98CE\u53E3"],
  "\u6311\u6218": ["\u56F0\u96BE", "\u8003\u9A8C", "\u96BE\u5173"],
  "\u9009\u62E9": ["\u51B3\u5B9A", "\u6289\u62E9", "\u53D6\u820D"],
  "\u540E\u679C": ["\u7ED3\u679C", "\u4EE3\u4EF7", "\u5F71\u54CD"],
  "\u76EE\u6807": ["\u76EE\u7684", "\u65B9\u5411", "\u8FFD\u6C42"],
  "\u8BA1\u5212": ["\u5B89\u6392", "\u89C4\u5212", "\u6253\u7B97"],
  "\u6267\u884C": ["\u843D\u5B9E", "\u505A", "\u5B9E\u65BD"],
  "\u9752\u6625": ["\u5E74\u8F7B", "\u9752\u5E74", "\u5E74\u5C11"],
  "\u4E2D\u5E74": ["\u4E2D\u5E74\u5371\u673A", "\u4E0A\u6709\u8001\u4E0B\u6709\u5C0F"],
  "\u8001\u5E74": ["\u9000\u4F11", "\u517B\u8001", "\u665A\u5E74"],
  "\u6000\u65E7": ["\u60F3\u5FF5", "\u4EE5\u524D", "\u5F53\u5E74"],
  "\u4FE1\u4EFB": ["\u76F8\u4FE1", "\u9760\u8C31", "\u6258\u4ED8"],
  "\u80CC\u53DB": ["\u51FA\u5356", "\u6B3A\u9A97", "\u8F9C\u8D1F"],
  "\u6127\u759A": ["\u5BF9\u4E0D\u8D77", "\u5185\u759A", "\u6B49\u610F"],
  "\u5BBD\u5BB9": ["\u539F\u8C05", "\u5305\u5BB9", "\u5927\u5EA6"],
  "\u8D23\u4EFB": ["\u62C5\u5F53", "\u4E49\u52A1", "\u8D1F\u8D23"],
  "\u81EA\u7531": ["\u65E0\u62D8\u65E0\u675F", "\u968F\u5FC3", "\u89E3\u653E"],
  "\u75DB\u82E6": ["\u6298\u78E8", "\u96BE\u53D7", "\u53D7\u82E6"],
  "\u5E0C\u671B": ["\u671F\u5F85", "\u76FC\u671B", "\u61A7\u61AC"],
  "\u52AA\u529B": ["\u594B\u6597", "\u62FC\u640F", "\u52A0\u6CB9"],
  "\u61D2\u60F0": ["\u61D2", "\u4E0D\u60F3\u52A8", "\u6478\u9C7C"],
  "\u597D\u4E60\u60EF": ["\u81EA\u5F8B", "\u575A\u6301", "\u89C4\u5F8B"],
  "\u504F\u98DF": ["\u6311\u98DF", "\u4E0D\u7231\u5403", "\u5ACC\u5F03"],
  "\u5473\u9053": ["\u53E3\u5473", "\u53E3\u611F", "\u98CE\u5473"],
  "\u54C1\u5473": ["\u5BA1\u7F8E", "\u773C\u5149", "\u683C\u8C03"],
  "\u6C1B\u56F4": ["\u6C14\u6C1B", "\u73AF\u5883", "\u611F\u89C9", "\u8C03\u8C03"],
  "\u4EEA\u5F0F\u611F": ["\u4EEA\u5F0F", "\u90D1\u91CD", "\u7279\u522B"],
  "\u5B89\u5168\u611F": ["\u8E0F\u5B9E", "\u7A33\u5B9A", "\u53EF\u9760"],
  "\u5B58\u5728\u611F": ["\u88AB\u5173\u6CE8", "\u88AB\u770B\u89C1"],
  "\u5F52\u5C5E\u611F": ["\u5BB6\u7684\u611F\u89C9", "\u878D\u5165", "\u8BA4\u540C"],
  "\u526F\u4E1A": ["\u517C\u804C", "\u5916\u5FEB", "\u659C\u6760"],
  "\u804C\u4E1A\u89C4\u5212": ["\u53D1\u5C55\u65B9\u5411", "\u804C\u4E1A\u8DEF\u5F84", "\u664B\u5347"],
  "\u6512\u94B1": ["\u5B58\u94B1", "\u50A8\u84C4", "\u79EF\u84C4"],
  "\u6708\u5149\u65CF": ["\u82B1\u5149", "\u5165\u4E0D\u6577\u51FA", "\u8D85\u652F"],
  "\u793E\u4EA4\u6050\u60E7": ["\u793E\u6050", "\u4E0D\u5584\u4EA4\u9645", "\u5185\u5411", "\u6015\u751F"],
  "\u793E\u4EA4\u725B\u4EBA": ["\u793E\u725B", "\u81EA\u6765\u719F", "\u5916\u5411"],
  "\u4EEA\u5F0F": ["\u4E60\u60EF", "\u65E5\u5E38", "\u56FA\u5B9A\u6D41\u7A0B"],
  "\u65E9\u8D77": ["\u65E9\u9E1F", "\u6668\u578B\u4EBA", "\u65E9\u8D77\u7684\u9E1F"],
  "\u591C\u732B\u5B50": ["\u71AC\u591C", "\u665A\u7761", "\u591C\u665A"],
  "\u62D6\u5EF6\u75C7": ["\u62D6\u5EF6", "\u660E\u5929\u518D\u8BF4", "\u62D6\u62C9"],
  "\u5B8C\u7F8E\u4E3B\u4E49": ["\u5F3A\u8FEB\u75C7", "\u8FFD\u6C42\u5B8C\u7F8E", "\u4E0D\u6EE1\u610F"],
  "\u9009\u62E9\u56F0\u96BE": ["\u7EA0\u7ED3", "\u9009\u4E0D\u597D", "\u72B9\u8C6B"],
  "\u5206\u79BB\u7126\u8651": ["\u60F3\u5FF5", "\u4E0D\u820D", "\u4F9D\u8D56"],
  "\u8D22\u52A1\u7126\u8651": ["\u7F3A\u94B1", "\u8FD8\u4E0D\u8D77", "\u538B\u529B\u5927"],
  "\u6625\u5929": ["\u6625\u5B63", "\u5F00\u6625", "\u4E07\u7269\u590D\u82CF", "\u82B1\u5F00"],
  "\u590F\u5929": ["\u590F\u5B63", "\u9177\u6691", "\u4E09\u4F0F\u5929", "\u7A7A\u8C03"],
  "\u79CB\u5929": ["\u79CB\u5B63", "\u91D1\u79CB", "\u843D\u53F6", "\u51C9\u723D"],
  "\u51AC\u5929": ["\u51AC\u5B63", "\u5BD2\u51AC", "\u4E0B\u96EA", "\u6696\u6C14"],
  "\u4E0B\u96E8": ["\u96E8\u5929", "\u66B4\u96E8", "\u6885\u96E8", "\u6253\u4F1E"],
  "\u4E0B\u96EA": ["\u96EA\u5929", "\u5806\u96EA\u4EBA", "\u66B4\u96EA"],
  "\u53F0\u98CE": ["\u66B4\u98CE", "\u98D3\u98CE", "\u5F3A\u98CE"],
  "\u5730\u9707": ["\u9707", "\u4F59\u9707", "\u9707\u611F"],
  "\u6674\u5929": ["\u5927\u592A\u9633", "\u84DD\u5929", "\u597D\u5929\u6C14"],
  "\u9634\u5929": ["\u591A\u4E91", "\u7070\u8499\u8499"],
  "\u96FE\u973E": ["\u7A7A\u6C14\u8D28\u91CF", "PM2.5", "\u53E3\u7F69"],
  "\u9AD8\u6E29": ["\u70ED\u6D6A", "\u4E2D\u6691", "\u9632\u6691"],
  "\u6A31\u82B1": ["\u82B1\u5F00", "\u8D4F\u82B1", "\u82B1\u5B63"],
  "\u7EA2\u53F6": ["\u8D4F\u79CB", "\u67AB\u53F6", "\u91D1\u9EC4"],
  "\u6D77\u8FB9": ["\u6C99\u6EE9", "\u6D77\u6EE9", "\u51B2\u6D6A", "\u65E5\u843D"],
  "\u5C71\u9876": ["\u767B\u9876", "\u98CE\u666F", "\u8FDC\u773A"],
  "\u65E5\u51FA": ["\u671D\u9633", "\u6E05\u6668", "\u4E1C\u65B9"],
  "\u65E5\u843D": ["\u5915\u9633", "\u9EC4\u660F", "\u665A\u971E"],
  "\u661F\u7A7A": ["\u94F6\u6CB3", "\u6D41\u661F", "\u89C2\u661F"],
  "\u6708\u4EAE": ["\u6EE1\u6708", "\u6708\u5149", "\u8D4F\u6708"],
  "PMP": ["\u9879\u76EE\u7BA1\u7406", "\u9879\u76EE\u7ECF\u7406\u8BA4\u8BC1", "PMI"],
  "CPA": ["\u6CE8\u518C\u4F1A\u8BA1\u5E08", "\u4F1A\u8BA1\u8003\u8BD5"],
  "\u6559\u5E08\u8D44\u683C": ["\u6559\u8D44", "\u6559\u5E08\u8BC1", "\u6559\u7F16"],
  "\u5F8B\u5E08\u8D44\u683C": ["\u53F8\u6CD5\u8003\u8BD5", "\u6CD5\u8003", "\u5F8B\u5E08\u8BC1"],
  "\u56DB\u516D\u7EA7": ["CET", "\u82F1\u8BED\u7B49\u7EA7", "\u8FC7\u56DB\u7EA7"],
  "\u7A0B\u5E8F\u5458": ["\u7801\u519C", "\u5DE5\u7A0B\u5E08", "\u5F00\u53D1\u8005"],
  "\u4EA7\u54C1\u7ECF\u7406": ["PM", "\u4EA7\u54C1\u8BBE\u8BA1", "\u9700\u6C42"],
  "\u8BBE\u8BA1\u5E08": ["UI", "UX", "\u7F8E\u5DE5", "\u89C6\u89C9"],
  "\u8FD0\u8425": ["\u5185\u5BB9\u8FD0\u8425", "\u7528\u6237\u8FD0\u8425", "\u6D3B\u52A8"],
  "\u9500\u552E": ["\u4E1A\u52A1", "\u5BA2\u6237", "\u4E1A\u7EE9"],
  "\u4EBA\u529B\u8D44\u6E90": ["HR", "\u62DB\u8058", "\u9762\u8BD5\u5B98"],
  "\u5E02\u573A\u8425\u9500": ["\u8425\u9500", "\u63A8\u5E7F", "\u54C1\u724C"],
  "\u54A8\u8BE2": ["\u987E\u95EE", "\u54A8\u8BE2\u5E08", "\u65B9\u6848"],
  "\u81EA\u7531\u804C\u4E1A": ["freelance", "\u72EC\u7ACB", "\u63A5\u5355"],
  "\u8FDC\u7A0B\u529E\u516C": ["\u5728\u5BB6\u529E\u516C", "WFH", "\u5C45\u5BB6\u529E\u516C"],
  "\u5171\u4EAB\u529E\u516C": ["co-working", "\u4F17\u521B\u7A7A\u95F4"],
  "\u7F51\u7EA6\u8F66": ["\u6253\u8F66", "\u6EF4\u6EF4", "\u51FA\u79DF\u8F66"],
  "\u81EA\u9A7E": ["\u81EA\u9A7E\u6E38", "\u5F00\u8F66\u51FA\u53BB", "\u516C\u8DEF\u65C5\u884C"],
  "\u52A0\u6CB9\u7AD9": ["\u52A0\u6CB9", "\u6CB9\u4EF7", "\u5145\u7535\u7AD9"],
  "\u8F7B\u8F68": ["\u57CE\u8F68", "\u6709\u8F68\u7535\u8F66"],
  "\u673A\u7968": ["\u8BA2\u673A\u7968", "\u7279\u4EF7\u673A\u7968", "\u5EC9\u822A"],
  "\u706B\u8F66\u7968": ["\u62A2\u7968", "12306", "\u786C\u5EA7\u8F6F\u5367"],
  "\u6C99\u53D1": ["\u5BA2\u5385", "\u5E03\u827A\u6C99\u53D1", "\u771F\u76AE\u6C99\u53D1"],
  "\u5E8A": ["\u5E8A\u57AB", "\u5E8A\u5355", "\u6795\u5934"],
  "\u7A97\u5E18": ["\u906E\u5149\u5E18", "\u767E\u53F6\u7A97"],
  "\u7A7A\u8C03": ["\u5236\u51B7", "\u6696\u98CE", "\u7A7A\u8C03\u75C5"],
  "\u6D17\u8863\u673A": ["\u6D17\u8863\u670D", "\u6EDA\u7B52", "\u70D8\u5E72"],
  "\u51B0\u7BB1": ["\u4FDD\u9C9C", "\u51B7\u51BB", "\u51B0\u9547"],
  "\u5FAE\u6CE2\u7089": ["\u52A0\u70ED", "\u70ED\u996D"],
  "\u5438\u5C18\u5668": ["\u626B\u5730\u673A\u5668\u4EBA", "\u9664\u5C18"],
  "\u9A6C\u6876": ["\u536B\u751F\u95F4", "\u51B2\u6C34", "\u667A\u80FD\u9A6C\u6876"],
  "\u6D74\u5BA4": ["\u6DCB\u6D74", "\u6D74\u7F38", "\u6D17\u6FA1"],
  "\u706F": ["\u53F0\u706F", "\u540A\u706F", "\u591C\u706F"],
  "\u63D2\u5EA7": ["\u5145\u7535", "\u63D2\u5934", "\u8F6C\u6362\u5668"],
  "\u5783\u573E\u6876": ["\u5783\u573E\u5206\u7C7B", "\u5012\u5783\u573E"],
  "\u62D6\u628A": ["\u62D6\u5730", "\u626B\u5730", "\u6E05\u6D01"],
  "\u76AE\u80A4": ["\u62A4\u80A4", "\u75D8\u75D8", "\u9632\u6652", "\u4FDD\u6E7F"],
  "\u5934\u53D1": ["\u53D1\u578B", "\u6D17\u5934", "\u6389\u53D1", "\u67D3\u53D1"],
  "\u773C\u775B": ["\u89C6\u529B", "\u8FD1\u89C6", "\u773C\u955C", "\u773C\u836F\u6C34"],
  "\u8033\u6735": ["\u542C\u529B", "\u8033\u673A", "\u8033\u9E23"],
  "\u7259\u9F7F": ["\u5237\u7259", "\u8865\u7259", "\u667A\u9F7F", "\u77EB\u6B63"],
  "\u9AA8\u5934": ["\u9AA8\u6298", "\u5173\u8282", "\u8170\u690E"],
  "\u808C\u8089": ["\u589E\u808C", "\u62C9\u4F24", "\u9178\u75DB"],
  "\u514D\u75AB\u529B": ["\u62B5\u6297\u529B", "\u4F53\u8D28", "\u4E0D\u5BB9\u6613\u751F\u75C5"],
  "\u65B0\u9648\u4EE3\u8C22": ["\u4EE3\u8C22", "\u57FA\u7840\u4EE3\u8C22"],
  "\u6FC0\u7D20": ["\u5185\u5206\u6CCC", "\u8377\u5C14\u8499"],
  "\u4E2D\u6691": ["\u70ED\u5C04\u75C5", "\u9632\u6691\u964D\u6E29"],
  "\u6655\u8F66": ["\u6655\u8239", "\u6655\u673A", "\u8FD0\u52A8\u75C5"],
  "\u62BD\u7B4B": ["\u817F\u62BD\u7B4B", "\u808C\u8089\u75C9\u631B"],
  "\u6253\u547C\u565C": ["\u547C\u565C", "\u7761\u7720\u547C\u5438", "\u9F3E\u58F0"],
  "\u5E03\u5076\u732B": ["\u732B\u54C1\u79CD", "\u957F\u6BDB\u732B"],
  "\u82F1\u77ED": ["\u82F1\u56FD\u77ED\u6BDB", "\u84DD\u732B"],
  "\u91D1\u6BDB": ["\u91D1\u6BDB\u730E\u72AC", "\u5927\u578B\u72AC"],
  "\u67EF\u57FA": ["\u5C0F\u77ED\u817F", "\u5A01\u5C14\u58EB\u67EF\u57FA"],
  "\u54C8\u58EB\u5947": ["\u4E8C\u54C8", "\u62C6\u5BB6", "\u96EA\u6A47\u72AC"],
  "\u67F4\u72AC": ["\u5C0F\u67F4", "\u65E5\u672C\u72AC"],
  "\u732B\u7802": ["\u732B\u5395\u6240", "\u94F2\u732B\u7802"],
  "\u72D7\u7CAE": ["\u72AC\u7CAE", "\u5BA0\u7269\u98DF\u54C1"],
  "\u5BA0\u7269\u533B\u9662": ["\u517D\u533B", "\u770B\u75C5", "\u75AB\u82D7"],
  "\u7EDD\u80B2": ["\u505A\u624B\u672F", "\u7EDD\u80B2\u624B\u672F"],
  "\u4ED3\u9F20": ["\u9F99\u732B", "\u5154\u5B50", "\u5C0F\u52A8\u7269"],
  "\u91D1\u9C7C": ["\u89C2\u8D4F\u9C7C", "\u9C7C\u7F38", "\u517B\u9C7C"],
  "\u4E4C\u9F9F": ["\u9646\u9F9F", "\u6C34\u9F9F", "\u9F9F\u58F3"],
  "\u9E66\u9E49": ["\u9E1F", "\u517B\u9E1F", "\u5B66\u8BF4\u8BDD"],
  "\u4E00\u4F1A\u513F": ["\u5F85\u4F1A", "\u7B49\u4E00\u4E0B", "\u7A0D\u540E"],
  "\u521A\u624D": ["\u521A\u521A", "\u65B9\u624D", "\u4E4B\u524D"],
  "\u7ECF\u5E38": ["\u5E38\u5E38", "\u603B\u662F", "\u8001\u662F"],
  "\u5076\u5C14": ["\u6709\u65F6\u5019", "\u65F6\u4E0D\u65F6", "\u95F4\u6216"],
  "\u4ECE\u6765": ["\u4E00\u76F4", "\u59CB\u7EC8", "\u5411\u6765"],
  "\u7A81\u7136": ["\u5FFD\u7136", "\u731B\u7136", "\u9AA4\u7136"],
  "\u9A6C\u4E0A": ["\u7ACB\u523B", "\u7ACB\u9A6C", "\u8D76\u7D27"],
  "\u6162\u6162": ["\u9010\u6E10", "\u6E10\u6E10", "\u4E00\u70B9\u70B9"],
  "\u6C38\u8FDC": ["\u4E00\u8F88\u5B50", "\u59CB\u7EC8", "\u6C38\u6052"],
  "\u6682\u65F6": ["\u4E34\u65F6", "\u5148", "\u76EE\u524D"],
  "\u5927\u6982": ["\u5927\u7EA6", "\u5DEE\u4E0D\u591A", "\u5DE6\u53F3"],
  "\u81F3\u5C11": ["\u8D77\u7801", "\u6700\u5C11", "\u4E0D\u4F4E\u4E8E"],
  "\u6700\u591A": ["\u9876\u591A", "\u4E0D\u8D85\u8FC7", "\u4E0A\u9650"],
  "\u51E0\u4E4E": ["\u5DEE\u4E0D\u591A", "\u5FEB\u8981", "\u63A5\u8FD1"],
  // ── 概念级近义（美食/人生事件/宠物/数码/节日）─────────────────────────
  "\u6BCD\u6821": ["\u5927\u5B66", "\u5B66\u6821", "\u9AD8\u4E2D", "\u6821\u53CB"],
  "\u706B\u9505": ["\u6DAE\u9505", "\u9EBB\u8FA3\u70EB", "\u4E32\u4E32", "\u6DAE\u8089", "\u91CD\u5E86\u706B\u9505"],
  "\u70E7\u70E4": ["\u64B8\u4E32", "BBQ", "\u70E4\u8089", "\u70E7\u70E4\u644A"],
  "\u5976\u8336": ["\u5976\u8336\u5E97", "\u73CD\u73E0\u5976\u8336", "\u871C\u96EA\u51B0\u57CE", "\u8336\u996E"],
  "\u5496\u5561": ["\u62FF\u94C1", "\u7F8E\u5F0F", "\u661F\u5DF4\u514B", "\u5496\u5561\u56E0", "coffee"],
  "\u9152": ["\u559D\u9152", "\u5564\u9152", "\u767D\u9152", "\u7EA2\u9152", "\u9189"],
  "\u96F6\u98DF": ["\u85AF\u7247", "\u997C\u5E72", "\u5C0F\u98DF", "\u5634\u998B"],
  "\u65E9\u9910": ["\u65E9\u996D", "\u65E9\u8D77\u5403", "\u65E9\u70B9", "\u5403\u65E9\u9910"],
  "\u665A\u9910": ["\u665A\u996D", "\u665A\u4E0A\u5403", "\u591C\u5BB5", "\u5BB5\u591C"],
  "\u6000\u5B55": ["\u5B55\u671F", "\u5B55\u5987", "\u5F85\u4EA7", "\u9884\u4EA7\u671F", "\u4EA7\u68C0"],
  "\u5BA0\u7269": ["\u732B", "\u72D7", "\u94F2\u5C4E\u5B98", "\u5BA0\u7269\u533B\u9662", "\u732B\u54AA", "\u72D7\u72D7"],
  "\u732B": ["\u55B5", "\u732B\u54AA", "\u517B\u732B", "\u94F2\u5C4E", "\u732B\u7CAE"],
  "\u72D7": ["\u6C6A", "\u72D7\u5B50", "\u517B\u72D7", "\u905B\u72D7", "\u72D7\u7CAE"],
  "\u5929\u6C14": ["\u4E0B\u96E8", "\u6674\u5929", "\u51B7", "\u70ED", "\u964D\u6E29"],
  "\u624B\u673A": ["\u624B\u673A\u58F3", "\u5145\u7535", "\u6362\u624B\u673A", "iPhone", "\u5B89\u5353"],
  "\u7535\u8111": ["\u7B14\u8BB0\u672C", "\u53F0\u5F0F\u673A", "\u4FEE\u7535\u8111", "Mac", "PC", "MacBook", "ThinkPad", "iPad", "\u5E73\u677F"],
  "\u5BB6": ["\u56DE\u5BB6", "\u5BB6\u91CC", "\u5728\u5BB6", "\u8001\u5BB6", "\u5BB6\u4EBA"],
  "\u8FC7\u5E74": ["\u6625\u8282", "\u9664\u5915", "\u5E74\u4E09\u5341", "\u62DC\u5E74", "\u5E74\u591C\u996D"],
  "\u751F\u65E5": ["\u751F\u65E5\u5FEB\u4E50", "\u5E86\u751F", "\u86CB\u7CD5", "\u8BB8\u613F"],
  // ── 工作职场（50组）──────────────────────────────────────────────────
  "\u7B80\u5386": ["CV", "\u5C65\u5386", "\u4E2A\u4EBA\u7B80\u4ECB", "resume"],
  "\u5DE5\u8D44": ["\u85AA\u8D44", "\u85AA\u6C34", "\u6708\u85AA", "\u5E74\u85AA", "salary"],
  "\u52A0\u85AA": ["\u6DA8\u85AA", "\u8C03\u85AA", "\u6DA8\u5DE5\u8D44", "\u63D0\u85AA"],
  "\u5347\u804C": ["\u664B\u5347", "\u63D0\u62D4", "\u5347\u5B98", "promotion"],
  "\u79BB\u804C": ["\u8F9E\u804C", "\u8D70\u4EBA", "\u8DD1\u8DEF", "\u4E0D\u5E72\u4E86"],
  "\u8DF3\u69FD": ["\u6362\u5DE5\u4F5C", "\u6362\u516C\u53F8", "\u53E6\u8C0B\u9AD8\u5C31"],
  "\u540C\u4E8B": ["\u540C\u50DA", "\u642D\u6863", "\u961F\u53CB", "colleague"],
  "\u8001\u677F": ["\u9886\u5BFC", "\u4E0A\u53F8", "\u4E3B\u7BA1", "boss"],
  "\u9879\u76EE": ["\u5DE5\u7A0B", "\u9700\u6C42", "\u4EFB\u52A1", "project"],
  "\u4F1A\u8BAE": ["\u5F00\u4F1A", "\u4F8B\u4F1A", "\u4F1A", "meeting"],
  "\u7EE9\u6548": ["\u8003\u6838", "\u8BC4\u4F30", "KPI", "performance"],
  "KPI": ["\u6307\u6807", "\u7EE9\u6548", "\u76EE\u6807", "OKR"],
  "\u6C47\u62A5": ["\u62A5\u544A", "\u8FF0\u804C", "\u603B\u7ED3", "report"],
  "\u57F9\u8BAD": ["\u57F9\u8BAD\u8BFE", "\u5185\u8BAD", "\u5B66\u4E60", "training"],
  "\u5B9E\u4E60": ["\u5B9E\u4E60\u751F", "\u5B9E\u4E60\u671F", "intern", "internship"],
  "\u88C1\u5458": ["\u88C1\u4EBA", "\u4F18\u5316", "\u6BD5\u4E1A", "layoff"],
  "\u5165\u804C": ["\u62A5\u5230", "\u5165\u804C\u65E5", "\u4E0A\u73ED\u7B2C\u4E00\u5929", "onboarding"],
  "\u8BD5\u7528\u671F": ["\u8003\u5BDF\u671F", "\u8F6C\u6B63", "\u8BD5\u7528"],
  "\u8F6C\u6B63": ["\u6B63\u5F0F\u5458\u5DE5", "\u8FC7\u4E86\u8BD5\u7528\u671F", "\u901A\u8FC7\u8003\u6838"],
  "\u7532\u65B9": ["\u5BA2\u6237", "\u5BA2\u6237\u65B9", "\u9700\u6C42\u65B9"],
  "\u4E59\u65B9": ["\u4F9B\u5E94\u5546", "\u5916\u5305", "\u670D\u52A1\u65B9"],
  "\u9700\u6C42": ["\u9700\u6C42\u6587\u6863", "PRD", "\u4EA7\u54C1\u9700\u6C42", "\u529F\u80FD\u9700\u6C42"],
  "\u6392\u671F": ["\u8BA1\u5212", "\u65F6\u95F4\u8868", "\u91CC\u7A0B\u7891", "schedule"],
  "\u4E0A\u7EBF": ["\u53D1\u5E03", "\u4E0A\u7EBF\u90E8\u7F72", "\u63A8\u9001", "release"],
  "\u5468\u62A5": ["\u65E5\u62A5", "\u6708\u62A5", "\u8FDB\u5EA6\u6C47\u62A5"],
  "\u56E2\u961F": ["\u5C0F\u7EC4", "\u90E8\u95E8", "\u7EC4", "team"],
  "HR": ["\u4EBA\u4E8B", "\u4EBA\u529B\u8D44\u6E90", "\u62DB\u8058"],
  "\u798F\u5229": ["\u4E94\u9669\u4E00\u91D1", "\u5E74\u7EC8\u5956", "\u5956\u91D1", "\u8865\u8D34"],
  "\u5E74\u5047": ["\u5E26\u85AA\u5047", "\u5047\u671F", "\u4F11\u5047", "\u653E\u5047"],
  "\u51FA\u52E4": ["\u6253\u5361", "\u7B7E\u5230", "\u8003\u52E4"],
  "\u65E9\u9000": ["\u63D0\u524D\u8D70", "\u5148\u8D70\u4E86"],
  "\u52A0\u73ED\u8D39": ["\u52A0\u73ED\u5DE5\u8D44", "\u8865\u8D34", "\u8C03\u4F11"],
  "\u8C03\u4F11": ["\u8865\u4F11", "\u6362\u4F11", "\u5012\u4F11"],
  "\u5E74\u7EC8\u5956": ["\u5E74\u7EC8", "\u5341\u4E09\u85AA", "\u53CC\u85AA"],
  "\u80A1\u6743": ["\u671F\u6743", "\u80A1\u7968\u671F\u6743", "RSU", "option"],
  "\u521B\u4E1A": ["\u521B\u4E1A\u516C\u53F8", "\u521D\u521B", "startup", "\u81EA\u5DF1\u5E72"],
  "\u878D\u8D44": ["\u98CE\u6295", "VC", "\u6295\u8D44", "funding"],
  "\u4E0A\u5E02": ["IPO", "\u6572\u949F", "\u5E02\u503C"],
  "PPT": ["\u5E7B\u706F\u7247", "\u6F14\u793A\u6587\u7A3F", "slide", "\u505APPT"],
  "\u65B9\u6848": ["\u63D0\u6848", "\u8BA1\u5212\u4E66", "\u7B56\u5212"],
  "\u590D\u76D8": ["\u56DE\u987E", "\u53CD\u601D", "\u4E8B\u540E\u603B\u7ED3", "retrospective"],
  "\u534F\u4F5C": ["\u5408\u4F5C", "\u914D\u5408", "\u534F\u540C", "collaboration"],
  "\u6C9F\u901A": ["\u4EA4\u6D41", "\u5BF9\u63A5", "\u62C9\u901A", "communication"],
  "\u6478\u9C7C": ["\u5212\u6C34", "\u5077\u61D2", "\u78E8\u6D0B\u5DE5", "\u5E26\u85AA\u62C9\u5C4E"],
  "\u5185\u5377": ["\u5377", "\u8FC7\u5EA6\u7ADE\u4E89", "996"],
  "\u8EBA\u5E73": ["\u4F5B\u7CFB", "\u968F\u7F18", "\u4E0D\u5377\u4E86"],
  "\u80CC\u9505": ["\u80CC\u9ED1\u9505", "\u66FF\u7F6A\u7F8A", "\u7529\u9505"],
  "\u8DD1\u8DEF": ["\u6E9C\u4E86", "\u95EA\u4EBA", "\u5F00\u6E9C"],
  // ── 技术编程（60组）──────────────────────────────────────────────────
  "Go": ["golang", "goroutine", "channel", "go\u8BED\u8A00"],
  "Rust": ["rust", "cargo", "crate", "borrow checker"],
  "Java": ["java", "jvm", "spring", "maven", "gradle"],
  "C++": ["cpp", "c plus plus", "\u6307\u9488", "stl"],
  "Swift": ["swift", "swiftui", "xcode", "ios\u5F00\u53D1"],
  "PHP": ["php", "laravel", "composer", "wordpress"],
  "Ruby": ["ruby", "rails", "gem", "rake"],
  "React": ["react", "jsx", "hooks", "redux", "\u524D\u7AEF\u6846\u67B6"],
  "Vue": ["vue", "vuex", "nuxt", "vue3"],
  "Angular": ["angular", "rxjs", "ngrx", "ng"],
  "TypeScript": ["ts", "typescript", "\u7C7B\u578B", "\u6CDB\u578B"],
  "SQL": ["sql", "\u67E5\u8BE2", "SELECT", "JOIN", "\u6570\u636E\u5E93\u67E5\u8BE2"],
  "Redis": ["redis", "\u7F13\u5B58", "cache", "key-value"],
  "MongoDB": ["mongo", "nosql", "\u6587\u6863\u6570\u636E\u5E93", "mongoose"],
  "PostgreSQL": ["pg", "postgres", "\u5173\u7CFB\u578B\u6570\u636E\u5E93", "psql"],
  "MySQL": ["mysql", "mariadb", "\u5173\u7CFB\u578B\u6570\u636E\u5E93"],
  "SQLite": ["sqlite", "sqlite3", "\u5D4C\u5165\u5F0F\u6570\u636E\u5E93", "\u8F7B\u91CF\u6570\u636E\u5E93"],
  "Kubernetes": ["k8s", "kubectl", "pod", "helm", "\u5BB9\u5668\u7F16\u6392"],
  "HTTP": ["http", "https", "\u8BF7\u6C42", "\u54CD\u5E94", "status code"],
  "REST": ["restful", "rest api", "\u63A5\u53E3\u8BBE\u8BA1"],
  "GraphQL": ["graphql", "query", "mutation", "schema"],
  "gRPC": ["grpc", "protobuf", "rpc"],
  "\u524D\u7AEF": ["frontend", "\u9875\u9762", "HTML", "CSS", "UI"],
  "\u540E\u7AEF": ["backend", "\u670D\u52A1\u7AEF", "\u63A5\u53E3", "server"],
  "\u5168\u6808": ["fullstack", "\u524D\u540E\u7AEF", "\u5168\u6808\u5F00\u53D1"],
  "\u7B97\u6CD5": ["algorithm", "\u6570\u636E\u7ED3\u6784", "\u5237\u9898", "leetcode"],
  "\u6570\u636E\u7ED3\u6784": ["\u94FE\u8868", "\u6811", "\u56FE", "\u54C8\u5E0C\u8868", "\u6808", "\u961F\u5217"],
  "\u90E8\u7F72": ["deploy", "\u4E0A\u7EBF", "\u53D1\u5E03", "\u8FD0\u7EF4", "CI/CD"],
  "\u8C03\u8BD5": ["debug", "\u6392\u67E5", "\u5B9A\u4F4D", "\u65AD\u70B9"],
  "bug": ["\u7F3A\u9677", "\u95EE\u9898", "\u6545\u969C", "\u62A5\u9519", "issue"],
  "\u4EE3\u7801\u5BA1\u67E5": ["code review", "CR", "\u5BA1\u4EE3\u7801", "review"],
  "\u91CD\u6784": ["refactor", "\u4F18\u5316\u4EE3\u7801", "\u91CD\u5199", "\u6539\u5584"],
  "\u6846\u67B6": ["framework", "\u5E93", "\u4E2D\u95F4\u4EF6", "library"],
  "\u5FAE\u670D\u52A1": ["microservice", "\u670D\u52A1\u62C6\u5206", "\u5206\u5E03\u5F0F", "SOA"],
  "\u6D88\u606F\u961F\u5217": ["MQ", "Kafka", "RabbitMQ", "\u961F\u5217"],
  "\u8D1F\u8F7D\u5747\u8861": ["load balancer", "nginx", "\u53CD\u5411\u4EE3\u7406", "LB"],
  "\u76D1\u63A7": ["monitoring", "\u544A\u8B66", "Prometheus", "Grafana"],
  "\u65E5\u5FD7": ["log", "\u65E5\u5FD7\u7CFB\u7EDF", "ELK", "\u65E5\u5FD7\u5206\u6790"],
  "\u6D4B\u8BD5": ["test", "\u5355\u5143\u6D4B\u8BD5", "\u96C6\u6210\u6D4B\u8BD5", "QA", "\u81EA\u52A8\u5316\u6D4B\u8BD5"],
  "\u6027\u80FD": ["performance", "\u4F18\u5316", "\u5E76\u53D1", "\u54CD\u5E94\u65F6\u95F4"],
  "\u5B89\u5168": ["security", "\u6F0F\u6D1E", "\u52A0\u5BC6", "\u8BA4\u8BC1", "\u9274\u6743"],
  "\u67B6\u6784": ["architecture", "\u8BBE\u8BA1\u6A21\u5F0F", "\u7CFB\u7EDF\u8BBE\u8BA1"],
  "\u4E91\u670D\u52A1": ["AWS", "\u963F\u91CC\u4E91", "\u817E\u8BAF\u4E91", "Azure", "GCP"],
  "\u670D\u52A1\u5668": ["server", "\u4E3B\u673A", "VPS", "\u4E91\u4E3B\u673A"],
  "Shell": ["bash", "zsh", "\u7EC8\u7AEF", "terminal", "\u547D\u4EE4\u884C"],
  "\u6B63\u5219": ["regex", "\u6B63\u5219\u8868\u8FBE\u5F0F", "\u5339\u914D", "pattern"],
  "\u722C\u866B": ["spider", "crawler", "\u6293\u53D6", "scrape"],
  "\u673A\u5668\u5B66\u4E60": ["ML", "\u6DF1\u5EA6\u5B66\u4E60", "AI", "\u6A21\u578B", "\u8BAD\u7EC3"],
  "\u5927\u6A21\u578B": ["LLM", "GPT", "Claude", "transformer", "\u5927\u8BED\u8A00\u6A21\u578B"],
  "\u5411\u91CF": ["embedding", "\u5411\u91CF\u6570\u636E\u5E93", "vector", "FAISS"],
  "Nginx": ["nginx", "\u53CD\u5411\u4EE3\u7406", "\u8D1F\u8F7D\u5747\u8861", "web\u670D\u52A1\u5668"],
  "\u7248\u672C\u63A7\u5236": ["git", "svn", "\u5206\u652F", "merge", "commit"],
  "CI/CD": ["\u6301\u7EED\u96C6\u6210", "\u6301\u7EED\u90E8\u7F72", "pipeline", "Jenkins", "GitHub Actions"],
  "\u5BB9\u5668": ["docker", "\u955C\u50CF", "image", "dockerfile"],
  "ORM": ["orm", "ActiveRecord", "SQLAlchemy", "Prisma"],
  "\u7F13\u5B58": ["cache", "Redis", "CDN", "\u6D4F\u89C8\u5668\u7F13\u5B58"],
  "\u5E76\u53D1": ["\u591A\u7EBF\u7A0B", "\u591A\u8FDB\u7A0B", "\u5F02\u6B65", "async", "goroutine"],
  "\u7F51\u7EDC": ["TCP", "UDP", "DNS", "IP", "socket", "\u7F51\u7EDC\u534F\u8BAE"],
  "\u52A0\u5BC6": ["encryption", "RSA", "AES", "HTTPS", "\u7B7E\u540D"],
  "\u5F00\u6E90": ["open source", "GitHub", "\u793E\u533A", "MIT", "Apache"],
  // ── 健康医疗（40组）──────────────────────────────────────────────────
  "\u5934\u75BC": ["\u5934\u75DB", "\u504F\u5934\u75DB", "\u8111\u888B\u75BC", "headache"],
  "\u611F\u5192": ["\u7740\u51C9", "\u6D41\u611F", "\u9F3B\u585E", "\u6253\u55B7\u568F", "cold"],
  "\u53D1\u70E7": ["\u53D1\u70ED", "\u9AD8\u70E7", "\u4F4E\u70E7", "\u4F53\u6E29\u9AD8", "fever"],
  "\u54B3\u55FD": ["\u54B3", "\u5E72\u54B3", "\u55D3\u5B50\u75D2", "cough"],
  "\u8FC7\u654F": ["\u76AE\u80A4\u75D2", "\u8FC7\u654F\u53CD\u5E94", "\u82B1\u7C89\u8FC7\u654F", "allergy"],
  "\u5931\u7720": ["\u7761\u4E0D\u7740", "\u96BE\u4EE5\u5165\u7761", "\u7FFB\u6765\u8986\u53BB", "insomnia", "\u7761\u7720\u4E0D\u597D", "\u7761\u7720\u8D28\u91CF"],
  "\u4F53\u68C0": ["\u68C0\u67E5", "\u68C0\u67E5\u8EAB\u4F53", "\u5E74\u5EA6\u4F53\u68C0", "\u5065\u5EB7\u68C0\u67E5"],
  "\u624B\u672F": ["\u5F00\u5200", "\u505A\u624B\u672F", "\u5FAE\u521B", "surgery"],
  "\u836F": ["\u5403\u836F", "\u7528\u836F", "\u5904\u65B9\u836F", "\u836F\u7269", "medicine"],
  "\u51CF\u80A5\u836F": ["\u51CF\u80A5\u4EA7\u54C1", "\u7626\u8EAB\u836F", "\u4EE3\u9910"],
  "\u86CB\u767D\u8D28": ["protein", "\u9E21\u80F8\u8089", "\u86CB\u767D"],
  "\u78B3\u6C34": ["\u78B3\u6C34\u5316\u5408\u7269", "\u4E3B\u98DF", "\u7CD6", "carb"],
  "\u8102\u80AA": ["\u6CB9\u8102", "\u80A5\u8089", "\u5361\u8DEF\u91CC", "fat"],
  "\u7EF4\u751F\u7D20": ["\u7EF4C", "\u7EF4D", "vitamin", "\u8425\u517B\u7D20"],
  "\u8840\u538B": ["\u9AD8\u8840\u538B", "\u4F4E\u8840\u538B", "\u91CF\u8840\u538B", "\u8840\u538B\u8BA1", "\u8840\u538B\u9AD8"],
  "\u8840\u7CD6": ["\u9AD8\u8840\u7CD6", "\u4F4E\u8840\u7CD6", "\u7CD6\u5C3F\u75C5", "\u6D4B\u8840\u7CD6"],
  "\u80C3\u75BC": ["\u80C3\u75DB", "\u80C3\u75C5", "\u6D88\u5316\u4E0D\u826F", "\u80C3\u708E"],
  "\u62C9\u809A\u5B50": ["\u8179\u6CFB", "\u80A0\u80C3\u708E", "\u6C34\u571F\u4E0D\u670D", "diarrhea"],
  "\u4FBF\u79D8": ["\u6392\u4FBF\u56F0\u96BE", "\u80A0\u9053\u4E0D\u901A", "\u901A\u4FBF"],
  "\u8170\u75BC": ["\u8170\u75DB", "\u8170\u9178", "\u8170\u690E", "\u4E45\u5750"],
  "\u9888\u690E": ["\u9888\u690E\u75C5", "\u8116\u5B50\u75BC", "\u80A9\u9888", "\u843D\u6795"],
  "\u8FD1\u89C6": ["\u89C6\u529B", "\u773C\u955C", "\u6563\u5149", "\u77EB\u6B63"],
  "\u7259\u75BC": ["\u7259\u75DB", "\u86C0\u7259", "\u667A\u9F7F", "\u770B\u7259"],
  "\u6253\u9488": ["\u6CE8\u5C04", "\u6253\u70B9\u6EF4", "\u8F93\u6DB2", "\u75AB\u82D7"],
  "\u4E2D\u836F": ["\u4E2D\u533B", "\u6C64\u836F", "\u9488\u7078", "\u8349\u836F"],
  "\u897F\u836F": ["\u897F\u533B", "\u6297\u751F\u7D20", "\u6D88\u708E\u836F"],
  "\u6838\u9178": ["\u6838\u9178\u68C0\u6D4B", "\u6297\u539F", "\u68C0\u6D4B"],
  "\u5065\u8EAB\u623F": ["gym", "\u64B8\u94C1", "\u5668\u68B0", "\u79C1\u6559"],
  "\u8DD1\u6B65\u673A": ["\u692D\u5706\u673A", "\u52A8\u611F\u5355\u8F66", "\u6709\u6C27\u5668\u68B0"],
  "\u8425\u517B": ["\u8425\u517B\u642D\u914D", "\u81B3\u98DF", "\u996E\u98DF\u5747\u8861", "nutrition"],
  "\u70ED\u91CF": ["\u5361\u8DEF\u91CC", "kcal", "\u70ED\u91CF\u6444\u5165", "\u57FA\u7840\u4EE3\u8C22"],
  "\u4F53\u91CD": ["\u79F0\u91CD", "\u79E4", "\u4F53\u8102", "BMI"],
  "\u5851\u5F62": ["\u8EAB\u6750", "\u589E\u808C", "\u7EBF\u6761", "\u9A6C\u7532\u7EBF"],
  "\u62C9\u4F38": ["\u67D4\u97E7\u6027", "\u7B4B\u819C", "\u6CE1\u6CAB\u8F74", "stretching"],
  "\u5FC3\u7387": ["\u5FC3\u8DF3", "\u8109\u640F", "\u6709\u6C27\u5FC3\u7387", "\u8FD0\u52A8\u624B\u8868"],
  "\u4FDD\u5065\u54C1": ["\u8865\u54C1", "\u4FDD\u5065", "\u81B3\u98DF\u8865\u5145\u5242"],
  "\u5EB7\u590D": ["\u590D\u5065", "\u7406\u7597", "\u6062\u590D", "rehab"],
  "\u6302\u53F7": ["\u9884\u7EA6\u6302\u53F7", "\u7F51\u4E0A\u6302\u53F7", "\u6392\u53F7"],
  "\u533B\u4FDD": ["\u533B\u7597\u4FDD\u9669", "\u62A5\u9500", "\u793E\u4FDD\u5361"],
  "\u5904\u65B9": ["\u5904\u65B9\u836F", "\u533B\u5631", "\u5F00\u836F"],
  // ── 教育学习（30组）──────────────────────────────────────────────────
  "\u8003\u8BD5": ["\u8003", "\u6D4B\u8BD5", "\u7B14\u8BD5", "exam"],
  "\u82F1\u8BED": ["English", "\u53E3\u8BED", "\u542C\u529B", "\u56DB\u516D\u7EA7", "\u96C5\u601D"],
  "\u6570\u5B66": ["math", "\u9AD8\u6570", "\u5FAE\u79EF\u5206", "\u7EBF\u6027\u4EE3\u6570"],
  "\u8BBA\u6587": ["paper", "\u6BD5\u4E1A\u8BBA\u6587", "\u5B66\u672F", "\u671F\u520A"],
  "\u8BFE\u7A0B": ["\u8BFE", "\u7F51\u8BFE", "\u516C\u5F00\u8BFE", "course"],
  "\u5927\u5B66": ["\u672C\u79D1", "\u9AD8\u6821", "\u5B66\u6821", "\u9AD8\u4E2D", "\u6821\u53CB", "university"],
  "\u7814\u7A76\u751F": ["\u7855\u58EB", "\u8BFB\u7814", "\u8003\u7814", "\u7814\u4E00"],
  "\u7559\u5B66": ["\u51FA\u56FD", "\u7559\u5B66\u7533\u8BF7", "\u6D77\u5916", "study abroad"],
  "\u8BC1\u4E66": ["\u8BA4\u8BC1", "\u8003\u8BC1", "\u8D44\u683C\u8BC1", "\u8BC1"],
  "\u5237\u9898": ["\u505A\u9898", "\u7EC3\u4E60", "\u9898\u5E93", "leetcode"],
  "\u8003\u7814": ["\u7814\u7A76\u751F\u8003\u8BD5", "\u5907\u8003", "\u8003\u7814\u515A"],
  "\u8003\u516C": ["\u516C\u52A1\u5458\u8003\u8BD5", "\u4E8B\u4E1A\u7F16", "\u56FD\u8003", "\u7701\u8003"],
  "\u96C5\u601D": ["IELTS", "\u51FA\u56FD\u8003\u8BD5", "\u8BED\u8A00\u8003\u8BD5"],
  "\u6258\u798F": ["TOEFL", "\u7559\u5B66\u8003\u8BD5", "\u82F1\u8BED\u8003\u8BD5"],
  "GPA": ["\u7EE9\u70B9", "\u6210\u7EE9", "\u5B66\u5206"],
  "\u6BD5\u4E1A": ["\u6BD5\u4E1A\u5178\u793C", "\u7B54\u8FA9", "\u6BD5\u4E1A\u5B63"],
  "\u5B66\u8D39": ["tuition", "\u6559\u80B2\u8D39\u7528", "\u4E66\u8D39"],
  "\u5956\u5B66\u91D1": ["scholarship", "\u52A9\u5B66\u91D1", "\u8865\u52A9"],
  "\u5BFC\u5E08": ["mentor", "\u8001\u5E08", "\u6559\u6388", "\u6307\u5BFC"],
  "\u5B9E\u9A8C\u5BA4": ["lab", "\u5B9E\u9A8C", "\u79D1\u7814"],
  "\u56FE\u4E66\u9986": ["library", "\u81EA\u4E60\u5BA4", "\u9605\u89C8\u5BA4"],
  "\u7F51\u8BFE": ["\u5728\u7EBF\u8BFE\u7A0B", "\u76F4\u64AD\u8BFE", "\u5F55\u64AD\u8BFE", "MOOC"],
  "\u7F16\u7A0B\u8BFE": ["\u7F16\u7A0B\u57F9\u8BAD", "\u7F16\u7A0B\u5B66\u4E60", "\u4EE3\u7801\u8BAD\u7EC3\u8425", "bootcamp"],
  "\u5B66\u5386": ["\u6587\u51ED", "\u5B66\u4F4D", "\u672C\u79D1", "\u7855\u58EB"],
  "\u8F85\u5BFC": ["\u8865\u8BFE", "\u5BB6\u6559", "\u8F85\u5BFC\u73ED", "\u57F9\u4F18"],
  "\u7B14\u8BB0": ["\u8BFE\u5802\u7B14\u8BB0", "\u5B66\u4E60\u7B14\u8BB0", "\u8BB0\u5F55", "note"],
  "\u590D\u4E60": ["\u6E29\u4E60", "\u56DE\u987E", "\u5907\u8003", "review"],
  "\u9884\u4E60": ["\u63D0\u524D\u5B66", "\u81EA\u5B66"],
  "\u4F5C\u4E1A": ["homework", "\u7EC3\u4E60", "\u4F5C\u4E1A\u672C", "\u5199\u4F5C\u4E1A"],
  "\u9605\u8BFB": ["\u7CBE\u8BFB", "\u6CDB\u8BFB", "\u770B\u4E66", "\u8BFB"],
  // ── 财务理财（30组）──────────────────────────────────────────────────
  "\u6536\u5165": ["\u8FDB\u8D26", "\u5165\u8D26", "\u5230\u624B", "income"],
  "\u82B1\u8D39": ["\u5F00\u9500", "\u652F\u51FA", "\u6D88\u8D39", "expense"],
  "\u623F\u8D37": ["\u6708\u4F9B", "\u6309\u63ED", "\u8D37\u6B3E", "mortgage"],
  "\u4FE1\u7528\u5361": ["\u5237\u5361", "\u8FD8\u6B3E", "\u8D26\u5355", "\u4FE1\u7528\u989D\u5EA6"],
  "\u57FA\u91D1": ["\u5B9A\u6295", "\u6307\u6570\u57FA\u91D1", "\u7406\u8D22\u4EA7\u54C1", "fund"],
  "\u80A1\u7968": ["\u7092\u80A1", "\u80A1\u5E02", "A\u80A1", "\u7F8E\u80A1", "stock"],
  "\u4FDD\u9669": ["\u6295\u4FDD", "\u4FDD\u5355", "\u7406\u8D54", "\u8F66\u9669", "\u533B\u7597\u9669", "\u5BFF\u9669", "insurance"],
  "\u517B\u8001": ["\u517B\u8001\u91D1", "\u9000\u4F11\u91D1", "\u9000\u4F11", "\u793E\u4FDD", "\u8001\u5E74", "pension"],
  "\u516C\u79EF\u91D1": ["\u4F4F\u623F\u516C\u79EF\u91D1", "\u63D0\u53D6\u516C\u79EF\u91D1", "\u516C\u79EF\u91D1\u8D37\u6B3E"],
  "\u5B58\u6B3E": ["\u50A8\u84C4", "\u5B9A\u671F", "\u6D3B\u671F", "\u5B58\u94B1"],
  "\u6295\u8D44": ["\u7406\u8D22", "\u589E\u503C", "\u8D44\u4EA7\u914D\u7F6E", "\u57FA\u91D1", "\u80A1\u7968", "\u7092\u80A1", "\u5B9A\u6295", "invest"],
  "\u7406\u8D22": ["\u8D22\u52A1\u7BA1\u7406", "\u8D44\u4EA7\u7BA1\u7406", "\u94B1\u751F\u94B1"],
  "\u5229\u606F": ["\u5229\u7387", "\u5E74\u5316", "\u6536\u76CA\u7387", "interest"],
  "\u8D37\u6B3E": ["\u501F\u94B1", "\u501F\u8D37", "\u5206\u671F", "\u623F\u8D37", "\u8F66\u8D37", "\u8FD8\u6B3E", "\u6708\u4F9B", "loan"],
  "\u8FD8\u6B3E": ["\u8FD8\u94B1", "\u8FD8\u8D37", "\u6708\u4F9B"],
  "\u8D26\u5355": ["\u5BF9\u8D26", "\u6D41\u6C34", "\u660E\u7EC6", "bill"],
  "\u9884\u7B97": ["\u82B1\u8D39\u8BA1\u5212", "\u5F00\u652F\u9884\u7B97", "budget"],
  "\u7701\u94B1": ["\u8282\u7701", "\u8282\u7EA6", "\u7701\u7740\u82B1"],
  "\u8D1F\u503A": ["\u6B20\u94B1", "\u6B20\u6B3E", "\u8D1F\u8D44\u4EA7", "debt"],
  "\u8BB0\u8D26": ["\u8D26\u672C", "\u8BB0\u5F55\u652F\u51FA", "\u8D26\u76EE"],
  "\u7A0E": ["\u4E2A\u7A0E", "\u6240\u5F97\u7A0E", "\u7A0E\u7387", "tax"],
  "\u6C47\u7387": ["\u5916\u6C47", "\u6362\u6C47", "\u7F8E\u5143", "\u6C47\u5151"],
  "\u6BD4\u7279\u5E01": ["BTC", "\u52A0\u5BC6\u8D27\u5E01", "crypto", "\u5E01\u5708"],
  "\u6570\u5B57\u8D27\u5E01": ["\u865A\u62DF\u8D27\u5E01", "USDT", "\u533A\u5757\u94FE"],
  "\u5B9A\u6295": ["\u57FA\u91D1\u5B9A\u6295", "\u5B9A\u671F\u6295\u8D44", "\u957F\u671F\u6301\u6709"],
  "\u5206\u7EA2": ["\u80A1\u606F", "\u7EA2\u5229", "\u6D3E\u606F", "dividend"],
  "\u4E8F\u635F": ["\u4E8F\u94B1", "\u8D54\u94B1", "\u6D6E\u4E8F", "loss"],
  "\u76C8\u5229": ["\u8D5A\u94B1", "\u76C8\u4F59", "\u56DE\u62A5", "profit"],
  "\u901A\u80C0": ["\u901A\u8D27\u81A8\u80C0", "\u7269\u4EF7\u4E0A\u6DA8", "\u8D2C\u503C", "inflation"],
  "\u8D22\u52A1\u81EA\u7531": ["FIRE", "\u7ECF\u6D4E\u81EA\u7531", "\u9000\u4F11\u81EA\u7531"],
  // ── 家庭关系（30组）──────────────────────────────────────────────────
  "\u7238\u7238": ["\u7236\u4EB2", "\u7239", "\u8001\u7238", "\u8001\u7239", "\u51C6\u7238\u7238", "\u7238", "\u5F53\u7238\u7238", "dad"],
  "\u5988\u5988": ["\u6BCD\u4EB2", "\u5A18", "\u8001\u5988", "mom"],
  "\u8001\u516C": ["\u4E08\u592B", "\u5148\u751F", "\u53E6\u4E00\u534A", "husband"],
  "\u513F\u5B50": ["\u7537\u5B69", "\u5C0F\u5B50", "\u5D3D", "son"],
  "\u5973\u513F": ["\u5973\u5B69", "\u95FA\u5973", "\u4E2B\u5934", "daughter"],
  "\u54E5\u54E5": ["\u5144", "\u5927\u54E5", "\u8001\u54E5", "brother"],
  "\u59D0\u59D0": ["\u59D0", "\u5927\u59D0", "\u8001\u59D0", "sister"],
  "\u5F1F\u5F1F": ["\u5F1F", "\u5C0F\u5F1F", "\u8001\u5F1F"],
  "\u59B9\u59B9": ["\u59B9", "\u5C0F\u59B9", "\u59B9\u5B50"],
  "\u7237\u7237": ["\u7956\u7236", "\u5916\u516C", "\u59E5\u7237", "grandfather"],
  "\u5976\u5976": ["\u7956\u6BCD", "\u5916\u5A46", "\u59E5\u59E5", "grandmother"],
  "\u670B\u53CB": ["\u597D\u53CB", "\u54E5\u4EEC", "\u95FA\u871C", "\u4F19\u4F34", "\u5144\u5F1F", "\u6B7B\u515A", "friend"],
  "\u540C\u5B66": ["\u540C\u7A97", "\u6821\u53CB", "\u5B66\u957F", "\u5B66\u59D0", "classmate"],
  "\u90BB\u5C45": ["\u9694\u58C1", "\u90BB\u91CC", "\u697C\u4E0A\u697C\u4E0B", "neighbor"],
  "\u4EB2\u621A": ["\u4EB2\u5C5E", "\u5BB6\u4EBA", "\u5BB6\u65CF"],
  "\u53D4\u53D4": ["\u5927\u53D4", "\u8205\u8205", "\u4F2F\u4F2F", "uncle"],
  "\u963F\u59E8": ["\u5927\u59E8", "\u59D1\u59D1", "\u5A76\u5A76", "aunt"],
  "\u5B9D\u5B9D": ["\u5C0F\u5A74\u513F", "\u5A03\u5A03", "\u5B9D\u8D1D", "\u5A74\u513F", "\u65B0\u751F\u513F", "\u5A03", "baby"],
  "\u7236\u6BCD": ["\u7238\u5988", "\u53CC\u4EB2", "\u5BB6\u957F", "\u7238\u7238", "\u5988\u5988", "\u7236\u4EB2", "\u6BCD\u4EB2", "parents"],
  "\u5BB6\u4EBA": ["\u5BB6\u5EAD", "\u5BB6\u65CF", "\u5BB6\u91CC\u4EBA", "family"],
  "\u5973\u670B\u53CB": ["\u5973\u53CB", "\u5BF9\u8C61", "\u5AB3\u5987"],
  "\u7537\u670B\u53CB": ["\u7537\u53CB", "\u5BF9\u8C61", "\u8001\u516C"],
  "\u5BF9\u8C61": ["\u5973\u670B\u53CB", "\u7537\u670B\u53CB", "\u5973\u53CB", "\u7537\u53CB", "\u4F34\u4FA3", "\u53E6\u4E00\u534A"],
  "\u60C5\u4FA3": ["\u7537\u5973\u670B\u53CB", "\u5BF9\u8C61", "\u604B\u4EBA", "couple"],
  "\u524D\u4EFB": ["\u524D\u7537\u53CB", "\u524D\u5973\u53CB", "\u524D\u5BF9\u8C61", "ex"],
  "\u6697\u604B": ["\u5355\u604B", "\u6697\u604B\u5BF9\u8C61", "\u6084\u6084\u559C\u6B22"],
  "\u8868\u767D": ["\u544A\u767D", "\u8BF4\u559C\u6B22", "\u8FFD", "confess"],
  "\u5206\u624B": ["\u5206\u4E86", "\u6563\u4E86", "\u63B0\u4E86", "break up"],
  "\u7ED3\u5A5A": ["\u5A5A\u793C", "\u5A5A\u59FB", "\u9886\u8BC1", "\u5AC1", "\u5A36", "marry"],
  "\u79BB\u5A5A": ["\u79BB\u4E86", "\u5206\u5F00", "\u79BB\u5F02", "\u6563\u4E86", "\u4E0D\u8FC7\u4E86", "divorce"],
  "\u5A46\u5AB3": ["\u5A46\u5A46", "\u513F\u5AB3", "\u5A46\u5AB3\u5173\u7CFB"],
  "\u80B2\u513F": ["\u517B\u5A03", "\u5E26\u5B69\u5B50", "\u6559\u80B2\u5B69\u5B50", "parenting"],
  "\u966A\u4F34": ["\u5728\u4E00\u8D77", "\u966A", "\u76F8\u4F34", "companion"],
  // ── 住房出行（30组）──────────────────────────────────────────────────
  "\u79DF\u623F": ["\u79DF", "\u623F\u79DF", "\u5408\u79DF", "\u6574\u79DF", "\u62BC\u91D1", "\u4E2D\u4ECB", "rent"],
  "\u4E70\u623F": ["\u8D2D\u623F", "\u9996\u4ED8", "\u623F\u4EA7", "\u65B0\u623F"],
  "\u623F\u4EF7": ["\u623F\u4EF7\u8D70\u52BF", "\u5747\u4EF7", "\u697C\u76D8", "\u5730\u6BB5"],
  "\u5730\u94C1": ["\u5730\u94C1\u7AD9", "\u6362\u4E58", "\u65E9\u9AD8\u5CF0", "subway"],
  "\u516C\u4EA4": ["\u516C\u4EA4\u8F66", "\u5750\u516C\u4EA4", "\u516C\u4EA4\u7AD9", "bus"],
  "\u6253\u8F66": ["\u53EB\u8F66", "\u51FA\u79DF\u8F66", "\u7F51\u7EA6\u8F66", "\u6EF4\u6EF4"],
  "\u5F00\u8F66": ["\u81EA\u9A7E", "\u9A7E\u9A76", "\u9A7E\u8F66", "drive"],
  "\u9AD8\u94C1": ["\u706B\u8F66", "\u52A8\u8F66", "\u94C1\u8DEF", "12306"],
  "\u98DE\u673A": ["\u822A\u73ED", "\u673A\u7968", "\u767B\u673A", "\u822A\u7A7A", "flight"],
  "\u9152\u5E97": ["\u5BBE\u9986", "\u6C11\u5BBF", "\u4F4F\u5BBF", "hotel"],
  "\u8F66\u4F4D": ["\u505C\u8F66\u4F4D", "\u505C\u8F66\u573A", "\u5730\u4E0B\u8F66\u5E93"],
  "\u7269\u4E1A": ["\u7269\u4E1A\u8D39", "\u7269\u4E1A\u7BA1\u7406", "\u4E1A\u4E3B\u59D4\u5458\u4F1A"],
  "\u4E8C\u624B\u623F": ["\u4E8C\u624B", "\u5B58\u91CF\u623F", "\u6302\u724C"],
  "\u5B66\u533A\u623F": ["\u5B66\u533A", "\u5212\u7247", "\u5BF9\u53E3\u5B66\u6821"],
  "\u65B0\u623F": ["\u671F\u623F", "\u73B0\u623F", "\u6837\u677F\u95F4"],
  "\u9996\u4ED8": ["\u9996\u4ED8\u6B3E", "\u4ED8\u9996\u4ED8", "\u9996\u4ED8\u6BD4\u4F8B"],
  "\u8D37\u6B3E\u5229\u7387": ["\u623F\u8D37\u5229\u7387", "LPR", "\u5229\u7387\u4E0B\u8C03"],
  "\u901A\u52E4": ["\u4E0A\u4E0B\u73ED", "\u901A\u52E4\u65F6\u95F4", "\u8DDD\u79BB"],
  "\u5BFC\u822A": ["\u5730\u56FE", "\u767E\u5EA6\u5730\u56FE", "\u9AD8\u5FB7", "GPS"],
  "\u8FDD\u7AE0": ["\u7F5A\u5355", "\u6263\u5206", "\u8D85\u901F", "\u95EF\u7EA2\u706F"],
  "\u9A7E\u7167": ["\u9A7E\u9A76\u8BC1", "\u8003\u9A7E\u7167", "\u79D1\u76EE", "\u5B66\u8F66"],
  "\u7535\u52A8\u8F66": ["\u7535\u74F6\u8F66", "\u7535\u52A8\u81EA\u884C\u8F66", "\u5145\u7535"],
  "\u5171\u4EAB\u5355\u8F66": ["\u54C8\u5570", "\u7F8E\u56E2\u5355\u8F66", "\u9752\u6854"],
  "\u9650\u53F7": ["\u5C3E\u53F7\u9650\u884C", "\u5355\u53CC\u53F7", "\u9650\u884C"],
  "\u8DEF\u51B5": ["\u5835\u4E0D\u5835", "\u8DEF\u51B5\u4FE1\u606F", "\u62E5\u5835"],
  "\u9AD8\u901F": ["\u9AD8\u901F\u516C\u8DEF", "\u6536\u8D39\u7AD9", "ETC"],
  "\u7B7E\u8BC1": ["visa", "\u529E\u7B7E\u8BC1", "\u7B7E\u8BC1\u7533\u8BF7"],
  "\u62A4\u7167": ["passport", "\u529E\u62A4\u7167", "\u51FA\u5883"],
  "\u884C\u674E": ["\u884C\u674E\u7BB1", "\u62C9\u6746\u7BB1", "\u6536\u62FE\u884C\u674E", "luggage"],
  "\u6C11\u5BBF": ["airbnb", "\u77ED\u79DF", "\u5BA2\u6808"],
  // ── 饮食烹饪（30组）──────────────────────────────────────────────────
  "\u7C73\u996D": ["\u767D\u996D", "\u5927\u7C73", "\u84B8\u996D", "rice"],
  "\u9762\u6761": ["\u9762", "\u62C9\u9762", "\u610F\u9762", "\u6302\u9762", "noodle"],
  "\u706B\u9505": ["\u6DAE\u9505", "\u81EA\u52A9\u706B\u9505", "\u9EBB\u8FA3\u9505", "hotpot"],
  "\u70E7\u70E4": ["\u64B8\u4E32", "BBQ", "\u70E4\u4E32", "\u70E4\u8089"],
  "\u5496\u5561": ["coffee", "\u62FF\u94C1", "\u7F8E\u5F0F", "\u661F\u5DF4\u514B", "\u745E\u5E78"],
  "\u5976\u8336": ["\u8336\u996E", "\u559C\u8336", "\u871C\u96EA\u51B0\u57CE", "\u73CD\u73E0\u5976\u8336"],
  "\u5564\u9152": ["beer", "\u7CBE\u917F", "\u624E\u5564", "\u51B0\u5564"],
  "\u6C34\u679C": ["fruit", "\u82F9\u679C", "\u9999\u8549", "\u6A58\u5B50", "\u8461\u8404"],
  "\u852C\u83DC": ["\u9752\u83DC", "\u852C", "\u83DC", "vegetable"],
  "\u8089": ["\u732A\u8089", "\u725B\u8089", "\u9E21\u8089", "\u7F8A\u8089", "meat"],
  "\u9C7C": ["\u9C7C\u8089", "\u9C7C\u7C7B", "\u6D77\u9C7C", "\u6DE1\u6C34\u9C7C", "fish"],
  "\u9E21\u86CB": ["\u86CB", "\u9E21\u86CB", "\u86CB\u7C7B", "egg"],
  "\u997A\u5B50": ["\u6C34\u997A", "\u5305\u997A\u5B50", "\u84B8\u997A", "dumpling"],
  "\u5305\u5B50": ["\u9992\u5934", "\u8089\u5305", "\u84B8\u5305"],
  "\u7CA5": ["\u7A00\u996D", "\u516B\u5B9D\u7CA5", "\u767D\u7CA5"],
  "\u7092\u83DC": ["\u7092", "\u7206\u7092", "\u6E05\u7092", "\u5C0F\u7092"],
  "\u7EA2\u70E7": ["\u7EA2\u70E7\u8089", "\u7EA2\u70E7\u9C7C", "\u7116\u716E"],
  "\u7172\u6C64": ["\u7096\u6C64", "\u6C64", "\u8001\u706B\u6C64", "\u9753\u6C64"],
  "\u51C9\u83DC": ["\u51C9\u62CC", "\u51B7\u76D8", "\u62CD\u9EC4\u74DC"],
  "\u751C\u70B9": ["dessert", "\u86CB\u7CD5", "\u751C\u54C1", "\u51B0\u6DC7\u6DCB"],
  "\u96F6\u98DF": ["snack", "\u85AF\u7247", "\u997C\u5E72", "\u575A\u679C"],
  "\u8C03\u6599": ["\u9171\u6CB9", "\u76D0", "\u918B", "\u8FA3\u6912", "seasoning"],
  "\u8FA3": ["\u8FA3\u6912", "\u9EBB\u8FA3", "\u5FAE\u8FA3", "\u53D8\u6001\u8FA3", "spicy"],
  "\u9178": ["\u918B", "\u9178\u5473", "\u67E0\u6AAC", "sour"],
  "\u751C": ["\u7CD6", "\u751C\u5473", "\u8702\u871C", "sweet"],
  "\u82E6": ["\u82E6\u5473", "\u82E6\u74DC", "\u82E6\u53E3", "bitter"],
  "\u70B9\u9910": ["\u70B9\u5916\u5356", "\u5916\u9001", "\u914D\u9001"],
  "\u98DF\u5802": ["\u996D\u5802", "\u98DF\u5802\u996D", "\u5DE5\u4F5C\u9910"],
  "\u4E0B\u53A8": ["\u505A\u996D", "\u81EA\u5DF1\u505A", "\u5728\u5BB6\u505A"],
  "\u98DF\u8C31": ["\u83DC\u8C31", "\u505A\u6CD5", "\u914D\u65B9", "recipe"],
  // ── 娱乐休闲（30组）──────────────────────────────────────────────────
  "\u7535\u89C6\u5267": ["\u5267", "\u8FDE\u7EED\u5267", "\u7F51\u5267", "TV series"],
  "\u7EFC\u827A": ["\u7EFC\u827A\u8282\u76EE", "\u771F\u4EBA\u79C0", "\u9009\u79C0", "variety show"],
  "\u52A8\u6F2B": ["\u52A8\u753B", "\u756A\u5267", "\u4E8C\u6B21\u5143", "anime"],
  "\u5C0F\u8BF4": ["\u7F51\u6587", "\u5C0F\u8BF4\u4E66", "\u770B\u5C0F\u8BF4", "novel"],
  "\u6E38\u620F": ["game", "\u624B\u6E38", "\u7AEF\u6E38", "\u4E3B\u673A\u6E38\u620F"],
  "\u6444\u5F71": ["\u62CD\u7167", "\u5355\u53CD", "\u76F8\u673A", "photography"],
  "\u5065\u8EAB": ["gym", "\u529B\u91CF\u8BAD\u7EC3", "\u6709\u6C27", "\u64B8\u94C1"],
  "\u745C\u4F3D": ["yoga", "\u51A5\u60F3", "\u62C9\u4F38", "\u6B63\u5FF5"],
  "\u753B\u753B": ["\u7ED8\u753B", "\u7D20\u63CF", "\u6C34\u5F69", "drawing"],
  "\u4E66\u6CD5": ["\u6BDB\u7B14", "\u7EC3\u5B57", "\u5B57\u5E16", "calligraphy"],
  "\u4E50\u5668": ["\u5409\u4ED6", "\u94A2\u7434", "\u8D1D\u65AF", "\u67B6\u5B50\u9F13"],
  "\u76F4\u64AD": ["live", "\u4E3B\u64AD", "\u76F4\u64AD\u95F4", "\u5E26\u8D27"],
  "\u77ED\u89C6\u9891": ["\u6296\u97F3", "\u5FEB\u624B", "vlog", "B\u7AD9"],
  "\u64AD\u5BA2": ["podcast", "\u64AD\u5BA2\u8282\u76EE", "\u6709\u58F0"],
  "\u684C\u6E38": ["\u5267\u672C\u6740", "\u72FC\u4EBA\u6740", "\u4E09\u56FD\u6740", "board game"],
  "\u5BC6\u5BA4": ["\u5BC6\u5BA4\u9003\u8131", "\u6C89\u6D78\u5F0F", "\u4F53\u9A8C\u9986"],
  "\u9732\u8425": ["camping", "\u5E10\u7BF7", "\u91CE\u9910", "\u6237\u5916"],
  "\u6ED1\u96EA": ["skiing", "\u96EA\u573A", "\u6ED1\u677F"],
  "\u6F5C\u6C34": ["diving", "\u6D6E\u6F5C", "\u6DF1\u6F5C"],
  "\u51B2\u6D6A": ["surfing", "\u6D6A", "\u6C34\u4E0A\u8FD0\u52A8"],
  "\u6500\u5CA9": ["climbing", "\u62B1\u77F3", "\u5CA9\u58C1"],
  "\u8DD1\u56E2": ["TRPG", "\u8DD1\u56E2\u6E38\u620F", "DND"],
  "\u624B\u529E": ["\u6A21\u578B", "\u76F2\u76D2", "\u6F6E\u73A9", "figure"],
  "\u8FFD\u661F": ["\u7C89\u4E1D", "\u5076\u50CF", "\u996D\u5708", "fan"],
  "\u6F14\u5531\u4F1A": ["concert", "\u97F3\u4E50\u8282", "\u770B\u6F14\u51FA", "\u73B0\u573A"],
  "\u5C55\u89C8": ["\u5C55", "\u7F8E\u672F\u9986", "\u535A\u7269\u9986", "exhibition"],
  "KTV": ["\u5531\u6B4C", "K\u6B4C", "\u9EA6\u9738"],
  "\u9EBB\u5C06": ["\u68CB\u724C", "\u6253\u724C", "\u6253\u9EBB\u5C06", "\u6413\u9EBB"],
  "\u5267\u672C\u6740": ["\u5267\u672C", "\u63A8\u7406", "\u672C\u683C"],
  "\u5BA0\u7269": ["\u732B", "\u72D7", "\u5BA0\u7269\u5E97", "pet", "\u732B\u54AA", "\u72D7\u72D7"],
  // ── 通用形容（40组）──────────────────────────────────────────────────
  "\u4E0D\u9519": ["\u633A\u597D", "\u8FD8\u884C", "\u53EF\u4EE5", "\u884C"],
  "\u68D2": ["\u8D5E", "\u5389\u5BB3", "\u725B\u903C", "\u7ED9\u529B", "awesome"],
  "\u7CDF\u7CD5": ["\u5B8C\u86CB", "\u60E8\u4E86", "\u574F\u4E86", "\u7CDF\u4E86"],
  "\u591A": ["\u5F88\u591A", "\u4E00\u5927\u5806", "\u4E0D\u5C11", "\u5927\u91CF"],
  "\u5C11": ["\u4E0D\u591A", "\u5F88\u5C11", "\u7A00\u5C11", "\u4EC5\u6709"],
  "\u8FDC": ["\u9065\u8FDC", "\u5F88\u8FDC", "\u8DEF\u7A0B\u957F", "far"],
  "\u8FD1": ["\u5F88\u8FD1", "\u9644\u8FD1", "\u4E0D\u8FDC", "near"],
  "\u96BE": ["\u56F0\u96BE", "\u4E0D\u5BB9\u6613", "\u8D39\u52B2", "difficult"],
  "\u7B80\u5355": ["\u5BB9\u6613", "\u4E0D\u96BE", "\u8F7B\u677E", "easy"],
  "\u590D\u6742": ["\u9EBB\u70E6", "\u7E41\u7410", "\u590D\u6742\u5EA6\u9AD8", "complex"],
  "\u91CD\u8981": ["\u5173\u952E", "\u8981\u7D27", "\u6838\u5FC3", "important"],
  "\u6709\u8DA3": ["\u597D\u73A9", "\u6709\u610F\u601D", "\u6709\u6897", "interesting"],
  "\u70ED": ["\u708E\u70ED", "\u95F7\u70ED", "\u9AD8\u6E29", "hot"],
  "\u51B7": ["\u5BD2\u51B7", "\u51B0\u51B7", "\u96F6\u4E0B", "cold"],
  "\u65B0": ["\u5D2D\u65B0", "\u6700\u65B0", "\u5168\u65B0", "new"],
  "\u65E7": ["\u8001\u65E7", "\u8FC7\u65F6", "\u8001\u7684", "old"],
  "\u9AD8": ["\u5F88\u9AD8", "\u504F\u9AD8", "\u5C45\u9AD8\u4E0D\u4E0B", "high"],
  "\u4F4E": ["\u504F\u4F4E", "\u5F88\u4F4E", "\u4E0D\u9AD8", "low"],
  "\u957F": ["\u5F88\u957F", "\u5197\u957F", "\u65F6\u95F4\u957F", "long"],
  "\u77ED": ["\u5F88\u77ED", "\u7B80\u77ED", "\u65F6\u95F4\u77ED", "short"],
  "\u5E72\u51C0": ["\u6574\u6D01", "\u6E05\u723D", "\u4E00\u5C18\u4E0D\u67D3", "clean"],
  "\u810F": ["\u80AE\u810F", "\u4E0D\u5E72\u51C0", "\u908B\u9062", "dirty"],
  "\u6F02\u4EAE": ["\u597D\u770B", "\u7F8E\u4E3D", "\u989C\u503C\u9AD8", "\u517B\u773C", "beautiful"],
  "\u4E11": ["\u96BE\u770B", "\u4E11\u964B", "\u4E0D\u597D\u770B", "ugly"],
  "\u806A\u660E": ["\u667A\u6167", "\u673A\u7075", "\u8111\u5B50\u597D\u4F7F", "smart"],
  "\u7B28": ["\u8822", "\u8FDF\u949D", "\u8111\u5B50\u4E0D\u597D\u4F7F", "stupid"],
  "\u5B89\u9759": ["\u9759", "\u6E05\u9759", "\u5B89\u9759\u4E00\u4E0B", "quiet"],
  "\u5435": ["\u5608\u6742", "\u5435\u95F9", "\u95F9\u817E", "noisy"],
  "\u5FD9": ["\u7E41\u5FD9", "\u6CA1\u7A7A", "\u4E8B\u60C5\u591A", "busy"],
  "\u95F2": ["\u7A7A\u95F2", "\u6CA1\u4E8B", "\u6709\u7A7A", "free"],
  "\u539A": ["\u539A\u5B9E", "\u5F88\u539A", "\u539A\u91CD"],
  "\u8584": ["\u5F88\u8584", "\u8584\u8584\u7684", "\u5355\u8584"],
  "\u786C": ["\u575A\u786C", "\u5F88\u786C", "\u786C\u90A6\u90A6"],
  "\u8F6F": ["\u67D4\u8F6F", "\u5F88\u8F6F", "\u8F6F\u7EF5\u7EF5"],
  "\u4EAE": ["\u660E\u4EAE", "\u5149\u4EAE", "\u53D1\u5149", "bright"],
  "\u6697": ["\u9ED1\u6697", "\u660F\u6697", "\u7070\u6697", "dark"],
  "\u9999": ["\u597D\u95FB", "\u9999\u5473", "\u82B3\u9999", "fragrant"],
  "\u81ED": ["\u96BE\u95FB", "\u81ED\u5473", "\u6076\u81ED", "stink"],
  "\u6B63\u5E38": ["\u6CA1\u6BDB\u75C5", "\u6B63\u5E38\u7684", "\u4E00\u5207\u6B63\u5E38", "normal"],
  "\u5947\u602A": ["\u602A", "\u8BE1\u5F02", "\u4E0D\u6B63\u5E38", "\u79BB\u8C31", "weird"],
  // ── English synonym groups ──────────────────────────────────────────────
  "happy": ["glad", "cheerful", "joyful", "pleased", "delighted"],
  "sad": ["unhappy", "depressed", "down", "miserable", "upset"],
  "angry": ["mad", "furious", "annoyed", "irritated", "pissed"],
  "work": ["job", "office", "career", "employment", "workplace"],
  "home": ["house", "apartment", "residence", "place"],
  "food": ["meal", "eat", "dinner", "lunch", "breakfast", "snack"],
  "health": ["fitness", "exercise", "workout", "medical", "wellness"],
  "money": ["salary", "income", "budget", "savings", "pay", "wage"],
  "family": ["parents", "children", "kids", "relatives", "siblings"],
  "friend": ["buddy", "mate", "pal", "colleague", "peer"],
  "learn": ["study", "practice", "training", "course", "tutorial"],
  "travel": ["trip", "vacation", "holiday", "journey", "flight"],
  "code": ["programming", "coding", "development", "software", "dev"],
  "bug": ["error", "issue", "problem", "crash", "failure", "glitch"],
  "deploy": ["release", "ship", "publish", "launch", "rollout"],
  "database": ["db", "sql", "postgres", "mysql", "mongo", "redis"],
  "frontend": ["ui", "react", "vue", "css", "html", "web"],
  "backend": ["server", "api", "rest", "graphql", "microservice"],
  "tired": ["exhausted", "drained", "burnt", "burnout", "fatigue"],
  "stressed": ["anxious", "overwhelmed", "pressure", "tense"],
  "excited": ["thrilled", "pumped", "stoked", "hyped", "eager"],
  "boring": ["dull", "tedious", "monotonous", "uninteresting"],
  "difficult": ["hard", "tough", "challenging", "tricky", "complex"],
  "easy": ["simple", "straightforward", "effortless", "trivial"],
  "expensive": ["costly", "pricey", "overpriced"],
  "cheap": ["affordable", "budget", "bargain", "inexpensive"],
  // ── English cold-start synonyms (200+ groups) ──────────────────────────
  // Emotions & feelings
  "happy": ["glad", "joyful", "cheerful", "pleased", "delighted", "content"],
  "sad": ["unhappy", "depressed", "down", "miserable", "heartbroken", "upset"],
  "angry": ["mad", "furious", "annoyed", "irritated", "pissed", "outraged"],
  "afraid": ["scared", "frightened", "terrified", "fearful", "phobia", "phobias"],
  "worried": ["concerned", "anxious", "nervous", "uneasy", "apprehensive"],
  "lonely": ["alone", "isolated", "solitary", "lonesome"],
  "proud": ["accomplished", "fulfilled", "satisfied", "achieved"],
  "confused": ["puzzled", "bewildered", "lost", "unsure"],
  "grateful": ["thankful", "appreciative", "blessed"],
  "frustrated": ["stuck", "blocked", "hitting a wall", "can't figure out"],
  // Health & body
  "sick": ["ill", "unwell", "not feeling well", "under the weather"],
  "pain": ["ache", "hurt", "sore", "discomfort", "chronic"],
  "allergy": ["allergic", "allergies", "intolerance", "sensitive", "reaction"],
  "exercise": ["workout", "training", "gym", "fitness", "running", "jogging"],
  "sleep": ["rest", "nap", "insomnia", "bedtime", "wake up", "sleeping"],
  "diet": ["eating", "nutrition", "fasting", "calories", "weight loss", "meal plan"],
  "surgery": ["operation", "procedure", "medical procedure"],
  "medication": ["medicine", "pills", "prescription", "drugs", "treatment"],
  "doctor": ["physician", "specialist", "appointment", "checkup", "clinic"],
  "phobia": ["fear", "afraid", "phobias", "terrified", "scared of"],
  "wellness": ["wellbeing", "health", "self-care", "mindfulness", "meditation"],
  // Work & career
  "job": ["work", "career", "employment", "position", "role", "occupation"],
  "boss": ["manager", "supervisor", "lead", "director", "superior"],
  "colleague": ["coworker", "teammate", "peer", "workmate"],
  "promotion": ["promoted", "advancement", "raise", "title change", "career progress"],
  "salary": ["pay", "wage", "income", "compensation", "earnings"],
  "interview": ["job interview", "hiring", "recruiter", "application"],
  "resign": ["quit", "leave", "resign", "hand in notice", "stepping down"],
  "meeting": ["conference", "standup", "sync", "call", "huddle"],
  "deadline": ["due date", "timeline", "crunch", "rush"],
  "overtime": ["extra hours", "working late", "staying late", "long hours"],
  "review": ["evaluation", "assessment", "appraisal", "feedback", "annual review"],
  "mentor": ["mentoring", "coaching", "guiding", "teaching", "training"],
  // Family & relationships
  "wife": ["spouse", "partner", "significant other", "better half"],
  "husband": ["spouse", "partner", "significant other"],
  "child": ["kid", "son", "daughter", "children", "kids"],
  "parent": ["mom", "dad", "mother", "father", "parents"],
  "friend": ["buddy", "mate", "pal", "bestie", "best friend", "close friend"],
  "pet": ["cat", "dog", "pets", "animal", "fur baby"],
  "dating": ["relationship", "seeing someone", "going out", "girlfriend", "boyfriend"],
  "marriage": ["married", "wedding", "engaged", "engagement"],
  "divorce": ["separated", "split up", "broke up", "ex"],
  "baby": ["infant", "newborn", "toddler", "little one"],
  "birthday": ["bday", "born", "turning", "anniversary"],
  // Housing & living
  "home": ["house", "apartment", "flat", "condo", "place", "residence"],
  "rent": ["renting", "tenant", "landlord", "lease"],
  "mortgage": ["home loan", "house payment", "monthly payment"],
  "move": ["moving", "relocate", "relocation", "new place"],
  "renovation": ["remodel", "remodeling", "fixing up", "home improvement"],
  "commute": ["commuting", "travel to work", "daily drive", "train ride"],
  // Finance & money
  "money": ["cash", "funds", "finance", "finances", "financial"],
  "invest": ["investment", "investing", "portfolio", "stocks", "crypto"],
  "save": ["savings", "saving up", "piggy bank", "emergency fund"],
  "debt": ["loan", "owe", "borrowed", "credit card debt"],
  "budget": ["budgeting", "spending", "expenses", "cost"],
  "insurance": ["coverage", "policy", "premium", "insured"],
  // Education
  "school": ["university", "college", "campus", "alma mater", "class"],
  "degree": ["diploma", "bachelor", "master", "MBA", "PhD", "graduate"],
  "study": ["studying", "learning", "coursework", "homework", "exam"],
  "teacher": ["professor", "instructor", "tutor", "lecturer"],
  "roommate": ["flatmate", "housemate", "dorm mate"],
  "graduation": ["graduated", "commencement", "finishing school"],
  // Transportation
  "car": ["vehicle", "automobile", "ride", "drive", "driving"],
  "flight": ["airplane", "plane", "flying", "airline", "airport"],
  "train": ["railway", "rail", "metro", "subway"],
  "trip": ["travel", "vacation", "holiday", "journey", "getaway"],
  "commute": ["daily travel", "getting to work", "ride to work"],
  // Food & dining
  "restaurant": ["dining", "eat out", "eatery", "place to eat", "dine"],
  "cook": ["cooking", "prepare", "make food", "kitchen", "homemade"],
  "breakfast": ["morning meal", "brunch"],
  "lunch": ["midday meal", "lunchtime"],
  "dinner": ["supper", "evening meal", "dinnertime"],
  "vegetarian": ["vegan", "plant-based", "meatless"],
  "recipe": ["dish", "meal prep", "ingredients", "how to make"],
  // Hobbies & leisure
  "movie": ["film", "cinema", "theater", "watching", "streaming"],
  "book": ["reading", "novel", "read", "literature", "author"],
  "game": ["gaming", "video game", "playing", "gamer"],
  "music": ["song", "listen", "playlist", "concert", "band"],
  "sport": ["sports", "athletic", "playing", "team"],
  "running": ["jogging", "jog", "marathon", "half marathon", "run"],
  "hiking": ["hike", "trail", "trekking", "outdoor"],
  "photography": ["photo", "camera", "pictures", "shooting"],
  "volunteer": ["volunteering", "charity", "community service", "giving back"],
  "hobby": ["hobbies", "pastime", "side project", "interest", "passion"],
  // Technology
  "laptop": ["computer", "notebook", "PC", "MacBook", "ThinkPad"],
  "phone": ["mobile", "smartphone", "iPhone", "Android", "cell phone"],
  "app": ["application", "software", "program", "tool"],
  "update": ["upgrade", "new version", "patch", "release"],
  "password": ["credential", "login", "authentication", "passphrase"],
  "wifi": ["internet", "network", "connection", "online"],
  // Time expressions
  "morning": ["AM", "sunrise", "early", "dawn", "wake up"],
  "evening": ["PM", "night", "sunset", "dusk", "nighttime"],
  "routine": ["habit", "daily", "regular", "schedule", "ritual"],
  "weekend": ["Saturday", "Sunday", "day off", "off day"],
  // General adjectives
  "big": ["large", "huge", "massive", "enormous"],
  "small": ["tiny", "little", "mini", "compact"],
  "fast": ["quick", "rapid", "speedy", "swift"],
  "slow": ["sluggish", "lagging", "delayed"],
  "good": ["great", "excellent", "awesome", "fantastic", "wonderful"],
  "bad": ["terrible", "awful", "horrible", "poor", "worst"],
  "old": ["ancient", "vintage", "previous", "former", "used to"],
  "new": ["latest", "recent", "fresh", "brand new", "modern"],
  "important": ["critical", "crucial", "essential", "vital", "key"],
  // ── 美食烹饪扩展（100组）──────────────────────────────────────────────
  "\u9984\u9968": ["\u4E91\u541E", "\u6284\u624B", "\u6241\u98DF", "\u9984\u9968\u6C64"],
  "\u70E7\u997C": ["\u829D\u9EBB\u70E7\u997C", "\u6CB9\u9165\u70E7\u997C", "\u8089\u5939\u998D"],
  "\u9EBB\u8FA3\u70EB": ["\u4E32\u4E32\u9999", "\u5192\u83DC", "\u5173\u4E1C\u716E", "\u9EBB\u8FA3\u62CC"],
  "\u5BFF\u559C\u70E7": ["sukiyaki", "\u65E5\u5F0F\u706B\u9505", "\u5BFF\u559C\u9505"],
  "\u5496\u55B1": ["curry", "\u5496\u55B1\u996D", "\u65E5\u5F0F\u5496\u55B1", "\u5370\u5EA6\u5496\u55B1"],
  "\u6CE1\u9762": ["\u65B9\u4FBF\u9762", "\u901F\u98DF\u9762", "\u676F\u9762", "\u6CE1\u9762\u5403"],
  "\u4E09\u660E\u6CBB": ["sandwich", "\u5939\u5FC3\u9762\u5305", "\u5E15\u5C3C\u5C3C"],
  "\u84B8": ["\u84B8\u83DC", "\u84B8\u9C7C", "\u84B8\u86CB", "\u6E05\u84B8", "\u4E0A\u9505\u84B8"],
  "\u716E": ["\u716E\u83DC", "\u6C34\u716E", "\u767D\u716E", "\u716E\u996D"],
  "\u70B8": ["\u6CB9\u70B8", "\u70B8\u9E21", "\u70B8\u85AF\u6761", "\u6DF1\u70B8", "\u714E\u70B8"],
  "\u70E4": ["\u70D8\u70E4", "\u70E7\u70E4", "\u70AD\u70E4", "\u7117\u70E4", "\u70E4\u7BB1"],
  "\u7096": ["\u7096\u8089", "\u6162\u7096", "\u5C0F\u706B\u7096", "\u7168", "\u7116"],
  "\u918B": ["\u9648\u918B", "\u7C73\u918B", "\u767D\u918B", "\u9999\u918B", "vinegar"],
  "\u76D0": ["\u98DF\u76D0", "\u7C97\u76D0", "\u6D77\u76D0", "\u52A0\u76D0", "salt"],
  "\u7CD6": ["\u767D\u7CD6", "\u51B0\u7CD6", "\u7EA2\u7CD6", "\u8517\u7CD6", "sugar"],
  "\u997C\u5E72": ["\u66F2\u5947", "cookie", "\u82CF\u6253\u997C", "\u5A01\u5316"],
  "\u767D\u9152": ["baijiu", "\u8305\u53F0", "\u4E8C\u9505\u5934", "\u767D\u7684"],
  "\u7EA2\u9152": ["wine", "\u8461\u8404\u9152", "\u5E72\u7EA2", "\u7EA2\u7684"],
  "\u8336": ["tea", "\u7EFF\u8336", "\u7EA2\u8336", "\u4E4C\u9F99\u8336", "\u666E\u6D31"],
  "\u7EA2\u85AF": ["\u5730\u74DC", "\u756A\u85AF", "\u70E4\u7EA2\u85AF", "sweet potato"],
  "\u8C46\u6D46": ["soy milk", "\u8C46\u5976", "\u65E9\u9910\u8C46\u6D46"],
  "\u6CB9\u6761": ["\u70B8\u6CB9\u6761", "\u8C46\u6D46\u6CB9\u6761", "\u65E9\u70B9"],
  "\u6708\u997C": ["mooncake", "\u4E2D\u79CB", "\u4E94\u4EC1\u6708\u997C", "\u5E7F\u5F0F\u6708\u997C"],
  "\u7CBD\u5B50": ["\u7AEF\u5348", "\u8089\u7CBD", "\u751C\u7CBD", "\u5305\u7CBD\u5B50"],
  "\u6C64\u5706": ["\u5143\u5BB5", "\u829D\u9EBB\u6C64\u5706", "\u5403\u6C64\u5706"],
  "\u6625\u5377": ["spring roll", "\u70B8\u6625\u5377", "\u6625\u5377\u76AE"],
  "\u5E74\u7CD5": ["\u7CCD\u7C91", "\u7092\u5E74\u7CD5", "\u5E74\u7CD5\u7247"],
  "\u87BA\u86F3\u7C89": ["\u87BA\u86F3", "\u67F3\u5DDE\u87BA\u86F3\u7C89", "\u81ED\u5473\u7C89"],
  "\u9178\u8FA3\u7C89": ["\u7EA2\u85AF\u7C89", "\u7C89\u4E1D", "\u91CD\u5E86\u9178\u8FA3\u7C89"],
  "\u81ED\u8C46\u8150": ["\u957F\u6C99\u81ED\u8C46\u8150", "\u70B8\u81ED\u8C46\u8150", "\u81ED\u5E72\u5B50"],
  "\u714E\u86CB": ["\u8377\u5305\u86CB", "\u714E\u9E21\u86CB", "\u592A\u9633\u86CB", "\u6E8F\u5FC3\u86CB"],
  "\u7092\u996D": ["\u86CB\u7092\u996D", "\u626C\u5DDE\u7092\u996D", "\u7092\u7C73\u996D"],
  "\u76D6\u6D47\u996D": ["\u76D6\u996D", "\u6D47\u5934\u996D", "\u5FEB\u9910"],
  "\u9EC4\u7116\u9E21": ["\u9EC4\u7116\u9E21\u7C73\u996D", "\u7116\u9505", "\u9E21\u7172"],
  "\u9EBB\u5A46\u8C46\u8150": ["\u9EBB\u8FA3\u8C46\u8150", "\u5DDD\u83DC\u8C46\u8150"],
  "\u5BAB\u4FDD\u9E21\u4E01": ["\u5BAB\u7206\u9E21\u4E01", "\u5DDD\u83DC\u9E21\u4E01"],
  "\u7CD6\u918B\u6392\u9AA8": ["\u7CD6\u918B\u91CC\u810A", "\u7CD6\u918B\u9C7C", "\u7CD6\u918B"],
  "\u56DE\u9505\u8089": ["\u5DDD\u83DC", "\u56DE\u9505", "\u849C\u82D7\u56DE\u9505\u8089"],
  "\u6C34\u716E\u9C7C": ["\u6C34\u716E\u8089\u7247", "\u9EBB\u8FA3\u9C7C", "\u6CB8\u817E\u9C7C"],
  "\u5C0F\u9F99\u867E": ["\u9F99\u867E", "\u849C\u84C9\u5C0F\u9F99\u867E", "\u5341\u4E09\u9999\u9F99\u867E", "\u867E"],
  "\u70E4\u4E32": ["\u7F8A\u8089\u4E32", "\u70E4\u97ED\u83DC", "\u70E4\u9762\u7B4B", "\u70E4\u751F\u869D"],
  "\u5364\u5473": ["\u5364\u8089", "\u5364\u9E21\u722A", "\u5364\u9E2D\u8116", "\u7EDD\u5473"],
  "\u814A\u8089": ["\u814A\u80A0", "\u54B8\u8089", "\u814C\u8089", "\u718F\u8089"],
  "\u8783\u87F9": ["\u5927\u95F8\u87F9", "\u5E1D\u738B\u87F9", "\u87F9", "\u5403\u87F9"],
  "\u9F99\u867E": ["\u6CE2\u58EB\u987F\u9F99\u867E", "\u5C0F\u9F99\u867E", "\u9F99\u867E\u5C3E"],
  "\u725B\u8169": ["\u7096\u725B\u8169", "\u725B\u8169\u9762", "\u7EA2\u70E7\u725B\u8169"],
  "\u9E21\u7FC5": ["\u53EF\u4E50\u9E21\u7FC5", "\u70E4\u9E21\u7FC5", "\u70B8\u9E21\u7FC5", "\u7FC5\u4E2D"],
  "\u6392\u9AA8": ["\u7EA2\u70E7\u6392\u9AA8", "\u7CD6\u918B\u6392\u9AA8", "\u84B8\u6392\u9AA8", "\u7096\u6392\u9AA8"],
  "\u8C46\u89D2": ["\u56DB\u5B63\u8C46", "\u957F\u8C46\u89D2", "\u7092\u8C46\u89D2"],
  "\u6930\u5B50": ["coconut", "\u6930\u6C41", "\u6930\u5976", "\u6930\u5B50\u9E21"],
  "\u725B\u5976": ["milk", "\u9C9C\u5976", "\u9178\u5976", "\u7EAF\u725B\u5976"],
  "\u9178\u5976": ["yogurt", "\u5E0C\u814A\u9178\u5976", "\u76CA\u751F\u83CC"],
  "\u9762\u5305": ["bread", "\u5410\u53F8", "\u5168\u9EA6\u9762\u5305", "\u6CD5\u68CD"],
  "\u9EC4\u6CB9": ["butter", "\u5976\u6CB9", "\u829D\u58EB", "\u829D\u58EB\u7247"],
  "\u756A\u8304\u9171": ["ketchup", "\u8FA3\u9171", "\u849C\u84C9\u9171", "\u6C99\u62C9\u9171"],
  "\u8471\u59DC\u849C": ["\u8471", "\u59DC", "\u849C", "\u7206\u9999", "\u709D\u9505"],
  "\u8150\u4E73": ["\u8C46\u8150\u4E73", "\u81ED\u8150\u4E73", "\u4E0B\u996D\u83DC"],
  "\u6CE1\u83DC": ["kimchi", "\u97E9\u56FD\u6CE1\u83DC", "\u9178\u83DC", "\u814C\u83DC"],
  "\u5E72\u9505": ["\u5E72\u9505\u82B1\u83DC", "\u5E72\u9505\u9E21", "\u5E72\u9505\u867E"],
  "\u62CC\u9762": ["\u70ED\u5E72\u9762", "\u51C9\u9762", "\u70B8\u9171\u9762", "\u62C5\u62C5\u9762"],
  "\u5200\u524A\u9762": ["\u5C71\u897F\u9762", "\u624B\u64C0\u9762", "\u62C9\u6761\u5B50"],
  "\u8089\u5939\u998D": ["\u51C9\u76AE", "\u9655\u897F\u5C0F\u5403", "\u814A\u6C41\u8089"],
  "\u51C9\u76AE": ["\u9EBB\u9171\u51C9\u76AE", "\u79E6\u9547\u51C9\u76AE", "\u64C0\u9762\u76AE"],
  "\u714E\u997A": ["\u9505\u8D34", "\u751F\u714E", "\u714E\u5305", "\u9505\u8D34\u997A"],
  "\u8C46\u82B1": ["\u8C46\u8150\u82B1", "\u751C\u8C46\u82B1", "\u54B8\u8C46\u82B1"],
  "\u70B8\u9171\u9762": ["\u8001\u5317\u4EAC\u70B8\u9171\u9762", "\u6742\u9171\u9762", "\u6253\u5364\u9762"],
  "\u9C7C\u9999\u8089\u4E1D": ["\u9C7C\u9999\u8304\u5B50", "\u9C7C\u9999\u5473", "\u5DDD\u83DC\u7ECF\u5178"],
  "\u4E1C\u5761\u8089": ["\u7EA2\u70E7\u8089", "\u4E94\u82B1\u8089", "\u6162\u7096\u8089"],
  "\u767D\u5207\u9E21": ["\u767D\u65A9\u9E21", "\u7CA4\u83DC", "\u9E21\u8089"],
  "\u53C9\u70E7": ["\u871C\u6C41\u53C9\u70E7", "\u6E2F\u5F0F", "\u53C9\u70E7\u996D"],
  "\u70E4\u9C7C": ["\u7EB8\u5305\u9C7C", "\u4E07\u5DDE\u70E4\u9C7C", "\u91CD\u5E86\u70E4\u9C7C"],
  "\u9178\u83DC\u9C7C": ["\u9178\u6C64\u9C7C", "\u9C7C\u7247", "\u9178\u83DC"],
  "\u86CB\u631E": ["\u8461\u5F0F\u86CB\u631E", "\u6E2F\u5F0F\u86CB\u631E", "\u70D8\u7119"],
  "\u63D0\u62C9\u7C73\u82CF": ["tiramisu", "\u610F\u5F0F\u751C\u70B9", "\u5496\u5561\u86CB\u7CD5"],
  "\u62B9\u8336": ["matcha", "\u62B9\u8336\u62FF\u94C1", "\u62B9\u8336\u86CB\u7CD5", "\u62B9\u8336\u5473"],
  "\u6930\u5976": ["coconut milk", "\u6930\u6D46", "\u6930\u5B50\u6C34"],
  "\u67E0\u6AAC\u6C34": ["\u67E0\u6AAC\u8336", "\u67E0\u6AAC\u6C41", "\u8702\u871C\u67E0\u6AAC"],
  "\u59DC\u8336": ["\u7EA2\u7CD6\u59DC\u8336", "\u6696\u80C3", "\u9A71\u5BD2"],
  "\u517B\u751F\u7CA5": ["\u7EA2\u8C46\u7CA5", "\u5C0F\u7C73\u7CA5", "\u76AE\u86CB\u7626\u8089\u7CA5", "\u6742\u7CAE\u7CA5"],
  "\u5364\u9E21\u722A": ["\u6CE1\u6912\u51E4\u722A", "\u9E21\u722A", "\u67E0\u6AAC\u9E21\u722A"],
  "\u9E21\u6392": ["\u70B8\u9E21\u6392", "\u5927\u9E21\u6392", "\u9E21\u6392\u996D"],
  "\u70ED\u72D7": ["hotdog", "\u9999\u80A0", "\u70E4\u80A0"],
  "\u85AF\u6761": ["fries", "\u70B8\u85AF\u6761", "\u7C97\u85AF\u6761", "\u7EC6\u85AF\u6761"],
  "\u5173\u4E1C\u716E": ["\u65E5\u5F0F\u5173\u4E1C\u716E", "\u4FBF\u5229\u5E97", "\u716E\u7269"],
  // ── 社交媒体/互联网/数码（100组）──────────────────────────────────────
  "\u5FEB\u624B": ["\u5FEB\u624B\u76F4\u64AD", "\u8001\u94C1", "\u53CC\u51FB", "\u77ED\u89C6\u9891\u5E73\u53F0"],
  "\u77E5\u4E4E": ["\u77E5\u4E4E\u95EE\u7B54", "\u5237\u77E5\u4E4E", "\u77E5\u4E4E\u56DE\u7B54", "\u5927V"],
  "\u8C46\u74E3": ["\u8C46\u74E3\u8BC4\u5206", "\u5F71\u8BC4", "\u4E66\u8BC4", "\u8C46\u74E3\u5C0F\u7EC4"],
  "\u8D34\u5427": ["\u767E\u5EA6\u8D34\u5427", "\u5427\u53CB", "\u8D34\u5427\u5E16\u5B50"],
  "4G": ["5G", "\u6D41\u91CF", "\u4FE1\u53F7", "\u79FB\u52A8\u7F51\u7EDC", "\u8702\u7A9D"],
  "\u6D41\u91CF": ["\u6570\u636E\u6D41\u91CF", "\u6D41\u91CF\u5957\u9910", "\u8D85\u6D41\u91CF", "\u6D41\u91CF\u4E0D\u591F"],
  "\u6536\u85CF": ["mark", "\u4E66\u7B7E", "\u6536\u85CF\u5939", "\u6536\u8D77\u6765"],
  "\u79C1\u4FE1": ["DM", "\u79C1\u804A", "\u53D1\u6D88\u606F", "\u7AD9\u5185\u4FE1"],
  "\u62C9\u9ED1": ["\u5C4F\u853D", "\u9ED1\u540D\u5355", "\u4E0D\u770B\u4ED6", "\u5220\u597D\u53CB"],
  "\u53D6\u5173": ["\u53D6\u6D88\u5173\u6CE8", "\u6389\u7C89", "\u8131\u7C89"],
  "\u5934\u50CF": ["avatar", "\u6362\u5934\u50CF", "\u7167\u7247", "\u5F62\u8C61"],
  "\u6635\u79F0": ["\u7F51\u540D", "\u540D\u5B57", "\u5907\u6CE8\u540D", "\u7528\u6237\u540D"],
  "\u7FA4\u804A": ["\u5FAE\u4FE1\u7FA4", "\u7FA4\u6D88\u606F", "\u7FA4\u516C\u544A", "\u62C9\u7FA4"],
  "\u8BDD\u9898": ["hashtag", "\u6807\u7B7E", "\u8BA8\u8BBA", "\u70ED\u95E8\u8BDD\u9898"],
  "\u76F4\u64AD\u95F4": ["\u76F4\u64AD\u623F\u95F4", "\u76F4\u64AD", "\u770B\u76F4\u64AD", "\u8FDB\u76F4\u64AD\u95F4"],
  "\u6253\u8D4F": ["\u9001\u793C\u7269", "\u5237\u793C\u7269", "\u6253\u94B1", "\u6295\u5E01"],
  "\u7F51\u66B4": ["\u7F51\u7EDC\u66B4\u529B", "\u952E\u76D8\u4FA0", "\u55B7\u5B50", "\u4EBA\u8089"],
  "\u6760\u7CBE": ["\u62AC\u6760", "\u627E\u832C", "\u6760", "\u6311\u523A"],
  "\u6C34\u519B": ["\u5237\u8BC4\u8BBA", "\u5E26\u8282\u594F", "\u63A7\u8BC4", "\u8425\u9500\u53F7"],
  "\u8425\u9500\u53F7": ["\u81EA\u5A92\u4F53", "\u8E6D\u70ED\u5EA6", "\u6807\u9898\u515A", "\u6D17\u7A3F"],
  "\u89C6\u9891\u53F7": ["\u5FAE\u4FE1\u89C6\u9891\u53F7", "\u53D1\u89C6\u9891", "\u77ED\u89C6\u9891"],
  "AI": ["\u4EBA\u5DE5\u667A\u80FD", "\u667A\u80FD", "ChatGPT", "AI\u52A9\u624B"],
  "ChatGPT": ["GPT", "AI\u804A\u5929", "\u667A\u80FD\u52A9\u624B", "OpenAI"],
  "VPN": ["\u7FFB\u5899", "\u68AF\u5B50", "\u79D1\u5B66\u4E0A\u7F51", "\u4EE3\u7406"],
  "\u7FFB\u5899": ["VPN", "\u68AF\u5B50", "\u79D1\u5B66\u4E0A\u7F51", "\u51FA\u5899"],
  "\u4E91\u76D8": ["\u7F51\u76D8", "\u767E\u5EA6\u7F51\u76D8", "\u963F\u91CC\u4E91\u76D8", "\u5B58\u50A8"],
  "\u84DD\u7259": ["bluetooth", "\u84DD\u7259\u8033\u673A", "\u914D\u5BF9", "\u65E0\u7EBF"],
  "\u5145\u7535\u5B9D": ["\u79FB\u52A8\u7535\u6E90", "\u5145\u7535", "\u5171\u4EAB\u5145\u7535\u5B9D"],
  "\u667A\u80FD\u624B\u8868": ["Apple Watch", "\u624B\u73AF", "\u53EF\u7A7F\u6234", "\u8FD0\u52A8\u624B\u8868"],
  "\u5E73\u677F": ["iPad", "\u5E73\u677F\u7535\u8111", "tablet", "\u5B89\u5353\u5E73\u677F"],
  "\u6295\u5F71\u4EEA": ["\u6295\u5F71", "\u5E55\u5E03", "\u5BB6\u5EAD\u5F71\u9662", "\u4FBF\u643A\u6295\u5F71"],
  "\u8DEF\u7531\u5668": ["router", "\u4FE1\u53F7", "\u7F51\u901F", "\u5343\u5146"],
  "\u6444\u50CF\u5934": ["\u76D1\u63A7", "\u6444\u50CF", "\u5B89\u9632", "\u95E8\u94C3\u6444\u50CF\u5934"],
  "\u65E0\u4EBA\u673A": ["drone", "\u822A\u62CD", "\u5927\u7586", "\u98DE\u884C\u5668"],
  "VR": ["\u865A\u62DF\u73B0\u5B9E", "VR\u773C\u955C", "\u5143\u5B87\u5B99", "AR"],
  "\u5143\u5B87\u5B99": ["metaverse", "\u865A\u62DF\u4E16\u754C", "\u6570\u5B57\u4EBA", "Web3"],
  "\u533A\u5757\u94FE": ["blockchain", "Web3", "NFT", "\u53BB\u4E2D\u5FC3\u5316"],
  "NFT": ["\u6570\u5B57\u85CF\u54C1", "\u52A0\u5BC6\u827A\u672F", "\u6570\u5B57\u8D44\u4EA7"],
  "\u4EBA\u8138\u8BC6\u522B": ["\u5237\u8138", "\u9762\u90E8\u8BC6\u522B", "\u751F\u7269\u8BC6\u522B"],
  "\u6307\u7EB9": ["\u6307\u7EB9\u89E3\u9501", "\u6307\u7EB9\u8BC6\u522B", "\u751F\u7269\u8BC6\u522B"],
  "\u622A\u56FE": ["screenshot", "\u5C4F\u5E55\u622A\u56FE", "\u5F55\u5C4F", "\u622A\u5C4F"],
  "\u4E0B\u8F7D": ["download", "\u4E0B\u8F7D\u5B89\u88C5", "\u79BB\u7EBF\u4E0B\u8F7D", "\u7F13\u5B58"],
  "\u4E0A\u4F20": ["upload", "\u4F20\u6587\u4EF6", "\u5206\u4EAB\u6587\u4EF6", "\u53D1\u9001\u6587\u4EF6"],
  "\u538B\u7F29": ["zip", "\u89E3\u538B", "\u538B\u7F29\u5305", "\u6253\u5305"],
  "\u683C\u5F0F": ["\u6587\u4EF6\u683C\u5F0F", "PDF", "JPG", "PNG", "\u683C\u5F0F\u8F6C\u6362"],
  "\u5B58\u50A8": ["storage", "\u786C\u76D8", "SSD", "\u5185\u5B58\u5361", "\u6269\u5BB9"],
  "\u5907\u4EFD": ["backup", "\u4E91\u5907\u4EFD", "\u6570\u636E\u5907\u4EFD", "\u6062\u590D"],
  "\u6740\u6BD2": ["\u6740\u6BD2\u8F6F\u4EF6", "\u75C5\u6BD2", "\u6728\u9A6C", "\u5B89\u5168\u8F6F\u4EF6"],
  "\u5F39\u7A97": ["\u5E7F\u544A\u5F39\u7A97", "\u63A8\u9001", "\u901A\u77E5", "\u70E6\u4EBA\u5E7F\u544A"],
  "\u5361\u987F": ["\u5361", "\u4E0D\u6D41\u7545", "\u5EF6\u8FDF", "\u6389\u5E27"],
  "\u6B7B\u673A": ["\u84DD\u5C4F", "\u9ED1\u5C4F", "\u91CD\u542F", "\u5361\u6B7B"],
  "\u95EA\u9000": ["crash", "\u5D29\u4E86", "\u9000\u51FA", "\u5E94\u7528\u95EA\u9000"],
  "\u9A8C\u8BC1\u7801": ["\u77ED\u4FE1\u9A8C\u8BC1", "\u56FE\u5F62\u9A8C\u8BC1", "\u6ED1\u5757\u9A8C\u8BC1", "\u4EBA\u673A\u9A8C\u8BC1"],
  "\u4E8C\u7EF4\u7801": ["QR code", "\u626B\u7801", "\u4E8C\u7EF4\u7801\u626B\u63CF"],
  "\u5C0F\u7A0B\u5E8F": ["\u5FAE\u4FE1\u5C0F\u7A0B\u5E8F", "\u652F\u4ED8\u5B9D\u5C0F\u7A0B\u5E8F", "\u8F7B\u5E94\u7528"],
  "APP": ["\u5E94\u7528", "\u624B\u673A\u5E94\u7528", "\u8F6F\u4EF6", "\u5BA2\u6237\u7AEF"],
  "\u652F\u4ED8\u5B9D": ["Alipay", "\u82B1\u5457", "\u4F59\u989D\u5B9D", "\u8682\u8681"],
  "\u5FAE\u4FE1\u652F\u4ED8": ["\u626B\u7801\u4ED8", "\u96F6\u94B1", "\u5FAE\u4FE1\u8F6C\u8D26"],
  "\u7F51\u901F": ["\u5E26\u5BBD", "\u4E0B\u8F7D\u901F\u5EA6", "\u4E0A\u4F20\u901F\u5EA6", "\u6D4B\u901F"],
  "\u670D\u52A1\u5668\u5D29\u4E86": ["\u5B95\u673A", "\u670D\u52A1\u5668\u6302\u4E86", "502", "503"],
  "\u6570\u636E\u6CC4\u9732": ["\u4FE1\u606F\u6CC4\u9732", "\u9690\u79C1\u6CC4\u9732", "\u88AB\u76D7\u53F7", "\u4FE1\u606F\u5B89\u5168"],
  "\u9493\u9C7C\u7F51\u7AD9": ["\u8BC8\u9A97", "\u9493\u9C7C\u94FE\u63A5", "\u5047\u7F51\u7AD9", "\u8BC8\u9A97\u77ED\u4FE1"],
  "\u7F51\u7EDC\u8BC8\u9A97": ["\u7535\u4FE1\u8BC8\u9A97", "\u6740\u732A\u76D8", "\u9A97\u5C40", "\u88AB\u9A97"],
  "emoji": ["\u8868\u60C5", "\u7B26\u53F7", "\u989C\u6587\u5B57", "\u7279\u6B8A\u7B26\u53F7"],
  "\u7B97\u6CD5\u63A8\u8350": ["\u4FE1\u606F\u8327\u623F", "\u63A8\u8350\u7B97\u6CD5", "\u731C\u4F60\u559C\u6B22", "\u5343\u4EBA\u5343\u9762"],
  "\u5927\u6570\u636E": ["\u6570\u636E\u5206\u6790", "\u6570\u636E\u6316\u6398", "\u6570\u636E\u9A71\u52A8", "big data"],
  "\u4E91\u8BA1\u7B97": ["cloud", "\u4E91\u670D\u52A1", "SaaS", "PaaS"],
  "\u7269\u8054\u7F51": ["IoT", "\u667A\u80FD\u5BB6\u5C45", "\u667A\u80FD\u8BBE\u5907", "\u4E07\u7269\u4E92\u8054"],
  "\u81EA\u52A8\u9A7E\u9A76": ["\u65E0\u4EBA\u9A7E\u9A76", "\u667A\u80FD\u9A7E\u9A76", "L4", "\u81EA\u52A8\u6CCA\u8F66"],
  "\u673A\u5668\u4EBA": ["robot", "\u667A\u80FD\u673A\u5668\u4EBA", "bot", "\u673A\u68B0\u81C2"],
  "\u82AF\u7247": ["chip", "\u5904\u7406\u5668", "CPU", "GPU", "\u534A\u5BFC\u4F53"],
  "\u663E\u5361": ["GPU", "\u663E\u5B58", "N\u5361", "A\u5361", "\u72EC\u663E"],
  "SSD": ["\u56FA\u6001\u786C\u76D8", "\u786C\u76D8", "\u673A\u68B0\u786C\u76D8", "\u5B58\u50A8\u76D8"],
  "\u5185\u5B58": ["RAM", "\u8FD0\u884C\u5185\u5B58", "8G", "16G", "32G"],
  "\u5C4F\u5E55": ["display", "\u663E\u793A\u5C4F", "OLED", "LCD", "\u5206\u8FA8\u7387"],
  "\u6D4F\u89C8\u5668": ["browser", "Chrome", "Safari", "Firefox", "\u4E0A\u7F51"],
  "\u641C\u7D22\u5F15\u64CE": ["\u767E\u5EA6", "Google", "\u641C\u7D22", "\u641C\u4E00\u4E0B"],
  "\u8BBA\u575B": ["forum", "\u793E\u533A", "\u677F\u5757", "\u704C\u6C34"],
  "\u535A\u5BA2": ["blog", "\u4E2A\u4EBA\u535A\u5BA2", "\u5199\u535A\u5BA2", "\u6280\u672F\u535A\u5BA2"],
  "\u64AD\u5BA2\u8282\u76EE": ["podcast", "\u97F3\u9891\u8282\u76EE", "\u7535\u53F0"],
  "\u8BA2\u9605": ["subscribe", "\u5173\u6CE8", "\u8BA2\u9605\u53F7", "RSS"],
  "\u63A8\u9001\u901A\u77E5": ["push", "\u6D88\u606F\u63A8\u9001", "\u901A\u77E5", "\u63D0\u9192"],
  "\u4EBA\u5DE5\u5BA2\u670D": ["\u5728\u7EBF\u5BA2\u670D", "\u667A\u80FD\u5BA2\u670D", "\u673A\u5668\u4EBA\u5BA2\u670D", "\u8F6C\u4EBA\u5DE5"],
  "\u8BED\u97F3\u52A9\u624B": ["Siri", "\u5C0F\u7231\u540C\u5B66", "\u5929\u732B\u7CBE\u7075", "\u8BED\u97F3\u63A7\u5236"],
  "\u667A\u80FD\u97F3\u7BB1": ["HomePod", "\u5C0F\u7231", "\u5929\u732B\u7CBE\u7075", "\u5C0F\u5EA6"],
  "\u626B\u5730\u673A\u5668\u4EBA": ["\u626B\u5730\u673A", "\u77F3\u5934\u626B\u5730\u673A", "\u81EA\u52A8\u6E05\u626B"],
  "\u667A\u80FD\u95E8\u9501": ["\u6307\u7EB9\u9501", "\u5BC6\u7801\u9501", "\u7535\u5B50\u9501", "\u667A\u80FD\u9501"],
  "\u7A7A\u6C14\u51C0\u5316\u5668": ["\u51C0\u5316\u5668", "\u6EE4\u82AF", "PM2.5", "\u65B0\u98CE"],
  "\u7535\u52A8\u7259\u5237": ["\u58F0\u6CE2\u7259\u5237", "\u7259\u5237\u5934", "Oral-B"],
  "\u6570\u636E\u7EBF": ["\u5145\u7535\u7EBF", "Type-C", "Lightning", "USB"],
  "\u8F6C\u63A5\u5934": ["\u9002\u914D\u5668", "\u6269\u5C55\u575E", "hub", "\u62D3\u5C55"],
  "\u8D34\u819C": ["\u624B\u673A\u819C", "\u94A2\u5316\u819C", "\u5C4F\u5E55\u4FDD\u62A4"],
  "\u624B\u673A\u58F3": ["\u4FDD\u62A4\u58F3", "\u624B\u673A\u5957", "\u900F\u660E\u58F3"],
  "\u4E8C\u624B\u624B\u673A": ["\u4E8C\u624B\u673A", "\u7FFB\u65B0\u673A", "\u5B98\u7FFB"],
  "\u4EE5\u65E7\u6362\u65B0": ["\u6298\u62B5", "\u65E7\u673A\u56DE\u6536", "\u6362\u65B0"],
  "\u79D1\u6280\u65B0\u95FB": ["\u6570\u7801\u5708", "\u53D1\u5E03\u4F1A", "\u65B0\u54C1", "\u79D1\u6280\u5A92\u4F53"],
  "\u5F00\u53D1\u8005": ["developer", "\u7A0B\u5E8F\u5458", "\u7801\u519C", "\u5DE5\u7A0B\u5E08"],
  "\u7528\u6237\u4F53\u9A8C": ["UX", "\u4EA4\u4E92\u8BBE\u8BA1", "\u7528\u6237\u7814\u7A76", "\u4F53\u9A8C\u4F18\u5316"],
  "\u6697\u9ED1\u6A21\u5F0F": ["dark mode", "\u591C\u95F4\u6A21\u5F0F", "\u6DF1\u8272\u6A21\u5F0F"],
  // ── 影视音乐娱乐（100组）──────────────────────────────────────────────
  "\u7EFC\u827A\u8282\u76EE": ["\u9009\u79C0", "\u8131\u53E3\u79C0", "\u559C\u5267", "\u771F\u4EBA\u79C0\u8282\u76EE"],
  "\u6D41\u884C\u97F3\u4E50": ["pop", "\u6D41\u884C\u6B4C", "\u6D41\u884C\u66F2", "\u70ED\u95E8\u6B4C"],
  "R&B": ["\u8282\u594F\u5E03\u9C81\u65AF", "\u7075\u9B42\u4E50", "soul"],
  "\u91D1\u5C5E": ["metal", "\u91CD\u91D1\u5C5E", "\u6B7B\u4EA1\u91D1\u5C5E", "\u786C\u6838"],
  "\u670B\u514B": ["punk", "\u670B\u514B\u6447\u6EDA", "\u53DB\u9006", "\u72EC\u7ACB\u670B\u514B"],
  "\u563B\u54C8": ["hip-hop", "\u8BF4\u5531", "rapper", "\u563B\u54C8\u6587\u5316"],
  "\u8D1D\u65AF": ["bass", "\u8D1D\u65AF\u624B", "\u4F4E\u97F3\u5409\u4ED6"],
  "\u8428\u514B\u65AF": ["saxophone", "\u5439\u8428\u514B\u65AF", "\u7BA1\u4E50"],
  "\u97F3\u4E50\u8282": ["festival", "\u8349\u8393\u97F3\u4E50\u8282", "\u8FF7\u7B1B", "\u6237\u5916\u97F3\u4E50"],
  "\u7F51\u6613\u4E91": ["\u7F51\u6613\u4E91\u97F3\u4E50", "\u4E91\u6751", "QQ\u97F3\u4E50", "\u542C\u6B4CApp"],
  "QQ\u97F3\u4E50": ["\u542C\u6B4C", "\u97F3\u4E50App", "\u9177\u72D7", "\u9177\u6211"],
  "\u7FFB\u5531": ["cover", "\u7FFB\u5531\u6B4C\u66F2", "\u6539\u7F16", "\u91CD\u65B0\u6F14\u7ECE"],
  "\u539F\u521B": ["\u539F\u521B\u97F3\u4E50", "\u539F\u521B\u6B4C\u66F2", "\u81EA\u5DF1\u5199\u7684"],
  "\u6B4C\u8BCD": ["lyrics", "\u6B4C\u8BCD\u672C", "\u5199\u6B4C\u8BCD"],
  "\u559C\u5267\u7247": ["comedy", "\u641E\u7B11\u7535\u5F71", "\u559C\u5267\u7535\u5F71", "\u7B11\u6B7B"],
  "\u60AC\u7591\u7247": ["thriller", "\u60AC\u7591\u7535\u5F71", "\u63A8\u7406", "\u60AC\u5FF5"],
  "\u6218\u4E89\u7247": ["war film", "\u519B\u4E8B", "\u6218\u4E89\u7535\u5F71", "\u5386\u53F2\u6218\u4E89"],
  "\u6B66\u4FA0": ["\u6B66\u4FA0\u7247", "\u6C5F\u6E56", "\u529F\u592B", "\u4ED9\u4FA0"],
  "\u52A8\u753B\u7535\u5F71": ["animated", "\u76AE\u514B\u65AF", "\u8FEA\u58EB\u5C3C", "\u5BAB\u5D0E\u9A8F"],
  "\u6F2B\u753B": ["manga", "\u6F2B\u753B\u4E66", "\u8FDE\u8F7D", "\u770B\u6F2B\u753B"],
  "\u756A\u5267": ["anime", "\u65B0\u756A", "\u8FFD\u756A", "\u65E5\u756A"],
  "\u4E8C\u6B21\u5143": ["ACG", "\u52A8\u6F2B\u6587\u5316", "\u5B85", "\u4E8C\u6B21\u5143\u6587\u5316"],
  "cosplay": ["cos", "\u89D2\u8272\u626E\u6F14", "coser", "\u626E\u88C5"],
  "\u6F2B\u5C55": ["\u52A8\u6F2B\u5C55", "CJ", "CP", "\u6F2B\u5C55\u6D3B\u52A8"],
  "\u8F7B\u5C0F\u8BF4": ["light novel", "\u8F7B\u5C0F\u8BF4\u6539\u7F16", "\u65E5\u8F7B"],
  "\u7F51\u6587": ["\u7F51\u7EDC\u5C0F\u8BF4", "\u7F51\u6587\u5C0F\u8BF4", "\u8D77\u70B9", "\u9605\u6587"],
  "\u7384\u5E7B": ["\u4ED9\u4FA0", "\u4FEE\u771F", "\u5947\u5E7B", "\u5F02\u4E16\u754C"],
  "\u7A7F\u8D8A": ["\u7A7F\u8D8A\u5267", "\u7A7F\u8D8A\u5C0F\u8BF4", "\u91CD\u751F", "\u65F6\u7A7A\u7A7F\u8D8A"],
  "\u8131\u53E3\u79C0": ["stand-up", "\u5355\u53E3\u559C\u5267", "\u8131\u53E3\u79C0\u6F14\u5458", "\u6BB5\u5B50"],
  "\u76F8\u58F0": ["\u8BF4\u76F8\u58F0", "\u6367\u54CF", "\u9017\u54CF", "\u90ED\u5FB7\u7EB2"],
  "\u5C0F\u54C1": ["\u6625\u665A\u5C0F\u54C1", "\u559C\u5267\u5C0F\u54C1", "\u8D75\u672C\u5C71"],
  "\u8BDD\u5267": ["\u821E\u53F0\u5267", "theater", "\u6F14\u8BDD\u5267", "\u770B\u8BDD\u5267"],
  "\u6B4C\u5267": ["opera", "\u6B4C\u5531", "\u58F0\u4E50", "\u6B4C\u5267\u9662"],
  "\u82AD\u857E": ["ballet", "\u82AD\u857E\u821E", "\u821E\u8005", "\u8DF3\u82AD\u857E"],
  "\u97F3\u4E50\u5267": ["musical", "\u767E\u8001\u6C47", "\u821E\u53F0", "\u5267\u573A"],
  "\u5F71\u8BC4": ["movie review", "\u8C46\u74E3\u5F71\u8BC4", "\u7535\u5F71\u8BC4\u8BBA", "\u5F71\u8BC4\u4EBA"],
  "\u660E\u661F": ["star", "\u5076\u50CF", "\u827A\u4EBA", "\u660E\u661F\u516B\u5366"],
  "\u7C89\u4E1D\u7ECF\u6D4E": ["\u996D\u5708", "\u5E94\u63F4", "\u6253\u6295", "\u8FFD\u661F"],
  "\u9009\u79C0": ["\u9009\u79C0\u8282\u76EE", "\u51FA\u9053", "\u5076\u50CF\u7EC3\u4E60\u751F", "\u521B\u9020\u8425"],
  "\u9881\u5956": ["\u9881\u5956\u5178\u793C", "\u5965\u65AF\u5361", "\u91D1\u9A6C", "\u91D1\u9E21"],
  "\u5965\u65AF\u5361": ["Oscar", "\u5B66\u9662\u5956", "\u5965\u65AF\u5361\u91D1\u50CF\u5956"],
  "\u91D1\u66F2": ["\u7ECF\u5178\u6B4C\u66F2", "\u70ED\u95E8\u6B4C\u66F2", "\u6392\u884C\u699C", "\u699C\u5355"],
  "\u6392\u884C\u699C": ["\u699C\u5355", "\u70ED\u6B4C\u699C", "\u65B0\u6B4C\u699C", "chart"],
  "\u5F69\u86CB": ["easter egg", "\u9690\u85CF\u5267\u60C5", "\u7247\u5C3E\u5F69\u86CB", "\u60CA\u559C"],
  "\u5267\u900F": ["spoiler", "\u900F\u5267", "\u5267\u900F\u8B66\u544A", "\u6CC4\u9732\u5267\u60C5"],
  "\u5F03\u5267": ["\u4E0D\u770B\u4E86", "\u70C2\u5C3E", "\u770B\u4E0D\u4E0B\u53BB", "\u592A\u70C2\u4E86"],
  "\u50AC\u66F4": ["\u66F4\u65B0", "\u8FDE\u8F7D", "\u7B49\u66F4\u65B0", "\u4EC0\u4E48\u65F6\u5019\u66F4"],
  "\u5B8C\u7ED3": ["\u5927\u7ED3\u5C40", "\u5B8C\u7ED3\u6492\u82B1", "\u5168\u5267\u7EC8", "\u7ED3\u5C40"],
  "\u7ECF\u5178": ["classic", "\u795E\u4F5C", "\u5DC5\u5CF0", "\u5FC5\u770B"],
  "\u70C2\u7247": ["\u70C2\u5267", "\u5783\u573E\u7247", "\u6D6A\u8D39\u65F6\u95F4", "\u96F7\u5267"],
  "\u9884\u544A": ["trailer", "\u9884\u544A\u7247", "\u5148\u5BFC\u7247", "\u82B1\u7D6E"],
  "\u9996\u6620": ["premiere", "\u9996\u6620\u5F0F", "\u4E0A\u6620", "\u516C\u6620"],
  "\u9662\u7EBF": ["\u7535\u5F71\u9662", "\u5F71\u9662", "\u5927\u94F6\u5E55", "\u6392\u7247"],
  "\u6D41\u5A92\u4F53": ["streaming", "\u5728\u7EBF\u89C2\u770B", "\u70B9\u64AD", "\u89C6\u9891\u5E73\u53F0"],
  "\u7231\u5947\u827A": ["\u4F18\u9177", "\u817E\u8BAF\u89C6\u9891", "\u8292\u679CTV", "\u89C6\u9891\u7F51\u7AD9"],
  "Netflix": ["\u7F51\u98DE", "\u5948\u98DE", "\u6D41\u5A92\u4F53\u5E73\u53F0", "Disney+"],
  "Spotify": ["Apple Music", "\u97F3\u4E50\u5E73\u53F0", "\u542C\u6B4C\u8F6F\u4EF6"],
  "\u4E50\u8BC4": ["music review", "\u4E50\u8BC4\u4EBA", "\u97F3\u4E50\u8BC4\u8BBA"],
  "MV": ["music video", "\u97F3\u4E50\u89C6\u9891", "\u62CDMV", "PV"],
  "\u4E13\u8F91": ["album", "\u65B0\u4E13\u8F91", "\u53D1\u4E13\u8F91", "\u51FA\u789F"],
  "\u5355\u66F2": ["single", "\u65B0\u5355\u66F2", "\u4E3B\u6253\u6B4C"],
  "\u5DE1\u6F14": ["tour", "\u4E16\u754C\u5DE1\u6F14", "\u5168\u56FD\u5DE1\u6F14", "\u5DE1\u56DE\u6F14\u51FA"],
  "\u5B89\u53EF": ["encore", "\u52A0\u573A", "\u8FD4\u573A", "\u518D\u6765\u4E00\u9996"],
  "\u5E94\u63F4": ["\u5E94\u63F4\u68D2", "\u706F\u6D77", "\u7C89\u4E1D\u5E94\u63F4", "\u6253call"],
  "\u6DF7\u97F3": ["remix", "\u91CD\u6DF7", "DJ\u6DF7\u97F3", "\u91CD\u5236"],
  "\u91C7\u6837": ["sample", "\u53D6\u6837", "\u97F3\u4E50\u91C7\u6837"],
  "\u7F16\u66F2": ["arrangement", "\u4F5C\u66F2", "\u914D\u4E50", "\u5236\u4F5C\u4EBA"],
  "\u8C03\u97F3": ["mixing", "\u6DF7\u97F3", "\u97F3\u6548", "\u97F3\u9891\u5904\u7406"],
  "\u540E\u671F": ["post-production", "\u526A\u8F91", "\u7279\u6548", "\u8C03\u8272"],
  "\u526A\u8F91": ["editing", "\u89C6\u9891\u526A\u8F91", "\u526A\u7247", "\u540E\u671F\u526A\u8F91"],
  "\u7279\u6548": ["VFX", "\u89C6\u89C9\u7279\u6548", "CGI", "\u7EFF\u5E55"],
  "\u914D\u97F3": ["dubbing", "\u914D\u97F3\u6F14\u5458", "\u58F0\u4F18", "\u4E2D\u914D"],
  "\u58F0\u4F18": ["CV", "\u65E5\u672C\u58F0\u4F18", "\u914D\u97F3", "\u89D2\u8272\u58F0\u97F3"],
  "\u5B57\u5E55": ["subtitle", "\u4E2D\u6587\u5B57\u5E55", "\u5916\u6302\u5B57\u5E55", "\u7FFB\u8BD1"],
  "\u5F39\u5E55\u6587\u5316": ["\u5F39\u5E55\u6897", "\u6EE1\u5C4F\u5F39\u5E55", "\u5F39\u5E55\u4E92\u52A8"],
  "\u72EC\u7ACB\u7535\u5F71": ["indie", "\u6587\u827A\u7247", "\u5C0F\u4F17\u7535\u5F71", "\u72EC\u7ACB\u5236\u4F5C"],
  "\u9ED1\u8272\u7535\u5F71": ["film noir", "\u72AF\u7F6A\u7247", "\u9ED1\u6697\u98CE\u683C"],
  "\u516C\u8DEF\u7247": ["road movie", "\u81EA\u9A7E\u65C5\u884C", "\u5728\u8DEF\u4E0A"],
  "\u9ED8\u7247": ["silent film", "\u65E0\u58F0\u7535\u5F71", "\u5353\u522B\u6797"],
  "\u77ED\u7247": ["short film", "\u5FAE\u7535\u5F71", "\u77ED\u7247\u7535\u5F71"],
  "\u5965\u7279\u66FC": ["ultraman", "\u7279\u6444", "\u602A\u517D", "\u53D8\u8EAB"],
  "\u9AD8\u8FBE": ["gundam", "\u673A\u7532", "\u673A\u5668\u4EBA\u52A8\u753B"],
  "\u6D77\u8D3C\u738B": ["one piece", "\u8DEF\u98DE", "\u822A\u6D77\u738B"],
  "\u706B\u5F71\u5FCD\u8005": ["naruto", "\u5FCD\u8005", "\u9E23\u4EBA"],
  "\u8FDB\u51FB\u7684\u5DE8\u4EBA": ["\u5DE8\u4EBA", "\u7ACB\u4F53\u673A\u52A8", "\u8C03\u67E5\u5175\u56E2"],
  "\u9B3C\u706D\u4E4B\u5203": ["\u9B3C\u706D", "\u70AD\u6CBB\u90CE", "\u547C\u5438\u6CD5"],
  "\u95F4\u8C0D\u8FC7\u5BB6\u5BB6": ["SPY\xD7FAMILY", "\u963F\u5C3C\u4E9A", "\u95F4\u8C0D\u5BB6\u5BB6\u9152"],
  "\u65B0\u6D77\u8BDA": ["\u4F60\u7684\u540D\u5B57", "\u5929\u6C14\u4E4B\u5B50", "\u94C3\u82BD\u4E4B\u65C5"],
  "\u5409\u535C\u529B": ["\u5BAB\u5D0E\u9A8F", "\u9F99\u732B", "\u5343\u4E0E\u5343\u5BFB", "\u54C8\u5C14"],
  "\u97E9\u5267": ["K-drama", "\u97E9\u56FD\u7535\u89C6\u5267", "\u8FFD\u97E9\u5267"],
  "\u7F8E\u5267": ["\u7F8E\u56FD\u7535\u89C6\u5267", "\u8FFD\u7F8E\u5267", "HBO", "Netflix\u5267"],
  "\u65E5\u5267": ["\u65E5\u672C\u7535\u89C6\u5267", "\u8FFD\u65E5\u5267", "\u65E5\u5267\u8DD1"],
  "\u56FD\u4EA7\u5267": ["\u56FD\u5267", "\u5185\u5730\u5267", "\u53E4\u88C5\u5267", "\u90FD\u5E02\u5267"],
  "\u5076\u50CF\u5267": ["\u53F0\u5267", "\u751C\u5BA0\u5267", "\u604B\u7231\u5267"],
  "\u60AC\u7591\u5267": ["\u70E7\u8111\u5267", "\u63A8\u7406\u5267", "\u72AF\u7F6A\u5267"],
  "\u53E4\u88C5\u5267": ["\u4ED9\u4FA0\u5267", "\u5BAB\u6597", "\u6743\u8C0B"],
  "\u771F\u4EBA\u79C0": ["reality show", "\u7D20\u4EBA", "\u660E\u661F\u771F\u4EBA\u79C0"],
  "\u65C5\u884C\u7EFC\u827A": ["\u65C5\u6E38\u8282\u76EE", "\u82B1\u5C11", "\u5411\u5F80\u7684\u751F\u6D3B"],
  "\u97F3\u4E50\u7EFC\u827A": ["\u6B4C\u624B", "\u597D\u58F0\u97F3", "\u6211\u662F\u6B4C\u624B", "\u97F3\u4E50\u8282\u76EE"],
  "\u559C\u5267\u7EFC\u827A": ["\u4E00\u5E74\u4E00\u5EA6\u559C\u5267\u5927\u8D5B", "\u559C\u5267\u8282\u76EE", "\u8131\u53E3\u79C0\u5927\u4F1A"],
  // ── 购物消费（100组）──────────────────────────────────────────────────
  "\u6DD8\u5B9D": ["taobao", "\u6DD8\u5B9D\u7F51", "\u5929\u732B", "\u901B\u6DD8\u5B9D"],
  "\u4EAC\u4E1C": ["JD", "\u4EAC\u4E1C\u5546\u57CE", "\u4EAC\u4E1C\u81EA\u8425", "\u4EAC\u4E1C\u5FEB\u9012"],
  "\u62FC\u591A\u591A": ["\u62FC\u56E2", "\u780D\u4EF7", "\u62FC\u5355", "\u767E\u4EBF\u8865\u8D34"],
  "\u5929\u732B": ["Tmall", "\u5929\u732B\u65D7\u8230\u5E97", "\u5929\u732B\u8D85\u5E02"],
  "\u53CC\u5341\u4E8C": ["\u53CC12", "\u5E74\u7EC8\u5927\u4FC3", "\u8D2D\u7269\u8282"],
  "618": ["\u4EAC\u4E1C618", "\u5E74\u4E2D\u5927\u4FC3", "618\u5927\u4FC3"],
  "\u5C3E\u6B3E": ["\u4ED8\u5C3E\u6B3E", "\u5C3E\u6B3E\u4EBA", "\u8865\u5DEE\u4EF7"],
  "\u8D2D\u7269\u8F66": ["\u52A0\u8D2D", "\u8D2D\u7269\u8F66\u6E05\u7A7A", "\u51D1\u6EE1\u51CF"],
  "\u6E05\u7A7A\u8D2D\u7269\u8F66": ["\u4E0B\u5355", "\u5168\u4E70\u4E86", "\u4ED8\u6B3E"],
  "\u8FD0\u8D39": ["\u5FEB\u9012\u8D39", "\u8FD0\u8D39\u9669", "\u5230\u4ED8"],
  "\u6D77\u6DD8": ["\u6D77\u5916\u76F4\u90AE", "\u8F6C\u8FD0", "\u8DE8\u5883\u7535\u5546", "\u4E9A\u9A6C\u900A"],
  "\u514D\u7A0E": ["\u514D\u7A0E\u5E97", "\u673A\u573A\u514D\u7A0E", "\u65E5\u4E0A"],
  "\u9000\u6B3E": ["\u9000\u94B1", "\u9000\u56DE", "\u4EC5\u9000\u6B3E", "\u9000\u8D27\u9000\u6B3E"],
  "\u4FDD\u4FEE": ["warranty", "\u8D28\u4FDD", "\u4FDD\u4FEE\u671F", "\u5EF6\u4FDD"],
  "\u8BC4\u4EF7": ["\u8BC4\u8BBA", "\u4E70\u5BB6\u79C0", "\u6652\u5355", "\u8BC4\u5206"],
  "\u4E70\u5BB6\u79C0": ["\u6652\u56FE", "\u5B9E\u7269\u56FE", "\u771F\u5B9E\u8BC4\u4EF7"],
  "\u65D7\u8230\u5E97": ["\u5B98\u65B9\u5E97", "\u4E13\u5356\u5E97", "\u54C1\u724C\u5E97"],
  "\u53D1\u8D27": ["\u5DF2\u53D1\u8D27", "\u5F85\u53D1\u8D27", "\u50AC\u53D1\u8D27", "\u53D1\u5FEB\u9012"],
  "\u6F6E\u724C": ["\u6F6E\u6D41\u54C1\u724C", "\u8857\u5934\u54C1\u724C", "\u8054\u540D", "\u9650\u91CF"],
  "\u8054\u540D": ["\u8054\u540D\u6B3E", "\u5408\u4F5C\u6B3E", "\u8054\u540D\u5546\u54C1", "\u8DE8\u754C"],
  "\u9650\u91CF": ["\u9650\u91CF\u7248", "\u7A00\u6709", "\u9650\u5B9A", "\u7EDD\u7248"],
  "\u6298\u6263\u5E97": ["\u5965\u7279\u83B1\u65AF", "outlets", "\u5DE5\u5382\u5E97", "\u7279\u5356"],
  "\u8FD4\u5229": ["\u8FD4\u73B0", "\u4F63\u91D1", "\u63A8\u5E7F", "\u8FD4\u5229\u7F51"],
  "\u5206\u671F": ["\u5206\u671F\u4ED8\u6B3E", "\u82B1\u5457\u5206\u671F", "\u767D\u6761", "\u514D\u606F"],
  "\u82B1\u5457": ["\u8682\u8681\u82B1\u5457", "\u82B1\u5457\u5206\u671F", "\u5148\u4E70\u540E\u4ED8"],
  "\u767D\u6761": ["\u4EAC\u4E1C\u767D\u6761", "\u767D\u6761\u5206\u671F", "\u4FE1\u7528\u8D2D"],
  "\u4FE1\u7528\u8D2D": ["\u5148\u4EAB\u540E\u4ED8", "\u514D\u606F", "\u8D4A\u8D26"],
  "\u6BD4\u4EF7": ["\u4EF7\u683C\u5BF9\u6BD4", "\u5386\u53F2\u4EF7\u683C", "\u5168\u7F51\u6BD4\u4EF7"],
  "\u56E4\u8D27": ["\u56E4", "\u5907\u8D27", "\u5C6F\u8D27", "\u591A\u4E70\u51E0\u4E2A"],
  "\u51D1\u5355": ["\u51D1\u6EE1\u51CF", "\u51D1\u5305\u90AE", "\u52A0\u8D2D\u51D1"],
  "\u5241\u624B": ["\u4E70\u4E70\u4E70", "\u5FCD\u4E0D\u4F4F", "\u94B1\u5305\u54ED\u4E86", "\u5403\u571F"],
  "\u5403\u571F": ["\u6708\u5E95\u5403\u571F", "\u7A77\u4E86", "\u82B1\u5149\u4E86", "\u6CA1\u94B1\u4E86"],
  "\u7701\u94B1\u653B\u7565": ["\u8585\u7F8A\u6BDB", "\u7701\u94B1\u79D8\u7C4D", "\u4F4E\u4EF7\u653B\u7565"],
  "\u8585\u7F8A\u6BDB": ["\u7F8A\u6BDB\u515A", "\u4F18\u60E0", "\u767D\u5AD6", "\u4FBF\u5B9C"],
  "\u54C1\u8D28": ["\u8D28\u91CF", "\u505A\u5DE5", "\u7528\u6599", "\u54C1\u63A7"],
  "\u5C3A\u7801": ["size", "\u504F\u5927", "\u504F\u5C0F", "\u5C3A\u5BF8"],
  "\u989C\u8272": ["color", "\u8272\u53F7", "\u914D\u8272", "\u8272\u7CFB"],
  "\u6B3E\u5F0F": ["style", "\u6837\u5F0F", "\u7248\u578B", "\u578B\u53F7"],
  "\u5E93\u5B58": ["stock", "\u6709\u8D27", "\u7F3A\u8D27", "\u8865\u8D27"],
  "\u9884\u7EA6\u8D2D\u4E70": ["\u62A2\u8D2D", "\u9884\u7EA6", "\u5B9A\u95F9\u949F", "\u5F00\u62A2"],
  "\u53D1\u7968": ["\u5F00\u53D1\u7968", "\u7535\u5B50\u53D1\u7968", "\u62A5\u9500"],
  "\u652F\u4ED8": ["\u4ED8\u6B3E", "\u4ED8\u94B1", "\u7ED3\u8D26", "\u652F\u4ED8\u65B9\u5F0F"],
  "\u8D27\u5230\u4ED8\u6B3E": ["\u5230\u4ED8", "COD", "\u5148\u9A8C\u540E\u4ED8"],
  "\u62C6\u5305\u88F9": ["\u5F00\u7BB1", "\u62C6\u5FEB\u9012", "\u5F00\u5305\u88F9", "unboxing"],
  "\u5F00\u7BB1": ["unboxing", "\u5F00\u7BB1\u89C6\u9891", "\u62C6\u7BB1", "\u6652\u5F00\u7BB1"],
  "\u79CD\u8349\u6E05\u5355": ["\u8D2D\u7269\u6E05\u5355", "\u5FC5\u4E70\u6E05\u5355", "\u63A8\u8350\u6E05\u5355"],
  "\u9ED1\u4E94": ["Black Friday", "\u9ED1\u8272\u661F\u671F\u4E94", "\u6D77\u5916\u4FC3\u9500"],
  "Prime Day": ["\u4E9A\u9A6C\u900A\u4F1A\u5458\u65E5", "\u6D77\u5916\u5927\u4FC3"],
  "\u76F4\u64AD\u8D2D\u7269": ["\u76F4\u64AD\u4E70", "\u76F4\u64AD\u95F4\u4E70", "\u4E3B\u64AD\u63A8\u8350"],
  "\u6837\u54C1": ["\u8BD5\u7528\u88C5", "\u5C0F\u6837", "\u8D60\u54C1", "\u4F53\u9A8C\u88C5"],
  "\u8D60\u54C1": ["\u4E70\u8D60", "\u9644\u8D60", "\u9001\u8D60\u54C1", "\u6EE1\u8D60"],
  "\u62BD\u5956": ["\u62BD\u7B7E", "\u4E2D\u5956", "\u5E78\u8FD0\u62BD\u5956", "\u62BD\u5956\u6D3B\u52A8"],
  "\u56E2\u8D2D": ["\u62FC\u56E2", "\u7EC4\u56E2", "\u56E2\u8D2D\u4EF7", "\u5F00\u56E2"],
  "\u780D\u4EF7": ["\u8BB2\u4EF7", "\u8FD8\u4EF7", "\u780D\u4E00\u5200", "\u4FBF\u5B9C\u70B9"],
  "\u8BD5\u7A7F": ["\u8BD5\u8863", "\u8BD5\u6234", "\u8BD5\u7528", "\u4F53\u9A8C"],
  "\u5B9A\u5236": ["\u4E2A\u6027\u5316", "\u79C1\u4EBA\u5B9A\u5236", "\u4E13\u5C5E", "\u624B\u5DE5"],
  "\u4E8C\u624B": ["\u4E8C\u624B\u95F2\u7F6E", "\u95F2\u9C7C", "\u65E7\u8D27", "\u8F6C\u8BA9"],
  "\u95F2\u9C7C": ["\u4E8C\u624B\u5E73\u53F0", "\u8F6C\u8F6C", "\u95F2\u7F6E", "\u4E8C\u624B\u4EA4\u6613"],
  "\u5962\u4F88\u54C1": ["luxury", "\u5927\u724C", "\u540D\u724C", "\u5962\u4F88"],
  "\u5316\u5986\u54C1": ["\u7F8E\u5986", "\u62A4\u80A4\u54C1", "\u5F69\u5986", "cosmetics"],
  "\u62A4\u80A4\u54C1": ["skincare", "\u9762\u971C", "\u7CBE\u534E", "\u6C34\u4E73"],
  "\u53E3\u7EA2": ["lipstick", "\u5507\u818F", "\u8272\u53F7", "\u6D82\u53E3\u7EA2"],
  "\u9999\u6C34": ["perfume", "\u9999\u6C1B", "\u55B7\u9999\u6C34", "\u9999\u5473"],
  "\u670D\u88C5": ["\u8863\u670D", "\u670D\u9970", "\u7A7F\u642D", "fashion"],
  "\u978B\u5B50": ["shoes", "\u7403\u978B", "\u8FD0\u52A8\u978B", "\u62D6\u978B"],
  "\u7403\u978B": ["sneaker", "AJ", "\u6930\u5B50", "\u8FD0\u52A8\u978B", "\u9650\u91CF\u978B"],
  "\u624B\u8868": ["watch", "\u8155\u8868", "\u667A\u80FD\u624B\u8868", "\u673A\u68B0\u8868"],
  "\u6570\u7801\u4EA7\u54C1": ["\u7535\u5B50\u4EA7\u54C1", "\u6570\u7801", "3C", "\u79D1\u6280\u4EA7\u54C1"],
  "\u5BB6\u7535": ["\u7535\u5668", "\u5BB6\u7528\u7535\u5668", "\u5C0F\u5BB6\u7535", "\u5927\u5BB6\u7535"],
  "\u5BB6\u5177": ["furniture", "\u6C99\u53D1", "\u684C\u6905", "\u67DC\u5B50"],
  "\u751F\u9C9C": ["\u852C\u679C", "\u65B0\u9C9C\u98DF\u6750", "\u51B7\u94FE", "\u751F\u9C9C\u914D\u9001"],
  "\u7AE5\u88C5": ["\u513F\u7AE5\u670D\u88C5", "\u5B9D\u5B9D\u8863\u670D", "\u7AE5\u978B"],
  "\u5185\u8863": ["\u6587\u80F8", "\u5185\u88E4", "\u8D34\u8EAB\u8863\u7269", "underwear"],
  "\u9632\u6652": ["\u9632\u6652\u971C", "\u906E\u9633", "\u9632\u6652\u8863", "SPF"],
  "\u773C\u971C": ["\u773C\u90E8\u62A4\u7406", "\u53BB\u9ED1\u773C\u5708", "\u6297\u76B1"],
  "\u9762\u819C": ["\u8D34\u7247\u9762\u819C", "\u6CE5\u819C", "\u7761\u7720\u9762\u819C", "\u8865\u6C34\u9762\u819C"],
  "\u6D17\u9762\u5976": ["\u6D01\u9762\u4E73", "\u6D17\u8138", "\u6E05\u6D01", "\u6C28\u57FA\u9178\u6D17\u9762\u5976"],
  "\u6C90\u6D74\u9732": ["body wash", "\u6C90\u6D74", "\u8EAB\u4F53\u6E05\u6D01"],
  "\u6D17\u53D1\u6C34": ["shampoo", "\u62A4\u53D1\u7D20", "\u6D17\u62A4"],
  "\u7259\u818F": ["\u5237\u7259", "\u7259\u5237", "\u53E3\u8154\u62A4\u7406", "toothpaste"],
  "\u7EB8\u5DFE": ["\u62BD\u7EB8", "\u6E7F\u5DFE", "\u536B\u751F\u7EB8", "\u624B\u5E15\u7EB8"],
  "\u5783\u573E\u888B": ["\u5783\u573E\u6876", "\u4FDD\u9C9C\u888B", "\u6536\u7EB3\u888B"],
  "\u5145\u7535\u5668": ["\u5145\u7535\u5934", "\u5FEB\u5145", "\u65E0\u7EBF\u5145\u7535", "\u5145\u7535\u5957\u88C5"],
  "\u6570\u636E\u7EBF": ["\u5145\u7535\u7EBF", "Type-C", "Lightning", "\u6570\u636E\u4F20\u8F93"],
  "\u884C\u674E\u7BB1": ["\u62C9\u6746\u7BB1", "\u65C5\u884C\u7BB1", "\u767B\u673A\u7BB1", "\u6258\u8FD0\u7BB1"],
  "\u80CC\u5305": ["\u53CC\u80A9\u5305", "\u4E66\u5305", "\u7535\u8111\u5305", "backpack"],
  "\u94B1\u5305": ["wallet", "\u5361\u5305", "\u96F6\u94B1\u5305", "\u957F\u6B3E\u94B1\u5305"],
  "\u773C\u955C": ["glasses", "\u58A8\u955C", "\u592A\u9633\u955C", "\u955C\u6846"],
  "\u5E3D\u5B50": ["hat", "\u68D2\u7403\u5E3D", "\u6E14\u592B\u5E3D", "\u906E\u9633\u5E3D"],
  "\u56F4\u5DFE": ["scarf", "\u4E1D\u5DFE", "\u62AB\u80A9", "\u56F4\u8116"],
  "\u624B\u5957": ["gloves", "\u4FDD\u6696\u624B\u5957", "\u89E6\u5C4F\u624B\u5957"],
  "\u889C\u5B50": ["socks", "\u68C9\u889C", "\u957F\u889C", "\u8239\u889C"],
  "\u4FDD\u6E29\u676F": ["\u6C34\u676F", "\u4FDD\u6E29\u58F6", "\u968F\u884C\u676F", "\u676F\u5B50"],
  "\u96E8\u4F1E": ["umbrella", "\u6298\u53E0\u4F1E", "\u592A\u9633\u4F1E", "\u81EA\u52A8\u4F1E"],
  "\u6587\u5177": ["\u7B14", "\u672C\u5B50", "\u6587\u5177\u76D2", "\u529E\u516C\u7528\u54C1"],
  "\u73A9\u5177": ["toy", "\u79EF\u6728", "\u4E50\u9AD8", "\u6BDB\u7ED2\u73A9\u5177"],
  // ── 日常生活/习惯（100组）──────────────────────────────────────────────
  "\u8D77\u5E8A": ["\u9192\u6765", "\u8D77\u6765", "\u95F9\u949F\u54CD", "\u7741\u773C"],
  "\u8D56\u5E8A": ["\u4E0D\u60F3\u8D77", "\u8D2A\u7761", "\u518D\u7761\u4F1A", "\u8D77\u4E0D\u6765"],
  "\u6D17\u8138": ["\u6D01\u9762", "\u5378\u5986", "\u6D17\u9762\u5976", "\u6E05\u6D01\u9762\u90E8"],
  "\u6D17\u5934": ["\u6D17\u53D1", "\u6D17\u5934\u53D1", "\u6D17\u53D1\u6C34", "\u62A4\u53D1\u7D20"],
  "\u62A4\u80A4": ["\u6D82\u9762\u971C", "\u6D82\u9632\u6652", "\u6577\u9762\u819C", "\u4FDD\u517B"],
  "\u6577\u9762\u819C": ["\u9762\u819C", "\u8D34\u9762\u819C", "\u62A4\u7406", "\u8865\u6C34"],
  "\u5439\u5934\u53D1": ["\u5439\u98CE\u673A", "\u5439\u5E72", "\u9020\u578B"],
  "\u6362\u8863\u670D": ["\u7A7F\u8863\u670D", "\u642D\u914D", "\u9009\u8863\u670D", "\u6362\u88C5"],
  "\u6324\u5730\u94C1": ["\u6324\u516C\u4EA4", "\u65E9\u9AD8\u5CF0", "\u4EBA\u592A\u591A", "\u6C99\u4E01\u9C7C"],
  "\u5237\u5361": ["\u6253\u5361", "\u5237\u4EA4\u901A\u5361", "\u626B\u7801\u4E58\u8F66"],
  "\u7B49\u7535\u68AF": ["\u5750\u7535\u68AF", "\u6324\u7535\u68AF", "\u7535\u68AF\u95F4"],
  "\u5348\u996D": ["\u4E2D\u996D", "\u5348\u9910", "\u4E2D\u5348\u5403\u4EC0\u4E48", "\u5DE5\u4F5C\u9910"],
  "\u4E0B\u5348\u8336": ["teatime", "\u70B9\u5FC3", "\u559D\u4E0B\u5348\u8336", "\u6478\u9C7C\u5403"],
  "\u6D17\u8863\u670D": ["\u6D17\u8863\u673A", "\u667E\u8863\u670D", "\u71A8\u70EB", "\u6D17\u6DA4"],
  "\u667E\u8863\u670D": ["\u6652\u8863\u670D", "\u667E\u6652", "\u6302\u8863\u670D", "\u6536\u8863\u670D"],
  "\u53E0\u8863\u670D": ["\u6574\u7406\u8863\u670D", "\u6536\u7EB3", "\u53E0\u88AB\u5B50"],
  "\u62D6\u5730": ["\u64E6\u5730", "\u62D6\u628A", "\u6E7F\u62D6", "\u5E72\u62D6"],
  "\u64E6\u7A97": ["\u64E6\u73BB\u7483", "\u64E6\u7A97\u6237", "\u6E05\u6D01\u7A97\u6237"],
  "\u6D17\u7897": ["\u5237\u7897", "\u6D17\u7897\u673A", "\u6D17\u76D8\u5B50", "\u6E05\u6D17\u9910\u5177"],
  "\u6536\u62FE\u623F\u95F4": ["\u6574\u7406\u623F\u95F4", "\u6253\u626B\u623F\u95F4", "\u6536\u62FE\u5C4B\u5B50"],
  "\u6362\u5E8A\u5355": ["\u6362\u88AB\u5957", "\u6D17\u5E8A\u5355", "\u6362\u5E8A\u54C1"],
  "\u6D47\u82B1": ["\u517B\u82B1", "\u6D47\u6C34", "\u82B1\u8349", "\u7EFF\u690D"],
  "\u517B\u9C7C": ["\u9C7C\u7F38", "\u6362\u6C34", "\u5582\u9C7C", "\u89C2\u8D4F\u9C7C"],
  "\u5582\u5BA0\u7269": ["\u5582\u732B", "\u5582\u72D7", "\u5BA0\u7269\u7CAE", "\u5BA0\u7269\u96F6\u98DF"],
  "\u716E\u5496\u5561": ["\u51B2\u5496\u5561", "\u78E8\u8C46", "\u5496\u5561\u673A", "\u624B\u51B2"],
  "\u6CE1\u8336": ["\u8336\u9053", "\u559D\u8336", "\u6CE1\u529F\u592B\u8336", "\u716E\u8336"],
  "\u770B\u65B0\u95FB": ["\u5237\u65B0\u95FB", "\u4ECA\u65E5\u5934\u6761", "\u770B\u62A5", "\u65E9\u62A5"],
  "\u770B\u5929\u6C14": ["\u5929\u6C14\u9884\u62A5", "\u67E5\u5929\u6C14", "\u660E\u5929\u5929\u6C14"],
  "\u5E26\u4F1E": ["\u5E26\u96E8\u4F1E", "\u4E0B\u96E8\u4E86", "\u5FD8\u5E26\u4F1E"],
  "\u5316\u5986\u51FA\u95E8": ["\u6253\u626E", "\u753B\u5986", "\u51FA\u95E8\u524D", "\u7167\u955C\u5B50"],
  "\u63A5\u5B69\u5B50": ["\u63A5\u653E\u5B66", "\u5E7C\u513F\u56ED\u63A5", "\u5B66\u6821\u95E8\u53E3\u7B49"],
  "\u8F85\u5BFC\u4F5C\u4E1A": ["\u966A\u5199\u4F5C\u4E1A", "\u68C0\u67E5\u4F5C\u4E1A", "\u5BB6\u5EAD\u4F5C\u4E1A"],
  "\u54C4\u7761": ["\u54C4\u5B9D\u5B9D", "\u8BB2\u6545\u4E8B", "\u7761\u524D\u6545\u4E8B", "\u6447\u7BEE\u66F2"],
  "\u505A\u65E9\u64CD": ["\u6668\u64CD", "\u5E7F\u64AD\u4F53\u64CD", "\u6668\u95F4\u8FD0\u52A8"],
  "\u901B\u8D85\u5E02": ["\u8D85\u5E02\u8D2D\u7269", "\u4E70\u83DC", "\u901B\u5546\u573A"],
  "\u4E70\u83DC": ["\u83DC\u5E02\u573A", "\u4E70\u98DF\u6750", "\u6311\u83DC", "\u9009\u83DC"],
  "\u4E0B\u73ED": ["\u6536\u5DE5", "\u4E0B\u73ED\u4E86", "\u51C6\u65F6\u4E0B\u73ED", "\u5230\u70B9\u8D70"],
  "\u56DE\u5BB6": ["\u56DE\u53BB", "\u5230\u5BB6", "\u5230\u5BB6\u4E86", "\u56DE\u5BB6\u8DEF\u4E0A"],
  "\u6362\u62D6\u978B": ["\u8FDB\u95E8\u6362\u978B", "\u5BA4\u5185\u978B", "\u7A7F\u62D6\u978B"],
  "\u6D17\u624B": ["\u6E05\u6D01\u53CC\u624B", "\u6D17\u624B\u6DB2", "\u6D88\u6BD2"],
  "\u6362\u7761\u8863": ["\u7A7F\u7761\u8863", "\u6362\u8212\u670D\u7684", "\u5BB6\u5C45\u670D"],
  "\u770B\u7535\u89C6": ["\u770B\u8282\u76EE", "\u9065\u63A7\u5668", "\u6362\u53F0", "\u770B\u9891\u9053"],
  "\u73A9\u624B\u673A": ["\u5237\u624B\u673A", "\u770B\u624B\u673A", "\u624B\u673A\u4E0D\u79BB\u624B", "\u5C4F\u5E55\u65F6\u95F4"],
  "\u591C\u5BB5": ["\u5403\u591C\u5BB5", "\u5BB5\u591C", "\u534A\u591C\u5403", "\u6DF1\u591C\u98DF\u5802"],
  "\u6577\u70ED\u6C34\u888B": ["\u6696\u6C34\u888B", "\u6696\u5B9D\u5B9D", "\u53D6\u6696"],
  "\u5173\u706F": ["\u5F00\u706F", "\u706F\u5149", "\u53F0\u706F", "\u591C\u706F"],
  "\u8BBE\u95F9\u949F": ["\u5B9A\u95F9\u949F", "\u95F9\u949F\u51E0\u70B9", "\u63D0\u9192"],
  "\u5145\u624B\u673A": ["\u5145\u7535", "\u624B\u673A\u5FEB\u6CA1\u7535", "\u5145\u7535\u5668", "\u5145\u7535\u7EBF"],
  "\u9501\u95E8": ["\u5173\u95E8", "\u53CD\u9501", "\u5E26\u94A5\u5319", "\u95E8\u7981"],
  "\u7A7F\u5916\u5957": ["\u52A0\u8863\u670D", "\u7A7F\u591A\u70B9", "\u51B7\u4E86\u52A0\u8863"],
  "\u6234\u53E3\u7F69": ["\u53E3\u7F69", "\u9632\u62A4", "\u51FA\u95E8\u6234\u53E3\u7F69"],
  "\u64E6\u684C\u5B50": ["\u64E6\u53F0\u9762", "\u62B9\u5E03", "\u6E05\u6D01\u684C\u9762"],
  "\u6536\u5FEB\u9012": ["\u53D6\u5305\u88F9", "\u5FEB\u9012\u67DC", "\u83DC\u9E1F\u9A7F\u7AD9", "\u4E30\u5DE2"],
  "\u5BC4\u5FEB\u9012": ["\u5BC4\u4E1C\u897F", "\u53D1\u8D27", "\u53EB\u5FEB\u9012\u5458"],
  "\u4EA4\u6C34\u7535\u8D39": ["\u4EA4\u623F\u79DF", "\u7F34\u8D39", "\u6C34\u7535\u7164", "\u7269\u4E1A\u8D39"],
  "\u4FEE\u4E1C\u897F": ["\u4FEE\u7406", "\u574F\u4E86\u4FEE", "\u7EF4\u4FEE", "\u627E\u5E08\u5085"],
  "\u6362\u706F\u6CE1": ["\u706F\u574F\u4E86", "\u6362\u706F", "\u4FEE\u706F"],
  "\u901A\u9A6C\u6876": ["\u9A6C\u6876\u5835\u4E86", "\u5395\u6240\u5835\u4E86", "\u4E0B\u6C34\u9053"],
  "\u5012\u6C34": ["\u63A5\u6C34", "\u559D\u6C34", "\u70ED\u6C34", "\u51C9\u767D\u5F00"],
  "\u5348\u89C9": ["\u5348\u7761", "\u5C0F\u61A9", "\u6253\u4E2A\u76F9", "\u772F\u4E00\u4F1A"],
  "\u4F38\u61D2\u8170": ["\u8212\u5C55", "\u6D3B\u52A8\u7B4B\u9AA8", "\u8D77\u6765\u52A8\u52A8"],
  "\u773C\u4FDD\u5065\u64CD": ["\u62A4\u773C", "\u4F11\u606F\u773C\u775B", "\u770B\u8FDC\u5904"],
  "\u79F0\u4F53\u91CD": ["\u4E0A\u79E4", "\u4F53\u91CD\u8BA1", "\u6BCF\u65E5\u79F0\u91CD"],
  "\u8BB0\u65E5\u8BB0": ["\u5199\u65E5\u8BB0", "\u65E5\u8BB0\u672C", "\u6BCF\u65E5\u8BB0\u5F55", "\u624B\u8D26"],
  "\u624B\u8D26": ["\u624B\u5E10", "\u8BB0\u5F55", "bullet journal", "\u624B\u8D26\u672C"],
  "\u51A5\u60F3": ["meditation", "\u6B63\u5FF5", "\u6253\u5750", "\u9759\u5FC3"],
  "\u6CE1\u811A": ["\u70ED\u6C34\u6CE1\u811A", "\u8DB3\u6D74", "\u517B\u751F"],
  "\u559D\u725B\u5976": ["\u7761\u524D\u5976", "\u70ED\u725B\u5976", "\u4E00\u676F\u725B\u5976"],
  "\u5237\u5267": ["\u8FFD\u5267", "\u770B\u5267", "\u7172\u5267", "\u4E00\u53E3\u6C14\u770B\u5B8C"],
  "\u5237\u89C6\u9891": ["\u77ED\u89C6\u9891", "\u5237\u6296\u97F3", "\u5237\u5FEB\u624B", "\u5237B\u7AD9"],
  "\u53EB\u5916\u5356": ["\u70B9\u9910", "\u5916\u5356\u5230\u4E86", "\u7B49\u5916\u5356", "\u5916\u5356\u5C0F\u54E5"],
  "\u7B49\u516C\u4EA4": ["\u7B49\u8F66", "\u516C\u4EA4\u7AD9", "\u8F66\u8FD8\u6CA1\u6765"],
  "\u8D76\u8DEF": ["\u8D76\u65F6\u95F4", "\u5FEB\u8FDF\u5230\u4E86", "\u52A0\u5FEB\u811A\u6B65"],
  "\u96E8\u5929": ["\u4E0B\u96E8", "\u4E0B\u96E8\u4E86", "\u9634\u5929", "\u66B4\u96E8"],
  "\u964D\u6E29": ["\u53D8\u51B7", "\u51B7\u7A7A\u6C14", "\u964D\u6E29\u4E86", "\u5165\u51AC"],
  "\u5347\u6E29": ["\u53D8\u70ED", "\u70ED\u4E86", "\u56DE\u6696", "\u5347\u6E29\u4E86"],
  "\u6362\u5B63": ["\u5B63\u8282\u4EA4\u66FF", "\u6362\u5B63\u8863\u670D", "\u6625\u79CB\u6362\u5B63"],
  "\u8FC7\u5468\u672B": ["\u5468\u672B\u5B89\u6392", "\u4F11\u606F\u65E5", "\u53CC\u4F11", "\u653E\u677E"],
  "\u5B85\u5BB6": ["\u7A9D\u5BB6", "\u5728\u5BB6\u5F85\u7740", "\u54EA\u90FD\u4E0D\u53BB", "\u5BB6\u91CC\u8E72"],
  "\u901B\u516C\u56ED": ["\u53BB\u516C\u56ED", "\u516C\u56ED\u6563\u6B65", "\u6237\u5916\u6D3B\u52A8"],
  "\u901B\u5546\u573A": ["\u901B\u8857", "\u5546\u573A\u8D2D\u7269", "\u6A71\u7A97", "\u8840\u62FC"],
  "\u7EA6\u670B\u53CB": ["\u7EA6\u4EBA", "\u53EB\u4E0A\u670B\u53CB", "\u4E00\u8D77\u51FA\u53BB\u73A9"],
  "\u805A\u9910": ["\u5403\u996D", "\u996D\u5C40", "\u7EA6\u996D", "\u56E2\u5EFA\u5403\u996D"],
  "\u70E4\u8089": ["\u97E9\u5F0F\u70E4\u8089", "\u65E5\u5F0F\u70E4\u8089", "\u81EA\u52A9\u70E4\u8089", "\u70E4\u4E94\u82B1\u8089"],
  "\u81EA\u52A9\u9910": ["buffet", "\u81EA\u52A9", "\u4E0D\u9650\u91CF", "\u5403\u56DE\u672C"],
  "\u5403\u706B\u9505": ["\u6DAE\u706B\u9505", "\u7EA6\u706B\u9505", "\u706B\u9505\u5C40"],
  "\u62CD\u5168\u5BB6\u798F": ["\u5BB6\u5EAD\u7167", "\u5408\u5F71", "\u5168\u5BB6\u5408\u7167"],
  "\u5927\u626B\u9664": ["\u5E74\u7EC8\u5927\u626B\u9664", "\u5168\u5C4B\u6E05\u6D01", "\u5F7B\u5E95\u6253\u626B"],
  "\u6362\u5B63\u6536\u7EB3": ["\u6536\u7EB3\u6574\u7406", "\u8863\u67DC\u6574\u7406", "\u6362\u5B63\u8863\u7269"],
  "\u7F51\u4E0A\u529E\u4E8B": ["\u7EBF\u4E0A\u529E\u7406", "\u7535\u5B50\u653F\u52A1", "\u7F51\u4E0A\u9884\u7EA6"],
  "\u6392\u53F7\u7B49\u4F4D": ["\u7B49\u53EB\u53F7", "\u53D6\u53F7", "\u6392\u961F\u7B49"],
  "\u526A\u6307\u7532": ["\u6307\u7532\u94B3", "\u4FEE\u6307\u7532", "\u7F8E\u7532"],
  "\u7406\u53D1\u9884\u7EA6": ["\u9884\u7EA6\u7406\u53D1", "\u526A\u5934", "\u7EA6Tony"],
  "\u6652\u592A\u9633": ["\u65E5\u5149\u6D74", "\u6652", "\u6652\u6696"],
  "\u6253\u54C8\u6B20": ["\u56F0\u4E86", "\u72AF\u56F0", "\u778C\u7761"],
  "\u7FFB\u8EAB": ["\u8F97\u8F6C", "\u7FFB\u6765\u8986\u53BB", "\u7761\u4E0D\u7740\u7FFB\u8EAB"],
  "\u5F00\u7A97\u901A\u98CE": ["\u901A\u98CE", "\u6362\u6C14", "\u5F00\u7A97"],
  "\u5173\u7A97": ["\u5173\u7A97\u6237", "\u7A97\u6237\u5173\u4E86", "\u6015\u51B7\u5173\u7A97"],
  "\u5F00\u7A7A\u8C03": ["\u7A7A\u8C03", "\u5236\u51B7", "\u5236\u6696", "\u8C03\u6E29\u5EA6"],
  "\u5F00\u6696\u6C14": ["\u6696\u6C14", "\u6696\u98CE", "\u4F9B\u6696", "\u5730\u6696"],
  "\u5582\u5976": ["\u6BCD\u4E73", "\u5976\u74F6", "\u51B2\u5976\u7C89", "\u5582\u5B9D\u5B9D"],
  "\u6362\u5C3F\u5E03": ["\u5C3F\u4E0D\u6E7F", "\u7EB8\u5C3F\u88E4", "\u6362\u5C3F\u88E4"],
  "\u80CC\u5355\u8BCD": ["\u8BB0\u5355\u8BCD", "\u5355\u8BCD\u672C", "\u80CC\u82F1\u8BED", "\u8BCD\u6C47"],
  "\u5F39\u7434": ["\u7EC3\u7434", "\u5F39\u94A2\u7434", "\u5F39\u5409\u4ED6", "\u7EC3\u4E60"],
  "\u505A\u624B\u5DE5": ["\u624B\u5DE5", "DIY", "\u624B\u4F5C", "\u7F16\u7EC7"],
  "\u79CD\u83DC": ["\u79CD\u5730", "\u83DC\u56ED", "\u9633\u53F0\u79CD\u83DC", "\u852C\u83DC\u79CD\u690D"],
  "\u5582\u9E1F": ["\u517B\u9E1F", "\u9E1F\u7B3C", "\u9E1F\u98DF"],
  "\u905B\u5C0F\u5B69": ["\u5E26\u5C0F\u5B69", "\u63A8\u5A74\u513F\u8F66", "\u6237\u5916\u73A9"],
  "\u63A5\u7535\u8BDD": ["\u6253\u7535\u8BDD", "\u901A\u8BDD", "\u6765\u7535\u8BDD\u4E86"],
  "\u56DE\u6D88\u606F": ["\u56DE\u5FAE\u4FE1", "\u56DE\u590D", "\u770B\u6D88\u606F"],
  "\u8BA2\u5916\u5356": ["\u70B9\u5916\u5356", "\u4E0B\u5355\u5916\u5356", "\u53EB\u9910"],
  "\u627E\u94A5\u5319": ["\u94A5\u5319\u4E22\u4E86", "\u94A5\u5319\u5728\u54EA", "\u5FD8\u5E26\u94A5\u5319"],
  "\u4FEE\u7709": ["\u4FEE\u7709\u6BDB", "\u753B\u7709", "\u7709\u7B14"],
  "\u64E6\u978B": ["\u5237\u978B", "\u6D17\u978B", "\u978B\u6CB9"],
  "\u8865\u89C9": ["\u8865\u7720", "\u591A\u7761\u4F1A", "\u7761\u56DE\u7B3C\u89C9"],
  "\u505A\u68A6": ["\u68A6", "\u5669\u68A6", "\u68A6\u5883", "\u505A\u4E86\u4E2A\u68A6"],
  "\u6253\u55DD": ["\u55DD", "\u6B62\u55DD", "\u6253\u4E86\u4E2A\u55DD"],
  "\u6253\u55B7\u568F": ["\u55B7\u568F", "\u9F3B\u5B50\u75D2", "achoo"],
  "\u4F38\u5C55": ["\u62C9\u4F38", "\u505A\u62C9\u4F38", "\u4F38\u5C55\u8FD0\u52A8"],
  "\u8DF3\u7EF3": ["\u8DF3\u7EF3\u8FD0\u52A8", "\u82B1\u5F0F\u8DF3\u7EF3", "\u8DF3\u7EF3\u51CF\u80A5"]
};
const _synonymsByLang = /* @__PURE__ */ new Map();
const _reverseIndex = /* @__PURE__ */ new Map();
function buildReverseIndex(lang, syns) {
  const idx = /* @__PURE__ */ new Map();
  for (const [key, words] of Object.entries(syns)) {
    for (const w of words) {
      if (!idx.has(w)) idx.set(w, []);
      idx.get(w).push(key);
    }
  }
  _reverseIndex.set(lang, idx);
}
function classifySynonymLang(key) {
  return detectLanguage(key);
}
function splitDefaultSynonyms() {
  const zh = {};
  const en = {};
  for (const [key, syns] of Object.entries(_defaultSynonyms)) {
    const lang = classifySynonymLang(key);
    if (lang === "zh") zh[key] = syns;
    else en[key] = syns;
  }
  return { zh, en };
}
function getSynonyms(lang) {
  if (!_synonymsByLang.has(lang)) {
    const p = synonymsPath(lang);
    const defaults = splitDefaultSynonyms();
    const seed = defaults[lang] || {};
    const loaded = loadJson(p, seed);
    let dirty = false;
    for (const [key, syns] of Object.entries(seed)) {
      if (!loaded[key]) {
        loaded[key] = syns;
        dirty = true;
      } else {
        for (const syn of syns) {
          if (!loaded[key].includes(syn)) {
            loaded[key].push(syn);
            dirty = true;
          }
        }
      }
    }
    try {
      const seedPath = resolve(DATA_DIR, `seeds-${lang}.json`);
      if (existsSync(seedPath)) {
        const seeds = JSON.parse(readFileSync(seedPath, "utf-8"));
        let seedCount = 0;
        for (const [key, syns] of Object.entries(seeds)) {
          if (key.startsWith("_")) continue;
          if (!loaded[key]) {
            loaded[key] = syns;
            dirty = true;
            seedCount++;
          } else {
            for (const syn of syns) {
              if (!loaded[key].includes(syn)) {
                loaded[key].push(syn);
                dirty = true;
              }
            }
          }
        }
        if (seedCount > 0) console.log(`[cc-soul][aam] loaded ${seedCount} seed groups from seeds-${lang}.json`);
      }
    } catch {
    }
    if (dirty || !existsSync(p)) debouncedSave(p, loaded);
    _synonymsByLang.set(lang, loaded);
    buildReverseIndex(lang, loaded);
  }
  return _synonymsByLang.get(lang);
}
function migrateOldSynonyms() {
  const oldPath = resolve(DATA_DIR, "aam_synonyms.json");
  if (!existsSync(oldPath)) return;
  if (existsSync(synonymsPath("zh"))) return;
  try {
    const old = loadJson(oldPath, {});
    const zh = {};
    const en = {};
    for (const [key, syns] of Object.entries(old)) {
      if (/^[\u4e00-\u9fff]{2}$/.test(key) && isJunkToken(key)) continue;
      const cleanSyns = syns.filter((s) => {
        if (typeof s !== "string" || s.length < 2) return false;
        if (/^[\u4e00-\u9fff]{2}$/.test(s) && isJunkToken(s)) return false;
        return true;
      });
      if (cleanSyns.length === 0) continue;
      if (classifySynonymLang(key) === "zh") zh[key] = cleanSyns;
      else en[key] = cleanSyns;
    }
    if (Object.keys(zh).length > 0) debouncedSave(synonymsPath("zh"), zh);
    if (Object.keys(en).length > 0) debouncedSave(synonymsPath("en"), en);
    console.log(`[cc-soul][aam] migrated legacy aam_synonyms.json \u2192 per-language (zh: ${Object.keys(zh).length}, en: ${Object.keys(en).length})`);
  } catch {
  }
}
migrateOldSynonyms();
let COLD_START_SYNONYMS = getSynonyms("zh");
const _enSynonyms = getSynonyms("en");
let _seedTranslationDone = false;
function maybeTranslateSeedsForLanguage(userMsg) {
  if (_seedTranslationDone) return;
  _seedTranslationDone = true;
  const hasCJK = /[\u4e00-\u9fff]/.test(userMsg);
  const hasLatin = /[a-zA-Z]{3,}/.test(userMsg);
  if (hasCJK || hasLatin) return;
  try {
    const { hasLLM, spawnCLI } = require("./cli.ts");
    if (!hasLLM()) return;
    const coreSeedWords = ["\u5F00\u5FC3", "\u96BE\u8FC7", "\u751F\u6C14", "\u5BB3\u6015", "\u559C\u6B22", "\u8BA8\u538C", "\u5DE5\u4F5C", "\u5BB6\u4EBA", "\u670B\u53CB", "\u5065\u5EB7"];
    spawnCLI(
      `Translate these Chinese words to the SAME language as this message: "${userMsg.slice(0, 50)}"

Words: ${coreSeedWords.join(", ")}

Output format: one translation per line, same order. Just the word, no explanation.`,
      (output) => {
        if (!output || output.length < 10) return;
        const translations = output.split("\n").map((l) => l.trim()).filter((l) => l.length >= 1);
        if (translations.length < 5) return;
        for (let i = 0; i < Math.min(coreSeedWords.length, translations.length); i++) {
          const key = coreSeedWords[i];
          const translated = translations[i].toLowerCase();
          if (!COLD_START_SYNONYMS[key]) COLD_START_SYNONYMS[key] = [];
          if (!COLD_START_SYNONYMS[key].includes(translated)) {
            COLD_START_SYNONYMS[key].push(translated);
          }
        }
        debouncedSave(synonymsPath("zh"), COLD_START_SYNONYMS);
        try {
          require("./decision-log.ts").logDecision("seed_translation", userMsg.slice(0, 20), `translated ${translations.length} seed words`);
        } catch {
        }
      },
      15e3
    );
  } catch {
  }
}
function injectSeedsLite(lang) {
  const net = getNetwork(lang);
  const syns = getSynonyms(lang);
  let dfInjected = 0, pairInjected = 0;
  for (const [word, synonyms] of Object.entries(syns)) {
    const allWords = [word, ...synonyms];
    for (const w of allWords) {
      if (w.length >= 2 && !net.df[w]) {
        net.df[w] = 2;
        dfInjected++;
      }
      const cjk = w.match(/[\u4e00-\u9fff]+/g) || [];
      for (const seg of cjk) {
        for (let i = 0; i <= seg.length - 2; i++) {
          const sub = seg.slice(i, i + 2);
          if (!net.df[sub]) {
            net.df[sub] = 2;
            dfInjected++;
          }
        }
      }
    }
    const keyToken = word.length >= 2 ? word.toLowerCase() : null;
    if (!keyToken) continue;
    for (const syn of synonyms) {
      const synToken = syn.length >= 2 ? syn.toLowerCase() : null;
      if (!synToken || synToken === keyToken) continue;
      const existing = net.cooccur[keyToken]?.[synToken] ?? 0;
      if (existing < 2) {
        if (!net.cooccur[keyToken]) net.cooccur[keyToken] = {};
        net.cooccur[keyToken][synToken] = 2;
        if (!net.cooccur[synToken]) net.cooccur[synToken] = {};
        net.cooccur[synToken][keyToken] = 2;
        pairInjected++;
      }
    }
  }
  if (dfInjected > 0 || pairInjected > 0) {
    console.log(`[cc-soul][aam] seed injection [${lang}]: ${dfInjected} df + ${pairInjected} cooccur pairs`);
  }
}
injectSeedsLite("zh");
injectSeedsLite("en");
function tokenize(text) {
  return _utilTokenize(text, "standard");
}
const STOPWORDS_PATH = resolve(DATA_DIR, "aam_stopwords.json");
const _defaultStopWords = [
  "\u7684",
  "\u4E86",
  "\u662F",
  "\u5728",
  "\u6211",
  "\u4F60",
  "\u4ED6",
  "\u5979",
  "\u5B83",
  "\u4EEC",
  "\u4E0D",
  "\u6709",
  "\u8FD9",
  "\u90A3",
  "\u5C31",
  "\u4E5F",
  "\u548C",
  "\u4F46",
  "\u8FD8",
  "\u90FD",
  "\u4F1A",
  "\u80FD",
  "\u53EF\u4EE5",
  "\u4EC0\u4E48",
  "\u600E\u4E48",
  "\u4E3A\u4EC0\u4E48",
  "\u5417",
  "\u5462",
  "\u5427",
  "\u5F88",
  "\u592A",
  "\u6700",
  "\u6BD4\u8F83",
  "\u975E\u5E38",
  "\u4E00\u4E2A",
  "\u4E00\u4E9B",
  "\u4E00\u4E0B",
  "\u88AB\u95EE",
  "\u95EE\u4E86",
  "\u5230\u4E86",
  "\u8BD5\u5B8C",
  "\u5B8C\u62FF",
  "\u62FF\u5230",
  "\u671F\u95F4",
  "\u591A\u4E86",
  "\u4E8C\u5929",
  "\u592A\u591A",
  "\u73ED\u592A",
  "\u7B2C\u4E8C",
  "\u4E0A\u5403",
  "\u60F3\u5B66",
  "\u5199\u4E86",
  "\u8BD5\u88AB",
  "\u5929\u79F0",
  "\u79F0\u91CD",
  "\u91CD\u6DA8",
  "\u6DA8\u4E86",
  "\u5C11\u5403",
  "\u70B9\u75BC",
  "the",
  "and",
  "for",
  "that",
  "this",
  "with",
  "from",
  "are",
  "was",
  "not",
  "but",
  "have",
  "has",
  "had",
  "will",
  "can",
  "you",
  "your"
];
const STOP_WORDS = new Set(loadJson(STOPWORDS_PATH, _defaultStopWords));
function filterStopWords(words) {
  return words.filter((w) => !STOP_WORDS.has(w) && w.length >= 2);
}
const CJK_FUNCTION_CHARS = new Set(
  "\u7684\u4E86\u662F\u5728\u5F88\u4E0D\u4E5F\u90FD\u5C31\u6709\u6211\u4F60\u4ED6\u5979\u5B83\u548C\u4E0E\u88AB\u628A\u8BA9\u7ED9\u4F1A\u80FD\u8981\u60F3\u5230\u8FC7\u7740\u5417\u5462\u5427\u554A\u4E48"
);
function isJunkToken(word) {
  if (word.length !== 2 || !/^[\u4e00-\u9fff]{2}$/.test(word)) return false;
  const chars = [...word];
  if (chars.length === 2 && CJK_FUNCTION_CHARS.has(chars[0]) && CJK_FUNCTION_CHARS.has(chars[1])) return true;
  if (network().totalDocs >= 50) {
    const cooc = network().cooccur[word];
    const fanOut = cooc ? Object.keys(cooc).length : 0;
    const df = network().df[word] || 0;
    const dfRatio = df / Math.max(1, network().totalDocs);
    let avgPMI = 0;
    if (cooc && fanOut > 0) {
      let sum = 0;
      for (const partner of Object.keys(cooc)) {
        sum += pmi(word, partner);
      }
      avgPMI = sum / fanOut;
    }
    if (fanOut > 20 && avgPMI < 1) return true;
    if (dfRatio > 0.3) return true;
    if (fanOut <= 1 && df <= 1) return true;
  }
  return false;
}
const CONCEPT_HIERARCHY = {
  // ── 健康 & 身体 & 健康隐患 ──
  "\u5065\u5EB7": ["\u8840\u538B", "\u8840\u7CD6", "\u4F53\u91CD", "\u7761\u7720", "\u5931\u7720", "\u8FD0\u52A8", "\u4F53\u68C0", "\u611F\u5192", "\u8FC7\u654F", "\u5934\u75BC", "\u8170\u75BC", "\u89C6\u529B", "\u8FD1\u89C6", "\u624B\u672F", "\u51CF\u80A5", "\u75AB\u82D7", "\u4E2D\u6691", "\u54EE\u5598", "\u80C3\u708E", "\u7259\u75BC", "\u819D\u76D6", "\u8170\u690E", "\u9888\u690E"],
  "\u8EAB\u4F53": ["\u8840\u538B", "\u8840\u7CD6", "\u4F53\u91CD", "\u7761\u7720", "\u8FD0\u52A8", "\u4F53\u68C0", "\u75B2\u52B3", "\u8170\u75BC", "\u8EAB\u9AD8", "\u4F53\u6E29", "\u5FC3\u7387"],
  "\u5065\u5EB7\u9690\u60A3": ["\u8FC7\u654F", "\u8FD1\u89C6", "\u8840\u538B", "\u8840\u7CD6", "\u5931\u7720", "\u80C3\u708E", "\u8170\u75BC", "\u9888\u690E", "\u7126\u8651", "\u80A5\u80D6"],
  "\u5065\u5EB7\u95EE\u9898": ["\u8840\u538B", "\u8840\u7CD6", "\u8FC7\u654F", "\u5931\u7720", "\u8FD1\u89C6", "\u80C3\u708E", "\u5934\u75BC", "\u8170\u75BC", "\u624B\u672F", "\u51CF\u80A5", "\u54EE\u5598", "\u7126\u8651"],
  // ── 经济 & 财务 & 理财 & 经济压力 ──
  "\u7ECF\u6D4E": ["\u623F\u8D37", "\u5DE5\u8D44", "\u85AA\u8D44", "\u6536\u5165", "\u80A1\u7968", "\u7406\u8D22", "\u50A8\u84C4", "\u82B1\u9500", "\u4FE1\u7528\u5361", "\u8D37\u6B3E", "\u7A0E", "\u4E8F\u94B1", "\u6B20\u6B3E"],
  "\u8D22\u52A1": ["\u623F\u8D37", "\u5DE5\u8D44", "\u6536\u5165", "\u80A1\u7968", "\u7406\u8D22", "\u50A8\u84C4", "\u4FE1\u7528\u5361", "\u8D37\u6B3E", "\u9884\u7B97"],
  "\u7406\u8D22": ["\u6295\u8D44", "\u5B58\u6B3E", "\u57FA\u91D1", "\u80A1\u7968", "\u623F\u8D37", "\u8F66\u8D37", "\u4FDD\u9669", "\u9884\u7B97", "\u6536\u5165", "\u82B1\u9500", "\u5B9A\u6295"],
  "\u7ECF\u6D4E\u538B\u529B": ["\u623F\u8D37", "\u8F66\u8D37", "\u8D37\u6B3E", "\u6B20\u6B3E", "\u4E8F\u94B1", "\u82B1\u9500", "\u4FE1\u7528\u5361", "\u5DE5\u8D44", "\u6DA8\u85AA", "\u5F00\u9500"],
  "\u6536\u5165\u53D8\u5316": ["\u6DA8\u85AA", "\u964D\u85AA", "\u5956\u91D1", "\u8DF3\u69FD", "\u52A0\u85AA", "\u5347\u804C", "\u7EE9\u6548"],
  // ── 学校 & 教育 & 考试 ──
  "\u5B66\u6821": ["\u5927\u5B66", "\u6BCD\u6821", "\u9AD8\u4E2D", "\u4E13\u4E1A", "\u5BFC\u5E08", "\u8BBA\u6587", "\u8003\u8BD5", "\u5B66\u4F4D", "\u6BD5\u4E1A", "\u540C\u5B66"],
  "\u6559\u80B2": ["\u5927\u5B66", "\u6BCD\u6821", "\u9AD8\u4E2D", "\u4E13\u4E1A", "\u5BFC\u5E08", "\u8BBA\u6587", "\u8003\u8BD5", "\u57F9\u8BAD", "\u5B66\u4F4D", "\u8BA4\u8BC1", "\u8003\u8BC1", "\u81EA\u5B66", "\u7F51\u8BFE"],
  "\u8003\u8BD5": ["\u8003\u7814", "\u8003\u516C", "\u96C5\u601D", "\u6258\u798F", "PMP", "\u9A7E\u7167", "\u6559\u8D44", "\u8BA4\u8BC1", "\u8003\u8BC1"],
  // ── 工作 & 职业 & 职业规划 ──
  "\u5DE5\u4F5C": ["\u52A0\u73ED", "\u85AA\u8D44", "\u540C\u4E8B", "\u8001\u677F", "\u9879\u76EE", "\u664B\u5347", "\u8DF3\u69FD", "\u9762\u8BD5", "\u7EE9\u6548", "\u88F8\u8F9E", "\u7B80\u5386", "\u8FDC\u7A0B", "\u51FA\u5DEE", "\u521B\u4E1A", "\u81EA\u7531\u804C\u4E1A", "\u8BA4\u8BC1", "PMP"],
  "\u804C\u4E1A": ["\u52A0\u73ED", "\u85AA\u8D44", "\u664B\u5347", "\u8DF3\u69FD", "\u9762\u8BD5", "\u7EE9\u6548", "\u8F6C\u884C"],
  "\u804C\u4E1A\u89C4\u5212": ["\u8DF3\u69FD", "\u9762\u8BD5", "\u8F6C\u884C", "\u664B\u5347", "\u7B80\u5386", "\u8003\u8BC1", "\u57F9\u8BAD", "\u6362\u5DE5\u4F5C", "\u521B\u4E1A", "\u76EE\u6807"],
  "\u5DE5\u4F5C\u7D2F": ["\u52A0\u73ED", "\u75B2\u60EB", "\u538B\u529B", "996", "\u71AC\u591C", "\u4F11\u606F", "\u5E74\u5047", "\u5026\u6020"],
  // ── 家庭 & 家人 ──
  "\u5BB6\u5EAD": ["\u7236\u6BCD", "\u7238\u5988", "\u5B69\u5B50", "\u8001\u5A46", "\u8001\u516C", "\u5BA0\u7269", "\u732B", "\u72D7", "\u5BB6\u52A1", "\u6000\u5B55", "\u9884\u4EA7\u671F", "\u751F\u5B69\u5B50", "\u5A5A\u793C", "\u751F\u65E5", "\u642C\u5BB6", "\u88C5\u4FEE"],
  "\u5BB6\u4EBA": ["\u7236\u6BCD", "\u7238\u5988", "\u5B69\u5B50", "\u8001\u5A46", "\u8001\u516C", "\u5144\u5F1F", "\u59D0\u59B9", "\u5973\u513F", "\u513F\u5B50", "\u7237\u7237", "\u5976\u5976", "\u5916\u5A46", "\u8205\u8205"],
  // ── 住房 & 居住 ──
  "\u4F4F\u623F": ["\u623F\u8D37", "\u79DF\u623F", "\u88C5\u4FEE", "\u642C\u5BB6", "\u5C0F\u533A", "\u7269\u4E1A", "\u623F\u4E1C", "\u623F\u4EF7"],
  "\u5C45\u4F4F": ["\u623F\u8D37", "\u79DF\u623F", "\u88C5\u4FEE", "\u642C\u5BB6", "\u5C0F\u533A", "\u623F\u4E1C"],
  // ── 饮食 & 吃 & 饮品 & 美食 ──
  "\u996E\u98DF": ["\u51CF\u80A5", "\u5916\u5356", "\u505A\u996D", "\u98DF\u8C31", "\u65E9\u9910", "\u5348\u9910", "\u665A\u9910", "\u96F6\u98DF", "\u8425\u517B", "\u5FCC\u53E3", "\u9999\u83DC", "\u8FC7\u654F\u98DF\u7269", "\u7D20\u98DF", "\u8FA3", "\u751C", "\u53A8\u827A", "\u62FF\u624B\u83DC"],
  "\u5403": ["\u5916\u5356", "\u505A\u996D", "\u65E9\u9910", "\u5348\u9910", "\u665A\u9910", "\u96F6\u98DF", "\u706B\u9505", "\u5976\u8336"],
  "\u996E\u54C1": ["\u5496\u5561", "\u8336", "\u5976\u8336", "\u679C\u6C41", "\u53EF\u4E50", "\u5564\u9152", "\u7EA2\u9152"],
  "\u7F8E\u98DF": ["\u706B\u9505", "\u70E4\u8089", "\u62C9\u9762", "\u5BFF\u53F8", "\u70E7\u70E4", "\u751C\u54C1", "\u5C0F\u5403", "\u6D77\u9C9C", "\u5DDD\u83DC", "\u7CA4\u83DC", "\u65E5\u6599", "\u897F\u9910", "\u62FF\u624B\u83DC", "\u5916\u5356"],
  // ── 厨艺 ──
  "\u53A8\u827A": ["\u505A\u996D", "\u70F9\u996A", "\u7092\u83DC", "\u84B8", "\u716E", "\u70E4", "\u62FF\u624B\u83DC", "\u83DC\u8C31", "\u4E0B\u53A8\u623F"],
  // ── 出行 & 交通 ──
  "\u51FA\u884C": ["\u5F00\u8F66", "\u5730\u94C1", "\u822A\u73ED", "\u51FA\u5DEE", "\u9AD8\u94C1", "\u6253\u8F66", "\u5835\u8F66", "\u673A\u7968", "\u901A\u52E4", "\u5171\u4EAB\u5355\u8F66", "\u9A7E\u7167", "\u81EA\u9A7E", "\u9A91\u884C"],
  "\u4EA4\u901A": ["\u5F00\u8F66", "\u5730\u94C1", "\u9AD8\u94C1", "\u6253\u8F66", "\u5835\u8F66", "\u516C\u4EA4"],
  // ── 情绪 & 心理 & 烦恼 & 恐惧 ──
  "\u60C5\u7EEA": ["\u7126\u8651", "\u538B\u529B", "\u6291\u90C1", "\u5931\u7720", "\u5F00\u5FC3", "\u70E6\u8E81", "\u75B2\u60EB", "\u5B64\u72EC", "\u5D29\u6E83", "\u6050\u60E7", "\u793E\u6050", "\u7D27\u5F20", "\u5BB3\u6015", "\u6050\u60E7\u75C7"],
  "\u5FC3\u7406": ["\u7126\u8651", "\u538B\u529B", "\u6291\u90C1", "\u5931\u7720", "\u70E6\u8E81", "\u5B64\u72EC", "\u54A8\u8BE2", "\u5FC3\u7406\u533B\u751F", "\u51A5\u60F3"],
  "\u70E6\u607C": ["\u538B\u529B", "\u7126\u8651", "\u4E8F\u94B1", "\u52A0\u73ED", "\u5931\u7720", "\u5435\u67B6", "\u7EA0\u7ED3"],
  "\u6050\u60E7": ["\u5BB3\u6015", "\u6015", "\u6050\u60E7\u75C7", "\u7D27\u5F20", "\u86C7", "\u9AD8\u5904", "\u6253\u9488", "\u9ED1\u6697", "\u8718\u86DB", "\u5BC6\u95ED", "\u6DF1\u6C34"],
  "\u62C5\u5FC3": ["\u7126\u8651", "\u538B\u529B", "\u6000\u5B55", "\u664B\u5347", "\u5065\u5EB7", "\u94B1", "\u52A0\u73ED", "\u5931\u4E1A", "\u8003\u8BD5", "\u5B69\u5B50"],
  // ── 社交 & 人际 & 社交媒体 ──
  "\u793E\u4EA4": ["\u670B\u53CB", "\u540C\u4E8B", "\u90BB\u5C45", "\u76F8\u4EB2", "\u805A\u4F1A", "\u5435\u67B6", "\u5206\u624B", "\u7EA6\u4F1A", "\u5FAE\u4FE1", "\u670B\u53CB\u5708", "\u5C0F\u7EA2\u4E66", "\u793E\u4EA4\u5A92\u4F53", "\u516B\u5366"],
  "\u4EBA\u9645": ["\u670B\u53CB", "\u540C\u4E8B", "\u90BB\u5C45", "\u5435\u67B6", "\u6C9F\u901A", "\u51B2\u7A81"],
  "\u793E\u4EA4\u5A92\u4F53": ["\u6296\u97F3", "\u5FAE\u535A", "\u5FAE\u4FE1", "\u5C0F\u7EA2\u4E66", "B\u7AD9", "\u670B\u53CB\u5708", "\u77ED\u89C6\u9891"],
  // ── 技术 & 编程 ──
  "\u6280\u672F": ["\u670D\u52A1\u5668", "\u6570\u636E\u5E93", "\u90E8\u7F72", "\u524D\u7AEF", "\u540E\u7AEF", "bug", "\u6846\u67B6", "API", "\u8FD0\u7EF4", "AI", "\u5927\u6A21\u578B", "ChatGPT", "\u533A\u5757\u94FE", "\u4E91\u8BA1\u7B97"],
  "\u7F16\u7A0B": ["\u670D\u52A1\u5668", "\u6570\u636E\u5E93", "\u524D\u7AEF", "\u540E\u7AEF", "bug", "\u6846\u67B6", "API", "\u7B97\u6CD5"],
  // ── 娱乐 & 休闲 & 影视 & 音乐 ──
  "\u5A31\u4E50": ["\u7535\u5F71", "\u6E38\u620F", "\u97F3\u4E50", "\u8DD1\u6B65", "\u65C5\u6E38", "\u770B\u4E66", "\u5237\u5267", "\u7EFC\u827A", "\u6296\u97F3", "\u77ED\u89C6\u9891", "\u52A8\u6F2B", "B\u7AD9", "\u76F4\u64AD", "\u7F51\u7EA2"],
  "\u4F11\u95F2": ["\u7535\u5F71", "\u6E38\u620F", "\u97F3\u4E50", "\u65C5\u6E38", "\u770B\u4E66", "\u5237\u5267"],
  "\u5F71\u89C6": ["\u7535\u5F71", "\u7535\u89C6\u5267", "\u7EFC\u827A", "\u7EAA\u5F55\u7247", "\u52A8\u6F2B", "\u756A\u5267", "\u9662\u7EBF"],
  "\u97F3\u4E50": ["\u6F14\u5531\u4F1A", "\u6447\u6EDA", "\u8BF4\u5531", "rap", "\u53E4\u5178", "\u6C11\u8C23", "\u4E50\u5668", "\u5409\u4ED6", "\u94A2\u7434"],
  // ── 生育 ──
  "\u751F\u80B2": ["\u6000\u5B55", "\u9884\u4EA7\u671F", "\u4EA7\u68C0", "\u5F53\u7238\u7238", "\u5F53\u5988\u5988", "\u751F\u5B69\u5B50", "\u6708\u5B50", "\u7238\u7238", "\u5988\u5988"],
  // ── 购物 & 数码 ──
  "\u8D2D\u7269": ["\u4E70\u8F66", "\u4E70\u623F", "\u7F51\u8D2D", "\u4E0B\u5355", "\u9000\u8D27", "\u7279\u65AF\u62C9", "\u8F66", "\u624B\u673A", "\u6DD8\u5B9D", "\u4EAC\u4E1C", "\u62FC\u591A\u591A", "\u53CC\u5341\u4E00", "\u6253\u6298", "\u5FEB\u9012"],
  "\u6570\u7801": ["\u624B\u673A", "\u7535\u8111", "\u5E73\u677F", "\u8033\u673A", "\u76F8\u673A", "\u624B\u8868", "\u5145\u7535\u5B9D"],
  // ── 童年 & 回忆 ──
  "\u7AE5\u5E74": ["\u5C0F\u65F6\u5019", "\u513F\u65F6", "\u56DE\u5FC6", "\u8001\u5BB6", "\u519C\u6751", "\u6821\u56ED", "\u73A9\u4F34", "\u73A9\u5177"],
  "\u56DE\u5FC6": ["\u7AE5\u5E74", "\u5927\u5B66", "\u7B2C\u4E00\u6B21", "\u96BE\u5FD8", "\u4EE5\u524D", "\u5F53\u5E74"],
  // ── 梦想 & 自我提升 ──
  "\u68A6\u60F3": ["\u76EE\u6807", "\u7406\u60F3", "\u613F\u671B", "\u8BA1\u5212", "\u521B\u4E1A", "\u5F00\u5E97", "\u6512\u94B1", "\u672A\u6765"],
  "\u81EA\u6211\u63D0\u5347": ["\u5B66\u4E60", "\u8BFB\u4E66", "\u8003\u8BC1", "\u57F9\u8BAD", "\u8BED\u8A00", "\u6280\u80FD", "\u8BA4\u8BC1", "\u65E5\u8BED", "\u82F1\u8BED", "\u5065\u8EAB"],
  // ── 坏习惯 ──
  "\u574F\u4E60\u60EF": ["\u6212", "\u6539\u6389", "\u514B\u670D", "\u4E0A\u763E", "\u71AC\u591C", "\u62BD\u70DF", "\u559D\u9152", "\u62D6\u5EF6", "\u6212\u70DF", "\u6212\u9152"],
  // ── 宠物护理 ──
  "\u5BA0\u7269\u62A4\u7406": ["\u732B\u7CAE", "\u72D7\u7CAE", "\u5BA0\u7269\u533B\u9662", "\u6D17\u6FA1", "\u905B\u72D7", "\u94F2\u5C4E"],
  // ── 季节 ──
  "\u5B63\u8282": ["\u6625\u5929", "\u590F\u5929", "\u79CB\u5929", "\u51AC\u5929", "\u82B1\u5F00", "\u4E0B\u96EA", "\u843D\u53F6"],
  // ── 个人特质 & 性格 ──
  "\u4E2A\u4EBA\u7279\u8D28": ["\u6027\u683C", "\u6015", "\u559C\u6B22", "\u8BA8\u538C", "\u4E60\u60EF", "\u7279\u957F", "\u7F3A\u70B9"],
  "\u6027\u683C": ["\u6025\u8E81", "\u5185\u5411", "\u5916\u5411", "\u6B63\u4E49", "\u7EA0\u7ED3", "\u72EC\u7ACB", "\u654F\u611F", "\u4E50\u89C2", "\u60B2\u89C2", "\u6267\u7740", "\u968F\u548C", "\u5014\u5F3A"],
  // ── 日常 & 晨练 ──
  "\u65E5\u5E38": ["\u8D77\u5E8A", "\u901A\u52E4", "\u5348\u4F11", "\u4E0B\u73ED", "\u6563\u6B65", "\u6D17\u6FA1", "\u7761\u89C9"],
  "\u6668\u7EC3": ["\u8DD1\u6B65", "\u6668\u8DD1", "\u65E9\u8D77", "\u953B\u70BC", "\u8FD0\u52A8", "\u745C\u4F3D", "\u592A\u6781"],
  // ── 运动 & 锻炼 ──
  "\u8FD0\u52A8\u7231\u597D": ["\u8DD1\u6B65", "\u7BEE\u7403", "\u7FBD\u6BDB\u7403", "\u6E38\u6CF3", "\u5065\u8EAB", "\u745C\u4F3D", "\u9A91\u884C", "\u767B\u5C71", "\u8DB3\u7403", "\u4E52\u4E53\u7403", "\u7F51\u7403", "\u6ED1\u96EA"],
  "\u953B\u70BC": ["\u8DD1\u6B65", "\u5065\u8EAB", "\u6E38\u6CF3", "\u745C\u4F3D", "\u7BEE\u7403", "\u7FBD\u6BDB\u7403", "\u767B\u5C71", "\u9A91\u884C", "\u6563\u6B65"],
  // ── 课外活动 ──
  "\u8BFE\u5916\u6D3B\u52A8": ["\u94A2\u7434", "\u821E\u8E48", "\u753B\u753B", "\u4E66\u6CD5", "\u56F4\u68CB", "\u8DC6\u62F3\u9053", "\u6E38\u6CF3", "\u7BEE\u7403", "\u8DB3\u7403", "\u7F16\u7A0B", "\u82F1\u8BED"],
  // ── 矛盾 & 碎片时间 & 仪式感 ──
  "\u77DB\u76FE": ["\u7EA0\u7ED3", "\u72B9\u8C6B", "\u4E24\u96BE", "\u53D6\u820D", "\u51B2\u7A81", "\u660E\u77E5\u6545\u72AF", "\u5FCD\u4E0D\u4F4F"],
  "\u788E\u7247\u65F6\u95F4": ["\u6296\u97F3", "\u5FAE\u535A", "B\u7AD9", "\u64AD\u5BA2", "\u5C0F\u7EA2\u4E66", "\u5237\u624B\u673A", "\u77ED\u89C6\u9891", "\u670B\u53CB\u5708"],
  "\u4EEA\u5F0F\u611F": ["\u5496\u5561", "\u65E9\u8D77", "\u6563\u6B65", "\u51A5\u60F3", "\u65E5\u8BB0", "\u6574\u7406", "\u6253\u626B", "\u6D17\u6F31", "\u89C6\u9891\u901A\u8BDD"],
  // ── English concept hierarchy（expanded for LOCOMO coverage）──
  "health": ["blood pressure", "weight", "sleep", "insomnia", "exercise", "checkup", "allergy", "headache", "vision", "surgery", "medication", "therapy", "diet", "symptoms", "diagnosis", "prescription", "hospital", "doctor", "mental health", "chronic", "asthma", "inhaler", "cholesterol", "knee", "back pain", "concussion", "heart rate"],
  "health problems": ["allergy", "asthma", "blood pressure", "cholesterol", "knee", "back pain", "concussion", "insomnia", "anxiety", "peanut", "shellfish", "vision", "contacts", "prescription", "inhaler", "surgery"],
  "breathing": ["asthma", "inhaler", "allergy", "lung", "respiratory"],
  "medical": ["doctor", "surgery", "prescription", "hospital", "checkup", "therapy", "chiropractor", "dental", "EpiPen", "inhaler", "cholesterol", "blood type", "diagnosis"],
  "finance": ["mortgage", "salary", "income", "stocks", "savings", "budget", "credit card", "loan", "tax", "investment", "retirement", "insurance", "debt", "expenses", "bonus", "raise", "rent", "bills", "financial", "401k", "Roth IRA", "index funds", "emergency fund", "crypto"],
  "retirement": ["401k", "Roth IRA", "index funds", "pension", "savings", "investment", "retirement fund", "social security"],
  "credit": ["credit score", "credit card", "loan", "debt", "mortgage", "interest rate", "FICO"],
  "income": ["salary", "bonus", "raise", "wages", "paycheck", "compensation", "earnings", "promotion"],
  "career": ["overtime", "colleague", "boss", "project", "promotion", "interview", "resume", "performance", "coworker", "manager", "meeting", "deadline", "startup", "business", "company", "hired", "fired", "layoff", "remote", "office", "mentor", "mentoring", "review"],
  "career progress": ["promoted", "promotion", "raise", "bonus", "review", "performance", "title", "senior", "lead", "manager"],
  "employer": ["company", "work at", "Microsoft", "Google", "startup", "office", "job", "hired", "position"],
  "work setup": ["laptop", "desk", "standing desk", "monitor", "keyboard", "office", "remote", "ThinkPad", "chair", "screen"],
  "office culture": ["coworker", "manager", "standup", "meeting", "Jira", "team", "donuts", "coffee", "lunch"],
  "family": ["parents", "children", "kids", "spouse", "partner", "pets", "cat", "dog", "mother", "father", "sister", "brother", "son", "daughter", "wife", "husband", "wedding", "divorce", "pregnant", "baby", "grandma", "uncle", "niece", "nephew", "cousin", "in-law"],
  "children": ["son", "daughter", "kid", "school", "soccer", "birthday", "grade", "coaching", "homework", "recital", "vet dream", "daycare"],
  "extended family": ["uncle", "aunt", "cousin", "niece", "nephew", "grandma", "grandfather", "in-law", "father-in-law", "mother-in-law"],
  "housing": ["mortgage", "rent", "renovation", "moving", "apartment", "landlord", "house", "condo", "neighborhood", "lease", "furniture", "kitchen", "bedroom", "backyard", "property"],
  "real estate": ["mortgage", "house", "condo", "rent", "buy", "sell", "property", "renovation", "kitchen", "sold", "bedroom", "HOA", "closing"],
  "food": ["takeout", "cooking", "recipe", "breakfast", "lunch", "dinner", "snack", "restaurant", "cuisine", "diet", "vegetarian", "baking", "groceries", "meal prep", "favorite food", "allergic", "pasta", "sourdough", "brew", "hot sauce"],
  "food restrictions": ["allergy", "allergic", "shellfish", "peanut", "vegetarian", "vegan", "lactose", "gluten", "intolerance", "EpiPen", "celiac"],
  "beverages": ["coffee", "tea", "beer", "wine", "oat milk", "brew", "Chemex", "latte", "espresso", "cocktail", "juice", "smoothie"],
  "transport": ["driving", "subway", "flight", "business trip", "train", "taxi", "traffic", "commute", "bus", "car", "parking", "road trip", "uber", "bicycle", "walk"],
  "emotion": ["anxiety", "stress", "depression", "insomnia", "happiness", "frustration", "loneliness", "burnout", "excited", "worried", "angry", "sad", "grateful", "confident", "overwhelmed", "jealous", "cry", "nightmares", "panic", "therapy"],
  "weakness": ["overthink", "procrastinate", "road rage", "impatient", "anxious", "stubborn", "perfectionist", "indecisive"],
  "fear": ["afraid", "phobia", "heights", "spiders", "public speaking", "dark", "claustrophobic", "needles", "snakes", "deep water"],
  "social": ["friend", "colleague", "neighbor", "dating", "party", "argument", "breakup", "relationship", "wedding", "reunion", "group", "community", "club", "gathering", "social media", "poker", "game night", "book club", "BBQ"],
  "gatherings": ["poker", "game night", "book club", "BBQ", "party", "reunion", "dinner party", "brunch", "meetup", "potluck"],
  "tech": ["server", "database", "deploy", "frontend", "backend", "bug", "framework", "api", "devops", "cloud", "machine learning", "software", "hardware", "app", "website", "coding", "React", "TypeScript", "Python", "JavaScript"],
  "entertainment": ["movie", "game", "music", "running", "travel", "reading", "streaming", "concert", "show", "podcast", "book", "series", "hobby", "sport", "painting", "photography"],
  "education": ["school", "college", "university", "degree", "professor", "thesis", "exam", "grade", "scholarship", "class", "major", "student", "homework", "graduation", "campus", "bootcamp", "MBA", "hackathon", "TA"],
  "academic": ["thesis", "hackathon", "scholarship", "TA", "dean", "GPA", "honors", "research", "published", "peer review"],
  "personality": ["introvert", "extrovert", "shy", "confident", "patient", "impatient", "organized", "messy", "punctual", "procrastinate", "competitive", "easygoing", "stubborn", "generous", "ambitious", "left-handed", "morning person"],
  "travel": ["vacation", "trip", "flight", "hotel", "destination", "passport", "sightseeing", "backpacking", "beach", "mountain", "abroad", "tourist", "itinerary", "luggage", "adventure", "Tokyo", "Bali", "Italy", "London"],
  "travel documents": ["passport", "visa", "ID", "driver license", "TSA", "boarding pass", "vaccination card"],
  "hobby": ["running", "hiking", "yoga", "painting", "gardening", "cooking", "photography", "chess", "reading", "gaming", "cycling", "fishing", "woodworking", "singing", "dancing", "brewing", "vinyl", "guitar", "puzzle", "sourdough"],
  "crafts": ["woodworking", "painting", "photography", "knitting", "pottery", "brewing", "sourdough", "vinyl", "puzzle", "scrapbook"],
  "exercise": ["running", "marathon", "gym", "basketball", "yoga", "cycling", "hiking", "swimming", "5K", "half marathon", "CrossFit", "stretching", "weights", "cardio", "heart rate"],
  "running": ["marathon", "half marathon", "5K", "10K", "pace", "time", "PR", "race", "training", "treadmill"],
  "routine": ["morning", "commute", "lunch break", "afternoon", "evening", "bedtime", "wake up", "coffee", "workout", "dinner", "walk", "shower", "sleep", "alarm", "schedule"],
  "morning routine": ["wake up", "alarm", "coffee", "meditate", "gym", "run", "shower", "breakfast", "commute", "journal"],
  "evening routine": ["dinner", "walk", "shower", "journal", "read", "bedtime", "white noise", "melatonin", "TV", "stretch"],
  "self improvement": ["learning", "Spanish", "guitar", "mentor", "mentoring", "reading", "meditation", "fasting", "journal", "screen time", "therapy", "bootcamp", "MBA"],
  "life event": ["wedding", "graduation", "promotion", "moving", "birth", "death", "accident", "surgery", "retirement", "engagement", "breakup", "new job", "bought house", "lost job"],
  "addiction": ["quit", "drinking", "smoking", "screen time", "gambling", "caffeine", "social media", "gaming"],
  "appearance": ["tattoo", "height", "weight", "gray hair", "birthmark", "glasses", "contacts", "left-handed", "shoe size", "haircut"],
  "body measurements": ["height", "weight", "shoe size", "waist", "BMI", "blood type", "vision", "prescription"],
  "outdoor": ["garden", "backyard", "grill", "fire pit", "patio", "deck", "lawn", "hiking", "camping", "picnic", "BBQ"],
  "green energy": ["Tesla", "solar panels", "EV", "electric car", "hybrid", "recycling", "compost", "carbon footprint"],
  "sleep": ["insomnia", "white noise", "melatonin", "nightmare", "snore", "nap", "bedtime", "alarm", "sleep schedule", "mattress"],
  // ── T2 补充：具体→抽象上位概念（填补 vocabulary gap）──
  "instrument": ["guitar", "piano", "violin", "drums", "ukulele", "bass", "flute", "saxophone", "cello", "trumpet", "harmonica", "keyboard", "banjo", "harp", "clarinet", "trombone", "accordion", "oboe"],
  "pet": ["dog", "cat", "fish", "hamster", "rabbit", "bird", "turtle", "parrot", "guinea pig", "snake", "lizard", "ferret", "goldfish", "kitten", "puppy"],
  "vehicle": ["car", "truck", "motorcycle", "bicycle", "scooter", "van", "suv", "sedan", "convertible", "pickup", "minivan", "jeep", "tesla"],
  "sport": ["basketball", "football", "soccer", "baseball", "tennis", "golf", "swimming", "running", "hiking", "yoga", "boxing", "volleyball", "cricket", "surfing", "skiing", "badminton", "wrestling"],
  "language": ["english", "spanish", "french", "german", "chinese", "japanese", "korean", "portuguese", "italian", "arabic", "hindi", "russian", "dutch", "swedish", "polish"],
  "cuisine type": ["italian", "mexican", "chinese", "japanese", "thai", "indian", "french", "korean", "mediterranean", "american", "vietnamese", "greek", "turkish", "brazilian"],
  "color": ["red", "blue", "green", "yellow", "purple", "orange", "pink", "black", "white", "brown", "gray", "gold", "silver", "turquoise", "maroon"],
  "furniture": ["table", "chair", "sofa", "bed", "desk", "shelf", "cabinet", "dresser", "couch", "bookcase", "nightstand", "recliner", "ottoman"],
  "clothing": ["shirt", "pants", "dress", "jacket", "coat", "sweater", "jeans", "skirt", "shoes", "boots", "hat", "scarf", "gloves", "socks", "hoodie"],
  "fruit": ["apple", "banana", "orange", "grape", "strawberry", "mango", "pineapple", "watermelon", "peach", "blueberry", "cherry", "kiwi", "pear", "plum"],
  "illness": ["cold", "flu", "fever", "headache", "stomachache", "allergy", "asthma", "diabetes", "arthritis", "migraine", "infection", "pneumonia", "bronchitis", "anemia"],
  "weather condition": ["rain", "snow", "sunshine", "wind", "storm", "fog", "hail", "thunder", "lightning", "drizzle", "hurricane", "tornado", "heat wave", "frost"],
  "room": ["bedroom", "kitchen", "bathroom", "living room", "dining room", "garage", "attic", "basement", "office", "hallway", "closet", "nursery", "den"],
  "tree": ["oak", "maple", "pine", "birch", "willow", "cedar", "palm", "cherry blossom", "redwood", "elm", "cypress", "spruce"],
  "flower": ["rose", "tulip", "daisy", "sunflower", "lily", "orchid", "lavender", "chrysanthemum", "peony", "violet", "jasmine", "hibiscus"],
  "board game": ["chess", "checkers", "monopoly", "scrabble", "risk", "settlers", "catan", "ticket to ride", "clue", "trivial pursuit"],
  "dance": ["ballet", "salsa", "tango", "waltz", "hip hop", "contemporary", "jazz", "swing", "breakdance", "tap", "ballroom", "flamenco"],
  "art form": ["painting", "sculpture", "photography", "pottery", "drawing", "calligraphy", "ceramics", "mosaic", "watercolor", "oil painting", "sketching"],
  "gemstone": ["diamond", "ruby", "emerald", "sapphire", "amethyst", "topaz", "opal", "jade", "pearl", "turquoise", "garnet"],
  // ── LOCOMO 失败模式补充：抽象查询词→具体活动/物品 ──
  "activity": ["hiking", "painting", "pottery", "camping", "reading", "cooking", "gardening", "dancing", "swimming", "running", "yoga", "fishing", "knitting", "singing", "playing", "volunteering", "traveling", "shopping"],
  "destress": ["paint", "read", "hike", "yoga", "meditate", "garden", "cook", "walk", "swim", "exercise", "music", "sleep", "bath", "journal"],
  "relax": ["paint", "read", "hike", "yoga", "meditate", "garden", "cook", "walk", "swim", "exercise", "music", "sleep", "bath", "nap", "unwind"],
  "partake": ["participate", "join", "attend", "do", "engage", "take part", "involved", "active"],
  "identity": ["transgender", "gender", "orientation", "sexuality", "queer", "nonbinary", "pronouns", "transition", "coming out", "LGBTQ"],
  "book": ["novel", "story", "read", "reading", "author", "title", "fiction", "nonfiction", "memoir", "biography", "literature"],
  "camp": ["camping", "tent", "campfire", "outdoor", "campsite", "campground", "trail", "backpack", "wilderness", "nature trip"],
  "event": ["conference", "parade", "rally", "meeting", "workshop", "seminar", "festival", "gathering", "celebration", "ceremony", "fundraiser", "race", "charity", "support group"],
  "participate": ["attend", "join", "volunteer", "contribute", "engage", "take part", "involved", "active", "signed up", "registered"]
};
const _conceptReverseIndex = /* @__PURE__ */ new Map();
function buildConceptReverseIndex() {
  _conceptReverseIndex.clear();
  for (const [parent, children] of Object.entries(CONCEPT_HIERARCHY)) {
    const pl = parent.toLowerCase();
    for (const child of children) {
      const cl = child.toLowerCase();
      if (!_conceptReverseIndex.has(cl)) _conceptReverseIndex.set(cl, []);
      const arr = _conceptReverseIndex.get(cl);
      if (!arr.includes(pl)) arr.push(pl);
    }
  }
}
buildConceptReverseIndex();
function getSemanticDimensions(word) {
  const dims = [];
  const wl = word.toLowerCase();
  const lang = detectLanguage(word);
  const seedKeys = _reverseIndex.get(lang)?.get(wl) || [];
  for (const k of seedKeys) dims.push("s:" + k);
  const conceptKeys = _conceptReverseIndex.get(wl) || [];
  for (const k of conceptKeys) dims.push("c:" + k);
  return dims;
}
let _knownWordCache = /* @__PURE__ */ new Set();
let _knownWordBuilt = false;
function isKnownWord(word) {
  if (!_knownWordBuilt) {
    for (const k of Object.keys(_defaultSynonyms)) _knownWordCache.add(k);
    for (const syns of Object.values(_defaultSynonyms)) {
      for (const s of syns) _knownWordCache.add(s);
    }
    for (const k of Object.keys(CONCEPT_HIERARCHY)) _knownWordCache.add(k);
    for (const children of Object.values(CONCEPT_HIERARCHY)) {
      for (const c of children) _knownWordCache.add(c);
    }
    _knownWordBuilt = true;
  }
  return _knownWordCache.has(word);
}
function resetLearnedData() {
  _activationDamping.clear();
  _maxHopByPattern.clear();
  _prevMessageWords = [];
  _temporalNet.directed = {};
}
function learnAssociation(content, emotionIntensity = 0, weight = 1, fullPair = false) {
  const lang = detectLanguage(content);
  _currentLang = lang;
  const emotionMultiplier = emotionIntensity >= 0.7 ? 3 : emotionIntensity >= 0.5 ? 2 : 1;
  const words = filterStopWords(tokenize(content));
  const unique = [...new Set(words)].filter((w) => !isJunkToken(w));
  if (unique.length < 2) return;
  if (emotionMultiplier > 1) {
    console.log(`[AAM] emotion-weighted learning: intensity=${emotionIntensity.toFixed(2)} multiplier=x${emotionMultiplier}`);
  }
  network().totalDocs++;
  for (const w of unique) {
    network().df[w] = (network().df[w] || 0) + 1;
  }
  const inc = emotionMultiplier * weight;
  const _addPair = (w1, w2) => {
    if (!network().cooccur[w1]) network().cooccur[w1] = {};
    network().cooccur[w1][w2] = Math.min(50, (network().cooccur[w1][w2] || 0) + inc);
    if (!network().cooccur[w2]) network().cooccur[w2] = {};
    network().cooccur[w2][w1] = Math.min(50, (network().cooccur[w2][w1] || 0) + inc);
  };
  if (fullPair) {
    for (let i = 0; i < unique.length; i++)
      for (let j = i + 1; j < unique.length; j++)
        _addPair(unique[i], unique[j]);
  } else {
    const WINDOW = 5;
    const seen = /* @__PURE__ */ new Set();
    for (let i = 0; i < words.length; i++) {
      if (isJunkToken(words[i])) continue;
      for (let j = i + 1; j < Math.min(i + WINDOW, words.length); j++) {
        if (isJunkToken(words[j])) continue;
        if (words[i] === words[j]) continue;
        const pair = words[i] < words[j] ? `${words[i]}\0${words[j]}` : `${words[j]}\0${words[i]}`;
        if (seen.has(pair)) continue;
        seen.add(pair);
        _addPair(words[i], words[j]);
      }
    }
  }
  if (!process.env.CC_SOUL_BENCHMARK && network().totalDocs % 10 === 0) {
    debouncedSave(cooccurPath(lang), network());
  }
  if (!process.env.CC_SOUL_BENCHMARK && network().totalDocs >= 30 && network().totalDocs % 50 === 0) {
    graduateStrongAssociations();
  }
}
function graduateStrongAssociations() {
  const lang = _currentLang;
  const syns = getSynonyms(lang);
  let graduated = 0;
  for (const [w1, related] of Object.entries(network().cooccur)) {
    if (w1.length < 2) continue;
    if (isJunkToken(w1)) continue;
    for (const [w2, count] of Object.entries(related)) {
      if (w2.length < 2 || count < 5) continue;
      if (isJunkToken(w2)) continue;
      const p = pmi(w1, w2);
      if (p > 3) {
        const totalDocs = Math.max(1, network().totalDocs);
        if ((network().df[w1] || 0) / totalDocs > 0.3 || (network().df[w2] || 0) / totalDocs > 0.3) continue;
        const fanOut1 = Object.keys(network().cooccur[w1] || {}).length;
        const fanOut2 = Object.keys(network().cooccur[w2] || {}).length;
        if (fanOut1 > 50 && fanOut2 > 50) continue;
        const existing = syns[w1];
        if (existing && existing.includes(w2)) continue;
        if (!syns[w1]) syns[w1] = [];
        syns[w1].push(w2);
        graduated++;
      }
    }
  }
  if (graduated > 0) {
    debouncedSave(synonymsPath(lang), syns);
    console.log(`[cc-soul][aam] graduated ${graduated} strong associations to synonym table [${lang}] (total groups: ${Object.keys(syns).length})`);
  }
}
function pmi(w1, w2) {
  const N = Math.max(1, network().totalDocs);
  const cooccurCount = network().cooccur[w1]?.[w2] || 0;
  if (cooccurCount === 0) return 0;
  const df1 = network().df[w1] || 1;
  const df2 = network().df[w2] || 1;
  const pmiVal = Math.log2(cooccurCount * N / (df1 * df2));
  return Math.max(0, pmiVal);
}
const _ufParent = /* @__PURE__ */ new Map();
const _ufRank = /* @__PURE__ */ new Map();
function ufFind(x) {
  if (!_ufParent.has(x)) {
    _ufParent.set(x, x);
    _ufRank.set(x, 0);
  }
  let root = x;
  while (_ufParent.get(root) !== root) root = _ufParent.get(root);
  let curr = x;
  while (curr !== root) {
    const next = _ufParent.get(curr);
    _ufParent.set(curr, root);
    curr = next;
  }
  return root;
}
function ufUnion(a, b) {
  const ra = ufFind(a), rb = ufFind(b);
  if (ra === rb) return;
  const rankA = _ufRank.get(ra) || 0;
  const rankB = _ufRank.get(rb) || 0;
  if (rankA < rankB) _ufParent.set(ra, rb);
  else if (rankA > rankB) _ufParent.set(rb, ra);
  else {
    _ufParent.set(rb, ra);
    _ufRank.set(ra, rankA + 1);
  }
}
let _pmiClusters = /* @__PURE__ */ new Map();
let _pmiClusterIndex = /* @__PURE__ */ new Map();
function buildPMIClusters(minPMI = 3) {
  _ufParent.clear();
  _ufRank.clear();
  const net = network();
  for (const [w1, related] of Object.entries(net.cooccur)) {
    if (w1.length < 2) continue;
    if (isJunkToken(w1)) continue;
    for (const [w2, count] of Object.entries(related)) {
      if (w2.length < 2 || count < 2) continue;
      if (isJunkToken(w2)) continue;
      const p = pmi(w1, w2);
      if (p < minPMI) continue;
      ufUnion(w1, w2);
    }
  }
  const clusters = /* @__PURE__ */ new Map();
  for (const word of _ufParent.keys()) {
    const root = ufFind(word);
    if (!clusters.has(root)) clusters.set(root, []);
    clusters.get(root).push(word);
  }
  const result = /* @__PURE__ */ new Map();
  const index = /* @__PURE__ */ new Map();
  for (const [root, members] of clusters) {
    if (members.length >= 2 && members.length <= 20) {
      result.set(root, members);
      for (const m of members) index.set(m, root);
    }
  }
  _pmiClusters = result;
  _pmiClusterIndex = index;
  if (result.size > 0) {
    console.log(`[cc-soul][aam] PMI clusters: ${result.size} groups, ${index.size} words`);
  }
  return result;
}
function getPMIClusterPeers(word) {
  const root = _pmiClusterIndex.get(word);
  if (!root) return [];
  return (_pmiClusters.get(root) || []).filter((w) => w !== word);
}
function getCooccurrence(wordA, wordB) {
  return network().cooccur[wordA]?.[wordB] ?? network().cooccur[wordB]?.[wordA] ?? 0;
}
function getAAMNeighbors(word, topK = 5) {
  const cooc = network().cooccur[word];
  if (!cooc) return [];
  const results = [];
  for (const [other, _count] of Object.entries(cooc)) {
    const p = pmi(word, other);
    if (p > 0.5) {
      const fanOut = Object.keys(network().cooccur[other] || {}).length;
      results.push({ word: other, pmiScore: p, fanOut });
    }
  }
  results.sort((a, b) => b.pmiScore - a.pmiScore);
  return results.slice(0, topK);
}
function expandQuery(queryWords, maxExpansion = 10) {
  const lang = detectLanguage(queryWords.join(" "));
  _currentLang = lang;
  const langSynonyms = getSynonyms(lang);
  const expanded = /* @__PURE__ */ new Map();
  for (const w of queryWords) expanded.set(w, 1);
  for (const w of queryWords) {
    const cooc = network().cooccur[w];
    if (!cooc) continue;
    const candidates = [];
    for (const [other, _count] of Object.entries(cooc)) {
      if (expanded.has(other)) continue;
      if (other.length === 2 && /^[\u4e00-\u9fff]+$/.test(other)) {
        const isKnown = !!langSynonyms[other] || !!_reverseIndex.get(lang)?.has(other);
        if (!isKnown && (network().df[other] || 0) < 1) continue;
      }
      const p = pmi(w, other);
      const _totalDocs = network().totalDocs || 100;
      const _pmiThr = _totalDocs < 100 ? 0.7 : 1;
      const _dfThr = _totalDocs < 100 ? 1 : 2;
      if (p > _pmiThr && (network().df[other] || 0) >= _dfThr) candidates.push({ word: other, pmiScore: p });
    }
    candidates.sort((a, b) => b.pmiScore - a.pmiScore);
    for (const c of candidates.slice(0, 3)) {
      const baseWeight = Math.min(0.8, c.pmiScore / 5);
      const damping = getDamping(c.word);
      const weight = baseWeight * damping;
      expanded.set(c.word, Math.max(expanded.get(c.word) || 0, weight));
    }
  }
  for (const w of queryWords) {
    const directSyns = langSynonyms[w];
    if (directSyns) {
      for (const syn of directSyns) {
        if (syn.length >= 2) {
          const existing = expanded.get(syn) || 0;
          if (existing < 0.9) expanded.set(syn, 0.9);
        }
      }
    }
    const _revIdx = _reverseIndex.get(lang);
    const _matchedKeys = _revIdx?.get(w);
    if (_matchedKeys) {
      for (const key of _matchedKeys) {
        if (key.length >= 2) {
          const existing = expanded.get(key) || 0;
          if (existing < 0.9) expanded.set(key, 0.9);
        }
        const peers = langSynonyms[key];
        if (peers) {
          for (const peer of peers) {
            if (peer !== w && peer.length >= 2) {
              const existing = expanded.get(peer) || 0;
              if (existing < 0.7) expanded.set(peer, 0.7);
            }
          }
        }
      }
    }
  }
  for (const w of queryWords) {
    const peers = getPMIClusterPeers(w);
    for (const peer of peers) {
      if (peer.length < 2) continue;
      const existing = expanded.get(peer) || 0;
      if (existing < 0.85) expanded.set(peer, 0.85);
    }
  }
  const isConceptCJK = (s) => /[\u4e00-\u9fff]/.test(s);
  const conceptLangMatch = lang === "zh" ? isConceptCJK : (s) => !isConceptCJK(s);
  try {
    const graph = require("./graph.ts");
    if (graph.graphState?.relations) {
      const rels = graph.graphState.relations.filter((r) => !r.invalid_at);
      const groups = /* @__PURE__ */ new Map();
      for (const r of rels) {
        const type = r.type || "related";
        if (!groups.has(type)) groups.set(type, /* @__PURE__ */ new Set());
        if (r.source?.length >= 2) groups.get(type).add(r.source);
        if (r.target?.length >= 2) groups.get(type).add(r.target);
      }
      for (const [type, members] of groups) {
        if (members.size >= 2 && !CONCEPT_HIERARCHY[type]) {
          CONCEPT_HIERARCHY[type] = [...members].slice(0, 15);
        }
      }
    }
  } catch {
  }
  const _conceptReverse = /* @__PURE__ */ new Map();
  for (const [parent, children] of Object.entries(CONCEPT_HIERARCHY)) {
    if (!conceptLangMatch(parent)) continue;
    for (const child of children) {
      if (!_conceptReverse.has(child)) _conceptReverse.set(child, []);
      _conceptReverse.get(child).push(parent);
    }
  }
  for (const w of queryWords) {
    let children = CONCEPT_HIERARCHY[w];
    if (!children && w.length >= 4 && /^[a-z]+$/i.test(w)) {
      const stems = [
        w.replace(/ies$/i, "y"),
        w.replace(/ves$/i, "f"),
        w.replace(/ses$/i, "se"),
        w.replace(/s$/i, ""),
        w.replace(/ing$/i, ""),
        w.replace(/ed$/i, "")
      ];
      for (const stem of stems) {
        if (stem !== w && CONCEPT_HIERARCHY[stem]) {
          children = CONCEPT_HIERARCHY[stem];
          break;
        }
      }
    }
    if (children) {
      for (const c of children) {
        if (c.length >= 2) {
          const existing = expanded.get(c) || 0;
          if (existing < 0.85) expanded.set(c, 0.85);
        }
      }
    }
    let parents = _conceptReverse.get(w);
    if (!parents && w.length >= 4 && /^[a-z]+$/i.test(w)) {
      const stems = [w.replace(/ies$/i, "y"), w.replace(/s$/i, ""), w.replace(/ing$/i, ""), w.replace(/ed$/i, "")];
      for (const stem of stems) {
        if (stem !== w && _conceptReverse.has(stem)) {
          parents = _conceptReverse.get(stem);
          break;
        }
      }
    }
    if (parents) {
      for (const p of parents) {
        if (!expanded.has(p)) expanded.set(p, 0.3);
        const siblings = CONCEPT_HIERARCHY[p];
        if (siblings) {
          for (const s of siblings) {
            if (s !== w && s.length >= 2 && !expanded.has(s)) expanded.set(s, 0.3);
          }
        }
      }
    }
  }
  const secondPassWords = [...expanded.entries()].filter(([w, wt]) => wt >= 0.9 && !queryWords.includes(w) && w.length >= 2).map(([w]) => w);
  for (const w of secondPassWords.slice(0, 5)) {
    const children2 = CONCEPT_HIERARCHY[w];
    if (children2) {
      for (const c of children2) {
        if (c.length >= 2) {
          const existing = expanded.get(c) || 0;
          if (existing < 0.5) expanded.set(c, 0.5);
        }
      }
    }
  }
  for (const [word] of [...expanded.entries()]) {
    if (queryWords.includes(word)) continue;
    if (isJunkToken(word)) expanded.delete(word);
  }
  for (const w of queryWords) {
    if (!/^[\u4e00-\u9fff]{2,}$/.test(w)) continue;
    const chars = [...w];
    for (const [key, syns] of Object.entries(langSynonyms)) {
      if (expanded.has(key)) continue;
      const keyChars = [...key];
      const shared = chars.filter((c) => keyChars.includes(c));
      if (shared.length > 0 && key.length >= 2) {
        const sharedWeight = Math.min(0.7, 0.4 * shared.length);
        if ((expanded.get(key) || 0) < sharedWeight) {
          expanded.set(key, sharedWeight);
        }
      }
    }
  }
  recoverDamping();
  for (const [word] of [...expanded.entries()]) {
    if (queryWords.includes(word)) continue;
    if (word.length === 2 && /^[\u4e00-\u9fff]{2}$/.test(word) && !isKnownWord(word)) {
      expanded.delete(word);
    }
  }
  return [...expanded.entries()].map(([word, weight]) => ({ word, weight })).sort((a, b) => b.weight - a.weight).slice(0, queryWords.length + maxExpansion);
}
const KEY_WEIGHTS_PATH = resolve(DATA_DIR, "aam_key_weights.json");
let keyWeights = loadJson(KEY_WEIGHTS_PATH, {
  weights: {
    lexical: 1,
    temporal: 1,
    emotional: 1,
    entity: 1,
    behavioral: 1,
    factual: 1,
    causal: 1,
    sequence: 1,
    cognitive: 1
  },
  feedbackCount: 0,
  lastUpdated: Date.now()
});
function saveKeyWeights() {
  debouncedSave(KEY_WEIGHTS_PATH, keyWeights);
}
function hebbianUpdate(keyScores, wasUseful) {
  const now = Date.now();
  const hoursSinceLastUpdate = (now - (keyWeights.lastUpdated || now)) / 36e5;
  if (hoursSinceLastUpdate > 1) {
    const decayFactor = Math.exp(-hoursSinceLastUpdate / 168);
    for (const key of Object.keys(keyWeights.weights)) {
      keyWeights.weights[key] = 1 + (keyWeights.weights[key] - 1) * decayFactor;
    }
  }
  keyWeights.lastUpdated = now;
  const lr = 0.05 / (1 + keyWeights.feedbackCount * 1e-3);
  keyWeights.feedbackCount++;
  for (const [keyType, score] of Object.entries(keyScores)) {
    if (score < 0.2) continue;
    const current = keyWeights.weights[keyType] || 1;
    if (wasUseful) {
      keyWeights.weights[keyType] = Math.min(3, current + lr * score);
    } else {
      const penalty = lr * score * (score > 0.5 ? 1.5 : 0.5);
      keyWeights.weights[keyType] = Math.max(0.3, current - penalty);
    }
  }
  saveKeyWeights();
  antiHebbianDecay();
}
function antiHebbianDecay() {
  if (keyWeights.feedbackCount % 100 !== 0 || keyWeights.feedbackCount === 0) return;
  let pruned = 0;
  for (const [w1, related] of Object.entries(network().cooccur)) {
    for (const [w2, count] of Object.entries(related)) {
      if (count < 3) continue;
      const pmiVal = pmi(w1, w2);
      if (pmiVal < 0.5 && count > 5) {
        const decayRate = count > 20 ? 0.9 : count > 10 ? 0.8 : 0.6;
        related[w2] = Math.max(1, Math.floor(count * decayRate));
        pruned++;
      }
    }
  }
  if (pruned > 0) {
    debouncedSave(cooccurPath(_currentLang), network());
    console.log(`[cc-soul][aam] anti-Hebbian [${_currentLang}]: pruned ${pruned} noise associations`);
  }
}
function decayCooccurrence() {
  for (const [lang, net] of networks) {
    _decayNetwork(lang, net);
  }
  decayTemporalLinks();
}
function _decayNetwork(lang, net) {
  _currentLang = lang;
  let decayed = 0, pruned = 0;
  for (const [w1, related] of Object.entries(net.cooccur)) {
    for (const [w2, count] of Object.entries(related)) {
      const baseDRate = count > 10 ? 0.995 : 0.98;
      let momentum = 0;
      try {
        const { getMomentumBoost } = require("./activation-field.ts");
        momentum = (getMomentumBoost(w1) || 0) + (getMomentumBoost(w2) || 0);
      } catch {
      }
      let factor = baseDRate * (1 + Math.min(0.1, momentum * 0.05));
      const newCount = count * Math.min(factor, 1);
      if (newCount < 0.5) {
        delete related[w2];
        pruned++;
      } else {
        related[w2] = newCount;
        decayed++;
      }
    }
    if (Object.keys(related).length === 0) {
      delete net.cooccur[w1];
    }
  }
  if (pruned > 0) {
    console.log(`[cc-soul][aam] decay [${lang}]: ${decayed} edges decayed, ${pruned} pruned`);
    debouncedSave(cooccurPath(lang), net);
  }
}
function getAAMStats() {
  const langStats = {};
  for (const [lang, net] of networks) {
    const syns = _synonymsByLang.get(lang);
    langStats[lang] = {
      vocabularySize: Object.keys(net.df).length,
      totalDocs: net.totalDocs,
      associationPairs: Object.values(net.cooccur).reduce((s, v) => s + Object.keys(v).length, 0),
      synonyms: syns ? Object.keys(syns).length : 0
    };
  }
  return {
    languages: Object.keys(langStats),
    perLanguage: langStats,
    vocabularySize: Object.keys(network().df).length,
    totalDocs: network().totalDocs,
    associationPairs: Object.values(network().cooccur).reduce((s, v) => s + Object.keys(v).length, 0),
    coldStartSynonyms: Object.keys(getSynonyms(_currentLang)).length,
    keyWeights: { ...keyWeights.weights },
    feedbackCount: keyWeights.feedbackCount
  };
}
const _activationDamping = /* @__PURE__ */ new Map();
function getDamping(word) {
  return _activationDamping.get(word) ?? 1;
}
function onTopicSwitch(oldTopicWords, newTopicWords) {
  for (const w of oldTopicWords) {
    _activationDamping.set(w, 0.3);
  }
  for (const w of newTopicWords) {
    _activationDamping.set(w, 1);
  }
  if (oldTopicWords.length > 0) {
    console.log(`[cc-soul][aam] topic switch: damped ${oldTopicWords.length} old words, activated ${newTopicWords.length} new words`);
  }
}
function recoverDamping() {
  for (const [word, factor] of _activationDamping) {
    const recovered = factor * 0.9 + 1 * 0.1;
    if (recovered > 0.95) {
      _activationDamping.delete(word);
    } else {
      _activationDamping.set(word, recovered);
    }
  }
}
const _maxHopByPattern = /* @__PURE__ */ new Map();
function reinforceTrace(trace, queryWords) {
  if (!queryWords || queryWords.length === 0 || !trace.memory?.content) return;
  const lang = detectLanguage(trace.memory.content);
  _currentLang = lang;
  const memWords = filterStopWords(tokenize(trace.memory.content)).filter((w) => !isJunkToken(w) && w.length >= 2).slice(0, 10);
  if (memWords.length === 0) return;
  let reinforced = 0;
  for (const qw of queryWords) {
    if (qw.length < 2 || isJunkToken(qw)) continue;
    for (const mw of memWords) {
      if (qw === mw) continue;
      if (!network().cooccur[qw]) network().cooccur[qw] = {};
      network().cooccur[qw][mw] = Math.min(50, (network().cooccur[qw][mw] || 0) + 1.5);
      if (!network().cooccur[mw]) network().cooccur[mw] = {};
      network().cooccur[mw][qw] = Math.min(50, (network().cooccur[mw][qw] || 0) + 1.5);
      reinforced++;
    }
  }
  if (reinforced > 0) console.log(`[cc-soul][aam] reinforced ${reinforced} pairs from ${queryWords.length} qw \xD7 ${memWords.length} mw`);
}
function suppressExpansion(queryPattern, missedVia) {
  if (_maxHopByPattern.size > 1e3) _maxHopByPattern.clear();
  const currentMax = _maxHopByPattern.get(queryPattern) ?? 2;
  if (missedVia === "aam_hop2" && currentMax > 1) {
    _maxHopByPattern.set(queryPattern, 1);
    console.log(`[cc-soul][aam] negative feedback: ${queryPattern} hop2\u2192hop1`);
  } else if (missedVia === "aam_hop1" && currentMax > 0) {
    _maxHopByPattern.set(queryPattern, 0);
    console.log(`[cc-soul][aam] negative feedback: ${queryPattern} hop1\u2192no expansion`);
  }
}
function restoreExpansion(queryPattern) {
  const currentMax = _maxHopByPattern.get(queryPattern);
  if (currentMax !== void 0 && currentMax < 2) {
    _maxHopByPattern.set(queryPattern, Math.min(2, currentMax + 1));
    console.log(`[cc-soul][aam] expansion restored: ${queryPattern} \u2192 hop${currentMax + 1}`);
  }
}
const _emotionWordCandidates = /* @__PURE__ */ new Map();
function learnEmotionWord(word, moodDelta) {
  if (Math.abs(moodDelta) < 0.15) return;
  if (word.length < 2) return;
  if (_emotionWordCandidates.size > 1e4) {
    const sorted = [..._emotionWordCandidates.entries()].sort((a, b) => a[1].posCount + a[1].negCount - (b[1].posCount + b[1].negCount));
    const toDelete = Math.floor(sorted.length / 2);
    for (let i = 0; i < toDelete; i++) _emotionWordCandidates.delete(sorted[i][0]);
  }
  let entry = _emotionWordCandidates.get(word);
  if (!entry) {
    entry = { posCount: 0, negCount: 0 };
    _emotionWordCandidates.set(word, entry);
  }
  if (moodDelta > 0.15) entry.posCount++;
  else if (moodDelta < -0.15) entry.negCount++;
}
function getLearnedEmotionWords() {
  const positive = [];
  const negative = [];
  for (const [word, counts] of _emotionWordCandidates) {
    const total = counts.posCount + counts.negCount;
    if (total < 3) continue;
    if (counts.posCount > counts.negCount * 2) positive.push(word);
    if (counts.negCount > counts.posCount * 2) negative.push(word);
  }
  return { positive, negative };
}
function bootstrapFromMemories() {
  if (network().totalDocs > 100) return;
  try {
    const { memoryState, ensureMemoriesLoaded } = require("./memory.ts");
    ensureMemoriesLoaded();
    const LEARN_SCOPES = /* @__PURE__ */ new Set(["fact", "preference", "event", "correction", "opinion", "episode"]);
    const candidates = memoryState.memories.filter((m) => m.content && LEARN_SCOPES.has(m.scope)).slice(-200);
    for (const m of candidates) {
      learnAssociation(m.content);
    }
    if (candidates.length > 0) console.log(`[cc-soul][aam] bootstrapped from ${candidates.length} memories`);
    try {
      const { getDistillStats, getMentalModel } = require("./distill.ts");
      const stats = getDistillStats();
      if (stats?.topicNodeCount > 0) {
        const model = getMentalModel();
        if (model?.traits) {
          for (const trait of Object.values(model.traits)) {
            if (trait?.examples?.length >= 2) {
              learnAssociation(trait.examples.join(" "));
            }
          }
        }
        console.log(`[cc-soul][aam] learned from ${stats.topicNodeCount} topic nodes`);
      }
    } catch {
    }
  } catch {
  }
}
setTimeout(() => bootstrapFromMemories(), 3e3);
async function generateSynonymSeed(lang) {
  const path = synonymsPath(lang);
  if (existsSync(path)) {
    const existing = loadJson(path, {});
    if (Object.keys(existing).length > 20) return;
  }
  console.log(`[AAM] New language "${lang}" detected. Generating synonym seed via LLM...`);
  try {
    const { spawnCLI } = await import("./cli.ts");
    const prompt = `Generate exactly 200 synonym groups for the "${lang}" language. Each group is a common word and its synonyms/related words that a personal AI assistant would need.

Cover these categories: emotions (30 groups), health (20), work/career (20), family (20), food (15), housing (15), finance (15), transport (10), education (10), hobbies (15), tech (15), time expressions (10), general adjectives (15).

Output as JSON object. Keys are the main word, values are arrays of synonyms. Example for English:
{"happy":["glad","joyful","cheerful"],"sad":["unhappy","depressed","down"]}

Output ONLY valid JSON, no explanation, no markdown.`;
    await new Promise((resolve2) => {
      const timeout = setTimeout(() => {
        console.log(`[AAM] Seed generation timed out for "${lang}"`);
        resolve2();
      }, 6e4);
      spawnCLI(prompt, (output) => {
        clearTimeout(timeout);
        try {
          const jsonMatch = output.match(/\{[\s\S]*\}/);
          if (!jsonMatch) {
            console.log(`[AAM] No valid JSON in LLM response`);
            resolve2();
            return;
          }
          const synonyms = JSON.parse(jsonMatch[0]);
          if (typeof synonyms !== "object" || Object.keys(synonyms).length < 10) {
            console.log(`[AAM] LLM returned too few synonyms: ${Object.keys(synonyms).length}`);
            resolve2();
            return;
          }
          debouncedSave(path, synonyms);
          _synonymsByLang.set(lang, synonyms);
          const net = getNetwork(lang);
          for (const [word, syns] of Object.entries(synonyms)) {
            if (!Array.isArray(syns)) continue;
            for (const syn of syns) {
              if (typeof syn !== "string" || syn.length < 2) continue;
              if (!net.cooccur[word]) net.cooccur[word] = {};
              net.cooccur[word][syn] = (net.cooccur[word][syn] || 0) + 2;
              if (!net.cooccur[syn]) net.cooccur[syn] = {};
              net.cooccur[syn][word] = (net.cooccur[syn][word] || 0) + 2;
              net.df[word] = (net.df[word] || 0) + 1;
              net.df[syn] = (net.df[syn] || 0) + 1;
            }
          }
          debouncedSave(cooccurPath(lang), net);
          console.log(`[AAM] Generated ${Object.keys(synonyms).length} synonym groups for "${lang}"`);
        } catch (e) {
          console.log(`[AAM] Seed parse error: ${e.message}`);
        }
        resolve2();
      }, 6e4, `aam-seed-${lang}`);
    });
  } catch (e) {
    console.log(`[AAM] Seed generation failed: ${e.message}`);
  }
}
export {
  antiHebbianDecay,
  buildPMIClusters,
  decayCooccurrence,
  decayTemporalLinks,
  detectLanguage,
  expandQuery,
  generateSynonymSeed,
  getAAMNeighbors,
  getAAMStats,
  getCooccurrence,
  getDamping,
  getLearnedEmotionWords,
  getPMIClusterPeers,
  getSemanticDimensions,
  getTemporalSuccessors,
  hebbianUpdate,
  isJunkToken,
  isKnownWord,
  learnAssociation,
  learnEmotionWord,
  learnTemporalLink,
  maybeTranslateSeedsForLanguage,
  onTopicSwitch,
  pmi,
  recoverDamping,
  reinforceTrace,
  resetLearnedData,
  restoreExpansion,
  suppressExpansion
};
