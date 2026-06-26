function hasAny(value) {
  return Array.isArray(value) && value.length > 0;
}

function countTrue(values) {
  return values.filter(Boolean).length;
}

export function createEmptyTriageFacts() {
  return {
    subject_role: "self",
    symptoms_active_now: null,
    chest_discomfort: null,
    chest_pressure_or_tightness: null,
    pain_duration_minutes: null,
    pain_started_at_rest: null,
    getting_worse: null,
    shortness_of_breath: null,
    sweating: null,
    nausea_or_vomiting: null,
    dizziness_or_faintness: null,
    radiation_sites: [],
    jaw_or_tooth_pain: null,
    pain_worse_with_pressing_on_chest: null,
    pain_worse_with_breathing_or_movement: null,
    recurrent_with_exertion: null,
    known_angina_pattern_changed: null,
    hypertension: null,
    diabetes: null,
    smoking: null,
    high_cholesterol: null,
    family_history_early_heart_disease: null,
    age_risk: null,
    prior_heart_disease: null
  };
}

function deriveEmergencyReasons(facts) {
  const reasons = [];
  const hasChestPattern =
    facts.chest_discomfort === true ||
    facts.chest_pressure_or_tightness === true ||
    facts.jaw_or_tooth_pain === true;
  const associatedCount = countTrue([
    facts.shortness_of_breath,
    facts.sweating,
    facts.nausea_or_vomiting,
    facts.dizziness_or_faintness
  ]);

  if (facts.symptoms_active_now && hasChestPattern && facts.pain_duration_minutes >= 15) {
    reasons.push("当前胸痛或胸闷已经持续 15 分钟以上。");
  }

  if (facts.symptoms_active_now && hasChestPattern && hasAny(facts.radiation_sites)) {
    reasons.push("疼痛或压迫感正在往胸口以外的部位放射。");
  }

  if (facts.symptoms_active_now && hasChestPattern && associatedCount >= 1) {
    reasons.push("胸部症状同时伴有气短、出汗、恶心或头晕等危险信号。");
  }

  if (facts.symptoms_active_now && hasChestPattern && facts.pain_started_at_rest) {
    reasons.push("症状是在休息或很轻的活动时出现的。");
  }

  if (facts.symptoms_active_now && hasChestPattern && facts.getting_worse) {
    reasons.push("症状没有缓解，反而在加重或反复出现。");
  }

  if (facts.known_angina_pattern_changed && hasChestPattern) {
    reasons.push("已知心绞痛的发作模式发生了变化。");
  }

  return reasons;
}

function deriveUrgentReasons(facts, snapshot) {
  const reasons = [];
  const riskCount = countTrue([
    facts.hypertension,
    facts.diabetes,
    facts.smoking,
    facts.high_cholesterol,
    facts.family_history_early_heart_disease,
    facts.age_risk,
    facts.prior_heart_disease
  ]);

  if (facts.recurrent_with_exertion) {
    reasons.push("活动或爬楼时容易反复出现不适。");
  }

  if (facts.chest_discomfort || facts.jaw_or_tooth_pain) {
    reasons.push("胸口、下巴或牙根样不适仍需要当天就医评估。");
  }

  if (riskCount >= 2) {
    reasons.push("同时存在多个心血管危险因素。");
  }

  if (snapshot?.overall_fatigue === "high") {
    reasons.push("近期工作和休息模式提示疲劳或睡眠明显不足。");
  }

  if (facts.pain_worse_with_pressing_on_chest === false && facts.chest_discomfort) {
    reasons.push("按压胸口不能明确复现这种疼痛。");
  }

  return reasons;
}

function deriveLaySignals(facts) {
  const laySignals = [];

  if (facts.chest_pressure_or_tightness) {
    laySignals.push("描述更像压着、发紧、发闷、像被攥住，不像单纯针扎一下。");
  }

  if (hasAny(facts.radiation_sites)) {
    laySignals.push("不适正在往后背、手臂、脖子或下巴这些部位放。");
  }

  if (facts.jaw_or_tooth_pain) {
    laySignals.push("下巴痛或像牙疼一样的感觉，也可能是同一组心脏危险信号。");
  }

  if (facts.pain_worse_with_pressing_on_chest) {
    laySignals.push("按压更痛可以像肌肉或肋软骨问题，但单凭这一点不能排除心脏风险。");
  }

  return laySignals;
}

export function classifyFastTriage(facts, options = {}) {
  const snapshot = options.snapshot ?? null;
  const emergencyReasons = deriveEmergencyReasons(facts);
  const urgentReasons = deriveUrgentReasons(facts, snapshot);
  const laySignals = deriveLaySignals(facts);

  if (emergencyReasons.length > 0) {
    return {
      urgency: "red",
      disposition: "call_emergency_now",
      confidence: "high",
      reasoning_summary: emergencyReasons,
      lay_signal_summary: laySignals,
      recommended_action:
        facts.subject_role === "other"
          ? "现在立刻呼救，让对方停止活动，不要让对方自己去医院或单独行动。"
          : "现在立刻呼救，停止走动，如果安全就先把门打开，不要自己开车。"
    };
  }

  return {
    urgency: "yellow",
    disposition: "urgent_medical_review",
    confidence: urgentReasons.length >= 2 ? "medium" : "low",
    reasoning_summary:
      urgentReasons.length > 0
        ? urgentReasons
        : ["现有信息还不能排除心脏方面的危险。"],
    lay_signal_summary: laySignals,
    recommended_action:
      "今天尽快就医。如果胸痛持续、加重，或开始出现气短、出汗、头晕等情况，立刻升级为呼救。"
  };
}

export function buildQuickModeQuestions() {
  return [
    "现在胸口还在不舒服吗？",
    "更像是压着、勒着、发紧、胸口被攥一下，还是像针扎、按一下就疼？",
    "有没有往左臂、后背、脖子、下巴，或者像牙疼那样往牙床放过去？",
    "已经持续多久了，是几秒、几分钟，还是超过 15 分钟？",
    "有没有喘不过气、出冷汗、恶心、头晕，或者快要晕倒？",
    "按压胸口那个位置，会不会更明显地疼？",
    "这是你自己，还是你正在帮别人判断？"
  ];
}
