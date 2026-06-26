#!/usr/bin/env node

import readline from "node:readline/promises";
import { stdin as input, stdout as output } from "node:process";
import { ensureConfig, saveConfig } from "./config-store.js";
import { generateSnapshot } from "./index.js";
import { loadProfile, appendEvent } from "./profile-store.js";
import { classifyFastTriage, createEmptyTriageFacts } from "./triage-engine.js";

const MESSAGE_MAP = {
  intro_title: {
    zh: "dont-deal 快速模式",
    en: "dont-deal quick mode"
  },
  intro_goal: {
    zh: "目标只有一个：判断现在更接近“立刻呼救”还是“尽快就医”。",
    en: "There is only one goal: decide whether this is closer to call-for-help-now or urgent-medical-review."
  },
  self_case: {
    zh: "这是你自己现在的情况吗？",
    en: "Is this your situation right now?"
  },
  symptoms_active: {
    zh: "现在胸口或相关部位还在不舒服吗？",
    en: "Is the chest or related discomfort happening right now?"
  },
  pain_type: {
    zh: "更像哪一种：\n1. 压着、发紧、发闷、像被攥住\n2. 针扎、按一下一个点疼\n3. 说不清，但不对劲",
    en: "Which is closer?\n1. Pressure, tightness, heaviness, squeezed feeling\n2. Sharp or pinpoint pain, hurts when pressed\n3. Hard to describe, but something feels wrong"
  },
  radiation: {
    zh: "会不会往左臂、后背、脖子、下巴，或者像牙疼那样往牙床放过去？没有就写“没有”。",
    en: "Does it spread to the left arm, back, neck, jaw, or feel like toothache into the gumline? If not, type none."
  },
  duration: {
    zh: "已经持续多久了？直接写分钟数，实在不清楚就写大概。",
    en: "How long has it lasted? Enter minutes if you can, or a rough estimate."
  },
  associated: {
    zh: "有没有这些情况：喘不过气、出冷汗、恶心、头晕、快晕倒？有的话简单写出来，没有就写“没有”。",
    en: "Any shortness of breath, cold sweat, nausea, dizziness, or near-fainting? Write them briefly, or type none."
  },
  rest_start: {
    zh: "这次是在休息、坐着、躺着，或者很轻的活动时开始的吗？",
    en: "Did this start while resting, sitting, lying down, or during very light activity?"
  },
  getting_worse: {
    zh: "它是在加重，或者一阵一阵回来，越来越不对劲吗？",
    en: "Is it getting worse, or returning in waves and feeling more concerning?"
  },
  pressing_worse: {
    zh: "用手按压胸口那个位置，会明显更疼吗？",
    en: "Does pressing on the spot make it clearly more painful?"
  },
  exertion_recurrent: {
    zh: "最近有没有一活动、爬楼、走快一点就容易出现这种不舒服？",
    en: "Recently, does this tend to come back with activity, climbing stairs, or walking faster?"
  },
  yes_no_retry: {
    zh: "请输入“是”或“否”。",
    en: "Please answer yes or no."
  },
  yes_no_suffix: {
    zh: "（是/否）",
    en: "(yes/no)"
  },
  result_red: {
    zh: "结论：红色",
    en: "Decision: red"
  },
  result_yellow: {
    zh: "结论：黄色",
    en: "Decision: yellow"
  },
  action_red: {
    zh: "建议：现在就呼救，不要自己开车，不要继续走动。",
    en: "Action: call emergency help now, do not drive yourself, and stop moving around."
  },
  action_yellow: {
    zh: "建议：今天尽快就医。如果胸痛持续、加重，或开始出现气短、出汗、头晕，立刻升级为呼救。",
    en: "Action: get urgent medical review today. If pain persists, worsens, or breathing trouble, sweating, or dizziness starts, switch to emergency help immediately."
  },
  reason_label: {
    zh: "原因",
    en: "Reasons"
  },
  signal_label: {
    zh: "提示",
    en: "Signals"
  },
  saved: {
    zh: "本次结果已写入本地 events.json。",
    en: "This result has been written to local events.json."
  },
  language_saved_zh: {
    zh: "后续界面将默认使用中文。",
    en: "Future runs will default to Chinese."
  },
  language_saved_en: {
    zh: "后续界面将默认使用英文。",
    en: "Future runs will default to English."
  }
};

