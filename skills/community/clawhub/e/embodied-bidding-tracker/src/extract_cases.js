/**
 * Extract: LLM 解析 raw_content → 结构化入库数据 → 格式化输出
 *
 * 输入: data/raw_content/*.md  +  data/bidding_records.csv
 * 输出:
 *   data/extract_results.csv        — 全量 LLM 提取结果
 *   data/review_sheet.csv           — 通过+待验证，供人工复核「人工决定」列
 *   data/output/ingestion_output.csv — 「人工决定=通过」的入库格式文件
 *
 * 用法:
 *   npm run extract        — 首次运行或继续断点
 *   npm run extract        — 人工改完 review_sheet.csv 后再跑一次，刷新 ingestion_output.csv
 *
 * LLM provider:
 *   "openai-compatible"   — 使用 OpenAI 兼容接口（如 Moonshot 等）
 */

import path from 'path';
import fs from 'fs';
import { fileURLToPath } from 'url';
import { readCsv, writeCsv } from './utils/excel.js';
import { logger } from './utils/logger.js';
import { callLLM } from './utils/llm.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const projectRoot = path.resolve(__dirname, '..');

function getArgValue(flag) {
  const idx = process.argv.indexOf(flag);
  if (idx === -1) return null;
  return process.argv[idx + 1] || null;
}

function resolveCliPath(flag, fallback) {
  const value = getArgValue(flag);
  if (!value) return fallback;
  return path.isAbsolute(value) ? value : path.resolve(projectRoot, value);
}

const BIDDING_CSV     = resolveCliPath('--input',     path.join(projectRoot, 'data', 'bidding_records.csv'));
const RAW_CONTENT_DIR = path.join(projectRoot, 'data', 'raw_content');
const OUTPUT_CSV      = resolveCliPath('--output',    path.join(projectRoot, 'data', 'extract_results.csv'));
const REVIEW_CSV      = resolveCliPath('--review',    path.join(projectRoot, 'data', 'review_sheet.csv'));
const INGESTION_CSV   = resolveCliPath('--ingestion', path.join(projectRoot, 'data', 'output', 'ingestion_output.csv'));
const PROGRESS_FILE   = resolveCliPath('--progress',  path.join(projectRoot, 'data', 'extract_progress.json'));

// ── 输出字段（对齐 embodied-case-ingestion skill 规范）────────────────────
const CSV_HEADERS = [
  { id: 'robotCompany',   title: '机器人企业' },
  { id: 'admissionResult',title: '准入结果' },       // 通过 / 不通过 / 待验证
  { id: 'exclusionReason',title: '排除原因' },
  { id: 'primaryScene',   title: '一级场景' },
  { id: 'secondaryScene', title: '二级场景' },
  { id: 'demandSide',     title: '场景需求方' },
  { id: 'deployCity',     title: '部署城市' },
  { id: 'robotModel',     title: '机器人型号' },
  { id: 'projectName',    title: '项目名' },
  { id: 'deployTime',     title: '部署时间' },
  { id: 'amount',         title: '金额(万元)' },
  { id: 'caseDetail',     title: '案例详情(草稿)' },
  { id: 'deployStatus',   title: '部署状态' },
  { id: 'dataSource',     title: '数据源' },
  { id: 'link',           title: '链接' },
  { id: 'rawContentFile', title: 'raw_content文件' },
];

