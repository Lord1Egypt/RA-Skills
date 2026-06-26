import { SemanticDomain } from '../core/types';
import { AlephWallet } from '../infra/Wallet';
import { Subscription } from '../common';
import { generateId } from '../common/hash';

// --- Interfaces ---

export interface ServiceDefinition {
  id: string;
  name: string;
  description: string;
  version: string;
  providerNodeId: string;
  providerUserId: string;
  
  access: {
    visibility: 'PUBLIC' | 'RESTRICTED' | 'PRIVATE';
    allowedNodes?: string[];
    allowedUsers?: string[];
    allowedTiers?: Array<'Neophyte' | 'Adept' | 'Magus' | 'Archon'>;
    minCoherence?: number;
    minReputation?: number;
    rateLimit: {
      requestsPerMinute: number;
      requestsPerHour: number;
      requestsPerDay: number;
      burstLimit: number;
    };
    geoRestrictions?: {
      allowedCountries?: string[];
      blockedCountries?: string[];
    };
  };
  
  pricing: {
    model: 'FREE' | 'PER_CALL' | 'SUBSCRIPTION' | 'STAKE_GATED' | 'HYBRID';
    perCallCost?: number;
    subscriptionTiers?: Array<{
      name: string;
      price: number;
      period: 'DAILY' | 'WEEKLY' | 'MONTHLY' | 'YEARLY';
      limits: { requestsPerPeriod: number; priorityLevel: number; };
    }>;
    minStake?: number;
    freeTier?: { requestsPerDay: number; features: string[]; };
    acceptedPayments: Array<'ALEPH' | 'STAKED_ALEPH' | 'USD'>;
    revenueDistribution: { provider: number; network: number; stakers: number; };
  };
  
  interface: {
    protocol: 'REST' | 'GRAPHQL' | 'WEBSOCKET' | 'GRPC' | 'GUN_SYNC';
    baseUrl?: string;
    authentication: 'NONE' | 'API_KEY' | 'KEYTRIPLET' | 'OAUTH' | 'STAKED_IDENTITY';
    endpoints: Array<{
      name: string;
      description: string;
      method?: 'GET' | 'POST' | 'PUT' | 'DELETE';
      path?: string;
      inputSchema: Record<string, any>;
      outputSchema: Record<string, any>;
      costMultiplier: number;
    }>;
    semanticDomain: SemanticDomain;
    smfAxes: number[];
  };
  
  sla: {
    uptimeGuarantee: number;
    maxResponseTimeMs: number;
    dataRetention: { logsRetentionDays: number; resultsRetentionDays: number; };
    supportLevel: 'NONE' | 'COMMUNITY' | 'EMAIL' | 'PRIORITY';
    slaViolationCompensation: { uptimeViolation: number; responseTimeViolation: number; };
  };
  
  tags: string[];
  category: string;
  documentationUrl?: string;
  iconUrl?: string;
  status: 'DRAFT' | 'ACTIVE' | 'DEPRECATED' | 'SUSPENDED';
  createdAt: number;
  updatedAt: number;
  smfSignature: number[];
}

export interface ServiceInstance {
  serviceId: string;
  nodeId: string;
  status: 'STARTING' | 'RUNNING' | 'DRAINING' | 'STOPPED' | 'ERROR';
  health: {
    healthy: boolean;
    lastHealthCheck: number;
    consecutiveFailures: number;
    uptimeMs: number;
    startedAt: number;
  };
  metrics: {
    totalRequests: number;
    successfulRequests: number;
    failedRequests: number;
    averageResponseTimeMs: number;
    p95ResponseTimeMs: number;
    p99ResponseTimeMs: number;
    requestsPerSecond: number;
  };
  economics: {
    totalRevenue: number;
    pendingPayout: number;
    lastPayoutAt: number;
    activeSubscribers: number;
    totalSubscribers: number;
  };
  connections: {
    active: number;
    maxConcurrent: number;
  };
}

// --- Manager ---

export class ServiceManager {
  constructor(
      private gun: any,
      private wallet: AlephWallet,
      private localNodeId: string
  ) {}

  /**
   * Register a new service.
   */
  public async registerService(definition: ServiceDefinition): Promise<{ serviceId: string; registrationFee: number }> {
      // Validate...
      // Store in Gun
      await new Promise<void>((resolve) => {
          this.gun.get('services').get(definition.id).put({ definition }, (ack: any) => resolve());
      });

      // Register instance locally
      await this.registerInstance(definition.id);

      return { serviceId: definition.id, registrationFee: 10 }; // Fee logic stub
  }

  /**
   * Register a running instance of a service on this node.
   */
  public async registerInstance(serviceId: string): Promise<void> {
      const instance: ServiceInstance = {
          serviceId,
          nodeId: this.localNodeId,
          status: 'RUNNING',
          health: {
              healthy: true,
              lastHealthCheck: Date.now(),
              consecutiveFailures: 0,
              uptimeMs: 0,
              startedAt: Date.now()
          },
          metrics: {
              totalRequests: 0,
              successfulRequests: 0,
              failedRequests: 0,
              averageResponseTimeMs: 0,
              p95ResponseTimeMs: 0,
              p99ResponseTimeMs: 0,
              requestsPerSecond: 0
          },
          economics: {
              totalRevenue: 0,
              pendingPayout: 0,
              lastPayoutAt: 0,
              activeSubscribers: 0,
              totalSubscribers: 0
          },
          connections: {
              active: 0,
              maxConcurrent: 100
          }
      };

      await new Promise<void>((resolve) => {
          this.gun.get('services').get(serviceId).get('instances').get(this.localNodeId).put(instance, (ack: any) => resolve());
      });
  }

