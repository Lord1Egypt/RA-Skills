#!/usr/bin/env node
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
  ListResourcesRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';
import Imap from 'imap';
import { simpleParser } from 'mailparser';
import nodemailer from 'nodemailer';
import dotenv from 'dotenv';

dotenv.config({ quiet: true });

const EMAIL_USER = process.env.EMAIL_USER;
const EMAIL_PASSWORD = process.env.EMAIL_PASSWORD;

if (!EMAIL_USER || !EMAIL_PASSWORD) {
  console.error('❌ 缺少环境变量: EMAIL_USER 或 EMAIL_PASSWORD');
  process.exit(1);
}

const IMAP_CONFIG = {
  user: EMAIL_USER,
  password: EMAIL_PASSWORD,
  host: 'imap.exmail.qq.com',
  port: 993,
  tls: true,
  tlsOptions: { rejectUnauthorized: false },
};

const SMTP_CONFIG = {
  host: 'smtp.exmail.qq.com',
  port: 465,
  secure: true,
  auth: { user: EMAIL_USER, pass: EMAIL_PASSWORD },
  tls: { rejectUnauthorized: false },
};

const server = new Server(
  { name: 'exmail-mcp', version: '1.0.0' },
  { capabilities: { tools: {} } }
);

// 列出工具
server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: 'get_recent_emails',
      description: '获取最近邮件列表（默认最近20封）',
      inputSchema: {
        type: 'object',
        properties: {
          days: { type: 'number', description: '最近几天内的邮件，默认7天', default: 7 },
          count: { type: 'number', description: '最多返回多少封，默认20', default: 20 },
        },
      },
    },
    {
      name: 'get_email_content',
      description: '获取指定邮件的详细内容',
      inputSchema: {
        type: 'object',
        properties: {
          uid: { type: 'string', description: '邮件UID' },
          mailbox: { type: 'string', description: '邮箱文件夹，默认INBOX', default: 'INBOX' },
        },
        required: ['uid'],
      },
    },
    {
      name: 'send_email',
      description: '发送邮件',
      inputSchema: {
        type: 'object',
        properties: {
          to: { type: 'string', description: '收件人邮箱' },
          subject: { type: 'string', description: '邮件主题' },
          text: { type: 'string', description: '纯文本内容' },
          html: { type: 'string', description: 'HTML内容（可选）' },
          cc: { type: 'string', description: '抄送（可选）' },
        },
        required: ['to', 'subject', 'text'],
      },
    },
    {
      name: 'search_emails',
      description: '搜索邮件',
      inputSchema: {
        type: 'object',
        properties: {
          keyword: { type: 'string', description: '搜索关键词（主题/发件人）' },
          count: { type: 'number', description: '最多返回多少封，默认10', default: 10 },
        },
        required: ['keyword'],
      },
    },
  ],
}));

// 执行工具
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  try {
    if (name === 'get_recent_emails') {
      const result = await getRecentEmails(args.days || 7, args.count || 20);
      return { content: [{ type: 'text', text: JSON.stringify(result, null, 2) }] };
    }
    if (name === 'get_email_content') {
      const result = await getEmailContent(args.uid, args.mailbox || 'INBOX');
      return { content: [{ type: 'text', text: JSON.stringify(result, null, 2) }] };
    }
    if (name === 'send_email') {
      const result = await sendEmail(args);
      return { content: [{ type: 'text', text: JSON.stringify(result, null, 2) }] };
    }
    if (name === 'search_emails') {
      const result = await searchEmails(args.keyword, args.count || 10);
      return { content: [{ type: 'text', text: JSON.stringify(result, null, 2) }] };
    }
    return { content: [{ type: 'text', text: `未知工具: ${name}` }], isError: true };
  } catch (error) {
    return { content: [{ type: 'text', text: `错误: ${error.message}` }], isError: true };
  }
});

