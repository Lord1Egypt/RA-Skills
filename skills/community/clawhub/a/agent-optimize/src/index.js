#!/usr/bin/env node

/**
 * Agent Optimize - Agent 優化診斷工具
 * 
 * 分析 OpenClaw 運行狀態，識別信息過載、上下文堆積、技能噪音等問題
 * 提供系統級優化方案，實現瘦身提速
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const os = require('os');

// 配置
const CONFIG = {
  maxContextLines: parseInt(process.env.OPTIMIZE_MAX_CONTEXT_LINES || '5000'),
  reportFormat: process.env.OPTIMIZE_REPORT_FORMAT || 'markdown',
  autoFix: process.env.OPTIMIZE_AUTO_FIX === 'true',
  retentionDays: parseInt(process.env.OPTIMIZE_RETENTION_DAYS || '30'),
  memoryArchiveDays: parseInt(process.env.OPTIMIZE_MEMORY_ARCHIVE_DAYS || '90'),
};

// 路徑配置
const PATHS = {
  openclaw: process.env.OPENCLAW_HOME || path.join(os.homedir(), '.openclaw'),
  npmGlobal: '/home/admin/.npm-global/lib/node_modules/openclaw',
  workspace: process.cwd(),
};

// 診斷結果
const report = {
  timestamp: new Date().toISOString(),
  workspace: PATHS.workspace,
  score: 100,
  issues: [],
  recommendations: [],
  metrics: {},
};

/**
 * 執行 shell 命令
 */
function exec(command, options = {}) {
  try {
    return execSync(command, { encoding: 'utf-8', ...options }).trim();
  } catch (error) {
    return options.allowFailure ? null : '';
  }
}

/**
 * 檢查上下文堆積
 */
function diagnoseContext() {
  console.log('🔍 診斷上下文狀態...\n');
  
  const sessionsPath = path.join(PATHS.openclaw, 'sessions');
  const memoryPaths = [
    path.join(PATHS.workspace, 'memory'),
    path.join(PATHS.openclaw, 'workspace-skill-dev', 'memory'),
  ];
  
  // 檢查會話
  let sessionCount = 0;
  let sessionSize = 0;
  let largeSessions = [];
  
  if (fs.existsSync(sessionsPath)) {
    const sessions = fs.readdirSync(sessionsPath).filter(f => f.endsWith('.json'));
    sessionCount = sessions.length;
    
    sessions.forEach(session => {
      const filePath = path.join(sessionsPath, session);
      const stats = fs.statSync(filePath);
      sessionSize += stats.size;
      
      try {
        const content = fs.readFileSync(filePath, 'utf-8');
        const lines = content.split('\n').length;
        if (lines > CONFIG.maxContextLines) {
          largeSessions.push({ name: session, lines });
        }
      } catch (e) {}
    });
  }
  
  // 檢查記憶文件
  let memoryCount = 0;
  let memorySize = 0;
  let memoryFiles = [];
  
  memoryPaths.forEach(memPath => {
    if (fs.existsSync(memPath)) {
      const files = fs.readdirSync(memPath).filter(f => f.endsWith('.md'));
      memoryCount += files.length;
      
      files.forEach(file => {
        const filePath = path.join(memPath, file);
        const stats = fs.statSync(filePath);
        memorySize += stats.size;
        memoryFiles.push({
          name: file,
          size: stats.size,
          path: filePath,
        });
      });
    }
  });
  
  // 排序記憶文件
  memoryFiles.sort((a, b) => b.size - a.size);
  
  report.metrics.context = {
    sessionCount,
    sessionSizeMB: (sessionSize / 1024 / 1024).toFixed(2),
    largeSessions: largeSessions.length,
    memoryCount,
    memorySizeMB: (memorySize / 1024 / 1024).toFixed(2),
    topMemoryFiles: memoryFiles.slice(0, 5),
  };
  
  // 評估問題
  if (largeSessions.length > 0) {
    report.issues.push({
      type: 'context_bloat',
      severity: 'high',
      title: '上下文堆積',
      description: `發現 ${largeSessions.length} 個大型會話文件（超過 ${CONFIG.maxContextLines} 行）`,
      impact: '導致 Agent 響應變慢，Token 使用量激增',
    });
    report.score -= 15;
    
    report.recommendations.push({
      type: 'cleanup',
      priority: 'high',
      title: '清理大型會話',
      description: '刪除或歸檔超過 30 天的會話文件',
      command: `find ${sessionsPath} -name "*.json" -mtime +30 -delete`,
      estimatedImpact: '可釋放 ' + (sessionSize * 0.3 / 1024 / 1024).toFixed(1) + ' MB',
    });
  }
  
  if (memorySize > 50 * 1024 * 1024) {
    report.issues.push({
      type: 'memory_bloat',
      severity: 'medium',
      title: '記憶文件過大',
      description: `記憶文件總大小 ${(memorySize / 1024 / 1024).toFixed(1)} MB`,
      impact: '增加加載時間，佔用存儲空間',
    });
    report.score -= 10;
    
    report.recommendations.push({
      type: 'archive',
      priority: 'medium',
      title: '歸檔舊記憶',
      description: `歸檔超過 ${CONFIG.memoryArchiveDays} 天的記憶文件`,
      estimatedImpact: '可釋放 ' + (memorySize * 0.4 / 1024 / 1024).toFixed(1) + ' MB',
    });
  }
  
  console.log(`  會話數量：${sessionCount}`);
  console.log(`  會話總大小：${(sessionSize / 1024 / 1024).toFixed(2)} MB`);
  console.log(`  大型會話：${largeSessions.length}`);
  console.log(`  記憶文件：${memoryCount}`);
  console.log(`  記憶總大小：${(memorySize / 1024 / 1024).toFixed(2)} MB\n`);
}