const REASON_TRANSLATIONS = {
  "当前胸痛或胸闷已经持续 15 分钟以上。": "Current chest pain or pressure has lasted 15 minutes or longer.",
  "疼痛或压迫感正在往胸口以外的部位放射。": "Pain or pressure is spreading beyond the chest.",
  "胸部症状同时伴有气短、出汗、恶心或头晕等危险信号。": "Chest symptoms are happening together with shortness of breath, sweating, nausea, or dizziness.",
  "症状是在休息或很轻的活动时出现的。": "Symptoms started at rest or during very light activity.",
  "症状没有缓解，反而在加重或反复出现。": "Symptoms are not settling and are getting worse or recurring.",
  "已知心绞痛的发作模式发生了变化。": "A known angina pattern has changed.",
  "活动或爬楼时容易反复出现不适。": "Symptoms tend to recur with activity or climbing stairs.",
  "胸口、下巴或牙根样不适仍需要当天就医评估。": "Chest, jaw, or tooth-like discomfort still needs urgent same-day medical review.",
  "同时存在多个心血管危险因素。": "Several cardiovascular risk factors are present.",
  "近期工作和休息模式提示疲劳或睡眠明显不足。": "Recent work and rest patterns suggest marked fatigue or sleep loss.",
  "按压胸口不能明确复现这种疼痛。": "Pressing on the chest does not clearly reproduce the pain.",
  "现有信息还不能排除心脏方面的危险。": "The available information still does not safely exclude heart danger.",
  "描述更像压着、发紧、发闷、像被攥住，不像单纯针扎一下。": "The description sounds more like pressure, tightness, heaviness, or being squeezed than a simple sharp pinpoint pain.",
  "不适正在往后背、手臂、脖子或下巴这些部位放。": "The discomfort is spreading toward the back, arm, neck, or jaw.",
  "下巴痛或像牙疼一样的感觉，也可能是同一组心脏危险信号。": "Jaw pain or a toothache-like feeling can be part of the same heart warning pattern.",
  "按压更痛可以像肌肉或肋软骨问题，但单凭这一点不能排除心脏风险。": "Pain that worsens with pressing can fit a chest wall cause, but that alone does not rule out heart risk."
};

function containsChinese(text) {
  return /[\u4e00-\u9fff]/.test(text);
}

function countEnglishLetters(text) {
  const matches = text.match(/[A-Za-z]/g);
  return matches ? matches.length : 0;
}

function detectLanguageFromInputs(inputs, fallback = "zh-CN") {
  const text = inputs.join(" ");
  const chinese = (text.match(/[\u4e00-\u9fff]/g) ?? []).length;
  const english = countEnglishLetters(text);

  if (chinese === 0 && english === 0) {
    return fallback;
  }

  return chinese >= english ? "zh-CN" : "en-US";
}

function shouldUseBilingual(config) {
  return !config.first_run_completed || config.language_preference === "bilingual";
}

function getMessage(key, languagePreference, bilingualMode) {
  const message = MESSAGE_MAP[key];
  if (!message) {
    return key;
  }

  if (bilingualMode) {
    return `${message.zh}\n${message.en}`;
  }

  return languagePreference === "en-US" ? message.en : message.zh;
}

function translateLines(lines, languagePreference, bilingualMode) {
  if (bilingualMode) {
    return lines.map((line) => `${line}\n${REASON_TRANSLATIONS[line] ?? line}`);
  }

  if (languagePreference === "en-US") {
    return lines.map((line) => REASON_TRANSLATIONS[line] ?? line);
  }

  return lines;
}

function normalizeYesNo(answer) {
  const value = answer.trim().toLowerCase();
  if (["y", "yes", "1", "true", "是", "有", "在", "会"].includes(value)) {
    return true;
  }

  if (["n", "no", "0", "false", "否", "没有", "不", "不会"].includes(value)) {
    return false;
  }

  return null;
}

function parseDuration(answer) {
  const match = answer.match(/\d+/);
  if (!match) {
    return null;
  }

  return Number(match[0]);
}

function parseRadiationSites(answer) {
  const sites = [];
  const text = answer.trim();
  if (!text) {
    return sites;
  }

  const mapping = [
    ["back", ["背", "后背", "肩胛", "背部"]],
    ["left_arm", ["左臂", "左胳膊", "手臂", "arm"]],
    ["neck", ["脖子", "颈", "脖颈", "neck"]],
    ["jaw", ["下巴", "下颌", "牙", "牙床", "牙根", "jaw", "tooth", "teeth", "gum"]],
    ["shoulder", ["肩", "肩膀", "shoulder"]],
    ["back", ["back"]]
  ];

  for (const [key, keywords] of mapping) {
    if (keywords.some((keyword) => text.includes(keyword))) {
      sites.push(key);
    }
  }

  return [...new Set(sites)];
}

