import { Type } from "@sinclair/typebox";
import { Client, EmbedBuilder, GatewayIntentBits } from "discord.js";

interface PluginApi {
  pluginConfig: unknown;
  config: unknown;
  logger: {
    info(msg: string): void;
    warn(msg: string): void;
    error(msg: string): void;
    debug?(msg: string): void;
  };
  runtime: {
    discord?: {
      getClient(accountId?: string): any | null;
    };
  };
  registerTool(tool: {
    name: string;
    label: string;
    description: string;
    parameters: unknown;
    execute: (
      toolCallId: string,
      params: unknown,
    ) => Promise<{
      content: Array<{ type: string; text: string }>;
      details?: unknown;
    }>;
  }): void;
  registerService(service: {
    id: string;
    start: () => Promise<void> | void;
    stop: () => Promise<void> | void;
  }): void;
}

const HexColorSchema = Type.String({ pattern: "^#?[0-9A-Fa-f]{6}$" });
const PermissionsSchema = Type.String({ pattern: "^[0-9]+$" });
const SnowflakeSchema = Type.String({ pattern: "^[0-9]{17,20}$" });
const MAX_TIMEOUT_MS = 28 * 24 * 60 * 60 * 1000;

const RoleCreateSchema = Type.Object(
  {
    action: Type.Literal("role-create"),
    guildId: SnowflakeSchema,
    name: Type.String(),
    color: Type.Optional(HexColorSchema),
    hoist: Type.Optional(Type.Boolean()),
    mentionable: Type.Optional(Type.Boolean()),
    permissions: Type.Optional(PermissionsSchema),
  },
  { additionalProperties: false },
);

const RoleEditSchema = Type.Object(
  {
    action: Type.Literal("role-edit"),
    guildId: SnowflakeSchema,
    roleId: SnowflakeSchema,
    name: Type.Optional(Type.String()),
    color: Type.Optional(HexColorSchema),
    hoist: Type.Optional(Type.Boolean()),
    mentionable: Type.Optional(Type.Boolean()),
    permissions: Type.Optional(PermissionsSchema),
  },
  { additionalProperties: false },
);

const RoleDeleteSchema = Type.Object(
  {
    action: Type.Literal("role-delete"),
    guildId: SnowflakeSchema,
    roleId: SnowflakeSchema,
  },
  { additionalProperties: false },
);

const KickSchema = Type.Object(
  {
    action: Type.Literal("kick"),
    guildId: SnowflakeSchema,
    userId: SnowflakeSchema,
    reason: Type.Optional(Type.String()),
  },
  { additionalProperties: false },
);

const BanSchema = Type.Object(
  {
    action: Type.Literal("ban"),
    guildId: SnowflakeSchema,
    userId: SnowflakeSchema,
    reason: Type.Optional(Type.String()),
    deleteMessageDays: Type.Optional(
      Type.Number({ minimum: 0, maximum: 7, multipleOf: 1 }),
    ),
  },
  { additionalProperties: false },
);

const UnbanSchema = Type.Object(
  {
    action: Type.Literal("unban"),
    guildId: SnowflakeSchema,
    userId: SnowflakeSchema,
  },
  { additionalProperties: false },
);

const TimeoutSchema = Type.Object(
  {
    action: Type.Literal("timeout"),
    guildId: SnowflakeSchema,
    userId: SnowflakeSchema,
    durationMs: Type.Number({ minimum: 1, maximum: MAX_TIMEOUT_MS, multipleOf: 1 }),
    reason: Type.Optional(Type.String()),
  },
  { additionalProperties: false },
);

const UntimeoutSchema = Type.Object(
  {
    action: Type.Literal("untimeout"),
    guildId: SnowflakeSchema,
    userId: SnowflakeSchema,
  },
  { additionalProperties: false },
);

const WarnSchema = Type.Object(
  {
    action: Type.Literal("warn"),
    guildId: SnowflakeSchema,
    userId: SnowflakeSchema,
    reason: Type.String(),
  },
  { additionalProperties: false },
);

