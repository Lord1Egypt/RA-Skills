import { HealthCheckable, HealthStatus } from '../common/types';

export class HealthCheckService {
  private checks: Map<string, HealthCheckable> = new Map();

  registerCheck(name: string, checkable: HealthCheckable): void {
    this.checks.set(name, checkable);
  }

  async checkAll(): Promise<Record<string, HealthStatus>> {
    const results: Record<string, HealthStatus> = {};
    
    for (const [name, check] of this.checks) {
      try {
        results[name] = await check.healthCheck();
      } catch (error: any) {
        results[name] = {
          status: 'unhealthy',
          lastCheck: Date.now(),
          details: { error: error.message }
        };
      }
    }
    
    return results;
  }

  async isHealthy(): Promise<boolean> {
    const results = await this.checkAll();
    return Object.values(results).every(r => r.status === 'healthy');
  }
}
