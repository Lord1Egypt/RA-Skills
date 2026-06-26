#!/usr/bin/env node
/**
 * A 股股票技能配置向导
 */

const fs = require('fs');
const path = require('path');
const readline = require('readline');

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

function ask(question) {
  return new Promise((resolve) => {
    rl.question(question, (answer) => {
      resolve(answer);
    });
  });
}

async function main() {
  console.log('📈 A 股每日精选 - 配置向导\n');
  
  // 读取当前配置
  const indexPath = path.join(__dirname, 'index.js');
  let indexContent = fs.readFileSync(indexPath, 'utf-8');
  
  // 当前邮箱
  const emailMatch = indexContent.match(/email:\s*'([^']+)'/);
  const currentEmail = emailMatch ? emailMatch[1] : '8@batype.com';
  
  // 当前价格上限
  const priceMatch = indexContent.match(/priceLimit:\s*(\d+)/);
  const currentPrice = priceMatch ? priceMatch[1] : 20;
  
  console.log(`当前配置:`);
  console.log(`  邮箱：${currentEmail}`);
  console.log(`  价格上限：¥${currentPrice}\n`);
  
  // 询问是否修改
  const modify = await ask('是否修改配置？(y/n) [n]: ');
  
  if (modify.toLowerCase() === 'y') {
    const newEmail = await ask(`新邮箱 [${currentEmail}]: `);
    const newPrice = await ask(`新价格上限 [${currentPrice}]: `);
    
    const email = newEmail || currentEmail;
    const price = newPrice || currentPrice;
    
    // 更新配置
    indexContent = indexContent.replace(
      /email:\s*'[^']+'/,
      `email: '${email}'`
    );
    indexContent = indexContent.replace(
      /priceLimit:\s*\d+/,
      `priceLimit: ${price}`
    );
    
    fs.writeFileSync(indexPath, indexContent);
    console.log(`\n✅ 配置已更新:`);
    console.log(`  邮箱：${email}`);
    console.log(`  价格上限：¥${price}`);
  }
  
  // SMTP 配置
  console.log('\n--- SMTP 邮件配置 ---');
  const setupSmtp = await ask('是否配置 SMTP 发送邮件？(y/n) [n]: ');
  
  if (setupSmtp.toLowerCase() === 'y') {
    console.log('\n常见邮箱 SMTP 配置:');
    console.log('  Gmail: smtp.gmail.com:587 (需要应用专用密码)');
    console.log('  QQ 邮箱：smtp.qq.com:587 (需要授权码)');
    console.log('  163 邮箱：smtp.163.com:587');
    console.log('  Outlook: smtp-mail.outlook.com:587\n');
    
    const host = await ask('SMTP 服务器：');
    const port = await ask('端口 [587]: ') || '587';
    const user = await ask('用户名 (邮箱): ');
    const pass = await ask('密码/授权码：');
    const from = await ask(`发件人邮箱 [${user}]: `) || user;
    
    const smtpConfig = {
      host,
      port: parseInt(port),
      secure: port === '465',
      user,
      pass,
      from: from || user,
    };
    
    console.log('\n✅ SMTP 配置完成！');
    console.log('\n使用方法:');
    console.log(`  export SMTP_CONFIG='${JSON.stringify(smtpConfig)}'`);
    console.log('\n或者添加到 ~/.zshrc 或 ~/.bashrc:');
    console.log(`  export SMTP_CONFIG='${JSON.stringify(smtpConfig)}'`);
    
    // 保存到 .env 文件
    const envPath = path.join(__dirname, '.env');
    fs.writeFileSync(envPath, `SMTP_CONFIG=${JSON.stringify(smtpConfig)}\n`);
    console.log(`\n💾 配置已保存到：${envPath}`);
  }
  
  console.log('\n--- 完成 ---');
  console.log('运行以下命令测试:');
  console.log('  node index.js\n');
  
  rl.close();
}

main().catch(console.error);
