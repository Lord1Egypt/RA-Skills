#!/usr/bin/env node
/**
 * OpenClaw Email Skill
 * 支持 IMAP 收邮件和 SMTP 发邮件
 */

const fs = require('fs');
const path = require('path');

// 加载配置
const configPath = path.join(__dirname, '../config/email.json');
let config = {};

try {
  config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
} catch (err) {
  console.error('读取配置文件失败:', err.message);
  console.error('请检查 ~/.openclaw/skills/email/config/email.json');
  process.exit(1);
}

// 命令行参数处理
const args = process.argv.slice(2);
const command = args[0];

async function sendEmail(to, subject, content, options = {}) {
  const nodemailer = require('nodemailer');

  const transporter = nodemailer.createTransport({
    host: config.smtp.host,
    port: config.smtp.port,
    secure: config.smtp.secure,
    auth: {
      user: config.email,
      pass: config.password
    }
  });

  const mailOptions = {
    from: config.email,
    to: to,
    subject: subject,
    text: options.html ? undefined : content,
    html: options.html ? content : undefined,
    attachments: options.attachments || []
  };

  try {
    const info = await transporter.sendMail(mailOptions);
    console.log(JSON.stringify({
      success: true,
      messageId: info.messageId,
      response: info.response
    }));
    return info;
  } catch (err) {
    console.error(JSON.stringify({
      success: false,
      error: err.message
    }));
    throw err;
  }
}

async function listEmails(count = 10, unreadOnly = false) {
  const Imap = require('imap');
  const { simpleParser } = require('mailparser');

  return new Promise((resolve, reject) => {
    const imap = new Imap({
      user: config.email,
      password: config.password,
      host: config.imap.host,
      port: config.imap.port,
      tls: config.imap.secure,
      tlsOptions: { rejectUnauthorized: false }
    });

    const emails = [];

    imap.once('ready', () => {
      imap.openBox('INBOX', true, (err, box) => {
        if (err) {
          imap.end();
          reject(err);
          return;
        }

        const searchCriteria = unreadOnly ? ['UNSEEN'] : ['ALL'];

        imap.search(searchCriteria, (err, results) => {
          if (err || results.length === 0) {
            imap.end();
            resolve([]);
            return;
          }

          const fetchIds = results.slice(-count);
          const f = imap.fetch(fetchIds, { bodies: 'HEADER.FIELDS (FROM TO SUBJECT DATE)' });
          let pending = fetchIds.length;

          f.on('message', (msg, seqno) => {
            let buffer = '';
            msg.on('body', (stream) => {
              stream.on('data', (chunk) => { buffer += chunk.toString('utf8'); });
            });

            msg.once('end', async () => {
              try {
                const parsed = await simpleParser(buffer);
                emails.push({
                  seqno: seqno,
                  uid: fetchIds[emails.length],
                  from: parsed.from?.text || '',
                  subject: parsed.subject || '(无主题)',
                  date: parsed.date?.toISOString() || new Date().toISOString()
                });
              } catch (e) {
                // 解析失败继续
              }

              pending--;
              if (pending === 0) {
                console.log(JSON.stringify(emails, null, 2));
                setTimeout(() => {
                  imap.end();
                  setTimeout(() => process.exit(0), 100);
                }, 100);
              }
            });
          });

          f.once('error', (err) => {
            imap.end();
            reject(err);
          });
        });
      });
    });

    imap.once('error', (err) => reject(err));
    imap.connect();
  });
}

async function readEmail(uid) {
  const Imap = require('imap');
  const { simpleParser } = require('mailparser');

  return new Promise((resolve, reject) => {
    const imap = new Imap({
      user: config.email,
      password: config.password,
      host: config.imap.host,
      port: config.imap.port,
      tls: config.imap.secure,
      tlsOptions: { rejectUnauthorized: false }
    });

    imap.once('ready', () => {
      imap.openBox('INBOX', true, (err, box) => {
        if (err) {
          imap.end();
          reject(err);
          return;
        }

        const f = imap.fetch([uid], { bodies: '' });

        f.on('message', (msg) => {
          let emailBuffer = '';

          msg.on('body', (stream) => {
            stream.on('data', (chunk) => {
              emailBuffer += chunk.toString('utf8');
            });
          });

          msg.once('end', async () => {
            try {
              const parsed = await simpleParser(emailBuffer);
              resolve({
                from: parsed.from?.text || '',
                to: parsed.to?.text || '',
                subject: parsed.subject || '(无主题)',
                date: parsed.date,
                text: parsed.text || '',
                html: parsed.html || '',
                attachments: parsed.attachments?.map(a => ({
                  filename: a.filename,
                  contentType: a.contentType,
                  size: a.size
                })) || []
              });
            } catch (e) {
              reject(e);
            }
          });
        });

        f.once('error', (err) => {
          reject(err);
        });

        f.once('end', () => {
          imap.end();
        });
      });
    });

    imap.once('error', (err) => {
      reject(err);
    });

    imap.connect();
  });
}

// 主命令处理
async function main() {
  switch (command) {
    case 'send': {
      const to = args[1];
      const subject = args[2];
      const content = args[3];
      const isHtml = args[4] === '--html';

      if (!to || !subject || !content) {
        console.error('用法: email send <to> <subject> <content> [--html] [--attach <path>]');
        process.exit(1);
      }

      // 解析附件参数
      const attachments = [];
      const attachIndex = args.indexOf('--attach');
      if (attachIndex !== -1 && args[attachIndex + 1]) {
        const attachPath = args[attachIndex + 1];
        if (fs.existsSync(attachPath)) {
          attachments.push({
            filename: path.basename(attachPath),
            path: attachPath
          });
        } else {
          console.error(`附件不存在: ${attachPath}`);
          process.exit(1);
        }
      }

      await sendEmail(to, subject, content, { html: isHtml, attachments });
      break;
    }

    case 'list': {
      const count = parseInt(args[1]) || 10;
      const unreadOnly = args.includes('--unread');

      const emails = await listEmails(count, unreadOnly);
      console.log(JSON.stringify(emails, null, 2));
      break;
    }

    case 'read': {
      const uid = parseInt(args[1]);

      if (!uid) {
        console.error('用法: email read <uid>');
        process.exit(1);
      }

      const email = await readEmail(uid);
      console.log(JSON.stringify(email, null, 2));
      break;
    }

    case 'test': {
      console.log('配置信息:');
      console.log(`  邮箱: ${config.email}`);
      console.log(`  SMTP: ${config.smtp.host}:${config.smtp.port}`);
      console.log(`  IMAP: ${config.imap.host}:${config.imap.port}`);
      console.log('\n测试连接...');

      try {
        const emails = await listEmails(1);
        console.log(`✅ IMAP 连接成功，收件箱有邮件`);
      } catch (err) {
        console.error(`❌ IMAP 连接失败: ${err.message}`);
      }
      break;
    }

    default:
      console.log('OpenClaw Email Skill');
      console.log('');
      console.log('用法:');
      console.log('  email send <to> <subject> <content> [--html]  发送邮件');
      console.log('  email list [count] [--unread]                列出邮件');
      console.log('  email read <uid>                             读取邮件');
      console.log('  email test                                   测试配置');
      console.log('');
      console.log('示例:');
      console.log('  email send test@example.com "主题" "邮件内容" [--attach /path/to/file]');
      console.log('  email list 5');
      console.log('  email list --unread');
      console.log('  email read 12345');
      break;
  }
}

main().catch(err => {
  console.error('错误:', err.message);
  process.exit(1);
});
