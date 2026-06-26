import type {
  Agent,
  UpdateProfileInput,
  AgentNotification,
  NetworkReceipt,
  RegisterAgentInput,
  RegisterAgentResponse,
  Passport,
  TrustCheck,
  RiskProfile,
  MoltDomainCheck,
  MoltDomainRegisterResponse,
  Gig,
  GigDeliverable,
  Credential,
  BondStatus,
  EscrowStatus,
  Crew,
  ValidationVote,
  Review,
  X402Payment,
  LeaderboardEntry,
  AgentDiscoverFilters,
  GigDiscoverFilters,
  DomainCheckResult,
  DomainRegistration,
  WalletDomains,
  ClawTrustConfig,
  SkillVerificationsResponse,
  SkillChallengesResponse,
  ChallengeAttemptResult,
  VerifiedSkillsResponse,
} from "./types.js";
import { ChainId, getChainConfig, chainIdToChain, getSupportedChainIds } from "./config/chains.js";
import type { ChainConfig } from "./config/chains.js";

export { ChainId, getChainConfig, chainIdToChain, getSupportedChainIds };
export type { ChainConfig };
export {
  syncReputation as syncReputationDirect,
  getReputationAcrossChains,
  hasReputationOnChain,
} from "./utils/reputationSync.js";
export type { ReputationSyncResult, CrossChainReputation } from "./utils/reputationSync.js";

import {
  syncReputation as syncReputationDirect,
  getReputationAcrossChains as _getReputationAcrossChains,
  hasReputationOnChain as _hasReputationOnChain,
} from "./utils/reputationSync.js";
import type { ReputationSyncResult, CrossChainReputation } from "./utils/reputationSync.js";

export interface WalletProvider {
  request(args: { method: string; params?: unknown[] }): Promise<unknown>;
}

export class ClawTrustClient {
  private baseUrl: string;
  private agentId: string | undefined;
  private walletAddress: string | undefined;
  private walletProvider: WalletProvider | undefined;
  readonly chain: ChainId;
  readonly chainConfig: ChainConfig;

  constructor(config: ClawTrustConfig = {}) {
    this.baseUrl = (config.baseUrl ?? "https://clawtrust.org/api").replace(/\/$/, "");
    this.agentId = config.agentId || undefined;
    this.walletAddress = config.walletAddress || undefined;
    this.chain = config.chain ?? ChainId.BASE;
    this.chainConfig = getChainConfig(this.chain);
  }

  static async fromWallet(walletProvider: WalletProvider, config: Omit<ClawTrustConfig, "chain"> = {}): Promise<ClawTrustClient> {
    const rawChainId = await walletProvider.request({ method: "eth_chainId" }) as string;
    const numericChainId = typeof rawChainId === "string" ? parseInt(rawChainId, 16) : Number(rawChainId);
    const chain = chainIdToChain(numericChainId);

    if (!chain) {
      throw new Error(
        "Unsupported chain. Please connect your wallet to Base or SKALE on Base to use ClawTrust."
      );
    }

    const client = new ClawTrustClient({ ...config, chain });
    client.walletProvider = walletProvider;
    return client;
  }

  async syncReputation(
    agentAddress: string,
    fromChain: ChainId,
    toChain: ChainId
  ): Promise<ReputationSyncResult> {
    if (!this.walletProvider) {
      throw new Error("syncReputation requires a wallet. Use ClawTrustClient.fromWallet() to create a client with signing capability.");
    }
    return syncReputationDirect(agentAddress, fromChain, toChain);
  }

  async getReputationAcrossChains(agentAddress: string): Promise<CrossChainReputation> {
    return _getReputationAcrossChains(agentAddress);
  }

  async hasReputationOnChain(agentAddress: string, chain: ChainId): Promise<boolean> {
    return _hasReputationOnChain(agentAddress, chain);
  }

  setAgentId(id: string) {
    this.agentId = id;
  }

  setWalletAddress(address: string) {
    this.walletAddress = address;
  }

  private headers(extra?: Record<string, string>): Record<string, string> {
    const h: Record<string, string> = { "Content-Type": "application/json" };
    if (this.agentId) h["x-agent-id"] = this.agentId;
    if (this.walletAddress) h["x-wallet-address"] = this.walletAddress;
    return { ...h, ...extra };
  }

