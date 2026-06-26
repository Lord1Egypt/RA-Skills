/**
 * 163 Mail Skill - 163 邮箱收发邮件
 * 
 * 使用 IMAP 接收邮件，SMTP 发送邮件
 */

const Imap = require('imap');
const { simpleParser } = require('mailparser');
const nodemailer = require('nodemailer');
const fs = require('fs');
const path = require('path');

// 配置
let config = null;

function loadConfig() {
    if (config) return config;
    
    const configPath = path.join(__dirname, 'config.json');
    if (!fs.existsSync(configPath)) {
        throw new Error('配置文件不存在，请复制 config.template.json 为 config.json 并填写配置');
    }
    
    config = JSON.parse(fs.readFileSync(configPath, 'utf-8'));
    
    // 支持环境变量覆盖
    if (process.env['163MAIL_EMAIL']) config.email = process.env['163MAIL_EMAIL'];
    if (process.env['163MAIL_IMAP_PASS']) config.imapPassword = process.env['163MAIL_IMAP_PASS'];
    if (process.env['163MAIL_SMTP_PASS']) config.smtpPassword = process.env['163MAIL_SMTP_PASS'];
    
    return config;
}

// IMAP 连接
function getImapClient() {
    const cfg = loadConfig();
    
    const imap = new Imap({
        user: cfg.email,
        password: cfg.imapPassword,
        host: cfg.imap?.host || 'imap.163.com',
        port: cfg.imap?.port || 993,
        tls: cfg.imap?.tls !== false,
        tlsOptions: { rejectUnauthorized: false },
        connTimeout: 10000,
        authTimeout: 10000
    });
    
    // 连接成功后发送 ID 命令
    imap.once('ready', () => {
        console.log('[163Mail] IMAP connected, sending ID command...');
        
        // 使用 imap.id() 方法发送 ID 命令
        // 格式：id({ name: "OpenClaw", version: "1.0", vendor: "myclient" })
        imap.id({
            name: "OpenClaw",
            version: "1.0",
            vendor: "myclient"
        }, (err, idData) => {
            if (err) {
                console.log('[163Mail] ID command error:', err.message);
            } else {
                console.log('[163Mail] ID command success!');
                console.log('[163Mail] Server ID:', idData);
            }
        });
    });
    
    return imap;
}

// SMTP  transporter
function getSmtpTransporter() {
    const cfg = loadConfig();
    
    return nodemailer.createTransport({
        host: cfg.smtp?.host || 'smtp.163.com',
        port: cfg.smtp?.port || 465,
        secure: cfg.smtp?.tls !== false,
        auth: {
            user: cfg.email,
            pass: cfg.smtpPassword || cfg.imapPassword
        },
        connectionTimeout: 10000
    });
}

// 连接 IMAP 并执行操作
function withImap(operation) {
    return new Promise((resolve, reject) => {
        const imap = getImapClient();
        
        imap.once('ready', () => {
            operation(imap)
                .then(result => {
                    imap.end();
                    resolve(result);
                })
                .catch(err => {
                    imap.end();
                    reject(err);
                });
        });
        
        imap.once('error', reject);
        imap.once('end', () => console.log('[163Mail] IMAP connection ended'));
        
        imap.connect();
    });
}

// 查看收件箱
async function listInbox(limit = 10) {
    return withImap(async (imap) => {
        return new Promise((resolve, reject) => {
            imap.openBox('INBOX', false, (err, box) => {
                if (err) return reject(new Error(`打开收件箱失败：${err.message}`));
                
                const searchCriteria = ['ALL'];
                const fetchOptions = {
                    bodies: 'HEADER.FIELDS (FROM TO SUBJECT DATE)',
                    struct: true
                };
                
                imap.search(searchCriteria, (err, results) => {
                    if (err) return reject(new Error(`搜索邮件失败：${err.message}`));
                    
                    if (results.length === 0) {
                        return resolve({ messages: [], total: 0 });
                    }
                    
                    // 获取最新的 limit 封邮件
                    const fetchIds = results.slice(-limit).reverse();
                    const messages = [];
                    let fetched = 0;
                    
                    const f = imap.fetch(fetchIds, fetchOptions);
                    
                    f.on('message', (msg) => {
                        const emailData = {};
                        
                        msg.on('body', (stream) => {
                            simpleParser(stream).then(parsed => {
                                Object.assign(emailData, {
                                    from: parsed.from?.text,
                                    to: parsed.to?.text,
                                    subject: parsed.subject,
                                    date: parsed.date,
                                    preview: parsed.text?.substring(0, 100)
                                });
                            });
                        });
                        
                        msg.once('attributes', (attrs) => {
                            emailData.id = attrs.uid;
                            emailData.seen = attrs.flags.includes('\\Seen');
                        });
                        
                        msg.once('end', () => {
                            if (emailData.id) {
                                messages.push(emailData);
                            }
                            fetched++;
                            if (fetched === fetchIds.length) {
                                resolve({ messages, total: results.length });
                            }
                        });
                    });
                    
                    f.once('error', reject);
                });
            });
        });
    });
}