function mergeProfileRisks(facts, profile) {
  const baseline = profile?.baseline_risks ?? {};
  return {
    ...facts,
    hypertension: facts.hypertension ?? baseline.hypertension ?? null,
    diabetes: facts.diabetes ?? baseline.diabetes ?? null,
    smoking: facts.smoking ?? baseline.smoking ?? null,
    high_cholesterol: facts.high_cholesterol ?? baseline.high_cholesterol ?? null,
    family_history_early_heart_disease:
      facts.family_history_early_heart_disease ??
      baseline.family_history_early_heart_disease ??
      null
  };
}

async function askYesNo(rl, question, languagePreference, bilingualMode) {
  while (true) {
    const answer = await rl.question(
      `${question}\n${getMessage("yes_no_suffix", languagePreference, bilingualMode)}\n> `
    );
    const normalized = normalizeYesNo(answer);
    if (normalized !== null) {
      return {
        value: normalized,
        raw: answer.trim()
      };
    }

    output.write(`${getMessage("yes_no_retry", languagePreference, bilingualMode)}\n`);
  }
}

async function askText(rl, question) {
  const answer = await rl.question(`${question}\n> `);
  return answer.trim();
}

function renderResult(result, languagePreference, bilingualMode) {
  const reasons = translateLines(result.reasoning_summary, languagePreference, bilingualMode);
  const signals = translateLines(result.lay_signal_summary, languagePreference, bilingualMode);

  if (result.urgency === "red") {
    return {
      body: [
        getMessage("result_red", languagePreference, bilingualMode),
        getMessage("action_red", languagePreference, bilingualMode),
        `${getMessage("reason_label", languagePreference, bilingualMode)}：${reasons.join("；")}`
      ].join("\n"),
      signals
    };
  }

  return {
    body: [
      getMessage("result_yellow", languagePreference, bilingualMode),
      getMessage("action_yellow", languagePreference, bilingualMode),
      `${getMessage("reason_label", languagePreference, bilingualMode)}：${reasons.join("；")}`
    ].join("\n"),
    signals
  };
}