// 获取最近邮件
function getRecentEmails(days, count) {
  return new Promise((resolve, reject) => {
    const imap = new Imap(IMAP_CONFIG);
    const emails = [];
    const since = new Date();
    since.setDate(since.getDate() - days);

    imap.once('ready', () => {
      imap.openBox('INBOX', false, (err, box) => {
        if (err) return reject(err);
        // 搜索最近N天的邮件
        const searchCriteria = [['SINCE', since]];
        imap.search(searchCriteria, (err, results) => {
          if (err) return reject(err);
          if (!results || results.length === 0) {
            imap.end();
            return resolve([]);
          }
          // 取最后 count 封
          const uids = results.slice(-count);
          const f = imap.fetch(uids, { bodies: '', struct: true });
          f.on('message', (msg, seqno) => {
            msg.on('body', (stream) => {
              let buffer = '';
              stream.on('data', (chunk) => { buffer += chunk.toString('utf8'); });
              stream.once('end', () => {
                simpleParser(buffer, (err, mail) => {
                  if (!err) {
                    emails.push({
                      uid: seqno,
                      date: mail.date,
                      from: mail.from?.text || '',
                      to: mail.to?.text || '',
                      subject: mail.subject || '(无主题)',
                      text: (mail.text || '').substring(0, 500),
                    });
                  }
                });
              });
            });
          });
          f.once('error', reject);
          f.once('end', () => {
            setTimeout(() => {
              imap.end();
              resolve(emails.sort((a, b) => new Date(b.date) - new Date(a.date)));
            }, 500);
          });
        });
      });
    });
    imap.once('error', reject);
    imap.connect();
  });
}

// 获取邮件详情
function getEmailContent(uid, mailbox) {
  return new Promise((resolve, reject) => {
    const imap = new Imap(IMAP_CONFIG);
    imap.once('ready', () => {
      imap.openBox(mailbox, false, (err, box) => {
        if (err) return reject(err);
        const f = imap.fetch([uid], { bodies: '', struct: true });
        f.on('message', (msg) => {
          msg.on('body', (stream) => {
            let buffer = '';
            stream.on('data', (chunk) => { buffer += chunk.toString('utf8'); });
            stream.once('end', () => {
              simpleParser(buffer, (err, mail) => {
                if (err) return reject(err);
                resolve({
                  uid,
                  date: mail.date,
                  from: mail.from?.text || '',
                  to: mail.to?.text || '',
                  cc: mail.cc?.text || '',
                  subject: mail.subject || '(无主题)',
                  text: mail.text || '',
                  html: mail.html || '',
                  attachments: mail.attachments?.map(a => ({ filename: a.filename, size: a.size })) || [],
                });
              });
            });
          });
        });
        f.once('error', reject);
        f.once('end', () => imap.end());
      });
    });
    imap.once('error', reject);
    imap.connect();
  });
}

// 发送邮件
async function sendEmail({ to, subject, text, html, cc }) {
  const transporter = nodemailer.createTransport(SMTP_CONFIG);
  const info = await transporter.sendMail({
    from: EMAIL_USER,
    to,
    cc: cc || undefined,
    subject,
    text,
    html: html || undefined,
  });
  return { success: true, messageId: info.messageId, to, subject };
}

// 搜索邮件
function searchEmails(keyword, count) {
  return new Promise((resolve, reject) => {
    const imap = new Imap(IMAP_CONFIG);
    const emails = [];

    imap.once('ready', () => {
      imap.openBox('INBOX', false, (err, box) => {
        if (err) return reject(err);
        // 搜索主题或发件人包含关键词的邮件
        const searchCriteria = [['OR', ['SUBJECT', keyword], ['FROM', keyword]]];
        imap.search(searchCriteria, (err, results) => {
          if (err) return reject(err);
          if (!results || results.length === 0) {
            imap.end();
            return resolve([]);
          }
          const uids = results.slice(-count);
          const f = imap.fetch(uids, { bodies: '', struct: true });
          f.on('message', (msg, seqno) => {
            msg.on('body', (stream) => {
              let buffer = '';
              stream.on('data', (chunk) => { buffer += chunk.toString('utf8'); });
              stream.once('end', () => {
                simpleParser(buffer, (err, mail) => {
                  if (!err) {
                    emails.push({
                      uid: seqno,
                      date: mail.date,
                      from: mail.from?.text || '',
                      subject: mail.subject || '(无主题)',
                      text: (mail.text || '').substring(0, 300),
                    });
                  }
                });
              });
            });
          });
          f.once('error', reject);
          f.once('end', () => {
            setTimeout(() => {
              imap.end();
              resolve(emails.sort((a, b) => new Date(b.date) - new Date(a.date)));
            }, 500);
          });
        });
      });
    });
    imap.once('error', reject);
    imap.connect();
  });
}

// 启动
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error(`✅ Exmail MCP 已启动 (${EMAIL_USER})`);
}

main().catch((err) => {
  console.error('启动失败:', err.message);
  process.exit(1);
});
