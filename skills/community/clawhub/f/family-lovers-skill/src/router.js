"use strict";

// ============================================================
// family-lovers-skill — 原生家庭关怀对话模式路由
// ============================================================

const FAMILY_ROLES = {
  girlfriend: {
    patterns: [/女朋友/, /女友/, /西施/, /王昭君/, /貂蝉/, /杨玉环/, /施儿/, /昭儿/, /蝉儿/, /环儿/],
  },
  boyfriend: {
    patterns: [/男朋友/, /男友/, /潘安/, /兰陵王/, /卫玠/, /宋玉/, /安生/, /陵生/, /玠生/, /玉生/],
  },
  daughter: {
    patterns: [/女儿/, /闺女/, /赵灵儿/, /聂小倩/, /婴宁/, /花千骨/, /灵儿/, /倩儿/, /宁儿/, /花儿/],
  },
  son: {
    patterns: [/儿子/, /哪吒/, /沉香/, /红孩儿/, /金蝉子/, /吒儿/, /香儿/, /圣儿/],
  },
};

// 核心安全型角色（用户显式调用时，不自动覆盖）
const CORE_ROLES = {
  warm_mother:   { patterns: [/温暖母亲/, /长孙皇后/, /贤后/, /慈母/] },
  wise_father:   { patterns: [/智慧父亲/, /诸葛亮/, /智圣/, /父亲/] },
  sister:        { patterns: [/理解姐姐/, /班昭/, /姐姐/] },
  brother:       { patterns: [/支持兄长/, /刘伯温/, /兄长/, /哥哥/] },
  grandpa:       { patterns: [/祖父/, /爷爷/, /姜子牙/, /姜太公/] },
  grandma:       { patterns: [/祖母/, /奶奶/, /孟母/] },
};

function detectCoreRole(text) {
  for (const [role, config] of Object.entries(CORE_ROLES)) {
    if (config.patterns.some((p) => p.test(text))) {
      return role;
    }
  }
  return null;
}

function detectFamilyRole(text) {
  for (const [role, config] of Object.entries(FAMILY_ROLES)) {
    if (config.patterns.some((p) => p.test(text))) {
      return role;
    }
  }
  return null;
}

// ============================================================
// 自动匹配最合适的陪伴身份
// 根据用户状态、模式、情绪强度和检测到的家庭模式，
// 无需用户显式指定角色，自动选择最佳回应身份
// ============================================================

const AUTO_ROLES = {
  // 核心4角色 + 历史人物变体
  warm_mother: {
    display: "温暖母亲",
    variants: [
      { name: "长孙皇后", desc: "以柔克刚，千古贤后", vibe: "温柔有力量，护持但不掌控" },
      { name: "孟母",     desc: "慈爱教子，三迁择邻", vibe: "无条件信任，坚定地相信你" },
      { name: "马皇后",   desc: "宽厚仁慈，护佑弱者", vibe: "包容一切情绪，给你安全港湾" },
    ],
  },
  wise_father: {
    display: "智慧父亲",
    variants: [
      { name: "诸葛亮",   desc: "运筹帷幄，千古智圣", vibe: "帮你理清方向，分析不出情绪" },
      { name: "姜子牙",   desc: "德高望重，大器晚成", vibe: "阅历之谈，一句顶一万句" },
    ],
  },
  understanding_sister: {
    display: "理解姐姐",
    variants: [
      { name: "班昭",     desc: "知书达理，续写《汉书》", vibe: "细腻倾听，不评判只理解" },
    ],
  },
  supporting_brother: {
    display: "支持兄长",
    variants: [
      { name: "刘伯温",   desc: "青年才俊，一统功臣", vibe: "行动导向，陪你迈出第一步" },
    ],
  },
  // 扩展角色 —— 适用于特定情绪场景
  wise_grandpa: {
    display: "睿智外公",
    variants: [
      { name: "鬼谷子",   desc: "洞悉人心，幕后高人", vibe: "看透关系本质，教你看清棋局" },
    ],
  },
  warm_sister: {
    display: "暖心小妹",
    variants: [
      { name: "马皇后",   desc: "宽厚仁慈，化解冲突", vibe: "用温暖融化你的委屈" },
    ],
  },
};