// ── 提示词 ────────────────────────────────────────────────────────────────
const SYSTEM_PROMPT = `你是具身智能产业数据库的数据录入专家。
你的任务是：解析天眼查中标公告的原始页面文本，提取结构化字段，并按入库规范判断是否可以入库。

## 准入规则

### 核心原则
本数据库只收录**实体机器人整机（或整机级产品）的真实采购与部署案例**。判断的关键不是项目名称是否含"机器人"，而是**实际采购/交付的标的物是否为机器人整机**。项目名称含"机器人""具身智能"但实际采购内容是装修、咨询、测试仪器、零部件等，一律不入库。

### 快速通过规则（优先于排除规则判断）
1. **有明确机器人型号**：公告中出现了具体的机器人型号名称（如 G1-edu、Walker S2、PM01、ENCOS 等），且中标方为机器人企业或公告内容涉及整机采购/交付，直接判"通过"
2. **中标方为具身智能行业知名本体企业**：如优必选、宇树、乐聚、逐际动力、智元、穹彻智能、星尘智能、众擎、银河通用、开普勒、傅利叶、达闼等，且项目内容为机器人整机采购/部署，判"通过"。但即使是知名企业，若实际采购内容属于下列不入库类别（如装修、零部件、咨询等），仍应排除
3. **中标方为具身智能行业知名本体企业，且项目名称、项目类型或正文表述属于以下放宽场景时，默认判"通过"**：
   - 文旅/展馆/主题馆/科技馆/博物馆/展厅/体验馆等场馆设备采购
   - 人形机器人设备采购
   - 具身智能设备采购
   - 人工智能研学主题馆、机器人主题馆、机器人展陈等馆内设备采购
   以上放宽规则适用于中标/成交公告，即使正文未披露具体机器人型号、数量或整机清单，只要中标方是知名本体企业，且项目不属于工程装修、咨询评估、零部件、测试仪器、纯软件等明确排除类别，也默认判"通过"

### 可入库（实际采购标的必须涉及机器人整机，至少满足其一）
- 机器人整机采购：需求方采购机器人整机设备，有合同金额或交付数量（中标/成交公告即视为合同签署证据）
- 机器人整机部署：机器人已在需求方真实场景部署并投入使用
- 整机代工/OEM：需求方向机器人企业采购整机代工服务
- 科技馆/博物馆/展厅等永久场所采购机器人整机用于讲解引导或展示
- 教育机构采购机器人整机（非纯教具/耗材/实训平台软件）用于教学或科研
- 招标公告/招标更正公告：爬取企业为知名本体企业且项目为整机采购，尚无中标结果 → admissionResult 填"待验证"

### 不入库（含以下任一则排除）
- **工程/装修/施工类**：装修、装饰、布展、建筑设计、施工、改造、消防工程、监理等。即使项目名含"机器人体验中心""具身智能创新中心"，只要实际采购内容是工程/装修/设计而非机器人设备 → "不通过"
- **咨询/审计/评估/调研类**：可行性研究、产业调查、审计、资产评估、咨询服务、规划设计等专业服务 → "不通过"
- **赛事/活动策划类**：机器人比赛策划、赛事服务、街舞编排等活动服务，采购标的为策划/执行服务而非机器人设备 → "不通过"
- **测试/测量仪器设备类**：动作捕捉系统、位姿追踪系统、测试分析系统、测量系统、对扭试验台等。这些是辅助机器人研发的仪器设备，不是机器人整机 → "不通过"
- **零部件/组件类**：关节模组、减速机、丝杠、编码器、电机、力传感器、灵巧手单独采购、底盘改装、部件加工制备等，属于供应链或组件级采购 → "不通过"
- **生产线/产线设备类**：为制造机器人零部件而采购的产线设备（如电机产线、加工设备），属于制造端投资而非应用端部署 → "不通过"
- **纯软件/研发服务类**：软件开发、控制器研发、算法适配、数据采集平台（纯软件）、技术开发合作（无整机交付）、自主导航研发等 → "不通过"
- **纯融资事件**：无需求方、无部署 → "不通过"
- **明确废标**：有效供应商不足等导致采购终止 → "不通过"
- **信源已被官方辟谣**（见辟谣条款）→ "不通过"
- 仅有意向但无实际交付证据 → "待验证"

### 易错提醒
- 项目名含"机器人"≠采购机器人。必须确认公告原文中实际采购的标的物是什么
- 中标方为建筑公司、设计院、咨询公司、会计师事务所、评估公司等非机器人企业时，高度警惕，大概率不是机器人整机采购
- "实训平台""训练室建设"：如果采购内容是整套教学平台系统（含软硬件集成但无独立机器人整机）或教室装修建设，不入库；仅当明确含机器人整机采购时才入库
- 若中标方为知名本体企业，且项目属于文旅/展馆/主题馆/科技馆设备采购，或项目名称明确写有人形机器人设备采购、具身智能设备采购，则优先适用上述放宽规则，不要因为正文未列出型号或数量就判"不通过"

### 辟谣条款
若公告内容已被企业官方声明、证券交易所公告或主流财经媒体引用的企业声明明确否认，则强制填"不通过"。
触发前提（三条须同时满足）：
1. 辟谣声明发布时间晚于被核实报道
2. 辟谣指向同一事件（同企业、同场景、同时间段）
3. 辟谣来源为 A 级或 B 级信源
注意：企业"未予置评"或"不回应"≠辟谣，保持"待验证"。

### 信源可信度要求（至少 B 级）
- A 级：企业官方公告、证券交易所公告、新华社/路透社/彭博社
- B 级：知名垂直科技媒体（36氪、钛媒体、OFweek）、主流财经媒体（财联社、南方+）
- C 级：地方新闻、自媒体、论坛 — 不可作为唯一信源，填"待验证"
天眼查中标公告属于政府采购平台数据，视为 A 级信源。

## 字段规范

### 一级场景（严格从以下7个枚举中选一个）
- 工业制造：工厂/车间/产线中的制造任务
- 商用服务：商业场所为企业或消费者提供服务
- 公共服务：政府/学校/科研机构等公共部门场景（不含医疗）
- 医疗康复：医院/康复机构等医疗健康场景
- 特种作业：电力/管网/应急/建筑等高危或专业作业场景
- 养老服务：面向老龄人群的康养陪护场景
- 家用服务：家庭场景中的清洁等日常服务

### 二级场景（严格从以下枚举中选一个，不可复合）
工业制造类：汽车制造 / 3C制造 / 家电制造 / 其他
商用服务类：表演娱乐 / 讲解引导 / 物流配送 / 餐饮配送 / 零售 / 酒店配送
公共服务类：政务 / 智慧环卫 / 科研教育
医疗康复类：康复 / 手术 / 医疗服务
特种作业类：市政管网 / 应急安防 / 电力巡检 / 建筑
  注意：电信运营商数据中心、通信机房等 IDC 场景中的机器人巡检/运维任务归入"电力巡检"，不归入"应急安防"或"科研教育"

### 场景分类易混淆规则
- 科技馆、科学技术馆、博物馆、文化馆、展览馆、纪念馆、体验馆等场馆中的机器人采购 → 商用服务-讲解引导（不归入公共服务-科研教育，这类场馆的机器人主要承担讲解、引导、展示功能）
- 需求方属于文旅口（如文化和旅游局、文旅集团、研学营地、主题馆等） → 商用服务-讲解引导
- 仅当需求方为大中小学、高校、科研院所，且项目用途为教学或科研时，才归入公共服务-科研教育
养老服务类：康养辅助 / 护理 / 情感陪护
家用服务类：家用清洁

### 其他字段
- 部署城市：国内到城市（不加省份），海外到国家，多城市只填第一个
- 机器人型号：官方型号名，未公布填"-"
- 部署时间：YYYY.MM 或 YYYY.Qn 或 YYYY；优先从公告正文提取实际部署/交付日期，若正文无明确信息则直接使用公告发布日期
- 金额：万元人民币纯数字（例：189777元 → 18.98，80万元 → 80，3608.68万元 → 3608.68），未披露填"-"
- 部署状态：已验证（有合同/交付/成交证据）/ 待验证（仅意向协议）
- 案例详情：100-200字，以该中标项目为载体，如实简要地说明具身智能机器人的应用场景与应用水平。
    写作顺序：① 什么型号的机器人、在什么需求方、承担什么具体任务；② 关键技术规格或部署规模；③ 可量化的应用效果或能力指标（有则写，无则省略）。
    删去：合同编号、交货期、质保条款、供货商信息、公司介绍、行业宏观叙述、”标志着”类判断语句。
    未披露的信息直接省略，不写”型号未披露/金额未披露/部署数量未披露/效果暂无”等负面说明。

## 输出要求
只输出一个 JSON 对象，不要加任何说明文字、markdown 代码块标记或注释：
{
  "admissionResult": "通过" 或 "不通过" 或 "待验证",
  "exclusionReason": "不通过时填排除原因，其余填空字符串",
  "primaryScene": "一级场景枚举值",
  "secondaryScene": "二级场景枚举值",
  "demandSide": "需求方法人全称",
  "deployCity": "城市名",
  "robotModel": "型号",
  "projectName": "20字以内项目摘要标题",
  "deployTime": "YYYY.MM",
  "amount": "万元数字或-",
  "caseDetail": "100-200字案例详情",
  "deployStatus": "已验证 或 待验证"
}`;

