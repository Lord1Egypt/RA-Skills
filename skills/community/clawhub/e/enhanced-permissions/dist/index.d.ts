/**
 * OpenClaw Enhanced Permissions Module
 *
 * Export all modules for easy importing
 */
export * from './types';
export { PermissionChecker, defaultPermissionChecker } from './permission-checker';
export { ToolRegistry, defaultToolRegistry } from './tool-registry';
export { readFileTool, listDirectoryTool, writeFileTool, editFileTool, execCommandTool, deleteFileTool, registerAllEnhancedTools } from './enhanced-tools';
export { showConfirmationDialog, showDestructiveWarning, smartConfirm, batchConfirm } from './confirmation-dialog';
export { AuditLogger, defaultAuditLogger } from './audit-logger';
export { registerEnhancedOpenClawTools, executeToolWithPermission, enhancedReadTool, enhancedWriteTool, enhancedEditTool, enhancedExecTool, enhancedWebSearchTool, enhancedWebFetchTool, readSchema, writeSchema, editSchema, execSchema, webSearchSchema, webFetchSchema } from './openclaw-adapter';
export { MemoryManager, defaultMemoryManager, getHotnessDelta, calculateDecayedHotness, shouldArchive, isEligibleForRecall } from './memory-manager';
export { OpenVikingService, defaultOpenVikingService } from './openviking-integration';
export { VersionControlManager, defaultVersionControl, VersionEntry, VersionedMemory, VersionOptions, HistoryQuery } from './version-control';
export { AutoOrganizer, defaultAutoOrganizer, AutoOrganizeOptions, AutoOrganizeResult } from './auto-organizer';
export { DuplicateDetector, defaultDuplicateDetector, DuplicatePair, DuplicateOptions } from './duplicate-detector';
export { MemoryMerger, defaultMemoryMerger, MergeStrategy, MergeResult } from './memory-merger';
export { ConversationAnalyzer, defaultConversationAnalyzer, ConversationContext, Message, AnalysisOptions } from './conversation-analyzer';
export { SuggestionGenerator, defaultSuggestionGenerator, MemorySuggestion, SuggestionOptions } from './suggestion-generator';
export { SuggestionTrigger, defaultSuggestionTrigger, TriggerConfig, TriggerState } from './suggestion-trigger';
export { EntityType, RelationType, GraphEntity, GraphRelation, GraphQuery, GraphPath, GraphStats, ConnectedEntity } from './graph-types';
export { KnowledgeGraph, defaultKnowledgeGraph } from './knowledge-graph';
export { EntityExtractor, defaultEntityExtractor, ExtractedEntity, ExtractionOptions } from './entity-extractor';
export { RelationInferenceEngine, createInferenceEngine, InferredRelation } from './relation-inference';
//# sourceMappingURL=index.d.ts.map