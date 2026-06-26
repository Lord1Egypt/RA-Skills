# Correlation Plugin Research

## Background

The correlation plugin emerged from the need to enhance memory search capabilities in OpenClaw by automatically retrieving related contexts when querying memory. Traditional memory search returns results directly related to the query terms, but often misses contextual information that is crucial for making informed decisions.

## Problem Statement

When users search for specific topics in OpenClaw's memory system, they often need additional context that isn't directly captured by the search terms. For example, when searching for "backup error," it's valuable to also retrieve information about "last backup time," "recovery procedures," and "similar errors" because these contexts consistently matter together.

## Research Findings

### 1. Contextual Decision Making

Research in cognitive science shows that human decision-making relies heavily on contextual information. When presented with a problem, experts automatically recall related experiences, constraints, and solutions that inform their approach.

### 2. Information Retrieval Enhancement

Traditional information retrieval systems focus on keyword matching and relevance scoring. However, for decision support systems like OpenClaw, it's essential to retrieve not just relevant information but also correlated information that enhances understanding.

### 3. Rule-Based Correlation

The correlation plugin implements a rule-based approach where domain experts can define relationships between concepts. These rules specify that when certain contexts or keywords are detected, additional related information should be retrieved.

### 4. Confidence Scoring

Each correlation rule includes a confidence score that determines how strongly the relationship should be enforced. This allows for nuanced correlations that adapt to different situations.

## Technical Approach

### Merged Architecture

The plugin combines two previous approaches:
1. **SDK-native tool registration** (from `correlation-rules-mem`) — proper OpenClaw plugin lifecycle
2. **Rich matching logic** (from `correlation-memory`) — keyword matching, confidence filtering, lenient/strict modes

### Matching Modes

Three matching modes provide flexibility for different use cases:
- `auto` (default) — keyword + context matching
- `strict` — exact keyword match only
- `lenient` — fuzzy matching for broad queries

## Related Work

### Coolmanns Architecture

The correlation plugin draws inspiration from the Coolmanns architecture for context-aware systems, which emphasizes the importance of retrieving related information to support decision-making processes.

### Previous Implementations

Two earlier implementations informed the current approach:
1. `correlation-rules-mem` - Focused on proper plugin lifecycle integration
2. `correlation-memory` - Implemented rich matching logic and confidence filtering

## Evaluation

Initial testing showed that the correlation plugin significantly improves the quality of information retrieval for complex decision-making scenarios by automatically including relevant contextual information.

## Future Directions

1. Machine learning approaches to automatically discover correlation rules
2. Integration with external knowledge bases
3. Adaptive confidence scoring based on user feedback
4. Cross-domain correlation rules

## Sources

- Cognitive science research on contextual decision making
- Information retrieval literature on query expansion
- Coolmanns architecture for context-aware systems
- OpenClaw internal development discussions and experiments