const BulkDeleteSchema = Type.Object(
  {
    action: Type.Literal("bulk-delete"),
    channelId: SnowflakeSchema,
    count: Type.Number({ minimum: 2, maximum: 100, multipleOf: 1 }),
    reason: Type.Optional(Type.String()),
  },
  { additionalProperties: false },
);

const ChannelCloneSchema = Type.Object(
  {
    action: Type.Literal("channel-clone"),
    channelId: SnowflakeSchema,
    name: Type.Optional(Type.String()),
  },
  { additionalProperties: false },
);

const ChannelLockSchema = Type.Object(
  {
    action: Type.Literal("channel-lock"),
    channelId: SnowflakeSchema,
    guildId: SnowflakeSchema,
    reason: Type.Optional(Type.String()),
  },
  { additionalProperties: false },
);

const ChannelUnlockSchema = Type.Object(
  {
    action: Type.Literal("channel-unlock"),
    channelId: SnowflakeSchema,
    guildId: SnowflakeSchema,
    reason: Type.Optional(Type.String()),
  },
  { additionalProperties: false },
);

const ChannelSlowmodeSchema = Type.Object(
  {
    action: Type.Literal("channel-slowmode"),
    channelId: SnowflakeSchema,
    seconds: Type.Number({ minimum: 0, maximum: 21600, multipleOf: 1 }),
  },
  { additionalProperties: false },
);

const ChannelPrivateSchema = Type.Object(
  {
    action: Type.Literal("channel-private"),
    channelId: SnowflakeSchema,
    guildId: SnowflakeSchema,
    allowRoleIds: Type.Array(SnowflakeSchema, { description: "Role IDs that can see the channel" }),
    reason: Type.Optional(Type.String()),
  },
  { additionalProperties: false },
);

const InviteCreateSchema = Type.Object(
  {
    action: Type.Literal("invite-create"),
    channelId: SnowflakeSchema,
    maxAge: Type.Optional(Type.Number({ minimum: 0, multipleOf: 1 })),
    maxUses: Type.Optional(Type.Number({ minimum: 0, multipleOf: 1 })),
    temporary: Type.Optional(Type.Boolean()),
  },
  { additionalProperties: false },
);

const InviteListSchema = Type.Object(
  {
    action: Type.Literal("invite-list"),
    guildId: SnowflakeSchema,
  },
  { additionalProperties: false },
);

const InviteDeleteSchema = Type.Object(
  {
    action: Type.Literal("invite-delete"),
    code: Type.String(),
  },
  { additionalProperties: false },
);

const WebhookCreateSchema = Type.Object(
  {
    action: Type.Literal("webhook-create"),
    channelId: SnowflakeSchema,
    name: Type.String(),
    avatarUrl: Type.Optional(Type.String()),
  },
  { additionalProperties: false },
);

const WebhookListSchema = Type.Object(
  {
    action: Type.Literal("webhook-list"),
    channelId: Type.Optional(SnowflakeSchema),
    guildId: Type.Optional(SnowflakeSchema),
  },
  { additionalProperties: false },
);

const WebhookDeleteSchema = Type.Object(
  {
    action: Type.Literal("webhook-delete"),
    webhookId: SnowflakeSchema,
  },
  { additionalProperties: false },
);

const ServerInfoSchema = Type.Object(
  {
    action: Type.Literal("server-info"),
    guildId: SnowflakeSchema,
  },
  { additionalProperties: false },
);

const AuditLogSchema = Type.Object(
  {
    action: Type.Literal("audit-log"),
    guildId: SnowflakeSchema,
    limit: Type.Optional(Type.Number({ minimum: 1, maximum: 100, multipleOf: 1 })),
    actionType: Type.Optional(Type.Number({ minimum: 0, multipleOf: 1 })),
  },
  { additionalProperties: false },
);

const MemberListSchema = Type.Object(
  {
    action: Type.Literal("member-list"),
    guildId: SnowflakeSchema,
    roleId: Type.Optional(SnowflakeSchema),
    limit: Type.Optional(Type.Number({ minimum: 1, maximum: 1000, multipleOf: 1 })),
  },
  { additionalProperties: false },
);

