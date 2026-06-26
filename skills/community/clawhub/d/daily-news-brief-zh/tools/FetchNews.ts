#!/usr/bin/env node

import { readFileSync, existsSync, appendFileSync, mkdirSync } from 'fs';
import { join } from 'path';
import { homedir } from 'os';
import { spawnSync } from 'child_process';
import { NewsFetcher } from './NewsFetcher';
import { NewsClassifier } from './NewsClassifier';
import { MarkdownGenerator } from './MarkdownGenerator';
import type { Config, FetchNewsOptions, CategorizedNews } from './types';

const CONFIG_PATH = join(homedir(), '.daily-news-brief/config.json');
const LOG_DIR = join(homedir(), '.daily-news-brief/logs');

async function loadConfig(): Promise<Config> {
  if (!existsSync(CONFIG_PATH)) {
    throw new Error('配置文件不存在，请先运行 Setup workflow');
  }

  const configContent = readFileSync(CONFIG_PATH, 'utf-8');
  return JSON.parse(configContent);
}

function log(message: string, error?: Error) {
  const timestamp = new Date().toISOString();
  const logMessage = `[${timestamp}] ${message}${error ? `\n${error.stack}` : ''}\n`;

  console.log(logMessage.trim());

  mkdirSync(LOG_DIR, { recursive: true });
  appendFileSync(join(LOG_DIR, 'fetch-news.log'), logMessage);
}

async function fetchNews(options: FetchNewsOptions = {}): Promise<CategorizedNews> {
  log('开始抓取新闻...');

  const config = await loadConfig();

  let fetcher = new NewsFetcher(config.newsSources);

  if (options.category) {
    log(`仅抓取 ${options.category} 类新闻`);
    fetcher = new NewsFetcher(config.newsSources.filter(s => s.category === options.category));
  }

  const allNews = await fetcher.fetchAll();
  log(`共抓取 ${allNews.length} 条新闻`);

  const classifier = new NewsClassifier();
  const classifiedNews = classifier.classifyAll(allNews);
  log('新闻分类完成');

  const categorizedNews = classifier.categorize(classifiedNews);
  log('新闻分组完成');

  const limitedNews = classifier.limitPerCategoryWithSourceCap(
    categorizedNews,
    config.maxNewsPerCategory,
    config.maxPerSourcePerCategory
  );
  log(`每类限制为 ${config.maxNewsPerCategory} 条（单来源上限 ${config.maxPerSourcePerCategory}）`);

  return limitedNews;
}

async function generateAndSave(
  categorizedNews: CategorizedNews,
  config: Config
): Promise<{ filePath?: string; summary: string }> {
  const generator = new MarkdownGenerator();

  const markdown = generator.generate(categorizedNews);
  log('Markdown 文档生成完成');

  let filePath: string | undefined;
  if (config.saveLocalDoc) {
    filePath = await generator.saveLocal(markdown, config.localDocPath);
    log(`本地文档已保存：${filePath}`);
  }

  const summary = generator.generateSummary(categorizedNews, {
    filePath,
    maxPerCategory: config.summaryMaxPerCategory,
    maxPerSource: config.summaryMaxPerSource
  });

  console.log(`\n${summary}`);
  return { filePath, summary };
}

function sendViaOpenClaw(summary: string, config: Config) {
  if (!config.push || !config.push.enabled || config.push.channels.length === 0) {
    return;
  }

  for (const channel of config.push.channels) {
    const args = ['message', 'send', '--channel', channel, '--message', summary];
    const target = config.push.targets?.[channel];
    if (target) {
      args.push('--target', target);
    }

    const result = spawnSync('openclaw', args, { encoding: 'utf-8' });
    if (result.error) {
      log(`OpenClaw 推送失败（${channel}）：${result.error.message}`);
      continue;
    }

    if (result.status !== 0) {
      log(`OpenClaw 推送失败（${channel}）：${result.stderr || result.stdout}`);
    } else {
      log(`OpenClaw 推送成功（${channel}）`);
    }
  }
}

async function main() {
  try {
    const args = process.argv.slice(2);
    const options: FetchNewsOptions = {};

    if (args.includes('--test')) {
      options.test = true;
      log('测试模式：只抓取少量新闻');
    }

    if (args.includes('--date')) {
      const dateIndex = args.indexOf('--date');
      if (dateIndex !== -1 && args[dateIndex + 1]) {
        options.date = args[dateIndex + 1];
      }
    }

    if (args.includes('--category')) {
      const categoryIndex = args.indexOf('--category');
      if (categoryIndex !== -1 && args[categoryIndex + 1]) {
        options.category = args[categoryIndex + 1] as any;
      }
    }

    if (args.includes('--push')) {
      options.push = true;
    }

    if (args.includes('--no-push')) {
      options.push = false;
    }

    const categorizedNews = await fetchNews(options);
    const config = await loadConfig();
    const { summary } = await generateAndSave(categorizedNews, config);

    const shouldPush = options.push ?? config.push?.enabled ?? false;
    if (shouldPush) {
      sendViaOpenClaw(summary, config);
    }

    log('新闻抓取完成！');

    process.exit(0);
  } catch (error) {
    log('新闻抓取失败！', error as Error);
    process.exit(1);
  }
}

if (import.meta.url === `file://${process.argv[1]}`) {
  main();
}

export { fetchNews, loadConfig };
