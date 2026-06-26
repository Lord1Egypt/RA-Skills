import { AlephWallet } from '../infra/Wallet';

export interface ReputationScore {
  nodeId: string;
  score: number; // 0.0 to 1.0
  interactions: number;
  lastInteraction: number;
  history: number[]; // Recent scores
}

export class ReputationService {
  private scores: Map<string, ReputationScore> = new Map();

  constructor(private gun: any) {
    // Load scores from Gun
    this.gun.get('reputation').map().on((data: any, key: string) => {
        if (data) {
            this.scores.set(key, data);
        }
    });
  }

  public getScore(nodeId: string): number {
    const record = this.scores.get(nodeId);
    return record ? record.score : 0.5; // Default neutral reputation
  }

  public async updateScore(nodeId: string, delta: number): Promise<void> {
    const record = this.scores.get(nodeId) || {
        nodeId,
        score: 0.5,
        interactions: 0,
        lastInteraction: 0,
        history: []
    };

    // Update score with decay or weight
    // Simple moving average for now
    const weight = 0.1;
    const newScore = Math.max(0, Math.min(1, record.score * (1 - weight) + (record.score + delta) * weight));
    
    record.score = newScore;
    record.interactions++;
    record.lastInteraction = Date.now();
    record.history.push(newScore);
    if (record.history.length > 10) record.history.shift();

    this.scores.set(nodeId, record);
    
    // Persist
    return new Promise((resolve) => {
        this.gun.get('reputation').get(nodeId).put(record, (ack: any) => resolve());
    });
  }

  public async recordInteraction(nodeId: string, success: boolean): Promise<void> {
      const delta = success ? 0.05 : -0.1;
      await this.updateScore(nodeId, delta);
  }
}
