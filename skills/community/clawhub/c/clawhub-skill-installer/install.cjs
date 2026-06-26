#!/usr/bin/env node
/**
 * Skill Installer - 直接从 ClawHub 下载 zip 包安装技能
 * 用法: 
 *   node install.cjs search <关键词>
 *   node install.cjs install <技能名称>
 *   node install.cjs install-batch <技能1> <技能2> ...
 */

const https = require('https');
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const CLAWHUB_API = 'https://clawhub.com';
const SKILLS_DIR = '/Users/xufan65/.openclaw/workspace/skills';
const TEMP_DIR = '/tmp/clawhub-downloads';

// 确保目录存在
if (!fs.existsSync(TEMP_DIR)) {
  fs.mkdirSync(TEMP_DIR, { recursive: true });
}

// HTTP GET 请求
function httpGet(url, headers = {}) {
  return new Promise((resolve, reject) => {
    const urlObj = new URL(url);
    const options = {
      hostname: urlObj.hostname,
      port: urlObj.port || 443,
      path: urlObj.pathname + urlObj.search,
      method: 'GET',
      headers: {
        'User-Agent': 'Mozilla/5.0',
        ...headers
      }
    };

    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', (chunk) => { data += chunk; });
      res.on('end', () => {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          resolve(data);
        } else if (res.statusCode === 302 || res.statusCode === 301) {
          // 跟随重定向
          httpGet(res.headers.location, headers).then(resolve).catch(reject);
        } else {
          reject(new Error(`HTTP ${res.statusCode}: ${data}`));
        }
      });
    });

    req.on('error', reject);
    req.end();
  });
}

// 下载文件
function downloadFile(url, destPath) {
  return new Promise((resolve, reject) => {
    const file = fs.createWriteStream(destPath);
    
    const request = https.get(url, (response) => {
      if (response.statusCode === 302 || response.statusCode === 301) {
        // 跟随重定向
        downloadFile(response.headers.location, destPath).then(resolve).catch(reject);
        return;
      }
      
      response.pipe(file);
      file.on('finish', () => {
        file.close();
        resolve(destPath);
      });
    });

    request.on('error', (err) => {
      fs.unlink(destPath, () => {});
      reject(err);
    });
  });
}

// 搜索技能
async function searchSkill(query) {
  console.log(`🔍 搜索技能: "${query}"`);
  
  try {
    // 使用 ClawHub API 搜索
    const searchUrl = `${CLAWHUB_API}/api/skills?search=${encodeURIComponent(query)}&limit=10`;
    const data = await httpGet(searchUrl);
    const result = JSON.parse(data);
    
    if (!result.skills || result.skills.length === 0) {
      console.log('❌ 未找到相关技能');
      return [];
    }
    
    console.log(`\n找到 ${result.skills.length} 个技能:\n`);
    result.skills.forEach((skill, i) => {
      console.log(`${i + 1}. ${skill.name} - ${skill.description}`);
      console.log(`   评分: ${skill.score || 'N/A'} | 版本: ${skill.version || 'N/A'}`);
      console.log(`   作者: ${skill.author || 'N/A'}\n`);
    });
    
    return result.skills;
  } catch (error) {
    console.error('❌ 搜索失败:', error.message);
    
    // 如果 API 失败，尝试使用 CLI 搜索
    console.log('\n尝试使用 ClawHub CLI 搜索...');
    try {
      const output = execSync(`npx clawhub search ${query} 2>&1`, {
        encoding: 'utf-8',
        cwd: SKILLS_DIR
      });
      console.log(output);
    } catch (cliError) {
      console.error('❌ CLI 搜索也失败:', cliError.message);
    }
    
    return [];
  }
}

// 获取技能详情（包括下载链接）
async function getSkillDetails(skillName) {
  try {
    // 尝试从 ClawHub 网页获取信息
    const skillUrl = `${CLAWHUB_API}/api/skills/${skillName}`;
    const data = await httpGet(skillUrl);
    return JSON.parse(data);
  } catch (error) {
    console.log('⚠️  API 获取失败，尝试从 GitHub 获取...');
    
    // 尝试从 GitHub API 获取（如果技能在 GitHub 上）
    try {
      const githubUrl = `https://api.github.com/search/repositories?q=${encodeURIComponent(skillName)}+clawhub+skill`;
      const data = await httpGet(githubUrl, { 'User-Agent': 'OpenClaw' });
      const result = JSON.parse(data);
      
      if (result.items && result.items.length > 0) {
        const repo = result.items[0];
        return {
          name: skillName,
          github_url: repo.html_url,
          download_url: `${repo.html_url}/archive/refs/heads/main.zip`
        };
      }
    } catch (githubError) {
      console.error('❌ GitHub 搜索失败:', githubError.message);
    }
    
    return null;
  }
}