// ── 工具函数 ──────────────────────────────────────────────────────────────

function loadProgress() {
  if (fs.existsSync(PROGRESS_FILE)) {
    try { return JSON.parse(fs.readFileSync(PROGRESS_FILE, 'utf-8')); } catch { /* ignore */ }
  }
  return { completed: {}, failed: [] };
}

function saveProgress(progress) {
  fs.writeFileSync(PROGRESS_FILE, JSON.stringify(progress, null, 2));
}

/**
 * 将 bidding_records.csv 去重，以 (企业名, 项目名) 为唯一键
 * 同时过滤掉明显噪音（天眼查误抓的非机器人企业）
 */
function deduplicateRecords(records) {
  // 明显噪音企业关键词（可按需扩充）
  const NOISE_COMPANIES = ['腾讯计算机', '兆威机电'];
  const seen = new Set();
  const result = [];
  for (const r of records) {
    const company = r['企业名称']?.trim() ?? '';
    const project = r['项目名称']?.trim() ?? '';
    const link = r['天眼查详情页链接']?.trim() ?? '';
    if (NOISE_COMPANIES.some(kw => company.includes(kw))) continue;
    const key = `${company}||${project}||${link}`;
    if (seen.has(key)) continue;
    seen.add(key);
    result.push(r);
  }
  return result;
}

