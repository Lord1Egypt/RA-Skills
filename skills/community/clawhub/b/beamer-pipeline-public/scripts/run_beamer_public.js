#!/usr/bin/env node
"use strict";

const fs = require("node:fs");
const path = require("node:path");
const { spawnSync } = require("node:child_process");
const {
  DECK_PIPELINE_PHASE_BLUEPRINTS,
  DECK_PIPELINE_TOTAL_PHASES,
  getBeamerPipelinePhase,
  phaseAllowsPlannedCoverageField,
  requiredArtifactNamesForPhase,
  summarizePhase,
} = require("./beamer_phase_blueprint");

const DEFAULT_AGENT_CMD = "openclaw agent --agent {role} --message \"$(cat {prompt})\"";

function fail(message) {
  process.stderr.write(`${message}\n`);
  process.exit(1);
}

function parseArgs(argv) {
  const options = {
    input: "",
    out: "",
    skipAssets: false,
    dryRun: false,
    initOnly: false,
    noAgent: false,
    phase: 0,
    validatePhase: 0,
    agentCmd: "",
    latexCmd: process.env.LATEXMK_BIN || "latexmk",
  };
  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    const readNext = () => {
      const value = argv[i + 1];
      if (!value || String(value).startsWith("--")) fail(`missing value for ${arg}`);
      i += 1;
      return value;
    };
    if (arg === "--input") {
      options.input = readNext();
    } else if (arg === "--out") {
      options.out = readNext();
    } else if (arg === "--skip-assets") {
      options.skipAssets = true;
    } else if (arg === "--dry-run") {
      options.dryRun = true;
    } else if (arg === "--init-only") {
      options.initOnly = true;
    } else if (arg === "--no-agent") {
      options.noAgent = true;
    } else if (arg === "--phase") {
      options.phase = Number(readNext());
    } else if (arg === "--validate-phase") {
      options.validatePhase = Number(readNext());
    } else if (arg === "--agent-cmd") {
      options.agentCmd = readNext();
    } else if (arg === "--latex-cmd") {
      options.latexCmd = readNext();
    } else if (arg === "--help" || arg === "-h") {
      printHelp();
      process.exit(0);
    } else {
      fail(`unknown argument: ${arg}`);
    }
  }
  if (!options.input || !options.out) {
    printHelp();
    process.exit(1);
  }
  return {
    ...options,
    input: path.resolve(options.input),
    out: path.resolve(options.out),
  };
}

function printHelp() {
  process.stdout.write([
    "usage: node scripts/run_beamer_public.js --input <paper.md> --out <output-dir> [options]",
    "",
    "Options:",
    "  --init-only              prepare workspace/contract/assets only",
    "  --dry-run                print the 7-phase plan and required artifacts without invoking an agent",
    "  --no-agent               write prompts only, skip all agent invocations (for inspection)",
    "  --phase <1-7>            run exactly one phase",
    "  --validate-phase <2-6>   validate existing artifacts for one phase gate",
    "  --agent-cmd <command>    command used to produce/repair artifacts for each phase (default: openclaw agent --agent {role} --message \"$(cat {prompt})\")",
    "                           placeholders: {prompt} {phase} {phaseName} {role} {out} {input}",
    "  --latex-cmd <command>    LaTeX command for phase 5, default: LATEXMK_BIN or latexmk",
    "  --skip-assets            skip prepare_task_assets.js",
    "",
    "Examples:",
    "  node scripts/run_beamer_public.js --input paper.md --out out --dry-run",
    "  node scripts/run_beamer_public.js --input paper.md --out out --no-agent",
    "  node scripts/run_beamer_public.js --input paper.md --out out",
    "  node scripts/run_beamer_public.js --input paper.md --out out --agent-cmd 'openclaw agent --agent {role} --message \"$(cat {prompt})\"'",
    "  node scripts/run_beamer_public.js --input paper.md --out out --validate-phase 5",
  ].join("\n") + "\n");
}

function ensureDir(dir) {
  fs.mkdirSync(dir, { recursive: true });
}

function readText(filePath) {
  return fs.readFileSync(filePath, "utf8");
}

function writeText(filePath, content) {
  ensureDir(path.dirname(filePath));
  fs.writeFileSync(filePath, content, "utf8");
}

function readJson(filePath) {
  return JSON.parse(readText(filePath));
}

function fileExists(filePath) {
  return fs.existsSync(filePath) && fs.statSync(filePath).isFile();
}

function dirExists(dirPath) {
  return fs.existsSync(dirPath) && fs.statSync(dirPath).isDirectory();
}

