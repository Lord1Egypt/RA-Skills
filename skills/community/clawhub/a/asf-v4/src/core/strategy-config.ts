/**
 * Core Strategy Interface
 * 
 * @module asf-v4/core/strategy
 */

export interface Strategy {
  name: string;
  type: string;
  config?: any;
}

export interface OrchestrationStrategy extends Strategy {
  config: {
    transactionProtocol: boolean;
    incrementalDelivery: boolean;
    executionOrder: string[];
    syncPoints: string[];
    rollbackStrategy: string;
    timeout: {
      perModule: number;
      total: number;
    };
  };
}

export interface StandardStrategy extends Strategy {
  config: {
    transactionProtocol: boolean;
    incrementalDelivery: boolean;
  };
}