import { describe, it, expect } from 'vitest';
import { RuleSignalModel } from '../src/signals/rule-model.js';

describe('RuleSignalModel', () => {
  it('detects bearish hack news', async () => {
    const m = new RuleSignalModel();
    const s = await m.analyze({ id:'1', ts:1, source:'x', title:'Binance suffers hack', body:'major exploit on BSC', url:'', lang:'en' });
    expect(s.sentiment).toBeLessThan(0);
    expect(s.confidence).toBeGreaterThan(0.5);
  });
});