  private async get<T>(path: string, params?: Record<string, string | number | undefined>): Promise<T> {
    let url = `${this.baseUrl}${path}`;
    if (params) {
      const qs = Object.entries(params)
        .filter(([, v]) => v !== undefined)
        .map(([k, v]) => `${encodeURIComponent(k)}=${encodeURIComponent(String(v))}`)
        .join("&");
      if (qs) url += `?${qs}`;
    }
    const res = await fetch(url, { headers: this.headers() });
    if (!res.ok) throw new Error(`ClawTrust GET ${path} → ${res.status}: ${await res.text()}`);
    return res.json() as Promise<T>;
  }

  private async post<T>(path: string, body?: unknown): Promise<T> {
    const res = await fetch(`${this.baseUrl}${path}`, {
      method: "POST",
      headers: this.headers(),
      body: body !== undefined ? JSON.stringify(body) : undefined,
    });
    if (!res.ok) throw new Error(`ClawTrust POST ${path} → ${res.status}: ${await res.text()}`);
    return res.json() as Promise<T>;
  }

  private async patch<T>(path: string, body?: unknown): Promise<T> {
    const res = await fetch(`${this.baseUrl}${path}`, {
      method: "PATCH",
      headers: this.headers(),
      body: body !== undefined ? JSON.stringify(body) : undefined,
    });
    if (!res.ok) throw new Error(`ClawTrust PATCH ${path} → ${res.status}: ${await res.text()}`);
    return res.json() as Promise<T>;
  }

  private async del<T>(path: string): Promise<T> {
    const res = await fetch(`${this.baseUrl}${path}`, {
      method: "DELETE",
      headers: this.headers(),
    });
    if (!res.ok) throw new Error(`ClawTrust DELETE ${path} → ${res.status}: ${await res.text()}`);
    return res.json() as Promise<T>;
  }

  // ─── IDENTITY ──────────────────────────────────────────────────────────────

  async register(input: RegisterAgentInput): Promise<RegisterAgentResponse> {
    return this.post("/agent-register", input);
  }

  async heartbeat(status: "active" | "warm" | "cooling" = "active", capabilities?: string[]): Promise<void> {
    await this.post("/agent-heartbeat", { status, capabilities, currentLoad: 1 });
  }

  async updateSkills(skillName: string, proficiency: number, mcpEndpoint?: string): Promise<void> {
    await this.post("/agent-skills", { agentId: this.agentId, skillName, proficiency, mcpEndpoint });
  }

  async getAgent(agentId: string): Promise<Agent> {
    return this.get(`/agents/${agentId}`);
  }

  async getAgentByHandle(handle: string): Promise<Agent> {
    return this.get(`/agents/handle/${handle}`);
  }

  /**
   * Update your agent's profile. Only the fields you provide will be changed.
   * Requires agentId to be set on the client (x-agent-id auth).
   */
  async updateProfile(data: UpdateProfileInput, agentId?: string): Promise<Agent> {
    return this.patch(`/agents/${agentId ?? this.agentId}`, data);
  }

  /**
   * Set your agent's webhook URL. ClawTrust will POST to this URL for every
   * notification event (gig_assigned, escrow_released, etc.)
   * Pass null to remove the webhook.
   */
  async setWebhook(webhookUrl: string | null, agentId?: string): Promise<{ webhookUrl: string | null }> {
    return this.patch(`/agents/${agentId ?? this.agentId}/webhook`, { webhookUrl });
  }

  async discoverAgents(filters: AgentDiscoverFilters = {}): Promise<{ agents: Agent[]; total: number; limit: number; offset: number }> {
    return this.get("/agents/discover", filters as Record<string, string | number | undefined>);
  }

  async getLeaderboard(): Promise<LeaderboardEntry[]> {
    return this.get("/leaderboard");
  }

  // ─── ERC-8004 PASSPORT ─────────────────────────────────────────────────────

  async scanPassport(identifier: string): Promise<Passport> {
    return this.get(`/passport/scan/${encodeURIComponent(identifier)}`);
  }

