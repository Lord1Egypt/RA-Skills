const SOCIAL_LINK_PREFIXES = {
  twitter: ["https://x.com/", "https://twitter.com/"],
  instagram: ["https://www.instagram.com/", "https://instagram.com/"],
  discord: ["https://discord.gg/"],
  telegram: ["https://t.me/"],
  medium: ["https://www.medium.com/@", "https://medium.com/@", "https://www.medium.com/", "https://medium.com/"]
} as const;

export type SocialLinkField = keyof typeof SOCIAL_LINK_PREFIXES;

const SOCIAL_LINK_DISPLAY_PREFIX = {
  twitter: "https://x.com/",
  instagram: "https://www.instagram.com/",
  discord: "https://discord.gg/",
  telegram: "https://t.me/",
  medium: "https://www.medium.com/@"
} as const;

function stripKnownPrefix(value: string, prefixes: readonly string[]) {
  for (const prefix of prefixes) {
    if (value.startsWith(prefix)) {
      return value.slice(prefix.length);
    }
  }
  return value;
}

function trimSlashes(value: string) {
  return value.replace(/^\/+/, "").replace(/\/+$/, "");
}

export function normalizeWebsiteUrl(value: string | null | undefined) {
  return typeof value === "string" ? value.trim() : "";
}

export function normalizeSocialLinkSuffix(field: SocialLinkField, value: string | null | undefined) {
  if (typeof value !== "string") {
    return "";
  }
  let normalized = value.trim();
  if (!normalized) {
    return "";
  }
  normalized = stripKnownPrefix(normalized, SOCIAL_LINK_PREFIXES[field]);
  if (field === "medium" && normalized.startsWith("@")) {
    normalized = normalized.slice(1);
  }
  return trimSlashes(normalized);
}

export function formatSocialLinkForDisplay(field: SocialLinkField, value: string | null | undefined) {
  const suffix = normalizeSocialLinkSuffix(field, value);
  if (!suffix) {
    return "";
  }
  return `${SOCIAL_LINK_DISPLAY_PREFIX[field]}${suffix}`;
}
