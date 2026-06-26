#!/usr/bin/env node
import { parseArgs, printJson, resolveToken, sanitizeObject, writeJson } from './common.mjs';
import { createGuildChannel, deleteChannel, getChannel } from './discord-api.mjs';
import { buildNukeCode } from './job-code.mjs';

const helpText = `Usage:
  node scripts/purge-nuke.mjs --channel-id <id> --confirm <code> [options]

Options:
  --token <token>            Discord bot token (or use DISCORD_BOT_TOKEN)
  --channel-id <id>          Target guild channel id
  --confirm <code>           Confirmation code
  --delete-old               Delete original channel after clone
  --reason <text>            Audit log reason
  --out <path>               Persist result JSON
  --help                     Show this message
`;

function buildClonePayload(channel) {
  return sanitizeObject({
    name: channel.name,
    type: channel.type,
    topic: channel.topic,
    bitrate: channel.bitrate,
    user_limit: channel.user_limit,
    rate_limit_per_user: channel.rate_limit_per_user,
    position: channel.position,
    permission_overwrites: channel.permission_overwrites,
    parent_id: channel.parent_id,
    nsfw: channel.nsfw,
    rtc_region: channel.rtc_region,
    video_quality_mode: channel.video_quality_mode,
    default_auto_archive_duration: channel.default_auto_archive_duration,
    default_thread_rate_limit_per_user: channel.default_thread_rate_limit_per_user,
    default_sort_order: channel.default_sort_order,
    default_forum_layout: channel.default_forum_layout,
    available_tags: channel.available_tags,
    default_reaction_emoji: channel.default_reaction_emoji,
    default_tag_ids: channel.default_tag_ids,
    flags: channel.flags,
  });
}

async function main() {
  const args = parseArgs();

  if (args.help) {
    process.stdout.write(helpText);
    return;
  }

  const channelId = String(args['channel-id'] ?? '');
  if (!channelId) throw new Error('Missing required argument --channel-id');

  const token = resolveToken(args);
  const expectedCode = buildNukeCode({ channelId });
  const providedCode = String(args.confirm ?? '');

  if (!providedCode) throw new Error('Missing required argument --confirm');
  if (providedCode !== expectedCode) {
    throw new Error(`Confirmation mismatch. Expected ${expectedCode}`);
  }

  const channel = await getChannel({ token, channelId });
  if (!channel.guild_id) {
    throw new Error('Target channel is not in a guild. Nuke flow supports guild channels only.');
  }

  const clonePayload = buildClonePayload(channel);
  const reason = args.reason ? String(args.reason) : undefined;
  const newChannel = await createGuildChannel({
    token,
    guildId: String(channel.guild_id),
    body: clonePayload,
    reason,
  });

  let deletedOriginal = false;
  if (args['delete-old']) {
    await deleteChannel({ token, channelId, reason });
    deletedOriginal = true;
  }

  const result = {
    generatedAt: new Date().toISOString(),
    guildId: String(channel.guild_id),
    originalChannelId: channelId,
    newChannelId: String(newChannel.id),
    deletedOriginal,
    expectedConfirmCode: expectedCode,
  };

  if (args.out) {
    await writeJson(String(args.out), result);
  }

  printJson(result);
}

main().catch((error) => {
  process.stderr.write(`${error.message}\n`);
  process.exitCode = 1;
});