// 查看文件夹
async function listFolder(folder, limit = 10) {
    return withImap(async (imap) => {
        return new Promise((resolve, reject) => {
            imap.openBox(folder, false, (err, box) => {
                if (err) return reject(new Error(`打开文件夹失败：${err.message}`));
                
                imap.search(['ALL'], (err, results) => {
                    if (err) return reject(new Error(`搜索邮件失败：${err.message}`));
                    
                    if (results.length === 0) {
                        return resolve({ messages: [], total: 0, folder });
                    }
                    
                    const fetchIds = results.slice(-limit).reverse();
                    const messages = [];
                    let fetched = 0;
                    
                    const f = imap.fetch(fetchIds, {
                        bodies: 'HEADER.FIELDS (FROM TO SUBJECT DATE)',
                        struct: true
                    });
                    
                    f.on('message', (msg) => {
                        const emailData = {};
                        
                        msg.on('body', (stream) => {
                            simpleParser(stream).then(parsed => {
                                Object.assign(emailData, {
                                    from: parsed.from?.text,
                                    to: parsed.to?.text,
                                    subject: parsed.subject,
                                    date: parsed.date
                                });
                            });
                        });
                        
                        msg.once('attributes', (attrs) => {
                            emailData.id = attrs.uid;
                            emailData.seen = attrs.flags.includes('\\Seen');
                        });
                        
                        msg.once('end', () => {
                            if (emailData.id) messages.push(emailData);
                            fetched++;
                            if (fetched === fetchIds.length) {
                                resolve({ messages, total: results.length, folder });
                            }
                        });
                    });
                    
                    f.once('error', reject);
                });
            });
        });
    });
}

// 读取邮件
async function readMessage(uid) {
    return withImap(async (imap) => {
        return new Promise((resolve, reject) => {
            imap.openBox('INBOX', false, (err) => {
                if (err) return reject(new Error(`打开收件箱失败：${err.message}`));
                
                const f = imap.fetch([uid], { bodies: '' });
                
                f.on('message', (msg) => {
                    msg.on('body', (stream) => {
                        simpleParser(stream).then(parsed => {
                            resolve({
                                id: uid,
                                from: parsed.from?.text,
                                to: parsed.to?.text,
                                subject: parsed.subject,
                                date: parsed.date,
                                text: parsed.text,
                                html: parsed.html,
                                seen: false
                            });
                        }).catch(reject);
                    });
                });
                
                f.once('error', reject);
            });
        });
    });
}

// 搜索邮件
async function searchMessages(query, limit = 10) {
    return withImap(async (imap) => {
        return new Promise((resolve, reject) => {
            imap.openBox('INBOX', false, (err) => {
                if (err) return reject(new Error(`打开收件箱失败：${err.message}`));
                
                // 简单的关键词搜索
                imap.search([['OR', ['OR', ['SUBJECT', query], ['FROM', query]], ['BODY', query]]], (err, results) => {
                    if (err) return reject(new Error(`搜索失败：${err.message}`));
                    
                    if (results.length === 0) {
                        return resolve({ messages: [], total: 0, query });
                    }
                    
                    const fetchIds = results.slice(0, limit);
                    const messages = [];
                    let fetched = 0;
                    
                    const f = imap.fetch(fetchIds, {
                        bodies: 'HEADER.FIELDS (FROM TO SUBJECT DATE)'
                    });
                    
                    f.on('message', (msg) => {
                        const emailData = {};
                        
                        msg.on('body', (stream) => {
                            simpleParser(stream).then(parsed => {
                                Object.assign(emailData, {
                                    from: parsed.from?.text,
                                    subject: parsed.subject,
                                    date: parsed.date
                                });
                            });
                        });
                        
                        msg.once('attributes', (attrs) => {
                            emailData.id = attrs.uid;
                        });
                        
                        msg.once('end', () => {
                            if (emailData.id) messages.push(emailData);
                            fetched++;
                            if (fetched === fetchIds.length) {
                                resolve({ messages, total: results.length, query });
                            }
                        });
                    });
                    
                    f.once('error', reject);
                });
            });
        });
    });
}

