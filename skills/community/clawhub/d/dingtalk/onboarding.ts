import type {
  ChannelOnboardingAdapter,
  ChannelOnboardingDmPolicy,
  ClawdbotConfig,
  DmPolicy,
  WizardPrompter,
} from "openclaw/plugin-sdk";
import { addWildcardAllowFrom, DEFAULT_ACCOUNT_ID, formatDocsLink } from "openclaw/plugin-sdk";
import type { DingTalkConfig } from "./index.js";

const channel = "dingtalk" as const;

function setDingTalkDmPolicy(cfg: ClawdbotConfig, dmPolicy: DmPolicy): ClawdbotConfig {
  const allowFrom =
    dmPolicy === "open"
      ? addWildcardAllowFrom(cfg.channels?.dingtalk?.allowFrom)?.map((entry) => String(entry))
      : undefined;
  return {
    ...cfg,
    channels: {
      ...cfg.channels,
      dingtalk: {
        ...cfg.channels?.dingtalk,
        dmPolicy,
        ...(allowFrom ? { allowFrom } : {}),
      },
    },
  };
}

function setDingTalkAllowFrom(cfg: ClawdbotConfig, allowFrom: string[]): ClawdbotConfig {
  return {
    ...cfg,
    channels: {
      ...cfg.channels,
      dingtalk: {
        ...cfg.channels?.dingtalk,
        allowFrom,
      },
    },
  };
}

function parseAllowFromInput(raw: string): string[] {
  return raw
    .split(/[\n,;]+/g)
    .map((entry) => entry.trim())
    .filter(Boolean);
}

async function promptDingTalkAllowFrom(params: {
  cfg: ClawdbotConfig;
  prompter: WizardPrompter;
}): Promise<ClawdbotConfig> {
  const existing = params.cfg.channels?.dingtalk?.allowFrom ?? [];
  await params.prompter.note(
    [
      "Allowlist DingTalk DMs by user ID (staffId).",
      "You can find user IDs in DingTalk admin console.",
      "Examples:",
      "- 01234567890123456789012345678901",
      "- manager001",
    ].join("\n"),
    "DingTalk allowlist",
  );

  while (true) {
    const entry = await params.prompter.text({
      message: "DingTalk allowFrom (user IDs)",
      placeholder: "user001, user002",
      initialValue: existing[0] ? String(existing[0]) : undefined,
      validate: (value) => (String(value ?? "").trim() ? undefined : "Required"),
    });
    const parts = parseAllowFromInput(String(entry));
    if (parts.length === 0) {
      await params.prompter.note("Enter at least one user.", "DingTalk allowlist");
      continue;
    }

    const unique = [
      ...new Set([
        ...existing.map((v: string | number) => String(v).trim()).filter(Boolean),
        ...parts,
      ]),
    ];
    return setDingTalkAllowFrom(params.cfg, unique);
  }
}

async function noteDingTalkCredentialHelp(prompter: WizardPrompter): Promise<void> {
  await prompter.note(
    [
      "1) Go to DingTalk Open Platform (open.dingtalk.com)",
      "2) Create a micro-app or robot",
      "3) Get App Key and App Secret from app credentials",
      "4) For internal apps, enable required permissions:",
      "   - Contact management",
      "   - Message notifications",
      "5) Publish the app and add it to your organization",
      "Tip: you can also set DINGTALK_CLIENT_ID / DINGTALK_CLIENT_SECRET env vars.",
      "Docs: https://open.dingtalk.com/document/isv/app-types",
    ].join("\n"),
    "DingTalk credentials",
  );
}

async function promptDingTalkCredentials(prompter: WizardPrompter): Promise<{
  clientId: string;
  clientSecret: string;
}> {
  const clientId = String(
    await prompter.text({
      message: "Enter DingTalk Client ID (App Key)",
      validate: (value) => (value?.trim() ? undefined : "Required"),
    })
  ).trim();
  const clientSecret = String(
    await prompter.text({
      message: "Enter DingTalk Client Secret (App Secret)",
      validate: (value) => (value?.trim() ? undefined : "Required"),
    })
  ).trim();
  return { clientId, clientSecret };
}

function setDingTalkGroupPolicy(
  cfg: ClawdbotConfig,
  groupPolicy: "open" | "allowlist" | "disabled"
): ClawdbotConfig {
  return {
    ...cfg,
    channels: {
      ...cfg.channels,
      dingtalk: {
        ...cfg.channels?.dingtalk,
        enabled: true,
        groupPolicy,
      },
    },
  };
}

function setDingTalkGroupAllowFrom(cfg: ClawdbotConfig, groupAllowFrom: string[]): ClawdbotConfig {
  return {
    ...cfg,
    channels: {
      ...cfg.channels,
      dingtalk: {
        ...cfg.channels?.dingtalk,
        groupAllowFrom,
      },
    },
  };
}

const dmPolicy: ChannelOnboardingDmPolicy = {
  label: "DingTalk",
  channel,
  policyKey: "channels.dingtalk.dmPolicy",
  allowFromKey: "channels.dingtalk.allowFrom",
  getCurrent: (cfg) => (cfg.channels?.dingtalk as DingTalkConfig | undefined)?.dmPolicy ?? "pairing",
  setPolicy: (cfg, policy) => setDingTalkDmPolicy(cfg, policy),
  promptAllowFrom: promptDingTalkAllowFrom,
};

