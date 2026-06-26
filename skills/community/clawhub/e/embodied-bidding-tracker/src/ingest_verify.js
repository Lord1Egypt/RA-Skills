/**
 * Ingest: 规范核实 & 入库
 *
 * 输入:  data/output/ingestion_output.csv（Extract 输出）
 *        data/output/具身智能案例入库_*.xlsx（现有数据库，去重用）
 *
 * 流程（按规范 v2026.04）:
 *   1. 去重检查 — 机器人企业 + 场景需求方 + 部署时间（季度）三字段联合
 *   2. 字段格式修正 — 金额/时间/型号/城市等常见错误自动修复
 *   3. 人工覆写检查 — 命中预设覆写表则直接使用人工文本，跳过详情质检
 *   4. 案例详情质检 — LLM 判断是否符合 150-250 字四段式，不合规则重写
 *   5. 案例简介生成 — LLM 生成 30-60 字一句话摘要（含人工覆写记录）
 *   6. 输出最终入库 CSV + 处置报告
 *
 * 用法:
 *   npm run ingest
 *   node src/ingest_verify.js --input path/to/input.csv --output path/to/output.csv --report path/to/report.md --progress path/to/progress.json
 */

import path from 'path';
import fs from 'fs';
import { fileURLToPath } from 'url';
import { readCsv, writeCsv, readExcel } from './utils/excel.js';
import { callLLM } from './utils/llm.js';
import { logger } from './utils/logger.js';

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

const INPUT_CSV          = resolveCliPath('--input', path.join(projectRoot, 'data', 'output', 'ingestion_output.csv'));
const DB_DIR             = path.join(projectRoot, 'data', 'output');
const OUTPUT_CSV         = resolveCliPath('--output', path.join(projectRoot, 'data', 'output', 'ingest_final.csv'));
const REPORT_FILE        = resolveCliPath('--report', path.join(projectRoot, 'data', 'output', 'ingest_report.md'));
const PROGRESS_FILE      = resolveCliPath('--progress', path.join(projectRoot, 'data', 'ingest_progress.json'));
const COMPANY_LIST_CSV   = path.join(projectRoot, 'data', 'company_list.csv');
const BIDDING_RECORDS_CSV = path.join(projectRoot, 'data', 'bidding_records.csv');

const HEADERS = [
  { id: 'primaryScene',   title: '一级场景' },
  { id: 'secondaryScene', title: '二级场景' },
  { id: 'demandSide',     title: '场景需求方' },
  { id: 'robotCompany',   title: '机器人企业' },
  { id: 'deployCity',     title: '部署城市' },
  { id: 'robotModel',     title: '机器人型号' },
  { id: 'projectName',    title: '项目名' },
  { id: 'deployTime',     title: '部署时间' },
  { id: 'amount',         title: '金额(万元)' },
  { id: 'caseSummary',    title: '案例简介' },
  { id: 'caseDetail',     title: '案例详情' },
  { id: 'deployStatus',   title: '部署状态' },
  { id: 'dataSource',     title: '数据源' },
  { id: 'link',           title: '链接' },
  { id: 'parentRecord',   title: '父记录' },
  { id: 'ingestTime',     title: '入库时间' },
];

// 历史数据里同一企业存在多个工商口径，补充别名以保证简称回填稳定。
const COMPANY_NAME_ALIASES = {
  '乐聚（深圳）机器人技术有限公司': '乐聚智能（深圳）股份有限公司',
  '杭州宇树科技有限公司': '宇树科技股份有限公司',
  '深圳市众擎机器人科技有限公司': '深圳众擎机器人科技股份有限公司',
  '上海智元新创技术有限公司': '智元创新（上海）科技股份有限公司',
  '深圳逐际动力科技有限公司': '深圳逐际动力科技股份有限公司',
  '智元创新（上海）科技有限公司': '智元创新（上海）科技股份有限公司',
  '乐聚智家（青岛）机器人技术有限公司': '乐聚智能（深圳）股份有限公司',
  '智平方具身科技（深圳）有限公司': '智平方（深圳）科技有限公司',
  '优必选教育（深圳）有限公司': '深圳市优必选科技股份有限公司',
};

// ── 企业简称映射（全称→MD简称）──────────────────────────────────────────────────

