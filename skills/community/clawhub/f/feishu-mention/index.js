/**
 * FeishuMentionResolver - Feishu @Mention Resolver
 * 
 * Supports resolving @mentions to <at> tags using:
 * 1. Configured Bots (Priority 1)
 * 2. User Aliases (Priority 2)
 * 3. Group Members (Priority 3 - Cached/API)
 */

import fs from 'fs';
import path from 'path';
import crypto from 'crypto';
import https from 'https';

// Global log switch
const DEBUG_LOG = process.env.DEBUG === 'true';

function log(level, ...args) {
  if (DEBUG_LOG || level === 'ERROR') {
    const timestamp = new Date().toISOString();
    const msg = `[${timestamp}] [FeishuMention ${level}] ${args.map(a => typeof a === 'object' ? JSON.stringify(a) : a).join(' ')}`;
    console.log(msg);
  }
}

export class FeishuMentionResolver {
  constructor(cacheDir, options = {}) {
    this.cacheDir = cacheDir || path.join(
      process.env.HOME || process.env.USERPROFILE,
      '.openclaw',
      'workspace',
      'cache',
      'feishu_mentions'
    );
    
    if (!fs.existsSync(this.cacheDir)) {
      fs.mkdirSync(this.cacheDir, { recursive: true });
    }
    
    this.cacheTTL = 2 * 60 * 60 * 1000; // 2 hours
    this.memoryCache = new Map(); // For group members
    this.tokenCache = new Map(); // appId -> { token, expireTime }
    this.botInfos = []; // Array of { name, open_id, appId, accountId }
    
    // Legacy support
    this.staticMappings = options.staticMappings || {};
    this.userAliases = options.aliases || [];
    
    // Load config
    this.accountsConfig = this._getOpenClawConfig();
    
    // Initialize bots info (async, but we trigger it)
    this._ensureBotInfos().catch(err => log('ERROR', 'Failed to ensure bot infos:', err.message));
  }
  
  _getOpenClawConfig() {
    try {
      const configPath = path.join(process.env.HOME || process.env.USERPROFILE, '.openclaw', 'openclaw.json');
      if (fs.existsSync(configPath)) {
        const content = fs.readFileSync(configPath, 'utf8');
        const config = JSON.parse(content);
        return config?.channels?.feishu?.accounts || {};
      }
    } catch (error) {
      log('ERROR', 'Failed to load OpenClaw config:', error.message);
    }
    return {};
  }
  
  async _ensureBotInfos() {
    const botCacheFile = path.join(this.cacheDir, 'bots_info.json');
    
    // Try to load from disk first
    if (fs.existsSync(botCacheFile)) {
      try {
        const cached = JSON.parse(fs.readFileSync(botCacheFile, 'utf8'));
        if (Date.now() - cached.updated_at < 24 * 60 * 60 * 1000) { // 24 hours cache for bots
          this.botInfos = cached.data;
          // log('INFO', `Loaded ${this.botInfos.length} bots from cache`);
          return;
        }
      } catch (e) {
        log('WARN', 'Failed to read bot cache, refreshing...');
      }
    }

    // Fetch from API
    // We only need to fetch for accounts that have credentials
    const promises = Object.entries(this.accountsConfig).map(async ([accountId, config]) => {
      if (!config.appId || !config.appSecret) return null;
      try {
        const token = await this._getTenantAccessToken(config.appId, config.appSecret);
        if (!token) return null;
        
        const res = await fetch('https://open.feishu.cn/open-apis/bot/v3/info', {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        const data = await res.json();
        if (data.code === 0 && data.bot) {
          return {
            name: data.bot.app_name,
            open_id: data.bot.open_id, // This is usually the bot's open_id
            appId: config.appId,
            accountId: accountId
          };
        }
      } catch (e) {
        log('ERROR', `Failed to fetch bot info for ${accountId}:`, e.message);
      }
      return null;
    });

    const results = await Promise.all(promises);
    this.botInfos = results.filter(r => r !== null);
    
    // Save to cache
    fs.writeFileSync(botCacheFile, JSON.stringify({
      updated_at: Date.now(),
      data: this.botInfos
    }, null, 2));
    
    // log('INFO', `Refreshed bot info for ${this.botInfos.length} bots`);
  }

  _getCacheFile(appId, chatId) {
    const cacheKey = `${appId}_${chatId}`;
    const hash = crypto.createHash('md5').update(cacheKey).digest('hex').substring(0, 16);
    return path.join(this.cacheDir, `${hash}.json`);
  }
  
  async _getTenantAccessToken(appId, appSecret) {
    const cache = this.tokenCache.get(appId);
    if (cache && Date.now() < cache.expireTime) {
      return cache.token;
    }

    try {
      const response = await fetch('https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json; charset=utf-8' },
        body: JSON.stringify({ app_id: appId, app_secret: appSecret })
      });
      const data = await response.json();
      if (data.code === 0) {
        const expireTime = Date.now() + (data.expire - 300) * 1000;
        this.tokenCache.set(appId, { token: data.tenant_access_token, expireTime });
        return data.tenant_access_token;
      }
    } catch (error) {
      log('ERROR', `Get token failed for ${appId}:`, error.message);
    }
    return null;
  }

