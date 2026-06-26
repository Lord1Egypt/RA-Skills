#!/usr/bin/env node
"use strict";
/**
 * CLI入口
 * Command Line Interface Entry Point
 */
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const commander_1 = require("commander");
const chalk_1 = __importDefault(require("chalk"));
const skill_1 = require("../skill");
const config_manager_1 = require("../security/config-manager");
const program = new commander_1.Command();
const skill = new skill_1.FeishuBitableSkill();
const configManager = new config_manager_1.ConfigManager();
program
    .name('fbt')
    .description('企业级飞书多维表格智能操作技能')
    .version('1.0.0');
// 配置命令
program
    .command('config')
    .description('配置飞书应用凭证')
    .option('--app-id <id>', '飞书应用ID')
    .option('--app-secret <secret>', '飞书应用密钥')
    .action(async (options) => {
    try {
        if (options.appId && options.appSecret) {
            await configManager.setCredentials(options.appId, options.appSecret);
            console.log(chalk_1.default.green('✓ 配置已保存'));
        }
        else {
            // 交互式配置
            const inquirer = (await Promise.resolve().then(() => __importStar(require('inquirer')))).default;
            const answers = await inquirer.prompt([
                {
                    type: 'input',
                    name: 'appId',
                    message: '请输入飞书应用 ID:',
                    validate: (input) => input.length > 0 || '应用ID不能为空'
                },
                {
                    type: 'password',
                    name: 'appSecret',
                    message: '请输入飞书应用密钥:',
                    validate: (input) => input.length > 0 || '应用密钥不能为空'
                }
            ]);
            await configManager.setCredentials(answers.appId, answers.appSecret);
            console.log(chalk_1.default.green('✓ 配置已保存到系统密钥链'));
        }
    }
    catch (error) {
        console.error(chalk_1.default.red('配置失败:'), error instanceof Error ? error.message : error);
        process.exit(1);
    }
});
// 查询命令 - 自然语言
program
    .command('query <text>')
    .description('使用自然语言查询表格')
    .option('-a, --app <token>', '多维表格App Token')
    .option('-t, --table <id>', '表格ID')
    .action(async (text, options) => {
    try {
        await skill.initialize();
        const result = await skill.executeNaturalLanguage(text, {
            appToken: options.app,
            tableId: options.table
        });
        if (result.success) {
            console.log(chalk_1.default.green('✓ 执行成功'));
            if (result.data) {
                console.log('\n结果:');
                console.log(JSON.stringify(result.data, null, 2));
            }
        }
        else {
            console.error(chalk_1.default.red('✗ 执行失败:'), result.error?.message);
        }
    }
    catch (error) {
        console.error(chalk_1.default.red('错误:'), error instanceof Error ? error.message : error);
        process.exit(1);
    }
});
// 列出表格
program
    .command('tables')
    .description('列出多维表格中的所有表格')
    .requiredOption('-a, --app <token>', '多维表格App Token')
    .action(async (options) => {
    try {
        await skill.initialize();
        const result = await skill.listTables(options.app);
        if (result.success && result.data) {
            console.log(chalk_1.default.green(`\n找到 ${result.data.length} 个表格:\n`));
            console.table(result.data.map(t => ({
                ID: t.table_id,
                名称: t.name,
                字段数: t.fields?.length || 0
            })));
        }
        else {
            console.error(chalk_1.default.red('获取失败:'), result.error?.message);
        }
    }
    catch (error) {
        console.error(chalk_1.default.red('错误:'), error instanceof Error ? error.message : error);
        process.exit(1);
    }
});
// 列出记录
program
    .command('records')
    .description('列出表格中的记录')
    .requiredOption('-a, --app <token>', '多维表格App Token')
    .requiredOption('-t, --table <id>', '表格ID')
    .option('-f, --filter <filter>', '过滤条件（飞书filter表达式）')
    .option('-l, --limit <limit>', '每页数量', '500')
    .action(async (options) => {
    try {
        await skill.initialize();
        const result = await skill.listRecords(options.app, options.table, {
            filter: options.filter,
            pageSize: parseInt(options.limit)
        });
        if (result.success && result.data) {
            console.log(chalk_1.default.green(`\n找到 ${result.data.records.length} 条记录:\n`));
            // 简化显示
            const simplified = result.data.records.map((r) => {
                const fields = Object.entries(r.fields || {})
                    .slice(0, 5)
                    .reduce((acc, [key, value]) => {
                    acc[key] = typeof value === 'object' ? '[对象]' : String(value).slice(0, 50);
                    return acc;
                }, {});
                return { ID: r.record_id, ...fields };
            });
            console.table(simplified);
            if (result.data.hasMore) {
                console.log(chalk_1.default.yellow('\n还有更多记录，使用 --page-token 获取下一页'));
            }
        }
        else {
            console.error(chalk_1.default.red('获取失败:'), result.error?.message);
        }
    }
    catch (error) {
        console.error(chalk_1.default.red('错误:'), error instanceof Error ? error.message : error);
        process.exit(1);
    }
});
// 创建记录
program
    .command('create')
    .description('创建新记录')
    .requiredOption('-a, --app <token>', '多维表格App Token')
    .requiredOption('-t, --table <id>', '表格ID')
    .requiredOption('-d, --data <json>', '记录数据（JSON格式）')
    .action(async (options) => {
    try {
        await skill.initialize();
        const fields = JSON.parse(options.data);
        const result = await skill.createRecord(options.app, options.table, fields);
        if (result.success) {
            console.log(chalk_1.default.green('✓ 记录创建成功'));
            console.log('记录ID:', result.data?.record_id);
        }
        else {
            console.error(chalk_1.default.red('创建失败:'), result.error?.message);
        }
    }
    catch (error) {
        console.error(chalk_1.default.red('错误:'), error instanceof Error ? error.message : error);
        process.exit(1);
    }
});
// 更新记录
program
    .command('update')
    .description('更新记录')
    .requiredOption('-a, --app <token>', '多维表格App Token')
    .requiredOption('-t, --table <id>', '表格ID')
    .requiredOption('-r, --record <id>', '记录ID')
    .requiredOption('-d, --data <json>', '更新数据（JSON格式）')
    .action(async (options) => {
    try {
        await skill.initialize();
        const fields = JSON.parse(options.data);
        const result = await skill.updateRecord(options.app, options.table, options.record, fields);
        if (result.success) {
            console.log(chalk_1.default.green('✓ 记录更新成功'));
        }
        else {
            console.error(chalk_1.default.red('更新失败:'), result.error?.message);
        }
    }
    catch (error) {
        console.error(chalk_1.default.red('错误:'), error instanceof Error ? error.message : error);
        process.exit(1);
    }
});
// 删除记录
program
    .command('delete')
    .description('删除记录')
    .requiredOption('-a, --app <token>', '多维表格App Token')
    .requiredOption('-t, --table <id>', '表格ID')
    .requiredOption('-r, --record <id>', '记录ID')
    .action(async (options) => {
    try {
        const inquirer = (await Promise.resolve().then(() => __importStar(require('inquirer')))).default;
        const { confirm } = await inquirer.prompt([{
                type: 'confirm',
                name: 'confirm',
                message: chalk_1.default.yellow(`确定要删除记录 ${options.record} 吗？此操作不可撤销。`),
                default: false
            }]);
        if (!confirm) {
            console.log(chalk_1.default.gray('操作已取消'));
            return;
        }
        await skill.initialize();
        const result = await skill.deleteRecord(options.app, options.table, options.record);
        if (result.success) {
            console.log(chalk_1.default.green('✓ 记录删除成功'));
        }
        else {
            console.error(chalk_1.default.red('删除失败:'), result.error?.message);
        }
    }
    catch (error) {
        console.error(chalk_1.default.red('错误:'), error instanceof Error ? error.message : error);
        process.exit(1);
    }
});
// 批量导入
program
    .command('import')
    .description('从JSON文件批量导入记录')
    .requiredOption('-a, --app <token>', '多维表格App Token')
    .requiredOption('-t, --table <id>', '表格ID')
    .requiredOption('-f, --file <path>', 'JSON文件路径')
    .action(async (options) => {
    try {
        const fs = await Promise.resolve().then(() => __importStar(require('fs')));
        const data = JSON.parse(fs.readFileSync(options.file, 'utf-8'));
        if (!Array.isArray(data)) {
            throw new Error('文件内容必须是记录数组');
        }
        await skill.initialize();
        const ora = (await Promise.resolve().then(() => __importStar(require('ora')))).default;
        const spinner = ora('正在导入...').start();
        // 分批导入（每批500条）
        const batchSize = 500;
        let successCount = 0;
        let failCount = 0;
        for (let i = 0; i < data.length; i += batchSize) {
            const batch = data.slice(i, i + batchSize);
            const result = await skill.batchCreateRecords(options.app, options.table, batch);
            if (result.success) {
                successCount += batch.length;
            }
            else {
                failCount += batch.length;
            }
            spinner.text = `正在导入... (${successCount + failCount}/${data.length})`;
        }
        spinner.stop();
        console.log(chalk_1.default.green(`✓ 导入完成: 成功 ${successCount} 条, 失败 ${failCount} 条`));
    }
    catch (error) {
        console.error(chalk_1.default.red('导入失败:'), error instanceof Error ? error.message : error);
        process.exit(1);
    }
});
// 导出命令
program
    .command('export')
    .description('导出记录到JSON文件')
    .requiredOption('-a, --app <token>', '多维表格App Token')
    .requiredOption('-t, --table <id>', '表格ID')
    .requiredOption('-f, --file <path>', '输出文件路径')
    .action(async (options) => {
    try {
        await skill.initialize();
        const ora = (await Promise.resolve().then(() => __importStar(require('ora')))).default;
        const spinner = ora('正在导出...').start();
        const allRecords = [];
        let pageToken;
        let hasMore = true;
        while (hasMore) {
            const result = await skill.listRecords(options.app, options.table, { pageToken });
            if (result.success && result.data) {
                allRecords.push(...result.data.records);
                hasMore = result.data.hasMore;
                pageToken = result.data.pageToken;
                spinner.text = `已导出 ${allRecords.length} 条记录...`;
            }
            else {
                throw new Error(result.error?.message || '导出失败');
            }
        }
        const fs = await Promise.resolve().then(() => __importStar(require('fs')));
        fs.writeFileSync(options.file, JSON.stringify(allRecords, null, 2));
        spinner.stop();
        console.log(chalk_1.default.green(`✓ 导出完成: ${allRecords.length} 条记录已保存到 ${options.file}`));
    }
    catch (error) {
        console.error(chalk_1.default.red('导出失败:'), error instanceof Error ? error.message : error);
        process.exit(1);
    }
});
// 交互模式
program
    .command('interactive')
    .alias('i')
    .description('进入交互模式')
    .action(async () => {
    try {
        await skill.initialize();
        console.log(chalk_1.default.cyan('\n🤖 FeishuBitable-Plus 交互模式\n'));
        console.log(chalk_1.default.gray('输入自然语言命令操作表格，或输入 "exit" 退出\n'));
        const inquirer = (await Promise.resolve().then(() => __importStar(require('inquirer')))).default;
        while (true) {
            const { command } = await inquirer.prompt([{
                    type: 'input',
                    name: 'command',
                    message: 'fbt>'
                }]);
            if (command.toLowerCase() === 'exit') {
                console.log(chalk_1.default.gray('再见！'));
                break;
            }
            if (!command.trim())
                continue;
            try {
                const result = await skill.executeNaturalLanguage(command);
                if (result.success) {
                    console.log(chalk_1.default.green('✓ 执行成功'));
                    if (result.data) {
                        console.log(JSON.stringify(result.data, null, 2));
                    }
                }
                else {
                    console.error(chalk_1.default.red('✗'), result.error?.message);
                }
            }
            catch (error) {
                console.error(chalk_1.default.red('错误:'), error instanceof Error ? error.message : error);
            }
            console.log(); // 空行分隔
        }
    }
    catch (error) {
        console.error(chalk_1.default.red('错误:'), error instanceof Error ? error.message : error);
        process.exit(1);
    }
});
// 默认显示帮助
if (process.argv.length === 2) {
    program.help();
}
program.parse();
//# sourceMappingURL=index.js.map