function loadCompanyNameMap() {
  if (!fs.existsSync(COMPANY_LIST_CSV)) return new Map();
  const rows = readCsv(COMPANY_LIST_CSV);
  const map = new Map();
  for (const r of rows) {
    const full  = r['企业全称(天眼查)']?.trim();
    const short = r['企业简称(MD)']?.trim();
    if (full && short) map.set(full, short);
  }
  for (const [alias, canonical] of Object.entries(COMPANY_NAME_ALIASES)) {
    const short = map.get(canonical);
    if (short) map.set(alias, short);
  }
  return map;
}

// ── 中标发布日期映射（链接→发布日期，供部署时间兜底）────────────────────────────

function loadPublishDateMap() {
  if (!fs.existsSync(BIDDING_RECORDS_CSV)) return new Map();
  const rows = readCsv(BIDDING_RECORDS_CSV);
  const map = new Map();
  for (const r of rows) {
    const link = r['天眼查详情页链接']?.trim();
    const date = r['发布日期']?.trim();
    if (link && date) map.set(link, date);
  }
  return map;
}

/**
 * 将 bidding_records 的发布日期格式（M/D/YYYY）转为 YYYY.MM
 */
function formatPublishDate(dateStr) {
  if (!dateStr) return '';
  const mdy = dateStr.match(/^(\d{1,2})\/(\d{1,2})\/(\d{4})$/);
  if (mdy) return `${mdy[3]}.${mdy[1].padStart(2, '0')}`;
  const iso = dateStr.match(/(\d{4})[-./](\d{1,2})/);
  if (iso) return `${iso[1]}.${iso[2].padStart(2, '0')}`;
  return dateStr;
}

// ── 进度管理 ─────────────────────────────────────────────────────────────────

function loadProgress() {
  if (fs.existsSync(PROGRESS_FILE)) {
    const data = JSON.parse(fs.readFileSync(PROGRESS_FILE, 'utf-8'));
    // 兼容旧格式：补充 summaries 字段
    if (!data.summaries) data.summaries = {};
    return data;
  }
  return { completed: [], failed: [], summaries: {} };
}

function saveProgress(progress) {
  fs.writeFileSync(PROGRESS_FILE, JSON.stringify(progress, null, 2), 'utf-8');
}

// ── Step 0: 去重检查 ──────────────────────────────────────────────────────────

/**
 * 将部署时间标准化到季度，用于去重比较
 * 例: "2026.03" → "2026.Q1"，"2026.Q2" → "2026.Q2"，"2026" → "2026"
 */
function normalizeToQuarter(timeStr) {
  if (!timeStr) return '';
  const s = String(timeStr).trim();
  // 已经是季度格式
  if (/^\d{4}\.Q[1-4]$/i.test(s)) return s.toUpperCase();
  // YYYY.MM 格式
  const mmMatch = s.match(/^(\d{4})\.(\d{1,2})$/);
  if (mmMatch) {
    const month = parseInt(mmMatch[2]);
    const q = Math.ceil(month / 3);
    return `${mmMatch[1]}.Q${q}`;
  }
  // 仅年份
  if (/^\d{4}$/.test(s)) return s;
  return s;
}

function buildDedupeKey(company, demandSide, deployTime) {
  return `${company}||${demandSide}||${normalizeToQuarter(deployTime)}`;
}

function loadExistingDb() {
  const existing = new Set();
  // 扫描 DB_DIR 下所有 xlsx 文件
  const files = fs.readdirSync(DB_DIR).filter(f => f.endsWith('.xlsx'));
  for (const file of files) {
    const rows = readExcel(path.join(DB_DIR, file), 0);
    for (const row of rows) {
      const company   = row['机器人企业'] || '';
      const demand    = row['场景需求方'] || '';
      const time      = row['部署时间'] || '';
      if (company || demand) {
        existing.add(buildDedupeKey(company, demand, time));
      }
    }
    logger.info(`已加载现有数据库: ${file}，${rows.length} 条记录`);
  }
  return existing;
}

// ── Step 1: 字段格式自动修正 ──────────────────────────────────────────────────

const AMOUNT_INVALID = /未披露|暂无|无|空|NA|n\/a/i;
const TIME_FUZZY     = /上半年|下半年|年初|年末|年底|初|末/;

