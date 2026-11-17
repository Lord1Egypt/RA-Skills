import path from "node:path";
import { addToken, emptyToken } from "./report-schema.mjs";
import { analyzePrompt, classifyCategory, summarizeActions } from "./prompt-analysis.mjs";

const GENERIC_DIRS = new Set([
  "", "desktop", "documents", "downloads", "workspace", "workspaces", "work", "projects",
  "project", "code", "repo", "repos", "src", "tmp", "temp", "home",
  "工作区", "项目", "新建文件夹",
]);

export function groupUsage({ sessions = [], artifacts = [], config = {} }) {
  const projects = new Map();
  const rules = normalizeRules(config.projectRules);
  const mainSessions = sessions.filter((item) => !item.isAuxiliary && !item.isSynthetic);
  const artifactAssignments = assignArtifacts(mainSessions, artifacts);

  for (const session of mainSessions) {
    const nearbyArtifacts = artifactAssignments.get(session.id) || [];
    const identity = inferIdentity(session, nearbyArtifacts, rules);
    const key = `${identity.name}::${identity.category}`;
    const project = ensureProject(projects, key, identity);
    project.minutes += Number(session.minutes || 0);
    project.sessionCount += 1;
    addToken(project.token, session.token);
    project._analyses.push(analyzePrompt(session.userMessages || [], identity.category));
    for (const artifact of nearbyArtifacts) {
      if (!project._artifactSet.has(artifact.relative)) {
        project._artifactSet.add(artifact.relative);
        project.artifacts.push(artifact);
      }
    }
  }

  for (const artifact of artifacts) {
    if ([...artifactAssignments.values()].some((items) => items.includes(artifact))) continue;
    const identity = inferArtifactIdentity(artifact, rules);
    const key = `${identity.name}::${identity.category}`;
    const project = ensureProject(projects, key, identity);
    if (!project._artifactSet.has(artifact.relative)) {
      project._artifactSet.add(artifact.relative);
      project.artifacts.push(artifact);
    }
  }

  return [...projects.values()].map(finalizeProject).sort((a, b) => {
    if (b.minutes !== a.minutes) return b.minutes - a.minutes;
    return b.artifacts.length - a.artifacts.length;
  });
}

function assignArtifacts(sessions, artifacts) {
  const assignments = new Map(sessions.map((session) => [session.id, []]));
  for (const artifact of artifacts) {
    const ranked = sessions
      .map((session) => ({ session, score: artifactScore(session, artifact) }))
      .filter((item) => item.score > 0)
      .sort((a, b) => b.score - a.score);
    if (ranked[0]) assignments.get(ranked[0].session.id).push(artifact);
  }
  return assignments;
}

function artifactScore(session, artifact) {
  const modified = new Date(artifact.modifiedAt).getTime();
  if (!Number.isFinite(modified)) return 0;
  const activityTimes = Array.isArray(session.activityTimes) ? session.activityTimes : [];
  const distance = activityTimes.length
    ? Math.min(...activityTimes.map((time) => Math.abs(modified - time)))
    : Math.abs(modified - new Date(session.end).getTime());

  const relative = String(artifact.relative || "");
  const top = relative.split(path.sep)[0];
  const text = `${session.title || ""}\n${(session.userMessages || []).join("\n")}\n${session.cwd || ""}`.toLowerCase();
  const mentionsTop = Boolean(top && text.includes(top.toLowerCase()));
  const cwdMatches = Boolean(session.cwd && path.resolve(session.cwd).endsWith(path.sep + top));
  const mentionsPath = Boolean(relative && text.includes(relative.toLowerCase()));
  if (!mentionsTop && !cwdMatches && !mentionsPath && distance > 30 * 60 * 1000) return 0;
  if ((mentionsTop || cwdMatches || mentionsPath) && distance > 36 * 60 * 60 * 1000) return 0;

  let score = Math.max(1, 100 - distance / (5 * 60 * 1000));
  if (mentionsTop) score += 240;
  if (cwdMatches) score += 300;
  if (mentionsPath) score += 360;
  return score;
}

