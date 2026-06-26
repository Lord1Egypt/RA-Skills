#!/usr/bin/env node
/**
 * 🪂 AirdropAlert - 提醒管理
 * 设置和管理快照时间提醒
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const DATA_DIR = path.join(__dirname, '..', 'data');
const REMINDERS_FILE = path.join(DATA_DIR, 'reminders.json');

// 确保数据目录存在
if (!fs.existsSync(DATA_DIR)) {
    fs.mkdirSync(DATA_DIR, { recursive: true });
}

// 加载提醒
function loadReminders() {
    try {
        if (fs.existsSync(REMINDERS_FILE)) {
            return JSON.parse(fs.readFileSync(REMINDERS_FILE, 'utf8'));
        }
    } catch (e) {
        console.error('⚠️  加载提醒失败:', e.message);
    }
    return { reminders: [] };
}

// 保存提醒
function saveReminders(data) {
    fs.writeFileSync(REMINDERS_FILE, JSON.stringify(data, null, 2));
}

// 添加提醒
function addReminder(project, date) {
    const data = loadReminders();
    
    const reminder = {
        id: Date.now(),
        project,
        snapshotDate: date,
        reminderDate: new Date(new Date(date).getTime() - 4 * 60 * 60 * 1000).toISOString().split('T')[0], // 提前 4 小时
        createdAt: new Date().toISOString(),
        notified: false
    };
    
    data.reminders.push(reminder);
    saveReminders(data);
    
    console.log(`\n✅ 提醒已设置\n`);
    console.log(`项目：${project}`);
    console.log(`快照时间：${date}`);
    console.log(`提醒时间：${reminder.reminderDate} (提前 4 小时)`);
    console.log(`\n💡 查看提醒：node scripts/reminder.mjs --list`);
    console.log(`\n🪂 AirdropAlert v0.1.0 - Never Miss an Airdrop`);
}

// 查看所有提醒
function listReminders() {
    const data = loadReminders();
    
    if (data.reminders.length === 0) {
        console.log('ℹ️  暂无提醒');
        console.log('\n💡 添加提醒：node scripts/reminder.mjs add --project zksync --date 2026-03-20');
        return;
    }
    
    console.log('\n🪂 AirdropAlert - 快照提醒\n');
    console.log(`ID     项目              快照时间    提醒时间     状态`);
    console.log(`─────────────────────────────────────────────────────────`);
    
    data.reminders.forEach(r => {
        const id = r.id.toString().padEnd(6);
        const project = r.project.padEnd(16);
        const snapshot = r.snapshotDate.padEnd(10);
        const reminder = r.reminderDate.padEnd(10);
        const status = r.notified ? '✅ 已通知' : '⏳ 待通知';
        
        console.log(`${id} ${project} ${snapshot} ${reminder} ${status}`);
    });
    
    console.log(`\n💡 删除提醒：node scripts/reminder.mjs remove <ID>`);
}

// 删除提醒
function removeReminder(id) {
    const data = loadReminders();
    const initialLength = data.reminders.length;
    
    data.reminders = data.reminders.filter(r => r.id.toString() !== id);
    
    if (data.reminders.length === initialLength) {
        console.log(`❌ 未找到提醒 ID: ${id}`);
        return;
    }
    
    saveReminders(data);
    console.log(`✅ 提醒已删除`);
    console.log(`\n🪂 AirdropAlert v0.1.0 - Never Miss an Airdrop`);
}

// 主函数
const args = process.argv.slice(2);

if (args.includes('--help') || args.includes('-h')) {
    console.log(`
🪂 AirdropAlert - 提醒管理

用法:
  node scripts/reminder.mjs add --project <name> --date <YYYY-MM-DD>  # 添加提醒
  node scripts/reminder.mjs --list         # 查看所有提醒
  node scripts/reminder.mjs remove <ID>    # 删除提醒

示例:
  node scripts/reminder.mjs add --project zksync --date 2026-03-20
  node scripts/reminder.mjs --list
  node scripts/reminder.mjs remove 1234567890

选项:
  --help, -h        显示帮助
  --list            查看提醒列表
  --project <name>  项目名称
  --date <date>     快照日期 (YYYY-MM-DD)
`);
    process.exit(0);
}

const action = args[0];

if (action === 'add') {
    const projectIndex = args.indexOf('--project');
    const dateIndex = args.indexOf('--date');
    
    const project = projectIndex > -1 ? args[projectIndex + 1] : null;
    const date = dateIndex > -1 ? args[dateIndex + 1] : null;
    
    if (!project || !date) {
        console.log('❌ 请提供项目名称和日期');
        console.log('用法：node scripts/reminder.mjs add --project zksync --date 2026-03-20');
        process.exit(1);
    }
    
    addReminder(project, date);
} else if (action === '--list' || args.includes('--list')) {
    listReminders();
} else if (action === 'remove') {
    const id = args[1];
    if (!id) {
        console.log('❌ 请提供提醒 ID');
        process.exit(1);
    }
    removeReminder(id);
} else {
    console.log('❌ 未知操作');
    console.log('用法：node scripts/reminder.mjs --help');
    process.exit(1);
}