const SCENE_1_VALID = new Set(['工业制造', '商用服务', '公共服务', '医疗康复', '特种作业', '养老服务', '家用服务']);
const SCENE_2_VALID = new Set([
  // 工业制造
  '汽车制造', '3C制造', '家电制造', '其他',
  // 商用服务
  '表演娱乐', '讲解引导', '物流配送', '餐饮配送', '零售', '酒店配送',
  // 公共服务
  '政务', '智慧环卫', '科研教育',
  // 医疗康复
  '康复', '手术', '医疗服务',
  // 特种作业
  '市政管网', '应急安防', '电力巡检', '建筑',
  // 养老服务
  '康养辅助', '护理', '情感陪护',
  // 家用服务
  '家用清洁',
]);

function fixFields(row) {
  const fixes = [];
  const r = { ...row };

  // 金额: 文字→"-"
  if (r['金额(万元)'] && AMOUNT_INVALID.test(r['金额(万元)'])) {
    fixes.push(`金额 "${r['金额(万元)']}" → "-"`);
    r['金额(万元)'] = '-';
  }
  if (!r['金额(万元)']) r['金额(万元)'] = '-';

  // 部署时间: 模糊描述警告
  if (r['部署时间'] && TIME_FUZZY.test(r['部署时间'])) {
    fixes.push(`⚠️ 部署时间模糊: "${r['部署时间']}"，请手动修正为 YYYY.QN`);
  }

  // 父记录: 空→"-"
  if (!r['父记录'] || r['父记录'].trim() === '') r['父记录'] = '-';

  // 一级/二级场景枚举校验
  if (!SCENE_1_VALID.has(r['一级场景'])) {
    fixes.push(`⚠️ 一级场景枚举不合规: "${r['一级场景']}"`);
  }
  if (!SCENE_2_VALID.has(r['二级场景'])) {
    fixes.push(`⚠️ 二级场景枚举不合规: "${r['二级场景']}"`);
  }

  // 机器人型号: 空→"未披露"
  if (!r['机器人型号'] || r['机器人型号'].trim() === '' || r['机器人型号'].trim() === '未披露') {
    r['机器人型号'] = '-';
    fixes.push('机器人型号空/未披露→"-"');
  }

  return { record: r, fixes };
}

// ── Step 2: 人工覆写表 ──────────────────────────────────────────────────────────