const NicknameSetSchema = Type.Object(
  {
    action: Type.Literal("nickname-set"),
    guildId: SnowflakeSchema,
    userId: SnowflakeSchema,
    nickname: Type.String(),
  },
  { additionalProperties: false },
);

const AdminActionSchema = Type.Union([
  RoleCreateSchema,
  RoleEditSchema,
  RoleDeleteSchema,
  KickSchema,
  BanSchema,
  UnbanSchema,
  TimeoutSchema,
  UntimeoutSchema,
  WarnSchema,
  BulkDeleteSchema,
  ChannelCloneSchema,
  ChannelLockSchema,
  ChannelUnlockSchema,
  ChannelSlowmodeSchema,
  ChannelPrivateSchema,
  InviteCreateSchema,
  InviteListSchema,
  InviteDeleteSchema,
  WebhookCreateSchema,
  WebhookListSchema,
  WebhookDeleteSchema,
  ServerInfoSchema,
  AuditLogSchema,
  MemberListSchema,
  NicknameSetSchema,
]);

const json = (payload: unknown) => ({
  content: [{ type: "text", text: JSON.stringify(payload, null, 2) }],
  details: payload,
});

const getErrorMessage = (error: unknown): string => {
  if (error instanceof Error) return error.message;
  return String(error);
};

const parseColor = (input?: string): number | undefined => {
  if (input == null) return undefined;
  const normalized = input.startsWith("#") ? input.slice(1) : input;
  if (!/^[0-9A-Fa-f]{6}$/.test(normalized)) {
    throw new Error(`Invalid color '${input}'. Use #RRGGBB format.`);
  }
  return parseInt(normalized, 16);
};

const parsePermissions = (input?: string): bigint | undefined => {
  if (input == null) return undefined;
  if (!/^[0-9]+$/.test(input)) {
    throw new Error("permissions must be a decimal string bitfield");
  }
  try {
    return BigInt(input);
  } catch {
    throw new Error(`Invalid permissions bitfield: ${input}`);
  }
};

// Module-level client — initialized in register(), shared across all tool calls
let _adminClient: Client | null = null;

const requireClient = (_api: PluginApi): any => {
  if (!_adminClient) {
    throw new Error("Discord admin client not ready — plugin may still be connecting");
  }
  return _adminClient;
};

const requireGuild = async (client: any, guildId: string): Promise<any> => {
  const guild = await client.guilds.fetch(guildId);
  if (!guild) throw new Error(`Guild not found: ${guildId}`);
  return guild;
};

const requireChannel = async (client: any, channelId: string): Promise<any> => {
  const channel = await client.channels.fetch(channelId);
  if (!channel) throw new Error(`Channel not found: ${channelId}`);
  return channel;
};

const hasGuildMembersIntent = (client: any): boolean => {
  const intents = client?.options?.intents;
  if (intents == null) return true;
  if (typeof intents.has === "function") {
    return intents.has(GatewayIntentBits.GuildMembers);
  }
  if (typeof intents === "number") {
    return (intents & GatewayIntentBits.GuildMembers) === GatewayIntentBits.GuildMembers;
  }
  if (typeof intents === "bigint") {
    const bit = BigInt(GatewayIntentBits.GuildMembers);
    return (intents & bit) === bit;
  }
  if (typeof intents?.bitfield === "number") {
    return (
      (intents.bitfield & GatewayIntentBits.GuildMembers) === GatewayIntentBits.GuildMembers
    );
  }
  if (typeof intents?.bitfield === "bigint") {
    const bit = BigInt(GatewayIntentBits.GuildMembers);
    return (intents.bitfield & bit) === bit;
  }
  if (Array.isArray(intents)) {
    return (
      intents.includes(GatewayIntentBits.GuildMembers) ||
      intents.includes("GuildMembers") ||
      intents.includes("GUILD_MEMBERS")
    );
  }
  return true;
};

