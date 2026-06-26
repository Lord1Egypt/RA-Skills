#!/usr/bin/env node
/**
 * CLI 增强工具 v6.1-Phase6.1.4
 * 
 * 核心功能:
 * 1. 输出美化 (表格/颜色/进度条/图标)
 * 2. 快捷命令 (别名/宏/管道/批处理)
 * 3. 交互式命令 (菜单/输入/向导)
 * 4. 自动补全 (命令/参数/路径)
 */

// ============ 颜色输出 ============

const colors = {
  reset: '\x1b[0m',
  bright: '\x1b[1m',
  dim: '\x1b[2m',
  underscore: '\x1b[4m',
  blink: '\x1b[5m',
  reverse: '\x1b[7m',
  hidden: '\x1b[8m',
  
  black: '\x1b[30m',
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  magenta: '\x1b[35m',
  cyan: '\x1b[36m',
  white: '\x1b[37m',
  
  bgBlack: '\x1b[40m',
  bgRed: '\x1b[41m',
  bgGreen: '\x1b[42m',
  bgYellow: '\x1b[43m',
  bgBlue: '\x1b[44m',
  bgMagenta: '\x1b[45m',
  bgCyan: '\x1b[46m',
  bgWhite: '\x1b[47m'
};

class ColorOutput {
  static colorize(text, color) {
    return `${colors[color]}${text}${colors.reset}`;
  }

  static success(text) {
    return this.colorize(text, 'green');
  }

  static error(text) {
    return this.colorize(text, 'red');
  }

  static warning(text) {
    return this.colorize(text, 'yellow');
  }

  static info(text) {
    return this.colorize(text, 'blue');
  }

  static highlight(text) {
    return this.colorize(text, 'cyan');
  }

  static bold(text) {
    return this.colorize(text, 'bright');
  }
}

// ============ 表格输出 ============

class Table {
  constructor(options = {}) {
    this.headers = options.headers || [];
    this.rows = [];
    this.options = {
      border: options.border !== false,
      padding: options.padding !== undefined ? options.padding : 1
    };
  }

  push(row) {
    this.rows.push(row);
  }

  toString() {
    if (this.headers.length === 0 && this.rows.length === 0) {
      return '';
    }

    // 计算每列最大宽度
    const columnWidths = this.calculateColumnWidths();

    // 生成表格
    let output = '';

    if (this.options.border) {
      // 顶部分隔线
      output += this.createSeparator(columnWidths, '┌', '┬', '┐') + '\n';
      
      // 表头
      if (this.headers.length > 0) {
        output += this.createRow(this.headers, columnWidths, '│') + '\n';
        output += this.createSeparator(columnWidths, '├', '┼', '┤') + '\n';
      }
      
      // 数据行
      for (let i = 0; i < this.rows.length; i++) {
        output += this.createRow(this.rows[i], columnWidths, '│') + '\n';
        if (i < this.rows.length - 1) {
          output += this.createSeparator(columnWidths, '├', '┼', '┤') + '\n';
        }
      }
      
      // 底部分隔线
      output += this.createSeparator(columnWidths, '└', '┴', '┘');
    } else {
      // 无框表格
      if (this.headers.length > 0) {
        output += this.createRow(this.headers, columnWidths, ' ', false) + '\n';
      }
      for (const row of this.rows) {
        output += this.createRow(row, columnWidths, ' ', false) + '\n';
      }
    }

    return output;
  }

