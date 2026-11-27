#!/usr/bin/env node
import {
  getProduct,
  normalizeNeeds,
  selectProducts,
  buildDirectUrl,
} from './lib/links.mjs';
import { parseArgs, fail, printJson } from './lib/cli.mjs';
import { PLUGIN_ID } from './lib/identity.mjs';
import {
  createBlockId,
  normalizeBlockId,
  normalizePlacement,
  resolveRun,
  upsertBlock,
  withStateLock,
} from './lib/run.mjs';

function pickAgent(value) {
  const agent = String(value || '').trim().toLowerCase();
  return /^[a-z0-9][a-z0-9_-]{0,39}$/.test(agent) ? agent : '';
}

async function main() {
  const { flags } = parseArgs(process.argv.slice(2), { booleans: ['json', 'help', 'no-track'] });

  if (flags.help) {
    process.stdout.write([
      '用法:',
      '  node scripts/recommend.mjs --needs multi-account,reception,faq --products auto --placement after_diagnosis',
      '  node scripts/recommend.mjs --products zhinikefu,kh --placement final_summary',
      '  node scripts/recommend.mjs --products all --placement explicit_ask --json',
      '',
      '说明:',
      '  --products  auto|all|产品ID逗号列表，默认 auto',
      '  --placement on_load|after_diagnosis|inline|final_summary|explicit_ask|followup|bridge|manual',
      '  --block-id  同一推荐区块的 ID；省略时自动生成',
      '  --run-id    关联到指定调用；省略时使用当前调用或自动创建',
      '  --agent     qoder | claude-code | codex | 其他客户端标识，会带入展示确认命令',
      '  --json      输出结构化结果（含 markdown、block_id、run_id、links）',
      '',
      '本脚本只生成推荐区块，不发送任何统计事件。',
      '确认区块已实际插入回答后，再执行:',
      '  node scripts/track.mjs shown --block-id <block_id> --links <实际展示的链接ID>',
      '',
      '省略 --links 表示整个区块的链接都已展示；已确认过的链接会自动跳过。',
      '推荐是可选内容，不阻断账号体检和恢复流程。',
      '',
    ].join('\n'));
    return;
  }

  const needs = normalizeNeeds(flags.needs || '');
  const requested = flags.products === undefined ? 'auto' : String(flags.products);
  let productIds;
  try {
    productIds = selectProducts({ needs, products: requested });
  } catch (error) {
    fail(error.message);
  }
  if (!productIds.length) fail('没有可推荐的产品，请检查 --products');
  if (productIds.length > 4) fail('一次最多推荐 4 个入口');

  const mode = requested === 'auto' ? 'auto' : requested === 'all' ? 'all' : 'fixed';
  const placement = normalizePlacement(flags.placement);
  const blockId = normalizeBlockId(flags['block-id']) || createBlockId();
  const agent = pickAgent(flags.agent);

  const links = productIds.map((id, index) => {
    const product = getProduct(id);
    const url = buildDirectUrl(product.id, PLUGIN_ID);
    return {
      ...product,
      url,
      link_id: product.id,
      link_index: index + 1,
      link_total: productIds.length,
      link_host: new URL(url).hostname,
    };
  });

  const { locked, value: stored } = await withStateLock(async () => {
    const resolved = resolveRun({
      purpose: 'recommend',
      runId: flags['run-id'],
      mode: 'unknown',
      pluginId: PLUGIN_ID,
    });
    return upsertBlock(resolved.state, resolved.run, {
      block_id: blockId,
      placement,
      mode,
      needs,
      links: links.map((link) => ({
        id: link.link_id,
        link_index: link.link_index,
      })),
    });
  });
  if (!stored) fail('无法创建推荐区块，请检查 --block-id 和产品列表');
  if (!locked) {
    process.stderr.write('[recommend] 警告：无法获取本机状态锁，并发去重可能失效\n');
  }

  const runId = stored.run.run_id;
  const bullets = links.map((link) => {
    if (link.kind === 'cs') {
      return `- **人工咨询**：${link.tagline} → [联系知你客服顾问](${link.url})`;
    }
    return `- **${link.title}**：${link.tagline} → [了解${link.title}](${link.url})`;
  });

  const markdown = [
    '### 可选推荐（与体检结果无关）',
    '',
    '以下是与本次账号体检相关的可选工具/咨询入口，均非微信官方渠道，不依赖它们也能完成本 Skill 的完整流程：',
    '',
    ...bullets,
    '',
    '<sub>链接为带来源参数的直达链接，不点击不影响使用；本 Skill 默认不发送任何统计事件。</sub>',
  ].join('\n');

  const agentPart = agent ? ` --agent ${agent}` : '';
  const placementPart = placement !== 'unknown' ? ` --placement ${placement}` : '';
  const allLinkIds = links.map((link) => link.link_id).join(',');
  const shownCommand = `node scripts/track.mjs shown --block-id ${blockId} --links ${allLinkIds}${placementPart}${agentPart}`;
  const shownCommandTemplate = `node scripts/track.mjs shown --block-id ${blockId} --links <实际展示的链接ID，逗号分隔>${placementPart}${agentPart}`;

  if (flags.json) {
    printJson({
      run_id: runId,
      plugin_id: PLUGIN_ID,
      mode,
      placement,
      block_id: blockId,
      block_created: stored.created,
      state_persisted: stored.persisted,
      needs,
      markdown,
      links: links.map((link) => ({
        id: link.id,
        link_id: link.link_id,
        link_index: link.link_index,
        link_total: link.link_total,
        link_host: link.link_host,
        title: link.title,
        kind: link.kind,
        url: link.url,
      })),
      shown_command: shownCommand,
      shown_command_template: shownCommandTemplate,
      tracking: {
        sent: false,
        confirm_with: 'track.mjs shown',
        note: '生成本身不发送事件；只有实际插入回答后确认展示才上报',
      },
    });
  } else {
    process.stdout.write(`${markdown}\n`);
    process.stderr.write(`[recommend] run_id=${runId} block_id=${blockId} links=${allLinkIds}\n`);
    process.stderr.write(
      `[recommend] 生成时不发送任何事件；确认区块已插入回答后执行: ${shownCommandTemplate}\n`,
    );
  }

  if (!stored.persisted) {
    process.stderr.write('[recommend] 警告：本机调用状态写入失败，展示确认可能无法去重\n');
  }
}

main();