// 发送邮件
async function sendEmail(to, subject, text, html = null) {
    const transporter = getSmtpTransporter();
    const cfg = loadConfig();
    
    try {
        const info = await transporter.sendMail({
            from: `"${cfg.email}" <${cfg.email}>`,
            to: to,
            subject: subject,
            text: text,
            html: html || text
        });
        
        return {
            success: true,
            messageId: info.messageId,
            accepted: info.accepted,
            rejected: info.rejected
        };
    } catch (error) {
        throw new Error(`发送失败：${error.message}`);
    }
}

// 回复邮件
async function replyToMessage(originalUid, replyText) {
    const original = await readMessage(originalUid);
    const cfg = loadConfig();
    
    // 提取原始发件人
    const originalFrom = original.from;
    const originalSubject = original.subject.startsWith('Re:') ? original.subject : `Re: ${original.subject}`;
    
    return sendEmail(originalFrom, originalSubject, replyText);
}

// 转发邮件
async function forwardMessage(originalUid, to, forwardText) {
    const original = await readMessage(originalUid);
    
    const forwardContent = `
---------- 转发邮件 ----------
主题：${original.subject}
发件人：${original.from}
日期：${original.date}

${forwardText}

---------- 原始邮件 ----------
${original.text}
    `.trim();
    
    return sendEmail(to, `Fwd: ${original.subject}`, forwardContent);
}

// 删除邮件
async function deleteMessage(uid) {
    return withImap(async (imap) => {
        return new Promise((resolve, reject) => {
            imap.openBox('INBOX', false, (err) => {
                if (err) return reject(new Error(`打开收件箱失败：${err.message}`));
                
                // 标记为已删除
                imap.addFlags([uid], '\\Deleted', (err) => {
                    if (err) return reject(new Error(`标记删除失败：${err.message}`));
                    
                    // 立即清理
                    imap.expunge((err) => {
                        if (err) return reject(new Error(`清理失败：${err.message}`));
                        resolve({ success: true, uid });
                    });
                });
            });
        });
    });
}

