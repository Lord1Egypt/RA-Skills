const EMOTION_POSITIVE = ["\u5F00\u5FC3", "\u54C8\u54C8", "\u725B\u903C", "\u592A\u68D2", "\u611F\u8C22", "\u8C22\u8C22", "\u5389\u5BB3", "\u5B8C\u7F8E", "\u723D", "\u8D5E", "\u8212\u670D", "\u7EC8\u4E8E", "happy", "great", "awesome", "thanks", "perfect", "amazing", "lol", "haha", "nice"];
const EMOJI_MOOD = {
  "\u{1F60A}": 0.5,
  "\u{1F603}": 0.5,
  "\u{1F604}": 0.5,
  "\u{1F642}": 0.2,
  "\u{1F601}": 0.4,
  "\u{1F602}": 0.4,
  "\u{1F923}": 0.4,
  "\u{1F606}": 0.3,
  "\u{1F389}": 0.6,
  "\u{1F973}": 0.6,
  "\u{1F3C6}": 0.5,
  "\u2764\uFE0F": 0.5,
  "\u{1F495}": 0.4,
  "\u{1F970}": 0.5,
  "\u{1F60D}": 0.4,
  "\u{1F44D}": 0.3,
  "\u{1F4AA}": 0.3,
  "\u2705": 0.3,
  "\u{1F64F}": 0.3,
  "\u{1F622}": -0.5,
  "\u{1F62D}": -0.6,
  "\u{1F972}": -0.3,
  "\u{1F621}": -0.6,
  "\u{1F92C}": -0.7,
  "\u{1F624}": -0.4,
  "\u{1F630}": -0.4,
  "\u{1F628}": -0.5,
  "\u{1F631}": -0.5,
  "\u{1F629}": -0.4,
  "\u{1F62B}": -0.5,
  "\u{1F97A}": -0.3,
  "\u{1F494}": -0.5,
  "\u{1F61E}": -0.4,
  "\u{1F614}": -0.4,
  "\u{1F610}": 0,
  "\u{1F914}": 0,
  "\u{1F605}": -0.1,
  "\u{1FAE0}": -0.2,
  "\u{1F525}": 0.3,
  "\u{1F480}": -0.2,
  "\u{1F921}": -0.2
};
function detectEmojiMood(msg) {
  let totalMood = 0;
  let count = 0;
  for (const [emoji, mood] of Object.entries(EMOJI_MOOD)) {
    if (msg.includes(emoji)) {
      totalMood += mood;
      count++;
    }
  }
  return count > 0 ? totalMood / count : null;
}
const EMOTION_NEGATIVE = ["\u70E6", "\u7D2F", "\u96BE\u8FC7", "\u5D29\u6E83", "\u538B\u529B\u5927", "\u538B\u529B\u597D\u5927", "\u7126\u8651", "\u90C1\u95F7", "\u70E6\u6B7B", "\u53D7\u4E0D\u4E86", "\u5934\u75BC", "\u65E0\u8BED", "\u5410\u4E86", "\u4E0D\u60F3\u5E72", "\u4E0D\u60F3\u8BF4", "\u5FC3\u60C5\u5DEE", "\u5FC3\u60C5\u5F88\u5DEE", "\u4E0D\u60F3\u6D3B", "\u96BE\u53D7", "annoyed", "tired", "sad", "overwhelmed", "stressed", "anxious", "frustrated", "exhausted", "depressed"];
const EMOTION_ALL = [...EMOTION_NEGATIVE, ...EMOTION_POSITIVE];
function detectEmotionLabel(msg) {
  const m = msg.toLowerCase();
  const len = msg.length;
  if (/[！!]{2,}/.test(msg) && EMOTION_NEGATIVE.some((w) => m.includes(w))) return { label: "anger", confidence: 0.9 };
  if (["\u6C14\u6B7B", "\u751F\u6C14", "\u6012\u4E86", "\u64CD", "\u5988\u7684", "\u4EC0\u4E48\u73A9\u610F", "\u8111\u6B8B", "\u667A\u969C", "angry", "furious", "pissed", "hate"].some((w) => m.includes(w))) return { label: "anger", confidence: 0.9 };
  if (["\u7126\u8651", "\u62C5\u5FC3", "\u7D27\u5F20", "\u5BB3\u6015", "\u614C", "\u7740\u6025", "\u6765\u4E0D\u53CA", "\u600E\u4E48\u529E", "\u5B8C\u86CB", "\u538B\u529B\u5927", "\u538B\u529B\u597D\u5927", "\u6491\u4E0D\u4F4F", "\u88AB\u88C1", "\u8981\u88AB\u88C1", "worried", "nervous", "scared", "anxious", "panic", "deadline"].some((w) => m.includes(w))) return { label: "anxiety", confidence: 0.85 };
  if (/deadline|ddl|来不及|赶不上/.test(m)) return { label: "anxiety", confidence: 0.8 };
  if (["\u70E6\u6B7B", "\u53D7\u4E0D\u4E86", "\u65E0\u8BED", "\u670D\u4E86", "\u5E9F\u4E86", "\u5934\u75BC", "\u641E\u4E0D\u5B9A", "\u53C8\u51FA\u95EE\u9898", "\u53C8\u6302\u4E86", "\u53C8\u5D29\u4E86", "\u4E0D\u9002\u5408", "\u653E\u5F03\u4E86", "\u6CA1\u6551\u4E86", "stuck", "broken", "failed", "give up", "hopeless"].some((w) => m.includes(w))) return { label: "frustration", confidence: 0.85 };
  if (/又.*了|还是不行|试了.*[次遍]|改了.*天|搞了.*还|都不行|还是不对/.test(m)) return { label: "frustration", confidence: 0.7 };
  if (/是不是不适合/.test(m)) return { label: "frustration", confidence: 0.65 };
  if (["\u5931\u671B", "\u767D\u8D39", "\u767D\u5FD9", "\u6CA1\u60F3\u5230", "\u539F\u6765\u662F\u8FD9\u6837", "\u65E9\u77E5\u9053", "disappointed", "wasted", "regret"].some((w) => m.includes(w))) return { label: "disappointment", confidence: 0.8 };
  if (["\u96BE\u8FC7", "\u4F24\u5FC3", "\u5FC3\u75BC", "\u60F3\u54ED", "\u54ED\u4E86", "\u597D\u96BE", "\u592A\u96BE\u4E86", "\u5FC3\u7D2F", "\u65E0\u529B", "\u5206\u624B", "\u79BB\u804C", "\u4F4F\u9662", "\u53BB\u4E16", "\u8D70\u4E86", "sad", "heartbroken", "crying", "lonely", "miss", "breakup", "quit", "hospitalized", "died"].some((w) => m.includes(w))) return { label: "sadness", confidence: 0.85 };
  if (["\u56F0\u60D1", "\u4E0D\u660E\u767D", "\u641E\u4E0D\u61C2", "\u4EC0\u4E48\u610F\u601D", "\u4E3A\u4EC0\u4E48\u4F1A", "\u600E\u4E48\u56DE\u4E8B", "\u770B\u4E0D\u61C2", "\u8FF7\u832B", "\u600E\u4E48\u7406\u89E3", "\u5E2E\u6211\u89E3\u91CA", "\u5230\u5E95\u600E\u4E48", "confused", "don't understand", "what do you mean", "lost", "how"].some((w) => m.includes(w))) return { label: "confusion", confidence: 0.8 };
  if (/[？?]{2,}/.test(msg)) return { label: "confusion", confidence: 0.6 };
  if (["\u7EC8\u4E8E", "\u641E\u5B9A\u4E86", "\u89E3\u51B3\u4E86", "\u539F\u6765\u5982\u6B64", "\u604D\u7136\u5927\u609F", "\u660E\u767D\u4E86", "\u901A\u4E86", "\u603B\u7B97", "\u4E0D\u5BB9\u6613", "finally", "solved", "fixed", "got it", "aha"].some((w) => m.includes(w))) return { label: "relief", confidence: 0.8 };
  if (["\u641E\u5B9A", "\u6210\u529F", "\u505A\u5230\u4E86", "\u5B8C\u6210\u4E86", "\u4E0A\u7EBF\u4E86", "\u8FC7\u4E86", "\u62FF\u5230\u4E86", "\u901A\u8FC7\u4E86", "\u5938\u4E86\u6211", "star", "did it", "success", "deployed", "passed", "promoted"].some((w) => m.includes(w))) return { label: "pride", confidence: 0.75 };
  if (["\u671F\u5F85", "\u597D\u60F3", "\u7B49\u4E0D\u53CA", "\u5E0C\u671B", "\u6253\u7B97", "\u51C6\u5907", "\u8981\u5F00\u59CB", "excited", "looking forward", "can't wait", "hope", "planning"].some((w) => m.includes(w))) return { label: "anticipation", confidence: 0.7 };
  if (["\u611F\u8C22", "\u8C22\u8C22", "\u591A\u4E8F", "\u5E78\u597D", "\u8FD8\u597D\u6709\u4F60", "\u5E2E\u4E86\u5927\u5FD9", "grateful", "thank you", "thanks to", "appreciate"].some((w) => m.includes(w))) return { label: "gratitude", confidence: 0.85 };
  if (["\u5F00\u5FC3", "\u54C8\u54C8", "\u592A\u68D2", "\u725B\u903C", "\u5389\u5BB3", "\u5B8C\u7F8E", "\u723D", "\u8212\u670D", "\u8D5E", "\u563F\u563F", "\u5FC3\u60C5\u597D", "\u5FC3\u60C5\u8D85\u597D", "\u9AD8\u5174", "\u592A\u597D\u4E86", "\u597D\u5F00\u5FC3", "happy", "great", "awesome", "amazing", "perfect", "love it", "so good"].some((w) => m.includes(w))) return { label: "joy", confidence: 0.8 };
  if (/[哈嘻]{3,}/.test(msg)) return { label: "joy", confidence: 0.7 };
  if (EMOTION_POSITIVE.some((w) => m.includes(w))) return { label: "joy", confidence: 0.4 };
  if (EMOTION_NEGATIVE.some((w) => m.includes(w))) return { label: "frustration", confidence: 0.4 };
  const emojiMood = detectEmojiMood(msg);
  if (emojiMood !== null) {
    if (emojiMood > 0.3) return { label: "joy", confidence: Math.min(0.8, Math.abs(emojiMood)) };
    if (emojiMood < -0.3) return { label: "sadness", confidence: Math.min(0.8, Math.abs(emojiMood)) };
  }
  try {
    const { getLearnedEmotionWords } = require("./aam.ts");
    const learned = getLearnedEmotionWords();
    const msgLower = msg.toLowerCase();
    if (learned.positive.some((w) => msgLower.includes(w))) return { label: "joy", confidence: 0.5 };
    if (learned.negative.some((w) => msgLower.includes(w))) return { label: "sadness", confidence: 0.5 };
  } catch {
  }
  return { label: "neutral", confidence: 0.3 };
}
function computeEmotionSpectrum(msg) {
  const m = msg.toLowerCase();
  const spectrum = {
    anger: 0,
    anxiety: 0,
    frustration: 0,
    sadness: 0,
    joy: 0,
    pride: 0,
    relief: 0,
    curiosity: 0
  };
  const angerSignals = (m.match(/生气|愤怒|气死|混蛋|什么鬼|太过分|凭什么|受够|垃圾|什么垃圾|angry|furious|hate|damn|wtf|bullshit/g) || []).length;
  if (/[！!]{2,}/.test(msg) && angerSignals > 0) spectrum.anger = Math.min(1, 0.5 + angerSignals * 0.2);
  else spectrum.anger = Math.min(1, angerSignals * 0.3);
  const anxietySignals = (m.match(/焦虑|担心|害怕|紧张|不安|怎么办|来不及|deadline|ddl|赶不上|被裁|一堆bug|上线.*bug|worried|anxious|scared|nervous|panic|laid off/g) || []).length;
  spectrum.anxiety = Math.min(1, anxietySignals * 0.3);
  const frustSignals = (m.match(/又.*了|还是不行|试了.*次|搞不定|放弃|算了|不想|太难|不适合|改了.*天|都不行|还是不对|stuck|broken|failed|give up|still not|tried .* times|can.t fix/g) || []).length;
  spectrum.frustration = Math.min(1, frustSignals * 0.3);
  const sadSignals = (m.match(/难过|伤心|失望|遗憾|可惜|唉|哭|委屈|孤独|想念|分手|离职|住院|去世|走了|担心|sad|lonely|miss|crying|disappointed|heartbroken|quit|breakup/g) || []).length;
  spectrum.sadness = Math.min(1, sadSignals * 0.35);
  const joySignals = (m.match(/开心|高兴|太好了|哈哈|[🎉😊😄🥳]|棒|赞|厉害|成功|心情好|心情超好|迪士尼|太棒|年终奖|太爽|好开心|happy|great|awesome|amazing|perfect|love it|so good/g) || []).length;
  spectrum.joy = Math.min(1, joySignals * 0.3);
  if (/太好了|跑通了/.test(m)) spectrum.joy = Math.min(1, spectrum.joy + 0.2);
  const prideSignals = (m.match(/搞定|做到了|完成了|(?<!要|即将|准备|快要)上线了|通过了|拿到了|star|夸了|零故障|认证|did it|success|deployed|passed|promoted|shipped|merged/g) || []).length;
  spectrum.pride = Math.min(1, prideSignals * 0.35);
  const reliefSignals = (m.match(/终于|解决了|松了口气|还好|幸好|好在|没事了|总算|不容易|finally|solved|fixed|got it|aha/g) || []).length;
  spectrum.relief = Math.min(1, reliefSignals * 0.35);
  const curSignals = (m.match(/怎么.*的|为什么|好奇|想知道|有意思|原来|没想到|居然|怎么理解|帮我解释|到底怎么|生命周期|共识算法|how|why|curious|interesting|wonder|what if/g) || []).length;
  spectrum.curiosity = Math.min(1, curSignals * 0.25);
  const emojiMoodSpectrum = detectEmojiMood(msg);
  if (emojiMoodSpectrum !== null) {
    if (emojiMoodSpectrum > 0) spectrum.joy = Math.min(1, spectrum.joy + emojiMoodSpectrum * 0.5);
    if (emojiMoodSpectrum < 0) {
      spectrum.sadness = Math.min(1, spectrum.sadness + Math.abs(emojiMoodSpectrum) * 0.3);
      spectrum.frustration = Math.min(1, spectrum.frustration + Math.abs(emojiMoodSpectrum) * 0.2);
    }
  }
  for (const key of Object.keys(spectrum)) {
    spectrum[key] = Math.min(1, Math.max(0, spectrum[key]));
  }
  return spectrum;
}
function spectrumToDominant(spectrum) {
  let maxVal = 0.15;
  let maxKey = "";
  for (const [key, val] of Object.entries(spectrum)) {
    if (val > maxVal) {
      maxVal = val;
      maxKey = key;
    }
  }
  return maxKey ? { label: maxKey, confidence: maxVal } : null;
}
function emotionLabelToLegacy(label) {
  switch (label) {
    case "joy":
    case "gratitude":
    case "relief":
      return "warm";
    case "anxiety":
    case "frustration":
    case "anger":
    case "sadness":
    case "disappointment":
      return "painful";
    case "pride":
    case "anticipation":
      return "important";
    default:
      return "neutral";
  }
}
function emotionLabelToPADCN(label) {
  switch (label) {
    case "joy":
      return { pleasure: 0.6, arousal: 0.4, dominance: 0.2, certainty: 0.3, novelty: 0.1 };
    case "gratitude":
      return { pleasure: 0.5, arousal: 0.1, dominance: -0.1, certainty: 0.3, novelty: 0 };
    case "pride":
      return { pleasure: 0.5, arousal: 0.3, dominance: 0.5, certainty: 0.4, novelty: 0.1 };
    case "anticipation":
      return { pleasure: 0.3, arousal: 0.5, dominance: 0.1, certainty: -0.2, novelty: 0.5 };
    case "relief":
      return { pleasure: 0.4, arousal: -0.3, dominance: 0.2, certainty: 0.5, novelty: -0.1 };
    case "anxiety":
      return { pleasure: -0.5, arousal: 0.6, dominance: -0.4, certainty: -0.6, novelty: 0.2 };
    case "frustration":
      return { pleasure: -0.5, arousal: 0.4, dominance: -0.2, certainty: -0.1, novelty: -0.2 };
    case "anger":
      return { pleasure: -0.7, arousal: 0.8, dominance: 0.3, certainty: 0.2, novelty: -0.1 };
    case "sadness":
      return { pleasure: -0.6, arousal: -0.4, dominance: -0.5, certainty: -0.2, novelty: -0.3 };
    case "disappointment":
      return { pleasure: -0.5, arousal: -0.2, dominance: -0.3, certainty: -0.3, novelty: -0.2 };
    case "confusion":
      return { pleasure: -0.1, arousal: 0.2, dominance: -0.4, certainty: -0.7, novelty: 0.3 };
    default:
      return { pleasure: 0, arousal: 0, dominance: 0, certainty: 0, novelty: 0 };
  }
}
const CORRECTION_WORDS = ["\u4E0D\u5BF9", "\u9519\u4E86", "\u641E\u9519", "\u7406\u89E3\u9519", "\u4E0D\u662F\u8FD9\u6837", "\u8BF4\u53CD\u4E86", "\u522B\u778E\u8BF4", "wrong", "\u91CD\u6765", "\u6709\u95EE\u9898", "\u641E\u6DF7", "\u5F04\u9519", "\u4F60\u8BF4\u7684\u4E0D", "\u5B9E\u9645\u4E0A", "mistake", "incorrect", "not right", "misunderstood", "actually", "correction"];
const CORRECTION_EXCLUDE = ["\u6CA1\u9519", "\u4E0D\u9519", "\u5BF9\u4E0D\u5BF9", "\u9519\u4E86\u5417", "\u662F\u4E0D\u662F\u9519", "\u4E0D\u5BF9\u79F0", "\u4E0D\u5BF9\u52B2", "\u9519\u4E86\u9519\u4E86\u6211\u7684", "\u4F60\u8BF4\u5F97\u5BF9", "\u6CA1\u6709\u9519", "not wrong", "correct", "you're right", "no mistake"];
const TECH_WORDS = [
  // 通用编程
  "\u4EE3\u7801",
  "\u51FD\u6570",
  "\u62A5\u9519",
  "error",
  "bug",
  "crash",
  "\u7F16\u8BD1",
  "\u8C03\u8BD5",
  "debug",
  "\u5B9E\u73B0",
  "\u600E\u4E48\u5199",
  "\u7B97\u6CD5",
  "\u63A5\u53E3",
  "api",
  "\u53D8\u91CF",
  "\u5FAA\u73AF",
  "\u9012\u5F52",
  "\u6392\u5E8F",
  "\u6570\u636E\u7ED3\u6784",
  "\u6CDB\u578B",
  "\u7C7B\u578B",
  // 语言
  "python",
  "javascript",
  "typescript",
  "go",
  "golang",
  "rust",
  "java",
  "swift",
  "c++",
  "php",
  "vue",
  "react",
  "angular",
  "node",
  "deno",
  "bun",
  // 基础设施
  "docker",
  "kubernetes",
  "k8s",
  "nginx",
  "apache",
  "linux",
  "git",
  "ci/cd",
  "jenkins",
  "redis",
  "mysql",
  "mongodb",
  "postgresql",
  "kafka",
  "rabbitmq",
  "elasticsearch",
  // 云/部署
  "\u670D\u52A1\u5668",
  "\u90E8\u7F72",
  "deploy",
  "\u5BB9\u5668",
  "\u96C6\u7FA4",
  "\u8D1F\u8F7D\u5747\u8861",
  "\u5FAE\u670D\u52A1",
  "grpc",
  "rest",
  "\u963F\u91CC\u4E91",
  "aws",
  "gcp",
  "\u4E91\u670D\u52A1",
  // 安全/逆向
  "hook",
  "frida",
  "ida",
  "\u9006\u5411",
  "\u52A0\u5BC6",
  "\u7B7E\u540D",
  "\u8BC1\u4E66",
  // 性能
  "\u6027\u80FD",
  "\u4F18\u5316",
  "\u5185\u5B58",
  "\u6CC4\u6F0F",
  "leak",
  "\u6162\u67E5\u8BE2",
  "\u7D22\u5F15",
  "\u7F13\u5B58",
  // 概念
  "raft",
  "\u5171\u8BC6",
  "\u5206\u5E03\u5F0F",
  "\u5E76\u53D1",
  "\u7EBF\u7A0B",
  "\u534F\u7A0B",
  "goroutine",
  "channel",
  "async",
  "await",
  "hpa",
  "rebase",
  "\u591A\u9636\u6BB5\u6784\u5EFA",
  "\u53CD\u5411\u4EE3\u7406",
  "\u6570\u636E\u5206\u7247"
];
const CASUAL_WORDS = ["\u55EF", "\u597D", "\u54E6", "\u884C", "\u53EF\u4EE5", "ok", "\u660E\u767D", "\u5728\u5417", "\u4F60\u597D", "\u5403\u4E86", "\u65E0\u804A", "\u54C8\u54C8", "\u54C8\u54C8\u54C8", "\u5468\u672B", "\u563F\u563F", "\u5475\u5475", "hey", "hi", "hello", "yeah", "yep", "sure", "hmm", "lol", "haha", "bored", "weekend"];
const TECH_CLASSIFY = ["\u4EE3\u7801", "code", "\u51FD\u6570", "bug", "error", "\u5B9E\u73B0", "\u600E\u4E48\u5199", "function", "class", "\u62A5\u9519"];
const EMOTION_CLASSIFY = ["\u70E6", "\u7D2F", "\u96BE\u8FC7", "\u5F00\u5FC3", "\u7126\u8651", "\u538B\u529B", "\u90C1\u95F7", "\u5D29\u6E83"];
function classifyQuick(msg) {
  const m = msg.toLowerCase();
  const techHits = TECH_WORDS.filter((w) => m.includes(w)).length;
  const emotionHits = EMOTION_ALL.filter((w) => m.includes(w)).length;
  const casualHits = CASUAL_WORDS.filter((w) => m === w || m === w + "\u7684").length;
  if (techHits >= 2 || techHits >= 1 && msg.length > 30) return "technical";
  if (emotionHits >= 2) return "emotional";
  if (casualHits >= 1 && msg.length < 15) return "casual";
  if (msg.length < 8) return "casual";
  return "general";
}
export {
  CASUAL_WORDS,
  CORRECTION_EXCLUDE,
  CORRECTION_WORDS,
  EMOTION_ALL,
  EMOTION_CLASSIFY,
  EMOTION_NEGATIVE,
  EMOTION_POSITIVE,
  TECH_CLASSIFY,
  TECH_WORDS,
  classifyQuick,
  computeEmotionSpectrum,
  detectEmojiMood,
  detectEmotionLabel,
  emotionLabelToLegacy,
  emotionLabelToPADCN,
  spectrumToDominant
};