  calculateColumnWidths() {
    const allRows = this.headers.length > 0 ? [this.headers, ...this.rows] : this.rows;
    const columnCount = Math.max(...allRows.map(r => r.length));
    const widths = new Array(columnCount).fill(0);

    for (const row of allRows) {
      for (let i = 0; i < columnCount; i++) {
        const cell = row[i] !== undefined ? String(row[i]) : '';
        // 移除颜色代码计算实际长度
        const cleanCell = cell.replace(/\x1b\[[0-9;]*m/g, '');
        widths[i] = Math.max(widths[i], cleanCell.length);
      }
    }

    return widths;
  }

  createSeparator(widths, left, middle, right) {
    return left + widths.map(w => '─'.repeat(w + this.options.padding * 2)).join(middle) + right;
  }

  createRow(cells, widths, border, padding = true) {
    const paddedCells = cells.map((cell, i) => {
      const cleanCell = String(cell).replace(/\x1b\[[0-9;]*m/g, '');
      const paddingStr = ' '.repeat(widths[i] - cleanCell.length);
      const padded = padding ? ' '.repeat(this.options.padding) : '';
      return `${padded}${cell}${paddingStr}${padded}`;
    });
    return border + paddedCells.join(border) + border;
  }
}

// ============ 进度条 ============

class ProgressBar {
  constructor(options = {}) {
    this.total = options.total || 100;
    this.current = 0;
    this.width = options.width || 30;
    this.showPercentage = options.showPercentage !== false;
    this.showEta = options.showEta || false;
    this.startTime = Date.now();
  }

  update(current, options = {}) {
    this.current = current;
    this.total = options.total || this.total;
    this.render(options);
  }

  increment(amount = 1, options = {}) {
    this.current += amount;
    this.update(this.current, options);
  }

  render(options = {}) {
    const percentage = this.current / this.total;
    const filledWidth = Math.round(this.width * percentage);
    const emptyWidth = this.width - filledWidth;

    const filled = '█'.repeat(filledWidth);
    const empty = '░'.repeat(emptyWidth);

    let output = `\r${ColorOutput.blue('[')}${filled}${empty}${ColorOutput.blue(']')}`;

    if (this.showPercentage) {
      const percentStr = (percentage * 100).toFixed(1) + '%';
      output += ` ${ColorOutput.bold(percentStr)}`;
    }

    if (this.showEta && this.current > 0) {
      const elapsed = Date.now() - this.startTime;
      const eta = Math.round((elapsed / this.current) * (this.total - this.current));
      output += ` ${ColorOutput.dim(`ETA: ${this.formatTime(eta)}`)}`;
    }

    if (options.suffix) {
      output += ` ${options.suffix}`;
    }

    process.stdout.write(output);
  }

  complete(options = {}) {
    this.update(this.total, options);
    console.log(); // 换行
  }

  formatTime(ms) {
    if (ms < 1000) return `${ms}ms`;
    if (ms < 60000) return `${(ms / 1000).toFixed(1)}s`;
    return `${Math.round(ms / 60000)}m${Math.round((ms % 60000) / 1000)}s`;
  }
}

// ============ 图标库 ============

const icons = {
  // 状态
  success: '✅',
  error: '❌',
  warning: '⚠️',
  info: 'ℹ️',
  pending: '⏳',
  running: '🚀',
  completed: '✓',
  failed: '✗',
  
  // 类型
  file: '📄',
  folder: '📁',
  config: '⚙️',
  test: '🧪',
  report: '📊',
  code: '💻',
  doc: '📚',
  
  // 操作
  add: '➕',
  remove: '➖',
  update: '🔄',
  delete: '🗑️',
  download: '⬇️',
  upload: '⬆️',
  search: '🔍',
  settings: '🔧',
  
  // 箭头
  right: '→',
  left: '←',
  up: '↑',
  down: '↓',
  enter: '↵'
};

class IconOutput {
  static get(name) {
    return icons[name] || '';
  }

  static withIcon(name, text, space = true) {
    const icon = this.get(name);
    return icon ? `${icon}${space ? ' ' : ''}${text}` : text;
  }

  static status(status, text) {
    const iconMap = {
      success: 'success',
      error: 'error',
      warning: 'warning',
      info: 'info',
      pending: 'pending',
      running: 'running'
    };
    return this.withIcon(iconMap[status] || 'info', text);
  }
}

// ============ 命令别名系统 ============

class CommandAlias {
  constructor() {
    this.aliases = new Map();
    this.macros = new Map();
  }

  add(alias, command) {
    this.aliases.set(alias, command);
  }

  addMacro(name, commands) {
    this.macros.set(name, commands);
  }

  resolve(input) {
    const parts = input.split(' ');
    const cmd = parts[0];
    const args = parts.slice(1);

    // 检查宏
    if (this.macros.has(cmd)) {
      return {
        type: 'macro',
        commands: this.macros.get(cmd),
        args
      };
    }

    // 检查别名
    if (this.aliases.has(cmd)) {
      return {
        type: 'alias',
        command: this.aliases.get(cmd),
        args
      };
    }

    return {
      type: 'command',
      command: cmd,
      args
    };
  }

  list() {
    return {
      aliases: Object.fromEntries(this.aliases),
      macros: Object.fromEntries(this.macros)
    };
  }
}

// ============ 交互式菜单 ============

class InteractiveMenu {
  constructor(options = {}) {
    this.items = options.items || [];
    this.title = options.title || '请选择';
    this.selected = 0;
  }

  async select() {
    console.log(ColorOutput.bold(this.title));
    console.log();

    this.items.forEach((item, index) => {
      const marker = index === this.selected ? '❯' : ' ';
      const color = index === this.selected ? ColorOutput.cyan : ColorOutput.dim;
      console.log(color(` ${marker} ${item.label || item}`));
    });

    console.log();
    console.log(ColorOutput.dim('  使用 ↑↓ 选择，Enter 确认'));

    // 简化版本：直接输入数字选择
    const readline = require('readline').createInterface({
      input: process.stdin,
      output: process.stdout
    });

    return new Promise(resolve => {
      readline.question(ColorOutput.info('  选择 (0-' + (this.items.length - 1) + '): '), answer => {
        const index = parseInt(answer);
        if (index >= 0 && index < this.items.length) {
          resolve(this.items[index]);
        } else {
          resolve(null);
        }
        readline.close();
      });
    });
  }
}

// ============ 输入提示 ============

class InputPrompt {
  static async text(question, options = {}) {
    const readline = require('readline').createInterface({
      input: process.stdin,
      output: process.stdout
    });

    const defaultValue = options.default ? ` [${options.default}]` : '';
    
    return new Promise(resolve => {
      readline.question(ColorOutput.info(`? ${question}${defaultValue}: `), answer => {
        resolve(answer || options.default || '');
        readline.close();
      });
    });
  }

  static async confirm(question, options = {}) {
    const readline = require('readline').createInterface({
      input: process.stdin,
      output: process.stdout
    });

    const defaultValue = options.default !== undefined ? options.default : true;
    const defaultStr = defaultValue ? 'Y/n' : 'y/N';
    
    return new Promise(resolve => {
      readline.question(ColorOutput.info(`? ${question} (${defaultStr}): `), answer => {
        if (answer === '') {
          resolve(defaultValue);
        } else {
          resolve(['y', 'yes', 'true', '1'].includes(answer.toLowerCase()));
        }
        readline.close();
      });
    });
  }

  static async password(question) {
    const readline = require('readline').createInterface({
      input: process.stdin,
      output: process.stdout
    });

    // 隐藏输入
    readline.question(question + ': ', {
      hideEchoBack: true
    }, answer => {
      readline.close();
      return answer;
    });
  }
}

// ============ CLI 增强主类 ============

class CLIEnhanced {
  constructor() {
    this.alias = new CommandAlias();
    this.setupDefaultAliases();
  }

  setupDefaultAliases() {
    // 常用别名
    this.alias.add('ls', 'list');
    this.alias.add('ll', 'list --long');
    this.alias.add('rm', 'remove');
    this.alias.add('mv', 'move');
    this.alias.add('cp', 'copy');
    this.alias.add('cat', 'show');
    this.alias.add('help', '--help');
    this.alias.add('h', '--help');
    this.alias.add('v', '--version');

    // 宏命令
    this.alias.addMacro('status', [
      'agent-manager.js status',
      'config-manager.js get'
    ]);

    this.alias.addMacro('test', [
      'integration-test.js',
      'test-framework.js test'
    ]);
  }

  createTable(headers, rows, options = {}) {
    const table = new Table({ headers, ...options });
    rows.forEach(row => table.push(row));
    return table;
  }

  createProgress(options = {}) {
    return new ProgressBar(options);
  }

  createMenu(items, options = {}) {
    return new InteractiveMenu({ items, ...options });
  }

  color(text, color) {
    return ColorOutput.colorize(text, color);
  }

  success(text) {
    return IconOutput.status('success', text);
  }

  error(text) {
    return IconOutput.status('error', text);
  }

  warning(text) {
    return IconOutput.status('warning', text);
  }

  info(text) {
    return IconOutput.status('info', text);
  }

  icon(name, text) {
    return IconOutput.withIcon(name, text);
  }

  async prompt(question, options = {}) {
    return InputPrompt.text(question, options);
  }

  async confirm(question, options = {}) {
    return InputPrompt.confirm(question, options);
  }

  resolveCommand(input) {
    return this.alias.resolve(input);
  }

  printBanner(title, subtitle = '') {
    const width = Math.max(title.length, subtitle.length) + 4;
    const border = '═'.repeat(width);
    
    console.log();
    console.log(ColorOutput.cyan(border));
    console.log(ColorOutput.cyan('  ') + ColorOutput.bold(title));
    if (subtitle) {
      console.log(ColorOutput.dim('  ' + subtitle));
    }
    console.log(ColorOutput.cyan(border));
    console.log();
  }
}

// ============ CLI 接口 ============

function printHelp() {
  console.log(`
CLI 增强工具 v6.1

用法：node cli-enhanced.js <命令> [选项]

命令:
  demo                演示所有功能
  table               表格输出演示
  progress            进度条演示
  colors              颜色输出演示
  icons               图标输出演示
  menu                菜单演示
  prompt              输入提示演示

示例:
  node cli-enhanced.js demo
  node cli-enhanced.js table
  node cli-enhanced.js progress
`);
}

// ============ 主程序 ============

async function main() {
  const args = process.argv.slice(2);
  const command = args[0];

  if (!command || command === '--help' || command === '-h') {
    printHelp();
    return;
  }

  const cli = new CLIEnhanced();

  switch (command) {
    case 'demo':
      console.clear();
      cli.printBanner('🚀 CLI 增强工具演示', 'v6.1-Phase6.1.4');

      // 颜色演示
      console.log(ColorOutput.bold('📝 颜色输出:'));
      console.log(cli.success('✅ 成功消息'));
      console.log(cli.error('❌ 错误消息'));
      console.log(cli.warning('⚠️  警告消息'));
      console.log(cli.info('ℹ️  信息消息'));
      console.log();

      // 表格演示
      console.log(ColorOutput.bold('📊 表格输出:'));
      const table = cli.createTable(
        ['模块', '大小', '状态', '评分'],
        [
          ['缓存管理', '11KB', cli.success('完成'), '88 分'],
          ['并发执行', '14KB', cli.success('完成'), '88 分'],
          ['测试框架', '19KB', cli.success('完成'), '89 分'],
          ['CLI 增强', '12KB', cli.warning('进行中'), '待评分']
        ]
      );
      console.log(table.toString());
      console.log();

      // 图标演示
      console.log(ColorOutput.bold('🎨 图标输出:'));
      console.log(cli.icon('success', '成功'));
      console.log(cli.icon('error', '失败'));
      console.log(cli.icon('warning', '警告'));
      console.log(cli.icon('info', '信息'));
      console.log(cli.icon('running', '运行中'));
      console.log();

      // 进度条演示
      console.log(ColorOutput.bold('📈 进度条:'));
      const progress = cli.createProgress({ total: 20, width: 30 });
      for (let i = 0; i <= 20; i++) {
        progress.update(i);
        await new Promise(resolve => setTimeout(resolve, 100));
      }
      progress.complete();
      console.log();

      // 命令别名演示
      console.log(ColorOutput.bold('🔧 命令别名:'));
      const aliases = cli.alias.list();
      console.log('别名:', Object.keys(aliases.aliases).join(', '));
      console.log('宏:', Object.keys(aliases.macros).join(', '));
      console.log();

      console.log(cli.success('演示完成！'));
      break;

    case 'table':
      const demoTable = cli.createTable(
        [cli.bold('名称'), cli.bold('类型'), cli.bold('大小'), cli.bold('状态')],
        [
          ['cache-manager.js', '缓存', '11KB', cli.success('✅ 完成')],
          ['concurrent-executor.js', '并发', '14KB', cli.success('✅ 完成')],
          ['test-framework.js', '测试', '19KB', cli.success('✅ 完成')],
          ['cli-enhanced.js', 'CLI', '12KB', cli.warning('⏳ 进行中')]
        ],
        { border: true }
      );
      console.log(demoTable.toString());
      break;

    case 'progress':
      const demoProgress = cli.createProgress({ 
        total: 50, 
        width: 40,
        showPercentage: true,
        showEta: true
      });
      
      for (let i = 0; i <= 50; i++) {
        demoProgress.update(i, { suffix: `处理 ${i}/50` });
        await new Promise(resolve => setTimeout(resolve, 50));
      }
      demoProgress.complete({ suffix: '完成！' });
      break;

    case 'colors':
      console.log('颜色输出演示:\n');
      
      const colorNames = Object.keys(colors).filter(c => !c.startsWith('bg'));
      colorNames.forEach(color => {
        console.log(ColorOutput.colorize(color, color));
      });
      break;

    case 'icons':
      console.log('图标输出演示:\n');
      
      const iconCategories = {
        '状态': ['success', 'error', 'warning', 'info', 'pending', 'running'],
        '类型': ['file', 'folder', 'config', 'test', 'report', 'code'],
        '操作': ['add', 'remove', 'update', 'delete', 'search', 'settings']
      };

      for (const [category, iconNames] of Object.entries(iconCategories)) {
        console.log(ColorOutput.bold(category + ':'));
        iconNames.forEach(name => {
          console.log(`  ${IconOutput.withIcon(name, name)}`);
        });
        console.log();
      }
      break;

    case 'menu':
      const menu = cli.createMenu([
        { label: '查看状态', value: 'status' },
        { label: '运行测试', value: 'test' },
        { label: '生成报告', value: 'report' },
        { label: '退出', value: 'exit' }
      ], { title: '📋 主菜单' });

      const selected = await menu.select();
      if (selected) {
        console.log(cli.success(`已选择：${selected.label}`));
      }
      break;

    case 'prompt':
      console.log('输入提示演示:\n');
      
      const name = await cli.prompt('请输入您的名字', { default: '用户' });
      console.log(cli.success(`你好，${name}！`));
      
      const confirm = await cli.confirm('继续操作吗？');
      if (confirm) {
        console.log(cli.info('继续中...'));
      } else {
        console.log(cli.warning('已取消'));
      }
      break;

    default:
      console.log(`未知命令：${command}`);
      printHelp();
  }
}

// 导出 API
module.exports = {
  CLIEnhanced,
  Table,
  ProgressBar,
  ColorOutput,
  IconOutput,
  InputPrompt,
  InteractiveMenu,
  CommandAlias,
  colors,
  icons
};

// 运行 CLI
if (require.main === module) {
  main().catch(console.error);
}
