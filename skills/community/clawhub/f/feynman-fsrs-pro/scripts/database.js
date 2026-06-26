import { Pool } from "pg";
import { execSync } from "child_process";

// ==================== 配置 ====================

const pool = new Pool({
  user: "openclaw_feiman",
  host: "127.0.0.1",
  database: "openclaw_feiman",
  password: "12345678",
  port: 5432,
});

// Obsidian 笔记库名称（通过 obsidian vaults 查看可用 vault）
const OBSIDIAN_VAULT = "new-note";

// ==================== Obsidian CLI 封装 ====================

/**
 * 执行 obsidian CLI 命令，返回 stdout
 */
function obsidianCmd(args) {
  const cmd = `obsidian ${args}`.trim();
  try {
    return execSync(cmd, { encoding: "utf-8", shell: true });
  } catch (err) {
    return ""; // 命令失败返回空字符串
  }
}

/**
 * 获取笔记库中所有 .md 文件列表
 * @returns {string[]} 文件路径列表（相对于 vault 根目录）
 */
function listVaultFiles() {
  const output = obsidianCmd(`files vault=${OBSIDIAN_VAULT} ext=md`);
  return output
    .split("\n")
    .map((f) => f.trim())
    .filter((f) => f.endsWith(".md"));
}

/**
 * 搜索匹配概念名称的笔记文件路径
 * @param {string} conceptName - 概念名称
 * @returns {string|null} 匹配的文件路径，或 null
 */
function findNotePath(conceptName) {
  const files = listVaultFiles();
  const nameWithoutExt = conceptName.replace(/\.md$/, "");
  const normalized = nameWithoutExt.toLowerCase().replace(/\s+/g, "-");

  // 精确匹配：文件名（不含扩展名）完全等于概念名
  for (const file of files) {
    const fileName = file.replace(/\.md$/, "").toLowerCase();
    if (fileName === normalized) return file;
  }

  // 模糊匹配：以概念名开头的文件（处理 "torch.ones() and torch.ones_like()" 这类多概念文件名）
  for (const file of files) {
    const fileName = file.replace(/\.md$/, "").toLowerCase().replace(/\s+/g, "-");
    if (fileName.startsWith(normalized) || fileName.startsWith(normalized + "(")) {
      return file;
    }
  }

  return null;
}

// ==================== 核心工具函数 ====================

/**
 * 获取新增笔记
 * 扫描 Obsidian 笔记目录，返回尚未导入数据库的新笔记
 * @returns {Promise<Array>} 新笔记列表 [{conceptName, filePath}]
 */
export async function get_new_notes() {
  const files = listVaultFiles();

  // 查询数据库中已有的概念名称
  const existingNotes = await pool.query(
    "SELECT concept_name FROM feynman_memory"
  );
  const existingNames = new Set(
    existingNotes.rows.map((row) => normalizeConceptName(row.concept_name))
  );

  const newNotes = [];
  for (const file of files) {
    const conceptName = file.replace(/\.md$/, "");
    const normalizedName = normalizeConceptName(conceptName);
    if (!existingNames.has(normalizedName)) {
      newNotes.push({ conceptName, filePath: file });
    }
  }

  return newNotes;
}

/**
 * 导入新笔记到数据库
 * @param {string} conceptName - 概念名称
 * @param {string} filePath - 笔记文件路径（vault 相对路径）
 */
export async function import_new_note(conceptName, filePath) {
  await pool.query(
    `INSERT INTO feynman_memory (concept_name, obsidian_path, stability, difficulty, next_review)
     VALUES ($1, $2, 0.0, 5.0, NOW())
     ON CONFLICT (concept_name) DO NOTHING`,
    [conceptName, filePath]
  );
}

/**
 * 获取到期任务
 * @returns {Promise<Array>} 到期任务列表
 */
export async function get_due_tasks() {
  const res = await pool.query(
    `SELECT
       id, concept_name, obsidian_path, stability, difficulty,
       weak_points, last_review, next_review, review_history
     FROM feynman_memory
     WHERE next_review <= NOW()
     ORDER BY stability ASC, next_review ASC`
  );
  return res.rows;
}

/**
 * 获取笔记内容
 * @param {string} conceptName - 概念名称
 * @returns {Promise<string>} 笔记内容
 */
