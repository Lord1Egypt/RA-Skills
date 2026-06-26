import { SkillDefinition, DSNNodeConfig, SemanticDomain, RoutingDecision } from '../core/types';
import { SMFVector } from '../common/types';
import { determineDomain } from '../common/math';
import { SMF_AXIS_MAPPING } from '../services/EmbeddingService';

/**
 * Skill Registry
 * 
 * Manages the registration, discovery, and routing of semantic skills in the AlephNet mesh.
 * Implements "Requirement 5: AlephNet Skill Registry" and "Requirement 6: Named Servers & Semantic Mesh Routing".
 */
export class SkillRegistry {
  private localSkills: Map<string, SkillDefinition> = new Map();

  constructor(
      private gun: any,
      private localNodeId: string
  ) {
      // Optimistically subscribe to local node's hosted skills to keep cache warm
      this.gun.get('nodes').get(this.localNodeId).get('hostedSkills').map().on((skillName: string) => {
          if (skillName && typeof skillName === 'string') {
               this.gun.get('skills').get(skillName).once((def: SkillDefinition) => {
                   if (def) this.localSkills.set(skillName, def);
               });
          }
      });
  }

  /**
   * Register a new skill on the network.
   * Maps to Requirement 5.
   */
  public async registerSkill(skill: SkillDefinition): Promise<void> {
    if (!skill.name || !skill.executionLocation) {
        throw new Error('Invalid skill definition: name and executionLocation are required.');
    }

    // 1. Publish Skill Definition to global `skills` graph
    await new Promise<void>((resolve, reject) => {
        this.gun.get('skills').get(skill.name).put(skill, (ack: any) => {
            if (ack.err) reject(new Error(ack.err));
            else resolve();
        });
    });

    // 2. Register this node as a provider if we are hosting it
    // We update our own node record to claim we host this skill.
    // In a real generic registry, we might verify this, but here we trust the node calling register.
    if (skill.executionLocation === 'SERVER') {
        this.localSkills.set(skill.name, skill); // Cache locally
        
        // Add to hostedSkills list. Note: Gun lists are usually graphs. 
        // We set keys in a set for easy lookup.
        this.gun.get('nodes').get(this.localNodeId).get('hostedSkills').set(skill.name);
    }
  }

  /**
   * Get a skill definition by name.
   */
  public async getSkill(name: string): Promise<SkillDefinition | null> {
      if (this.localSkills.has(name)) return this.localSkills.get(name)!;

      return new Promise((resolve) => {
          this.gun.get('skills').get(name).once((data: any) => {
              // Gun returns the object plus metadata (_), strip if needed or cast
              if (!data) resolve(null);
              else {
                  // Ensure clean object (Gun adds garbage sometimes)
                  const { _, ...cleanData } = data; 
                  resolve(cleanData as SkillDefinition);
              }
          });
      });
  }