export const dingtalkOnboardingAdapter: ChannelOnboardingAdapter = {
  channel,
  getStatus: async ({ cfg }) => {
    const dingCfg = cfg.channels?.dingtalk as DingTalkConfig | undefined;
    const clientId = dingCfg?.clientId?.trim() || dingCfg?.appKey?.trim() || process.env.DINGTALK_CLIENT_ID?.trim() || process.env.DINGTALK_APP_KEY?.trim();
    const clientSecret = dingCfg?.clientSecret?.trim() || dingCfg?.appSecret?.trim() || process.env.DINGTALK_CLIENT_SECRET?.trim() || process.env.DINGTALK_APP_SECRET?.trim();
    const configured = Boolean(clientId && clientSecret);

    const statusLines: string[] = [];
    if (!configured) {
      statusLines.push("DingTalk: needs app credentials");
    } else {
      statusLines.push(`DingTalk: configured (clientId: ${clientId!.substring(0, 8)}...)`);
    }

    return {
      channel,
      configured,
      statusLines,
      selectionHint: configured ? "configured" : "needs app creds",
      quickstartScore: configured ? 2 : 0,
    };
  },

  configure: async ({ cfg, prompter }) => {
    const dingCfg = cfg.channels?.dingtalk as DingTalkConfig | undefined;
    const hasConfigCreds = Boolean(
      dingCfg?.clientId?.trim() && dingCfg?.clientSecret?.trim()
    );
    const canUseEnv = Boolean(
      !hasConfigCreds &&
        (process.env.DINGTALK_CLIENT_ID?.trim() || process.env.DINGTALK_APP_KEY?.trim()) &&
        (process.env.DINGTALK_CLIENT_SECRET?.trim() || process.env.DINGTALK_APP_SECRET?.trim())
    );

    let next = cfg;
    let clientId: string | null = null;
    let clientSecret: string | null = null;

    if (!hasConfigCreds && !canUseEnv) {
      await noteDingTalkCredentialHelp(prompter);
    }

    if (canUseEnv) {
      const keepEnv = await prompter.confirm({
        message: "DINGTALK_CLIENT_ID + DINGTALK_CLIENT_SECRET detected. Use env vars?",
        initialValue: true,
      });
      if (keepEnv) {
        next = {
          ...next,
          channels: {
            ...next.channels,
            dingtalk: { ...next.channels?.dingtalk, enabled: true },
          },
        };
      } else {
        const entered = await promptDingTalkCredentials(prompter);
        clientId = entered.clientId;
        clientSecret = entered.clientSecret;
      }
    } else if (hasConfigCreds) {
      const keep = await prompter.confirm({
        message: "DingTalk credentials already configured. Keep them?",
        initialValue: true,
      });
      if (!keep) {
        const entered = await promptDingTalkCredentials(prompter);
        clientId = entered.clientId;
        clientSecret = entered.clientSecret;
      }
    } else {
      const entered = await promptDingTalkCredentials(prompter);
      clientId = entered.clientId;
      clientSecret = entered.clientSecret;
    }

    if (clientId && clientSecret) {
      next = {
        ...next,
        channels: {
          ...next.channels,
          dingtalk: {
            ...next.channels?.dingtalk,
            enabled: true,
            clientId,
            clientSecret,
          },
        },
      };
    }

    // Group policy
    const groupPolicy = await prompter.select({
      message: "Group chat policy",
      options: [
        { value: "allowlist", label: "Allowlist - only respond in specific groups" },
        { value: "open", label: "Open - respond in all groups (requires mention)" },
        { value: "disabled", label: "Disabled - don't respond in groups" },
      ],
      initialValue: (next.channels?.dingtalk as DingTalkConfig | undefined)?.groupPolicy ?? "allowlist",
    });
    if (groupPolicy) {
      next = setDingTalkGroupPolicy(next, groupPolicy as "open" | "allowlist" | "disabled");
    }

    // Group allowlist if needed
    if (groupPolicy === "allowlist") {
      const existing = (next.channels?.dingtalk as DingTalkConfig | undefined)?.groupAllowFrom ?? [];
      const entry = await prompter.text({
        message: "Group chat allowlist (chat IDs or openConversationId)",
        placeholder: "cidxxxxx, cidyyyyy",
        initialValue: existing.length > 0 ? existing.map(String).join(", ") : undefined,
      });
      if (entry) {
        const parts = parseAllowFromInput(String(entry));
        if (parts.length > 0) {
          next = setDingTalkGroupAllowFrom(next, parts);
        }
      }
    }

    // Webhook configuration (optional)
    const useWebhook = await prompter.confirm({
      message: "Configure webhook URL for group robot? (optional)",
      initialValue: false,
    });
    
    if (useWebhook) {
      const webhookUrl = await prompter.text({
        message: "Webhook URL",
        placeholder: "https://oapi.dingtalk.com/robot/send?access_token=xxxxx",
      });
      const webhookSecret = await prompter.text({
        message: "Webhook Secret (for signature verification, optional)",
        placeholder: "SECxxxxx",
      });
      
      next = {
        ...next,
        channels: {
          ...next.channels,
          dingtalk: {
            ...next.channels?.dingtalk,
            webhookUrl: webhookUrl || undefined,
            webhookSecret: webhookSecret || undefined,
          },
        },
      };
    }

    return { cfg: next, accountId: DEFAULT_ACCOUNT_ID };
  },

  dmPolicy,

  disable: (cfg) => ({
    ...cfg,
    channels: {
      ...cfg.channels,
      dingtalk: { ...cfg.channels?.dingtalk, enabled: false },
    },
  }),
};