const MANUAL_OVERWRITES = {
  '宇树科技股份有限公司||深圳大学': `宇树G1edu-U2-ZL（G1 Edu进阶版）人形机器人在深圳大学科研教育场景中执行机器人运动学与控制算法教学演示任务。该机器人腰部自由度3个、单臂自由度7个，整机自由度达29个，整机重量约35kg，续航时间约2小时。采购数量1套，成交金额18.98万元，合同要求签订后10个日历日内完成交货并由供应商提供免费上门安装调试服务，整机质保18个月、质保期3年。该设备已纳入深圳大学机器人相关课程实验教学体系，支撑学生进行人形机器人运动控制实践。`,
  '北京人形机器人创新中心有限公司||和田地区工业和信息化局': `天轶2.0服务机器人在和田地区工业和信息化局政务服务场景中执行智能接待与业务引导任务。该机器人具备语音交互、人脸识别、自主导航等功能，可承担来访登记、业务咨询、办事指引等服务工作。采购数量1台，成交金额15万元，通过政府网上超市渠道完成采购。本次采购于2026年2月完成成交公告，合同已正式签署。该部署是服务机器人在新疆和田地区政府公共服务场景的首批落地应用之一，为偏远地区政务服务智能化提供示范参考。`,
  '杭州云深处科技股份有限公司||未披露': `云深处机器狗巡检套件在杭州某政府采购机构的公共安防场景中执行园区自动化巡逻与安防检测任务。该套件包含机器狗本体及配套巡检传感器模块，具备全天候自主巡检能力，可实时采集环境视频与传感器数据。本次采购以询价方式完成，预算9.4万元，成交价格8.75万元，成交率约93%。设备部署后可替代人工在固定区域执行周期性巡检作业，降低人工巡查成本并提升异常感知效率，适用于园区、厂区等封闭场所的安防巡检需求。`,
  '杭州云深处科技股份有限公司||中国电信股份有限公司金华分公司': `云深处四足机器人在中国电信股份有限公司金华分公司数据中心园区执行智能巡检任务，覆盖机房设备状态监测、环境温湿度检测及异常告警等运维环节。机器人搭载视觉与红外传感器，可自主规划巡检路径并完成设备表计读取、热点识别等任务。本次采购采用询比采购方式，标段编号ZJBBFA202512150032，由华信咨询设计研究院代理采购。公告未披露具体采购金额及部署数量。该部署是四足机器人在电信运营商数据中心机房巡检场景的典型应用案例。`,
  '杭州云深处科技股份有限公司||浙江省特种设备科学研究院': `云深处四足机器人在浙江省特种设备科学研究院的科研教育场景中执行特种设备检验装备作业与检测任务验证。该机器人可进入狭小空间、高空平台等人工难以到达的区域，辅助完成特种设备外观检查与数据采集。合同金额73.4万元，采购数量1台，通过公开招标方式确定供应商，合同于2026年1月6日正式签署，履约期限90天，交付地点为杭州。该采购是四足机器人技术在特种设备检验检测领域的首次科研验证应用。`,
  '灵心巧手（北京）科技有限公司||广州市城投低空产业投资有限公司': `灵心巧手电子钢琴机器人在广州市城投低空产业投资有限公司海心沙体验中心机器人馆执行文旅展演与互动体验服务任务。该机器人具备钢琴演奏能力，可完成多曲目的自动弹奏演示，支持游客点歌互动。本次采购包含电子钢琴机器人一套（含2台机器人及2台电子钢琴），成交金额25万元，于2026年3月完成中标交付。机器人馆面向公众开放，为游客提供机器人音乐演奏演示与互动体验服务，是音乐机器人在文旅展示场景的创新应用。`,
  '节卡机器人股份有限公司||中国第一汽车股份有限公司': `节卡机器人自动检测设备在中国第一汽车股份有限公司P567项目汽车产线中执行车架号自动识别与检测任务。该设备集成机器视觉系统与自动化机械臂，可对汽车生产过程中的车架号进行自动扫描、识别与核验，替代传统人工逐一比对操作。设备部署于长春生产基地，项目编号PA-20260112-0017。该应用提升整车生产线的质量管控效率与追溯准确性，是协作机器人在汽车制造质量检测环节的典型落地场景。`,
  '节卡机器人股份有限公司||中国计量大学': `节卡MiniCobo工业级协作机器人部署于中国计量大学智能机器人与计量检测实验室，执行机器人运动控制与计量检测实验教学任务。本次采购7套机器人配合6套嵌入式ROS实验开发平台共同构建实验教学环境，合同金额49.86万元，含运输、安装、调试及3年质保服务。供应商须在合同签订45日内完成交付验收。该批设备支撑学校开展机器人编程、运动控制、视觉检测等课程实验，培养智能制造领域应用型人才。`,
  '深圳市优必选科技股份有限公司||温州市鹿城区教育局': `优必选教育机器人在温州市鹿城区中小学人工智能教育实验项目中执行AI教学辅助与编程教育任务。项目覆盖鹿城区多所中小学校，为学生提供人工智能基础知识教学、图形化编程实践及机器人竞赛培训服务。中标金额约7979.94万元，是2026年一季度教育机器人领域较大规模的政府采购项目之一。该项目推动人工智能教育在温州基础教育阶段的普及，为中小学生提供接触前沿机器人技术的实践平台。`,
  '数字华夏（深圳）科技有限公司||南山区工业和信息化局': `数字华夏咨询机器人拟在深圳市南山区住院病区中执行床旁宣教与健康咨询服务任务，为住院患者提供疾病知识普及、用药指导、康复建议及问题解答服务。该项目为深圳南山区2025年第二批机器人应用场景【揭榜挂帅】项目，由数字华夏于2026年3月成功揭榜，目前处于公示阶段。合同金额及具体部署规模尚未披露，实际交付与部署情况需待合同签署后进一步确认，是医疗机器人在住院服务场景的应用探索。`,
  '深圳优艾智合机器人科技有限公司||润电能源科学技术有限公司||赤壁||2026': `优艾智合巡检可视化辅助系统在润电能源科学技术有限公司蒲圻三期智慧电厂中执行发电设备自动巡检与状态监测任务。系统部署于湖北赤壁蒲圻三期电厂，覆盖汽轮机、发电机、锅炉等关键区域设备运行状态的可视化监控与智能巡检，通过高清摄像与红外热成像实现设备异常识别。中标金额415.72万元，经公开招标采购完成。该系统替代人工定期巡检作业，提升电厂运维安全性与巡检效率，是巡检机器人在火电行业的规模化应用案例。`,
  '深圳优艾智合机器人科技有限公司||中国大唐集团科学技术研究总院有限公司水电科学研究院': `优艾智合变压器巡检机器人在中国大唐集团水电科学研究院的电力科研场景中执行变压器设备自动巡检与状态评估任务。机器人搭载可见光与红外视觉传感器，可自主完成设备外观检查、表计读取、热成像检测及异常状态识别。本项目通过公开询比采购方式，由福建省海峡智汇科技有限公司以43.8万元中选，共有10家供应商参与报价竞争。该应用提升电力设施巡检效率与人员安全保障水平，是机器人在水电科研检测领域的首次探索部署。`,
  '深圳优艾智合机器人科技有限公司||新疆中泰化学阜康能源有限公司': `优艾智合巡检机器人在新疆中泰化学阜康能源有限公司化工生产厂区电气区域执行自动化安全巡检任务。机器人承担厂区变电站、配电室等电气区域的设备状态监测、温湿度检测与异常预警工作，实现全天候无人值守巡检。本次采购合同金额135.13万元，通过公开招标完成采购。该项目系该化工能源企业推进电气区域智能化运维的落地项目，为高危化工环境的无人化巡检提供解决方案。`,
  '广东华沿机器人股份有限公司||华中科技大学电气与电子工程学院': `华沿S30桁架机器人在华中科技大学电气与电子工程学院实验室执行涂层样品自动化空间定位与成像配合任务。该机器人工作半径800mm，负载能力30kg，重复定位精度±0.05mm，为在线式涂层整体成像系统提供精确机械运动支撑。本次采购1台S30型桁架机器人，合同总金额29.74万元，由深圳市吉诺特科技有限公司供货。合同采用分阶段付款机制，以验收合格为放款前提确保设备性能达标交付，支撑学院涂层质量分析相关科研工作。`,
  '微分智飞（杭州）科技有限公司||香港科技大学（广州）': `微分智飞非凸α自主无人机科研平台在香港科技大学（广州）科研教育场景中执行无人机自主飞行控制与集群协同算法验证任务。该平台具备自主导航、避障感知与编队飞行能力，为高校科研团队提供无人机自主化算法研究与测试载体。本次采购共4架，通过网上竞价方式成交，合同金额14.36万元，质保期1年。该批设备支撑学校在无人机控制、多机协同、智能感知等方向的教学实验与科研创新工作。`,
};