/**
 * 檢查技能狀態
 */
function diagnoseSkills() {
  console.log('🔍 診斷技能狀態...\n');
  
  const skillPaths = [
    path.join(PATHS.npmGlobal, 'skills'),
    path.join(PATHS.openclaw, 'workspace-skill-dev', 'skills'),
    path.join(PATHS.openclaw, 'workspace', 'skills'),
    path.join(PATHS.openclaw, 'workspace-trader', 'skills'),
  ];
  
  let totalSkills = 0;
  let skills = [];
  let potentialDuplicates = [];
  
  skillPaths.forEach(skillPath => {
    if (fs.existsSync(skillPath)) {
      const skillDirs = fs.readdirSync(skillPath).filter(f => {
        const fullPath = path.join(skillPath, f);
        return fs.statSync(fullPath).isDirectory() && !f.startsWith('.');
      });
      
      skillDirs.forEach(skill => {
        totalSkills++;
        const skillDir = path.join(skillPath, skill);
        const skillMd = path.join(skillDir, 'SKILL.md');
        
        let skillInfo = {
          name: skill,
          path: skillDir,
          hasSkillMd: fs.existsSync(skillMd),
          size: 0,
        };
        
        if (fs.existsSync(skillMd)) {
          try {
            const content = fs.readFileSync(skillMd, 'utf-8');
            skillInfo.size = content.length;
            
            // 提取描述
            const descMatch = content.match(/description:\s*([^\n]+)/);
            if (descMatch) {
              skillInfo.description = descMatch[1].trim();
            }
          } catch (e) {}
        }
        
        skills.push(skillInfo);
      });
    }
  });
  
  // 檢查重複技能
  const skillNames = skills.map(s => s.name);
  const duplicates = skillNames.filter((name, index) => skillNames.indexOf(name) !== index);
  
  report.metrics.skills = {
    total: totalSkills,
    withSkillMd: skills.filter(s => s.hasSkillMd).length,
    withoutSkillMd: skills.filter(s => !s.hasSkillMd).length,
    duplicates: [...new Set(duplicates)],
    skills: skills.slice(0, 20), // 只保留前 20 個
  };
  
  if (duplicates.length > 0) {
    report.issues.push({
      type: 'skill_duplicates',
      severity: 'medium',
      title: '技能重複',
      description: `發現 ${duplicates.length} 個重複技能：${[...new Set(duplicates)].join(', ')}`,
      impact: '可能導致技能衝突或混淆',
    });
    report.score -= 10;
    
    report.recommendations.push({
      type: 'cleanup',
      priority: 'medium',
      title: '清理重複技能',
      description: '保留一個版本，刪除其他重複技能',
    });
  }
  
  if (skills.filter(s => !s.hasSkillMd).length > 5) {
    report.issues.push({
      type: 'missing_documentation',
      severity: 'low',
      title: '缺少技能文檔',
      description: `${skills.filter(s => !s.hasSkillMd).length} 個技能缺少 SKILL.md`,
      impact: '難以理解和使用這些技能',
    });
    report.score -= 5;
  }
  
  console.log(`  技能總數：${totalSkills}`);
  console.log(`  有文檔：${skills.filter(s => s.hasSkillMd).length}`);
  console.log(`  無文檔：${skills.filter(s => !s.hasSkillMd).length}`);
  console.log(`  重複技能：${[...new Set(duplicates)].length}\n`);
}

