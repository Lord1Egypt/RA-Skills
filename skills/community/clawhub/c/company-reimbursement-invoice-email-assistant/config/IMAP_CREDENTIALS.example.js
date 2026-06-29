module.exports = {
  defaultProfile: 'qq-main',
  profiles: {
    'qq-main': {
      user: 'your@qq.com',
      password: 'your_email_app_password',
      host: 'imap.qq.com',
      port: 993,
      tls: true,
      rejectUnauthorized: false,
      mailbox: 'INBOX',
      mailWebUser: 'your_qq_number',
    },
  },
};
