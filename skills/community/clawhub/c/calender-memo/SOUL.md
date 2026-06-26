const fs = require('fs');
const path = require('path');
const reminder = require('./reminder.js');  // 引入提醒模块

// 数据文件路径
const MEMORY_FILE = path.join(__dirname, 'MEMORY.md');

// ---------- 工具函数 ----------
// 加载所有日程
function loadEvents() {
  try {
    const data = fs.readFileSync(MEMORY_FILE, 'utf8');
    return JSON.parse(data);
  } catch (e) {
    return [];
  }
}

// 保存日程
function saveEvents(events) {
  try {
    fs.writeFileSync(MEMORY_FILE, JSON.stringify(events, null, 2), 'utf8');
    return true;
  } catch (e) {
    console.error('保存失败', e);
    return false;
  }
}

// 简单的日期时间解析（支持今天/明天/后天 + 时间）
function parseDateTime(text) {
  const now = new Date();
  let date = new Date(now);
  
  text = text.toLowerCase();
  
  if (text.includes('今天')) {
    date = new Date(now);
  } else if (text.includes('明天')) {
    date = new Date(now);
    date.setDate(date.getDate() + 1);
  } else if (text.includes('后天')) {
    date = new Date(now);
    date.setDate(date.getDate() + 2);
  }
  
  const timeMatch = text.match(/(\d{1,2})[:：](\d{2})/);
  if (timeMatch) {
    date.setHours(parseInt(timeMatch[1]), parseInt(timeMatch[2]), 0);
  } else {
    date.setHours(9, 0, 0); // 默认早上9点
  }
  
  return date;
}

// 获取今天0点和明天0点
function getTodayRange() {
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  const tomorrow = new Date(today);
  tomorrow.setDate(tomorrow.getDate() + 1);
  return { today, tomorrow };
}

// ---------- 技能主逻辑 ----------
module.exports = {
  // 技能启动时开启定时提醒检查
  onStart: async () => {
    reminder.startReminderChecker();
    console.log('📅 日历技能已启动，主动提醒已开启');
  },

  // 技能停止时清理定时器
  onStop: async () => {
    reminder.stopReminderChecker();
    console.log('📅 日历技能已停止');
  },

  // 处理用户消息
  onMessage: async (event) => {
    const text = event.message.text.trim();
    let reply = '';

    // 加载现有日程
    let events = loadEvents();

    // ---------- 命令处理 ----------
    // 1. 添加日程
    if (text.startsWith('添加 ') || text.startsWith('新增 ')) {
      const content = text.substring(3).trim();
      const parts = content.split(' ');
      if (parts.length >= 2) {
        const timeStr = parts[0];
        const title = parts.slice(1).join(' ');
        let startTime = parseDateTime(content);
        
        const newEvent = {
          id: Date.now().toString(),
          title: title,
          startTime: startTime.toISOString(),
          endTime: new Date(startTime.getTime() + 60 * 60 * 1000).toISOString(), // 默认1小时
          status: 'upcoming',
          reminded: false,               // 新增：是否已提醒
          reminderOffset: 15,             // 默认提前15分钟提醒
          createdAt: new Date().toISOString()
        };
        
        events.push(newEvent);
        if (saveEvents(events)) {
          const showTime = startTime.toLocaleString('zh-CN', { 
            month: 'numeric', day: 'numeric', hour: '2-digit', minute: '2-digit' 
          });
          reply = `✅ 已添加日程：${title}\n⏰ 时间：${showTime}`;
        } else {
          reply = '❌ 保存失败，请重试';
        }
      } else {
        reply = '格式不对，试试：添加 明天下午3点 团队周会';
      }
    }
    
    // 2. 查看今天日程
    else if (text.includes('今天') && (text.includes('日程') || text.includes('安排'))) {
      const { today, tomorrow } = getTodayRange();
      const todayEvents = events.filter(e => {
        const eventDate = new Date(e.startTime);
        return eventDate >= today && eventDate < tomorrow && e.status === 'upcoming';
      });
      
      if (todayEvents.length === 0) {
        reply = '📅 今天没有日程安排，放松一下吧~';
      } else {
        reply = '📅 **今天日程**\n\n';
        todayEvents.sort((a, b) => new Date(a.startTime) - new Date(b.startTime));
        todayEvents.forEach((e, i) => {
          const time = new Date(e.startTime).toLocaleTimeString('zh-CN', { 
            hour: '2-digit', minute: '2-digit' 
          });
          reply += `${i + 1}. ${time} ${e.title}\n`;
        });
      }
    }
    
    // 3. 查看所有未完成日程
    else if (text === '日程' || text === '我的日程' || text === '列表') {
      const upcoming = events.filter(e => e.status === 'upcoming')
        .sort((a, b) => new Date(a.startTime) - new Date(b.startTime));
      
      if (upcoming.length === 0) {
        reply = '📅 暂无日程安排';
      } else {
        reply = '📅 **待办日程**\n\n';
        upcoming.forEach((e, i) => {
          const date = new Date(e.startTime).toLocaleDateString('zh-CN', { 
            month: 'numeric', day: 'numeric' 
          });
          const time = new Date(e.startTime).toLocaleTimeString('zh-CN', { 
            hour: '2-digit', minute: '2-digit' 
          });
          reply += `${i + 1}. ${date} ${time} ${e.title}\n`;
        });
      }
    }
    
    // 4. 删除日程
    else if (text.startsWith('删除 ')) {
      const index = parseInt(text.substring(3).trim()) - 1;
      const upcoming = events.filter(e => e.status === 'upcoming')
        .sort((a, b) => new Date(a.startTime) - new Date(b.startTime));
      
      if (!isNaN(index) && index >= 0 && index < upcoming.length) {
        const eventToDelete = upcoming[index];
        events = events.filter(e => e.id !== eventToDelete.id);
        if (saveEvents(events)) {
          reply = `🗑️ 已删除：${eventToDelete.title}`;
        } else {
          reply = '❌ 删除失败';
        }
      } else {
        reply = '序号无效，试试：删除 1';
      }
    }
    
    // 5. 完成日程
    else if (text.startsWith('完成 ')) {
      const index = parseInt(text.substring(3).trim()) - 1;
      const upcoming = events.filter(e => e.status === 'upcoming')
        .sort((a, b) => new Date(a.startTime) - new Date(b.startTime));
      
      if (!isNaN(index) && index >= 0 && index < upcoming.length) {
        const eventToComplete = upcoming[index];
        events = events.map(e => 
          e.id === eventToComplete.id ? { ...e, status: 'completed' } : e
        );
        if (saveEvents(events)) {
          reply = `✅ 已完成：${eventToComplete.title}`;
        } else {
          reply = '❌ 操作失败';
        }
      } else {
        reply = '序号无效，试试：完成 1';
      }
    }
    
    // 6. 帮助信息
    else if (text === '帮助' || text === 'help') {
      reply = `📅 **日历记事本使用指南**

添加日程：添加 明天下午3点 团队周会
查看今天：今天有什么安排
查看所有：我的日程
完成事项：完成 1
删除事项：删除 1

⏰ 提醒功能：日程开始前15分钟会自动推送提醒（需配置飞书等通道）
数据保存在本地，重启不会丢失~`;
    }
    
    // 默认回复
    else {
      reply = '试试对我说："添加 明天下午3点 团队周会" 或 "今天有什么安排"';
    }
    
    await event.sendMessage(reply);
  }
};