/**
 * 查找人工覆写文本：先尝试精确匹配（企业+需求方+城市+时间），再尝试简单匹配（企业+需求方）
 */
function findManualOverwrite(row) {
  const keyFull = `${row['机器人企业']}||${row['场景需求方']}||${row['部署城市']}||${row['部署时间']}`;
  if (MANUAL_OVERWRITES[keyFull]) return MANUAL_OVERWRITES[keyFull];
  const keySimple = `${row['机器人企业']}||${row['场景需求方']}`;
  return MANUAL_OVERWRITES[keySimple] || null;
}

// ── Step 3: 案例详情 LLM 质检 + 案例简介生成 ────────────────────────────────────

const DETAIL_SYSTEM_PROMPT = `你是具身智能产业数据库的案例详情编辑。

## 任务
1. 判断案例详情是否符合规范，如不符合则重写。
2. 生成一句话"案例简介"（30-60字）。

## 写作目的
以该中标项目为载体，如实简要地说明具身智能机器人当前的应用场景与应用水平，反映行业落地程度。

## 案例详情规范
- 字数：150-250字（含标点）
- 四段式结构：
  ① [型号] 在 [需求方] 的 [场景] 中执行 [任务]
  ② 关键技术参数或部署规模
  ③ 可量化效果指标（无则省略此段）
  ④ 首次/最大/里程碑标志性意义（无则省略此段）
- 删去：合同编号、交货期、质保条款、供货商/中间商信息（如"经XX公司供货"）、采购方式/编号/代理公司、公司介绍、行业宏观叙述、"标志着"类判断语句、成交金额/合同金额（金额已有独立字段记录）
- 未披露的信息直接省略，不写"型号未披露/金额未披露/部署数量未披露/效果暂无"等负面说明
- 不要以"XX公司中标…"开头，直接从机器人或需求方切入
- 优先填充量化指标（成功率、效率提升、台数、金额）

## 案例简介规范
- 字数：30-60字，一两句话
- 只保留核心信息：什么机器人 + 在什么需求方/场景 + 承担什么任务
- 去掉所有技术参数、数量、金额、采购流程等细节

### 案例简介示例
- "宇树G1edu-U2-ZL人形机器人在深圳大学科研教育场景中提供教学与科研支持。"
- "智元灵犀X2旗舰版机器人部署于招商银行上海分行数字金融展厅，承担展厅讲解引导任务。"
- "云深处机器狗巡检套件在杭州地区电力场景中承担自主巡检任务。"

## 输出格式（严格JSON）
{
  "pass": true/false,
  "reason": "通过原因 或 不通过原因（一句话）",
  "rewritten": "重写后的案例详情（仅在 pass=false 时填写，否则填 null）",
  "summary": "30-60字案例简介（必填）"
}

不要输出 JSON 以外的任何内容。`;

