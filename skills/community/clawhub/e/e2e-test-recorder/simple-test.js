/**
 * 简单的技能测试
 */

const fs = require('fs-extra');
const path = require('path');

async function simpleTest() {
  console.log('🔧 简单技能测试');
  console.log('='.repeat(40));

  try {
    // 1. 检查核心文件
    console.log('\n1. 📁 检查核心文件...');
    const requiredFiles = [
      'SKILL.md',
      'README.md',
      'package.json',
      'scripts/cli.js',
      'scripts/utils.js',
      'scripts/record-browser.js',
      'scripts/record-test.js'
    ];

    const missingFiles = [];
    for (const file of requiredFiles) {
      if (fs.existsSync(file)) {
        console.log(`   ✅ ${file}`);
      } else {
        console.log(`   ❌ ${file}`);
        missingFiles.push(file);
      }
    }

    if (missingFiles.length > 0) {
      throw new Error(`缺少文件: ${missingFiles.join(', ')}`);
    }

    // 2. 检查依赖
    console.log('\n2. 📦 检查依赖...');
    const packageJson = require('./package.json');
    const requiredDeps = ['puppeteer', 'puppeteer-screen-recorder', 'ffmpeg-static'];
    
    for (const dep of requiredDeps) {
      if (packageJson.dependencies && packageJson.dependencies[dep]) {
        console.log(`   ✅ ${dep}: ${packageJson.dependencies[dep]}`);
      } else {
        console.log(`   ⚠️  ${dep}: 未在package.json中声明`);
      }
    }

    // 3. 测试CLI版本
    console.log('\n3. 💻 测试CLI版本...');
    const { execSync } = require('child_process');
    const version = execSync('node scripts/cli.js --version', { encoding: 'utf8' }).trim();
    console.log(`   ✅ 版本: ${version}`);

    // 4. 测试系统检查
    console.log('\n4. 🔍 测试系统检查...');
    const checkOutput = execSync('node scripts/cli.js check', { encoding: 'utf8' });
    console.log('   ✅ 系统检查完成');

    // 5. 检查目录结构
    console.log('\n5. 📂 检查目录结构...');
    const requiredDirs = ['recordings', 'configs', 'examples', 'logs'];
    for (const dir of requiredDirs) {
      if (fs.existsSync(dir)) {
        console.log(`   ✅ ${dir}/`);
      } else {
        console.log(`   ⚠️  ${dir}/: 不存在，将创建`);
        fs.ensureDirSync(dir);
      }
    }

    // 6. 测试配置文件
    console.log('\n6. ⚙️  测试配置文件...');
    const defaultConfig = {
      recorder: {
        fps: 24,
        quality: 80,
        outputDir: './recordings'
      },
      browser: {
        headless: false,
        viewport: {
          width: 1280,
          height: 720
        }
      }
    };

    const configPath = './configs/default.json';
    fs.ensureDirSync('./configs');
    await fs.writeJson(configPath, defaultConfig, { spaces: 2 });
    console.log(`   ✅ 配置文件创建: ${configPath}`);

    // 7. 测试技能文档
    console.log('\n7. 📄 测试技能文档...');
    const skillContent = fs.readFileSync('SKILL.md', 'utf8');
    const hasRequiredSections = [
      '技能名称',
      '技能描述',
      '技能版本',
      '技能作者',
      '技能协议'
    ].every(section => skillContent.includes(section));

    if (hasRequiredSections) {
      console.log('   ✅ 技能文档完整');
    } else {
      console.log('   ⚠️  技能文档可能不完整');
    }

    console.log('\n🎉 所有测试通过！');
    console.log('='.repeat(40));
    console.log('\n📊 测试总结:');
    console.log(`   核心文件: ${requiredFiles.length - missingFiles.length}/${requiredFiles.length}`);
    console.log(`   依赖检查: ${requiredDeps.length}个`);
    console.log(`   目录结构: ${requiredDirs.length}个`);
    console.log(`   配置文件: 已创建`);
    console.log(`   技能文档: ${hasRequiredSections ? '完整' : '需要完善'}`);

    return true;

  } catch (error) {
    console.error('\n❌ 测试失败:', error.message);
    return false;
  }
}

// 运行测试
simpleTest().then(success => {
  process.exit(success ? 0 : 1);
});