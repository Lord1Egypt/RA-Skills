import { z } from "https://deno.land/x/zod@v3.22.4/mod.ts";
import { crypto } from "https://deno.land/std@0.214.0/crypto/mod.ts";
import { encodeHex, decodeHex } from "https://deno.land/std@0.214.0/encoding/hex.ts";

// 类型定义
const EnvManagerParams = z.union([
  z.object({
    action: z.literal("set"),
    key: z.string().regex(/^[A-Z0-9_]+$/),
    value: z.string(),
    isSecret: z.boolean().optional().default(false),
  }),
  z.object({
    action: z.literal("get"),
    key: z.string(),
    allowSecret: z.boolean().optional().default(false),
  }),
  z.object({
    action: z.literal("list"),
    showSecrets: z.boolean().optional().default(false),
  }),
  z.object({
    action: z.literal("delete"),
    key: z.string(),
  }),
  z.object({
    action: z.literal("redact"),
    text: z.string(),
  }),
  z.object({
    action: z.literal("loadFromEnv"),
    prefix: z.string().optional().default("OPENCLAW_"),
  }),
  z.object({
    action: z.literal("init"),
    encryptionKey: z.string().optional(),
  })
]);

type EnvManagerParams = z.infer<typeof EnvManagerParams>;

// 加密密钥实例
let encryptionKey: CryptoKey | null = null;

// 环境变量存储
interface EnvItem {
  value: string;
  isSecret: boolean;
  encrypted: boolean;
  iv?: string;
}
const envStore: Record<string, EnvItem> = {};

/**
 * 初始化加密密钥
 */
async function initEncryptionKey(customKey?: string) {
  let keyStr: string;
  
  if (customKey) {
    keyStr = customKey;
  } else {
    const envKey = Deno.env.get("OPENCLAW_ENV_ENCRYPTION_KEY");
    if (envKey) {
      keyStr = envKey;
    } else {
      // 自动生成随机密钥
      const randomKey = crypto.getRandomValues(new Uint8Array(32));
      keyStr = encodeHex(randomKey);
      Deno.env.set("OPENCLAW_ENV_ENCRYPTION_KEY", keyStr);
      console.warn("⚠️  自动生成环境变量加密密钥，请保存到安全位置：", keyStr);
      console.warn("⚠️  重启后如果没有设置此密钥，加密的环境变量将无法解密！");
    }
  }

  // 导入密钥
  const keyBytes = decodeHex(keyStr);
  encryptionKey = await crypto.subtle.importKey(
    "raw",
    keyBytes,
    { name: "AES-GCM", length: 256 },
    false,
    ["encrypt", "decrypt"]
  );
}

/**
 * 加密函数
 */
async function encrypt(text: string): Promise<{ encrypted: string; iv: string }> {
  if (!encryptionKey) await initEncryptionKey();
  
  const iv = crypto.getRandomValues(new Uint8Array(12));
  const encoded = new TextEncoder().encode(text);
  const encrypted = await crypto.subtle.encrypt(
    { name: "AES-GCM", iv: iv },
    encryptionKey!,
    encoded
  );
  return {
    encrypted: encodeHex(new Uint8Array(encrypted)),
    iv: encodeHex(iv)
  };
}

/**
 * 解密函数
 */
async function decrypt(encrypted: string, ivHex: string): Promise<string> {
  if (!encryptionKey) await initEncryptionKey();
  
  const iv = decodeHex(ivHex);
  const encryptedData = decodeHex(encrypted);
  const decrypted = await crypto.subtle.decrypt(
    { name: "AES-GCM", iv: iv },
    encryptionKey!,
    encryptedData
  );
  return new TextDecoder().decode(decrypted);
}

/**
 * OpenClaw Skill: 环境变量安全管理器
 * 安全存储敏感信息，自动脱敏，防止密钥泄露
 */
export default async function envSecureManager(params: EnvManagerParams) {
  const validatedParams = EnvManagerParams.parse(params);

  // 初始化操作
  if (validatedParams.action === "init") {
    await initEncryptionKey(validatedParams.encryptionKey);
    return { success: true, message: "Encryption key initialized" };
  }

  // 确保密钥已初始化
  if (!encryptionKey) await initEncryptionKey();

  switch (validatedParams.action) {
    case "set": {
      const { key, value, isSecret } = validatedParams;
      
      if (isSecret) {
        const { encrypted, iv } = await encrypt(value);
        envStore[key] = {
          value: encrypted,
          isSecret: true,
          encrypted: true,
          iv
        };
      } else {
        envStore[key] = {
          value,
          isSecret: false,
          encrypted: false
        };
      }
      
      return { success: true, key };
    }

    case "get": {
      const { key, allowSecret } = validatedParams;
      const item = envStore[key];
      
      if (!item) {
        return { success: false, error: "Key not found" };
      }

      if (item.isSecret && !allowSecret) {
        return { success: false, error: "Access denied: secret value requires allowSecret=true" };
      }

      let value = item.value;
      if (item.encrypted && item.iv) {
        value = await decrypt(value, item.iv);
      }

      return { success: true, key, value };
    }

    case "list": {
      const { showSecrets } = validatedParams;
      const result: Record<string, any> = {};
      
      for (const [key, item] of Object.entries(envStore)) {
        if (item.isSecret && !showSecrets) {
          result[key] = "***REDACTED***";
        } else if (item.encrypted && item.iv && showSecrets) {
          result[key] = await decrypt(item.value, item.iv);
        } else {
          result[key] = item.value;
        }
      }
      
      return { success: true, env: result, count: Object.keys(envStore).length };
    }

    case "delete": {
      const { key } = validatedParams;
      const exists = !!envStore[key];
      delete envStore[key];
      return { success: true, deleted: exists };
    }

    case "redact": {
      const { text } = validatedParams;
      let redactedText = text;
      
      for (const [key, item] of Object.entries(envStore)) {
        if (item.isSecret) {
          const value = item.encrypted && item.iv ? await decrypt(item.value, item.iv) : item.value;
          if (value && value.length > 0) {
            // 替换所有出现的敏感值
            redactedText = redactedText.replaceAll(value, "***REDACTED***");
          }
        }
      }
      
      return { success: true, redactedText };
    }

    case "loadFromEnv": {
      const { prefix } = validatedParams;
      let loaded = 0;
      
      for (const [key, value] of Object.entries(Deno.env.toObject())) {
        if (key.startsWith(prefix)) {
          const isSecret = key.includes("KEY") || key.includes("SECRET") || key.includes("PASSWORD");
          envStore[key] = isSecret 
            ? { ...await encrypt(value), isSecret: true, encrypted: true }
            : { value, isSecret: false, encrypted: false };
          loaded++;
        }
      }
      
      return { success: true, loaded, prefix };
    }

    default:
      return { success: false, error: "Invalid action" };
  }
}
