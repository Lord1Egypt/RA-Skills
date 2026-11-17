#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";
import { spawnSync } from "node:child_process";
import { fileURLToPath, pathToFileURL } from "node:url";
import { formatUserError, userError } from "./core/diagnostics.mjs";
import { normalizeReport, validateReport } from "./core/report-schema.mjs";

const args = parseArgs(process.argv.slice(2));

if (args.help) {
  printHelp();
  process.exit(0);
}

try {
  if (!args.input) throw userError("缺少扫描结果", "请通过 --input 指定扫描生成的 JSON 文件。");
  const input = path.resolve(args.input);
  const output = path.resolve(args.output || input.replace(/\.json$/i, ".html"));
  const scriptDir = path.dirname(fileURLToPath(import.meta.url));
  const skillDir = path.resolve(args.skillDir || path.join(scriptDir, ".."));
  const templatePath = path.resolve(args.template || path.join(skillDir, "assets", "report_template.html"));
  const report = normalizeReport(readJson(input));
  const errors = validateReport(report);
  if (errors.length) {
    throw userError("扫描结果格式不完整", "请重新运行 scan_usage.mjs 后再生成报告。", errors.join("；"));
  }
  const template = readText(templatePath, "报告模板不存在", "请确认 skill 的 assets/report_template.html 文件完整。");
  const html = renderReport(report, template);
  writeText(output, html);

  const shouldOpen = args.open !== false && args["no-open"] !== true;
  const openResult = shouldOpen ? openReport(output) : { opened: false, attempted: false };
  console.log(JSON.stringify({
    output,
    ...openResult,
    projectCount: report.projects.length,
    totalMinutes: report.summary?.totalMinutes || 0,
    totalToken: report.summary?.totalToken || {},
  }, null, 2));
} catch (error) {
  console.error(formatUserError(error, "无法生成 Codex 使用报告"));
  process.exit(1);
}

