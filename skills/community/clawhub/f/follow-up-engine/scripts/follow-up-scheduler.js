#!/usr/bin/env node

/**
 * Follow-up Scheduler - 自动跟进调度器
 * 
 * 功能：
 * 1. 读取 follow-up-strategies.json 获取各阶段的跟进序列
 * 2. 扫描 OKKI 客户数据，识别每个客户当前所处阶段
 * 3. 计算每个客户的下次跟进时间（基于阶段策略的 follow_up_sequence）
 * 4. 对到期需要跟进的客户，自动生成跟进邮件草稿
 * 5. 将草稿保存到指定目录，或创建 OKKI 跟进记录（draft 状态）
 * 6. 支持 dry-run 模式（预览将生成的草稿）
 * 7. 支持手动触发和定时触发两种模式
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// 配置路径
const CONFIG_DIR = path.join(__dirname, '..', 'config');
const STRATEGIES_FILE = path.join(CONFIG_DIR, 'follow-up-strategies.json');
const DRAFTS_DIR = path.join(__dirname, '..', 'drafts');
const LOGS_DIR = path.join(__dirname, '..', 'logs');

// 确保目录存在
[DRAFTS_DIR, LOGS_DIR].forEach(dir => {
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
});

// 日志工具
function log(message, level = 'INFO') {
  const timestamp = new Date().toISOString();
  const logLine = `[${timestamp}] [${level}] ${message}`;
  console.log(logLine);
  
  // 写入日志文件
  const logFile = path.join(LOGS_DIR, `scheduler-${new Date().toISOString().split('T')[0]}.log`);
  fs.appendFileSync(logFile, logLine + '\n');
}

// 加载配置文件
function loadStrategies() {
  if (!fs.existsSync(STRATEGIES_FILE)) {
    throw new Error(`配置文件不存在：${STRATEGIES_FILE}`);
  }
  const content = fs.readFileSync(STRATEGIES_FILE, 'utf8');
  return JSON.parse(content);
}

// 检查工作时间内
function isWorkingHours(settings) {
  const now = new Date();
  const tz = settings.timezone || 'Asia/Shanghai';
  
  // 简单实现：使用系统时间（实际应使用时区转换）
  const hours = now.getHours();
  const minutes = now.getMinutes();
  const dayOfWeek = now.getDay(); // 0 = Sunday, 6 = Saturday
  
  const [startHour, startMin] = settings.start.split(':').map(Number);
  const [endHour, endMin] = settings.end.split(':').map(Number);
  
  const currentTime = hours * 60 + minutes;
  const startTime = startHour * 60 + startMin;
  const endTime = endHour * 60 + endMin;
  
  if (settings.exclude_weekends && (dayOfWeek === 0 || dayOfWeek === 6)) {
    return false;
  }
  
  return currentTime >= startTime && currentTime <= endTime;
}

// 计算下次跟进日期
function calculateNextFollowUpDate(lastContactDate, followUpSequence, followUpIndex) {
  if (!lastContactDate || followUpIndex >= followUpSequence.length) {
    return null;
  }
  
  const daysToAdd = followUpSequence[followUpIndex];
  const nextDate = new Date(lastContactDate);
  nextDate.setDate(nextDate.getDate() + daysToAdd);
  
  return nextDate;
}

// 获取客户当前跟进索引
function getFollowUpIndex(customer, strategy) {
  // 从客户数据中获取已完成的跟进次数
  // 实际实现需要从 OKKI 或本地记录中读取
  return customer.follow_up_count || 0;
}

// 模拟 OKKI 客户数据扫描（实际实现需调用 OKKI API）
function scanOKKICustomers() {
  log('扫描 OKKI 客户数据...');
  
  // 模拟数据 - 实际实现应调用 OKKI API
  // 参考 task-002 的 OKKI 同步接口
  const mockCustomers = [
    {
      id: 'okki_001',
      name: 'ABC Trading Ltd',
      email: 'contact@abctrading.com',
      stage: 'new_inquiry',
      last_contact_date: '2026-03-20',
      follow_up_count: 0,
      owner: 'wilson',
      product_interest: 'HDMI Cable'
    },
    {
      id: 'okki_002',
      name: 'XYZ Electronics',
      email: 'sales@xyzelec.com',
      stage: 'quoted',
      last_contact_date: '2026-03-18',
      follow_up_count: 1,
      owner: 'wilson',
      quote_number: 'QT-2026-0042',
      product_interest: 'DP Cable'
    },
    {
      id: 'okki_003',
      name: 'Global Tech Inc',
      email: 'purchasing@globaltech.com',
      stage: 'sample_sent',
      last_contact_date: '2026-03-22',
      follow_up_count: 0,
      owner: 'wilson',
      tracking_number: 'SF1234567890',
      product_interest: 'USB-C Cable'
    }
  ];
  
  log(`找到 ${mockCustomers.length} 个客户`);
  return mockCustomers;
}

// 生成邮件草稿
function generateEmailDraft(customer, template, strategy) {
  const now = new Date();
  const draftId = `draft-${now.toISOString().replace(/[:.]/g, '-')}-${customer.id}`;
  
  // 替换模板变量（安全替换，处理未定义变量）
  let subject = template.subject || '';
  const replacements = {
    '{product_name}': customer.product_interest || 'our products',
    '{company_name}': customer.name,
    '{quote_number}': customer.quote_number || '',
    '{tracking_number}': customer.tracking_number || '',
    '{customer_name}': customer.name,
    '{order_number}': customer.order_number || '',
    '{deadline_date}': '',
    '{expiry_date}': '',
    '{similar_company}': '',
    '{new_product_name}': '',
    '{seasonal_promotion}': ''
  };
  
  for (const [placeholder, value] of Object.entries(replacements)) {
    subject = subject.split(placeholder).join(value);
  }
  
  const draft = {
    draft_id: draftId,
    customer_id: customer.id,
    customer_name: customer.name,
    customer_email: customer.email,
    stage: customer.stage,
    template_id: template.template_id,
    intent: template.intent,
    subject: subject,
    body_key: template.body_key,
    tone: template.tone,
    follow_up_day: strategy.follow_up_sequence[customer.follow_up_count || 0],
    created_at: now.toISOString(),
    status: 'draft',
    owner: customer.owner
  };
  
  return draft;
}

// 保存草稿到文件
function saveDraft(draft) {
  const filename = `${draft.draft_id}.json`;
  const filepath = path.join(DRAFTS_DIR, filename);
  
  fs.writeFileSync(filepath, JSON.stringify(draft, null, 2), 'utf8');
  log(`草稿已保存：${filename}`);
  
  return filepath;
}

// 创建 OKKI 跟进记录（draft 状态）
function createOKKIFollowUpRecord(draft) {
  log(`[OKKI] 创建跟进记录（draft）：${draft.customer_id}`);
  
  // 实际实现应调用 OKKI API
  // 参考 task-002 的 OKKI 同步接口
  const record = {
    okki_record_id: `okki_fu_${Date.now()}`,
    customer_id: draft.customer_id,
    type: 'email_draft',
    status: 'draft',
    content: {
      subject: draft.subject,
      body_key: draft.body_key,
      template_id: draft.template_id
    },
    scheduled_date: new Date().toISOString(),
    owner: draft.owner
  };
  
  // 保存到本地（模拟 OKKI 记录）
  const recordFile = path.join(DRAFTS_DIR, `okki-${record.okki_record_id}.json`);
  fs.writeFileSync(recordFile, JSON.stringify(record, null, 2), 'utf8');
  
  return record;
}

// 主调度逻辑
function runScheduler(options = {}) {
  const { dryRun = false, manual = true } = options;
  
  log('='.repeat(60));
  log('Follow-up Scheduler 启动');
  log(`模式：${dryRun ? 'DRY-RUN' : 'LIVE'} | 触发：${manual ? '手动' : '定时'}`);
  log('='.repeat(60));
  
  try {
    // 1. 加载配置
    const config = loadStrategies();
    log(`加载 ${config.strategies.length} 个跟进策略`);
    
    const globalSettings = config.global_settings;
    
    // 2. 检查工作时间（如果配置了）
    if (globalSettings.working_hours.working_hours_only && !dryRun) {
      if (!isWorkingHours(globalSettings.working_hours)) {
        log('当前不在工作时间内，跳过执行', 'WARN');
        return { skipped: true, reason: 'outside_working_hours' };
      }
    }
    
    // 3. 扫描 OKKI 客户
    const customers = scanOKKICustomers();
    
    // 4. 为每个客户计算跟进计划
    const draftsToGenerate = [];
    
    for (const customer of customers) {
      // 查找对应阶段的策略
      const strategy = config.strategies.find(s => s.stage_id === customer.stage);
      
      if (!strategy) {
        log(`客户 ${customer.name} 阶段 ${customer.stage} 无对应策略，跳过`, 'WARN');
        continue;
      }
      
      // 获取当前跟进索引
      const followUpIndex = getFollowUpIndex(customer, strategy);
      
      // 检查是否已达到最大跟进次数
      if (followUpIndex >= strategy.follow_up_sequence.length) {
        log(`客户 ${customer.name} 已达到最大跟进次数 (${followUpIndex})，跳过`);
        continue;
      }
      
      // 计算下次跟进日期
      const lastContactDate = new Date(customer.last_contact_date);
      const nextFollowUpDate = calculateNextFollowUpDate(
        lastContactDate,
        strategy.follow_up_sequence,
        followUpIndex
      );
      
      if (!nextFollowUpDate) {
        log(`客户 ${customer.name} 无法计算下次跟进日期，跳过`, 'WARN');
        continue;
      }
      
      // 检查是否到期
      const now = new Date();
      const isDue = nextFollowUpDate <= now;
      
      if (!isDue) {
        log(`客户 ${customer.name} 下次跟进日期：${nextFollowUpDate.toISOString().split('T')[0]}，未到期`);
        continue;
      }
      
      // 获取对应模板
      const template = strategy.templates.find(t => {
        const day = strategy.follow_up_sequence[followUpIndex];
        return t.day === day;
      });
      
      if (!template) {
        log(`客户 ${customer.name} 未找到第 ${followUpIndex + 1} 次跟进模板，跳过`, 'WARN');
        continue;
      }
      
      log(`✓ 客户 ${customer.name} 到期需要跟进（阶段：${customer.stage}，第 ${followUpIndex + 1} 次）`);
      draftsToGenerate.push({ customer, template, strategy });
    }
    
    // 5. 生成草稿
    log('-'.repeat(60));
    log(`将生成 ${draftsToGenerate.length} 个跟进草稿`);
    log('-'.repeat(60));
    
    const results = {
      total_customers: customers.length,
      drafts_generated: 0,
      drafts: []
    };
    
    for (const { customer, template, strategy } of draftsToGenerate) {
      const draft = generateEmailDraft(customer, template, strategy);
      
      if (dryRun) {
        log(`[DRY-RUN] 将生成草稿：${draft.draft_id}`);
        log(`  客户：${customer.name} (${customer.email})`);
        log(`  主题：${draft.subject}`);
        log(`  模板：${template.template_id}`);
      } else {
        // 保存草稿文件
        saveDraft(draft);
        
        // 创建 OKKI 跟进记录
        if (globalSettings.okki_sync.enabled) {
          createOKKIFollowUpRecord(draft);
        }
        
        results.drafts_generated++;
        results.drafts.push(draft);
      }
    }
    
    // 6. 输出摘要
    log('='.repeat(60));
    log('执行完成摘要');
    log('='.repeat(60));
    log(`扫描客户总数：${results.total_customers}`);
    log(`生成草稿数量：${results.drafts_generated}`);
    
    if (dryRun) {
      log('');
      log('DRY-RUN 模式：未实际生成草稿');
    }
    
    return {
      success: true,
      ...results,
      dry_run: dryRun
    };
    
  } catch (error) {
    log(`执行失败：${error.message}`, 'ERROR');
    return {
      success: false,
      error: error.message
    };
  }
}

// CLI 入口
function main() {
  const args = process.argv.slice(2);
  
  const options = {
    dryRun: args.includes('--dry-run') || args.includes('-n'),
    manual: !args.includes('--scheduled')
  };
  
  const result = runScheduler(options);
  
  // 输出 JSON 结果（便于 cron 调用）
  console.log('\n--- JSON RESULT ---');
  console.log(JSON.stringify(result, null, 2));
  
  // 退出码
  process.exit(result.success ? 0 : 1);
}

// 导出供其他模块使用
module.exports = {
  runScheduler,
  loadStrategies,
  scanOKKICustomers,
  generateEmailDraft,
  saveDraft,
  createOKKIFollowUpRecord
};

// 直接运行时执行
if (require.main === module) {
  main();
}