  async fetchMembersFromApi(appId, appSecret, chatId) {
    const token = await this._getTenantAccessToken(appId, appSecret);
    if (!token) return [];

    const members = [];
    let pageToken = '';
    let hasMore = true;

    try {
      while (hasMore) {
        const url = new URL(`https://open.feishu.cn/open-apis/im/v1/chats/${chatId}/members`);
        url.searchParams.append('member_id_type', 'open_id');
        if (pageToken) url.searchParams.append('page_token', pageToken);

        const response = await fetch(url.toString(), {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        const data = await response.json();
        
        if (data.code !== 0) {
          log('WARN', `Fetch members failed: ${data.msg}`);
          break;
        }
        
        if (data.data?.items) members.push(...data.data.items);
        hasMore = data.data?.has_more;
        pageToken = data.data?.page_token;
      }
    } catch (error) {
      log('ERROR', 'API fetch members error:', error.message);
    }
    return members;
  }

  getCachedMembers(appId, chatId) {
    const key = `${appId}_${chatId}`;
    if (this.memoryCache.has(key)) return this.memoryCache.get(key);

    const cacheFile = this._getCacheFile(appId, chatId);
    if (fs.existsSync(cacheFile)) {
      try {
        const data = JSON.parse(fs.readFileSync(cacheFile, 'utf8'));
        if (Date.now() - data.updated_at < this.cacheTTL) {
          this.memoryCache.set(key, data.members_data);
          return data.members_data;
        }
      } catch (e) { /* ignore */ }
    }
    return null;
  }

  buildMentionTag(name, openId) {
    return `<at user_id="${openId}">${name}</at>`;
  }

  async resolveMention(mention, accountId, chatId) {
    // Return early if already in <at> format
    if (/<at\s+user_id=".*?".*?>.*?<\/at>/.test(mention)) return mention;

    const nameMatch = mention.match(/^@(.*?)$/);
    if (!nameMatch) return mention;
    
    const name = nameMatch[1];
    if (name.toLowerCase() === 'all' || name === '所有人') return `<at user_id="all">所有人</at>`;

    // 1. Check Configured Bots
    // Refresh bots info if we find a potential bot mention but cache is empty
    if (this.botInfos.length === 0) await this._ensureBotInfos();
    
    // Check against Bot Name (case-insensitive) OR Account ID (case-insensitive)
    const lowerName = name.toLowerCase();
    const bot = this.botInfos.find(b => 
      b.name.toLowerCase() === lowerName || 
      b.accountId.toLowerCase() === lowerName
    );
    
    if (bot) return this.buildMentionTag(name, bot.open_id);

    // 2. Check Aliases
    const alias = this.userAliases.find(a => a.name === name || a.alias.includes(name));
    if (alias) {
      // Recursive resolve for the real name
      return this.resolveMention(`@${alias.name}`, accountId, chatId);
    }

    // 3. Check Members (Cache -> API)
    // We need the accountId to know which app credentials to use for fetching members
    const accountConfig = this.accountsConfig[accountId];
    if (!accountConfig) {
      log('WARN', `Account ID '${accountId}' not found in config.`);
      return mention;
    }
    const { appId, appSecret } = accountConfig;

    let members = this.getCachedMembers(appId, chatId);
    let matchedMember = members?.find(m => m.name === name);

    if (!matchedMember) {
      // Fetch from API
      const newMembers = await this.fetchMembersFromApi(appId, appSecret, chatId);
      if (newMembers.length > 0) {
        this.saveCache(appId, chatId, newMembers);
        matchedMember = newMembers.find(m => m.name === name);
      }
    }

    if (matchedMember) {
      return this.buildMentionTag(name, matchedMember.open_id || matchedMember.member_id);
    }

    return mention;
  }

  async resolveTextMentions(text, accountId, chatId) {
    if (!text || !text.includes('@')) return text;

    // Normalize chatId (remove 'chat:' prefix if present)
    const normalizedChatId = chatId ? chatId.replace(/^chat:/, '') : chatId;

    // Ensure bots info is loaded
    if (this.botInfos.length === 0) await this._ensureBotInfos();

    const pattern = /(?<!:)(@[^\s:,。\!?；:\'".,!?;]+)/g;
    const matches = [...text.matchAll(pattern)];
    
    if (matches.length === 0) return text;

    let result = text;
    // Process in reverse to avoid index shifting
    for (let i = matches.length - 1; i >= 0; i--) {
      const match = matches[i];
      const fullMatch = match[0];
      
      // Skip if part of existing tag
      if (/<at\s+user_id=".*?".*?>.*?<\/at>/.test(fullMatch)) continue;

      const resolved = await this.resolveMention(fullMatch, accountId, normalizedChatId);
      if (resolved !== fullMatch) {
         result = result.substring(0, match.index) + resolved + result.substring(match.index + fullMatch.length);
      }
    }
    
    return result;
  }

  saveCache(appId, chatId, membersData) {
    const cacheFile = this._getCacheFile(appId, chatId);
    fs.writeFileSync(cacheFile, JSON.stringify({
      updated_at: Date.now(),
      members_data: membersData
    }, null, 2));
    this.memoryCache.set(`${appId}_${chatId}`, membersData);
  }
  
  invalidateCache(appId, chatId) {
    const cacheFile = this._getCacheFile(appId, chatId);
    if (fs.existsSync(cacheFile)) fs.unlinkSync(cacheFile);
    this.memoryCache.delete(`${appId}_${chatId}`);
  }
  
  clearAllCache() {
    if (fs.existsSync(this.cacheDir)) {
      fs.readdirSync(this.cacheDir).forEach(file => {
        if (file.endsWith('.json')) fs.unlinkSync(path.join(this.cacheDir, file));
      });
    }
    this.memoryCache.clear();
  }
}

// Global instance
const globalResolver = new FeishuMentionResolver();

// Exported functions
export async function resolve(text, accountId, chatId, options = {}) {
  // options can still override aliases, but staticMappings are deprecated in favor of config
  if (options.aliases) {
      // In a real implementation we might merge, but for now we rely on global config
  }
  return await globalResolver.resolveTextMentions(text, accountId, chatId);
}

export function getCached(appId, chatId) {
  return globalResolver.getCachedMembers(appId, chatId);
}

export function clearCache(appId, chatId) {
  globalResolver.invalidateCache(appId, chatId);
}

// Stubs for backward compatibility
export function addStaticMapping() {}
export function addBotMapping() {}
export function addUserAlias(realName, aliases) {
   globalResolver.userAliases.push({ name: realName, alias: aliases });
}
export async function saveBotConfig() {}
export async function loadBotConfig() {}
