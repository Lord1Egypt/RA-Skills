#!/usr/bin/env node
/**
 * chudaxia-ai-coach / scripts/transcribe-interview-to-scene-card.js
 *
 * 将结构化业务场景访谈录音转录文本 转换为 场景选题卡内容
 *
 * 输入：遵循 interview-outline.md 大纲格式的访谈转录文本
 * 输出：JSON格式的选题卡数据（可直接填入 scene-card-template.md）
 *
 * 用法：
 *   node transcribe-interview-to-scene-card.js --input interview.txt [--output card.json]
 *
 * 处理流程：
 *   1. 读取访谈转录文本
 *   2. 按五层大纲解析关键信息
 *   3. 映射到选题卡五维评估体系
 *   4. 输出结构化JSON
 */

const fs = require('fs');
const path = require('path');

const args = process.argv.slice(2);
const inputIdx = args.indexOf('--input');
const outputIdx = args.indexOf('--output');
const printIdx = args.indexOf('--print');

const config = {
  inputFile: inputIdx !== -1 ? args[inputIdx + 1] : null,
  outputFile: outputIdx !== -1 ? args[outputIdx + 1] : null,
  print: printIdx !== -1,
};

function parseInterview(text) {
  const lines = text.split('\n').filter(l => l.trim());
  const result = {
    company: '',
    position: '',
    department: '',
    deptWork: '',
    posWork: '',
    topTask: {
      name: '',
      knowledge: '',
      experience: '',
      value: '',
    },
    taskProcess: {
      input: { dept: '', content: '' },
      steps: [],
      references: '',
      output: '',
    },
    compliance: {
      approver: '',
      forbidden: '',
    },
    repetitiveWork: {
      task: '',
      timePercent: '',
      desiredAction: '',
      valuableTask: '',
    },
  };

  let stage = 'meta';
  const stepAccum = [];

  for (const line of lines) {
    const t = line.trim();

    // Level 1: 岗位画像
    if (t.includes('我是') && t.includes('公司的员工')) {
      const m = t.match(/我是(.+?)公司的员工/);
      if (m) result.company = m[1].trim();
      continue;
    }
    if (t.startsWith('岗位名称是')) {
      result.position = t.replace('岗位名称是', '').trim();
      continue;
    }
    if (t.startsWith('属于') && t.includes('部门')) {
      result.department = t.replace('属于', '').replace('部门', '').trim();
      continue;
    }
    if (t.startsWith('我们部门主要工作是')) {
      result.deptWork = t.replace('我们部门主要工作是', '').trim();
      continue;
    }
    if (t.startsWith('我所属的岗位的主要工作是')) {
      result.posWork = t.replace('我所属的岗位的主要工作是', '').trim();
      continue;
    }

    // Level 2: 核心价值
    if (t.startsWith('其中业务价值最高的任务是')) {
      result.topTask.name = t.replace('其中业务价值最高的任务是', '').trim();
      stage = 'topTask';
      continue;
    }
    if (stage === 'topTask' && t.includes('核心知识')) {
      result.topTask.knowledge = t.replace(/.*核心知识和?/, '').replace(/和经验.*/, '').trim();
      continue;
    }
    if (stage === 'topTask' && t.includes('经验')) {
      result.topTask.experience = t.replace(/.*经验/, '').trim();
      continue;
    }
    if (stage === 'topTask' && t.includes('能够为企业带来')) {
      result.topTask.value = t.replace('能够为企业带来', '').replace('价值', '').trim();
      stage = 'process';
      continue;
    }

    // Level 3: 业务流程
    if (t.startsWith('这个任务输入是')) {
      const m = t.match(/输入是(.+?)(?:部门|外部).*提供/);
      if (m) result.taskProcess.input.dept = m[1].trim();
      const c = t.replace(/这个任务输入是.+?提供/, '').trim();
      result.taskProcess.input.content = c;
      continue;
    }
    if (/^第[一二三四五六七八九十\d]步/.test(t)) {
      stepAccum.push(t);
      continue;
    }
    if (t.startsWith('任务执行过程中需要依据')) {
      result.taskProcess.references = t.replace('任务执行过程中需要依据', '').trim();
      continue;
    }
    if (t.startsWith('任务执行结果输出是')) {
      result.taskProcess.output = t.replace('任务执行结果输出是', '').trim();
      continue;
    }

    // Level 4: 合规
    if (t.includes('需要经过') && (t.includes('确认') || t.includes('审批'))) {
      result.compliance.approver = t.replace(/.*需要经过/, '').replace(/进行确认.*/, '').replace(/进行审批.*/, '').trim();
      continue;
    }
    if (t.includes('绝对不能违背')) {
      result.compliance.forbidden = t.replace(/.*绝对不能违背/, '').trim();
      continue;
    }

    // Level 5: 机械化任务
    if (t.includes('重复性') || t.includes('机械性') || t.includes('占用') && t.includes('时间')) {
      const m = t.match(/(重复性|机械性|技能型)的(.+?)任务/);
      if (m) result.repetitiveWork.task = m[2].trim();
      const p = t.match(/占用\s*([\d%]+)\s*以上/);
      if (p) result.repetitiveWork.timePercent = p[1];
      continue;
    }
    if (t.includes('希望公司能够')) {
      result.repetitiveWork.desiredAction = t.replace('希望公司能够', '').replace('处理', '').trim();
      continue;
    }
    if (t.includes('让我有更多时间处理')) {
      result.repetitiveWork.valuableTask = t.replace('让我有更多时间处理', '').replace('任务', '').trim();
      continue;
    }
  }

  result.taskProcess.steps = stepAccum;
  return result;
}