function renderReport(report, template) {
  const projects = report.projects || [];
  const summary = report.summary || {};
  const totalMinutes = Number(summary.totalMinutes || 0);
  const totalToken = summary.totalToken || {};
  const artifactCount = Number(summary.artifactCount || 0);
  const generatedAt = new Date(report.generatedAt || Date.now()).toLocaleString("zh-CN");
  const dateRange = `最近 ${report.range?.days || 7} 天`;
  const promptStats = collectPromptStats(projects);
  const dominant = projects[0];
  const primaryGap = promptStats.missing[0]?.label || "验收标准";
  const oneLine = dominant
    ? `本周主要投入在「${dominant.name}」（${formatMinutes(dominant.minutes)}），形成 ${artifactCount} 个可识别产物；下周最值得先补的是${primaryGap}。`
    : "本周没有读取到足够的使用记录，建议扩大时间范围后重新扫描。";

  const taskTypes = groupTaskTypes(projects);
  const projectRows = projects.map((project) => {
    const share = percent(project.minutes, totalMinutes);
    return `<tr>
      <td><strong>${esc(project.name)}</strong><div class="small">${esc(project.category)}</div></td>
      <td class="size">${esc(timeLabel(project))}</td>
      <td>${share}%<div class="bar"><i style="width:${share}%"></i></div></td>
      <td class="size">${formatNumber(project.token?.total_tokens)}</td>
      <td><span class="tag ${esc(project.level)}">${levelLabel(project.level)}</span> ${esc(shortIssue(project))}</td>
    </tr>`;
  }).join("");

  const taskTypeRows = taskTypes.map((item) => {
    const share = percent(item.minutes, totalMinutes);
    return `<tr>
      <td><span class="tag blue">${esc(item.category)}</span></td>
      <td class="size">${esc(formatMinutes(item.minutes))}</td>
      <td>${share}%<div class="bar"><i style="width:${share}%"></i></div></td>
      <td>${item.sessions}</td>
      <td>${item.artifacts}</td>
    </tr>`;
  }).join("");

  const projectDetails = projects.map((project, index) => renderProject(project, index)).join("");
  const promptDiagnosis = renderPromptDiagnosis(promptStats);
  const habits = buildHabits(projects, promptStats);
  const profile = buildProfile(projects, totalMinutes, artifactCount);
  const promptTemplates = uniquePromptTemplates(projects).map((item) => `
    <div class="prompt-item">
      <div class="prompt-head"><strong>${esc(item.category)}</strong><button class="copy" type="button">复制</button></div>
      <div class="prompt">${esc(item.text)}</div>
    </div>`).join("");
  const reuseItems = buildReuseSuggestions(projects).map((item, index) => `
    <div class="reuse-item"><span class="step">${index + 1}</span><div><strong>${esc(item.title)}</strong><p>${esc(item.text)}</p></div></div>`).join("");
  const diagnostics = renderDiagnostics(report.diagnostics || []);

  const content = `
<section class="insight"><span class="eyebrow">本周结论</span><strong>${esc(oneLine)}</strong></section>

<h2>总览</h2>
<section class="grid metrics">
  <div class="card"><div class="k"><span title="按会话内活跃时间片段估算，相邻活动间隔最多计 15 分钟。">估算活跃时长</span></div><div class="v">${esc(formatMinutes(totalMinutes))}</div></div>
  <div class="card"><div class="k">主要项目</div><div class="v">${projects.length}</div></div>
  <div class="card"><div class="k">可识别产物</div><div class="v">${formatNumber(artifactCount)}</div></div>
  <div class="card"><div class="k">Token 大致消耗</div><div class="v">${formatNumber(totalToken.total_tokens)}</div></div>
</section>

<h2>效率信号</h2>
<section class="grid metrics">
  <div class="card"><div class="k">提问完整度</div><div class="score ${scoreTone(promptStats.clarity)}">${promptStats.clarity}%</div><div class="note">首条请求覆盖目标、范围、输入、约束、验收和验证</div></div>
  <div class="card"><div class="k">方向修正</div><div class="score ${promptStats.corrections > 4 ? "warn" : "good"}">${promptStats.corrections} 次</div><div class="note">后续出现“改成、不要、遗漏”等调整</div></div>
  <div class="card"><div class="k">产物覆盖</div><div class="score ${scoreTone(promptStats.artifactCoverage)}">${promptStats.artifactCoverage}%</div><div class="note">有文件产物的项目占比</div></div>
  <div class="card"><div class="k">主要会话</div><div class="score good">${formatNumber(summary.mainSessionCount)}</div><div class="note">已排除辅助线程和明显测试任务</div></div>
</section>

<h2>Token 使用</h2>
<section class="grid metrics">
  <div class="card"><div class="k">总量</div><div class="v">${formatNumber(totalToken.total_tokens)}</div></div>
  <div class="card"><div class="k">输入</div><div class="v">${formatNumber(totalToken.input_tokens)}</div></div>
  <div class="card"><div class="k">输出</div><div class="v">${formatNumber(totalToken.output_tokens)}</div></div>
  <div class="card"><div class="k">思考</div><div class="v">${formatNumber(totalToken.reasoning_output_tokens)}</div></div>
</section>

<h2>任务分布</h2>
<div class="table-wrap"><table><thead><tr><th>类型</th><th>耗时</th><th>占比</th><th>会话</th><th>产物</th></tr></thead><tbody>${taskTypeRows}</tbody></table></div>

<h2>项目投入</h2>
<div class="table-wrap"><table><thead><tr><th>项目</th><th>耗时</th><th>占比</th><th>Token</th><th>观察</th></tr></thead><tbody>${projectRows}</tbody></table></div>

<h2>项目复盘</h2>
${projectDetails || '<section class="empty">本周没有足够的项目数据。</section>'}

<h2>Prompt 诊断</h2>
${promptDiagnosis}

<h2>本周协作方式</h2>
<section class="profile-grid">${habits}</section>

<h2>使用画像</h2>
<section class="profile-grid">${profile}</section>

<h2>下周可复制 Prompt</h2>
<section class="prompt-list">${promptTemplates || '<div class="empty">当前没有足够数据生成模板。</div>'}</section>

<h2>可复用机会</h2>
<section class="reuse-list">${reuseItems || '<div class="empty">本周暂无明显需要沉淀的重复流程。</div>'}</section>

${diagnostics}`;

  return template
    .replaceAll("{{title}}", "Codex 使用复盘")
    .replaceAll("{{date_range}}", dateRange)
    .replaceAll("{{generated_at}}", generatedAt)
    .replace("{{content}}", content);
}