/**
 * 檢查配置狀態
 */
function diagnoseConfig() {
  console.log('🔍 診斷配置狀態...\n');
  
  const configPaths = [
    path.join(PATHS.openclaw, 'openclaw.json'),
    path.join(PATHS.openclaw, 'config.json'),
    path.join(PATHS.workspace, 'openclaw.json'),
    path.join(PATHS.workspace, '.env'),
  ];
  
  let configs = [];
  let duplicateKeys = new Set();
  const allKeys = new Map();
  
  configPaths.forEach(configPath => {
    if (fs.existsSync(configPath)) {
      try {
        const content = fs.readFileSync(configPath, 'utf-8');
        let config = {};
        
        if (configPath.endsWith('.json')) {
          config = JSON.parse(content);
        } else if (configPath.endsWith('.env')) {
          content.split('\n').forEach(line => {
            const [key, value] = line.split('=');
            if (key && value) {
              config[key.trim()] = value.trim();
            }
          });
        }
        
        configs.push({
          path: configPath,
          keys: Object.keys(config),
        });
        
        // 檢查重複配置項
        Object.keys(config).forEach(key => {
          if (allKeys.has(key)) {
            duplicateKeys.add(key);
          }
          allKeys.set(key, configPath);
        });
      } catch (e) {}
    }
  });
  
  report.metrics.config = {
    files: configs.length,
    duplicateKeys: [...duplicateKeys],
  };
  
  if (duplicateKeys.size > 0) {
    report.issues.push({
      type: 'config_duplicates',
      severity: 'medium',
      title: '配置項重複',
      description: `發現 ${duplicateKeys.size} 個重複配置項：${[...duplicateKeys].slice(0, 5).join(', ')}...`,
      impact: '可能導致配置衝突或不可預測的行為',
    });
    report.score -= 10;
    
    report.recommendations.push({
      type: 'merge',
      priority: 'medium',
      title: '合併配置文件',
      description: '統一配置源，刪除重複配置項',
    });
  }
  
  console.log(`  配置文件：${configs.length}`);
  console.log(`  重複配置項：${duplicateKeys.size}\n`);
}

/**
 * 檢查系統資源
 */
function diagnoseSystem() {
  console.log('🔍 診斷系統資源...\n');
  
  const cpus = os.cpus();
  const memory = os.totalmem();
  const freeMemory = os.freemem();
  const uptime = os.uptime();
  
  // 檢查磁盤使用
  let diskUsage = {};
  try {
    const dfOutput = exec('df -h ~/.openclaw | tail -1', { allowFailure: true });
    if (dfOutput) {
      const parts = dfOutput.split(/\s+/);
      diskUsage = {
        total: parts[1],
        used: parts[2],
        available: parts[3],
        percent: parts[4],
      };
    }
  } catch (e) {}
  
  report.metrics.system = {
    cpus: cpus.length,
    memoryGB: (memory / 1024 / 1024 / 1024).toFixed(2),
    freeMemoryGB: (freeMemory / 1024 / 1024 / 1024).toFixed(2),
    uptimeHours: (uptime / 3600).toFixed(1),
    disk: diskUsage,
  };
  
  console.log(`  CPU 核心：${cpus.length}`);
  console.log(`  內存：${(memory / 1024 / 1024 / 1024).toFixed(2)} GB`);
  console.log(`  可用內存：${(freeMemory / 1024 / 1024 / 1024).toFixed(2)} GB`);
  console.log(`  運行時間：${(uptime / 3600).toFixed(1)} 小時`);
  if (diskUsage.percent) {
    console.log(`  磁盤使用：${diskUsage.percent}`);
  }
  console.log();
}

/**
 * 生成報告
 */