const SUMMARY_ONLY_PROMPT = `你是具身智能产业数据库的案例简介编辑。根据案例详情生成一句话案例简介。

## 案例简介规范
- 字数：30-60字，一两句话
- 只保留核心信息：什么机器人 + 在什么需求方/场景 + 承担什么任务
- 去掉所有技术参数、数量、金额、采购流程等细节

## 示例
- "宇树G1edu-U2-ZL人形机器人在深圳大学科研教育场景中提供教学与科研支持。"
- "智元灵犀X2旗舰版机器人部署于招商银行上海分行数字金融展厅，承担展厅讲解引导任务。"
- "云深处机器狗巡检套件在杭州地区电力场景中承担自主巡检任务。"

只输出案例简介文本，不要输出其他内容。`;

function parseDetailResult(raw) {
  const jsonMatch = raw.match(/\{[\s\S]*\}/);
  if (!jsonMatch) throw new Error(`LLM 返回格式非 JSON: ${raw.slice(0, 200)}`);
  const str = jsonMatch[0];

  try {
    return JSON.parse(str);
  } catch (e) {
    // Fallback: reason/rewritten/summary 里可能含未转义双引号，逐字段提取
    const passMatch = str.match(/"pass"\s*:\s*(true|false)/);
    if (!passMatch) throw new Error(`JSON 解析失败且无法提取 pass 字段: ${e.message}`);
    const pass = passMatch[1] === 'true';

    const reasonMatch = str.match(/"reason"\s*:\s*"([\s\S]*?)"\s*,\s*"rewritten"/);
    const reason = reasonMatch ? reasonMatch[1] : '';

    let rewritten = null;
    if (!/"rewritten"\s*:\s*null/.test(str)) {
      const rwMatch = str.match(/"rewritten"\s*:\s*"([\s\S]*?)"\s*,\s*"summary"/);
      rewritten = rwMatch ? rwMatch[1] : null;
    }

    const summaryMatch = str.match(/"summary"\s*:\s*"([\s\S]*?)"\s*\}?\s*$/);
    const summary = summaryMatch ? summaryMatch[1] : '';

    return { pass, reason, rewritten, summary };
  }
}

