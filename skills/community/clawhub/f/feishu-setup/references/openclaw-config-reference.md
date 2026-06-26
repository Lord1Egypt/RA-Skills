# OpenClaw Configuration Reference for Feishu

Complete config template for Feishu integration. All credential fields use placeholders — replace with your own values.

## Channel Config (`channels.feishu`)

```json5
{
  channels: {
    feishu: {
      enabled: true,
      appId: '<YOUR_APP_ID>',              // e.g. cli_a945c2a5167bdbb4
      appSecret: '<YOUR_APP_SECRET>',       // Or use secret provider reference
      domain: 'feishu',                     // 'feishu' (China) or 'lark' (International)
      requireMention: true,                 // In groups, bot responds only when @mentioned
      dmPolicy: 'allowlist',                // 'open' | 'allowlist' | 'owner'
      allowFrom: [
        '<OWNER_OPEN_ID>',                  // e.g. ou_xxxxx — who can DM the bot
      ],
      groupPolicy: 'allowlist',             // 'open' | 'allowlist'
      groupAllowFrom: [
        '<OWNER_OPEN_ID>',                  // Who can add bot to groups
      ],
      groups: {
        '*': {
          enabled: true,                    // Enable all groups by default
        },
      },
      streaming: false,                     // Stream responses token-by-token
      threadSession: true,                  // Each group thread = separate session
      footer: {
        elapsed: false,                     // Show response time
        status: false,                      // Show status indicator
      },
    },
  },
}
```

### Policy Options

| Policy | dmPolicy | groupPolicy | Behavior |
|--------|----------|-------------|----------|
| Owner only | `owner` or `allowlist` with single ID | `allowlist` | Only owner can interact |
| Team | `allowlist` with multiple IDs | `allowlist` | Allowlisted users only |
| Open | `open` | `open` | Anyone can interact |

## Plugin Config (`plugins`)

```json5
{
  plugins: {
    allow: [
      'openclaw-lark',                      // Required: Feishu channel plugin
      'openclaw-extension-miaoda',          // Optional: Miaoda platform
      'openclaw-extension-miaoda-coding',   // Optional: Miaoda vibe-coding
    ],
    entries: {
      'openclaw-lark': {
        enabled: true,
      },
      // Disable the built-in feishu plugin (use openclaw-lark instead)
      'feishu': {
        enabled: false,
      },
    },
  },
}
```

## Tool Config (`tools`)

### Enable Feishu Tools (`tools.alsoAllow`)

```json5
{
  tools: {
    profile: 'full',
    alsoAllow: [
      // === Bitable (多维表格) ===
      'feishu_bitable_app',
      'feishu_bitable_app_table',
      'feishu_bitable_app_table_field',
      'feishu_bitable_app_table_record',
      'feishu_bitable_app_table_view',      // Optional: view management

      // === Calendar (日历) ===
      'feishu_calendar_calendar',
      'feishu_calendar_event',
      'feishu_calendar_event_attendee',
      'feishu_calendar_freebusy',

      // === Chat (群聊) ===
      'feishu_chat',
      'feishu_chat_members',

      // === Docs (文档) ===
      'feishu_create_doc',
      'feishu_fetch_doc',
      'feishu_update_doc',

      // === Drive & Media ===
      'feishu_doc_comments',                // Optional: document comments
      'feishu_doc_media',                   // Optional: document media
      'feishu_drive_file',                  // Optional: drive file management

      // === User & Contact ===
      'feishu_get_user',
      'feishu_search_user',

      // === IM (消息) ===
      'feishu_im_bot_image',                // Bot downloads images/files
      'feishu_im_user_fetch_resource',      // User identity downloads
      'feishu_im_user_get_messages',        // Read chat history
      'feishu_im_user_get_thread_messages', // Read thread messages
      'feishu_im_user_message',             // Send as user identity
      'feishu_im_user_search_messages',     // Cross-chat message search

      // === OAuth ===
      'feishu_oauth',                       // Revoke authorization
      'feishu_oauth_batch_auth',            // Batch authorize all scopes

      // === Search ===
      'feishu_search_doc_wiki',             // Search docs & wiki

      // === Sheets ===
      'feishu_sheet',                       // Optional: spreadsheet ops

      // === Task ===
      'feishu_task_task',                   // Optional: task CRUD
      'feishu_task_tasklist',               // Optional: task list management
      'feishu_task_comment',                // Optional: task comments
      'feishu_task_subtask',                // Optional: subtasks

      // === Wiki ===
      'feishu_wiki_space',                  // Optional: wiki space
      'feishu_wiki_space_node',             // Optional: wiki nodes
    ],
  },
}
```

### Disable Specific Tools (`tools.deny`)

```json5
{
  tools: {
    deny: [
      // Common non-feishu tools to disable
      'web_fetch',
      'tts',
      'agents_list',

      // Feishu tools to disable (based on your needs):
      // 'feishu_task_task',
      // 'feishu_task_tasklist',
      // 'feishu_task_comment',
      // 'feishu_task_subtask',
      // 'feishu_bitable_app_table_view',
      // 'feishu_doc_comments',
      // 'feishu_doc_media',
      // 'feishu_drive_file',
      // 'feishu_wiki_space',
      // 'feishu_wiki_space_node',
      // 'feishu_sheet',
    ],
  },
}
```

## Skills Config (`skills.entries`)

```json5
{
  skills: {
    entries: {
      // Feishu task skill — disabled by default, enable if needed
      'feishu-task': {
        enabled: false,  // Set true to enable task capabilities
      },
    },
  },
}
```

## Session Config

```json5
{
  session: {
    dmScope: 'per-channel-peer',  // Each DM user gets own session
  },
}
```

## Messages Config

```json5
{
  messages: {
    ackReactionScope: 'group-mentions',  // React emoji when mentioned in group
  },
}
```

## Full Minimal Config

Minimal config to get Feishu working:

```json5
{
  channels: {
    feishu: {
      enabled: true,
      appId: '<YOUR_APP_ID>',
      appSecret: '<YOUR_APP_SECRET>',
      domain: 'feishu',
      requireMention: true,
      dmPolicy: 'allowlist',
      allowFrom: ['<YOUR_OPEN_ID>'],
      groupPolicy: 'allowlist',
      groupAllowFrom: ['<YOUR_OPEN_ID>'],
      groups: { '*': { enabled: true } },
      streaming: false,
      threadSession: true,
      footer: { elapsed: false, status: false },
    },
  },
  plugins: {
    allow: ['openclaw-lark'],
    entries: {
      'openclaw-lark': { enabled: true },
      'feishu': { enabled: false },
    },
  },
}
```

## Using Secret Providers

For production, avoid putting secrets in config directly. Use secret providers:

```json5
{
  secrets: {
    providers: {
      'my-secret-provider': {
        source: 'file',           // Read from file
        path: '/path/to/secrets/', // Directory containing secret files
        mode: 'raw',              // 'raw' or 'base64'
      },
    },
  },
  channels: {
    feishu: {
      appSecret: {
        source: 'file',
        provider: 'my-secret-provider',
        id: 'feishu-app-secret',  // Reads from /path/to/secrets/feishu-app-secret
      },
    },
  },
}
```
