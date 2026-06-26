/**
 * 列出用户所有日历
 * 用法: node scripts/list-calendars.js
 */

const API_KEY = process.env.CLAW_CALENDAR_API_KEY;
const API_URL = process.env.CLAW_CALENDAR_API_URL || 'https://claw-calendar.com';

if (!API_KEY) {
  console.error('请设置环境变量 CLAW_CALENDAR_API_KEY');
  console.error('在 Claw Calendar 设置中生成 API Key');
  process.exit(1);
}

async function listCalendars() {
  try {
    const response = await fetch(`${API_URL}/api/calendars`, {
      headers: {
        'Authorization': `Bearer ${API_KEY}`,
        'Content-Type': 'application/json'
      }
    });

    if (!response.ok) {
      if (response.status === 401) {
        console.error('认证失败：API Key 无效或已过期');
      } else if (response.status === 403) {
        console.error('无权限访问，请检查 API Key 权限');
      } else {
        console.error(`请求失败: ${response.status} ${response.statusText}`);
      }
      process.exit(1);
    }

    const data = await response.json();
    
    if (!data.calendars || data.calendars.length === 0) {
      console.log('暂无日历');
      console.log('运行以下命令创建第一个日历：');
      console.log('  node scripts/create-calendar.js --name "我的日历"');
      return;
    }

    console.log(`共 ${data.calendars.length} 个日历：\n`);
    
    data.calendars.forEach((cal, i) => {
      console.log(`--- ${i + 1}. ${cal.name} ---`);
      console.log(`ID: ${cal.id}`);
      console.log(`描述: ${cal.description || '(无)'}`);
      console.log(`颜色: ${cal.color || '#000000'}`);
      console.log(`订阅链接: ${cal.subscriptionUrl}`);
      console.log('');
    });
  } catch (err) {
    console.error('请求失败:', err.message);
    process.exit(1);
  }
}

listCalendars();
