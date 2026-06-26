/**
 * 列出日历中的事件
 * 用法: node scripts/list-events.js --calendar-id <id> [--start YYYY-MM-DD] [--end YYYY-MM-DD]
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
    start: null,
    end: null
  };
  
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--calendar-id' && args[i + 1]) {
      result.calendarId = args[i + 1];
      i++;
    } else if (args[i] === '--start' && args[i + 1]) {
      result.start = args[i + 1];
      i++;
    } else if (args[i] === '--end' && args[i + 1]) {
      result.end = args[i + 1];
      i++;
    }
  }
  
  return result;
}

function formatDate(dateStr) {
  if (!dateStr) return '';
  const d = new Date(dateStr);
  return d.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  });
}

async function listEvents() {
  const { calendarId, start, end } = parseArgs();
  
  if (!calendarId) {
    console.error('用法: node scripts/list-events.js --calendar-id <id> [--start YYYY-MM-DD] [--end YYYY-MM-DD]');
    console.error('示例: node scripts/list-events.js --calendar-id abc123 --start 2026-04-01 --end 2026-04-30');
    process.exit(1);
  }
  
  try {
    let url = `${API_URL}/api/calendars/${calendarId}/events`;
    const params = [];
    if (start) params.push(`start=${start}`);
    if (end) params.push(`end=${end}`);
    if (params.length > 0) url += '?' + params.join('&');
    
    const response = await fetch(url, {
      headers: {
        'Authorization': `Bearer ${API_KEY}`,
        'Content-Type': 'application/json'
      }
    });

    const data = await response.json();

    if (!response.ok) {
      if (response.status === 404) {
        console.error(`日历不存在: ${calendarId}`);
        console.error('请运行: node scripts/list-calendars.js 查看可用日历');
      } else {
        console.error(`请求失败: ${data.message || response.statusText}`);
      }
      process.exit(1);
    }

    if (!data.events || data.events.length === 0) {
      console.log('该日历暂无事件');
      if (start || end) {
        console.log(`筛选条件: ${start || '...'} 至 ${end || '...'}`);
      }
      console.log('运行以下命令添加事件：');
      console.log(`  node scripts/create-event.js --calendar-id ${calendarId} --title "事件标题" --start-date 2026-04-15`);
      return;
    }

    const filter = start || end ? ` (${start || '...'} 至 ${end || '...'})` : '';
    console.log(`共 ${data.events.length} 个事件${filter}：\n`);
    
    data.events.forEach((evt, i) => {
      console.log(`--- ${i + 1}. ${evt.title} ---`);
      console.log(`ID: ${evt.id}`);
      console.log(`时间: ${formatDate(evt.startDate)}`);
      if (evt.startTime) console.log(`时间: ${evt.startTime} - ${evt.endTime || evt.startTime}`);
      if (evt.description) console.log(`描述: ${evt.description}`);
      if (evt.location) console.log(`地点: ${evt.location}`);
      if (evt.alarm) console.log(`提醒: 提前 ${evt.alarmMinutes} 分钟`);
      console.log('');
    });
  } catch (err) {
    console.error('请求失败:', err.message);
    process.exit(1);
  }
}

listEvents();
