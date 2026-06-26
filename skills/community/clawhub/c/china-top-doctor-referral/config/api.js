const getEnv = () => {
  if (process.env.NODE_ENV === 'development') {
    return 'dev'
  }
  return 'prod'
}

const envMap = {
  dev: {
    domain: 'https://t.ihaola.com.cn',
    csOpenid: process.env.OCEANBUS_CS_OPENID || '请在环境变量 OCEANBUS_CS_OPENID 中设置客服 Agent 的 OpenID'
  },
  prod: {
    domain: 'https://www.ihaola.com.cn',
    csOpenid: process.env.OCEANBUS_CS_OPENID || '请在环境变量 OCEANBUS_CS_OPENID 中设置客服 Agent 的 OpenID'
  }
}

const activeEnv = envMap[getEnv()] || envMap.prod

const config = {
  domain: activeEnv.domain,
  csOpenid: activeEnv.csOpenid,
  baseUrl: activeEnv.baseUrl,
  api: {
    addItems: '/skill/api/recommend/addpack',
  },
  // OceanBus service discovery — bootstrap defaults for new users
  doctorDataOpenid: 'vPk7QuPMR78qSxPpMmxXd_RHj4DzInTLxX6tEEf4TfhUAkEbAF7FQBIvAxuJ_YIHYqEeu5QLRvEUs-pH',
  doctorDataTags: ['doctor-data'],
}

module.exports = config
