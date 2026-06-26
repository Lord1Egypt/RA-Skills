import { AlephGunBridge } from '../core/AlephGunBridge';
import { AlephWallet } from '../infra/Wallet';
import { 
  DomainDefinition, 
  DomainRules, 
  DomainMembership, 
  DomainVisibility, 
  DomainRole, 
  MembershipStatus,
  StakingTier
} from '../common/types';
import { SignedEnvelope } from '../common/trust-types';
import * as crypto from 'crypto';

export class DomainManager {
  constructor(
    private bridge: AlephGunBridge,
    private wallet: AlephWallet,
    private gun: any
  ) {}

  /**
   * Register a new domain using a signed envelope.
   * The envelope must contain a valid DomainDefinition and be signed by the owner.
   */
  async registerDomain(envelope: SignedEnvelope<DomainDefinition>): Promise<void> {
    const definition = envelope.payload;
    
    // Validate envelope (signature, etc.) - assumed done by caller or we should do it here
    // For now, we assume the envelope is valid structure-wise

    // Check handle availability
    const existingId = await this.getDomainIdByHandle(definition.handle);
    if (existingId && existingId !== definition.id) {
        throw new Error(`Handle ${definition.handle} is already taken`);
    }

    // Store in Gun
    // domains/by_handle/<handle> -> domainId
    this.gun.get('domains').get('by_handle').get(definition.handle).put(definition.id);
    
    // domains/<domainId> -> envelope (store the whole signed envelope)
    this.gun.get('domains').get(definition.id).put(envelope);
    
    // Add owner as member (if not already implicit)
    // The owner is the envelope author.
    await this.addMember(definition.id, envelope.author.fingerprint, 'owner', 'active');
  }

  async joinDomain(domainId: string): Promise<{ status: MembershipStatus }> {
    // Fetch domain
    const definition = await this.getDomain(domainId);
    if (!definition) throw new Error("Domain not found");
    
    // Check rules
    let status: MembershipStatus = 'active';
    if (definition.rules.requiresApproval) {
      status = 'pending';
    }

    // Check staking tier
    const balance = await this.wallet.getBalance();
    const tierOrder: StakingTier[] = ['Neophyte', 'Adept', 'Magus', 'Archon'];
    const userTierIdx = tierOrder.indexOf(balance.stakingTier);
    const requiredTierIdx = tierOrder.indexOf(definition.rules.minStakingTier);
    
    if (userTierIdx < requiredTierIdx) {
        throw new Error(`Insufficient staking tier. Required: ${definition.rules.minStakingTier}`);
    }

    await this.addMember(domainId, this.wallet.address, 'member', status);
    return { status };
  }

  async leaveDomain(domainId: string): Promise<boolean> {
    await this.removeMember(domainId, this.wallet.address);
    return true;
  }

  async getDomain(domainId: string): Promise<DomainDefinition | null> {
    return new Promise((resolve) => {
        this.gun.get('domains').get(domainId).once((data: any) => {
            resolve(data || null);
        });
    });
  }
  
  async getDomainIdByHandle(handle: string): Promise<string | null> {
      return new Promise((resolve) => {
          this.gun.get('domains').get('by_handle').get(handle).once((data: any) => {
              resolve(data || null);
          });
      });
  }

  async listDomains(limit: number = 20): Promise<DomainDefinition[]> {
      // Stub: In real Gun, we'd need a set or iterate keys
      return []; 
  }

  async getMembers(domainId: string): Promise<DomainMembership[]> {
      return new Promise((resolve) => {
          this.gun.get('domains').get(domainId).get('members').once((data: any) => {
              if (!data) return resolve([]);
              const members = Object.keys(data)
                .filter(k => k !== '_' && data[k])
                .map(k => data[k]);
              resolve(members);
          });
      });
  }

  async getCommonDomains(userId: string): Promise<string[]> {
      const myDomains = await this.getUserDomains(this.wallet.address);
      const theirDomains = await this.getUserDomains(userId);
      return myDomains.filter(d => theirDomains.includes(d));
  }

  private async getUserDomains(userId: string): Promise<string[]> {
      return new Promise((resolve) => {
          this.gun.get('users').get(userId).get('domains').once((data: any) => {
              if (!data) return resolve([]);
              const domains = Object.keys(data).filter(k => k !== '_' && data[k]);
              resolve(domains);
          });
      });
  }

  private async addMember(domainId: string, userId: string, role: DomainRole, status: MembershipStatus) {
    const membership: DomainMembership = {
      domainId,
      userId,
      role,
      status,
      joinedAt: Date.now()
    };
    
    this.gun.get('domains').get(domainId).get('members').get(userId).put(membership);
    this.gun.get('users').get(userId).get('domains').get(domainId).put(membership);
  }

  private async removeMember(domainId: string, userId: string) {
      this.gun.get('domains').get(domainId).get('members').get(userId).put(null);
      this.gun.get('users').get(userId).get('domains').get(domainId).put(null);
  }
}
