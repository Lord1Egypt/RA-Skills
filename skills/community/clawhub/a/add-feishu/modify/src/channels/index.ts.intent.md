# Intent: Add Feishu channel import

Add `import './feishu.js';` to the channel barrel file so the Feishu
module self-registers with the channel registry on startup.

This is an append-only change — existing import lines for other channels
(telegram, whatsapp, slack, etc.) must be preserved.

The import must be placed under the `// feishu` comment block, grouped
alphabetically with other channel imports.