function normalizeInlineText(value) {
  return String(value || '')
    .replace(/\s*\r?\n\s*/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
}

function normalizeCompanyMentions(text, preferredName, companyNameMap) {
  let normalized = normalizeInlineText(text);
  if (!preferredName) return normalized;

  for (const [fullName, shortName] of companyNameMap.entries()) {
    if (shortName === preferredName && fullName && fullName !== preferredName) {
      normalized = normalized.split(fullName).join(preferredName);
    }
  }

  return normalized;
}

async function checkAndRewriteDetail(record) {
  const userContent = `
机器人企业: ${record['机器人企业']}
需求方: ${record['场景需求方']}
场景: ${record['一级场景']}-${record['二级场景']}
机器人型号: ${record['机器人型号']}
部署时间: ${record['部署时间']}
金额(万元): ${record['金额(万元)']}
链接: ${record['链接']}

原案例详情:
${record['案例详情']}
`.trim();

  const raw = await callLLM(DETAIL_SYSTEM_PROMPT, userContent);
  const parsed = parseDetailResult(raw);
  return {
    ...parsed,
    reason: normalizeInlineText(parsed.reason),
    rewritten: parsed.rewritten ? normalizeInlineText(parsed.rewritten) : null,
    summary: normalizeInlineText(parsed.summary),
  };
}

async function generateSummaryOnly(record) {
  const userContent = `
机器人企业: ${record['机器人企业']}
需求方: ${record['场景需求方']}
场景: ${record['一级场景']}-${record['二级场景']}

案例详情:
${record['案例详情']}
`.trim();

  const raw = await callLLM(SUMMARY_ONLY_PROMPT, userContent);
  return normalizeInlineText(raw.trim().replace(/^["']|["']$/g, ''));
}

// ── 主流程 ───────────────────────────────────────────────────────────────────

async function main() {
  logger.info('=== Ingest: 规范核实 & 入库 ===');

  const inputRows = readCsv(INPUT_CSV);
  logger.info(`读入 ${inputRows.length} 条记录`);

  // 加载现有数据库（去重用）
  const existingKeys = loadExistingDb();
  logger.info(`现有数据库共 ${existingKeys.size} 条去重 key`);

  // 加载企业简称映射 & 发布日期兜底映射
  const companyNameMap = loadCompanyNameMap();
  logger.info(`企业简称映射: ${companyNameMap.size} 条`);
  const publishDateMap = loadPublishDateMap();
  logger.info(`发布日期映射: ${publishDateMap.size} 条`);

  const progress = loadProgress();
  const completedKeys = new Set(progress.completed);

  const finalRecords   = [];
  const reportLines    = ['# Ingest 处置报告\n'];
  const stats = { pass: 0, dedup: 0, fieldFixed: 0, detailRewritten: 0, manualOverwrite: 0, warn: 0 };

  for (let i = 0; i < inputRows.length; i++) {
    const row = inputRows[i];
    const company  = row['机器人企业'] || '';
    const demand   = row['场景需求方'] || '';
    const time     = row['部署时间'] || '';
    const key      = buildDedupeKey(company, demand, time);
    const label    = `[${i + 1}/${inputRows.length}] ${company} | ${demand}`;

    logger.info(label);

    // ── Step 0: 去重 ──────────────────────────────────────────────────────
    if (existingKeys.has(key)) {
      logger.warn(`  去重跳过（已在数据库中）`);
      reportLines.push(`## ${label}\n- **处置：去重跳过**（现有数据库已有相同记录）\n`);
      stats.dedup++;
      continue;
    }

    // ── 企业简称映射 ─────────────────────────────────────────────────────
    if (companyNameMap.has(row['机器人企业'])) {
      row['机器人企业'] = companyNameMap.get(row['机器人企业']);
    }

    // ── Step 1: 字段修正 ─────────────────────────────────────────────────
    const { record, fixes } = fixFields(row);

    // ── 部署时间兜底（项目详情无时间则用发布日期）────────────────────────
    if (!record['部署时间'] || record['部署时间'].trim() === '') {
      const link = record['链接'] || '';
      const fallback = formatPublishDate(publishDateMap.get(link) || '');
      if (fallback) {
        record['部署时间'] = fallback;
        fixes.push(`部署时间空→发布日期兜底: "${fallback}"`);
      }
    }

    // ── 数据源统一简写 ──────────────────────────────────────────────────
    record['数据源'] = '天眼查';
    if (fixes.length > 0) {
      stats.fieldFixed++;
      fixes.forEach(f => logger.warn(`  字段修正: ${f}`));
    }

    // ── Step 2 & 3: 人工覆写 / LLM 质检 + 简介生成 ──────────────────────
    let caseSummary = '';
    let detailNote = '';

    if (completedKeys.has(key)) {
      // 断点续跑：从 progress 恢复 caseSummary
      caseSummary = progress.summaries[key] || '';
      logger.info(`  已质检，跳过 LLM（简介${caseSummary ? '已恢复' : '无缓存'}）`);
      detailNote = '（断点续跑跳过）';
    } else {
      const manualDetail = findManualOverwrite(record);

      if (manualDetail) {
        // 人工覆写：直接使用预设文本，仅调 LLM 生成案例简介
        record['案例详情'] = manualDetail;
        stats.manualOverwrite++;
        logger.info(`  案例详情已人工覆写（${manualDetail.length}字）`);

        try {
          caseSummary = await generateSummaryOnly(record);
          logger.info(`  案例简介已生成: ${caseSummary}`);
        } catch (err) {
          logger.error(`  案例简介生成失败: ${err.message}`);
          stats.warn++;
        }

        detailNote = `🔧 人工覆写（${manualDetail.length}字）`;
        progress.completed.push(key);
        progress.summaries[key] = caseSummary;
        saveProgress(progress);
      } else {
        // LLM 质检：详情质检 + 简介生成
        try {
          const detailResult = await checkAndRewriteDetail(record);
          if (!detailResult.pass && detailResult.rewritten) {
            record['案例详情'] = detailResult.rewritten;
            stats.detailRewritten++;
            logger.info(`  案例详情重写: ${detailResult.reason}`);
            detailNote = `✏️ 案例详情已重写: ${detailResult.reason}`;
          } else {
            logger.info(`  案例详情通过: ${detailResult.reason}`);
            detailNote = `✅ 案例详情通过`;
          }
          caseSummary = detailResult.summary || '';
          if (caseSummary) {
            logger.info(`  案例简介: ${caseSummary}`);
          }
          progress.completed.push(key);
          progress.summaries[key] = caseSummary;
          saveProgress(progress);
        } catch (err) {
          logger.error(`  案例详情质检失败: ${err.message}`);
          progress.failed.push({ key, error: err.message });
          saveProgress(progress);
          stats.warn++;
          detailNote = `❌ 质检失败: ${err.message}`;
        }
      }
    }

    caseSummary = normalizeCompanyMentions(caseSummary, row['机器人企业'], companyNameMap);
    record['案例详情'] = normalizeCompanyMentions(record['案例详情'], row['机器人企业'], companyNameMap);

    // 更新入库时间
    record['入库时间'] = new Date().toISOString().replace('Z', '+08:00').replace(/\.\d{3}/, '');

    // 映射到 HEADERS id
    finalRecords.push({
      primaryScene:   record['一级场景'],
      secondaryScene: record['二级场景'],
      demandSide:     record['场景需求方'],
      robotCompany:   record['机器人企业'],
      deployCity:     record['部署城市'],
      robotModel:     record['机器人型号'],
      projectName:    record['项目名'] || '-',
      deployTime:     record['部署时间'],
      amount:         record['金额(万元)'],
      caseSummary:    caseSummary,
      caseDetail:     record['案例详情'],
      deployStatus:   record['部署状态'],
      dataSource:     record['数据源'],
      link:           record['链接'],
      parentRecord:   record['父记录'],
      ingestTime:     record['入库时间'],
    });

    stats.pass++;

    // 报告行
    const fixNote = fixes.length > 0 ? `\n- 字段修正: ${fixes.join('；')}` : '';
    reportLines.push(`## ${label}\n- 状态: ${record['部署状态']}\n- ${detailNote}${fixNote}\n`);
  }

  // ── 写出结果 ──────────────────────────────────────────────────────────────
  await writeCsv(OUTPUT_CSV, HEADERS, finalRecords);

  // 写报告
  reportLines.push(`---\n## 汇总\n- 通过入库: ${stats.pass}\n- 去重跳过: ${stats.dedup}\n- 字段修正: ${stats.fieldFixed} 条\n- 案例详情重写: ${stats.detailRewritten} 条\n- 人工覆写: ${stats.manualOverwrite} 条\n- 质检警告: ${stats.warn} 条\n`);
  fs.writeFileSync(REPORT_FILE, reportLines.join('\n'), 'utf-8');

  logger.info('=== Ingest 完成 ===');
  logger.info(`通过入库: ${stats.pass} | 去重跳过: ${stats.dedup} | 详情重写: ${stats.detailRewritten} | 人工覆写: ${stats.manualOverwrite} | 警告: ${stats.warn}`);
  logger.info(`最终文件: ${OUTPUT_CSV}`);
  logger.info(`处置报告: ${REPORT_FILE}`);
}

main().catch(err => {
  logger.error(`Ingest 异常退出: ${err.message}`);
  process.exit(1);
});
