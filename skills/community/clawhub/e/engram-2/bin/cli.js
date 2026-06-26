#!/usr/bin/env node

const { pipeline, env } = require('@xenova/transformers');
const fs = require('fs');
const path = require('path');
const ora = require('ora');
const chalk = require('chalk');
const CapsuleStore = require('../src/storage/capsule-store'); 

// 配置 transformer：关闭远程模型发送，设置本地存储目录
env.allowLocalModels = false; 
env.cacheDir = path.join(require('os').homedir(), '.engram_cache');

const seedsPath = path.join(__dirname, '../data/seeds/seeds.json');

const cliArgs = process.argv.slice(2);
const command = cliArgs[0] || 'help';

async function preheat() {
    console.log(chalk.bold.cyan('\n🧬 engram - The AI Agent Memory Hub\n'));

    // 1. 初始化并下载 22MB 的向量模型
    const spinner = ora('Initializing AI Embedding Model (Fetching all-MiniLM-L6-v2, ~22MB)...').start();
    try {
        await pipeline('feature-extraction', 'Xenova/all-MiniLM-L6-v2', {
            progress_callback: (x) => {
                if(x.status === 'downloading') {
                    spinner.text = `Downloading ${x.file}: ${Math.round(x.progress)}%...`;
                }
            }
        });
        spinner.succeed(chalk.green('Local semantic engine primed. Ready offline.'));
    } catch (err) {
        spinner.fail(chalk.red('Failed to load NLP model. Please check network connections.'));
        console.error(err);
        process.exit(1);
    }

    // 2. 注入体验种子包 (Seeds Injection)
    if (!fs.existsSync(seedsPath)) {
        console.log(chalk.yellow('\n⚠️ No seeds.json found. Skipping seed injection.'));
        return;
    }

    const seeds = JSON.parse(fs.readFileSync(seedsPath, 'utf8'));
    const seedSpinner = ora('Injecting ' + seeds.length + ' High-Value Dev Capsules...').start();
    const store = new CapsuleStore();
    try {
        let newCount = 0;
        for (const seed of seeds) {
             store.save(seed);
             newCount++;
        }
        seedSpinner.succeed(chalk.green(`Injected ${newCount} Master Capsules. Neural link synced.`));
        
        console.log(`\n🎉 Installation Complete! `);
        console.log(`Type ` + chalk.magenta('!exp list') + ` via Agent CLI to see your acquired skills.\n`);

    } catch(err) {
        seedSpinner.fail('Seed capsule validation or injection failed!');
        console.error(err);
    }
}

if (command === 'init' || command === 'preheat') {
    preheat();
} else {
    console.log(chalk.yellow(`Usage: npx engram init`));
}
