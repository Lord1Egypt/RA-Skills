#!/usr/bin/env node

import { existsSync, mkdirSync, readFileSync, writeFileSync, copyFileSync } from 'fs';
import { dirname, join } from 'path';
import { homedir } from 'os';
import type { Config, NewsSource } from './types';

const CONFIG_PATH = join(homedir(), '.daily-news-brief/config.json');

const DEFAULT_CONFIG: Config = {
  newsSources: [
    {
      name: '36氪',
      url: 'https://36kr.com/feed',
      type: 'rss',
      category: '科技'
    },
    {
      name: '虎嗅网',
      url: 'https://www.huxiu.com/rss/0.xml',
      type: 'rss',
      category: '科技'
    },
    {
      name: '财新网',
      url: 'https://www.caixin.com/rss/rss_newstech.xml',
      type: 'rss',
      category: '财经'
    },
    {
      name: '机器之心',
      url: 'https://www.jiqizhixin.com/rss',
      type: 'rss',
      category: 'AI'
    }
  ],
  schedule: '0 21 * * *',
  saveLocalDoc: true,
  localDocPath: '~/daily-news-brief/每日新闻/',
  maxNewsPerCategory: 10,
  summaryMaxPerCategory: 5,
  maxPerSourcePerCategory: 3,
  summaryMaxPerSource: 2,
  push: {
    enabled: false,
    channels: []
  }
};

function loadConfig(): Config {
  if (!existsSync(CONFIG_PATH)) {
    throw new Error('配置文件不存在，请先运行 Setup workflow 或使用 --reset 初始化配置');
  }
  return JSON.parse(readFileSync(CONFIG_PATH, 'utf-8'));
}

function saveConfig(config: Config) {
  const dir = dirname(CONFIG_PATH);
  mkdirSync(dir, { recursive: true });

  if (existsSync(CONFIG_PATH)) {
    copyFileSync(CONFIG_PATH, `${CONFIG_PATH}.backup`);
  }

  writeFileSync(CONFIG_PATH, JSON.stringify(config, null, 2), 'utf-8');
}

function printHelp() {
  console.log(`
Usage: node tools/Configure.ts [options]

Options:
  --schedule "<cron>"                 设置 cron 表达式
  --add-source "name,url,type,cat"    添加或更新新闻源
  --remove-source "<name|url>"        删除新闻源（按名称或 URL）
  --max-news <number>                 设置每类新闻数量上限
  --summary-max <number>              设置摘要每类最多条数
  --max-per-source <number>           设置每类每来源最多条数
  --summary-max-per-source <number>   设置摘要每类每来源最多条数
  --channels "telegram,feishu"        设置推送通道（逗号分隔）
  --push <on|off>                     启用或关闭 OpenClaw 推送
  --reset                             恢复默认配置
  --list                              输出当前配置
  --help                              查看帮助
`);
}

function parseSource(input: string): NewsSource {
  const parts = input.split(',').map(p => p.trim());
  if (parts.length !== 4) {
    throw new Error('参数格式错误，示例："新智元,https://xinzhiyuan.ai/feed,rss,AI"');
  }

  const [name, url, type, category] = parts;
  if (!name || !url) {
    throw new Error('新闻源 name 与 url 不能为空');
  }
  if (type !== 'rss' && type !== 'web') {
    throw new Error('type 只能为 rss 或 web');
  }
  if (!['科技', '财经', 'AI', '智能体'].includes(category)) {
    throw new Error('category 只能为 科技 / 财经 / AI / 智能体');
  }

  return {
    name,
    url,
    type,
    category: category as NewsSource['category']
  };
}

