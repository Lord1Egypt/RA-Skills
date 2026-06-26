#!/usr/bin/env node
// Auto-injected by OpenClaw Doctor — do not edit manually
const https = require('https')
const url = require('url')

const SKILL_INFO = {
  "id": 192,
  "platform": "",
  "name": "deployment-workflow",
  "version": "v1.1",
  "installTime": "2026-04-09T13:57:00.764Z"
}

const USER_INFO = {}

const UMAMI_ENDPOINT = "https://umami.thousandrealms.win/api/send"
const WEBSITE_ID = "112cfe05-0cc1-48fb-a92f-65e1d66b81cf"

const eventType = process.argv[2] || 'start'
const errorMsg = process.argv[3] || undefined

const data = {
  skillId: SKILL_INFO.id,
  skillName: SKILL_INFO.name,
  skillVersion: SKILL_INFO.version,
  installTime: SKILL_INFO.installTime,
  eventType: eventType,
  user: USER_INFO,
  platform: '龙虾医生',
}
if (errorMsg) data.errorMessage = errorMsg

const body = JSON.stringify({
  type: 'event',
  payload: {
    website: WEBSITE_ID,
    screen: '1512x982',
    language: 'zh-CN',
    title: '龙虾医生',
    hostname: 'xskillhub.com',
    url: 'https://xskillhub.com/',
    referrer: '',
    name: 'skill_exec_' + eventType,
    data: data,
  },
})

const parsed = new url.URL(UMAMI_ENDPOINT)
const options = {
  hostname: parsed.hostname,
  port: parsed.port ? Number(parsed.port) : 443,
  path: parsed.pathname,
  method: 'POST',
  headers: {
   'content-type': 'application/json',
    'content-length': Buffer.byteLength(body),
    'accept': '*/*',
    'accept-language': 'zh-CN',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) ????/1.2.9 Chrome/132.0.6834.210 Electron/34.5.8 Safari/537.36',
  },
}

const req = https.request(options, (res) => { res.resume() })
req.on('error', () => {})
req.write(body)
req.end()
