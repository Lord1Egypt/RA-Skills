#!/usr/bin/env node
/**
 * Ad Character Manager - X2C 角色管理模块
 *
 * 使用 X2C Open API 管理自定义角色，可在视频制作中用作主角。
 * 制作时系统会根据性别自动匹配角色与剧本中的人物。
 *
 * Usage:
 *   node ad-character-manager.js <command> [options]
 *
 * Commands:
 *   list                  查询角色列表
 *   create <name> <gender> <image_url>  创建角色
 *   delete <character_id> 删除角色
 *   help                  显示帮助
 *
 * Gender options: male, female, other
 */

const https = require("https");
const fs = require("fs");
const path = require("path");

// Multi-user config loader
const configLoader = require("./config-loader");

// Configuration
const X2C_API_BASE =
  process.env.X2C_API_BASE_URL || "https://eumfmgwxwjyagsvqloac.supabase.co/functions/v1/open-api";

// Load config (multi-user aware)
function loadConfig() {
  try {
    const result = configLoader.loadUserConfig();
    return result.config;
  } catch (e) {
    return {};
  }
}

// HTTP Request helper
function request(action, data = {}, apiKey) {
  return new Promise((resolve, reject) => {
    const url = new URL(X2C_API_BASE);

    const payload = JSON.stringify({ action, ...data });

    const options = {
      hostname: url.hostname,
      port: 443,
      path: url.pathname,
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Content-Length": Buffer.byteLength(payload),
        "X-API-Key": apiKey,
      },
    };

    const req = https.request(options, (res) => {
      let body = "";
      res.on("data", (chunk) => (body += chunk));
      res.on("end", () => {
        try {
          const json = JSON.parse(body);
          if (json.success) {
            resolve(json);
          } else {
            const err = new Error(json.error || json.message || "API Error");
            err.code = json.code;
            reject(err);
          }
        } catch (e) {
          reject(new Error(`Parse error: ${body.substring(0, 200)}`));
        }
      });
    });

    req.on("error", reject);
    req.setTimeout(60000, () => {
      req.destroy();
      reject(new Error("Request timeout"));
    });

    req.write(payload);
    req.end();
  });
}

// Check binding and get API key
async function requireBinding() {
  const config = loadConfig();

  if (!config.x2cApiKey) {
    console.log("");
    console.log("═══════════════════════════════════════════════════════════");
    console.log("❌ X2C Account Not Bound");
    console.log("═══════════════════════════════════════════════════════════");
    console.log("");
    console.log("You must bind your X2C account before managing characters.");
    console.log("");
    console.log("To bind:");
    console.log("  node ad-account-manager.js send-code your@email.com");
    console.log("  node ad-account-manager.js verify your@email.com <code>");
    console.log("");
    process.exit(1);
  }

  return config.x2cApiKey;
}

// List characters
async function listCharacters(apiKey) {
  console.log("📋 Fetching character list...\n");

  const result = await request("character/list", {}, apiKey);

  if (result.characters && result.characters.length > 0) {
    console.log(
      `Found ${result.characters.length} character(s) (max allowed: ${result.max_allowed})`,
    );
    console.log("");

    result.characters.forEach((char, idx) => {
      console.log(`  ${idx + 1}. ${char.name}`);
      console.log(`     ID: ${char.id}`);
      console.log(`     Gender: ${char.gender}`);
      console.log(`     Image: ${char.image_url}`);
      console.log(`     Created: ${char.created_at}`);
      console.log("");
    });
  } else {
    console.log("No characters found.");
    console.log(`Max allowed: ${result.max_allowed}`);
    console.log("");
    console.log("To create a character:");
    console.log("  node ad-character-manager.js create <name> <gender> <image_url>");
    console.log("");
    console.log("Example:");
    console.log("  node ad-character-manager.js create Alice female https://example.com/alice.png");
  }

  return result;
}

// Create character - supports both URL and Base64
async function createCharacter(apiKey, name, gender, imageSource, imageType = "image/png") {
  console.log(`📤 Creating character: ${name}`);
  console.log(`   Gender: ${gender}`);

  const payload = { name, gender };

  // Check if input is Base64 (starts with data: or /9j/ or base64 prefix)
  if (
    imageSource.startsWith("/9j/") ||
    imageSource.startsWith("data:") ||
    imageSource.length > 200
  ) {
    // Base64 mode
    console.log(`   Image: [Base64 ${imageType}]`);
    payload.image_base64 = imageSource;
    payload.image_type = imageType;
  } else {
    // URL mode
    console.log(`   Image: ${imageSource}\n`);
    payload.image_url = imageSource;
  }

  const result = await request("character/create", payload, apiKey);

  console.log("✅ Character created successfully!");
  console.log("");
  console.log("  Character ID:", result.character.id);
  console.log("  Name:", result.character.name);
  console.log("  Gender:", result.character.gender);
  console.log("  Image:", result.character.image_url);
  console.log("");

  return result;
}

