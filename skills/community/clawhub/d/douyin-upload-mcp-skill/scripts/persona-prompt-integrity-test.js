#!/usr/bin/env node
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { dirname, join } from 'node:path';

const ROOT = new URL('..', import.meta.url).pathname;
const PROMPT_PATH = join(ROOT, 'references/persona-positioning-prompt.md');
const DEFAULT_REPORT_PATH = join(process.env.HOME || '.', '.openclaw', 'workspace', 'douyin-ops-tests', 'persona-prompt-integrity.json');

function parseArgs(argv) {
  const args = {};
  for (let i = 0; i < argv.length; i += 1) {
    const item = argv[i];
    if (!item.startsWith('--')) continue;
    const key = item.slice(2).replace(/-([a-z])/g, (_, c) => c.toUpperCase());
    const next = argv[i + 1];
    if (!next || next.startsWith('--')) args[key] = true;
    else {
      args[key] = next;
      i += 1;
    }
  }
  return args;
}

function includesAll(text, items) {
  return items.filter((item) => !text.includes(item));
}

function main() {
  const args = parseArgs(process.argv.slice(2));
  const prompt = readFileSync(PROMPT_PATH, 'utf8');
  const required = [
    'IP人设定位方案生成Prompt',
    '角色与核心任务',
    '你是顶尖全行业个人IP战略顾问',
    '核心任务是根据用户提供的信息，生成《IP人设定位方案》',
    '二、《IP人设定位方案》输出规范',
    '1. IP核心定位（整合精简，避免重复）',
    '2. 精准用户画像（按多个人群拆分，简化冗余）',
    '3. 账号全套定位资料（基础资料）',
    '* 姓名/昵称：{{name}}',
    '* 性别：{{sex}}',
    '* 从业/深耕年限：{{work_year}}年',
    '* 核心业务/主营服务：{{bissiness}}',
    '* 核心优势/差异化竞争力：{{advantage}}',
    '* 目标客户/精准受众（原始描述）：{{segment}}',
    '* 个人特质/性格优势：{{trials}}',
    '* 过往相关经验/案例：{{cases}}',
    '* IP核心诉求：{{demand}}',
    '* 禁忌与偏好：{{taboos}}',
    '* 账号名称：含姓名/昵称+核心业务关键词，好记易搜',
    '* 4. 行动引导：私信/咨询/领取干货等明确指引',
  ];
  const forbidden = [
    '自动化营销系统补充要求',
    'modelId',
    'vhBizId',
    '数字人形象生成暂不内置',
    '当前主流程不内置',
    '绑定数字人ID',
  ];
  const missing = includesAll(prompt, required);
  const leaked = forbidden.filter((item) => prompt.includes(item));
  const summary = {
    ok: missing.length === 0 && leaked.length === 0,
    promptPath: PROMPT_PATH,
    requiredChecked: required.length,
    missing,
    forbiddenChecked: forbidden.length,
    leaked,
    length: prompt.length,
  };
  const reportPath = args.output || DEFAULT_REPORT_PATH;
  mkdirSync(dirname(reportPath), { recursive: true });
  writeFileSync(reportPath, `${JSON.stringify(summary, null, 2)}\n`);
  console.log(JSON.stringify({ summary, reportPath }, null, 2));
  if (!summary.ok) process.exit(1);
}

main();
