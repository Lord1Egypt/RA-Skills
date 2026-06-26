#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

// 统一的状态管理文件
// 提供给 Agent 用于快速读取和更新 JSON 数据库

const args = process.argv.slice(2);
const command = args[0];

function showHelp() {
  console.log(`
Dream Novel Skill - 状态管理辅助工具
用法: node state-manager.js <command> [options...]

命令:
  init <project_dir>                    初始化一个项目数据结构
  read <project_dir> <db_name>          读取特定的数据库 (characters, foreshadowing, world, summary)
  update <project_dir> <db_name> <json> 更新/合并指定数据库的内容
  log <project_dir> <chapter> <file>    为指定章节保存生成的 txt 和摘要
`);
}

if (!command || command === 'help') {
  showHelp();
  process.exit(0);
}

const projectDir = args[1];
if (!projectDir) {
  console.error('Error: 必须提供 project_dir');
  process.exit(1);
}

const dbFiles = {
  characters: 'characters.json',
  foreshadowing: 'foreshadowing.json',
  world: 'world.json',
  summary: 'summary.json'
};

const fullPath = path.resolve(projectDir);

if (command === 'init') {
  if (!fs.existsSync(fullPath)) {
    fs.mkdirSync(fullPath, { recursive: true });
  }
  
  // 初始化空结构
  const initialData = {
    characters: { characters: [], relationships: [], factions: [], metadata: { totalCharacters: 0, activeCharacters: 0, lastUpdated: 0 } },
    foreshadowing: { foreshadowing: [], statistics: { total: 0, active: 0, resolved: 0, overdue: 0 } },
    world: { entries: [] },
    summary: { globalSummary: "", arcSummaries: [], chapterSummaries: [] }
  };

  for (const [key, filename] of Object.entries(dbFiles)) {
    const filePath = path.join(fullPath, filename);
    if (!fs.existsSync(filePath)) {
      fs.writeFileSync(filePath, JSON.stringify(initialData[key], null, 2), 'utf-8');
      console.log(`Created ${filePath}`);
    }
  }
  console.log(`Project initialized at ${fullPath}`);
  
} else if (command === 'read') {
  const dbName = args[2];
  if (!dbFiles[dbName]) {
    console.error(`Unknown DB: ${dbName}. Options: ${Object.keys(dbFiles).join(', ')}`);
    process.exit(1);
  }
  const filePath = path.join(fullPath, dbFiles[dbName]);
  if (!fs.existsSync(filePath)) {
    console.error(`File not found: ${filePath}`);
    process.exit(1);
  }
  console.log(fs.readFileSync(filePath, 'utf-8'));
  
} else if (command === 'update') {
  const dbName = args[2];
  let jsonData = args[3];
  
  if (!dbFiles[dbName]) {
    console.error(`Unknown DB: ${dbName}`);
    process.exit(1);
  }
  
  const filePath = path.join(fullPath, dbFiles[dbName]);
  if (!fs.existsSync(filePath)) {
    console.error(`File not found: ${filePath}, please run 'init' first`);
    process.exit(1);
  }
  
  // 支持从文件读取 json 参数，以防命令行超出长度限制
  if (jsonData.endsWith('.json') && fs.existsSync(jsonData)) {
    jsonData = fs.readFileSync(jsonData, 'utf-8');
  }

  let newObj;
  try {
    // 很多时候 LLM 输出的 JSON 会带有 markdown 的 ```json 前缀
    let cleanJson = jsonData.trim();
    if (cleanJson.startsWith('\`\`\`json')) {
      cleanJson = cleanJson.replace(/^```json\n/, '').replace(/\n```$/, '');
    }
    else if (cleanJson.startsWith('\`\`\`')) {
      cleanJson = cleanJson.replace(/^```\n/, '').replace(/\n```$/, '');
    }
    newObj = JSON.parse(cleanJson);
  } catch (e) {
    console.error('JSON parse error:', e.message);
    process.exit(1);
  }
  
  // 对于简单的脚本，直接全量覆盖/更新。在真实复杂的实现中可以做字段级 merge，此处从简以覆盖式更新为主
  fs.writeFileSync(filePath, JSON.stringify(newObj, null, 2), 'utf-8');
  console.log(`Successfully updated ${dbName} in ${filePath}`);
  
} else {
  console.error(`Unknown command: ${command}`);
  showHelp();
  process.exit(1);
}