function buildSceneCard(parsed) {
  // Determine AI intervention type
  const aiTypes = [];
  const text = [
    parsed.topTask.name,
    parsed.posWork,
    parsed.taskProcess.output,
    parsed.repetitiveWork.task,
  ].join(' ');

  if (/生成|撰写|创作|内容|文案|文章/.test(text)) aiTypes.push('内容生成');
  if (/搜索|查询|检索|知识|FAQ|问答|文档/.test(text)) aiTypes.push('知识检索与问答（RAG）');
  if (/分析|预测|报表|统计|数据/.test(text)) aiTypes.push('数据分析与预测');
  if (/流程|审批|调度|分配|通知|发送/.test(text)) aiTypes.push('流程自动化 / 智能体');
  if (/识别|检测|质检|图片|图像/.test(text)) aiTypes.push('图像识别 / 视觉质检');
  if (/客服|咨询|问答|售后/.test(text)) aiTypes.push('智能客服与交互');
  if (aiTypes.length === 0) aiTypes.push('流程自动化 / 智能体');

  // Assess scores based on detail richness
  const valueScore = parsed.topTask.value ? (parsed.topTask.value.includes('万') || parsed.topTask.value.includes('亿') ? 5 : 4) : 3;
  const stepsDetail = parsed.taskProcess.steps.length;
  const techScore = stepsDetail >= 3 ? 4 : stepsDetail >= 1 ? 3 : 2;
  const dataScore = parsed.taskProcess.input.content ? 4 : 2;
  const orgScore = parsed.compliance.approver ? 3 : 4;

  return {
    sceneName: parsed.topTask.name || parsed.posWork,
    department: parsed.department,
    painPoint: `当前流程：${parsed.posWork}。其中业务价值最高的任务是「${parsed.topTask.name}」，依赖${parsed.topTask.knowledge}核心知识和${parsed.topTask.experience}经验。`,
    aiDirections: aiTypes,
    assessment: {
      businessValue: { score: valueScore, note: parsed.topTask.value || '核心业务职责' },
      techFeasibility: { score: techScore, note: `流程可拆分为${stepsDetail}个步骤` },
      dataReadiness: { score: dataScore, note: parsed.taskProcess.input.content ? '有明确数据输入' : '需进一步确认数据来源' },
      orgReadiness: { score: orgScore, note: parsed.compliance.approver ? `需经过${parsed.compliance.approver}审批` : '可直接推进' },
    },
    repetitiveFinding: parsed.repetitiveWork.task
      ? `${parsed.repetitiveWork.task}（占用${parsed.repetitiveWork.timePercent || '大量'}时间）→ 建议AI自动化处理`
      : '未识别到明显机械化任务',
    recomendedAction: valueScore >= 4 && techScore >= 3 ? '可直接进入PoC验证' : '需要进一步调研确认',
  };
}

// ── Main ──
if (!config.inputFile) {
  // Demo mode with structured input example
  const demoInput = [
    '我是XX制造业公司的员工',
    '岗位名称是质检主管',
    '属于质量管理部门',
    '我们部门主要工作是产品质量检验和质量管理体系维护',
    '我所属的岗位的主要工作是制定检验标准、管理质检团队、处理质量异常',
    '',
    '其中业务价值最高的任务是新产品首件检验标准制定',
    '这个任务的决策或产出依赖我们部门和岗位员工的产品工艺核心知识和历史质量数据分析经验',
    '能够为企业带来降低批量质量事故风险的百万级价值',
    '',
    '这个任务输入是研发部门提供的产品图纸和技术规范文档',
    '第一步是分析产品图纸理解关键尺寸和技术要求',
    '第二步是查阅同类产品的历史检验标准和不良记录',
    '第三步是根据产品特性和历史数据制定检验项目和抽样方案',
    '第四步是编制检验作业指导书并培训质检员',
    '任务执行过程中需要依据ISO9001质量管理体系规范和行业检验标准',
    '任务执行结果输出是检验作业指导书和检验记录表模板',
    '',
    '这个任务的输出结果需要经过质量经理和技术部主管进行确认和会签',
    '其中绝对不能违背产品安全相关的强制性标准和法规要求',
    '',
    '在每周的工作中，重复性/机械性的检验数据录入和报告模板制作任务占用30%以上的时间',
    '完全不需要动脑，只需要动手即可',
    '希望公司能够用AI工具自动生成检验报告模板和数据分析图表处理',
    '让我有更多时间处理对公司业务最有价值的质量异常分析和流程优化的任务',
  ].join('\n');

  const parsed = parseInterview(demoInput);
  const card = buildSceneCard(parsed);

  const output = {
    parsed,
    sceneCard: card,
    _note: '这是基于结构化访谈生成的示例输出。使用 --input 传入真实访谈转录文件。',
  };

  console.log(JSON.stringify(output, null, 2));
  process.exit(0);
}

// ── File mode ──
try {
  const text = fs.readFileSync(config.inputFile, 'utf-8');
  const parsed = parseInterview(text);
  const card = buildSceneCard(parsed);

  const output = { parsed, sceneCard: card };

  if (config.outputFile) {
    fs.writeFileSync(config.outputFile, JSON.stringify(output, null, 2), 'utf-8');
    console.log(`✅ 选题卡已生成: ${config.outputFile}`);
  } else {
    console.log(JSON.stringify(output, null, 2));
  }
} catch (err) {
  console.error(`❌ 错误: ${err.message}`);
  process.exit(1);
}