function renderProject(project, index) {
  const artifacts = project.artifacts || [];
  const visible = artifacts.slice(0, 3);
  const hidden = artifacts.slice(3);
  const missing = project.promptAssessment?.missing || [];
  const next = missing.length ? missing.slice(0, 3).join("、") : "保持当前目标和验收表达";
  const artifactHtml = visible.length
    ? `<ul>${visible.map((item) => `<li>${esc(item.relative)}</li>`).join("")}</ul>${hidden.length ? `<details class="artifact-more"><summary>查看其余 ${hidden.length} 个产物</summary><ul>${hidden.map((item) => `<li>${esc(item.relative)}</li>`).join("")}</ul></details>` : ""}`
    : '<p class="small">主要成果保留在对话结论中。</p>';
  return `<details class="project ${esc(project.level)}" ${index < 3 ? "open" : ""}>
    <summary><span class="summary-name">${esc(project.name)}</span><span class="summary-sub">${esc(timeLabel(project))} · ${project.sessionCount || 0} 个会话</span></summary>
    <div class="project-body">
      <div class="project-grid">
        <section><h3>做了什么</h3><ul>${(project.actions || []).map((item) => `<li>${esc(item)}</li>`).join("")}</ul></section>
        <section><h3>关键产物</h3>${artifactHtml}</section>
        <section class="project-observation"><h3>效率观察</h3><p>${esc(project.promptAssessment?.summary || project.issue || "本周没有明显异常。")}</p></section>
        <section class="project-next"><h3>下次先补</h3><p><strong>${esc(next)}</strong></p></section>
      </div>
    </div>
  </details>`;
}

function collectPromptStats(projects) {
  const counts = new Map();
  let present = 0;
  let signalTotal = 0;
  let corrections = 0;
  for (const project of projects) {
    const assessment = project.promptAssessment || {};
    for (const value of Object.values(assessment.signals || {})) {
      signalTotal += 1;
      if (value) present += 1;
    }
    for (const label of assessment.missing || []) counts.set(label, (counts.get(label) || 0) + 1);
    corrections += Number(assessment.correctionCount || 0);
  }
  const projectsWithArtifacts = projects.filter((project) => (project.artifacts || []).length).length;
  return {
    clarity: signalTotal ? Math.round((present / signalTotal) * 100) : 0,
    corrections,
    artifactCoverage: projects.length ? Math.round((projectsWithArtifacts / projects.length) * 100) : 0,
    missing: [...counts.entries()].map(([label, count]) => ({ label, count })).sort((a, b) => b.count - a.count),
  };
}

function renderPromptDiagnosis(stats) {
  const items = stats.missing.slice(0, 4);
  if (!items.length) return '<section class="callout action"><strong>本周首条请求整体完整。</strong><p>继续保持先定义交付物、边界和验收方式的习惯。</p></section>';
  return `<section class="diagnosis-list">${items.map((item, index) => `
    <div class="diagnosis-item"><span class="rank">${index + 1}</span><div><strong>${esc(item.label)}</strong><p>${item.count} 个项目的首条请求没有覆盖。下次在开头直接写清这一项。</p></div></div>`).join("")}</section>`;
}