export function normalizeRules(value) {
  if (!Array.isArray(value)) return [];
  return value
    .filter((rule) => rule && typeof rule.name === "string" && Array.isArray(rule.patterns))
    .map((rule) => ({
      name: rule.name.trim(),
      category: typeof rule.category === "string" ? rule.category.trim() : "",
      patterns: rule.patterns.map((item) => String(item).trim().toLowerCase()).filter(Boolean),
    }))
    .filter((rule) => rule.name && rule.patterns.length);
}

function inferIdentity(session, artifacts, rules) {
  const text = `${session.title || ""}\n${(session.userMessages || []).join("\n")}\n${session.cwd || ""}\n${artifacts.map((item) => item.relative).join("\n")}`;
  const custom = matchRule(text, rules);
  const inferredCategory = classifyCategory(text, artifacts);
  const category = custom?.category
    || (inferredCategory === "其他任务" ? artifacts.map(artifactCategory).find(Boolean) : inferredCategory)
    || "其他任务";
  if (custom) {
    return { name: custom.name, category, confidence: "high", evidence: ["匹配工作区自定义项目规则"] };
  }

  const cwdName = usefulName(path.basename(session.cwd || ""));
  if (cwdName) {
    return { name: cwdName, category, confidence: "high", evidence: [`来自工作目录：${cwdName}`] };
  }

  const artifactName = topArtifactDirectory(artifacts);
  if (artifactName) {
    return { name: artifactName, category, confidence: "medium", evidence: [`来自产物目录：${artifactName}`] };
  }

  const title = usefulTitle(session.title || "");
  if (title) {
    return { name: title, category, confidence: "medium", evidence: ["来自会话标题"] };
  }

  return {
    name: category === "其他任务" ? "零散任务" : category,
    category,
    confidence: "low",
    evidence: ["未识别到稳定项目名，按任务内容归类"],
  };
}

function inferArtifactIdentity(artifact, rules) {
  const custom = matchRule(artifact.relative, rules);
  const category = custom?.category || artifactCategory(artifact) || classifyCategory(artifact.relative, [artifact]);
  if (custom) return { name: custom.name, category, confidence: "high", evidence: ["产物路径匹配自定义项目规则"] };
  const top = usefulName(String(artifact.relative || "").split(path.sep)[0]);
  if (top) return { name: top, category, confidence: "medium", evidence: [`来自产物目录：${top}`] };
  return {
    name: category === "其他任务" ? "待确认项目" : category,
    category,
    confidence: "low",
    evidence: ["仅识别到产物类型，缺少稳定项目名"],
  };
}

function artifactCategory(artifact) {
  const ext = path.extname(String(artifact.relative || "")).toLowerCase();
  if ([".mjs", ".js", ".jsx", ".ts", ".tsx", ".py", ".sh"].includes(ext)) return "代码开发";
  if ([".xlsx", ".xls", ".csv"].includes(ext)) return "数据与表格";
  if ([".png", ".jpg", ".jpeg", ".webp"].includes(ext)) return "视觉素材";
  if ([".md", ".docx", ".pptx", ".pdf"].includes(ext)) return "文档与内容";
  return "";
}

function ensureProject(projects, key, identity) {
  if (!projects.has(key)) {
    projects.set(key, {
      name: identity.name,
      category: identity.category,
      confidence: identity.confidence,
      evidence: [...identity.evidence],
      minutes: 0,
      sessionCount: 0,
      token: emptyToken(),
      artifacts: [],
      _artifactSet: new Set(),
      _analyses: [],
    });
  } else {
    const project = projects.get(key);
    project.evidence.push(...identity.evidence);
    if (confidenceRank(identity.confidence) > confidenceRank(project.confidence)) project.confidence = identity.confidence;
  }
  return projects.get(key);
}