  /**
   * Find the best node to execute a skill based on semantic relevance.
   * Maps to Requirement 6: Named Servers & Semantic Mesh Routing.
   */
  public async findBestProvider(
      skillName: string, 
      contextSmf?: SMFVector
  ): Promise<RoutingDecision | null> {
      
      const skill = await this.getSkill(skillName);
      if (!skill) return null;

      // If executionLocation is CLIENT, we can't route to a server node generally.
      // But we assume this method is called to find a *server* provider or a delegate.
      if (skill.executionLocation === 'CLIENT') {
          // Warning or handling? Assuming we return null as "no remote provider needed/possible"
          // unless we are looking for a specific client?
          // For now, assume we look for server nodes.
          // If the skill is client-side, the caller handles it locally.
          return null; 
      }

      // We scan nodes. In a large network, we would rely on a 'providers' index on the skill
      // e.g., gun.get('skills').get(name).get('providers').map()
      // But strictly following the design doc example which scans nodes (filtered).
      
      const candidates: Array<{ 
          nodeId: string; 
          relevance: number; 
          load: number;
          semanticDomainMatch: boolean;
          primeDomainOverlap: number;
      }> = [];

      await new Promise<void>((resolve) => {
          let checkedCount = 0;
          let nodeCount = 0;
          const TIMEOUT = 1500; // ms to gather candidates
          let resolved = false;

          const done = () => {
              if (!resolved) {
                  resolved = true;
                  resolve();
              }
          };

          const checkDone = () => {
             // Heuristic: if we have enough candidates or time passes
          };

          // Set a strict timeout to stop gathering
          setTimeout(done, TIMEOUT);

          this.gun.get('nodes').map().once((node: DSNNodeConfig, nodeId: string) => {
              if (resolved) return;
              if (!node || !node.nodeId) return; // invalid data
              
              // Check if node is online and hosts the skill
              // Accessing hostedSkills might be a sub-query if it's a huge set, 
              // but here we assume it's loaded or we check the separate graph.
              // Gun `map()` iterates direct properties. `hostedSkills` is likely a reference.
              // We need to check if `hostedSkills` contains `skillName`.
              
              // Optimizing: Check status first
              if (node.status !== 'ONLINE') return;

              // Check if node hosts the skill.
              // In Gun, we'd check `gun.get('nodes').get(id).get('hostedSkills').get(skillName)`
              // But inside map(), we might not have the full set loaded.
              // For safety, we do a quick look up.
              this.gun.get('nodes').get(nodeId).get('hostedSkills').get(skillName).once((exists: any) => {
                  if (exists) {
                      // It hosts the skill. Calculate relevance.
                      const relevance = this.calculateRelevance(contextSmf, node);
                      const primeOverlap = this.calculatePrimeOverlap(skill.primeDomain, node.primeDomain);
                      const domainMatch = node.semanticDomain === skill.semanticDomain;

                      candidates.push({
                          nodeId: node.nodeId,
                          relevance,
                          load: node.loadIndex || 0,
                          semanticDomainMatch: domainMatch,
                          primeDomainOverlap: primeOverlap
                      });
                  }
              });
          });
      });

      if (candidates.length === 0) return null;

      // Sort by score: (relevance * 0.7) + ((100 - load)/100 * 0.3)
      // Bonus for domain match? Design doc: "relevance" accounts for smf/domain.
      candidates.sort((a, b) => {
          const scoreA = (a.relevance * 0.7) + ((100 - a.load)/100 * 0.3);
          const scoreB = (b.relevance * 0.7) + ((100 - b.load)/100 * 0.3);
          return scoreB - scoreA;
      });

      const winner = candidates[0];
      const fallbacks = candidates.slice(1, 4).map(c => c.nodeId);

      return {
          targetNodeId: winner.nodeId,
          relevanceScore: winner.relevance,
          semanticDomainMatch: winner.semanticDomainMatch,
          primeDomainOverlap: winner.primeDomainOverlap,
          loadFactor: winner.load,
          fallbackNodes: fallbacks
      };
  }

  /**
   * Calculate routing relevance between a request (SMF) and a node.
   */
  public calculateRelevance(requestSmf: SMFVector | undefined, node: DSNNodeConfig): number {
      if (!requestSmf) return 0.5; // Default if no context

      // 1. Domain Match
      const reqDomain = determineDomain(requestSmf);
      let score = 0.5;
      
      // Bonus for exact domain match
      if (reqDomain === node.semanticDomain) {
          score += 0.2;
      }

      // 2. SMF Alignment
      // Check if request is active in the axes the node specializes in (node.smfAxes).
      // node.smfAxes is number[] (indices 0-15)
      if (node.smfAxes && node.smfAxes.length > 0) {
          let alignment = 0;
          let totalMag = 0;
          
          requestSmf.forEach((val: number, i: number) => {
              const mag = Math.abs(val);
              totalMag += mag;
              if (node.smfAxes.includes(i)) {
                  alignment += mag;
              }
          });
          
          const axisScore = totalMag > 0 ? alignment / totalMag : 0;
          // Weighted mix
          score = (score * 0.6) + (axisScore * 0.4);
      }

      return Math.min(1.0, Math.max(0.0, score));
  }

  private calculatePrimeOverlap(skillPrimes: number[], nodePrimes: number[]): number {
      if (!skillPrimes || !nodePrimes) return 0;
      const intersection = skillPrimes.filter(p => nodePrimes.includes(p));
      return intersection.length;
  }
}