async function main() {
  const rl = readline.createInterface({ input, output });

  try {
    const config = await ensureConfig(process.env);
    const bilingualMode = shouldUseBilingual(config);
    const languagePreference =
      config.language_preference === "bilingual" ? "zh-CN" : config.language_preference;
    const sessionInputs = [];

    output.write(getMessage("intro_title", languagePreference, bilingualMode) + "\n");
    output.write(getMessage("intro_goal", languagePreference, bilingualMode) + "\n\n");

    const profile = await loadProfile(process.env);
    let facts = createEmptyTriageFacts();

    const selfAnswer = await askYesNo(
      rl,
      getMessage("self_case", languagePreference, bilingualMode),
      languagePreference,
      bilingualMode
    );
    sessionInputs.push(selfAnswer.raw);
    facts.subject_role = selfAnswer.value ? "self" : "other";

    const activeAnswer = await askYesNo(
      rl,
      getMessage("symptoms_active", languagePreference, bilingualMode),
      languagePreference,
      bilingualMode
    );
    sessionInputs.push(activeAnswer.raw);
    facts.symptoms_active_now = activeAnswer.value;

    const painType = await askText(
      rl,
      getMessage("pain_type", languagePreference, bilingualMode)
    );
    sessionInputs.push(painType);
    if (painType.includes("1") || painType.includes("压") || painType.includes("紧") || painType.includes("闷")) {
      facts.chest_discomfort = true;
      facts.chest_pressure_or_tightness = true;
    } else if (
      painType.includes("2") ||
      painType.includes("针") ||
      painType.includes("按") ||
      painType.toLowerCase().includes("sharp") ||
      painType.toLowerCase().includes("point")
    ) {
      facts.chest_discomfort = true;
      facts.chest_pressure_or_tightness = false;
    } else {
      facts.chest_discomfort = true;
    }

    const radiationAnswer = await askText(
      rl,
      getMessage("radiation", languagePreference, bilingualMode)
    );
    sessionInputs.push(radiationAnswer);
    facts.radiation_sites = parseRadiationSites(radiationAnswer);
    facts.jaw_or_tooth_pain =
      facts.radiation_sites.includes("jaw") ||
      radiationAnswer.includes("牙") ||
      radiationAnswer.includes("下巴") ||
      radiationAnswer.toLowerCase().includes("jaw") ||
      radiationAnswer.toLowerCase().includes("tooth");

    const durationAnswer = await askText(rl, getMessage("duration", languagePreference, bilingualMode));
    sessionInputs.push(durationAnswer);
    facts.pain_duration_minutes = parseDuration(durationAnswer);

    const associatedAnswer = await askText(
      rl,
      getMessage("associated", languagePreference, bilingualMode)
    );
    sessionInputs.push(associatedAnswer);
    const associatedLower = associatedAnswer.toLowerCase();
    facts.shortness_of_breath =
      associatedAnswer.includes("喘") || associatedAnswer.includes("气短") || associatedLower.includes("breath");
    facts.sweating = associatedAnswer.includes("汗") || associatedLower.includes("sweat");
    facts.nausea_or_vomiting =
      associatedAnswer.includes("恶心") || associatedAnswer.includes("吐") || associatedLower.includes("nausea") || associatedLower.includes("vomit");
    facts.dizziness_or_faintness =
      associatedAnswer.includes("晕") ||
      associatedAnswer.includes("头昏") ||
      associatedAnswer.includes("头晕") ||
      associatedLower.includes("dizz") ||
      associatedLower.includes("faint");

    facts.pain_started_at_rest = await askYesNo(
      rl,
      getMessage("rest_start", languagePreference, bilingualMode),
      languagePreference,
      bilingualMode
    );
    sessionInputs.push(facts.pain_started_at_rest.raw);
    facts.pain_started_at_rest = facts.pain_started_at_rest.value;
    facts.getting_worse = await askYesNo(
      rl,
      getMessage("getting_worse", languagePreference, bilingualMode),
      languagePreference,
      bilingualMode
    );
    sessionInputs.push(facts.getting_worse.raw);
    facts.getting_worse = facts.getting_worse.value;
    facts.pain_worse_with_pressing_on_chest = await askYesNo(
      rl,
      getMessage("pressing_worse", languagePreference, bilingualMode),
      languagePreference,
      bilingualMode
    );
    sessionInputs.push(facts.pain_worse_with_pressing_on_chest.raw);
    facts.pain_worse_with_pressing_on_chest = facts.pain_worse_with_pressing_on_chest.value;
    facts.recurrent_with_exertion = await askYesNo(
      rl,
      getMessage("exertion_recurrent", languagePreference, bilingualMode),
      languagePreference,
      bilingualMode
    );
    sessionInputs.push(facts.recurrent_with_exertion.raw);
    facts.recurrent_with_exertion = facts.recurrent_with_exertion.value;

    facts = mergeProfileRisks(facts, profile);

    const snapshot = await generateSnapshot({ env: process.env });
    const result = classifyFastTriage(facts, { snapshot });
    const detectedLanguage = detectLanguageFromInputs(sessionInputs, languagePreference);
    const finalBilingualMode = bilingualMode;
    const rendered = renderResult(result, detectedLanguage, finalBilingualMode);

    output.write("\n");
    output.write(rendered.body + "\n");

    if (rendered.signals.length > 0) {
      output.write(`${getMessage("signal_label", detectedLanguage, finalBilingualMode)}：${rendered.signals.join("；")}\n`);
    }

    await appendEvent(
      {
        kind: "quick-triage",
        urgency: result.urgency,
        disposition: result.disposition,
        facts,
        result,
        snapshot_summary: {
          generated_at: snapshot.generated_at,
          overall_fatigue: snapshot.overall_fatigue,
          host: snapshot.host.host
        }
      },
      process.env
    );

    await saveConfig(
      {
        language_preference: detectedLanguage,
        last_detected_language: detectedLanguage,
        first_run_completed: true
      },
      process.env
    );

    output.write("\n" + getMessage("saved", detectedLanguage, finalBilingualMode) + "\n");
    output.write(
      `${getMessage(
        detectedLanguage === "en-US" ? "language_saved_en" : "language_saved_zh",
        detectedLanguage,
        finalBilingualMode
      )}\n`
    );
  } finally {
    rl.close();
  }
}

main().catch((error) => {
  if (error?.code === "ABORT_ERR") {
    process.exitCode = 130;
    return;
  }

  console.error(error);
  process.exitCode = 1;
});