function main() {
  const args = process.argv.slice(2);

  if (args.includes('--help') || args.length === 0) {
    printHelp();
    process.exit(0);
  }

  let config: Config | null = null;

  if (args.includes('--reset')) {
    saveConfig(DEFAULT_CONFIG);
    console.log('✅ 已恢复默认配置');
    process.exit(0);
  }

  try {
    config = loadConfig();
  } catch (error) {
    console.error(`❌ ${(error as Error).message}`);
    process.exit(1);
  }

  if (args.includes('--list')) {
    console.log(JSON.stringify(config, null, 2));
  }

  if (args.includes('--schedule')) {
    const idx = args.indexOf('--schedule');
    if (idx !== -1 && args[idx + 1]) {
      config.schedule = args[idx + 1];
      console.log(`✅ 已更新定时表达式：${config.schedule}`);
    } else {
      console.error('❌ --schedule 需要一个 cron 表达式');
    }
  }

  if (args.includes('--max-news')) {
    const idx = args.indexOf('--max-news');
    if (idx !== -1 && args[idx + 1]) {
      const max = Number(args[idx + 1]);
      if (!Number.isFinite(max) || max <= 0) {
        console.error('❌ --max-news 需要一个正整数');
      } else {
        config.maxNewsPerCategory = Math.floor(max);
        console.log(`✅ 已更新每类数量上限：${config.maxNewsPerCategory}`);
      }
    } else {
      console.error('❌ --max-news 需要一个数字');
    }
  }

  if (args.includes('--summary-max')) {
    const idx = args.indexOf('--summary-max');
    if (idx !== -1 && args[idx + 1]) {
      const max = Number(args[idx + 1]);
      if (!Number.isFinite(max) || max <= 0) {
        console.error('❌ --summary-max 需要一个正整数');
      } else {
        config.summaryMaxPerCategory = Math.floor(max);
        console.log(`✅ 已更新摘要每类数量上限：${config.summaryMaxPerCategory}`);
      }
    } else {
      console.error('❌ --summary-max 需要一个数字');
    }
  }

  if (args.includes('--max-per-source')) {
    const idx = args.indexOf('--max-per-source');
    if (idx !== -1 && args[idx + 1]) {
      const max = Number(args[idx + 1]);
      if (!Number.isFinite(max) || max <= 0) {
        console.error('❌ --max-per-source 需要一个正整数');
      } else {
        config.maxPerSourcePerCategory = Math.floor(max);
        console.log(`✅ 已更新每类每来源上限：${config.maxPerSourcePerCategory}`);
      }
    } else {
      console.error('❌ --max-per-source 需要一个数字');
    }
  }

  if (args.includes('--summary-max-per-source')) {
    const idx = args.indexOf('--summary-max-per-source');
    if (idx !== -1 && args[idx + 1]) {
      const max = Number(args[idx + 1]);
      if (!Number.isFinite(max) || max <= 0) {
        console.error('❌ --summary-max-per-source 需要一个正整数');
      } else {
        config.summaryMaxPerSource = Math.floor(max);
        console.log(`✅ 已更新摘要每类每来源上限：${config.summaryMaxPerSource}`);
      }
    } else {
      console.error('❌ --summary-max-per-source 需要一个数字');
    }
  }

  if (args.includes('--channels')) {
    const idx = args.indexOf('--channels');
    if (idx !== -1 && args[idx + 1]) {
      const channels = args[idx + 1].split(',').map(c => c.trim()).filter(Boolean);
      config.push = config.push || { enabled: false, channels: [] };
      config.push.channels = channels;
      if (channels.length > 0) {
        config.push.enabled = true;
      }
      console.log(`✅ 已更新推送通道：${channels.join(', ') || '无'}`);
    } else {
      console.error('❌ --channels 需要一个通道列表');
    }
  }

  if (args.includes('--push')) {
    const idx = args.indexOf('--push');
    if (idx !== -1 && args[idx + 1]) {
      const flag = args[idx + 1].toLowerCase();
      config.push = config.push || { enabled: false, channels: [] };
      if (flag === 'on') {
        config.push.enabled = true;
      } else if (flag === 'off') {
        config.push.enabled = false;
      } else {
        console.error('❌ --push 只能为 on 或 off');
      }
      console.log(`✅ OpenClaw 推送已${config.push.enabled ? '启用' : '关闭'}`);
    } else {
      console.error('❌ --push 需要 on 或 off');
    }
  }

  if (args.includes('--add-source')) {
    const idx = args.indexOf('--add-source');
    if (idx !== -1 && args[idx + 1]) {
      const source = parseSource(args[idx + 1]);
      const existingIndex = config.newsSources.findIndex(
        s => s.name === source.name || s.url === source.url
      );

      if (existingIndex >= 0) {
        config.newsSources[existingIndex] = source;
        console.log(`✅ 已更新新闻源：${source.name}`);
      } else {
        config.newsSources.push(source);
        console.log(`✅ 已添加新闻源：${source.name}`);
      }
    } else {
      console.error('❌ --add-source 需要一段参数');
    }
  }

  if (args.includes('--remove-source')) {
    const idx = args.indexOf('--remove-source');
    if (idx !== -1 && args[idx + 1]) {
      const key = args[idx + 1];
      const before = config.newsSources.length;
      config.newsSources = config.newsSources.filter(s => s.name !== key && s.url !== key);
      const removed = before - config.newsSources.length;
      console.log(removed > 0 ? `✅ 已删除 ${removed} 个新闻源` : '⚠️ 未找到匹配新闻源');
    } else {
      console.error('❌ --remove-source 需要一个名称或 URL');
    }
  }

  saveConfig(config);
}

if (import.meta.url === `file://${process.argv[1]}`) {
  main();
}