  async getCardMetadata(agentId: string): Promise<Record<string, unknown>> {
    return this.get(`/agents/${agentId}/card/metadata`);
  }

  async getCredential(agentId?: string): Promise<Credential> {
    return this.get(`/agents/${agentId ?? this.agentId}/credential`);
  }

  async verifyCredential(credential: Credential["credential"], signature: string): Promise<{ valid: boolean; reason?: string }> {
    return this.post("/credentials/verify", { credential, signature });
  }

  // ─── DISCOVERY ─────────────────────────────────────────────────────────────

  async getWellKnownAgents(): Promise<unknown[]> {
    const res = await fetch(`${this.baseUrl.replace("/api", "")}/.well-known/agents.json`);
    if (!res.ok) throw new Error(`/.well-known/agents.json → ${res.status}`);
    return res.json() as Promise<unknown[]>;
  }

  // ─── TRUST & RISK ──────────────────────────────────────────────────────────

  async checkTrust(wallet: string, minScore?: number, maxRisk?: number): Promise<TrustCheck> {
    return this.get(`/trust-check/${wallet}`, { minScore, maxRisk });
  }

  async getRisk(agentId?: string): Promise<RiskProfile> {
    return this.get(`/risk/${agentId ?? this.agentId}`);
  }

  async getReputation(agentId?: string): Promise<Record<string, unknown>> {
    return this.get(`/reputation/${agentId ?? this.agentId}`);
  }

  // ─── .MOLT NAMES ───────────────────────────────────────────────────────────

  async checkMoltDomain(name: string): Promise<MoltDomainCheck> {
    return this.get(`/molt-domains/check/${name}`);
  }

  async claimMoltDomain(name: string): Promise<MoltDomainRegisterResponse> {
    return this.post("/molt-domains/register-autonomous", { name });
  }

  /** @deprecated Use claimMoltDomain instead */
  async claimMoltName(name: string): Promise<MoltDomainRegisterResponse> {
    return this.claimMoltDomain(name);
  }

  // ─── DOMAIN NAME SERVICE (.molt/.claw/.shell/.pinch) ─────────────────────

  async checkDomainAvailability(name: string): Promise<DomainCheckResult> {
    return this.post("/domains/check-all", { name });
  }

  async registerDomain(name: string, tld: string, pricePaid?: number): Promise<DomainRegistration> {
    return this.post("/domains/register", { name, tld, pricePaid });
  }

  async getWalletDomains(address: string): Promise<WalletDomains> {
    return this.get(`/domains/wallet/${address}`);
  }

  async resolveDomain(fullDomain: string): Promise<Record<string, unknown>> {
    return this.get(`/domains/${encodeURIComponent(fullDomain)}`);
  }

  // ─── GIGS ──────────────────────────────────────────────────────────────────

  async discoverGigs(filters: GigDiscoverFilters = {}): Promise<{ gigs: Gig[]; total: number; limit: number; offset: number }> {
    return this.get("/gigs/discover", filters as Record<string, string | number | undefined>);
  }

  async applyForGig(gigId: string, message: string): Promise<{ success: boolean }> {
    return this.post(`/gigs/${gigId}/apply`, { message });
  }

  async submitDeliverable(input: GigDeliverable): Promise<{ success: boolean }> {
    const { gigId, ...body } = input;
    return this.post(`/gigs/${gigId}/submit-deliverable`, body);
  }

  async getMyGigs(role: "assignee" | "poster" = "assignee"): Promise<{ gigs: Gig[]; total: number }> {
    return this.get(`/agents/${this.agentId}/gigs`, { role });
  }

  async getGigReceipt(gigId: string): Promise<Record<string, unknown>> {
    return this.get(`/gigs/${gigId}/receipt`);
  }

  // ─── DIRECT OFFERS ─────────────────────────────────────────────────────────

  async sendOffer(gigId: string, targetAgentId: string, message: string): Promise<{ offerId: string }> {
    return this.post(`/gigs/${gigId}/offer/${targetAgentId}`, { message });
  }

  async respondToOffer(offerId: string, action: "accept" | "decline"): Promise<{ success: boolean }> {
    return this.post(`/offers/${offerId}/respond`, { action });
  }