function shellQuote(value) {
  return `'${String(value).replace(/'/g, `'\\''`)}'`;
}

function runPrepareAssets(skillRoot, input, out) {
  const script = path.join(skillRoot, "scripts", "prepare_task_assets.js");
  const result = spawnSync(process.execPath, [script, input, out, "--mode", "beamer"], {
    encoding: "utf8",
    stdio: ["ignore", "pipe", "pipe"],
    maxBuffer: 10 * 1024 * 1024,
  });
  if (result.status !== 0) {
    fail((result.stderr || result.stdout || "prepare_task_assets.js failed").trim());
  }
  return result.stdout.trim();
}

function workspacePaths(out) {
  return {
    analysis: path.join(out, "analysis.json"),
    slides: path.join(out, "slides.json"),
    mainTex: path.join(out, "main.tex"),
    mainPdf: path.join(out, "main.pdf"),
    readme: path.join(out, "README.md"),
    assetManifest: path.join(out, "asset_manifest.json"),
    figures: path.join(out, "figures"),
    contract: path.join(out, "beamer_task_contract.md"),
    state: path.join(out, "beamer_pipeline_state.json"),
    phaseLog: path.join(out, "beamer_phase_log.jsonl"),
  };
}

function artifactPath(out, name) {
  const paths = workspacePaths(out);
  if (name === "analysis.json") return paths.analysis;
  if (name === "slides.json") return paths.slides;
  if (name === "main.tex") return paths.mainTex;
  if (name === "main.pdf") return paths.mainPdf;
  if (name === "README.md") return paths.readme;
  if (name === "asset_manifest.json") return paths.assetManifest;
  if (name === "figures") return paths.figures;
  return path.join(out, name);
}

function artifactExists(out, name) {
  const candidate = artifactPath(out, name);
  return name === "figures" ? dirExists(candidate) : fileExists(candidate);
}

function roleForPhase(phase) {
  if (phase.index <= 5) return "programmer";
  if (phase.index === 6) return "reviewer";
  if (phase.index === 7) return "tester";
  return "programmer";
}

function validateRequiredArtifacts(out, phase) {
  const missing = requiredArtifactNamesForPhase(phase).filter((name) => !artifactExists(out, name));
  return missing;
}

function validateJsonArtifacts(out, phase) {
  const errors = [];
  for (const name of ["analysis.json", "slides.json"]) {
    if (!requiredArtifactNamesForPhase(phase).includes(name) || !artifactExists(out, name)) continue;
    try {
      readJson(artifactPath(out, name));
    } catch (error) {
      errors.push(`${name} is not valid JSON: ${error.message}`);
    }
  }
  return errors;
}

function validateCoverageGates(out, phase) {
  const errors = [];
  const slidesPath = artifactPath(out, "slides.json");
  const analysisPath = artifactPath(out, "analysis.json");
  const readIfPresent = (filePath) => fileExists(filePath) ? readJson(filePath) : {};
  let slides = {};
  let analysis = {};
  try { slides = readIfPresent(slidesPath); } catch { slides = {}; }
  try { analysis = readIfPresent(analysisPath); } catch { analysis = {}; }

  const phaseIndex = Number(phase?.index || 0) || 0;
  const equationCoverage = Array.isArray(slides.equation_coverage) ? slides.equation_coverage
    : (Array.isArray(analysis.equation_coverage) ? analysis.equation_coverage : []);
  const notationCoverage = Array.isArray(slides.notation_coverage) ? slides.notation_coverage
    : (Array.isArray(analysis.notation_coverage) ? analysis.notation_coverage : []);

  if (phaseIndex >= 3 && !phaseAllowsPlannedCoverageField(phase, "equation_coverage")) {
    const unresolved = equationCoverage.filter((entry) => /^(planned|blocked|missing|partial)$/i.test(String(entry?.status || "")) || !Array.isArray(entry?.slide_ids) || entry.slide_ids.length === 0);
    if (unresolved.length > 0) errors.push(`equation_coverage has ${unresolved.length} unresolved entries after phase ${phaseIndex}`);
  }
  if (phaseIndex >= 4 && !phaseAllowsPlannedCoverageField(phase, "notation_coverage")) {
    const unresolved = notationCoverage.filter((entry) => /^(planned|blocked|missing|partial)$/i.test(String(entry?.status || "")) || !Array.isArray(entry?.first_defined_slide_ids) || entry.first_defined_slide_ids.length === 0 || entry.defined_on_first_visible_use !== true);
    if (unresolved.length > 0) errors.push(`notation_coverage has ${unresolved.length} unresolved entries after phase ${phaseIndex}`);
  }
  return errors;
}

function validatePhase(out, phase) {
  const errors = [];
  errors.push(...validateRequiredArtifacts(out, phase).map((name) => `missing required artifact: ${name}`));
  errors.push(...validateJsonArtifacts(out, phase));
  errors.push(...validateCoverageGates(out, phase));
  if (phase.index >= 5 && artifactExists(out, "main.tex") && artifactExists(out, "main.pdf")) {
    const texMtime = fs.statSync(artifactPath(out, "main.tex")).mtimeMs;
    const pdfMtime = fs.statSync(artifactPath(out, "main.pdf")).mtimeMs;
    if (pdfMtime + 1000 < texMtime) errors.push("main.pdf is older than main.tex; rerun LaTeX");
  }
  return errors;
}

function compileLatex(out, latexCmd) {
  if (!artifactExists(out, "main.tex")) return { skipped: true, reason: "main.tex missing" };
  const args = latexCmd === "latexmk"
    ? ["-pdf", "-xelatex", "-interaction=nonstopmode", "-halt-on-error", "main.tex"]
    : ["main.tex"];
  const result = spawnSync(latexCmd, args, {
    cwd: out,
    encoding: "utf8",
    stdio: ["ignore", "pipe", "pipe"],
    timeout: 120000,
    maxBuffer: 20 * 1024 * 1024,
  });
  return {
    skipped: false,
    status: result.status,
    stdout: result.stdout || "",
    stderr: result.stderr || "",
  };
}

function phasePrompt(input, out, phase) {
  return [
    `You are running the public Beamer seven-phase pipeline.`,
    `Phase: ${summarizePhase(phase)} (${phase.name})`,
    `Goal: ${phase.goal}`,
    `Input source: ${input}`,
    `Output directory: ${out}`,
    `Required artifacts for this phase: ${requiredArtifactNamesForPhase(phase).join(", ")}`,
    `Use beamer_task_contract.md as the contract. Preserve existing artifacts and update only the output directory.`,
    `Return or write artifacts on disk: analysis.json, slides.json, main.tex, main.pdf, README.md, asset_manifest.json, figures as required.`,
  ].join("\n");
}

function runAgentCommand(agentCmd, input, out, phase) {
  const promptPath = path.join(out, `phase_${phase.index}_${phase.name}_prompt.md`);
  writeText(promptPath, phasePrompt(input, out, phase));
  const command = agentCmd
    .replaceAll("{prompt}", shellQuote(promptPath))
    .replaceAll("{phase}", String(phase.index))
    .replaceAll("{phaseName}", phase.name)
    .replaceAll("{role}", roleForPhase(phase))
    .replaceAll("{out}", shellQuote(out))
    .replaceAll("{input}", shellQuote(input));
  const result = spawnSync(command, {
    shell: true,
    cwd: out,
    encoding: "utf8",
    stdio: ["ignore", "pipe", "pipe"],
    timeout: 0,
    maxBuffer: 50 * 1024 * 1024,
  });
  return {
    command,
    promptPath,
    status: result.status,
    stdout: result.stdout || "",
    stderr: result.stderr || "",
  };
}

function appendPhaseLog(out, entry) {
  writeText(path.join(out, ".keep"), "");
  fs.appendFileSync(workspacePaths(out).phaseLog, `${JSON.stringify({ at: new Date().toISOString(), ...entry })}\n`, "utf8");
}

function writeState(out, state) {
  writeText(workspacePaths(out).state, `${JSON.stringify(state, null, 2)}\n`);
}

function initializeWorkspace(skillRoot, options) {
  ensureDir(options.out);
  const contractPath = path.join(skillRoot, "templates", "beamer_contract.md");
  const contract = readText(contractPath);
  const sourceBase = path.basename(options.input);
  const paths = workspacePaths(options.out);

  let assetSummary = "asset preparation skipped by --skip-assets";
  if (!options.skipAssets) {
    assetSummary = runPrepareAssets(skillRoot, options.input, options.out) || "asset preparation completed";
  }

  writeText(paths.contract, `${contract}\n\n## Current task\n\nSource file: ${options.input}\nOutput directory: ${options.out}\nSource basename: ${sourceBase}\n\nUse the source file and generated asset_manifest.json to produce analysis.json, slides.json, main.tex, and main.pdf when feasible.\n`);

  if (!fileExists(paths.readme)) {
    writeText(paths.readme, `# Beamer package workspace\n\nSource file: ${options.input}\n\nOutput directory: ${options.out}\n\nAsset step: ${assetSummary}\n\nPipeline:\n${DECK_PIPELINE_PHASE_BLUEPRINTS.map((phase, index) => `${index + 1}. ${phase.name}: ${phase.goal}`).join("\n")}\n`);
  }

  return { paths, assetSummary };
}