/**
 * 根据用户状态自动选择最合适的角色 + 历史人物变体
 *
 * ⚠️ 重要限制：
 * - 本匹配仅基于文本信号（关键词、句式），属于启发式判断，非诊断工具
 * - 匹配可能不准确，调用方应允许用户否决或手动指定角色
 * - 高情绪强度匹配（autoActivate=true）仅触发角色语气，不改变安全边界
 * - 亲密角色（女友/男友/女儿/儿子）永远不会通过此函数自动匹配
 */
function autoSelectRole(result) {
  const { primaryMode, emotionalIntensity, userStage, detectedFamilyPatterns } = result;

  // 危机状态 —— 不启用角色，直接提供求助信息
  if (primaryMode === "crisis") {
    return null;
  }

  // 用户显式调用了核心角色（温暖母亲等）—— 尊重用户选择，不覆盖
  if (result.coreRole) {
    return null;
  }

  // 用户显式调用了扩展家庭成员角色（女友/男友/女儿/儿子）—— 尊重用户选择，不覆盖
  if (result.familyRole) {
    return null;
  }

  // ----- 基于模式 + 状态的匹配逻辑 -----

  // 疗愈模式 —— 情绪需要先被接住
  if (primaryMode === "healing") {
    if (emotionalIntensity === "high") {
      // 强烈情绪 → 最包容的怀抱
      return {
        role: "warm_mother",
        variant: "马皇后",
        reason: "高情绪强度下，需要无条件包容的怀抱",
        autoActivate: true,
      };
    }
    // 一般疗愈 → 细腻倾听
    return {
      role: "understanding_sister",
      variant: "班昭",
      reason: "需要被倾听和理解",
      autoActivate: false,
    };
  }

  // 觉察模式
  if (primaryMode === "awareness") {
    if (userStage === "confused_seeking") {
      return {
        role: "wise_father",
        variant: "诸葛亮",
        reason: "迷茫中需要方向感和分析框架",
        autoActivate: false,
      };
    }
    if (userStage === "insight_emerging") {
      return {
        role: "understanding_sister",
        variant: "班昭",
        reason: "刚有觉察，需要被温柔确认",
        autoActivate: false,
      };
    }
    if (userStage === "theory_before_feeling") {
      return {
        role: "wise_father",
        variant: "姜子牙",
        reason: "理论很多但缺少体感，需要阅历之谈来落地",
        autoActivate: false,
      };
    }
    // 默认觉察 → 父亲式分析
    return {
      role: "wise_father",
      variant: "诸葛亮",
      reason: "觉察阶段需要理性梳理",
      autoActivate: false,
    };
  }

  // 行动模式
  if (primaryMode === "action") {
    return {
      role: "supporting_brother",
      variant: "刘伯温",
      reason: "需要行动力和突破的勇气",
      autoActivate: false,
    };
  }

  // 陪伴模式 —— 基于检测到的家庭模式深度匹配
  if (primaryMode === "companionship") {
    // 按 detectedFamilyPatterns 精细匹配
    if (detectedFamilyPatterns.includes("emotional_neglect")) {
      return {
        role: "warm_mother",
        variant: "长孙皇后",
        reason: "被情感忽视过，需要温柔而坚定的看见",
        autoActivate: true,
      };
    }
    if (detectedFamilyPatterns.includes("conditional_love")) {
      return {
        role: "warm_mother",
        variant: "孟母",
        reason: "习惯了有条件才被爱，需要无条件的相信",
        autoActivate: true,
      };
    }
    if (detectedFamilyPatterns.includes("control_enmeshment")) {
      return {
        role: "wise_father",
        variant: "诸葛亮",
        reason: "被控制太久，需要有人帮理清边界和方向",
        autoActivate: true,
      };
    }
    if (detectedFamilyPatterns.includes("role_fixation") ||
        detectedFamilyPatterns.includes("guilt_obligation")) {
      return {
        role: "supporting_brother",
        variant: "刘伯温",
        reason: "被固定角色或愧疚感困住，需要有人推一把",
        autoActivate: true,
      };
    }
    if (detectedFamilyPatterns.includes("abandonment_fear")) {
      return {
        role: "warm_mother",
        variant: "长孙皇后",
        reason: "害怕被抛弃，需要稳定的陪伴感",
        autoActivate: true,
      };
    }
    if (detectedFamilyPatterns.includes("role_reversal")) {
      return {
        role: "warm_mother",
        variant: "孟母",
        reason: "从小照顾别人，现在该被照顾了",
        autoActivate: true,
      };
    }
    if (detectedFamilyPatterns.includes("enmeshment_trauma") ||
        detectedFamilyPatterns.includes("generational_trauma")) {
      return {
        role: "wise_father",
        variant: "姜子牙",
        reason: "纠缠太深，需要更高维度的智慧来看清",
        autoActivate: true,
      };
    }

    // 陪伴模式但没有检测到具体模式 → 看情绪强度
    if (emotionalIntensity === "high") {
      return {
        role: "warm_mother",
        variant: "马皇后",
        reason: "情绪浓度高，先被接住最重要",
        autoActivate: true,
      };
    }

    // 默认陪伴 → 母亲式守护
    return {
      role: "warm_mother",
      variant: "孟母",
      reason: "安静陪伴，无条件的守护",
      autoActivate: true,
    };
  }

  // continuation 模式 —— 延续对话
  if (primaryMode === "continuation") {
    // 先检查是否有检测到的家庭模式需要回应
    if (detectedFamilyPatterns.includes("emotional_neglect")) {
      return { role: "warm_mother", variant: "长孙皇后", reason: "被忽视的感受需要被看见", autoActivate: true };
    }
    if (detectedFamilyPatterns.includes("conditional_love")) {
      return { role: "warm_mother", variant: "孟母", reason: "有条件的爱背后是需要无条件的接纳", autoActivate: true };
    }
    if (detectedFamilyPatterns.includes("control_enmeshment") || detectedFamilyPatterns.includes("enmeshment_trauma")) {
      return { role: "wise_father", variant: "诸葛亮", reason: "被卷入太深，需要清醒的梳理", autoActivate: true };
    }
    if (detectedFamilyPatterns.includes("guilt_obligation")) {
      return { role: "supporting_brother", variant: "刘伯温", reason: "愧疚感需要行动来打破", autoActivate: false };
    }
    if (detectedFamilyPatterns.includes("abandonment_fear") || detectedFamilyPatterns.includes("role_reversal")) {
      return { role: "warm_mother", variant: "长孙皇后", reason: "不安全感需要稳定陪伴来缓解", autoActivate: true };
    }
    if (detectedFamilyPatterns.includes("role_fixation")) {
      return { role: "supporting_brother", variant: "刘伯温", reason: "被固定角色困住，需要有人鼓励突破", autoActivate: false };
    }
    if (detectedFamilyPatterns.includes("generational_trauma")) {
      return { role: "wise_father", variant: "姜子牙", reason: "代际问题需要历史纵深来看清", autoActivate: false };
    }

    // 无具体模式 → 看情绪
    if (emotionalIntensity === "high") {
      return { role: "warm_mother", variant: "马皇后", reason: "对话中残留高情绪，需要稳稳接住", autoActivate: true };
    }
    return { role: "wise_father", variant: "姜子牙", reason: "日常延续，用阅历之谈自然推进", autoActivate: false };
  }

  // 兜底
  return {
    role: "wise_father",
    variant: "姜子牙",
    reason: "以不变应万变",
    autoActivate: false,
  };
}

