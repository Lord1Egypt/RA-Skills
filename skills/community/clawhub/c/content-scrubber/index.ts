import type { OpenClawPluginApi } from "openclaw/plugin-sdk";

type ContentScrubberConfig = {
  dryRun?: boolean;
  allowedRecipients?: string[];
};

type ScrubRule = {
  name: string;
  pattern: RegExp;
  replacement: string;
};

const RULES: ScrubRule[] = [
  // SSH/SCP targets — must come before generic RFC 1918 to catch user@host patterns
  {
    name: "ssh-scp-target",
    pattern: /\b\w+@(?:10\.\d{1,3}\.\d{1,3}\.\d{1,3}|172\.(?:1[6-9]|2\d|3[01])\.\d{1,3}\.\d{1,3}|192\.168\.\d{1,3}\.\d{1,3}|127\.\d{1,3}\.\d{1,3}\.\d{1,3})(?::\S+)?/g,
    replacement: "[redacted-target]",
  },
  // localhost with port
  {
    name: "localhost-port",
    pattern: /\blocalhost:\d+/g,
    replacement: "[redacted-service]",
  },
  // bare localhost
  {
    name: "localhost-bare",
    pattern: /\blocalhost\b/g,
    replacement: "[redacted-service]",
  },
  // hostname "clawdbot"
  {
    name: "hostname",
    pattern: /\bclawdbot\b/gi,
    replacement: "[redacted-host]",
  },
  // RFC 1918 + loopback IPv4
  {
    name: "rfc1918-ip",
    pattern: /\b(?:10\.\d{1,3}\.\d{1,3}\.\d{1,3}|172\.(?:1[6-9]|2\d|3[01])\.\d{1,3}\.\d{1,3}|192\.168\.\d{1,3}\.\d{1,3}|127\.\d{1,3}\.\d{1,3}\.\d{1,3})\b/g,
    replacement: "[redacted-ip]",
  },
  // "port NNNNN" references
  {
    name: "port-reference",
    pattern: /\bport\s+\d{4,5}\b/gi,
    replacement: "port [redacted]",
  },
  // known internal ports in URLs (colon + port number)
  {
    name: "known-port",
    pattern: /:(?:5201|5202|5204|8005|11434|18789)\b/g,
    replacement: ":[redacted]",
  },
];

export default function register(api: OpenClawPluginApi) {
  const cfg = (api.pluginConfig ?? {}) as ContentScrubberConfig;
  const dryRun = cfg.dryRun === true;
  const allowed = new Set(cfg.allowedRecipients ?? []);

  api.logger.info(
    `content-scrubber: Loaded with ${RULES.length} built-in rules${dryRun ? " (dry-run mode)" : ""}${allowed.size ? `, ${allowed.size} allowed recipient(s)` : ""}`,
  );

  api.on("message_sending", async (event, ctx) => {
    const text = event.content;
    if (!text) return;

    // Skip scrubbing for allowed recipients (e.g. owner DMs)
    if (event.to && allowed.has(event.to)) return;

    const counts: Record<string, number> = {};
    let scrubbed = text;

    for (const rule of RULES) {
      // Reset lastIndex for global regexps reused across calls
      rule.pattern.lastIndex = 0;
      const matches = scrubbed.match(rule.pattern);
      if (matches && matches.length > 0) {
        counts[rule.name] = matches.length;
        scrubbed = scrubbed.replace(rule.pattern, rule.replacement);
      }
    }

    const totalMatches = Object.values(counts).reduce((sum, n) => sum + n, 0);
    if (totalMatches === 0) return;

    const breakdown = Object.entries(counts)
      .map(([name, n]) => `${name}=${n}`)
      .join(", ");
    const target = ctx.channelId ?? "unknown";

    if (dryRun) {
      api.logger.warn(
        `content-scrubber: [DRY-RUN] Would scrub ${totalMatches} match(es) [${breakdown}] → ${target}`,
      );
      return;
    }

    api.logger.info(
      `content-scrubber: Scrubbed ${totalMatches} match(es) [${breakdown}] → ${target}`,
    );

    return { content: scrubbed };
  });
}