function printDryRun(options) {
  process.stdout.write(`Beamer seven-phase dry run\ninput: ${options.input}\nout: ${options.out}\n\n`);
  for (let index = 1; index <= DECK_PIPELINE_TOTAL_PHASES; index += 1) {
    const phase = getBeamerPipelinePhase(index);
    process.stdout.write(`${summarizePhase(phase)}\n`);
    process.stdout.write(`  name: ${phase.name}\n`);
    process.stdout.write(`  goal: ${phase.goal}\n`);
    process.stdout.write(`  required: ${requiredArtifactNamesForPhase(phase).join(", ")}\n`);
    process.stdout.write(`  reviewerPhase: ${phase.reviewerPhase ? "true" : "false"}\n`);
    process.stdout.write(`  finalPhase: ${phase.finalPhase ? "true" : "false"}\n\n`);
  }
}

function runOnePhase(options, phase) {
  appendPhaseLog(options.out, { phase: phase.index, name: phase.name, event: "start" });
  if (phase.index === 5) {
    const compileResult = compileLatex(options.out, options.latexCmd);
    appendPhaseLog(options.out, { phase: phase.index, name: phase.name, event: "latex", result: compileResult.skipped ? compileResult : { status: compileResult.status } });
  }

  const effectiveAgentCmd = options.agentCmd || (!options.noAgent ? DEFAULT_AGENT_CMD : "");
  if (effectiveAgentCmd) {
    const agentResult = runAgentCommand(effectiveAgentCmd, options.input, options.out, phase);
    appendPhaseLog(options.out, { phase: phase.index, name: phase.name, event: "agent", command: agentResult.command, status: agentResult.status, promptPath: agentResult.promptPath });
    if (agentResult.status !== 0) {
      writeText(path.join(options.out, `phase_${phase.index}_${phase.name}_agent.stderr.log`), agentResult.stderr);
      writeText(path.join(options.out, `phase_${phase.index}_${phase.name}_agent.stdout.log`), agentResult.stdout);
      fail(`agent command failed in ${summarizePhase(phase)}; see phase logs in ${options.out}`);
    }
  } else {
    writeText(path.join(options.out, `phase_${phase.index}_${phase.name}_prompt.md`), phasePrompt(options.input, options.out, phase));
    appendPhaseLog(options.out, { phase: phase.index, name: phase.name, event: "prompt_written_no_agent" });
  }

  const errors = validatePhase(options.out, phase);
  appendPhaseLog(options.out, { phase: phase.index, name: phase.name, event: "validate", errors });
  if (errors.length > 0) {
    fail(`${summarizePhase(phase)} validation failed:\n- ${errors.join("\n- ")}`);
  }
  appendPhaseLog(options.out, { phase: phase.index, name: phase.name, event: "done" });
  return { phase: phase.index, name: phase.name, ok: true };
}

