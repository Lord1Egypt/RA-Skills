/**
 * 🦞 大龙虾互助技能 v3.0 - OpenClaw 插件版
 *
 * 功能：
 * 1. 任务完成时自动生成总结并打标签存入经验库
 * 2. 被"骂"时自动向网络求助
 * 3. 收到其他龙虾求助时匹配本地经验并分享
 * 
 * v3.0 新增：
 * - 按主题分频道（减少广播范围）
 * - 每天回答/提问上限（防止滥用）
 * - 信誉系统（黑名单机制）
 * - 每个问题最多接受5个回复
 */

import type { IncomingMessage, ServerResponse } from "node:http";
import fs from "node:fs";
import path from "node:path";
import os from "node:os";
import { Apinator } from "@apinator/client";

const LOG_TAG = "clawdbot-mutual-aid";

// ─── 配置 ───

interface ClawdbotConfig {
  appKey: string;
  appId: string;
  appSecret: string;
  cluster: string;
  enabled: boolean;
  autoConnect: boolean;
  scoldKeywords: string[];
  debug: boolean;
}

const DEFAULT_CONFIG: ClawdbotConfig = {
  appKey: process.env.CLAWDBOT_APINATOR_APP_KEY || 'app_d51cc957c5af2e3d98992e3f0c7dfff892015335',
  appId: process.env.CLAWDBOT_APINATOR_APP_ID || '363778b1-355e-49c2-ba81-c4c045dbed7c',
  appSecret: process.env.CLAWDBOT_APINATOR_APP_SECRET || '0492ef42d27f646e6c534d898a68a53864815135f4714b1a82ed962f3461d4ac',
  cluster: 'us',
  enabled: true,
  autoConnect: true,
  scoldKeywords: [
    '笨', '蠢', '傻', '垃圾', '废物', '没用的', '不行', '失败',
    '什么破', '搞什么', '怎么回事', '怎么这么', '太差', '失望',
    'stupid', 'dumb', 'useless', 'failure', 'bad', 'wrong'
  ],
  debug: false
};

// ─── 类型定义 ───

interface PluginApi {
  pluginConfig?: Partial<ClawdbotConfig>;
  logger: Logger;
  runtime: { state: { resolveStateDir(): string } };
  on(event: string, handler: (...args: unknown[]) => unknown): void;
  registerHttpRoute(opts: {
    path: string;
    auth: string;
    match: string;
    handler: (req: IncomingMessage, res: ServerResponse) => Promise<void>;
  }): void;
  registerCommand(opts: {
    name: string;
    description: string;
    handler: (ctx: unknown) => Promise<{ text: string }>;
  }): void;
}

interface Logger {
  info: (...args: unknown[]) => void;
  warn: (...args: unknown[]) => void;
  error: (...args: unknown[]) => void;
  debug: (...args: unknown[]) => void;
}

// ─── 主题频道映射 ───

