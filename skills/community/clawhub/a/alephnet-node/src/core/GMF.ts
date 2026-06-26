import {
  GMFObject,
  GMFSnapshot,
  GMFDelta,
  SMFVector
} from '../core/types';
import { createHash } from 'crypto';

/**
 * Global Memory Field (GMF)
 * 
 * Represents the shared semantic state of the AlephNet.
 * Manages Objects (semantic units), Snapshots (state checkpoints), and Deltas (changes).
 * 
 * Implements "Semantic State Synchronization".
 */
export class GlobalMemoryField {
  private objects: Map<string, GMFObject> = new Map();
  private snapshots: Map<number, GMFSnapshot> = new Map();
  private deltas: GMFDelta[] = [];
  
  private currentSnapshotId: number = 0;
  private lastSnapshotHash: string = '00000000000000000000000000000000';

  constructor() {
    // Initialize with genesis snapshot synchronously
    this.createSnapshotSync();
  }

  // --- Data Structure Management ---

  /**
   * Insert or update an object in the GMF.
   * This is usually called after consensus is achieved.
   */
  public async insert(
    semanticObject: { term: any; normalForm: string },
    smf: SMFVector,
    metadata: { nodeId: string; proposalId: string; consensusAchieved: boolean },
    initialWeight: number = 1.0
  ): Promise<GMFObject> {
    const id = await this.generateObjectId(semanticObject.normalForm);
    
    const existing = this.objects.get(id);
    let deltaType: 'insert' | 'update_weight' = 'insert';

    let obj: GMFObject;

    if (existing) {
      // Update existing
      deltaType = 'update_weight';
      obj = {
        ...existing,
        weight: existing.weight + initialWeight, // simplistic accumulation
        redundancyScore: existing.redundancyScore + 1,
        // Update SMF? Usually SMF is intrinsic to the object's meaning. 
        // If meaning changes, it's a new object.
      };
    } else {
      // Create new
      obj = {
        id,
        semanticObject,
        weight: initialWeight,
        smf,
        insertedAt: Date.now(),
        proposalId: metadata.proposalId,
        redundancyScore: 1,
        metadata
      };
    }

    this.objects.set(id, obj);
    this.recordDelta(deltaType, id, obj);

    return obj;
  }

  public getObject(id: string): GMFObject | undefined {
    return this.objects.get(id);
  }

  public getAllObjects(): GMFObject[] {
    return Array.from(this.objects.values());
  }

  // --- Synchronization & Snapshots ---

  /**
   * Create a snapshot of the current state.
   * Snapshots are used for synchronization checkpoints.
   */
  public async createSnapshot(): Promise<GMFSnapshot> {
    return this.createSnapshotSync();
  }

  public getSnapshot(id: number): GMFSnapshot | undefined {
    return this.snapshots.get(id);
  }

  public getLatestSnapshot(): GMFSnapshot | undefined {
    return this.snapshots.get(this.currentSnapshotId);
  }

  /**
   * Apply a delta from a peer.
   */
  public applyDelta(delta: GMFDelta): boolean {
    if (delta.timestamp < (this.getLatestSnapshot()?.timestamp || 0)) {
       // Old delta, maybe ignore or check if needed
       return false;
    }

    if (delta.type === 'insert' || delta.type === 'update_weight') {
       if (!delta.data) return false;
       // We assume delta.data contains the GMFObject properties needed
       // But typically we need to verify consensus before applying.
       // This method assumes trusted source or verification happened elsewhere.
       const obj = delta.data as GMFObject;
       this.objects.set(delta.id, obj);
       this.deltas.push(delta);
       return true;
    } else if (delta.type === 'remove') {
       this.objects.delete(delta.id);
       this.deltas.push(delta);
       return true;
    }
    return false;
  }

  /**
   * Get deltas since a specific snapshot.
   * Returns deltas with timestamp >= snapshot.timestamp (inclusive)
   */
  public getDeltasSince(snapshotId: number): GMFDelta[] {
    const snapshot = this.snapshots.get(snapshotId);
    if (!snapshot) return []; // Or throw, or return all if snapshotId is 0
    return this.deltas.filter(d => d.timestamp >= snapshot.timestamp);
  }

  // --- Internal Helpers ---

  private recordDelta(type: 'insert' | 'update_weight' | 'remove', id: string, data?: any) {
    const delta: GMFDelta = {
      type,
      id,
      timestamp: Date.now(),
      snapshotId: this.currentSnapshotId,
      data
    };
    this.deltas.push(delta);
  }

  private async generateObjectId(content: string): Promise<string> {
    return this.hashStringSync(content);
  }

  private hashStringSync(content: string): string {
    const hash = createHash('sha256');
    hash.update(content);
    return hash.digest('hex');
  }

  /**
   * Synchronous snapshot creation for constructor
   */
  private createSnapshotSync(): GMFSnapshot {
    const timestamp = Date.now();
    const objectCount = this.objects.size;
    
    const sortedIds = Array.from(this.objects.keys()).sort();
    const stateStr = sortedIds.map(id => {
      const obj = this.objects.get(id)!;
      return `${id}:${obj.weight.toFixed(4)}`;
    }).join('|');
    
    const hash = this.hashStringSync(stateStr + this.lastSnapshotHash);
    
    this.currentSnapshotId++;
    const snapshot: GMFSnapshot = {
      id: this.currentSnapshotId,
      timestamp,
      objectCount,
      hash
    };

    this.snapshots.set(this.currentSnapshotId, snapshot);
    this.lastSnapshotHash = hash;
    
    return snapshot;
  }

  // --- Sync Logic Stub ---
  // The design doc mentions "Coherence-gated writes". 
  // This class manages the STORE. The Consensus module governs the WRITE access.
  // But we can add a method to verify state against a peer's snapshot.

  public verifyState(peerSnapshot: GMFSnapshot): { valid: boolean; missingDeltas: boolean } {
    const mySnapshot = this.getSnapshot(peerSnapshot.id);
    if (!mySnapshot) {
       // We don't have this snapshot history
       return { valid: false, missingDeltas: true };
    }
    if (mySnapshot.hash !== peerSnapshot.hash) {
      // Divergence detected
      return { valid: false, missingDeltas: false };
    }
    return { valid: true, missingDeltas: false };
  }
}
