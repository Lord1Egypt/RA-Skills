module.exports = {
  checkInterval: 30,
  reviewer: '刘欣',
  firstRunAutoApprove: true,
  loginUrl: 'http://ehis-unity-admin-afweb.psic.com.cn/user/login',
  reviewPath: '/task/review',
  
  complianceRules: {
    signature: {
      id: 'signature',
      name: '手写签名',
      required: true,
      type: 'image_detection',
      minConfidence: 0.7
    },
    authorizationNotice: {
      id: 'authorizationNotice',
      name: '授权通知书',
      required: true,
      type: 'document_exist',
      keywords: ['授权', '通知书']
    }
  },
  
  templates: {
    'picc': {
      id: 'picc',
      name: '人保健康',
      templateId: 'TPL_PICC_001',
      logoKeyword: '人保',
      priority: 1
    },
    'pingan': {
      id: 'pingan',
      name: '平安保险',
      templateId: 'TPL_PA_001',
      logoKeyword: '平安',
      priority: 2
    },
    'china_life': {
      id: 'china_life',
      name: '中国人寿',
      templateId: 'TPL_CL_001',
      logoKeyword: '人寿',
      priority: 3
    },
    'taikang': {
      id: 'taikang',
      name: '泰康保险',
      templateId: 'TPL_TK_001',
      logoKeyword: '泰康',
      priority: 4
    }
  },
  
  feishu: {
    enabled: true,
    webhookUrl: process.env.FEISHU_WEBHOOK || '',
    channelId: process.env.FEISHU_CHANNEL_ID || '',
    notifyOnComplete: true,
    notifyOnFailure: true,
    notifyOnFirstRun: true
  },
  
  logging: {
    level: 'info',
    saveAuditLog: true,
    logPath: './memory/compliance-audit.jsonl',
    retentionDays: 90
  }
};
