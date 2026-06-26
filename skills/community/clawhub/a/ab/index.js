#!/usr/bin/env node

const { program } = require('commander');
const chalk = require('chalk');
const fs = require('fs-extra');
const path = require('path');

// 创建测试目录
const TESTS_DIR = path.join(__dirname, 'tests');
fs.ensureDirSync(TESTS_DIR);

program
  .name('ab')
  .description('A/B testing tool for designing, running, and analyzing A/B tests')
  .version('1.0.0');

// 创建新测试
program
  .command('create')
  .description('Create a new A/B test')
  .option('--name <name>', 'Test name')
  .option('--variants <variants...>', 'Test variants')
  .action((options) => {
    if (!options.name || !options.variants) {
      console.log(chalk.red('Error: Test name and variants are required'));
      return;
    }

    const testData = {
      name: options.name,
      variants: options.variants,
      created: new Date().toISOString(),
      metrics: [],
      results: {}
    };

    const testFile = path.join(TESTS_DIR, `${options.name.replace(/\s+/g, '_')}.json`);
    fs.writeFileSync(testFile, JSON.stringify(testData, null, 2));

    console.log(chalk.green(`Test "${options.name}" created with variants: ${options.variants.join(', ')}`));
  });

// 设置测试指标
program
  .command('metrics')
  .description('Set metrics for a test')
  .option('--test <test>', 'Test name')
  .option('--metrics <metrics...>', 'Metrics to track')
  .action((options) => {
    if (!options.test || !options.metrics) {
      console.log(chalk.red('Error: Test name and metrics are required'));
      return;
    }

    const testFile = path.join(TESTS_DIR, `${options.test.replace(/\s+/g, '_')}.json`);
    if (!fs.existsSync(testFile)) {
      console.log(chalk.red(`Error: Test "${options.test}" not found`));
      return;
    }

    const testData = JSON.parse(fs.readFileSync(testFile, 'utf8'));
    testData.metrics = options.metrics;
    fs.writeFileSync(testFile, JSON.stringify(testData, null, 2));

    console.log(chalk.green(`Metrics set for test "${options.test}": ${options.metrics.join(', ')}`));
  });

// 开始测试
program
  .command('start')
  .description('Start a test')
  .option('--test <test>', 'Test name')
  .action((options) => {
    if (!options.test) {
      console.log(chalk.red('Error: Test name is required'));
      return;
    }

    const testFile = path.join(TESTS_DIR, `${options.test.replace(/\s+/g, '_')}.json`);
    if (!fs.existsSync(testFile)) {
      console.log(chalk.red(`Error: Test "${options.test}" not found`));
      return;
    }

    const testData = JSON.parse(fs.readFileSync(testFile, 'utf8'));
    testData.started = new Date().toISOString();
    fs.writeFileSync(testFile, JSON.stringify(testData, null, 2));

    console.log(chalk.green(`Test "${options.test}" started`));
  });

// 分析测试结果
program
  .command('analyze')
  .description('Analyze test results')
  .option('--test <test>', 'Test name')
  .action((options) => {
    if (!options.test) {
      console.log(chalk.red('Error: Test name is required'));
      return;
    }

    const testFile = path.join(TESTS_DIR, `${options.test.replace(/\s+/g, '_')}.json`);
    if (!fs.existsSync(testFile)) {
      console.log(chalk.red(`Error: Test "${options.test}" not found`));
      return;
    }

    const testData = JSON.parse(fs.readFileSync(testFile, 'utf8'));
    
    console.log(chalk.blue(`=== Test Analysis: ${testData.name} ===`));
    console.log(chalk.yellow(`Created: ${new Date(testData.created).toLocaleString()}`));
    if (testData.started) {
      console.log(chalk.yellow(`Started: ${new Date(testData.started).toLocaleString()}`));
    }
    console.log(chalk.yellow(`Variants: ${testData.variants.join(', ')}`));
    console.log(chalk.yellow(`Metrics: ${testData.metrics.join(', ')}`));
    
    if (Object.keys(testData.results).length > 0) {
      console.log(chalk.green('\nResults:'));
      for (const [variant, data] of Object.entries(testData.results)) {
        console.log(chalk.green(`  ${variant}:`));
        for (const [metric, value] of Object.entries(data)) {
          console.log(chalk.green(`    ${metric}: ${value}`));
        }
      }
    } else {
      console.log(chalk.yellow('\nNo results yet. Start collecting data.'));
    }
  });

// 添加测试数据
program
  .command('add-data')
  .description('Add data to a test')
  .option('--test <test>', 'Test name')
  .option('--variant <variant>', 'Variant name')
  .option('--metric <metric>', 'Metric name')
  .option('--value <value>', 'Metric value', parseFloat)
  .action((options) => {
    if (!options.test || !options.variant || !options.metric || options.value === undefined) {
      console.log(chalk.red('Error: Test name, variant, metric, and value are required'));
      return;
    }

    const testFile = path.join(TESTS_DIR, `${options.test.replace(/\s+/g, '_')}.json`);
    if (!fs.existsSync(testFile)) {
      console.log(chalk.red(`Error: Test "${options.test}" not found`));
      return;
    }

    const testData = JSON.parse(fs.readFileSync(testFile, 'utf8'));
    if (!testData.results[options.variant]) {
      testData.results[options.variant] = {};
    }
    testData.results[options.variant][options.metric] = options.value;
    fs.writeFileSync(testFile, JSON.stringify(testData, null, 2));

    console.log(chalk.green(`Data added: ${options.variant}.${options.metric} = ${options.value}`));
  });

program.parse(process.argv);