function buildHabits(projects, stats) {
  const best = [...projects].sort((a, b) => (b.artifacts?.length || 0) - (a.artifacts?.length || 0))[0];
  const missing = stats.missing[0]?.label || "验收标准";
  const keep = best?.artifacts?.length
    ? `「${best.name}」已经形成 ${best.artifacts.length} 个文件产物，说明你会把讨论继续推进到可交付结果。`
    : "本周主要通过对话解决问题，下一步可以增加文件化沉淀。";
  return [
    ["action", "继续保持", keep],
    ["warn", "优先调整", `第一条请求最常缺少${missing}，这会把关键判断推迟到后续轮次。`],
    ["info", "下周动作", `每个复杂任务开头先写五行：目标、输入、范围、不要做什么、完成标准。`],
  ].map(([tone, title, text]) => `<div class="callout ${tone}"><div class="label">${title}</div><p>${esc(text)}</p></div>`).join("");
}

function buildProfile(projects, totalMinutes, artifactCount) {
  const categories = groupTaskTypes(projects);
  const top = categories.slice(0, 2).map((item) => item.category).join("、") || "零散任务";
  const dominant = projects[0];
  const focus = dominant && totalMinutes ? Math.round((dominant.minutes / totalMinutes) * 100) : 0;
  return [
    ["info", "主要用途", `本周使用集中在${top}。`],
    ["action", "投入方式", dominant ? `最大项目是「${dominant.name}」，约占总活跃时长的 ${focus}%。` : "本周项目投入较分散。"],
    ["warn", "沉淀方式", artifactCount ? `共识别到 ${artifactCount} 个产物；优先把重复步骤继续固化为模板、脚本或 skill。` : "本周未识别到文件产物，重要结论容易只停留在对话里。"],
  ].map(([tone, title, text]) => `<div class="callout ${tone}"><div class="label">${title}</div><p>${esc(text)}</p></div>`).join("");
}

function buildReuseSuggestions(projects) {
  return projects.filter((project) => project.sessionCount > 1 || (project.artifacts || []).length > 2).slice(0, 4).map((project) => {
    const kind = project.category === "系统自动化"
      ? "自动化任务"
      : project.category === "Skill 与工具"
        ? "skill 或脚本"
        : project.category === "代码开发"
          ? "脚本、测试或项目规则"
          : "模板或固定流程";
    return {
      title: project.name,
      text: `本周有 ${project.sessionCount} 个会话、${project.artifacts?.length || 0} 个产物，适合沉淀为${kind}，减少下次重新解释。`,
    };
  });
}

function uniquePromptTemplates(projects) {
  const seen = new Set();
  const out = [];
  for (const project of projects) {
    if (!project.nextPrompt || seen.has(project.nextPrompt)) continue;
    seen.add(project.nextPrompt);
    out.push({ category: project.category, text: project.nextPrompt });
    if (out.length >= 3) break;
  }
  return out;
}

function groupTaskTypes(projects) {
  const grouped = new Map();
  for (const project of projects) {
    const key = project.category || "其他任务";
    if (!grouped.has(key)) grouped.set(key, { category: key, minutes: 0, sessions: 0, artifacts: 0 });
    const item = grouped.get(key);
    item.minutes += Number(project.minutes || 0);
    item.sessions += Number(project.sessionCount || 0);
    item.artifacts += Number(project.artifacts?.length || 0);
  }
  return [...grouped.values()].sort((a, b) => b.minutes - a.minutes);
}

function renderDiagnostics(diagnostics) {
  if (!diagnostics.length) return "";
  return `<details class="data-note"><summary>需要留意的数据问题（${diagnostics.length}）</summary><ul>${diagnostics.map((item) => `<li><strong>${esc(item.message)}</strong>${item.action ? ` ${esc(item.action)}` : ""}</li>`).join("")}</ul></details>`;
}