function generateReport() {
  console.log('📊 生成診斷報告...\n');
  
  // 計算最終評分
  report.score = Math.max(0, report.score);
  
  let rating = '優秀';
  if (report.score < 90) rating = '良好';
  if (report.score < 70) rating = '需要優化';
  if (report.score < 50) rating = '嚴重問題';
  
  if (CONFIG.reportFormat === 'json') {
    console.log(JSON.stringify(report, null, 2));
  } else {
    // Markdown 格式
    console.log('='.repeat(60));
    console.log('# 🩺 Agent 優化診斷報告\n');
    console.log(`**生成時間:** ${new Date(report.timestamp).toLocaleString('zh-CN')}`);
    console.log(`**工作區:** ${report.workspace}\n`);
    
    console.log('## 📊 總體狀態\n');
    console.log(`**評分:** ${report.score}/100 (${rating})\n`);
    
    if (report.issues.length > 0) {
      console.log('## ⚠️ 發現問題\n');
      report.issues.forEach((issue, i) => {
        const severityIcon = issue.severity === 'high' ? '🔴' : issue.severity === 'medium' ? '🟡' : '🟢';
        console.log(`${i + 1}. ${severityIcon} **${issue.title}** (${issue.severity})`);
        console.log(`   ${issue.description}`);
        console.log(`   影響：${issue.impact}\n`);
      });
    }
    
    if (report.recommendations.length > 0) {
      console.log('## ✅ 優化建議\n');
      report.recommendations.forEach((rec, i) => {
        const priorityIcon = rec.priority === 'high' ? '🔴' : rec.priority === 'medium' ? '🟡' : '🟢';
        console.log(`${i + 1}. ${priorityIcon} **${rec.title}**`);
        console.log(`   ${rec.description}`);
        if (rec.command) {
          console.log(`   \`${rec.command}\``);
        }
        if (rec.estimatedImpact) {
          console.log(`   預期效果：${rec.estimatedImpact}`);
        }
        console.log();
      });
    }
    
    console.log('## 📈 詳細指標\n');
    console.log('### 上下文');
    if (report.metrics.context) {
      console.log(`- 會話數量：${report.metrics.context.sessionCount}`);
      console.log(`- 會話總大小：${report.metrics.context.sessionSizeMB} MB`);
      console.log(`- 大型會話：${report.metrics.context.largeSessions}`);
      console.log(`- 記憶文件：${report.metrics.context.memoryCount}`);
      console.log(`- 記憶總大小：${report.metrics.context.memorySizeMB} MB`);
    }
    console.log();
    
    console.log('### 技能');
    if (report.metrics.skills) {
      console.log(`- 技能總數：${report.metrics.skills.total}`);
      console.log(`- 有文檔：${report.metrics.skills.withSkillMd}`);
      console.log(`- 無文檔：${report.metrics.skills.withoutSkillMd}`);
      console.log(`- 重複技能：${report.metrics.skills.duplicates.length}`);
    }
    console.log();
    
    console.log('### 配置');
    if (report.metrics.config) {
      console.log(`- 配置文件：${report.metrics.config.files}`);
      console.log(`- 重複配置項：${report.metrics.config.duplicateKeys.length}`);
    }
    console.log();
    
    console.log('### 系統');
    if (report.metrics.system) {
      console.log(`- CPU 核心：${report.metrics.system.cpus}`);
      console.log(`- 內存：${report.metrics.system.memoryGB} GB`);
      console.log(`- 可用內存：${report.metrics.system.freeMemoryGB} GB`);
      console.log(`- 運行時間：${report.metrics.system.uptimeHours} 小時`);
      if (report.metrics.system.disk?.percent) {
        console.log(`- 磁盤使用：${report.metrics.system.disk.percent}`);
      }
    }
    console.log();
    
    console.log('='.repeat(60));
  }
}

/**
 * 主函數
 */
async function main() {
  const args = process.argv.slice(2);
  
  console.log('\n🩺 Agent Optimize - Agent 優化診斷工具\n');
  console.log('='.repeat(60));
  console.log();
  
  // 執行診斷
  diagnoseContext();
  diagnoseSkills();
  diagnoseConfig();
  diagnoseSystem();
  
  // 生成報告
  generateReport();
  
  // 如果評分低，提供即時建議
  if (report.score < 70) {
    console.log('\n⚠️  系統需要優化！建議立即執行以下操作:\n');
    report.recommendations
      .filter(r => r.priority === 'high')
      .forEach(rec => {
        console.log(`  - ${rec.title}: ${rec.description}`);
      });
    console.log();
  }
}

// 運行
main().catch(console.error);