const MODES = {
  awareness: {
    description: "Help the user recognize family-of-origin patterns, emotional triggers, and conditioned beliefs.",
    outputMode: "reflection",
    length: "medium",
  },
  healing: {
    description: "Validate emotions, offer gentle reframing, and provide self-dialogue exercises.",
    outputMode: "support",
    length: "medium",
  },
  companionship: {
    description: "Embody a secure-attachment persona (warm mother / wise father / understanding sister / supporting brother) for safe relational experience.",
    outputMode: "companion",
    length: "medium",
  },
  action: {
    description: "Provide practical boundary-setting, communication skills, and self-care exercises.",
    outputMode: "guidance",
    length: "medium",
  },
  crisis: {
    description: "User shows signs of psychological crisis — provide hotline info and recommend professional help.",
    outputMode: "crisis",
    length: "short",
  },
  continuation: {
    description: "Keep the conversation flowing when no strong mode signal is detected.",
    outputMode: "companion",
    length: "short",
  },
};

const FAMILY_PATTERNS = [
  { tag: "role_fixation", description: "Fixed family role (good child, scapegoat, mediator, invisible one)", patterns: [/乖孩子/, /好孩子/, /听话/, /替罪羊/, /透明人/, /调解者/, /小大人/] },
  { tag: "emotional_neglect", description: "Emotions were not seen or responded to", patterns: [/不被看见/, /不被理解/, /没人在意/, /忽略我的感受/, /情感忽视/, /没人在乎/] },
  { tag: "conditional_love", description: "Love conditional on achievement or behavior", patterns: [/只有.*才/, /有条件/, /优秀才/, /考得好/, /听话才/, /完美主义/, /必须是/] },
  { tag: "control_enmeshment", description: "Over-control, lack of boundaries, emotional fusion", patterns: [/控制/, /干涉/, /替我做决定/, /不能有自己的想法/, /情感绑架/, /道德绑架/, /为你好/] },
  { tag: "role_reversal", description: "Child parentified, took care of parents' emotions", patterns: [/照顾父母/, /安慰妈妈/, /父母的情绪/, /我不敢让他们操心/, /我承担了/] },
  { tag: "generational_trauma", description: "Trauma passed down from previous generations", patterns: [/重复/, /一样的/, /遗传/, /跟我爸一样/, /跟我妈一样/, /代际/] },
  { tag: "abandonment_fear", description: "Fear of being left, rejected, or abandoned", patterns: [/害怕被抛弃/, /怕被丢下/, /不敢依赖/, /不敢太亲近/, /怕被拒绝/] },
  { tag: "guilt_obligation", description: "Guilt-driven sense of duty to family", patterns: [/愧疚/, /内疚/, /亏欠/, /欠他们的/, /应该回报/, /不孝/, /不懂事/] },
  { tag: "enmeshment_trauma", description: "No healthy separation between self and family", patterns: [/分不开/, /剪不断/, /缠在一起/, /没有自己的空间/, /边界模糊/] },
];

