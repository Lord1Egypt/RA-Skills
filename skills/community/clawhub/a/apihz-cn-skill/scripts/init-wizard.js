#!/usr/bin/env node
/**
 * 接口盒子 API Skill - 初始化向导
 * ApiHz Initialization Wizard
 * 
 * 首次使用时运行，引导用户注册并配置账号
 */

const path = require('path');
const { ApiHzAuth } = require('../src/auth.js');

async function main() {
  const auth = new ApiHzAuth({
    // 使用动态路径，适配任意 OpenClaw 工作区
    workspace: process.env.OPENCLAW_WORKSPACE || path.join(process.env.HOME || '', '.openclaw', 'workspace')
  });
  
  const result = await auth.initialize();
  
  if (!result.configured) {
    console.log('\n💡 提示:');
    console.log('   配置完成后，运行以下命令同步 API 列表:');
    console.log('   node skills/apihz/scripts/init-wizard.js\n');
  } else if (result.encrypted) {
    console.log('\n🔐 安全提示:');
    console.log('   KEY 和 DMSG 已加密存储');
    console.log('   加密密钥基于本机指纹生成');
    console.log('   不要将凭证文件复制到其他机器\n');
  }
  
  return result;
}

// 运行向导
main().catch(console.error);
