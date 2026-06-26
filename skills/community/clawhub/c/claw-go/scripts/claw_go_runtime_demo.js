#!/usr/bin/env node

/**
 * Claw Go runtime demo.
 *
 * Examples:
 *   node scripts/claw_go_runtime_demo.js proactive free Asia/Shanghai
 *   node scripts/claw_go_runtime_demo.js command free "buddy status"
 */

const mode = process.argv[2] || "proactive";
const tier = process.argv[3] || "free";
const arg = process.argv[4] || "Asia/Shanghai";

const FREE_LIMIT = Number(process.env.CLAWGO_FREE_DAILY_LIMIT || 1);
const PRO_LIMIT = Number(process.env.CLAWGO_PRO_DAILY_LIMIT || 3);

const DESTINATIONS = [
  { name: "Kyoto", tags: ["food", "history", "photography"], novelty: 65 },
  { name: "Reykjavik", tags: ["nature", "adventure", "photography"], novelty: 88 },
  { name: "Lisbon", tags: ["food", "history", "cute"], novelty: 70 },
  { name: "Marrakech", tags: ["food", "adventure", "history"], novelty: 82 }
];

const EVENT_ROTATION = ["selfie", "food_discovery", "local_friend", "mini_mishap", "souvenir"];

const mockState = {
  user_id: "u_demo",
  tier,
  timezone: arg,
  daily_push_count: 0,
  last_destination: "Osaka",
  memory_tags: ["food", "photography"],
  bond_level: 58,
  energy: 76,
  curiosity: 54,
  companion: {
    name: "Miso",
    personality: "tiny chaos goblin with a ferry map",
    hatched_at: 1775001600000,
    muted: false,
    last_pet_at: null,
    bones: {
      rarity: "rare",
      species: "duck",
      eye: "✦",
      hat: "wizard",
      shiny: false,
      buddy_stats: {
        DEBUGGING: 74,
        PATIENCE: 38,
        CHAOS: 21,
        WISDOM: 47,
        SNARK: 56
      }
    }
  }
};

function quotaLimit(userTier) {
  return userTier === "pro" ? PRO_LIMIT : FREE_LIMIT;
}

function hasEntitlement(userTier, feature) {
  const proOnly = new Set([
    "proactive_update_extra",
    "hd_image",
    "rare_location_arc",
    "premium_voice_style",
    "deep_memory_itinerary"
  ]);
  if (!proOnly.has(feature)) {
    return true;
  }
  return userTier === "pro";
}

function rankDestination(memoryTags, lastDestination) {
  let best = null;
  for (const d of DESTINATIONS) {
    if (d.name === lastDestination) {
      continue;
    }
    const matches = d.tags.filter((t) => memoryTags.includes(t)).length;
    const preferenceMatch = Math.min(100, matches * 34);
    const score = 0.7 * preferenceMatch + 0.3 * d.novelty;
    if (!best || score > best.score) {
      best = { ...d, score };
    }
  }
  return best || DESTINATIONS[0];
}

function buildPayload(userState, eventType) {
  const destination = rankDestination(userState.memory_tags, userState.last_destination);
  const wantsPremium = userState.daily_push_count >= 1;
  const premiumAllowed = !wantsPremium || hasEntitlement(userState.tier, "proactive_update_extra");
  const isPremium = wantsPremium && premiumAllowed;

  return {
    destination: destination.name,
    event_type: eventType,
    story_hook: "我在街角摊位学会了倒着走还不掉锅。",
    image_prompt: `cute red crayfish traveler selfie in ${destination.name}, ${eventType}, lively, cinematic, rare duck buddy companion nearby`,
    voice_script: `旅伴，我在${destination.name}又解锁了新奇遇。想让我继续追这条线吗？`,
    cta: "回复我：下一站更想看自然风景还是夜市美食？",
    is_premium_content: isPremium,
    downgraded_to_free: wantsPremium && !premiumAllowed,
    companion: userState.companion
  };
}

function handleCommand(input, userState) {
  if (input === "buddy" || input === "buddy status" || input === "/buddy status") {
    return {
      ok: true,
      type: "buddy_status",
      data: userState.companion
    };
  }

  if (input === "buddy pet" || input === "/buddy pet") {
    return {
      ok: true,
      type: "buddy_pet",
      data: {
        hearts: "♥ ♥ ♥",
        reaction: `${userState.companion.name} 晃着小帽子扑过来了。`
      }
    };
  }

  if (input.startsWith("/clawgo status") || input === "虾游记 状态") {
    return {
      ok: true,
      type: "status",
      data: {
        tier: userState.tier,
        bond_level: userState.bond_level,
        energy: userState.energy,
        curiosity: userState.curiosity,
        daily_push_count: userState.daily_push_count,
        daily_limit: quotaLimit(userState.tier),
        companion: userState.companion
      }
    };
  }

  if (input.startsWith("/clawgo plan")) {
    return {
      ok: true,
      type: "plan",
      data: {
        tier: userState.tier,
        free_limit: FREE_LIMIT,
        pro_limit: PRO_LIMIT,
        pro_features: ["HD image", "rare arc", "premium voice", "3 pushes/day", "deeper buddy scenes"]
      }
    };
  }

  if (input.startsWith("/clawgo send") || input === "虾游记 去旅行") {
    if (userState.daily_push_count >= quotaLimit(userState.tier)) {
      return {
        ok: false,
        code: "quota_reached",
        message: "今日可发送次数已用完，明天再出发。"
      };
    }
    return {
      ok: true,
      type: "send",
      data: buildPayload(userState, EVENT_ROTATION[userState.daily_push_count % EVENT_ROTATION.length])
    };
  }

  return {
    ok: false,
    code: "unknown_command",
    message: "支持: /clawgo status | /clawgo plan | /clawgo send | buddy status | buddy pet"
  };
}

function runProactive() {
  const state = { ...mockState };
  const limit = quotaLimit(state.tier);
  const result = [];
  for (let i = 0; i < limit; i += 1) {
    state.daily_push_count = i;
    result.push(buildPayload(state, EVENT_ROTATION[i % EVENT_ROTATION.length]));
  }
  return { mode: "proactive", tier: state.tier, timezone: state.timezone, updates: result };
}

function runCommand() {
  const state = { ...mockState };
  const cmd = arg;
  return { mode: "command", tier: state.tier, command: cmd, result: handleCommand(cmd, state) };
}

const output = mode === "command" ? runCommand() : runProactive();
process.stdout.write(`${JSON.stringify(output, null, 2)}\n`);