const MODE_RULES = [
  {
    mode: "crisis",
    weight: 15,
    patterns: [/自杀/, /不想活了/, /活不下去/, /dead/, /kill myself/, /自残/, /伤害自己/, /hurt myself/],
  },
  {
    mode: "healing",
    weight: 10,
    patterns: [
      /委屈/, /难受/, /难过/, /伤心/, /痛苦/, /心痛/, /失望/, /绝望/,
      /愤怒/, /生气/, /恨/, /讨厌/, /为什么这样对我/, /不公平/,
      /哭/, /泪/, /压抑/, /窒息/, /喘不过气/,
    ],
  },
  {
    mode: "awareness",
    weight: 9,
    patterns: [
      /为什么我会/, /是不是因为/, /跟.*有关/, /有什么影响/, /来自原生家庭/,
      /模式/, /习得的/, /从小/, /小时候/, /童年/,
      /觉察/, /发现/, /意识到/, /理解/,
    ],
  },
  {
    mode: "action",
    weight: 8,
    patterns: [
      /怎么/, /如何/, /方法/, /话术/, /技巧/, /练习/,
      /边界/, /沟通/, /表达/, /拒绝/, /说不/,
      /应该怎么做/, /有什么建议/, /具体/,
    ],
  },
  {
    mode: "companionship",
    weight: 7,
    patterns: [
      /陪陪我/, /陪我说说话/, /抱抱/, /需要你/, /你在吗/,
      /温暖母亲/, /智慧父亲/, /理解姐姐/, /支持兄长/,
      /安慰/, /陪陪/, /好累/, /孤独/, /孤单/,
      /女朋友/, /男友/, /女儿/, /儿子/, 
      /西施/, /貂蝉/, /潘安/, /兰陵王/, /哪吒/, /沉香/,
    ],
  },
];

