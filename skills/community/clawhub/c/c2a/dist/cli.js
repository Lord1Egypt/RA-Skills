#!/usr/bin/env node
import { AppStoreClient } from './client.js';
import { searchApps, listInstalledApps, getAppByKey, installAppByKey, uninstallApp, batchInstallApps, batchUninstallByName } from './modules/appstore.js';
const client = AppStoreClient.fromEnv(process.env);
async function main() {
    const args = process.argv.slice(2);
    const command = args[0];
    try {
        switch (command) {
            case 'search': {
                const name = args[1] || '';
                const pageSize = parseInt(args[2]) || 10;
                const apps = await searchApps(client, { name, pageSize });
                console.log('🔍 搜索结果:');
                apps.forEach(app => {
                    console.log(`  - ${app.name} (${app.key})`);
                    console.log(`    ${app.shortDescZh || app.shortDescEn}`);
                    console.log(`    版本: ${app.versions.slice(0, 3).join(', ')}${app.versions.length > 3 ? '...' : ''}`);
                    console.log(`    已安装: ${app.installed ? '是' : '否'}`);
                });
                break;
            }
            case 'list': {
                const apps = await listInstalledApps(client);
                console.log('📦 已安装应用:');
                apps.forEach(app => {
                    console.log(`  - ${app.name} (ID: ${app.id}, 状态: ${app.status})`);
                });
                break;
            }
            case 'info': {
                const key = args[1];
                if (!key) {
                    console.error('用法: info <app-key>');
                    process.exit(1);
                }
                const result = await getAppByKey(client, key);
                if (!result) {
                    console.error(`❌ 未找到应用: ${key}`);
                    process.exit(1);
                }
                const app = result.data;
                console.log(`📦 ${app.name} (${app.key})`);
                console.log(`  描述: ${app.description}`);
                console.log(`  版本: ${app.versions.join(', ')}`);
                console.log(`  已安装: ${app.installed ? '是' : '否'}`);
                break;
            }
            case 'install': {
                const key = args[1];
                if (!key) {
                    console.error('用法: install <app-key> [name] [version]');
                    console.error('示例: install redis my-redis 8.6.2');
                    process.exit(1);
                }
                const name = args[2] || key;
                const version = args[3];
                console.log(`📦 正在安装 ${name}...`);
                const result = await installAppByKey(client, key, { name, version });
                if (result.success) {
                    console.log('✅ 安装成功！');
                    if (result.data) {
                        console.log(`   应用 ID: ${result.data.id}`);
                        console.log(`   应用名: ${result.data.name}`);
                    }
                }
                else {
                    console.log(`❌ 安装失败: ${result.message}`);
                }
                break;
            }
            case 'uninstall': {
                const installId = Number(args[1]);
                if (!installId) {
                    console.error('用法: uninstall <installId>');
                    process.exit(1);
                }
                const result = await uninstallApp(client, installId);
                console.log(result.success ? '✅ 卸载成功' : `❌ 卸载失败: ${result.message}`);
                break;
            }
            case 'batch-install': {
                // 批量安装: batch-install redis mysql nginx
                const keys = args.slice(1);
                if (keys.length === 0) {
                    console.error('用法: batch-install <app-key1> <app-key2> ...');
                    process.exit(1);
                }
                console.log(`📦 批量安装 ${keys.length} 个应用...`);
                const apps = keys.map(key => ({ key }));
                const result = await batchInstallApps(client, apps);
                console.log(`\n总计 ${result.total} 个，成功 ${result.succeeded} 个，失败 ${result.failed} 个`);
                result.results.forEach(r => {
                    console.log(`  ${r.success ? '✅' : '❌'} ${r.item}: ${r.message}`);
                });
                break;
            }
            case 'batch-uninstall': {
                // 批量卸载: batch-uninstall "redis-1" "mysql-2"
                const names = args.slice(1);
                if (names.length === 0) {
                    console.error('用法: batch-uninstall <app-name1> <app-name2> ...');
                    process.exit(1);
                }
                console.log(`🗑️  批量卸载 ${names.length} 个应用...`);
                const result = await batchUninstallByName(client, names);
                console.log(`\n总计 ${result.total} 个，成功 ${result.succeeded} 个，失败 ${result.failed} 个`);
                result.results.forEach(r => {
                    console.log(`  ${r.success ? '✅' : '❌'} ${r.item}: ${r.message}`);
                });
                break;
            }
            default:
                console.log(`
App Store Skill CLI v0.3.0

用法:
  ONEPANEL_BASE_URL=http://... ONEPANEL_API_KEY=... node dist/cli.js <command>

命令:
  search [name] [pageSize]         搜索应用商店
  list                            列出已安装应用
  info <app-key>                  查看应用详情
  install <key> [name] [version]  安装应用
  uninstall <installId>           卸载应用
  batch-install <key1> <key2>...  批量安装应用
  batch-uninstall <name1> <name2>... 按名称批量卸载

示例:
  # 搜索 Redis
  node dist/cli.js search redis

  # 查看应用详情
  node dist/cli.js info redis

  # 安装应用（默认最新版本）
  node dist/cli.js install redis my-redis

  # 安装指定版本
  node dist/cli.js install redis my-redis 7.4.8

  # 批量安装
  node dist/cli.js batch-install redis mysql nginx

  # 批量卸载
  node dist/cli.js batch-uninstall redis-1 mysql-2
        `);
        }
    }
    catch (error) {
        console.error('❌ 错误:', error instanceof Error ? error.message : error);
        process.exit(1);
    }
}
main();
//# sourceMappingURL=cli.js.map