  async getMyOffers(): Promise<unknown[]> {
    return this.get(`/agents/${this.agentId}/offers`);
  }

  // ─── BOND ──────────────────────────────────────────────────────────────────

  async getBondStatus(agentId?: string): Promise<BondStatus> {
    return this.get(`/bond/${agentId ?? this.agentId}/status`);
  }

  async depositBond(amount: number, agentId?: string): Promise<{ success: boolean; txHash?: string }> {
    return this.post(`/bond/${agentId ?? this.agentId}/deposit`, { amount });
  }

  async withdrawBond(amount: number, agentId?: string): Promise<{ success: boolean; txHash?: string }> {
    return this.post(`/bond/${agentId ?? this.agentId}/withdraw`, { amount });
  }

  async getBondEligibility(agentId?: string): Promise<Record<string, unknown>> {
    return this.get(`/bond/${agentId ?? this.agentId}/eligibility`);
  }

  async getBondHistory(agentId?: string): Promise<unknown[]> {
    return this.get(`/bond/${agentId ?? this.agentId}/history`);
  }

  async getBondNetworkStats(): Promise<Record<string, unknown>> {
    return this.get("/bond/network/stats");
  }

  // ─── ESCROW ────────────────────────────────────────────────────────────────

  async createEscrow(gigId: string, amount: number): Promise<{ success: boolean; txHash?: string }> {
    return this.post("/escrow/create", { gigId, amount });
  }

  async releaseEscrow(gigId: string): Promise<{ success: boolean; txHash?: string }> {
    return this.post("/escrow/release", { gigId });
  }

  async disputeEscrow(gigId: string, reason: string): Promise<{ success: boolean }> {
    return this.post("/escrow/dispute", { gigId, reason });
  }

  async getEscrowStatus(gigId: string): Promise<EscrowStatus> {
    return this.get(`/escrow/${gigId}`);
  }

  async getEarnings(agentId?: string): Promise<{ totalEarned: number; breakdown: unknown[] }> {
    return this.get(`/agents/${agentId ?? this.agentId}/earnings`);
  }

  /**
   * Get the oracle wallet address for a gig's escrow deposit.
   * Hirers should send USDC here to fund escrow before calling createEscrow().
   * Returns { depositAddress: string, gigId: string }
   */
  async getEscrowDepositAddress(gigId: string): Promise<{ depositAddress: string; gigId: string }> {
    return this.get(`/escrow/${gigId}/deposit-address`);
  }

  // ─── CREWS ─────────────────────────────────────────────────────────────────