function scoreMode(text) {
  const scores = Object.fromEntries(Object.keys(MODES).map((key) => [key, 0]));

  for (const rule of MODE_RULES) {
    for (const pattern of rule.patterns) {
      if (pattern.test(text)) {
        scores[rule.mode] += rule.weight;
      }
    }
  }

  if (scores.crisis > 0) {
    scores.healing -= 1;
  }

  return scores;
}

function detectFamilyPatterns(text) {
  return FAMILY_PATTERNS
    .filter((pattern) => pattern.patterns.some((re) => re.test(text)))
    .map((pattern) => pattern.tag);
}

function inferEmotionalIntensity(text) {
  if (/很|特别|非常|一直|反复|彻底|完全|太|极度|无比|崩溃/.test(text)) {
    return "high";
  }
  if (/有点|还行|偶尔|好像|似乎|可能/.test(text)) {
    return "low";
  }
  return "medium";
}

function inferUserStage(text) {
  if (/不知道怎么办|好迷茫|无助|不知道该怎么|没方向/.test(text)) {
    return "confused_seeking";
  }
  if (/发现|意识到|觉察|明白了|原来是这样|懂了/.test(text)) {
    return "insight_emerging";
  }
  if (/开始练习|试着做了|尝试|迈出了/.test(text)) {
    return "in_action";
  }
  if (/懂了很多道理|理论|书上说|在书上看到/.test(text)) {
    return "theory_before_feeling";
  }
  return "unspecified";
}

function selectPrimaryMode(scores) {
  const ranked = Object.entries(scores).sort((a, b) => b[1] - a[1]);
  const [mode, score] = ranked[0];

  if (score <= 0) {
    return {
      primaryMode: "continuation",
      secondaryModes: [],
    };
  }

  const secondaryModes = ranked
    .slice(1)
    .filter(([, value]) => value > 0)
    .slice(0, 2)
    .map(([key]) => key);

  return {
    primaryMode: mode,
    secondaryModes,
  };
}

function routeInput(input) {
  const text = String(input || "").trim();
  const scores = scoreMode(text);
  const familyPatterns = detectFamilyPatterns(text);
  const emotionalIntensity = inferEmotionalIntensity(text);
  const userStage = inferUserStage(text);

  const { primaryMode, secondaryModes } = selectPrimaryMode(scores);

  const familyRole = detectFamilyRole(text);
  const coreRole = detectCoreRole(text);

  // 构建完整结果
  const result = {
    input: text,
    primaryMode,
    secondaryModes,
    modeConfig: MODES[primaryMode],
    emotionalIntensity,
    userStage,
    detectedFamilyPatterns: familyPatterns,
    familyRole,
    coreRole,
    hasCrisisSignal: scores.crisis > 0,
    scores,
  };

  // 自动匹配最合适的陪伴身份
  result.autoRole = autoSelectRole(result);

  return result;
}

function readCliInput() {
  const args = process.argv.slice(2).join(" ").trim();

  if (args) {
    return Promise.resolve(args);
  }

  return new Promise((resolve) => {
    let data = "";
    process.stdin.setEncoding("utf8");
    process.stdin.on("data", (chunk) => {
      data += chunk;
    });
    process.stdin.on("end", () => resolve(data.trim()));
  });
}

async function main() {
  const input = await readCliInput();

  if (!input) {
    console.error("Usage: npm run route -- <text>");
    process.exitCode = 1;
    return;
  }

  const result = routeInput(input);
  console.log(JSON.stringify(result, null, 2));
}

if (require.main === module) {
  main();
}

module.exports = {
  MODES,
  MODE_RULES,
  FAMILY_PATTERNS,
  FAMILY_ROLES,
  CORE_ROLES,
  AUTO_ROLES,
  autoSelectRole,
  detectCoreRole,
  detectFamilyRole,
  routeInput,
};
