import { DSNNodeConfig, RoutingDecision, AgentTriggerEvent, SemanticDomain } from '../core/types';

/**
 * Service responsible for calculating optimal routing paths for requests
 * based on semantic domain matching, relevance scores, and node load.
 */
export class SemanticRoutingService {
  constructor() {}

  /**
   * Calculates the best route for a given trigger event among a list of candidates.
   */
  calculateRoute(
    event: AgentTriggerEvent, 
    candidates: DSNNodeConfig[]
  ): RoutingDecision {
    const targetDomain = event.routing?.preferredDomain || 'cognitive';
    const requiredSmf = event.routing?.requiredSmfAxes;

    // Filter by domain match (strict or loose)
    const matchingNodes = candidates.filter(node => 
      node.status === 'ONLINE' && 
      (node.semanticDomain === targetDomain || !event.routing?.preferredDomain)
    );

    if (matchingNodes.length === 0) {
      // Fallback: just pick any online node or return empty
      // In reality, might search for 'meta' domain nodes
      return {
        targetNodeId: '',
        relevanceScore: 0,
        semanticDomainMatch: false,
        primeDomainOverlap: 0,
        loadFactor: 1,
        fallbackNodes: []
      };
    }

    // Sort by simple heuristic: load (lower is better)
    // In future: use SMF cosine similarity for relevance
    matchingNodes.sort((a, b) => a.loadIndex - b.loadIndex);

    const bestNode = matchingNodes[0];

    return {
      targetNodeId: bestNode.nodeId,
      relevanceScore: 1.0, // Mock
      semanticDomainMatch: true,
      primeDomainOverlap: 1.0, // Mock
      loadFactor: bestNode.loadIndex,
      fallbackNodes: matchingNodes.slice(1).map(n => n.nodeId)
    };
  }
}
