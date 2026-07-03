#!/usr/bin/env node
/**
 * 首次配置：指定要同步到哪张飞书多维表格。
 *
 * 两种后端:
 *   A) 授权码(可分发, 推荐): node setup.mjs <base链接> --token <pt-授权码>
 *      授权码在多维表格「更多→高级权限/扩展→获取授权码」生成; 只认 base 链接(个人端)。
 *   B) lark-cli(本机自用): node setup.mjs <飞书链接>   # 用你已登录的 lark-cli, 无需授权码
 *
 * 其它:
 *   node setup.mjs <链接> --table tblXXX   # 显式指定人才表
 *   node setup.mjs --show                  # 查看当前配置
 */
import { configureTarget, loadTarget, listTables, TARGET_FILE } from '../lib/target.mjs';

const argv = process.argv.slice(2);
const val = (f) => { const i = argv.indexOf(f); return i >= 0 ? argv[i + 1] : null; };

if (argv.includes('--show')) {
  const t = loadTarget();
  if (!t) { console.log('❌ 尚未配置。运行: node setup.mjs <飞书表链接> [--token <授权码>]'); process.exit(1); }
  console.log('当前目标表配置:');
  console.log(`  后端: ${t.backend}${t.personal_base_token ? ' (授权码 ' + t.personal_base_token.slice(0, 8) + '…)' : ''}`);
  console.log(`  表: ${t.talentTableName || t.talentTable} (${t.talentTable})`);
  console.log(`  Base: ${t.baseToken}`);
  console.log(`  附件字段: ${t.attachmentField || '(无)'}`);
  console.log(`  可写字段 ${t.fields.length} 个`);
  console.log(`  配置文件: ${TARGET_FILE}`);
  process.exit(0);
}

const token = val('--token');
const link = argv.find((a) => !a.startsWith('--') && a !== val('--table') && a !== token);
if (!link) {
  console.log('用法:\n  授权码模式: node setup.mjs <**/base/**链接> --token <pt-授权码>\n  lark-cli模式: node setup.mjs <飞书链接>');
  process.exit(1);
}

const res = await configureTarget(link, { tableId: val('--table'), token });

if (!res.ok) {
  const hints = {
    wiki_not_supported: '授权码不支持 /wiki/(企业端)链接，请用 /base/(个人端)链接。',
    need_base_link: '授权码模式必须给 /base/ 链接。',
    need_table_in_url: '请在链接里带上 ?table=tblXXX，或加 --table tblXXX。',
    ambiguous_table: null,
  };
  if (res.reason === 'ambiguous_table') {
    console.log(`\n⚠️ 这个 Base 里有多张表，无法自动判断哪张是人才表：${res.title || ''}`);
    for (const t of res.tables) console.log(`   ${t.id}  ${t.name}`);
    console.log(`\n请重跑并指定: node setup.mjs <链接> --table <上面的 tblXXX>`);
  } else {
    console.log(`❌ 配置失败: ${hints[res.reason] || res.reason}`);
  }
  process.exit(1);
}

const t = res.target;
console.log(`\n✅ 已配置目标表  [后端: ${res.backend}]`);
console.log(`  表: ${t.talentTableName || t.talentTable} (${t.talentTable})`);
console.log(`  Base: ${t.baseToken}${t.title ? '  «' + t.title + '»' : ''}`);
console.log(`  附件字段: ${t.attachmentField || '⚠️ 未发现附件字段，附件简历将无法同步'}`);
console.log(`  识别到 ${t.fields.length} 个字段`);
if (res.missing?.length) {
  console.log(`\n⚠️ 缺少建议字段(不影响运行，仅这些列不会被写入): ${res.missing.join('、')}`);
}
console.log(`\n配置已存到 ${TARGET_FILE}。现在可以跑场景1了。`);