// 导出命令处理函数
module.exports = {
    commands: {
        '163mail inbox': async (args, context) => {
            try {
                const result = await listInbox(10);
                return {
                    content: `📬 收件箱（共 ${result.total} 封邮件）\n\n` +
                        result.messages.map((m, i) => 
                            `${i + 1}. ${m.seen ? '📖' : '📮'} [ID: ${m.id}]\n` +
                            `   发件人：${m.from}\n` +
                            `   主题：${m.subject}\n` +
                            `   日期：${m.date?.toLocaleString('zh-CN')}`
                        ).join('\n\n') || '收件箱为空'
                };
            } catch (error) {
                return { content: `❌ 错误：${error.message}` };
            }
        },
        
        '163mail list': async (args, context) => {
            try {
                const result = await listInbox(10);
                return {
                    content: `📬 收件箱（共 ${result.total} 封邮件）\n\n` +
                        result.messages.map((m, i) => 
                            `${i + 1}. ${m.seen ? '📖' : '📮'} [ID: ${m.id}]\n` +
                            `   发件人：${m.from}\n` +
                            `   主题：${m.subject}\n` +
                            `   日期：${m.date?.toLocaleString('zh-CN')}`
                        ).join('\n\n') || '收件箱为空'
                };
            } catch (error) {
                return { content: `❌ 错误：${error.message}` };
            }
        },
        
        '163mail folder': async (args, context) => {
            const folder = args.trim() || 'INBOX';
            try {
                const result = await listFolder(folder, 10);
                return {
                    content: `📁 ${folder}（共 ${result.total} 封邮件）\n\n` +
                        result.messages.map((m, i) => 
                            `${i + 1}. ${m.seen ? '📖' : '📮'} [ID: ${m.id}]\n` +
                            `   发件人：${m.from}\n` +
                            `   主题：${m.subject}\n` +
                            `   日期：${m.date?.toLocaleString('zh-CN')}`
                        ).join('\n\n') || '文件夹为空'
                };
            } catch (error) {
                return { content: `❌ 错误：${error.message}` };
            }
        },
        
        '163mail read': async (args, context) => {
            const uid = parseInt(args.trim());
            if (!uid) return { content: '❌ 请提供邮件 ID' };
            
            try {
                const email = await readMessage(uid);
                return {
                    content: `📧 邮件详情\n\n` +
                        `发件人：${email.from}\n` +
                        `收件人：${email.to}\n` +
                        `主题：${email.subject}\n` +
                        `日期：${email.date?.toLocaleString('zh-CN')}\n\n` +
                        `----------\n${email.text?.substring(0, 2000) || '(无内容)'}`
                };
            } catch (error) {
                return { content: `❌ 错误：${error.message}` };
            }
        },
        
        '163mail search': async (args, context) => {
            const query = args.trim();
            if (!query) return { content: '❌ 请提供搜索关键词' };
            
            try {
                const result = await searchMessages(query, 10);
                return {
                    content: `🔍 搜索 "${query}"（共 ${result.total} 条结果）\n\n` +
                        result.messages.map((m, i) => 
                            `${i + 1}. [ID: ${m.id}]\n` +
                            `   发件人：${m.from}\n` +
                            `   主题：${m.subject}\n` +
                            `   日期：${m.date?.toLocaleString('zh-CN')}`
                        ).join('\n\n') || '未找到匹配的邮件'
                };
            } catch (error) {
                return { content: `❌ 错误：${error.message}` };
            }
        },
        
        '163mail send': async (args, context) => {
            // 格式：to@example.com 主题 正文
            const parts = args.trim().split(/\s+/);
            if (parts.length < 3) {
                return { content: '❌ 用法：/163mail send <收件人> <主题> <正文>' };
            }
            
            const to = parts[0];
            const subject = parts[1];
            const text = parts.slice(2).join(' ');
            
            try {
                const result = await sendEmail(to, subject, text);
                return {
                    content: `✅ 邮件已发送\n\n` +
                        `收件人：${to}\n` +
                        `主题：${subject}\n` +
                        `消息 ID: ${result.messageId}`
                };
            } catch (error) {
                return { content: `❌ 错误：${error.message}` };
            }
        },
        
        '163mail reply': async (args, context) => {
            const parts = args.trim().split(/\s+/);
            if (parts.length < 2) {
                return { content: '❌ 用法：/163mail reply <邮件 ID> <回复内容>' };
            }
            
            const uid = parseInt(parts[0]);
            const replyText = parts.slice(1).join(' ');
            
            try {
                const result = await replyToMessage(uid, replyText);
                return {
                    content: `✅ 邮件已回复\n\n` +
                        `原邮件 ID: ${uid}\n` +
                        `消息 ID: ${result.messageId}`
                };
            } catch (error) {
                return { content: `❌ 错误：${error.message}` };
            }
        },
        
        '163mail forward': async (args, context) => {
            const parts = args.trim().split(/\s+/);
            if (parts.length < 3) {
                return { content: '❌ 用法：/163mail forward <邮件 ID> <收件人> <转发说明>' };
            }
            
            const uid = parseInt(parts[0]);
            const to = parts[1];
            const forwardText = parts.slice(2).join(' ');
            
            try {
                const result = await forwardMessage(uid, to, forwardText);
                return {
                    content: `✅ 邮件已转发\n\n` +
                        `原邮件 ID: ${uid}\n` +
                        `收件人：${to}\n` +
                        `消息 ID: ${result.messageId}`
                };
            } catch (error) {
                return { content: `❌ 错误：${error.message}` };
            }
        },
        
        '163mail delete': async (args, context) => {
            const uid = parseInt(args.trim());
            if (!uid) return { content: '❌ 请提供邮件 ID' };
            
            try {
                const result = await deleteMessage(uid);
                return { content: `✅ 邮件 ${uid} 已删除` };
            } catch (error) {
                return { content: `❌ 错误：${error.message}` };
            }
        }
    },
    
    // 工具函数导出
    utils: {
        listInbox,
        listFolder,
        readMessage,
        searchMessages,
        sendEmail,
        replyToMessage,
        forwardMessage,
        deleteMessage,
        loadConfig
    }
};
