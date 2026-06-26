import { describe, it, expect, beforeEach, jest } from '@jest/globals';
import { ReputationService } from '../../src/services/ReputationService';

describe('ReputationService', () => {
  let service: ReputationService;
  let mockGun: any;

  beforeEach(() => {
    const mapMock = {
        on: jest.fn()
    };
    mockGun = {
      get: jest.fn().mockReturnThis(),
      map: jest.fn().mockReturnValue(mapMock),
      put: jest.fn((data: any, cb: any) => {
          if (cb) cb({ err: null });
      })
    };
    service = new ReputationService(mockGun);
  });

  it('should initialize with default score', () => {
    expect(service.getScore('node-1')).toBe(0.5);
  });

  it('should update score', async () => {
    // Mock get to return undefined initially (handled by class logic or map)
    // The class logic uses map().on() to populate cache.
    // We can simulate population or just call updateScore which creates record.
    
    await service.updateScore('node-1', 0.1);
    
    // It should have called put
    expect(mockGun.put).toHaveBeenCalled();
    const arg = mockGun.put.mock.calls[0][0];
    expect(arg.score).toBeGreaterThan(0.5);
  });

  it('should record interaction', async () => {
    await service.recordInteraction('node-1', true);
    // Success increases score
    const score1 = service.getScore('node-1');
    expect(score1).toBeGreaterThan(0.5);
    
    await service.recordInteraction('node-1', false);
    // Failure decreases score
    const score2 = service.getScore('node-1');
    expect(score2).toBeLessThan(score1);
  });
});