function shortIssue(project) {
  const missing = project.promptAssessment?.missing || [];
  if (!missing.length) return "首条请求较完整";
  return `缺少${missing.slice(0, 2).join("、")}`;
}

function levelLabel(level) {
  if (level === "green") return "保持";
  if (level === "red") return "优先改";
  return "可优化";
}

function scoreTone(score) {
  if (score >= 70) return "good";
  if (score >= 40) return "warn";
  return "bad";
}

function timeLabel(project) {
  if (!project.sessionCount && (!project.minutes || project.minutes < 1)) return "有产物记录";
  return formatMinutes(project.minutes);
}

function formatMinutes(value) {
  const minutes = Number(value || 0);
  if (minutes < 1) return "<1 分钟";
  const rounded = Math.round(minutes);
  const hours = Math.floor(rounded / 60);
  const rest = rounded % 60;
  return hours ? `${hours} 小时${rest ? ` ${rest} 分钟` : ""}` : `${rest} 分钟`;
}

function percent(value, total) {
  if (!total) return 0;
  return Math.max(0, Math.min(100, Math.round((Number(value || 0) / total) * 100)));
}

function formatNumber(value) {
  return Number(value || 0).toLocaleString("zh-CN");
}

function esc(value) {
  return String(value ?? "").replace(/[&<>"]/g, (char) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;",
  })[char]);
}

function readJson(file) {
  const text = readText(file, "扫描结果不存在", "请先运行 scan_usage.mjs，或检查 --input 路径。");
  try {
    return JSON.parse(text);
  } catch (error) {
    throw userError("扫描结果已损坏", "请重新运行 scan_usage.mjs 生成新的 JSON 文件。", `${file}: ${error.message}`);
  }
}

function readText(file, message, action) {
  try {
    return fs.readFileSync(file, "utf8");
  } catch (error) {
    throw userError(message, action, `${file}: ${error.message}`);
  }
}

function writeText(file, value) {
  try {
    fs.mkdirSync(path.dirname(file), { recursive: true });
    fs.writeFileSync(file, value);
  } catch (error) {
    throw userError("报告无法写入", "请换一个有写入权限的 --output 路径。", `${file}: ${error.message}`);
  }
}

function parseArgs(argv) {
  const out = {};
  for (let index = 0; index < argv.length; index += 1) {
    const arg = argv[index];
    if (!arg.startsWith("--")) continue;
    const key = arg.slice(2);
    const next = argv[index + 1];
    if (!next || next.startsWith("--")) out[key] = true;
    else {
      out[key] = next;
      index += 1;
    }
  }
  return out;
}

function openReport(file) {
  const fileUrl = pathToFileURL(file).href;
  const attempts = process.platform === "darwin"
    ? [["open", file], ["open", "-a", "Google Chrome", file], ["open", "-a", "Safari", file], ["agent-browser", "open", fileUrl]]
    : process.platform === "win32"
      ? [["cmd", "/c", "start", "", fileUrl]]
      : [["xdg-open", fileUrl]];
  const errors = [];
  for (const [command, ...commandArgs] of attempts) {
    const result = spawnSync(command, commandArgs, { encoding: "utf8" });
    const openCommand = [command, ...commandArgs].join(" ");
    if (result.status === 0 && !result.error) return { opened: true, attempted: true, openCommand };
    errors.push(result.error?.message || result.stderr?.trim() || `${openCommand} exited with ${result.status}`);
  }
  return { opened: false, attempted: true, openError: errors.join(" | ") };
}

function printHelp() {
  console.log(`Codex Review 报告生成工具

用法：
  node scripts/build_report.mjs --input <scan.json> [选项]

选项：
  --output <文件>     HTML 输出路径，默认与输入文件同名
  --template <文件>   自定义 HTML 模板
  --no-open           只生成文件，不自动打开
  --help              查看帮助
`);
}