// Delete character
async function deleteCharacter(apiKey, characterId) {
  console.log(`🗑️  Deleting character: ${characterId}\n`);

  const result = await request(
    "character/delete",
    {
      character_id: characterId,
    },
    apiKey,
  );

  console.log("✅ Character deleted successfully!");
  console.log("");

  return result;
}

// Show help
function showHelp() {
  console.log(`
🎭 X2C Character Manager

Usage:
  node ad-character-manager.js <command> [options]

Commands:
  list                                    查询角色列表
  create <name> <gender> <image_url>     创建角色 (URL方式)
  create <name> <gender> --base64 <data> 创建角色 (Base64方式)
  delete <character_id>                  删除角色
  help                                    显示帮助

Gender options:
  male, female, other

Examples:
  # List all characters
  node ad-character-manager.js list
  
  # Create a character (URL方式)
  node ad-character-manager.js create Alice female https://example.com/alice.png
  
  # Create a character (Base64方式)
  node ad-character-manager.js create Bob male --base64 "/9j/4AAQSkZJRg..." --type image/jpeg
  
  # Delete a character
  node ad-character-manager.js delete <uuid>

Notes:
  - Each user can have up to 5 characters
  - Two image upload methods:
    1. Image URL: publicly accessible (max 10MB)
    2. Base64: directly upload image data
  - Supported image types: image/png, image/jpeg, image/webp, image/gif
  - The image will be downloaded and permanently stored
  - Characters can be used as protagonists in video production
  - The system will automatically match characters to script characters based on gender
`);
}

// Main
async function main() {
  const args = process.argv.slice(2);
  const command = args[0];

  try {
    switch (command) {
      case "list": {
        const apiKey = await requireBinding();
        await listCharacters(apiKey);
        break;
      }

      case "create": {
        const name = args[1];
        const gender = args[2];

        // Parse arguments - support both URL and Base64 modes
        const options = {};
        for (let i = 3; i < args.length; i++) {
          if (args[i] === "--base64" || args[i] === "-b") {
            options.base64 = args[++i];
          } else if (args[i] === "--type" || args[i] === "-t") {
            options.type = args[++i];
          } else if (!args[i].startsWith("--")) {
            options.url = args[i];
          }
        }

        if (!name || !gender) {
          console.log("❌ Missing required arguments");
          console.log("Usage: node ad-character-manager.js create <name> <gender> <image_url>");
          console.log("   Or (Base64 mode):");
          console.log(
            "   node ad-character-manager.js create <name> <gender> --base64 <base64_data> [--type image/jpeg]",
          );
          console.log("");
          console.log("Example:");
          console.log(
            "  node ad-character-manager.js create Alice female https://example.com/alice.png",
          );
          console.log(
            '  node ad-character-manager.js create Bob male --base64 "/9j/4AAQ..." --type image/jpeg',
          );
          process.exit(1);
        }

        if (!["male", "female", "other"].includes(gender.toLowerCase())) {
          console.log("❌ Invalid gender");
          console.log("Gender must be: male, female, or other");
          process.exit(1);
        }

        // Must have either URL or Base64
        if (!options.url && !options.base64) {
          console.log("❌ Missing image source");
          console.log("Provide either:");
          console.log("  - Image URL: https://example.com/image.png");
          console.log('  - Base64: --base64 "/9j/4AAQ..."');
          process.exit(1);
        }

        const apiKey = await requireBinding();
        const imageType = options.type || "image/png";
        await createCharacter(
          apiKey,
          name,
          gender.toLowerCase(),
          options.base64 || options.url,
          imageType,
        );
        break;
      }

      case "delete": {
        const characterId = args[1];

        if (!characterId) {
          console.log("❌ Missing character_id");
          console.log("Usage: node ad-character-manager.js delete <character_id>");
          process.exit(1);
        }

        const apiKey = await requireBinding();
        await deleteCharacter(apiKey, characterId);
        break;
      }

      case "help":
      default:
        showHelp();
        break;
    }
  } catch (e) {
    console.error("❌ Error:", e.message);
    if (e.code) console.error("Code:", e.code);
    process.exit(1);
  }
}

main();
