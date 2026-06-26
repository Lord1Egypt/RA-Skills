/**
 * 创建新日历
 * 用法: node scripts/create-calendar.js --name "日历名称" [--description "描述"] [--color "#4f46e5"]
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
    name: null,
    description: null,
    color: null
  };
  
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--name' && args[i + 1]) {
      result.name = args[i + 1];
      i++;
    } else if (args[i] === '--description' && args[i + 1]) {
      result.description = args[i + 1];
      i++;
    } else if (args[i] === '--color' && args[i + 1]) {
      result.color = args[i + 1];
      i++;
    }
  }
  
  return result;
}

async function createCalendar() {
  const { name, description, color } = parseArgs();
  
  if (!name) {
    console.error('用法: node scripts/create-calendar.js --name "日历名称" [--description "描述"] [--color "#颜色"]');
    console.error('示例: node scripts/create-calendar.js --name "股票提醒" --color "#4f46e5"');
    process.exit(1);
  }
  
  try {
    const body = { name };
    if (description) body.description = description;
    if (color) body.color = color;
    
    const response = await fetch(`${API_URL}/api/calendars`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${API_KEY}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(body)
    });

    const data = await response.json();

    if (!response.ok) {
      console.error(`创建失败: ${data.message || response.statusText}`);
      process.exit(1);
    }

    const cal = data.calendar;
    
    console.log('✅ 日历创建成功！\n');
    console.log(`名称: ${cal.name}`);
    if (cal.description) console.log(`描述: ${cal.description}`);
    console.log(`颜色: ${cal.color || '#000000'}`);
    console.log(`ID: ${cal.id}`);
    console.log('\n📅 订阅链接（添加到手机日历）：');
    console.log(cal.subscriptionUrl);
    console.log('\n复制上述链接，按照以下步骤添加到日历：');
    console.log('- iOS: 设置 → 日历 → 账户 → 添加订阅日历');
    console.log('- Android: 日历应用 → 更多 → 设置 → 添加日历 → 订阅日历');
    console.log('- macOS: 日历 → 文件 → 新建日历订阅');
  } catch (err) {
    console.error('请求失败:', err.message);
    process.exit(1);
  }
}

createCalendar();