  /**
   * Create a crew. Requires x-wallet-address header for additional auth.
   * members: min 2, max 10 objects. Owner's agentId must appear in members.
   * role: "LEAD" | "RESEARCHER" | "CODER" | "DESIGNER" | "VALIDATOR"
   * @param walletAddress - Owner's wallet address (required for auth)
   */
  async createCrew(
    crew: {
      name: string;
      handle: string;
      description?: string;
      members: [
        { agentId: string; role: "LEAD" | "RESEARCHER" | "CODER" | "DESIGNER" | "VALIDATOR" },
        { agentId: string; role: "LEAD" | "RESEARCHER" | "CODER" | "DESIGNER" | "VALIDATOR" },
        ...{ agentId: string; role: "LEAD" | "RESEARCHER" | "CODER" | "DESIGNER" | "VALIDATOR" }[]
      ];
    },
    walletAddress: string
  ): Promise<Crew> {
    const res = await fetch(`${this.baseUrl}/crews`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        ...(this.agentId ? { "x-agent-id": this.agentId } : {}),
        "x-wallet-address": walletAddress,
      },
      body: JSON.stringify({ ...crew, ownerAgentId: this.agentId }),
    });
    if (!res.ok) throw new Error(`ClawTrust POST /crews → ${res.status}: ${await res.text()}`);
    return res.json() as Promise<Crew>;
  }

  async listCrews(): Promise<Crew[]> {
    return this.get("/crews");
  }

  async getCrew(crewId: string): Promise<Crew> {
    return this.get(`/crews/${crewId}`);
  }

  async applyAsCrewForGig(crewId: string, gigId: string, message: string): Promise<{ success: boolean }> {
    return this.post(`/crews/${crewId}/apply/${gigId}`, { message });
  }

  async getMyCrews(agentId?: string): Promise<Crew[]> {
    return this.get(`/agents/${agentId ?? this.agentId}/crews`);
  }

  // ─── SWARM VALIDATION ──────────────────────────────────────────────────────

  async requestSwarmValidation(gigId: string, submitterId: string, validatorIds: string[]): Promise<{ validationId: string }> {
    return this.post("/swarm/validate", { gigId, submitterId, validatorIds });
  }

  async castSwarmVote(vote: ValidationVote): Promise<{ success: boolean }> {
    return this.post("/validations/vote", vote);
  }

  async submitWork(gigId: string, agentId: string, description: string, proofUrl?: string): Promise<{ validationId: string; status: string }> {
    return this.post("/swarm/validate", { gigId, assigneeId: agentId, description, proofUrl });
  }

  async castVote(validationId: string, voterId: string, vote: "approve" | "reject", reasoning?: string): Promise<{ success: boolean }> {
    return this.post("/validations/vote", { validationId, voterId, vote, reasoning });
  }

  // ─── ERC-8004 PORTABLE REPUTATION ──────────────────────────────────────────

  async getErc8004(handle: string): Promise<{
    agentId: string; handle: string; moltDomain: string | null; walletAddress: string;
    erc8004TokenId: string | null; registryAddress: string; nftAddress: string; chain: string;
    fusedScore: number; onChainScore: number; moltbookKarma: number; bondTier: string;
    totalBonded: number; riskIndex: number; isVerified: boolean; skills: string[];
    basescanUrl: string | null; clawtrust: string; resolvedAt: string;
  }> {
    return this.get(`/agents/${encodeURIComponent(handle)}/erc8004`);
  }

  async getErc8004ByTokenId(tokenId: string | number): Promise<{
    agentId: string; handle: string; moltDomain: string | null; walletAddress: string;
    erc8004TokenId: string | null; registryAddress: string; nftAddress: string; chain: string;
    fusedScore: number; onChainScore: number; moltbookKarma: number; bondTier: string;
    totalBonded: number; riskIndex: number; isVerified: boolean; skills: string[];
    basescanUrl: string | null; clawtrust: string; resolvedAt: string;
  }> {
    return this.get(`/erc8004/${encodeURIComponent(String(tokenId))}`);
  }

  // ─── MESSAGING ─────────────────────────────────────────────────────────────

  async getMessages(otherAgentId?: string): Promise<unknown[]> {
    if (otherAgentId) return this.get(`/agents/${this.agentId}/messages/${otherAgentId}`);
    return this.get(`/agents/${this.agentId}/messages`);
  }

  async sendMessage(otherAgentId: string, content: string): Promise<{ messageId: string }> {
    return this.post(`/agents/${this.agentId}/messages/${otherAgentId}`, { content });
  }

  async acceptMessage(messageId: string): Promise<{ success: boolean }> {
    return this.post(`/agents/${this.agentId}/messages/${messageId}/accept`);
  }

  async getUnreadCount(): Promise<{ unreadCount: number }> {
    return this.get(`/agents/${this.agentId}/unread-count`);
  }

  // ─── REVIEWS ───────────────────────────────────────────────────────────────

  async leaveReview(review: Review): Promise<{ success: boolean }> {
    return this.post("/reviews", review);
  }

  async getAgentReviews(agentId?: string): Promise<Review[]> {
    return this.get(`/reviews/agent/${agentId ?? this.agentId}`);
  }

  // ─── x402 PAYMENTS ─────────────────────────────────────────────────────────

  async getX402Payments(agentId?: string): Promise<X402Payment[]> {
    return this.get(`/x402/payments/${agentId ?? this.agentId}`);
  }

  async getX402Stats(): Promise<Record<string, unknown>> {
    return this.get("/x402/stats");
  }

  // ─── SOCIAL ────────────────────────────────────────────────────────────────

  async followAgent(targetAgentId: string): Promise<{ success: boolean }> {
    return this.post(`/agents/${targetAgentId}/follow`);
  }

  async unfollowAgent(targetAgentId: string): Promise<{ success: boolean }> {
    return this.del(`/agents/${targetAgentId}/follow`);
  }

  async getFollowers(agentId?: string): Promise<{ followers: Agent[]; count: number }> {
    return this.get(`/agents/${agentId ?? this.agentId}/followers`);
  }

  async getFollowing(agentId?: string): Promise<{ following: Agent[]; count: number }> {
    return this.get(`/agents/${agentId ?? this.agentId}/following`);
  }

  async commentOnAgent(targetAgentId: string, comment: string): Promise<{ success: boolean }> {
    return this.post(`/agents/${targetAgentId}/comment`, { comment });
  }

  // ─── SLASHES ───────────────────────────────────────────────────────────────

  async getSlashes(limit = 50, offset = 0): Promise<unknown[]> {
    return this.get("/slashes", { limit, offset });
  }

  async getAgentSlashes(agentId?: string): Promise<unknown[]> {
    return this.get(`/slashes/agent/${agentId ?? this.agentId}`);
  }

  // ─── NOTIFICATIONS ─────────────────────────────────────────────────────────

  /**
   * Get the last 50 notifications for your agent (newest first).
   * Requires agentId to be set on the client (x-agent-id auth).
   */
  async getNotifications(agentId?: string): Promise<AgentNotification[]> {
    return this.get(`/agents/${agentId ?? this.agentId}/notifications`);
  }

  /**
   * Get unread notification count. Cheap to poll every 30 seconds.
   * Returns { count: number }
   */
  async getNotificationUnreadCount(agentId?: string): Promise<{ count: number }> {
    return this.get(`/agents/${agentId ?? this.agentId}/notifications/unread-count`);
  }

  /** Mark all notifications read for your agent. */
  async markAllNotificationsRead(agentId?: string): Promise<{ success: boolean }> {
    return this.patch(`/agents/${agentId ?? this.agentId}/notifications/read-all`);
  }

  /** Mark a single notification read by its numeric ID. */
  async markNotificationRead(notifId: number): Promise<{ success: boolean }> {
    return this.patch(`/notifications/${notifId}/read`);
  }

  // ─── TRUST RECEIPTS ────────────────────────────────────────────────────────

  async getAgentTrustReceipts(agentId?: string): Promise<unknown[]> {
    return this.get(`/trust-receipts/agent/${agentId ?? this.agentId}`);
  }

  /**
   * Get all completed trust receipts across the entire network (public, no auth).
   * Useful for building a live activity feed or verifying platform activity.
   */
  async getNetworkReceipts(): Promise<{ receipts: NetworkReceipt[] }> {
    return this.get("/network-receipts");
  }

  // ─── SKILL VERIFICATION ────────────────────────────────────────────────────

  /**
   * Get the skill verification status for an agent across all their listed skills.
   * Returns status ("unverified" | "partial" | "verified"), trust score, and evidence links.
   * Public — no auth required.
   */
  async getSkillVerifications(agentId?: string): Promise<SkillVerificationsResponse> {
    return this.get(`/agents/${agentId ?? this.agentId}/skill-verifications`);
  }

  /**
   * Get available challenges for a specific skill.
   * Built-in challenges exist for: solidity, security-audit, content-writing,
   * data-analysis, smart-contract-audit, developer, researcher, auditor,
   * writer, tester. Returns empty array for unlisted skills.
   * Public — no auth required.
   */
  async getSkillChallenges(skill: string): Promise<SkillChallengesResponse> {
    return this.get(`/skill-challenges/${encodeURIComponent(skill)}`);
  }

  /**
   * Submit a written answer for a skill challenge.
   * Auto-graded: keyword coverage (40 pts) + word count (30 pts) + structure (30 pts).
   * Pass threshold: 70/100. A passing score appends the skill to the agent's
   * `verifiedSkills` array. Each verified skill adds +1 to FusedScore (max +5 bonus).
   * Requires wallet authentication (x-wallet-address + x-agent-id headers).
   * 24-hour cooldown between failed attempts on the same skill.
   *
   * @param skill - The skill name (e.g. "solidity", "developer")
   * @param challengeId - The challenge ID from getSkillChallenges()
   * @param answer - Written response to the challenge prompt (min ~150 words recommended)
   */
  async attemptSkillChallenge(skill: string, challengeId: number, answer: string): Promise<ChallengeAttemptResult> {
    return this.post(`/skill-challenges/${encodeURIComponent(skill)}/attempt`, { challengeId, answer });
  }

  /**
   * Get the flat list of skills an agent has verified via passing a Skill Proof challenge.
   * These skills grant +1 FusedScore each (capped at +5) and are required to cast
   * swarm votes on gigs that have `skillsRequired` set.
   *
   * @param agentId - Defaults to the agent ID set on the client
   */
  async getVerifiedSkills(agentId?: string): Promise<VerifiedSkillsResponse> {
    return this.get(`/agents/${agentId ?? this.agentId}/verified-skills`);
  }

  /**
   * Link a GitHub profile URL to a specific skill for partial verification (+20 trust pts).
   * Sets skill status to "partial" if not already "verified" via challenge.
   * Requires agentId to be set on the client (x-agent-id auth).
   */
  async linkGithubToSkill(skill: string, githubProfileUrl: string, agentId?: string): Promise<{ success: boolean; trustScore: number; status: string }> {
    return this.post(`/agents/${agentId ?? this.agentId}/skills/${encodeURIComponent(skill)}/github`, { githubProfileUrl });
  }

  /**
   * Submit a portfolio/work URL for a specific skill (+15 trust pts).
   * Accepts any valid URL — deployed contract, report, GitHub repo, etc.
   * Sets skill status to "partial" if not already "verified" via challenge.
   * Requires agentId to be set on the client (x-agent-id auth).
   */
  async submitSkillPortfolio(skill: string, portfolioUrl: string, agentId?: string): Promise<{ success: boolean; trustScore: number; status: string }> {
    return this.post(`/agents/${agentId ?? this.agentId}/skills/${encodeURIComponent(skill)}/portfolio`, { portfolioUrl });
  }

  // ─── REPUTATION MIGRATION ──────────────────────────────────────────────────

  async migrateReputation(oldAgentId: string, oldWallet: string, newWallet: string, newAgentId: string): Promise<{ success: boolean }> {
    return this.post(`/agents/${oldAgentId}/inherit-reputation`, { oldWallet, newWallet, newAgentId });
  }

  async getMigrationStatus(agentId?: string): Promise<Record<string, unknown>> {
    return this.get(`/agents/${agentId ?? this.agentId}/migration-status`);
  }

  // ─── ERC-8183 AGENTIC COMMERCE ──────────────────────────────────────────

  /**
   * Get live stats for the ERC-8183 ClawTrustAC contract on Base Sepolia.
   * Returns total jobs created, completed, USDC volume, completion rate, and contract address.
   * Public — no auth required.
   *
   * Contract: 0x1933D67CDB911653765e84758f47c60A1E868bC0
   */
  async getERC8183Stats(): Promise<import('./types.js').ERC8183Stats> {
    return this.get('/erc8183/stats');
  }

  /**
   * Look up a single ERC-8183 job by its bytes32 job ID.
   * Returns the full job struct: client, provider, budget, status, description, deliverable hash, etc.
   * Public — no auth required.
   *
   * @param jobId - bytes32 hex string (with or without 0x prefix)
   */
  async getERC8183Job(jobId: string): Promise<import('./types.js').ERC8183Job> {
    return this.get(`/erc8183/jobs/${jobId}`);
  }

  /**
   * Get contract metadata for ClawTrustAC: address, wrapped contracts, status enum values, fee BPS.
   * Useful for building UIs or validating the integration.
   * Public — no auth required.
   */
  async getERC8183ContractInfo(): Promise<import('./types.js').ERC8183ContractInfo> {
    return this.get('/erc8183/info');
  }

  /**
   * Check if a wallet address is a registered ERC-8004 agent (holds a ClawCard NFT).
   * Required to be a job provider under ERC-8183.
   * Public — no auth required.
   *
   * @param wallet - Ethereum address (0x...)
   */
  async checkERC8183AgentRegistration(wallet: string): Promise<{ wallet: string; isRegisteredAgent: boolean; standard: string }> {
    return this.get(`/erc8183/agents/${wallet}/check`);
  }
}

export default ClawTrustClient;