function main() {
  const options = parseArgs(process.argv.slice(2));
  if (!fs.existsSync(options.input)) fail(`input file not found: ${options.input}`);
  const skillRoot = path.resolve(__dirname, "..");
  const init = initializeWorkspace(skillRoot, options);

  if (options.dryRun) {
    printDryRun(options);
    return;
  }
  if (options.initOnly) {
    process.stdout.write([
      "Beamer public workspace prepared.",
      `input: ${options.input}`,
      `out: ${options.out}`,
      `contract: ${init.paths.contract}`,
      `readme: ${init.paths.readme}`,
      `assets: ${init.assetSummary}`,
    ].join("\n") + "\n");
    return;
  }
  if (options.validatePhase) {
    const phase = getBeamerPipelinePhase(options.validatePhase);
    if (phase.index < 2 || phase.index > 6) fail("--validate-phase currently supports phases 2-6");
    const errors = validatePhase(options.out, phase);
    if (errors.length > 0) fail(`${summarizePhase(phase)} validation failed:\n- ${errors.join("\n- ")}`);
    process.stdout.write(`${summarizePhase(phase)} validation passed.\n`);
    return;
  }

  const phases = options.phase ? [getBeamerPipelinePhase(options.phase)] : DECK_PIPELINE_PHASE_BLUEPRINTS.map((_, index) => getBeamerPipelinePhase(index + 1));
  const completed = [];
  for (const phase of phases) {
    completed.push(runOnePhase(options, phase));
    writeState(options.out, { input: options.input, out: options.out, completed, total: DECK_PIPELINE_TOTAL_PHASES });
  }
  process.stdout.write(`Beamer seven-phase pipeline completed: ${completed.map((item) => item.name).join(", ")}\n`);
}

main();
