/**
 * 创建日历事件
 * 用法: node scripts/create-event.js --calendar-id <id> --title <标题> --start-date <日期>
 *       [--end-date <日期>] [--start-time <时间>] [--end-time <时间>]
 *       [--description <描述>] [--location <地点>]
 *       [--alarm] [--alarm-minutes <分钟>]
 */

const API_KEY = process.env.CLAW_CALENDAR_API_KEY;
const API_URL = process.env.CLAW_CALENDAR_API_URL || 'https://claw-calendar.com';

if (!API_KEY) {
  console.error('请设置环境变量 CLAW_CALENDAR_API_KEY');
  process.exit(1);
}

function parseArgs() {
  const args = process.argv.slice(2);
  const result = {
    calendarId: null,
    title: null,
    startDate: null,
    endDate: null,
    startTime: null,
    endTime: null,
    description: null,
    location: null,
    alarm: false,
    alarmMinutes: 15
  };
  
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--calendar-id' && args[i + 1]) {
      result.calendarId = args[i + 1];
      i++;
    } else if (args[i] === '--title' && args[i + 1]) {
      result.title = args[i + 1];
      i++;
    } else if (args[i] === '--start-date' && args[i + 1]) {
      result.startDate = args[i + 1];
      i++;
    } else if (args[i] === '--end-date' && args[i + 1]) {
      result.endDate = args[i + 1];
      i++;
    } else if (args[i] === '--start-time' && args[i + 1]) {
      result.startTime = args[i + 1];
      i++;
    } else if (args[i] === '--end-time' && args[i + 1]) {
      result.endTime = args[i + 1];
      i++;
    } else if (args[i] === '--description' && args[i + 1]) {
      result.description = args[i + 1];
      i++;
    } else if (args[i] === '--location' && args[i + 1]) {
      result.location = args[i + 1];
      i++;
    } else if (args[i] === '--alarm') {
      result.alarm = true;
    } else if (args[i] === '--alarm-minutes' && args[i + 1]) {
      result.alarmMinutes = parseInt(args[i + 1], 10) || 15;
      i++;
    }
  }
  
  return result;
}

function formatDate(dateStr) {
  if (!dateStr) return '';
  const d = new Date(dateStr);
  return d.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit'
  });
}

async function createEvent() {
  const args = parseArgs();
  
  if (!args.calendarId || !args.title || !args.startDate) {
    console.error('用法: node scripts/create-event.js --calendar-id <id> --title <标题> --start-date <日期>');
    console.error('       [--end-date <日期>] [--start-time <时间>] [--end-time <时间>]');
    console.error('       [--description <描述>] [--location <地点>] [--alarm] [--alarm-minutes <分钟>]');
    console.error('');
    console.error('示例 (全天事件):');
    console.error('  node scripts/create-event.js --calendar-id abc123 --title "股票分红" --start-date 2026-04-15');
    console.error('');
    console.error('示例 (定时事件):');
    console.error('  node scripts/create-event.js --calendar-id abc123 --title "会议" --start-date 2026-04-15 --start-time "14:00:00" --end-time "15:00:00" --alarm');
    process.exit(1);
  }
  
  // 验证日期格式
  if (!/^\d{4}-\d{2}-\d{2}$/.test(args.startDate)) {
    console.error('日期格式错误，请使用 YYYY-MM-DD 格式（如 2026-04-15）');
    process.exit(1);
  }
  
  if (args.endDate && !/^\d{4}-\d{2}-\d{2}$/.test(args.endDate)) {
    console.error('结束日期格式错误，请使用 YYYY-MM-DD 格式');
    process.exit(1);
  }
  
  try {
    const body = {
      title: args.title,
      startDate: args.startDate
    };
    
    if (args.endDate) body.endDate = args.endDate;
    if (args.startTime) body.startTime = args.startTime;
    if (args.endTime) body.endTime = args.endTime;
    if (args.description) body.description = args.description;
    if (args.location) body.location = args.location;
    if (args.alarm) {
      body.alarm = true;
      body.alarmMinutes = args.alarmMinutes;
    }
    
    const response = await fetch(`${API_URL}/api/calendars/${args.calendarId}/events`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${API_KEY}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(body)
    });

    const data = await response.json();

    if (!response.ok) {
      if (response.status === 404) {
        console.error(`日历不存在: ${args.calendarId}`);
        console.error('请运行: node scripts/list-calendars.js 查看可用日历');
      } else if (response.status === 403) {
        console.error('无权限在此日历中创建事件');
      } else {
        console.error(`创建失败: ${data.message || response.statusText}`);
      }
      process.exit(1);
    }

    const evt = data.event;
    
    console.log('✅ 事件创建成功！\n');
    console.log(`标题: ${evt.title}`);
    if (evt.description) console.log(`描述: ${evt.description}`);
    if (evt.location) console.log(`地点: ${evt.location}`);
    console.log(`时间: ${formatDate(evt.startDate)} ${evt.startTime || ''} ${evt.endTime ? '- ' + evt.endTime : ''}`);
    if (evt.alarm) {
      console.log(`提醒: 提前 ${evt.alarmMinutes} 分钟`);
    } else {
      console.log('提醒: 未设置');
    }
    console.log(`ID: ${evt.id}`);
    
    if (evt.alarm) {
      console.log('\n📲 提醒已设置，届时会收到通知');
    }
  } catch (err) {
    console.error('请求失败:', err.message);
    process.exit(1);
  }
}

createEvent();
