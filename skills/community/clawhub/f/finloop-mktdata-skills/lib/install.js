const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const SKILLS_DIR = path.join(__dirname, '..', '.agents', 'skills');
const TARGET_DIR = path.join(process.cwd(), '.agents', 'skills');

/**
 * 确保目标目录存在
 */
function ensureTargetDir() {
  const agentsDir = path.join(process.cwd(), '.agents');
  if (!fs.existsSync(agentsDir)) {
    fs.mkdirSync(agentsDir, { recursive: true });
  }
  if (!fs.existsSync(TARGET_DIR)) {
    fs.mkdirSync(TARGET_DIR, { recursive: true });
  }
}

/**
 * 复制目录
 */
function copyDirectory(src, dest) {
  if (!fs.existsSync(src)) {
    throw new Error(`源目录不存在: ${src}`);
  }

  if (!fs.existsSync(dest)) {
    fs.mkdirSync(dest, { recursive: true });
  }

  const entries = fs.readdirSync(src, { withFileTypes: true });

  for (const entry of entries) {
    const srcPath = path.join(src, entry.name);
    const destPath = path.join(dest, entry.name);

    if (entry.isDirectory()) {
      copyDirectory(srcPath, destPath);
    } else {
      fs.copyFileSync(srcPath, destPath);
    }
  }
}

/**
 * 安装 skill
 */
async function installSkill(skillName) {
  try {
    const skillPath = path.join(SKILLS_DIR, skillName);
    
    if (!fs.existsSync(skillPath)) {
      throw new Error(`Skill "${skillName}" 不存在`);
    }

    const manifestPath = path.join(skillPath, 'skill-manifest.json');
    if (!fs.existsSync(manifestPath)) {
      throw new Error(`Skill "${skillName}" 缺少 skill-manifest.json 文件`);
    }

    const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf-8'));
    
    console.log(`\n📦 正在安装 skill: ${manifest.name || skillName}`);
    console.log(`   版本: ${manifest.version || 'unknown'}`);
    console.log(`   描述: ${manifest.description || '无描述'}`);

    ensureTargetDir();

    const targetSkillPath = path.join(TARGET_DIR, skillName);
    
    if (fs.existsSync(targetSkillPath)) {
      console.log(`\n⚠️  警告: Skill "${skillName}" 已存在于目标目录`);
      console.log('   是否覆盖? (y/n)');
      
      const readline = require('readline');
      const rl = readline.createInterface({
        input: process.stdin,
        output: process.stdout
      });

      return new Promise((resolve, reject) => {
        rl.question('', (answer) => {
          rl.close();
          if (answer.toLowerCase() === 'y' || answer.toLowerCase() === 'yes') {
            fs.rmSync(targetSkillPath, { recursive: true, force: true });
            copyDirectory(skillPath, targetSkillPath);
            console.log(`\n✅ Skill "${skillName}" 安装成功!`);
            console.log(`   位置: ${targetSkillPath}`);
            resolve();
          } else {
            console.log('❌ 安装已取消');
            reject(new Error('用户取消安装'));
          }
        });
      });
    } else {
      copyDirectory(skillPath, targetSkillPath);
      console.log(`\n✅ Skill "${skillName}" 安装成功!`);
      console.log(`   位置: ${targetSkillPath}`);
    }
  } catch (error) {
    throw new Error(`安装失败: ${error.message}`);
  }
}

/**
 * 列出所有可用的 skills
 * @param {string} [binName='finloop-skills'] - 当前调用的 CLI 名称，用于安装提示
 */
async function listSkills(binName = 'finloop-skills') {
  try {
    if (!fs.existsSync(SKILLS_DIR)) {
      console.log('❌ Skills 目录不存在');
      return;
    }

    const skills = fs.readdirSync(SKILLS_DIR).filter(item => {
      const itemPath = path.join(SKILLS_DIR, item);
      return fs.statSync(itemPath).isDirectory();
    });

    if (skills.length === 0) {
      console.log('📦 没有找到可用的 skills');
      return;
    }

    console.log('\n📦 可用的 Skills:\n');
    
    for (const skill of skills) {
      const manifestPath = path.join(SKILLS_DIR, skill, 'skill-manifest.json');
      if (fs.existsSync(manifestPath)) {
        try {
          const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf-8'));
          console.log(`  ✨ ${manifest.name || skill}`);
          console.log(`     版本: ${manifest.version || 'unknown'}`);
          console.log(`     ID: ${manifest.id || skill}`);
          console.log(`     描述: ${manifest.description || '无描述'}`);
          if (manifest.tags && manifest.tags.length > 0) {
            console.log(`     标签: ${manifest.tags.join(', ')}`);
          }
          console.log('');
        } catch (error) {
          console.log(`  ⚠️  ${skill} (manifest 解析失败)`);
        }
      } else {
        console.log(`  ⚠️  ${skill} (缺少 manifest)`);
      }
    }

    console.log(`\n💡 使用 "npx ${binName} install <skill-id>" 安装 skill\n`);
  } catch (error) {
    throw new Error(`列出 skills 失败: ${error.message}`);
  }
}

module.exports = {
  installSkill,
  listSkills
};

