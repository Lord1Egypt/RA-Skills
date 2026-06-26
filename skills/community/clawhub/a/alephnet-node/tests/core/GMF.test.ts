import { describe, it, expect, beforeEach, jest } from '@jest/globals';
import { GlobalMemoryField } from '../../src/core/GMF';
import { SMFVector, GMFObject } from '../../src/core/types';

describe('GlobalMemoryField', () => {
  let gmf: GlobalMemoryField;
  const mockSmf: SMFVector = Array(16).fill(0) as unknown as SMFVector;
  const mockMetadata = {
    nodeId: 'node-1',
    proposalId: 'prop-1',
    consensusAchieved: true
  };

  beforeEach(() => {
    gmf = new GlobalMemoryField();
  });

  describe('insert', () => {
    it('should create a new object if it does not exist', async () => {
      const obj = await gmf.insert(
        { term: 'test', normalForm: 'test' },
        mockSmf,
        mockMetadata
      );

      expect(obj).toBeDefined();
      expect(obj.semanticObject.normalForm).toBe('test');
      expect(obj.weight).toBe(1.0);
      expect(obj.redundancyScore).toBe(1);
      
      const stored = gmf.getObject(obj.id);
      expect(stored).toEqual(obj);
    });

    it('should update existing object', async () => {
      // First insert
      await gmf.insert(
        { term: 'test', normalForm: 'test' },
        mockSmf,
        mockMetadata
      );
      
      // Second insert (same normalForm)
      const obj = await gmf.insert(
        { term: 'test', normalForm: 'test' },
        mockSmf,
        mockMetadata
      );
      
      expect(obj.weight).toBe(2.0);
      expect(obj.redundancyScore).toBe(2);
    });
  });

  describe('Snapshots', () => {
    it('should create initial snapshot on construction', () => {
      const snapshot = gmf.getLatestSnapshot();
      expect(snapshot).toBeDefined();
      expect(snapshot?.id).toBeGreaterThan(0);
    });

    it('should create new snapshot with correct ID', async () => {
      const initial = gmf.getLatestSnapshot()!;
      await gmf.insert(
        { term: 'test', normalForm: 'test' },
        mockSmf,
        mockMetadata
      );
      
      const newSnapshot = await gmf.createSnapshot();
      expect(newSnapshot.id).toBe(initial.id + 1);
      expect(newSnapshot.objectCount).toBe(1);
      expect(newSnapshot.hash).not.toBe(initial.hash);
    });
  });

  describe('applyDelta', () => {
    it('should apply insert delta', async () => {
      const deltaObj: GMFObject = {
        id: 'new-id',
        semanticObject: { term: 'foo', normalForm: 'foo' },
        weight: 1,
        smf: mockSmf,
        insertedAt: Date.now(),
        proposalId: 'p1',
        redundancyScore: 1,
        metadata: { nodeId: 'n1', consensusAchieved: true }
      };

      const applied = gmf.applyDelta({
        type: 'insert',
        id: 'new-id',
        timestamp: Date.now() + 1000,
        snapshotId: 1,
        data: deltaObj
      });

      expect(applied).toBe(true);
      expect(gmf.getObject('new-id')).toBe(deltaObj);
    });

    it('should apply remove delta', async () => {
        // Setup existing object
        await gmf.insert({ term: 'del', normalForm: 'del' }, mockSmf, mockMetadata);
        const objs = gmf.getAllObjects();
        const id = objs[0].id;

        const applied = gmf.applyDelta({
            type: 'remove',
            id: id,
            timestamp: Date.now() + 1000,
            snapshotId: 1
        });

        expect(applied).toBe(true);
        expect(gmf.getObject(id)).toBeUndefined();
    });

    it('should ignore old deltas', async () => {
        const latestSnapshotTimestamp = gmf.getLatestSnapshot()!.timestamp;
        
        const applied = gmf.applyDelta({
            type: 'insert',
            id: 'old',
            timestamp: latestSnapshotTimestamp - 1000,
            snapshotId: 0,
            data: {}
        });
        
        expect(applied).toBe(false);
    });
  });

  describe('getDeltasSince', () => {
    it('should return recent deltas', async () => {
      const snap1 = gmf.getLatestSnapshot()!;
      
      await gmf.insert({ term: 'a', normalForm: 'a' }, mockSmf, mockMetadata);
      
      const deltas = gmf.getDeltasSince(snap1.id);
      expect(deltas.length).toBe(1); // The insert we just did
      expect(deltas[0].type).toBe('insert');
    });
  });

  describe('verifyState', () => {
    it('should validate matching snapshots', async () => {
      const snap = gmf.getLatestSnapshot()!;
      const result = gmf.verifyState(snap);
      expect(result.valid).toBe(true);
      expect(result.missingDeltas).toBe(false);
    });

    it('should detect unknown snapshot', () => {
      const result = gmf.verifyState({
          id: 999,
          timestamp: 0,
          objectCount: 0,
          hash: 'unknown'
      });
      expect(result.valid).toBe(false);
      expect(result.missingDeltas).toBe(true);
    });

    it('should detect divergence (same ID, diff hash)', () => {
      const snap = gmf.getLatestSnapshot()!;
      const result = gmf.verifyState({
          ...snap,
          hash: 'different-hash'
      });
      expect(result.valid).toBe(false);
      expect(result.missingDeltas).toBe(false);
    });
  });
});