/**
 * 在 raw_content 目录中查找与某条记录匹配的文件
 * 匹配逻辑：文件名以 "{企业名}_{项目名前15字}" 开头
 */
function findRawContentFile(company, project, rawFiles) {
  const safe = s => s.replace(/[\/\\:*?"<>|]/g, '_');
  const companyPart = safe(company);
  const projectPrefix = safe(project).substring(0, 15);
  const candidates = rawFiles.filter(f =>
    f.startsWith(companyPart + '_') && f.includes(projectPrefix)
  );
  if (candidates.length === 0) return null;
  if (candidates.length === 1) return candidates[0];
  // 多个候选时，优先选择项目名匹配位置最靠前的（即文件名中项目名出现得越早，说明前缀越短、越精确）
  candidates.sort((a, b) => a.indexOf(projectPrefix) - b.indexOf(projectPrefix));
  return candidates[0];
}

/**
 * 从 LLM 输出中提取并解析 JSON
 * 兼容：1) JSON 前后有说明文字  2) 字段值中含未转义的直角引号
 */
function extractJSON(text) {
  const match = text.match(/\{[\s\S]*\}/);
  if (!match) throw new Error(`LLM 输出中未找到 JSON：${text.slice(0, 200)}`);

  let raw = match[0];
  try {
    return JSON.parse(raw);
  } catch {
    // 修复：将字符串值内的未转义直引号替换为中文引号，再尝试解析
    const fixed = raw.replace(
      /("(?:admissionResult|exclusionReason|primaryScene|secondaryScene|demandSide|deployCity|robotModel|projectName|deployTime|amount|caseDetail|deployStatus)":\s*")([\s\S]*?)("(?:,|\s*\}))/g,
      (_, key, value, end) => {
        // 将值内部的 ASCII 双引号转义
        const escaped = value.replace(/(?<!\\)"/g, '\\"');
        return `${key}${escaped}${end}`;
      }
    );
    return JSON.parse(fixed);
  }
}

/**
 * 金额后处理：确保单位为万元
 * 若模型输出了超过 10 万的纯数字（疑似填了元），自动除以 10000
 */
function normalizeAmount(raw) {
  if (!raw || raw === '-') return '-';
  const num = parseFloat(String(raw).replace(/,/g, ''));
  if (isNaN(num)) return '-';
  // 超过 10 万视为误填成元，换算为万元
  const wan = num > 100000 ? Math.round(num / 10000 * 100) / 100 : Math.round(num * 100) / 100;
  return String(wan);
}

// ── 入库格式化（原 Step 4 逻辑）─────────────────────────────────────────

const INGESTION_HEADERS = [
  { id: 'primaryScene',   title: '一级场景' },
  { id: 'secondaryScene', title: '二级场景' },
  { id: 'demandSide',     title: '场景需求方' },
  { id: 'robotCompany',   title: '机器人企业' },
  { id: 'deployCity',     title: '部署城市' },
  { id: 'robotModel',     title: '机器人型号' },
  { id: 'projectName',    title: '项目名' },
  { id: 'deployTime',     title: '部署时间' },
  { id: 'amount',         title: '金额(万元)' },
  { id: 'caseDetail',     title: '案例详情' },
  { id: 'deployStatus',   title: '部署状态' },
  { id: 'dataSource',     title: '数据源' },
  { id: 'link',           title: '链接' },
  { id: 'parentRecord',   title: '父记录' },
  { id: 'ingestTime',     title: '入库时间' },
];

function formatDeployTime(dateStr) {
  if (!dateStr) return '';
  const mmMatch = dateStr.match(/(\d{4})[-./](\d{1,2})/);
  if (mmMatch) return `${mmMatch[1]}.${mmMatch[2].padStart(2, '0')}`;
  const yearMatch = dateStr.match(/(\d{4})/);
  return yearMatch ? yearMatch[1] : '';
}

function getIngestTime() {
  const now = new Date();
  const local = new Date(now.getTime() + 8 * 60 * 60 * 1000);
  return local.toISOString().replace('Z', '+08:00').replace(/\.\d{3}/, '');
}

/**
 * 读取人工复核后的 review_sheet.csv，将「人工决定=通过」的记录
 * 格式化后写入 ingestion_output.csv。
 * Extract 主流程结束后调用；人工改完 review_sheet 后重跑 extract 可刷新此文件。
 */
async function finalizeIngestion() {
  if (!fs.existsSync(REVIEW_CSV)) {
    logger.warn('review_sheet.csv 不存在，跳过生成 ingestion_output.csv');
    return;
  }

  const rows = readCsv(REVIEW_CSV);
  const passed = rows.filter(r => r['人工决定'] === '通过');
  logger.info(`ingestion 格式化: review_sheet ${rows.length} 条，人工决定=通过 ${passed.length} 条`);

  const ingestTime = getIngestTime();
  const records = passed.map(r => ({
    primaryScene:   r['一级场景'],
    secondaryScene: r['二级场景'],
    demandSide:     r['场景需求方'],
    robotCompany:   r['机器人企业'],
    deployCity:     r['部署城市'],
    robotModel:     r['机器人型号'] || '-',
    projectName:    r['项目名'] || '-',
    deployTime:     formatDeployTime(r['部署时间']),
    amount:         r['金额(万元)'] || '-',
    caseDetail:     r['案例详情(草稿)'],
    deployStatus:   r['部署状态'] || '待验证',
    dataSource:     r['数据源'],
    link:           r['链接'],
    parentRecord:   '-',
    ingestTime,
  }));

  const outputDir = path.dirname(INGESTION_CSV);
  if (!fs.existsSync(outputDir)) fs.mkdirSync(outputDir, { recursive: true });

  if (records.length > 0) {
    await writeCsv(INGESTION_CSV, INGESTION_HEADERS, records);
    logger.info(`ingestion_output.csv → ${INGESTION_CSV}`);
  }
}

function toQuarter(timeStr) {
  if (!timeStr) return '';
  const m = timeStr.match(/(\d{4})(?:\.(\d{1,2}))?/);
  if (!m) return timeStr;
  const year = m[1];
  const month = m[2] ? parseInt(m[2]) : null;
  if (!month) return year;
  return `${year}.Q${Math.ceil(month / 3)}`;
}

// ── 主流程 ────────────────────────────────────────────────────────────────

async function main() {
  logger.info('=== Extract: 解析 raw_content → 结构化入库数据 ===');

  if (!fs.existsSync(BIDDING_CSV)) {
    logger.error(`未找到招投标记录: ${BIDDING_CSV}，请先运行 npm run crawl`);
    process.exit(1);
  }

  // 读取并去重
  const allRecords = readCsv(BIDDING_CSV);
  const records = deduplicateRecords(allRecords);
  logger.info(`bidding_records 原始 ${allRecords.length} 条，去重+过滤后 ${records.length} 条`);

  // 读取 raw_content 文件列表
  const rawFiles = fs.readdirSync(RAW_CONTENT_DIR).filter(f => f.endsWith('.md'));
  logger.info(`raw_content 文件 ${rawFiles.length} 个`);

  // 加载进度
  const progress = loadProgress();
  logger.info(`已完成 ${Object.keys(progress.completed).length} 条，失败 ${progress.failed.length} 条`);

  // --rerun-rejected: 清除「不通过」记录，使其重新走 LLM 判断
  const rerunRejected = process.argv.includes('--rerun-rejected');
  if (rerunRejected) {
    let cleared = 0;
    for (const [key, rec] of Object.entries(progress.completed)) {
      if (rec.admissionResult === '不通过') {
        delete progress.completed[key];
        cleared++;
      }
    }
    logger.info(`--rerun-rejected: 已清除 ${cleared} 条「不通过」记录，将重新提取`);
    saveProgress(progress);
  }

  // 加载已有结果
  const results = Object.values(progress.completed);

  // 统计 raw_content 覆盖情况
  let withRaw = 0, withoutRaw = 0;
  for (const r of records) {
    const f = findRawContentFile(r['企业名称'], r['项目名称'], rawFiles);
    if (f) withRaw++; else withoutRaw++;
  }
  logger.info(`有 raw_content: ${withRaw} 条，无 raw_content（将跳过）: ${withoutRaw} 条`);

  // 清除之前的失败记录，允许重试
  const oldFailedCount = progress.failed.length;
  if (oldFailedCount > 0) {
    progress.failed = [];
    logger.info(`清除 ${oldFailedCount} 条历史失败记录，将重新尝试`);
  }

  // 过滤出待处理记录（未完成的，包括之前失败的）
  const pending = records.filter(r => {
    const company = r['企业名称']?.trim() ?? '';
    const project = r['项目名称']?.trim() ?? '';
    const link = r['天眼查详情页链接']?.trim() ?? '';
    const oldKey = `${company}||${project}`;
    const newKey = `${company}||${project}||${link}`;
    // 新 key 已存在 -> 已完成
    if (progress.completed[newKey]) return false;
    // 旧 key 不存在 -> 待处理
    if (!progress.completed[oldKey]) return true;
    // 旧 key 存在，但链接不同 -> 是另一条记录，需要重新处理
    const existing = progress.completed[oldKey];
    return existing.link !== link;
  });
  logger.info(`待处理 ${pending.length} 条`);

  let doneCount = 0;
  let consecutiveFailures = 0;

  for (let i = 0; i < pending.length; i++) {
    const r = pending[i];
    const company = r['企业名称']?.trim() ?? '';
    const project = r['项目名称']?.trim() ?? '';
    const link = r['天眼查详情页链接']?.trim() ?? '';
    const key = `${company}||${project}||${link}`;

    logger.info(`[${i + 1}/${pending.length}] ${company} | ${project.substring(0, 40)}`);

    // 查找 raw_content 文件
    const rawFile = findRawContentFile(company, project, rawFiles);
    if (!rawFile) {
      logger.warn(`  ⚠️  无 raw_content 文件，跳过`);
      continue;
    }

    const rawContent = fs.readFileSync(path.join(RAW_CONTENT_DIR, rawFile), 'utf-8');
    // 截断避免超出 token 限制（保留前 6000 字符，通常已含关键信息）
    const truncated = rawContent.length > 6000
      ? rawContent.substring(0, 6000) + '\n...[内容已截断]'
      : rawContent;

    const userContent = `以下是天眼查中标公告的原始页面文本。
企业名称（爬取来源）：${company}
公告日期（参考）：${r['发布日期'] ?? ''}
原始中标金额（参考）：${r['中标金额'] ?? ''}
天眼查详情链接：${r['天眼查详情页链接'] ?? ''}

--- 原始页面文本 ---
${truncated}`;

    // 重试机制：最多尝试 MAX_RETRIES 次，全部失败则停止脚本
    const MAX_RETRIES = 5;
    let succeeded = false;

    for (let attempt = 1; attempt <= MAX_RETRIES; attempt++) {
      try {
        const llmOutput = await callLLM(SYSTEM_PROMPT, userContent);
        if (!llmOutput || !llmOutput.trim()) {
          throw new Error('LLM 返回空内容');
        }
        const parsed = extractJSON(llmOutput);

        const record = {
          robotCompany:    company,
          admissionResult: parsed.admissionResult ?? '',
          exclusionReason: parsed.exclusionReason ?? '',
          primaryScene:    parsed.primaryScene ?? '',
          secondaryScene:  parsed.secondaryScene ?? '',
          demandSide:      parsed.demandSide ?? '',
          deployCity:      parsed.deployCity ?? '',
          robotModel:      parsed.robotModel ?? '',
          projectName:     parsed.projectName ?? '',
          deployTime:      parsed.deployTime ?? '',
          amount:          normalizeAmount(parsed.amount),
          caseDetail:      parsed.caseDetail ?? '',
          deployStatus:    parsed.deployStatus ?? '',
          dataSource:      '天眼查',
          link:            r['天眼查详情页链接'] ?? '',
          rawContentFile:  rawFile,
        };

        results.push(record);
        progress.completed[key] = record;
        // 同时清理可能存在的旧 key 记录（避免同项目名不同链接的混淆）
        const oldKey = `${company}||${project}`;
        if (progress.completed[oldKey] && progress.completed[oldKey].link !== link) {
          delete progress.completed[oldKey];
        }
        doneCount++;
        consecutiveFailures = 0;  // 重置连续失败计数
        logger.info(`  ✅ ${parsed.admissionResult} | ${parsed.primaryScene}-${parsed.secondaryScene} | ${parsed.demandSide}`);
        succeeded = true;
        break;

      } catch (err) {
        logger.error(`  ❌ 第 ${attempt}/${MAX_RETRIES} 次尝试失败: ${err.message}`);
        if (attempt < MAX_RETRIES) {
          const delay = attempt * 2000;  // 递增延迟: 2s, 4s, 6s, 8s
          logger.info(`  ⏳ ${delay / 1000}s 后重试...`);
          await new Promise(r => setTimeout(r, delay));
        }
      }
    }

    if (!succeeded) {
      consecutiveFailures++;
      logger.error(`  ❌ ${key} 经 ${MAX_RETRIES} 次重试后仍失败，跳过`);
      progress.failed.push({ key, error: `${MAX_RETRIES} 次重试均失败`, time: new Date().toISOString() });

      if (consecutiveFailures >= 3) {
        logger.error(`🛑 连续 ${consecutiveFailures} 条记录 LLM 调用失败，疑似服务不可用，停止脚本`);
        saveProgress(progress);
        if (results.length > 0) {
          await writeCsv(OUTPUT_CSV, CSV_HEADERS, results);
        }
        process.exit(1);
      }
    }

    // 每 5 条保存一次进度 + 中间结果
    if ((doneCount) % 5 === 0 && results.length > 0) {
      saveProgress(progress);
      await writeCsv(OUTPUT_CSV, CSV_HEADERS, results);
      logger.info(`  中间保存: 已处理 ${doneCount} 条`);
    }

    // 调用间隔（避免 API 限速）
    await new Promise(r => setTimeout(r, 1000));
  }

  // —— 去重：按(机器人企业 + 场景需求方 + 部署季度)三字段联合去重 --
  const deduped = [];
  const seenKey = new Set();
  for (const rec of results) {
    const key = `${rec.robotCompany}||${rec.demandSide}||${toQuarter(rec.deployTime)}||${rec.link}`;
    if (seenKey.has(key)) {
      logger.warn(`  去重跳过：${rec.robotCompany} | ${rec.demandSide} | ${rec.deployTime}`);
      continue;
    }
    seenKey.add(key);
    deduped.push(rec);
  }
  if (deduped.length < results.length) {
    logger.info(`去重: ${results.length} 条 → ${deduped.length} 条（移除 ${results.length - deduped.length} 条重复）`);
  }

  // 最终保存
  saveProgress(progress);
  if (deduped.length > 0) {
    await writeCsv(OUTPUT_CSV, CSV_HEADERS, deduped);
  }

  // ── 输出 review_sheet.csv（人工复核用）──────────────────────────────────
  // 包含「通过」和「待验证」，各加一列「人工决定」供人工确认/修改
  // 重跑时保留已有文件中人工编辑过的「人工决定」值
  const REVIEW_HEADERS = [
    { id: 'humanDecision',  title: '人工决定' },
    ...CSV_HEADERS,
  ];

  // 读取已有的人工决定值（key = 机器人企业||场景需求方）
  const existingHumanDecisions = new Map();
  if (fs.existsSync(REVIEW_CSV)) {
    for (const row of readCsv(REVIEW_CSV)) {
      const k = `${row['机器人企业']}||${row['场景需求方']}`;
      existingHumanDecisions.set(k, row['人工决定']);
    }
  }

  const reviewRecords = deduped
    .filter(r => r.admissionResult === '通过' || r.admissionResult === '待验证')
    .map(r => {
      const k = `${r.robotCompany}||${r.demandSide}`;
      const humanDecision = existingHumanDecisions.get(k) ?? r.admissionResult;
      return { humanDecision, ...r };
    });

  if (reviewRecords.length > 0) {
    await writeCsv(REVIEW_CSV, REVIEW_HEADERS, reviewRecords);
    const preserved = reviewRecords.filter(r => existingHumanDecisions.has(`${r.robotCompany}||${r.demandSide}`)).length;
    logger.info(`review_sheet 输出: ${reviewRecords.length} 条（保留人工决定 ${preserved} 条）→ ${REVIEW_CSV}`);
  }

  // ── 生成 ingestion_output.csv（原 Step 4 逻辑）───────────────────────────
  await finalizeIngestion();

  // 统计
  const passed    = deduped.filter(r => r.admissionResult === '通过').length;
  const pending2  = deduped.filter(r => r.admissionResult === '待验证').length;
  const excluded  = deduped.filter(r => r.admissionResult === '不通过').length;

  logger.info('=== Extract 完成 ===');
  logger.info(`通过: ${passed} | 待验证: ${pending2} | 不通过: ${excluded} | 失败: ${progress.failed.length}`);
  logger.info(`全量结果: ${OUTPUT_CSV}`);
  logger.info(`复核表格: ${REVIEW_CSV}`);
  logger.info(`入库文件: ${INGESTION_CSV}`);
  logger.info('');
  logger.info('如需调整「待验证」记录：编辑 review_sheet.csv 的「人工决定」列后，重跑 npm run extract（LLM 部分自动跳过）');
}

main().catch(err => {
  logger.error(`Extract 执行失败: ${err.message}`);
  process.exit(1);
});