// 安装技能
async function installSkill(skillName) {
  console.log(`\n📦 安装技能: ${skillName}`);
  
  try {
    // 获取技能详情
    const details = await getSkillDetails(skillName);
    
    if (!details) {
      console.log('❌ 无法获取技能信息');
      return false;
    }
    
    // 构造下载链接（ClawHub 直接下载）
    const downloadUrl = details.download_url || `${CLAWHUB_API}/api/skills/${skillName}/download`;
    const zipPath = path.join(TEMP_DIR, `${skillName}.zip`);
    
    console.log(`📥 下载: ${downloadUrl}`);
    await downloadFile(downloadUrl, zipPath);
    console.log(`✅ 下载完成: ${zipPath}`);
    
    // 解压
    console.log('📂 解压中...');
    const extractDir = path.join(TEMP_DIR, skillName);
    if (fs.existsSync(extractDir)) {
      fs.rmSync(extractDir, { recursive: true });
    }
    fs.mkdirSync(extractDir, { recursive: true });
    
    execSync(`unzip -q "${zipPath}" -d "${extractDir}"`, { stdio: 'inherit' });
    
    // 找到解压后的目录
    const files = fs.readdirSync(extractDir);
    const skillDir = files.find(f => f.startsWith(skillName));
    
    if (!skillDir) {
      console.log('❌ 解压后的目录结构不符合预期');
      return false;
    }
    
    const sourceDir = path.join(extractDir, skillDir);
    const targetDir = path.join(SKILLS_DIR, skillName);
    
    // 去掉版本号（如果存在）
    const versionMatch = skillDir.match(/^(.+)-v?\d+\.\d+\.\d+$/);
    const finalName = versionMatch ? versionMatch[1] : skillName;
    const finalTargetDir = path.join(SKILLS_DIR, finalName);
    
    // 如果目标目录已存在，先删除
    if (fs.existsSync(finalTargetDir)) {
      console.log(`🗑️  删除旧版本: ${finalTargetDir}`);
      fs.rmSync(finalTargetDir, { recursive: true });
    }
    
    // 移动到目标目录
    console.log(`📁 安装到: ${finalTargetDir}`);
    fs.renameSync(sourceDir, finalTargetDir);
    
    // 清理临时文件
    fs.rmSync(zipPath);
    fs.rmSync(extractDir, { recursive: true });
    
    console.log(`✅ 安装完成: ${finalName}`);
    console.log(`📍 位置: ${finalTargetDir}`);
    
    return true;
  } catch (error) {
    console.error('❌ 安装失败:', error.message);
    console.log('\n尝试使用 ClawHub CLI 安装...');
    
    try {
      execSync(`npx clawhub install ${skillName} --force`, {
        encoding: 'utf-8',
        cwd: SKILLS_DIR,
        stdio: 'inherit'
      });
      console.log('✅ 通过 CLI 安装成功');
      return true;
    } catch (cliError) {
      console.error('❌ CLI 安装也失败:', cliError.message);
      return false;
    }
  }
}

// 批量安装
async function installBatch(skillNames) {
  console.log(`\n📦 批量安装 ${skillNames.length} 个技能\n`);
  
  const results = [];
  
  for (const skillName of skillNames) {
    const success = await installSkill(skillName);
    results.push({ skill: skillName, success });
    
    if (skillNames.indexOf(skillName) < skillNames.length - 1) {
      console.log('\n⏳ 等待 3 秒...\n');
      await new Promise(resolve => setTimeout(resolve, 3000));
    }
  }
  
  console.log('\n📊 安装结果:\n');
  results.forEach((r, i) => {
    console.log(`${i + 1}. ${r.skill}: ${r.success ? '✅' : '❌'}`);
  });
  
  const successCount = results.filter(r => r.success).length;
  console.log(`\n总计: ${successCount}/${results.length} 成功`);
}

// 主函数
async function main() {
  const args = process.argv.slice(2);
  const command = args[0];
  const params = args.slice(1);
  
  if (!command) {
    console.log('用法:');
    console.log('  node install.cjs search <关键词>');
    console.log('  node install.cjs install <技能名称>');
    console.log('  node install.cjs install-batch <技能1> <技能2> ...');
    process.exit(1);
  }
  
  switch (command) {
    case 'search':
      if (params.length === 0) {
        console.log('❌ 请提供搜索关键词');
        process.exit(1);
      }
      await searchSkill(params.join(' '));
      break;
      
    case 'install':
      if (params.length === 0) {
        console.log('❌ 请提供技能名称');
        process.exit(1);
      }
      await installSkill(params[0]);
      break;
      
    case 'install-batch':
      if (params.length === 0) {
        console.log('❌ 请提供至少一个技能名称');
        process.exit(1);
      }
      await installBatch(params);
      break;
      
    default:
      console.log('❌ 未知命令:', command);
      process.exit(1);
  }
}

main().catch(console.error);