function finalizeProject(project) {
  const analysis = aggregatePromptAnalyses(project._analyses, project.category);
  const artifacts = project.artifacts.sort((a, b) => String(b.modifiedAt).localeCompare(String(a.modifiedAt)));
  return {
    name: project.name,
    category: project.category,
    confidence: project.confidence,
    evidence: [...new Set(project.evidence)].slice(0, 3),
    minutes: project.minutes,
    sessionCount: project.sessionCount,
    token: project.token,
    artifacts,
    actions: summarizeActions({ sessionCount: project.sessionCount, artifacts, category: project.category }),
    promptAssessment: analysis.promptAssessment,
    issue: analysis.promptAssessment.summary,
    nextPrompt: analysis.nextPrompt,
    level: analysis.level,
  };
}

function aggregatePromptAnalyses(analyses, category) {
  if (!analyses.length) return analyzePrompt([], category);
  const signalKeys = Object.keys(analyses[0].promptAssessment.signals || {});
  const signalCounts = Object.fromEntries(signalKeys.map((key) => [key, 0]));
  const missingCounts = new Map();
  let correctionCount = 0;
  for (const analysis of analyses) {
    for (const [key, value] of Object.entries(analysis.promptAssessment.signals || {})) {
      if (value) signalCounts[key] = (signalCounts[key] || 0) + 1;
    }
    for (const label of analysis.promptAssessment.missing || []) {
      missingCounts.set(label, (missingCounts.get(label) || 0) + 1);
    }
    correctionCount += Number(analysis.promptAssessment.correctionCount || 0);
  }
  const signals = Object.fromEntries(signalKeys.map((key) => [key, signalCounts[key] / analyses.length >= 0.5]));
  const rankedMissing = [...missingCounts.entries()].sort((a, b) => b[1] - a[1]);
  const missing = rankedMissing.filter(([, count]) => count / analyses.length >= 0.5).map(([label]) => label);
  const mainMissing = missing.length ? missing : rankedMissing.slice(0, 3).map(([label]) => label);
  const completeSessions = analyses.filter((item) => item.level === "green").length;
  const redSessions = analyses.filter((item) => item.level === "red").length;
  const level = redSessions / analyses.length >= 0.5
    ? "red"
    : completeSessions / analyses.length >= 0.5 && correctionCount <= analyses.length
      ? "green"
      : "yellow";
  const summary = mainMissing.length
    ? `${analyses.length} 个会话中，最常缺少${mainMissing.slice(0, 3).join("、")}。${correctionCount ? ` 后续共检测到 ${correctionCount} 次方向或约束修正。` : ""}`.trim()
    : `${analyses.length} 个会话的首条请求整体覆盖了主要目标、边界和验收信息。`;
  return {
    promptAssessment: { signals, missing: mainMissing, correctionCount, summary },
    level,
    nextPrompt: analyses[0].nextPrompt,
  };
}

function matchRule(text, rules) {
  const haystack = String(text || "").toLowerCase();
  return rules.find((rule) => rule.patterns.some((pattern) => haystack.includes(pattern)));
}

function topArtifactDirectory(artifacts) {
  const counts = new Map();
  for (const artifact of artifacts) {
    const first = String(artifact.relative || "").split(path.sep)[0];
    const name = usefulName(first);
    if (name) counts.set(name, (counts.get(name) || 0) + 1);
  }
  return [...counts.entries()].sort((a, b) => b[1] - a[1])[0]?.[0] || "";
}

function usefulName(value) {
  const name = String(value || "").trim().replace(/^[-_.\s]+|[-_.\s]+$/g, "");
  if (!name || name.length < 2 || name.length > 60) return "";
  if (GENERIC_DIRS.has(name.toLowerCase())) return "";
  if (/工作区$|workspace$/i.test(name)) return "";
  if (/^users?$|^[a-f0-9]{16,}$/i.test(name)) return "";
  return name;
}

function usefulTitle(value) {
  const title = String(value || "").trim().replace(/\s+/g, " ");
  if (!title || title.length < 2 || title.length > 60) return "";
  if (/[。！？!?]$/.test(title) || /请|帮我|怎么|如何|为什么/.test(title)) return "";
  return title;
}

function confidenceRank(value) {
  return ({ low: 1, medium: 2, high: 3 })[value] || 0;
}