const ensureGuildMembersIntent = (client: any, action: string): void => {
  if (!hasGuildMembersIntent(client)) {
    throw new Error(
      `${action} requires the GuildMembers gateway intent (GatewayIntentBits.GuildMembers)`,
    );
  }
};

const ensureChannelInGuild = (channel: any, guildId: string, channelId: string): void => {
  const channelGuildId = (channel as { guildId?: string | null })?.guildId ?? null;
  if (channelGuildId == null) {
    throw new Error(`Channel ${channelId} is not a guild channel`);
  }
  if (channelGuildId !== guildId) {
    throw new Error(`Channel ${channelId} does not belong to guild ${guildId}`);
  }
};

const withActionResult = async (
  fn: () => Promise<Record<string, unknown>>,
): Promise<{ content: Array<{ type: string; text: string }>; details?: unknown }> => {
  try {
    const result = await fn();
    return json({ success: true, ...result });
  } catch (error) {
    return json({ success: false, error: getErrorMessage(error) });
  }
};

export default {
  id: "discord-admin",
  name: "Discord Admin",
  description:
    "Full Discord server administration suite: roles, moderation, channels, invites, webhooks, audit log",
  configSchema: {
    parse(v: unknown) {
      const raw = (v ?? {}) as { enabled?: unknown };
      return {
        enabled: typeof raw.enabled === "boolean" ? raw.enabled : true,
      };
    },
  },
  register(api: PluginApi) {
    const cfg = api.pluginConfig as { enabled?: boolean };
    if (cfg?.enabled === false) return;

    // Spin up our own Discord client (same pattern as discord-voice)
    const mainConfig = api.config as { channels?: { discord?: { token?: string } }; discord?: { token?: string } };
    const discordToken = mainConfig?.channels?.discord?.token || mainConfig?.discord?.token;

    if (!discordToken) {
      api.logger.error("[discord-admin] No Discord token found in config — plugin disabled");
      return;
    }

    const client = new Client({
      intents: [
        GatewayIntentBits.Guilds,
        GatewayIntentBits.GuildMembers,
        GatewayIntentBits.GuildModeration,
        GatewayIntentBits.GuildMessages,
        GatewayIntentBits.GuildInvites,
        GatewayIntentBits.GuildWebhooks,
      ],
    });

    client.once("ready", () => {
      _adminClient = client;
      api.logger.info(`[discord-admin] Connected as ${client.user?.tag}`);
    });

    api.registerService({
      id: "discord-admin-client",
      async start() {
        await client.login(discordToken);
      },
      async stop() {
        _adminClient = null;
        client.destroy();
      },
    });

    api.registerTool({
      name: "discord_admin",
      label: "Discord Admin",
      description:
        "Discord administration tool for roles, moderation, channels, invites, webhooks, member management, and audit data",
      parameters: AdminActionSchema,
      execute: async (_toolCallId: string, params: unknown) => {
        // TODO(security): require an explicit confirmation token for destructive actions.
        const action = (params as { action?: string })?.action;

        switch (action) {
          case "role-create":
            return withActionResult(async () => {
              const client = requireClient(api);
              const input = params as {
                guildId: string;
                name: string;
                color?: string;
                hoist?: boolean;
                mentionable?: boolean;
                permissions?: string;
              };
              const guild = await requireGuild(client, input.guildId);
              const role = await guild.roles.create({
                name: input.name,
                color: parseColor(input.color),
                hoist: input.hoist,
                mentionable: input.mentionable,
                permissions: parsePermissions(input.permissions),
              });
              return {
                action,
                guildId: guild.id,
                role: {
                  id: role.id,
                  name: role.name,
                  color: role.color,
                  hoist: role.hoist,
                  mentionable: role.mentionable,
                  permissions: role.permissions.bitfield.toString(),
                },
              };
            });

          case "role-edit":
            return withActionResult(async () => {
              const client = requireClient(api);
              const input = params as {
                guildId: string;
                roleId: string;
                name?: string;
                color?: string;
                hoist?: boolean;
                mentionable?: boolean;
                permissions?: string;
              };
              const guild = await requireGuild(client, input.guildId);
              const role = await guild.roles.fetch(input.roleId);
              if (!role) throw new Error(`Role not found: ${input.roleId}`);
              const updated = await role.edit({
                name: input.name,
                color: parseColor(input.color),
                hoist: input.hoist,
                mentionable: input.mentionable,
                permissions: parsePermissions(input.permissions),
              });
              return {
                action,
                guildId: guild.id,
                role: {
                  id: updated.id,
                  name: updated.name,
                  color: updated.color,
                  hoist: updated.hoist,
                  mentionable: updated.mentionable,
                  permissions: updated.permissions.bitfield.toString(),
                },
              };
            });

          case "role-delete":
            return withActionResult(async () => {
              const client = requireClient(api);
              const input = params as { guildId: string; roleId: string };
              const guild = await requireGuild(client, input.guildId);
              const role = await guild.roles.fetch(input.roleId);
              if (!role) throw new Error(`Role not found: ${input.roleId}`);
              await role.delete();
              return { action, guildId: guild.id, roleId: input.roleId, deleted: true };
            });

          case "kick":
            return withActionResult(async () => {
              const client = requireClient(api);
              const input = params as { guildId: string; userId: string; reason?: string };
              const guild = await requireGuild(client, input.guildId);
              ensureGuildMembersIntent(client, "kick");
              const member = await guild.members.fetch(input.userId);
              await member.kick(input.reason);
              return {
                action,
                guildId: guild.id,
                userId: input.userId,
                reason: input.reason ?? null,
                kicked: true,
              };
            });

          case "ban":
            return withActionResult(async () => {
              const client = requireClient(api);
              const input = params as {
                guildId: string;
                userId: string;
                reason?: string;
                deleteMessageDays?: number;
              };
              const guild = await requireGuild(client, input.guildId);
              const deleteMessageSeconds =
                input.deleteMessageDays == null
                  ? undefined
                  : Math.trunc(input.deleteMessageDays) * 24 * 60 * 60;
              await guild.members.ban(input.userId, {
                reason: input.reason,
                deleteMessageSeconds,
              });
              return {
                action,
                guildId: guild.id,
                userId: input.userId,
                reason: input.reason ?? null,
                deleteMessageDays: input.deleteMessageDays ?? null,
                banned: true,
              };
            });

          case "unban":
            return withActionResult(async () => {
              const client = requireClient(api);
              const input = params as { guildId: string; userId: string };
              const guild = await requireGuild(client, input.guildId);
              await guild.bans.remove(input.userId);
              return {
                action,
                guildId: guild.id,
                userId: input.userId,
                unbanned: true,
              };
            });

          case "timeout":
            return withActionResult(async () => {
              const client = requireClient(api);
              const input = params as {
                guildId: string;
                userId: string;
                durationMs: number;
                reason?: string;
              };
              const guild = await requireGuild(client, input.guildId);
              const durationMs = Math.trunc(input.durationMs);
              if (durationMs < 1 || durationMs > MAX_TIMEOUT_MS) {
                throw new Error(
                  `durationMs must be between 1 and ${MAX_TIMEOUT_MS} milliseconds (28 days)`,
                );
              }
              ensureGuildMembersIntent(client, "timeout");
              const member = await guild.members.fetch(input.userId);
              await member.timeout(durationMs, input.reason);
              return {
                action,
                guildId: guild.id,
                userId: input.userId,
                durationMs,
                reason: input.reason ?? null,
                timeoutApplied: true,
              };
            });

          case "untimeout":
            return withActionResult(async () => {
              const client = requireClient(api);
              const input = params as { guildId: string; userId: string };
              const guild = await requireGuild(client, input.guildId);
              ensureGuildMembersIntent(client, "untimeout");
              const member = await guild.members.fetch(input.userId);
              await member.timeout(null);
              return {
                action,
                guildId: guild.id,
                userId: input.userId,
                timeoutRemoved: true,
              };
            });

          case "warn":
            return withActionResult(async () => {
              const client = requireClient(api);
              const input = params as { guildId: string; userId: string; reason: string };
              const guild = await requireGuild(client, input.guildId);
              const user = await client.users.fetch(input.userId);
              const dm = await user.createDM();
              const embed = new EmbedBuilder()
                .setTitle(`Warning from ${guild.name}`)
                .setDescription(input.reason)
                .setColor(0xffaa00)
                .setTimestamp();

              await dm.send({ embeds: [embed] });

              return {
                action,
                guildId: guild.id,
                userId: input.userId,
                reason: input.reason,
                warned: true,
              };
            });

          case "bulk-delete":
            return withActionResult(async () => {
              const client = requireClient(api);
              const input = params as { channelId: string; count: number; reason?: string };
              const channel = await requireChannel(client, input.channelId);
              if (typeof (channel as any).bulkDelete !== "function") {
                throw new Error("Channel does not support bulk delete");
              }
              const deleted = await (channel as any).bulkDelete(
                Math.trunc(input.count),
                true,
              );
              const deletedCount = typeof deleted?.size === "number" ? deleted.size : 0;
              return {
                action,
                channelId: input.channelId,
                requestedCount: Math.trunc(input.count),
                deletedCount,
                reason: input.reason ?? null,
              };
            });

          case "channel-clone":
            return withActionResult(async () => {
              const client = requireClient(api);
              const input = params as { channelId: string; name?: string };
              const channel = await requireChannel(client, input.channelId);
              if (typeof (channel as any).clone !== "function") {
                throw new Error("Channel does not support clone");
              }
              const cloned = await (channel as any).clone({ name: input.name });
              return {
                action,
                sourceChannelId: input.channelId,
                clonedChannelId: cloned.id,
                name: cloned.name,
              };
            });

          case "channel-lock":
            return withActionResult(async () => {
              const client = requireClient(api);
              const input = params as {
                channelId: string;
                guildId: string;
                reason?: string;
              };
              const guild = await requireGuild(client, input.guildId);
              const channel = await requireChannel(client, input.channelId);
              ensureChannelInGuild(channel, guild.id, input.channelId);
              if (!(channel as any).permissionOverwrites?.edit) {
                throw new Error("Channel does not support permission overwrites");
              }
              await (channel as any).permissionOverwrites.edit(
                guild.roles.everyone,
                { SendMessages: false },
                { reason: input.reason },
              );
              return {
                action,
                guildId: guild.id,
                channelId: input.channelId,
                reason: input.reason ?? null,
                locked: true,
              };
            });

          case "channel-unlock":
            return withActionResult(async () => {
              const client = requireClient(api);
              const input = params as {
                channelId: string;
                guildId: string;
                reason?: string;
              };
              const guild = await requireGuild(client, input.guildId);
              const channel = await requireChannel(client, input.channelId);
              ensureChannelInGuild(channel, guild.id, input.channelId);
              if (!(channel as any).permissionOverwrites?.edit) {
                throw new Error("Channel does not support permission overwrites");
              }
              await (channel as any).permissionOverwrites.edit(
                guild.roles.everyone,
                { SendMessages: null },
                { reason: input.reason },
              );
              return {
                action,
                guildId: guild.id,
                channelId: input.channelId,
                reason: input.reason ?? null,
                unlocked: true,
              };
            });

          case "channel-slowmode":
            return withActionResult(async () => {
              const client = requireClient(api);
              const input = params as { channelId: string; seconds: number };
              const channel = await requireChannel(client, input.channelId);
              if (typeof (channel as any).setRateLimitPerUser !== "function") {
                throw new Error("Channel does not support slowmode");
              }
              await (channel as any).setRateLimitPerUser(Math.trunc(input.seconds));
              return {
                action,
                channelId: input.channelId,
                seconds: Math.trunc(input.seconds),
              };
            });

          case "channel-private":
            return withActionResult(async () => {
              const client = requireClient(api);
              const input = params as { channelId: string; guildId: string; allowRoleIds: string[]; reason?: string };
              const guild = await requireGuild(client, input.guildId);
              const channel = await requireChannel(client, input.channelId);
              // Deny ViewChannel for @everyone
              await channel.permissionOverwrites.edit(
                guild.roles.everyone,
                { ViewChannel: false },
                { reason: input.reason ?? "channel-private: hidden from @everyone" },
              );
              // Allow ViewChannel for each specified role
              for (const roleId of input.allowRoleIds) {
                await channel.permissionOverwrites.edit(
                  roleId,
                  { ViewChannel: true, SendMessages: true },
                  { reason: input.reason ?? "channel-private: granted to role" },
                );
              }
              return {
                action,
                channelId: input.channelId,
                guildId: input.guildId,
                everyoneDenied: true,
                rolesGranted: input.allowRoleIds,
              };
            });

          case "invite-create":
            return withActionResult(async () => {
              const client = requireClient(api);
              const input = params as {
                channelId: string;
                maxAge?: number;
                maxUses?: number;
                temporary?: boolean;
              };
              const channel = await requireChannel(client, input.channelId);
              if (typeof (channel as any).createInvite !== "function") {
                throw new Error("Channel does not support invites");
              }
              const invite = await (channel as any).createInvite({
                maxAge: input.maxAge == null ? undefined : Math.trunc(input.maxAge),
                maxUses: input.maxUses == null ? undefined : Math.trunc(input.maxUses),
                temporary: input.temporary,
              });
              return {
                action,
                channelId: input.channelId,
                invite: {
                  code: invite.code,
                  url: invite.url,
                  maxAge: invite.maxAge,
                  maxUses: invite.maxUses,
                  temporary: invite.temporary,
                  uses: invite.uses,
                },
              };
            });

          case "invite-list":
            return withActionResult(async () => {
              const client = requireClient(api);
              const input = params as { guildId: string };
              const guild = await requireGuild(client, input.guildId);
              const invites = await guild.invites.fetch();
              return {
                action,
                guildId: guild.id,
                invites: invites.map((invite: any) => ({
                  code: invite.code,
                  channelId: invite.channelId,
                  inviterId: invite.inviterId,
                  url: invite.url,
                  uses: invite.uses,
                  maxUses: invite.maxUses,
                  maxAge: invite.maxAge,
                  temporary: invite.temporary,
                })),
              };
            });

          case "invite-delete":
            return withActionResult(async () => {
              const client = requireClient(api);
              const input = params as { code: string };
              const invite = await client.fetchInvite(input.code);
              await invite.delete();
              return {
                action,
                code: input.code,
                deleted: true,
              };
            });

          case "webhook-create":
            return withActionResult(async () => {
              const client = requireClient(api);
              const input = params as { channelId: string; name: string; avatarUrl?: string };
              const channel = await requireChannel(client, input.channelId);
              if (typeof (channel as any).createWebhook !== "function") {
                throw new Error("Channel does not support webhooks");
              }
              const webhook = await (channel as any).createWebhook({
                name: input.name,
                avatar: input.avatarUrl,
              });
              return {
                action,
                channelId: input.channelId,
                webhook: {
                  id: webhook.id,
                  name: webhook.name,
                  channelId: webhook.channelId,
                  url: webhook.url,
                },
              };
            });

          case "webhook-list":
            return withActionResult(async () => {
              const client = requireClient(api);
              const input = params as { guildId?: string; channelId?: string };
              const hasChannelId = typeof input.channelId === "string";
              const hasGuildId = typeof input.guildId === "string";
              if (hasChannelId === hasGuildId) {
                throw new Error("webhook-list requires exactly one of channelId or guildId");
              }
              if (hasChannelId) {
                const channelId = input.channelId as string;
                const channel = await requireChannel(client, channelId);
                if (typeof (channel as any).fetchWebhooks !== "function") {
                  throw new Error("Channel does not support webhooks");
                }
                const hooks = await (channel as any).fetchWebhooks();
                return {
                  action,
                  channelId,
                  webhooks: hooks.map((hook: any) => ({
                    id: hook.id,
                    name: hook.name,
                    channelId: hook.channelId,
                    url: hook.url,
                  })),
                };
              }
              if (hasGuildId) {
                const guildId = input.guildId as string;
                const guild = await requireGuild(client, guildId);
                const hooks = await guild.fetchWebhooks();
                return {
                  action,
                  guildId: guild.id,
                  webhooks: hooks.map((hook: any) => ({
                    id: hook.id,
                    name: hook.name,
                    channelId: hook.channelId,
                    url: hook.url,
                  })),
                };
              }
              throw new Error("webhook-list requires exactly one of channelId or guildId");
            });

          case "webhook-delete":
            return withActionResult(async () => {
              const client = requireClient(api);
              const input = params as { webhookId: string };
              const webhook = await client.fetchWebhook(input.webhookId);
              await webhook.delete();
              return {
                action,
                webhookId: input.webhookId,
                deleted: true,
              };
            });

          case "server-info":
            return withActionResult(async () => {
              const client = requireClient(api);
              const input = params as { guildId: string };
              const guild = await requireGuild(client, input.guildId);
              const channels = await guild.channels.fetch();
              const roles = await guild.roles.fetch();
              return {
                action,
                guild: {
                  id: guild.id,
                  name: guild.name,
                  memberCount: guild.memberCount,
                  channelCount: channels.filter((ch: any) => ch != null).size,
                  roleCount: roles.filter((role: any) => role != null).size,
                  boostLevel: guild.premiumTier,
                  boostCount: guild.premiumSubscriptionCount ?? 0,
                  icon: guild.iconURL({ size: 1024 }) ?? null,
                  createdAt: guild.createdAt.toISOString(),
                },
              };
            });

          case "audit-log":
            return withActionResult(async () => {
              const client = requireClient(api);
              const input = params as { guildId: string; limit?: number; actionType?: number };
              const guild = await requireGuild(client, input.guildId);
              const limit = input.limit == null ? 10 : Math.trunc(input.limit);
              const logs = await guild.fetchAuditLogs({
                limit,
                type: input.actionType as any,
              });
              return {
                action,
                guildId: guild.id,
                totalEntries: logs.entries.size,
                entries: logs.entries.map((entry: any) => ({
                  id: entry.id,
                  action: entry.action,
                  actionType: entry.actionType,
                  reason: entry.reason,
                  targetId: entry.targetId,
                  executorId: entry.executorId,
                  createdTimestamp: entry.createdTimestamp,
                })),
              };
            });

          case "member-list":
            return withActionResult(async () => {
              const client = requireClient(api);
              const input = params as { guildId: string; roleId?: string; limit?: number };
              const guild = await requireGuild(client, input.guildId);
              const limit = input.limit == null ? 50 : Math.trunc(input.limit);
              ensureGuildMembersIntent(client, "member-list");
              const members = await guild.members.fetch({ limit });
              const filtered = input.roleId
                ? members.filter((member: any) => member.roles.cache.has(input.roleId))
                : members;

              return {
                action,
                guildId: guild.id,
                roleId: input.roleId ?? null,
                count: filtered.size,
                members: filtered.map((member: any) => ({
                  id: member.id,
                  username: member.user?.username ?? null,
                  discriminator: member.user?.discriminator ?? null,
                  tag: member.user?.tag ?? null,
                  displayName: member.displayName,
                  nickname: member.nickname,
                  joinedAt: member.joinedAt ? member.joinedAt.toISOString() : null,
                })),
              };
            });

          case "nickname-set":
            return withActionResult(async () => {
              const client = requireClient(api);
              const input = params as { guildId: string; userId: string; nickname: string };
              const guild = await requireGuild(client, input.guildId);
              ensureGuildMembersIntent(client, "nickname-set");
              const member = await guild.members.fetch(input.userId);
              const nickname = input.nickname === "" ? null : input.nickname;
              await member.setNickname(nickname);
              return {
                action,
                guildId: guild.id,
                userId: input.userId,
                nickname: nickname ?? "",
                updated: true,
              };
            });

          default:
            return json({
              success: false,
              error: `Unknown action: ${String(action)}`,
            });
        }
      },
    });
  },
};