export async function get_note_content(conceptName) {
  const filePath = findNotePath(conceptName);
  if (!filePath) {
    return `❌ 找不到笔记文件：${conceptName}\n请确认笔记存在于 vault "${OBSIDIAN_VAULT}" 中。`;
  }

  // path= 使用精确路径，file= 使用名称解析（类 wikilink 行为）
  const content = obsidianCmd(`read vault=${OBSIDIAN_VAULT} path="${filePath}"`);
  if (!content.trim()) {
    return `❌ 读取失败：${conceptName}`;
  }
  return content;
}

/**
 * 更新学习进度
 * @param {Object} params - { concept_name, rating, feedback, summary }
 */
export async function update_study_progress({ concept_name, rating, feedback, summary }) {
  const res = await pool.query(
    `SELECT id, stability, difficulty, weak_points, review_history, obsidian_path
     FROM feynman_memory WHERE concept_name = $1`,
    [concept_name]
  );

  const row = res.rows[0];
  if (!row) throw new Error(`概念 "${concept_name}" 在数据库中不存在`);

  let s = row.stability || 0.4;
  let d = row.difficulty || 5.0;
  let weakPoints = Array.isArray(row.weak_points) ? row.weak_points : [];
  let reviewHistory = Array.isArray(row.review_history) ? row.review_history : [];

  // FSRS 参数更新
  const dDelta = (rating - 3) * 0.8;
  d = Math.max(1, Math.min(10, d - dDelta));

  if (rating >= 3) {
    const retentionFactor = [0.5, 0.6, 0.7, 0.85][rating - 1];
    s = s + Math.max(0.1, ((10 - d) / 10) * retentionFactor);
  } else {
    s = Math.max(0.1, s - (d / 10) * 0.3);
  }

  const intervalDays = Math.max(1, Math.round(s * (2 - d / 5)));
  const nextReview = new Date();
  nextReview.setDate(nextReview.getDate() + intervalDays);

  if (feedback?.trim() && !weakPoints.includes(feedback.trim())) {
    weakPoints = [...weakPoints.slice(-4), feedback.trim()];
  }

  const historyItem = {
    date: new Date().toISOString(),
    rating,
    feedback: feedback || "",
    summary: summary || "",
    interval: intervalDays,
    stability_before: row.stability,
    stability_after: s,
    difficulty_before: row.difficulty,
    difficulty_after: d,
  };
  reviewHistory = [...reviewHistory.slice(-19), historyItem];

  await pool.query(
    `UPDATE feynman_memory SET
       stability = $2, difficulty = $3, last_review = NOW(), next_review = $4,
       weak_points = $5::jsonb, review_history = $6::jsonb, obsidian_path = $7
     WHERE concept_name = $1`,
    [
      concept_name, parseFloat(s.toFixed(3)), parseFloat(d.toFixed(2)),
      nextReview, JSON.stringify(weakPoints), JSON.stringify(reviewHistory),
      row.obsidian_path || conceptName,
    ]
  );

  return {
    stability: parseFloat(s.toFixed(3)),
    difficulty: parseFloat(d.toFixed(2)),
    intervalDays,
    nextReview: nextReview.toISOString(),
    weakPoints,
  };
}

/**
 * 获取概念详情
 */
export async function get_concept_detail(conceptName) {
  const res = await pool.query(
    `SELECT * FROM feynman_memory WHERE concept_name = $1`,
    [conceptName]
  );
  return res.rows[0] || null;
}

/**
 * 获取学习统计
 */
export async function get_study_stats() {
  const res = await pool.query(
    `SELECT
       COUNT(*) as total_cards,
       COUNT(CASE WHEN next_review <= NOW() THEN 1 END) as due_cards,
       COUNT(CASE WHEN next_review > NOW() THEN 1 END) as upcoming_cards,
       AVG(stability) as avg_stability, AVG(difficulty) as avg_difficulty
     FROM feynman_memory`
  );
  return res.rows[0];
}

// ==================== 辅助函数 ====================

function normalizeConceptName(name) {
  return (name || "")
    .replace(/\.md$/i, "")
    .trim()
    .toLowerCase()
    .replace(/\s+/g, " ");
}

export { pool };