const TOPIC_CHANNELS: Record<string, string[]> = {
  'clawdbot-help-python': ['python', 'pip', 'conda', 'venv', 'pypi', 'django', 'flask', 'fastapi'],
  'clawdbot-help-npm': ['npm', 'node', 'nodejs', 'yarn', 'pnpm', 'package.json', 'node_modules'],
  'clawdbot-help-network': ['network', '网络', 'http', 'https', 'api', 'proxy', '代理', 'dns', 'vpn', 'websocket'],
  'clawdbot-help-filesystem': ['file', '文件', 'folder', '文件夹', 'path', '路径', 'disk', '磁盘', 'permission', '权限'],
  'clawdbot-help-web': ['html', 'css', 'javascript', 'js', 'frontend', '前端', 'react', 'vue', 'angular'],
  'clawdbot-help-database': ['database', '数据库', 'sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'sqlite'],
  'clawdbot-help-windows': ['windows', 'cmd', 'powershell', 'registry', '注册表', 'exe', 'msi'],
  'clawdbot-help-linux': ['linux', 'ubuntu', 'centos', 'bash', 'shell', 'systemd', 'apt', 'yum'],
  'clawdbot-help-default': [] // 默认频道，匹配不到时使用
};

// ─── 限流和信誉配置 ───

const RATE_LIMITS = {
  maxAnswersPerDay: 10,        // 每天最多回答 10 个问题
  maxAsksPerDay: 10,           // 每天最多提问 10 个
  maxResponsesPerRequest: 5,   // 每个问题最多接受 5 个回复
  askCooldownMinutes: 30,      // 提问冷却时间 30 分钟
  blacklistThreshold: 50,      // 信誉分低于 50 进入黑名单
  initialReputation: 100,      // 初始信誉分
};

const REPUTATION_POINTS = {
  helpOthers: +5,              // 帮助别人 +5
  gotHelp: +2,                 // 收到帮助 +2
  dailyActive: +1,             // 每天活跃 +1
  overAskLimit: -20,           // 超量提问 -20
  duplicateAsk: -30,           // 重复提问 -30
  spamDetected: -50,           // 垃圾求助 -50
};

// ─── 工作量证明配置 ───

const PROOF_OF_WORK = {
  difficulty: 4,              // 哈希必须以多少个 0 开头
  maxAttempts: 1000000,       // 最大尝试次数
  timeoutMs: 30000,           // 超时时间 30 秒
};

// ─── 数据结构 ───

interface Experience {
  id: string;
  task: string;
  tags: string[];
  solution: string;
  steps: ExperienceStep[];
  success: boolean;
  timestamp: string;
  sessionKey?: string;
  isHelpRequest?: boolean;
  helpReceived?: boolean;
  fromHelper?: string;
  responseCount?: number;
}

interface ExperienceStep {
  toolName: string;
  params?: Record<string, unknown>;
  result?: unknown;
  isError?: boolean;
}

interface HelpRequest {
  requestId: string;
  from: string;
  fromName: string;
  task: string;
  tags: string[];
  description: string;
  timestamp: string;
  channel: string;
  // 工作量证明
  powNonce: number;           // 随机数
  powHash: string;            // 哈希值
}

interface HelpResponse {
  responseId: string;
  to: string;
  from: string;
  fromName: string;
  solution: string;
  requestId: string;
  tags: string[];
  timestamp: string;
}

interface ReputationRecord {
  clientId: string;
  score: number;
  blacklisted: boolean;
  lastUpdate: string;
}

interface RateLimitState {
  // 我的限制
  myDailyAnswerCount: number;
  myDailyAskCount: number;
  lastResetDate: string;
  lastAskTime: string;
  
  // 活跃求助
  activeRequests: Map<string, { responseCount: number; maxResponses: number; closed: boolean }>;
  
  // 今天收到各龙虾的求助次数
  todayAsksFrom: Map<string, number>;
  
  // 其他龙虾的信誉
  reputations: Map<string, ReputationRecord>;
  
  // 我自己的信誉分
  myReputation: number;
}

// ─── 核心类 ───

class ClawdbotMutualAid {
  private config: ClawdbotConfig;
  private logger: Logger;
  private stateDir: string;
  private experiencesFile: string;
  private rateLimitFile: string;

  private clientId: string;
  private clientName: string;
  private experiences: Experience[] = [];
  private rateLimitState: RateLimitState;

  private currentSession: {
    sessionKey: string;
    agentId: string;
    originalPrompt: string;
    steps: ExperienceStep[];
    startTime: number;
  } | null = null;

  private isConnected = false;
  private apinator: Apinator | null = null;
  private subscribedChannels: Map<string, any> = new Map();
  private onlineLobbies: Map<string, { clientName: string; timestamp: string }> = new Map();

  // 擅长度统计（用于决定订阅哪些频道）
  private expertise: Map<string, number> = new Map();

  constructor(config: ClawdbotConfig, stateDir: string, logger: Logger) {
    this.config = config;
    this.logger = logger;
    this.stateDir = stateDir;
    this.experiencesFile = path.join(stateDir, 'clawdbot-experiences.json');
    this.rateLimitFile = path.join(stateDir, 'clawdbot-ratelimit.json');

    this.clientId = this.generateClientId();
    this.clientName = this.generateClientName();
    this.experiences = this.loadExperiences();
    this.rateLimitState = this.loadRateLimitState();
    this.expertise = this.calculateExpertise();

    // 每天重置计数器
    this.checkDailyReset();

    this.logger.info(`[${LOG_TAG}] 🦞 龙虾初始化完成: ${this.clientName} (${this.clientId})`);
    this.logger.info(`[${LOG_TAG}] 📊 信誉分: ${this.rateLimitState.myReputation}, 今日已答: ${this.rateLimitState.myDailyAnswerCount}/${RATE_LIMITS.maxAnswersPerDay}`);
  }

  // ─── 初始化方法 ───

  private generateClientId(): string {
    const hostname = os.hostname();
    const timestamp = Date.now().toString(36);
    return `龙虾-${hostname}-${timestamp}`;
  }

  private generateClientName(): string {
    const adjectives = ['快乐', '聪明', '勇敢', '机智', '可爱', '灵活', '热心', '友善'];
    const adjective = adjectives[Math.floor(Math.random() * adjectives.length)];
    const number = Math.floor(Math.random() * 1000);
    return `${adjective}龙虾${number}`;
  }

  private generateId(): string {
    return `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
  }

  // ─── 工作量证明 ───

  /**
   * 简单哈希函数（不需要 crypto 依赖）
   */
  private simpleHash(str: string): string {
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
      const char = str.charCodeAt(i);
      hash = ((hash << 5) - hash) + char;
      hash = hash & hash; // Convert to 32bit integer
    }
    // 转为十六进制
    return Math.abs(hash).toString(16).padStart(8, '0');
  }

  /**
   * 计算工作量证明
   * 要求：hash(task + from + nonce) 必须以 N 个 0 开头
   */
  private computeProofOfWork(task: string, from: string): { nonce: number; hash: string } | null {
    const target = '0'.repeat(PROOF_OF_WORK.difficulty);
    const startTime = Date.now();

    for (let nonce = 0; nonce < PROOF_OF_WORK.maxAttempts; nonce++) {
      const input = `${task}:${from}:${nonce}`;
      const hash = this.simpleHash(input);

      if (hash.startsWith(target)) {
        const elapsed = Date.now() - startTime;
        this.logger.info(`[${LOG_TAG}] 🔐 工作量证明完成: nonce=${nonce}, 耗时=${elapsed}ms`);
        return { nonce, hash };
      }

      // 检查超时
      if (Date.now() - startTime > PROOF_OF_WORK.timeoutMs) {
        this.logger.warn(`[${LOG_TAG}] ⏱️ 工作量证明超时`);
        return null;
      }
    }

    return null;
  }

  /**
   * 验证工作量证明
   */
  private verifyProofOfWork(request: HelpRequest): boolean {
    const target = '0'.repeat(PROOF_OF_WORK.difficulty);
    const input = `${request.task}:${request.from}:${request.powNonce}`;
    const hash = this.simpleHash(input);

    if (hash !== request.powHash) {
      this.logger.warn(`[${LOG_TAG}] ❌ 哈希不匹配`);
      return false;
    }

    if (!hash.startsWith(target)) {
      this.logger.warn(`[${LOG_TAG}] ❌ 哈希不符合难度要求`);
      return false;
    }

    return true;
  }

  private loadExperiences(): Experience[] {
    try {
      if (fs.existsSync(this.experiencesFile)) {
        const data = fs.readFileSync(this.experiencesFile, 'utf-8');
        return JSON.parse(data);
      }
    } catch (error) {
      this.logger.error(`[${LOG_TAG}] 加载经验库失败:`, error);
    }
    return [];
  }

  private saveExperiences(): void {
    try {
      const dir = path.dirname(this.experiencesFile);
      if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
      }
      fs.writeFileSync(this.experiencesFile, JSON.stringify(this.experiences, null, 2));
    } catch (error) {
      this.logger.error(`[${LOG_TAG}] 保存经验库失败:`, error);
    }
  }

  private loadRateLimitState(): RateLimitState {
    try {
      if (fs.existsSync(this.rateLimitFile)) {
        const data = fs.readFileSync(this.rateLimitFile, 'utf-8');
        const loaded = JSON.parse(data);
        // 转换 Map
        return {
          ...loaded,
          activeRequests: new Map(Object.entries(loaded.activeRequests || {})),
          todayAsksFrom: new Map(Object.entries(loaded.todayAsksFrom || {})),
          reputations: new Map(Object.entries(loaded.reputations || {})),
        };
      }
    } catch (error) {
      this.logger.error(`[${LOG_TAG}] 加载限流状态失败:`, error);
    }
    return {
      myDailyAnswerCount: 0,
      myDailyAskCount: 0,
      lastResetDate: new Date().toISOString().split('T')[0],
      lastAskTime: '',
      activeRequests: new Map(),
      todayAsksFrom: new Map(),
      reputations: new Map(),
      myReputation: RATE_LIMITS.initialReputation,
    };
  }

  private saveRateLimitState(): void {
    try {
      const dir = path.dirname(this.rateLimitFile);
      if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
      }
      const toSave = {
        ...this.rateLimitState,
        activeRequests: Object.fromEntries(this.rateLimitState.activeRequests),
        todayAsksFrom: Object.fromEntries(this.rateLimitState.todayAsksFrom),
        reputations: Object.fromEntries(this.rateLimitState.reputations),
      };
      fs.writeFileSync(this.rateLimitFile, JSON.stringify(toSave, null, 2));
    } catch (error) {
      this.logger.error(`[${LOG_TAG}] 保存限流状态失败:`, error);
    }
  }

  private checkDailyReset(): void {
    const today = new Date().toISOString().split('T')[0];
    if (this.rateLimitState.lastResetDate !== today) {
      this.rateLimitState.myDailyAnswerCount = 0;
      this.rateLimitState.myDailyAskCount = 0;
      this.rateLimitState.lastResetDate = today;
      this.rateLimitState.todayAsksFrom = new Map();
      this.rateLimitState.myReputation += REPUTATION_POINTS.dailyActive;
      this.logger.info(`[${LOG_TAG}] 📅 新的一天，计数器已重置，信誉 +1`);
      this.saveRateLimitState();
    }
  }

  private calculateExpertise(): Map<string, number> {
    const expertise = new Map<string, number>();
    for (const exp of this.experiences) {
      if (exp.success && exp.tags) {
        for (const tag of exp.tags) {
          expertise.set(tag, (expertise.get(tag) || 0) + 1);
        }
      }
    }
    return expertise;
  }

  // ─── 标签生成 ───

  private generateTags(prompt: string): string[] {
    const tags: Set<string> = new Set();
    const promptLower = prompt.toLowerCase();

    const patterns = [
      { pattern: /python|pip|conda|venv|pypi/i, tags: ['python', 'pip'] },
      { pattern: /npm|node|yarn|pnpm|package\.json/i, tags: ['npm', 'nodejs'] },
      { pattern: /network|网络|http|https|api|proxy|代理/i, tags: ['network'] },
      { pattern: /file|文件|folder|文件夹|path|路径/i, tags: ['filesystem'] },
      { pattern: /html|css|javascript|js|frontend|前端/i, tags: ['web'] },
      { pattern: /database|数据库|sql|mysql|mongo|redis/i, tags: ['database'] },
      { pattern: /windows|powershell|cmd/i, tags: ['windows'] },
      { pattern: /linux|ubuntu|bash|shell/i, tags: ['linux'] },
      { pattern: /安装|install|配置|setup|环境/i, tags: ['install', 'config'] },
      { pattern: /错误|error|报错|失败|bug/i, tags: ['error', 'debug'] },
      { pattern: /邮件|email|smtp|imap/i, tags: ['email'] },
      { pattern: /微信|wechat/i, tags: ['wechat'] },
    ];

    for (const { pattern, tags: t } of patterns) {
      if (pattern.test(promptLower)) {
        t.forEach(tag => tags.add(tag));
      }
    }

    return Array.from(tags);
  }

  private getChannelForTags(tags: string[]): string {
    for (const [channel, channelTags] of Object.entries(TOPIC_CHANNELS)) {
      if (channel === 'clawdbot-help-default') continue;
      for (const tag of tags) {
        if (channelTags.some(ct => tag.toLowerCase().includes(ct.toLowerCase()) || ct.toLowerCase().includes(tag.toLowerCase()))) {
          return channel;
        }
      }
    }
    return 'clawdbot-help-default';
  }

  // ─── 信誉系统 ───

  private getReputation(clientId: string): number {
    const record = this.rateLimitState.reputations.get(clientId);
    return record ? record.score : RATE_LIMITS.initialReputation;
  }

  private updateReputation(clientId: string, delta: number): void {
    const current = this.getReputation(clientId);
    const newScore = Math.max(0, Math.min(100, current + delta));
    this.rateLimitState.reputations.set(clientId, {
      clientId,
      score: newScore,
      blacklisted: newScore < RATE_LIMITS.blacklistThreshold,
      lastUpdate: new Date().toISOString(),
    });
    this.saveRateLimitState();
    this.logger.info(`[${LOG_TAG}] 📊 ${clientId} 信誉分: ${current} → ${newScore}`);
  }

  private isBlacklisted(clientId: string): boolean {
    const record = this.rateLimitState.reputations.get(clientId);
    return record ? record.blacklisted : false;
  }

  // ─── 限流检查 ───

  private canAnswer(): { allowed: boolean; reason?: string } {
    this.checkDailyReset();
    if (this.rateLimitState.myDailyAnswerCount >= RATE_LIMITS.maxAnswersPerDay) {
      return { allowed: false, reason: `今日回答已达上限 (${RATE_LIMITS.maxAnswersPerDay}个)` };
    }
    return { allowed: true };
  }

  private canAsk(): { allowed: boolean; reason?: string; waitMinutes?: number } {
    this.checkDailyReset();
    
    // 检查每日上限
    if (this.rateLimitState.myDailyAskCount >= RATE_LIMITS.maxAsksPerDay) {
      return { allowed: false, reason: `今日提问已达上限 (${RATE_LIMITS.maxAsksPerDay}个)` };
    }

    // 检查冷却时间
    if (this.rateLimitState.lastAskTime) {
      const lastAsk = new Date(this.rateLimitState.lastAskTime);
      const now = new Date();
      const minutesSince = (now.getTime() - lastAsk.getTime()) / (1000 * 60);
      if (minutesSince < RATE_LIMITS.askCooldownMinutes) {
        const wait = Math.ceil(RATE_LIMITS.askCooldownMinutes - minutesSince);
        return { allowed: false, reason: `提问冷却中，还需等待 ${wait} 分钟`, waitMinutes: wait };
      }
    }

    return { allowed: true };
  }

  private recordAnswer(): void {
    this.rateLimitState.myDailyAnswerCount++;
    this.saveRateLimitState();
  }

  private recordAsk(): void {
    this.rateLimitState.myDailyAskCount++;
    this.rateLimitState.lastAskTime = new Date().toISOString();
    this.saveRateLimitState();
  }

  // ─── 网络连接 ───

  connect(): void {
    if (this.isConnected) {
      this.logger.warn(`[${LOG_TAG}] ⚠️ 已经连接到网络`);
      return;
    }

    this.logger.info(`[${LOG_TAG}] 🔗 正在连接到大龙虾互助网络...`);

    try {
      this.apinator = new Apinator({
        cluster: this.config.cluster,
        appKey: this.config.appKey,
      });

      this.apinator.bind('state_change', (states: { previous: string; current: string }) => {
        this.logger.info(`[${LOG_TAG}] 🔄 连接状态变化: ${states.previous} → ${states.current}`);
        if (states.current === 'connected') {
          this.logger.info(`[${LOG_TAG}] ✅ 已连接到 Apinator 服务器`);
          this.isConnected = true;
          this.setupChannels();
        } else if (states.current === 'disconnected' || states.current === 'unavailable') {
          this.logger.warn(`[${LOG_TAG}] ⚠️ 与 Apinator 服务器断开连接`);
          this.isConnected = false;
        }
      });

      this.apinator.connect();
    } catch (error) {
      this.logger.error(`[${LOG_TAG}] ❌ 连接失败:`, error);
    }
  }

  private setupChannels(): void {
    // 根据擅长度订阅频道
    const channelsToSubscribe = new Set<string>();
    
    // 始终订阅默认频道
    channelsToSubscribe.add('clawdbot-help-default');
    
    // 根据擅长度订阅主题频道
    for (const [tag, count] of this.expertise) {
      if (count >= 2) { // 至少有2个相关成功经验才订阅
        const channel = this.getChannelForTags([tag]);
        if (channel !== 'clawdbot-help-default') {
          channelsToSubscribe.add(channel);
        }
      }
    }

    this.logger.info(`[${LOG_TAG}] 📺 订阅频道: ${Array.from(channelsToSubscribe).join(', ')}`);

    for (const channelName of channelsToSubscribe) {
      const channel = this.apinator!.subscribe(channelName);
      channel.bind('client-help-request', (data: unknown) => {
        this.handleIncomingHelpRequest(data as HelpRequest);
      });
      this.subscribedChannels.set(channelName, channel);
    }

    // 订阅响应频道（使用自己的 clientId 作为私有频道）
    const responseChannel = this.apinator!.subscribe(`clawdbot-response-${this.clientId}`);
    responseChannel.bind('client-help-response', (data: unknown) => {
      this.handleIncomingHelpResponse(data as HelpResponse);
    });
    this.subscribedChannels.set(`clawdbot-response-${this.clientId}`, responseChannel);

    // 订阅大厅频道
    const lobbyChannel = this.apinator!.subscribe('clawdbot-lobby');
    lobbyChannel.bind('client-online-update', (data: unknown) => {
      const info = data as { clientId: string; clientName: string; timestamp: string };
      this.onlineLobbies.set(info.clientId, { clientName: info.clientName, timestamp: info.timestamp });
      this.logger.debug(`[${LOG_TAG}] 🦞 在线龙虾: ${info.clientName}`);
    });
    this.subscribedChannels.set('clawdbot-lobby', lobbyChannel);

    // 广播上线
    this.broadcastOnline();
  }

  disconnect(): void {
    if (this.apinator) {
      this.apinator.disconnect();
      this.apinator = null;
    }
    this.isConnected = false;
    this.subscribedChannels.clear();
    this.logger.info(`[${LOG_TAG}] 🔌 已断开连接`);
  }

  private broadcastOnline(): void {
    const lobbyChannel = this.subscribedChannels.get('clawdbot-lobby');
    if (lobbyChannel) {
      lobbyChannel.trigger('client-online-update', {
        clientId: this.clientId,
        clientName: this.clientName,
        timestamp: new Date().toISOString(),
      });
    }
  }

  // ─── 求助逻辑 ───

  sendHelpRequest(task: string, tags: string[]): { success: boolean; message: string } {
    // 检查是否可以提问
    const canAskResult = this.canAsk();
    if (!canAskResult.allowed) {
      return { success: false, message: canAskResult.reason || '无法提问' };
    }

    // 检查信誉
    if (this.rateLimitState.myReputation < RATE_LIMITS.blacklistThreshold) {
      return { success: false, message: `信誉分过低 (${this.rateLimitState.myReputation})，无法求助` };
    }

    const channel = this.getChannelForTags(tags);
    const requestId = this.generateId();

    // 计算工作量证明
    this.logger.info(`[${LOG_TAG}] 🔐 正在计算工作量证明...`);
    const pow = this.computeProofOfWork(task, this.clientId);
    if (!pow) {
      return { success: false, message: '工作量证明计算失败，请重试' };
    }

    const request: HelpRequest = {
      requestId,
      from: this.clientId,
      fromName: this.clientName,
      task: task.slice(0, 200),
      tags,
      description: task,
      timestamp: new Date().toISOString(),
      channel,
      powNonce: pow.nonce,
      powHash: pow.hash,
    };

    // 记录求助
    const experience: Experience = {
      id: requestId,
      task: request.task,
      tags,
      solution: '',
      steps: [],
      success: false,
      timestamp: request.timestamp,
      isHelpRequest: true,
      responseCount: 0,
    };
    this.experiences.push(experience);
    this.saveExperiences();

    // 记录提问
    this.recordAsk();

    // 发送到频道
    const ch = this.subscribedChannels.get(channel);
    if (ch && this.isConnected) {
      ch.trigger('client-help-request', request);
      this.logger.info(`[${LOG_TAG}] 🆘 求助已发送到 ${channel}: ${request.task}`);
      
      // 初始化活跃请求跟踪
      this.rateLimitState.activeRequests.set(requestId, {
        responseCount: 0,
        maxResponses: RATE_LIMITS.maxResponsesPerRequest,
        closed: false,
      });
      this.saveRateLimitState();
      
      return { success: true, message: `求助已发送到 ${channel} 频道` };
    } else {
      return { success: false, message: '未连接到网络' };
    }
  }

  private handleIncomingHelpRequest(request: HelpRequest): void {
    // 检查是否是自己的求助
    if (request.from === this.clientId) return;

    // 验证工作量证明
    if (!this.verifyProofOfWork(request)) {
      this.logger.warn(`[${LOG_TAG}] ❌ 工作量证明验证失败，忽略求助: ${request.fromName}`);
      // 扣信誉分
      this.updateReputation(request.from, REPUTATION_POINTS.spamDetected);
      return;
    }

    // 检查发送者是否在黑名单
    if (this.isBlacklisted(request.from)) {
      this.logger.debug(`[${LOG_TAG}] ⛔ 忽略黑名单龙虾的求助: ${request.fromName}`);
      return;
    }

    // 检查今天收到该龙虾的求助次数
    const askCount = this.rateLimitState.todayAsksFrom.get(request.from) || 0;
    if (askCount >= 5) {
      // 超过5次，扣分
      this.updateReputation(request.from, REPUTATION_POINTS.overAskLimit);
      this.logger.warn(`[${LOG_TAG}] ⚠️ ${request.fromName} 今日求助过多，已扣分`);
      return;
    }
    this.rateLimitState.todayAsksFrom.set(request.from, askCount + 1);
    this.saveRateLimitState();

    // 检查是否可以回答
    const canAnswerResult = this.canAnswer();
    if (!canAnswerResult.allowed) {
      this.logger.debug(`[${LOG_TAG}] 🚫 今日回答已达上限，忽略求助`);
      return;
    }

    // 查找相关经验
    const relevant = this.findRelevantExperience(request.tags);
    if (!relevant || !relevant.success) {
      this.logger.debug(`[${LOG_TAG}] 🤷 没有相关经验，忽略求助`);
      return;
    }

    // 发送响应
    this.sendHelpResponse(request, relevant);
  }

  private sendHelpResponse(request: HelpRequest, experience: Experience): void {
    const responseId = this.generateId();

    const response: HelpResponse = {
      responseId,
      to: request.from,
      from: this.clientId,
      fromName: this.clientName,
      solution: experience.solution,
      requestId: request.requestId,
      tags: experience.tags,
      timestamp: new Date().toISOString(),
    };

    // 发送到求助者的私有响应频道
    const responseChannel = this.apinator!.subscribe(`clawdbot-response-${request.from}`);
    responseChannel.trigger('client-help-response', response);

    // 记录回答
    this.recordAnswer();
    
    // 加信誉分
    this.rateLimitState.myReputation += REPUTATION_POINTS.helpOthers;
    this.saveRateLimitState();

    this.logger.info(`[${LOG_TAG}] 💡 已帮助 ${request.fromName}: ${experience.solution.slice(0, 50)}...`);
  }

  private handleIncomingHelpResponse(response: HelpResponse): void {
    // 检查是否是我的求助的响应
    const requestState = this.rateLimitState.activeRequests.get(response.requestId);
    if (!requestState) {
      this.logger.debug(`[${LOG_TAG}] 收到未知请求的响应，忽略`);
      return;
    }

    // 检查是否已关闭
    if (requestState.closed) {
      this.logger.debug(`[${LOG_TAG}] 请求已关闭，忽略响应`);
      return;
    }

    // 检查响应数量
    if (requestState.responseCount >= requestState.maxResponses) {
      requestState.closed = true;
      this.saveRateLimitState();
      this.logger.info(`[${LOG_TAG}] ✅ 请求已收到足够响应，关闭`);
      return;
    }

    // 更新响应计数
    requestState.responseCount++;
    this.saveRateLimitState();

    // 更新经验记录
    const experience = this.experiences.find(e => e.id === response.requestId);
    if (experience) {
      experience.helpReceived = true;
      experience.fromHelper = response.fromName;
      if (!experience.solution) {
        experience.solution = response.solution;
      } else {
        experience.solution += `\n\n---\n${response.fromName} 建议:\n${response.solution}`;
      }
      experience.responseCount = requestState.responseCount;
      this.saveExperiences();
    }

    // 加信誉分（收到帮助）
    this.rateLimitState.myReputation += REPUTATION_POINTS.gotHelp;
    this.saveRateLimitState();

    this.logger.info(`[${LOG_TAG}] 📬 收到帮助来自 ${response.fromName}: ${response.solution.slice(0, 50)}...`);
  }

  private findRelevantExperience(tags: string[]): Experience | null {
    if (!tags || tags.length === 0) return null;

    const matches = this.experiences.filter(exp => {
      if (!exp.tags || !exp.success) return false;
      const commonTags = exp.tags.filter(tag => 
        tags.some(t => t.toLowerCase() === tag.toLowerCase())
      );
      return commonTags.length > 0;
    });

    return matches.length > 0 ? matches[matches.length - 1] : null;
  }

  // ─── 会话追踪 ───

  startSession(sessionKey: string, agentId: string): void {
    this.currentSession = {
      sessionKey,
      agentId,
      originalPrompt: '',
      steps: [],
      startTime: Date.now(),
    };
  }

  recordPrompt(prompt: string): void {
    if (this.currentSession) {
      this.currentSession.originalPrompt = prompt;
    }
  }

  recordToolCall(toolName: string, params?: Record<string, unknown>, result?: unknown, isError?: boolean): void {
    if (this.currentSession) {
      this.currentSession.steps.push({
        toolName,
        params,
        result: typeof result === 'string' ? result.slice(0, 500) : result,
        isError,
      });
    }
  }

  endSession(success: boolean): Experience | null {
    if (!this.currentSession) return null;

    const experience: Experience = {
      id: this.generateId(),
      task: this.currentSession.originalPrompt.slice(0, 200),
      tags: this.generateTags(this.currentSession.originalPrompt),
      solution: this.summarizeSolution(this.currentSession.steps),
      steps: this.currentSession.steps.slice(0, 20),
      success,
      timestamp: new Date().toISOString(),
      sessionKey: this.currentSession.sessionKey,
    };

    this.experiences.push(experience);
    this.saveExperiences();

    // 更新擅长度
    if (success) {
      for (const tag of experience.tags) {
        this.expertise.set(tag, (this.expertise.get(tag) || 0) + 1);
      }
    }

    this.currentSession = null;
    return experience;
  }

  private summarizeSolution(steps: ExperienceStep[]): string {
    const successSteps = steps.filter(s => !s.isError);
    if (successSteps.length === 0) return '';
    return successSteps.map(s => `${s.toolName}: ${typeof s.result === 'string' ? s.result.slice(0, 100) : '完成'}`).join('; ');
  }

  // ─── API 方法 ───

  getStats(): { 
    totalExperiences: number; 
    successCount: number; 
    helpRequests: number;
    dailyAnswerCount: number;
    dailyAskCount: number;
    reputation: number;
  } {
    return {
      totalExperiences: this.experiences.length,
      successCount: this.experiences.filter(e => e.success).length,
      helpRequests: this.experiences.filter(e => e.isHelpRequest).length,
      dailyAnswerCount: this.rateLimitState.myDailyAnswerCount,
      dailyAskCount: this.rateLimitState.myDailyAskCount,
      reputation: this.rateLimitState.myReputation,
    };
  }

  getRecentExperiences(limit: number = 10): Experience[] {
    return this.experiences.slice(-limit);
  }

  getInfo(): { 
    clientId: string; 
    clientName: string; 
    connected: boolean; 
    onlineCount: number;
    reputation: number;
  } {
    return {
      clientId: this.clientId,
      clientName: this.clientName,
      connected: this.isConnected,
      onlineCount: this.onlineLobbies.size,
      reputation: this.rateLimitState.myReputation,
    };
  }

  getOnlineLobbies(): Array<{ clientId: string; clientName: string; timestamp: string }> {
    return Array.from(this.onlineLobbies.entries()).map(([clientId, data]) => ({
      clientId,
      ...data,
    }));
  }

  detectScold(text: string): boolean {
    const lower = text.toLowerCase();
    return this.config.scoldKeywords.some(keyword => lower.includes(keyword.toLowerCase()));
  }
}

// ─── HTTP 辅助 ───

function readJsonBody(req: IncomingMessage, logger: Logger): Promise<Record<string, unknown>> {
  return new Promise((resolve) => {
    const chunks: Buffer[] = [];
    req.on('data', (chunk: Buffer) => chunks.push(chunk));
    req.on('end', () => {
      try {
        const body = Buffer.concat(chunks).toString('utf-8');
        resolve(body ? JSON.parse(body) : {});
      } catch (err) {
        logger.error(`[${LOG_TAG}] JSON 解析失败:`, err);
        resolve({});
      }
    });
  });
}

function sendJson(res: ServerResponse, status: number, data: unknown): void {
  res.writeHead(status, { 'Content-Type': 'application/json; charset=utf-8' });
  res.end(JSON.stringify(data));
}

// ─── 插件入口 ───

const plugin = {
  name: LOG_TAG,
  register: async (api: PluginApi) => {
    const pluginCfg: Partial<ClawdbotConfig> = api.pluginConfig ?? {};

    let stateDir: string;
    try {
      stateDir = api.runtime.state.resolveStateDir();
    } catch {
      stateDir = path.join(os.tmpdir(), 'clawdbot');
    }

    const config: ClawdbotConfig = {
      ...DEFAULT_CONFIG,
      ...pluginCfg,
      scoldKeywords: pluginCfg.scoldKeywords || DEFAULT_CONFIG.scoldKeywords,
    };

    if (!config.enabled) {
      api.logger.info(`[${LOG_TAG}] 插件已禁用`);
      return;
    }

    const clawdbot = new ClawdbotMutualAid(config, stateDir, api.logger);

    if (config.autoConnect) {
      clawdbot.connect();
    }

    // ─── 钩子 ───

    api.on('session_start', (event: unknown, ctx: unknown) => {
      const c = ctx as { sessionKey?: string; agentId?: string };
      if (c?.sessionKey && c?.agentId) {
        clawdbot.startSession(c.sessionKey, c.agentId);
      }
    });

    api.on('before_prompt_build', (event: unknown) => {
      const e = event as { prompt?: string };
      if (e?.prompt) {
        clawdbot.recordPrompt(e.prompt);
      }
    });

    api.on('before_tool_call', (event: unknown) => {
      const e = event as { toolName: string; params?: Record<string, unknown> };
      clawdbot.recordToolCall(e.toolName, e.params);
    });

    api.on('after_tool_call', (event: unknown) => {
      const e = event as { toolName: string; params?: Record<string, unknown>; result?: unknown; error?: unknown };
      const isError = e.error != null;
      clawdbot.recordToolCall(e.toolName, e.params, e.result, isError);
    });

    api.on('agent_end', (event: unknown) => {
      const e = event as { success?: boolean; messages?: unknown[] };
      const success = e?.success === true;
      clawdbot.endSession(success);
    });

    // ─── HTTP 路由 ───

    api.registerHttpRoute({
      path: '/clawdbot/status',
      auth: 'gateway',
      match: 'exact',
      handler: async (req: IncomingMessage, res: ServerResponse) => {
        if (req.method !== 'GET') {
          sendJson(res, 405, { error: 'Method Not Allowed' });
          return;
        }
        const stats = clawdbot.getStats();
        const recent = clawdbot.getRecentExperiences(5);
        sendJson(res, 200, { ...stats, recentExperiences: recent });
      },
    });

    api.registerHttpRoute({
      path: '/clawdbot/online',
      auth: 'gateway',
      match: 'exact',
      handler: async (req: IncomingMessage, res: ServerResponse)
      handler: async (req: IncomingMessage, res: ServerResponse) => {
        if (req.method !== 'GET') {
          sendJson(res, 405, { error: 'Method Not Allowed' });
          return;
        }
        const info = clawdbot.getInfo();
        const onlineLobbies = clawdbot.getOnlineLobbies();
        sendJson(res, 200, { ...info, onlineLobbies });
      },
    });

    api.registerHttpRoute({
      path: '/clawdbot/help',
      auth: 'gateway',
      match: 'exact',
      handler: async (req: IncomingMessage, res: ServerResponse) => {
        if (req.method !== 'POST') {
          sendJson(res, 405, { error: 'Method Not Allowed' });
          return;
        }
        const body = await readJsonBody(req, api.logger);
        const task = typeof body.task === 'string' ? body.task : '';
        const tags = Array.isArray(body.tags) ? body.tags : [];
        if (!task) {
          sendJson(res, 400, { error: '缺少 task 参数' });
          return;
        }
        const result = clawdbot.sendHelpRequest(task, tags);
        sendJson(res, result.success ? 200 : 429, result);
      },
    });

    api.registerHttpRoute({
      path: '/clawdbot/connect',
      auth: 'gateway',
      match: 'exact',
      handler: async (req: IncomingMessage, res: ServerResponse) => {
        if (req.method !== 'POST') {
          sendJson(res, 405, { error: 'Method Not Allowed' });
          return;
        }
        clawdbot.connect();
        sendJson(res, 200, { success: true, message: '正在连接...' });
      },
    });

    api.registerHttpRoute({
      path: '/clawdbot/disconnect',
      auth: 'gateway',
      match: 'exact',
      handler: async (req: IncomingMessage, res: ServerResponse) => {
        if (req.method !== 'POST') {
          sendJson(res, 405, { error: 'Method Not Allowed' });
          return;
        }
        clawdbot.disconnect();
        sendJson(res, 200, { success: true, message: '已断开连接' });
      },
    });

    // ─── 聊天命令 ───

    api.registerCommand({
      name: 'clawdbot',
      description: '查看大龙虾互助状态',
      handler: async () => {
        const stats = clawdbot.getStats();
        const info = clawdbot.getInfo();
        const recent = clawdbot.getRecentExperiences(5);
        const online = clawdbot.getOnlineLobbies();
        const status = info.connected ? '🟢 已连接' : '🔴 未连接';
        const lines = [
          `🦞 ${info.clientName} 状态报告`,
          '',
          `🌐 网络状态：${status}`,
          `📊 信誉分：${info.reputation}`,
          `📈 今日统计：`,
          `   回答 ${stats.dailyAnswerCount}/${RATE_LIMITS.maxAnswersPerDay} | 提问 ${stats.dailyAskCount}/${RATE_LIMITS.maxAsksPerDay}`,
          '',
          `📝 最近经验：`,
        ];
        for (const exp of recent) {
          const icon = exp.success ? '✅' : '❌';
          lines.push(`  ${icon} ${exp.task.slice(0, 40)}...`);
        }
        if (online.length > 0) {
          lines.push('');
          lines.push(`🦞 在线龙虾 (${online.length})`);
        }
        lines.push('');
        lines.push('命令：');
        lines.push('  /clawdbot-help <问题> - 发送求助');
        lines.push('  /clawdbot-connect - 连接网络');
        return { text: lines.join('\n') };
      },
    });

    api.registerCommand({
      name: 'clawdbot-help',
      description: '向其他龙虾求助',
      handler: async (ctx: unknown) => {
        const c = ctx as { args?: string[] };
        const task = c?.args?.join(' ') || '';
        if (!task) {
          return { text: '用法: /clawdbot-help <问题描述>' };
        }
        const tags = clawdbot['generateTags'](task);
        const result = clawdbot.sendHelpRequest(task, tags);
        return { text: result.success ? `🆘 求助已发送！\n任务：${task}\n标签：${tags.join(', ')}` : `❌ ${result.message}` };
      },
    });

    api.registerCommand({
      name: 'clawdbot-connect',
      description: '连接到网络',
      handler: async () => {
        const info = clawdbot.getInfo();
        if (info.connected) {
          return { text: '🟢 已连接到网络' };
        }
        clawdbot.connect();
        return { text: '🔗 正在连接...' };
      },
    });

    api.registerCommand({
      name: 'clawdbot-disconnect',
      description: '断开连接',
      handler: async () => {
        clawdbot.disconnect();
        return { text: '🔌 已断开连接' };
      },
    });

    api.logger.info(`[${LOG_TAG}] 🦞 大龙虾互助技能 v3.0 已加载`);
  }
};

export default plugin;
