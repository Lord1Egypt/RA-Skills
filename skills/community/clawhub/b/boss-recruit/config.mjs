/**
 * Boss 招聘 Skill 配置
 * 字段选项 / 话术 / 节奏参数。按需改这里。
 *
 * ⚠️ 飞书"同步到哪张表"不在这里硬编码 —— 由 `node scenarios/setup.mjs <飞书表链接>`
 *    解析并存到 ~/.opencli/boss-recruit/target.json（见 lib/target.mjs）。
 */

/** 应聘岗位 select 的合法选项（job_name 命中才写，避免误建新选项）。 */
export const POSITION_OPTIONS = new Set([
  '数据分析师', '产品经理', 'AI 算法工程师', '运维工程师',
  '前端开发工程师', '后端开发工程师', '策略产品经理',
]);

/** 当前阶段 select 选项映射（状态机 → 飞书阶段）。 */
export const STAGE = {
  pending: '新简历',
  resume_read: '新简历',
  attachment_requested: '新简历',
  synced: '通过初筛',
  rejected: '不匹配',
};

/** 称呼：性别已知 → 姓+先生/女士您好；未知 → 您好（不冒险误称）。 */
function addr(c) {
  if (c.name && (c.gender === '男' || c.gender === '女')) {
    return `${c.name[0]}${c.gender === '女' ? '女士' : '先生'}您好`;
  }
  return '您好';
}

/**
 * 要简历话术（调性：简洁专业 —— 稳重、给理由、不推销）。
 * 3 条同调性变体，逐人轮换，避免千篇一律触发风控。性别由 profile 传入。
 */
export const RESUME_REQUEST_TEMPLATES = [
  (c) => `${addr(c)}，看到您对${c.job_name || '这个岗位'}有意向，想更全面地了解一下您的背景，方便发一份附件简历（PDF）给我吗？我看完尽快跟您沟通后续。`,
  (c) => `${addr(c)}，您应聘的${c.job_name || '这个岗位'}和我们这边挺匹配，为了更全面地评估，方便发一份附件简历（PDF 优先）给我吗？我看后尽快和您同步进展。`,
  (c) => `${addr(c)}，想进一步了解您在${c.job_name || '相关'}方向的经历，麻烦您发一份完整的附件简历给我，PDF 格式最好，我看完会尽快给您反馈。`,
];

/** 节奏参数（覆盖 rhythm.DEFAULTS）。 */
export const RHYTHM = {
  delayMinSec: 25,
  delayMaxSec: 70,
  roundLimit: 5,      // 单轮最多处理/打招呼人数
  checkEvery: 3,
};

export const SESSION = 'boss';     // 默认 browser session 名
export const RESUME_SOURCE = 'BOSS直聘';