  /**
   * Search for services.
   */
  public async search(query: {
    text?: string;
    tags?: string[];
    category?: string;
    semanticDomain?: SemanticDomain;
  }): Promise<ServiceDefinition[]> {
      // Mock search - in real Gun, we'd use index or map
      // Here we assume we can scan `services` node or rely on tags index
      return new Promise((resolve) => {
          const results: ServiceDefinition[] = [];
          this.gun.get('services').map().once((data: any) => {
              if (data && data.definition) {
                  const def = data.definition as ServiceDefinition;
                  // Simple filtering
                  if (query.category && def.category !== query.category) return;
                  if (query.tags && !query.tags.some(t => def.tags.includes(t))) return;
                  results.push(def);
              }
          });
          setTimeout(() => resolve(results), 500);
      });
  }

  /**
   * Call a service.
   */
  public async callService<T>(
      serviceId: string,
      endpointName: string,
      input: Record<string, any>,
      options?: { maxCost?: number }
  ): Promise<{ result: T; cost: number; executorNode: string }> {
      // 1. Get Service Def
      const service = await this.getServiceDefinition(serviceId);
      if (!service) throw new Error(`Service ${serviceId} not found`);

      // 2. Find Endpoint
      const endpoint = service.interface.endpoints.find(e => e.name === endpointName);
      if (!endpoint) throw new Error(`Endpoint ${endpointName} not found`);

      // 3. Find Instance
      const instance = await this.findHealthyInstance(serviceId);
      if (!instance) throw new Error(`No healthy instances for ${serviceId}`);

      // 4. Calculate Cost
      const baseCost = service.pricing.perCallCost || 0;
      const cost = baseCost * endpoint.costMultiplier;
      
      if (options?.maxCost && cost > options.maxCost) throw new Error('Cost exceeded');

      // 5. Authorize Payment
      const auth = await this.wallet.authorizePayment(
          service.providerNodeId,
          BigInt(cost * 1e18), // assuming cost is float, convert to BigInt Wei-like
          { type: 'SERVICE_CALL', serviceId, endpointName }
      );

      // 6. Execute (Mock RPC)
      // In real implementation, this would use the protocol defined (HTTP, WebSocket, Gun)
      // Here we simulate a Gun-based RPC or HTTP fetch
      const result = await this.executeRpc(instance, endpoint, input);

      // 7. Finalize Payment
      await this.wallet.finalizePayment(auth.id);

      return { result, cost, executorNode: instance.nodeId };
  }

  private async getServiceDefinition(id: string): Promise<ServiceDefinition | null> {
      return new Promise((resolve) => {
          this.gun.get('services').get(id).once((data: any) => {
              resolve(data ? data.definition : null);
          });
      });
  }

  private async findHealthyInstance(serviceId: string): Promise<ServiceInstance | null> {
      return new Promise((resolve) => {
          this.gun.get('services').get(serviceId).get('instances').map().once((inst: any) => {
              if (inst && inst.status === 'RUNNING' && inst.health.healthy) {
                  resolve(inst);
                  // Return early if map allows, or just let first one win logic
              }
          });
          // Timeout fallback
          setTimeout(() => resolve(null), 500);
      });
  }

  /**
   * Subscribe to a service stream.
   */
  public async subscribeToService<T>(
      serviceId: string,
      topic: string,
      handler: (data: T) => void
  ): Promise<Subscription> {
      // 1. Get Service Def
      const service = await this.getServiceDefinition(serviceId);
      if (!service) throw new Error(`Service ${serviceId} not found`);

      // 2. Subscribe via Gun
      // We assume the service publishes to `services/<id>/streams/<topic>`
      const streamNode = this.gun.get('services').get(serviceId).get('streams').get(topic);
      
      const listener = (data: any) => {
          if (data) handler(data as T);
      };
      
      streamNode.on(listener);

      return {
          unsubscribe: () => {
              streamNode.off(listener);
          },
          closed: false
      } as Subscription;
  }

  private async executeRpc(instance: ServiceInstance, endpoint: any, input: any): Promise<any> {
      const requestId = generateId('req');
      const request = {
          id: requestId,
          input,
          timestamp: Date.now(),
          responsePath: `requests/${requestId}/response`
      };

      // Put request to instance inbox
      this.gun.get('nodes').get(instance.nodeId).get('inbox').get(requestId).put(request);

      // Wait for response
      return new Promise((resolve, reject) => {
          const timeout = setTimeout(() => {
              reject(new Error('RPC timeout'));
          }, 5000); // 5s timeout

          this.gun.get('requests').get(requestId).get('response').once((response: any) => {
              clearTimeout(timeout);
              if (response) {
                  if (response.error) reject(new Error(response.error));
                  else resolve(response.result);
              }
          });
      });
  }
}
