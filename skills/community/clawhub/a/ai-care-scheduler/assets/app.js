/**
 * 智能照护排班系统 - 极简版
 * 简单又好用的护理排班工具
 */

// ==================== 数据处理 ====================

const ScheduleApp = {
  // 班次配置
  shifts: [
    { id: 'morning', name: '早班', time: '07:00-15:00', required: 2 },
    { id: 'afternoon', name: '中班', time: '15:00-23:00', required: 2 },
    { id: 'night', name: '夜班', time: '23:00-07:00', required: 1 },
  ],

  // 排班算法
  generateSchedule(staffList, shiftsPerWeek, startDate, cycle) {
    const days = cycle === 'week' ? 7 : 30;
    const schedule = [];
    const staffShifts = {}; // 员工已排班次计数
    
    // 初始化
    staffList.forEach(s => staffShifts[s.id] = 0);
    
    // 每天每个班次分配员工
    for (let d = 0; d < days; d++) {
      const date = this.addDays(startDate, d);
      const dayOfWeek = new Date(date).getDay();
      
      // 每周限制
      const weekNum = Math.floor(d / 7);
      const weekStart = weekNum * 7;
      const weekShifts = {}; // 本周每人的班次
      
      for (const shift of this.shifts) {
        const assigned = [];
        
        // 筛选可用员工
        let available = staffList.filter(s => {
          // 检查周上限
          const weekShiftCount = Object.entries(staffShifts)
            .filter(([sid]) => sid.startsWith(s.id.split('-')[0]))
            .reduce((sum, [, count]) => sum + count, 0);
          
          if (weekShiftCount >= shiftsPerWeek) return false;
          if (s.available && !s.available.includes(dayOfWeek)) return false;
          
          // 检查是否连续排班
          const lastDate = s.lastDate;
          if (lastDate && this.isConsecutive(lastDate, date)) return false;
          
          // 检查夜班后休息
          if (shift.id === 'morning' && s.lastShift === 'night') return false;
          
          return true;
        });
        
        // 按顺序分配
        available.sort((a, b) => (staffShifts[a.id] || 0) - (staffShifts[b.id] || 0));
        
        for (const s of available) {
          if (assigned.length >= shift.required) break;
          assigned.push(s);
        }
        
        // 记录
        for (const s of assigned) {
          staffShifts[s.id] = (staffShifts[s.id] || 0) + 1;
          s.lastDate = date;
          s.lastShift = shift.id;
        }
        
        if (assigned.length > 0) {
          schedule.push({
            date,
            shift: shift.name,
            shiftId: shift.id,
            time: shift.time,
            staff: assigned.map(s => s.name).join('、')
          });
        }
      }
    }
    
    return schedule;
  },

  addDays(date, days) {
    const d = new Date(date);
    d.setDate(d.getDate() + days);
    return d.toISOString().split('T')[0];
  },

  isConsecutive(d1, d2) {
    const diff = new Date(d2).getTime() - new Date(d1).getTime();
    return diff <= 86400000 * 2; // 48小时内
  },

  formatDate(dateStr) {
    const d = new Date(dateStr);
    const weeks = ['周日', '周一', '周二', '周三', '周四', '周五', '周六'];
    return `${d.getMonth() + 1}月${d.getDate()}日 ${weeks[d.getDay()]}`;
  },

  // 导出CSV
  exportCSV(schedule, filename) {
    const rows = [['日期', '班次', '时间', '值班人员']];
    schedule.forEach(s => rows.push([s.date, s.shift, s.time, s.staff]));
    
    const csv = rows.map(r => r.join(',')).join('\n');
    const blob = new Blob(['\ufeff' + csv], { type: 'text/csv;charset=utf-8' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = filename;
    link.click();
  }
};

// ==================== 界面渲染 ====================

const App = {
  step: 1,           // 当前步骤
  staffInput: '',     // 员工输入
  shiftsPerWeek: 5,   // 每周班次
  cycle: 'week',      // 排班周期
  startDate: '',      // 开始日期
  schedule: [],       // 排班结果
  apiKey: '',         // API Key

  // 预设示例员工
  demoStaff: `张护士
李护理员
王护工
赵阿姨
钱大姐
孙护士
周护理员`,

  init() {
    const today = new Date();
    const monday = new Date(today);
    monday.setDate(today.getDate() - today.getDay() + 1);
    this.startDate = monday.toISOString().split('T')[0];
    // 自动填入示例员工
    this.staffInput = this.demoStaff;
    this.render();
    // 3秒后自动跳到最后一步生成
    setTimeout(() => this.autoGenerate(), 1500);
  },

  async autoGenerate() {
    try {
      await this.generate();
    } catch(e) {
      console.log('自动生成:', e.message);
    }
  },

  render() {
    const html = `
      <div class="container">
        <div class="header">
          <h1>🏥 智能照护排班</h1>
          <p class="subtitle">简单又好用的排班工具</p>
        </div>
        
        <div class="progress">
          <div class="step ${this.step >= 1 ? 'active' : ''}">1. 员工</div>
          <div class="step ${this.step >= 2 ? 'active' : ''}">2. 规则</div>
          <div class="step ${this.step >= 3 ? 'active' : ''}">3. 周期</div>
          <div class="step ${this.step >= 4 ? 'active' : ''}">4. 生成</div>
        </div>

        <div class="card">
          ${this.renderStep()}
        </div>

        <div class="nav-buttons">
          ${this.step > 1 ? `<button class="btn btn-secondary" onclick="App.prevStep()">上一步</button>` : ''}
          ${this.step < 4 ? `<button class="btn btn-primary" onclick="App.nextStep()">下一步</button>` : ''}
        </div>
      </div>
    `;
    
    document.getElementById('app').innerHTML = html;
  },

  renderStep() {
    switch(this.step) {
      case 1: return this.renderStaffStep();
      case 2: return this.renderRuleStep();
      case 3: return this.renderCycleStep();
      case 4: return this.renderGenerateStep();
      default: return '';
    }
  },

  // 步骤1: 输入员工
  renderStaffStep() {
    return `
      <div class="step-content">
        <h2>👥 添加工作人员</h2>
        <p class="hint">请输入工作人员姓名或编号，每行一个</p>
        <textarea 
          id="staffInput" 
          rows="8" 
          placeholder="例如：
张护士
李护理员
王护工
赵阿姨
钱大姐">${this.staffInput}</textarea>
        <div class="example">
          <span>💡 提示：可以用编号+姓名，如 "001 张护士"</span>
        </div>
      </div>
    `;
  },

  // 步骤2: 设置规则
  renderRuleStep() {
    return `
      <div class="step-content">
        <h2>⚙️ 排班规则</h2>
        
        <div class="form-group">
          <label>每人每周上班 <strong>${this.shiftsPerWeek}</strong> 班</label>
          <input type="range" min="2" max="7" value="${this.shiftsPerWeek}" 
            oninput="App.shiftsPerWeek = this.value; this.previousElementSibling.innerHTML = '每人每周上班 <strong>' + this.value + '</strong> 班'; App.render()">
        </div>

        <div class="rules-preview">
          <div class="rule-item enabled">
            <span class="check">✓</span>
            <span>不连续排班（休息一天）</span>
          </div>
          <div class="rule-item enabled">
            <span class="check">✓</span>
            <span>夜班后休息一天</span>
          </div>
          <div class="rule-item enabled">
            <span class="check">✓</span>
            <span>每周班次不超过设定值</span>
          </div>
        </div>
      </div>
    `;
  },

  // 步骤3: 设置周期
  renderCycleStep() {
    const dateStr = new Date(this.startDate).toLocaleDateString('zh-CN', { 
      year: 'numeric', month: 'long', day: 'numeric' 
    });
    
    return `
      <div class="step-content">
        <h2>📅 排班周期</h2>
        
        <div class="form-group">
          <label>开始日期</label>
          <input type="date" value="${this.startDate}" 
            onchange="App.startDate = this.value; App.render()">
          <span class="date-preview">${dateStr}</span>
        </div>

        <div class="form-group">
          <label>排班周期</label>
          <div class="radio-group">
            <label class="radio ${this.cycle === 'week' ? 'checked' : ''}">
              <input type="radio" name="cycle" value="week" ${this.cycle === 'week' ? 'checked' : ''}
                onchange="App.cycle = 'week'; App.render()">
              <span>📅 一周</span>
            </label>
            <label class="radio ${this.cycle === 'month' ? 'checked' : ''}">
              <input type="radio" name="cycle" value="month" ${this.cycle === 'month' ? 'checked' : ''}
                onchange="App.cycle = 'month'; App.render()">
              <span>📆 一个月</span>
            </label>
          </div>
        </div>

        <div class="summary">
          <h3>📋 排班概要</h3>
          <p>周期：${this.cycle === 'week' ? '一周（7天）' : '一个月（30天）'}</p>
          <p>开始：${dateStr}</p>
        </div>
      </div>
    `;
  },

  // 步骤4: 生成排班
  renderGenerateStep() {
    const staffCount = this.staffInput.split('\n').filter(s => s.trim()).length;
    const days = this.cycle === 'week' ? 7 : 30;
    const shiftCount = this.shifts.length;
    const totalShifts = days * shiftCount;
    
    return `
      <div class="step-content">
        <h2>🤖 生成排班</h2>
        
        <div class="form-group">
          <label>通义千问 API Key（可选）</label>
          <input type="password" id="apiKey" placeholder="不填则使用本地算法" value="${this.apiKey}">
          <small>申请地址：dashscope.console.aliyun.com</small>
        </div>

        <div class="info-box">
          <h3>📊 排班信息</h3>
          <p>👥 工作人员：<strong>${staffCount} 人</strong></p>
          <p>📅 排班天数：<strong>${days} 天</strong></p>
          <p>⏰ 班次数量：<strong>${shiftCount} 个/天</strong></p>
          <p>📈 总班次：<strong>${totalShifts} 班</strong></p>
        </div>

        ${this.schedule.length > 0 ? this.renderSchedule() : `
          <button class="btn btn-generate" onclick="App.generate()">
            ✨ 智能生成排班表
          </button>
        `}
      </div>
    `;
  },

  renderSchedule() {
    const days = this.cycle === 'week' ? 7 : 30;
    const dates = [];
    for (let i = 0; i < days; i++) {
      const d = new Date(this.startDate);
      d.setDate(d.getDate() + i);
      dates.push(d.toISOString().split('T')[0]);
    }

    let html = `
      <div class="schedule-result">
        <div class="result-header">
          <h3>✅ 排班结果</h3>
          <button class="btn btn-small" onclick="App.export()">📥 导出CSV</button>
        </div>
        
        <table class="schedule-table">
          <thead>
            <tr>
              <th>日期</th>
              <th>班次</th>
              <th>时间</th>
              <th>值班人员</th>
            </tr>
          </thead>
          <tbody>
    `;

    dates.forEach(date => {
      const dayShifts = this.schedule.filter(s => s.date === date);
      if (dayShifts.length > 0) {
        dayShifts.forEach((s, i) => {
          html += `
            <tr>
              ${i === 0 ? `<td rowspan="${dayShifts.length}" class="date-col">${ScheduleApp.formatDate(date)}</td>` : ''}
              <td><span class="shift-tag">${s.shift}</span></td>
              <td>${s.time}</td>
              <td>${s.staff}</td>
            </tr>
          `;
        });
      }
    });

    html += `</tbody></table></div>`;
    return html;
  },

  // 下一步
  nextStep() {
    if (this.step === 1) {
      this.staffInput = document.getElementById('staffInput')?.value || '';
      if (!this.staffInput.trim()) {
        alert('请输入工作人员姓名');
        return;
      }
    }
    if (this.step === 3) {
      this.apiKey = document.getElementById('apiKey')?.value || '';
    }
    this.step++;
    this.render();
  },

  // 上一步
  prevStep() {
    this.step--;
    this.render();
  },

  // 生成排班
  async generate() {
    const btn = document.querySelector('.btn-generate');
    btn.textContent = '⏳ 生成中...';
    btn.disabled = true;

    try {
      // 解析员工
      const staffLines = this.staffInput.split('\n').filter(s => s.trim());
      const staff = staffLines.map((line, i) => {
        const parts = line.split(/\s+/);
        const id = parts[0] || (i + 1).toString();
        const name = parts[1] || line;
        return {
          id: id.toString(),
          name: name,
          available: [0,1,2,3,4,5,6] // 每天可用
        };
      });

      const days = this.cycle === 'week' ? 7 : 30;
      
      // 使用AI或本地算法
      if (this.apiKey) {
        this.schedule = await this.generateWithAI(staff, days);
      } else {
        await new Promise(r => setTimeout(r, 500));
        this.schedule = ScheduleApp.generateSchedule(
          staff, 
          this.shiftsPerWeek, 
          this.startDate, 
          this.cycle
        );
      }

      this.render();
    } catch (e) {
      alert('生成失败: ' + e.message);
      btn.textContent = '✨ 智能生成排班表';
      btn.disabled = false;
    }
  },

  // AI生成（简化版）
  async generateWithAI(staff, days) {
    const shifts = ScheduleApp.shifts;
    
    const prompt = `
请为养老机构生成${days}天的排班表。

员工：${staff.map(s => s.name).join('、')}
每人每周${this.shiftsPerWeek}班。
开始日期：${this.startDate}

班次：
- 早班 07:00-15:00 需要2人
- 中班 15:00-23:00 需要2人  
- 夜班 23:00-07:00 需要1人

规则：
1. 不连续排班
2. 夜班后休息一天
3. 每周不超${this.shiftsPerWeek}班

请生成JSON格式：
[{"date": "2024-01-01", "shift": "早班", "time": "07:00-15:00", "staff": "张三、李四"}]
`;

    const resp = await fetch('https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${this.apiKey}`
      },
      body: JSON.stringify({
        model: 'qwen-plus',
        messages: [
          { role: 'system', content: '你是排班专家，请严格按照JSON数组格式返回结果。' },
          { role: 'user', content: prompt }
        ]
      })
    });

    const json = await resp.json();
    const content = json.choices?.[0]?.message?.content || '';
    const match = content.match(/\[[\s\S]*\]/);
    if (!match) throw new Error('无法解析结果');
    return JSON.parse(match[0]);
  },

  // 导出
  export() {
    const filename = `排班表_${this.startDate}_${this.cycle === 'week' ? '一周' : '一月'}.csv`;
    ScheduleApp.exportCSV(this.schedule, filename);
  }
};

// 启动
document.addEventListener('DOMContentLoaded', () => App.init());
