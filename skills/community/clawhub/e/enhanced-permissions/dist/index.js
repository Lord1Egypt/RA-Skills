"use strict";
/**
 * OpenClaw Enhanced Permissions Module
 *
 * Export all modules for easy importing
 */
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __exportStar = (this && this.__exportStar) || function(m, exports) {
    for (var p in m) if (p !== "default" && !Object.prototype.hasOwnProperty.call(exports, p)) __createBinding(exports, m, p);
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.defaultConversationAnalyzer = exports.ConversationAnalyzer = exports.MergeStrategy = exports.defaultMemoryMerger = exports.MemoryMerger = exports.defaultDuplicateDetector = exports.DuplicateDetector = exports.defaultAutoOrganizer = exports.AutoOrganizer = exports.defaultVersionControl = exports.VersionControlManager = exports.defaultOpenVikingService = exports.OpenVikingService = exports.isEligibleForRecall = exports.shouldArchive = exports.calculateDecayedHotness = exports.getHotnessDelta = exports.defaultMemoryManager = exports.MemoryManager = exports.webFetchSchema = exports.webSearchSchema = exports.execSchema = exports.editSchema = exports.writeSchema = exports.readSchema = exports.enhancedWebFetchTool = exports.enhancedWebSearchTool = exports.enhancedExecTool = exports.enhancedEditTool = exports.enhancedWriteTool = exports.enhancedReadTool = exports.executeToolWithPermission = exports.registerEnhancedOpenClawTools = exports.defaultAuditLogger = exports.AuditLogger = exports.batchConfirm = exports.smartConfirm = exports.showDestructiveWarning = exports.showConfirmationDialog = exports.registerAllEnhancedTools = exports.deleteFileTool = exports.execCommandTool = exports.editFileTool = exports.writeFileTool = exports.listDirectoryTool = exports.readFileTool = exports.defaultToolRegistry = exports.ToolRegistry = exports.defaultPermissionChecker = exports.PermissionChecker = void 0;
exports.createInferenceEngine = exports.RelationInferenceEngine = exports.defaultEntityExtractor = exports.EntityExtractor = exports.defaultKnowledgeGraph = exports.KnowledgeGraph = exports.RelationType = exports.EntityType = exports.defaultSuggestionTrigger = exports.SuggestionTrigger = exports.defaultSuggestionGenerator = exports.SuggestionGenerator = void 0;
// Types
__exportStar(require("./types"), exports);
// Permission Checker
var permission_checker_1 = require("./permission-checker");
Object.defineProperty(exports, "PermissionChecker", { enumerable: true, get: function () { return permission_checker_1.PermissionChecker; } });
Object.defineProperty(exports, "defaultPermissionChecker", { enumerable: true, get: function () { return permission_checker_1.defaultPermissionChecker; } });
// Tool Registry
var tool_registry_1 = require("./tool-registry");
Object.defineProperty(exports, "ToolRegistry", { enumerable: true, get: function () { return tool_registry_1.ToolRegistry; } });
Object.defineProperty(exports, "defaultToolRegistry", { enumerable: true, get: function () { return tool_registry_1.defaultToolRegistry; } });
// Enhanced Tools (Basic)
var enhanced_tools_1 = require("./enhanced-tools");
Object.defineProperty(exports, "readFileTool", { enumerable: true, get: function () { return enhanced_tools_1.readFileTool; } });
Object.defineProperty(exports, "listDirectoryTool", { enumerable: true, get: function () { return enhanced_tools_1.listDirectoryTool; } });
Object.defineProperty(exports, "writeFileTool", { enumerable: true, get: function () { return enhanced_tools_1.writeFileTool; } });
Object.defineProperty(exports, "editFileTool", { enumerable: true, get: function () { return enhanced_tools_1.editFileTool; } });
Object.defineProperty(exports, "execCommandTool", { enumerable: true, get: function () { return enhanced_tools_1.execCommandTool; } });
Object.defineProperty(exports, "deleteFileTool", { enumerable: true, get: function () { return enhanced_tools_1.deleteFileTool; } });
Object.defineProperty(exports, "registerAllEnhancedTools", { enumerable: true, get: function () { return enhanced_tools_1.registerAllEnhancedTools; } });
// Confirmation Dialog
var confirmation_dialog_1 = require("./confirmation-dialog");
Object.defineProperty(exports, "showConfirmationDialog", { enumerable: true, get: function () { return confirmation_dialog_1.showConfirmationDialog; } });
Object.defineProperty(exports, "showDestructiveWarning", { enumerable: true, get: function () { return confirmation_dialog_1.showDestructiveWarning; } });
Object.defineProperty(exports, "smartConfirm", { enumerable: true, get: function () { return confirmation_dialog_1.smartConfirm; } });
Object.defineProperty(exports, "batchConfirm", { enumerable: true, get: function () { return confirmation_dialog_1.batchConfirm; } });
// Audit Logger
var audit_logger_1 = require("./audit-logger");
Object.defineProperty(exports, "AuditLogger", { enumerable: true, get: function () { return audit_logger_1.AuditLogger; } });
Object.defineProperty(exports, "defaultAuditLogger", { enumerable: true, get: function () { return audit_logger_1.defaultAuditLogger; } });
// OpenClaw Adapter
var openclaw_adapter_1 = require("./openclaw-adapter");
Object.defineProperty(exports, "registerEnhancedOpenClawTools", { enumerable: true, get: function () { return openclaw_adapter_1.registerEnhancedOpenClawTools; } });
Object.defineProperty(exports, "executeToolWithPermission", { enumerable: true, get: function () { return openclaw_adapter_1.executeToolWithPermission; } });
Object.defineProperty(exports, "enhancedReadTool", { enumerable: true, get: function () { return openclaw_adapter_1.enhancedReadTool; } });
Object.defineProperty(exports, "enhancedWriteTool", { enumerable: true, get: function () { return openclaw_adapter_1.enhancedWriteTool; } });
Object.defineProperty(exports, "enhancedEditTool", { enumerable: true, get: function () { return openclaw_adapter_1.enhancedEditTool; } });
Object.defineProperty(exports, "enhancedExecTool", { enumerable: true, get: function () { return openclaw_adapter_1.enhancedExecTool; } });
Object.defineProperty(exports, "enhancedWebSearchTool", { enumerable: true, get: function () { return openclaw_adapter_1.enhancedWebSearchTool; } });
Object.defineProperty(exports, "enhancedWebFetchTool", { enumerable: true, get: function () { return openclaw_adapter_1.enhancedWebFetchTool; } });
Object.defineProperty(exports, "readSchema", { enumerable: true, get: function () { return openclaw_adapter_1.readSchema; } });
Object.defineProperty(exports, "writeSchema", { enumerable: true, get: function () { return openclaw_adapter_1.writeSchema; } });
Object.defineProperty(exports, "editSchema", { enumerable: true, get: function () { return openclaw_adapter_1.editSchema; } });
Object.defineProperty(exports, "execSchema", { enumerable: true, get: function () { return openclaw_adapter_1.execSchema; } });
Object.defineProperty(exports, "webSearchSchema", { enumerable: true, get: function () { return openclaw_adapter_1.webSearchSchema; } });
Object.defineProperty(exports, "webFetchSchema", { enumerable: true, get: function () { return openclaw_adapter_1.webFetchSchema; } });
// Memory Manager
var memory_manager_1 = require("./memory-manager");
Object.defineProperty(exports, "MemoryManager", { enumerable: true, get: function () { return memory_manager_1.MemoryManager; } });
Object.defineProperty(exports, "defaultMemoryManager", { enumerable: true, get: function () { return memory_manager_1.defaultMemoryManager; } });
Object.defineProperty(exports, "getHotnessDelta", { enumerable: true, get: function () { return memory_manager_1.getHotnessDelta; } });
Object.defineProperty(exports, "calculateDecayedHotness", { enumerable: true, get: function () { return memory_manager_1.calculateDecayedHotness; } });
Object.defineProperty(exports, "shouldArchive", { enumerable: true, get: function () { return memory_manager_1.shouldArchive; } });
Object.defineProperty(exports, "isEligibleForRecall", { enumerable: true, get: function () { return memory_manager_1.isEligibleForRecall; } });
// OpenViking Integration
var openviking_integration_1 = require("./openviking-integration");
Object.defineProperty(exports, "OpenVikingService", { enumerable: true, get: function () { return openviking_integration_1.OpenVikingService; } });
Object.defineProperty(exports, "defaultOpenVikingService", { enumerable: true, get: function () { return openviking_integration_1.defaultOpenVikingService; } });
// Version Control
var version_control_1 = require("./version-control");
Object.defineProperty(exports, "VersionControlManager", { enumerable: true, get: function () { return version_control_1.VersionControlManager; } });
Object.defineProperty(exports, "defaultVersionControl", { enumerable: true, get: function () { return version_control_1.defaultVersionControl; } });
// Auto Organization
var auto_organizer_1 = require("./auto-organizer");
Object.defineProperty(exports, "AutoOrganizer", { enumerable: true, get: function () { return auto_organizer_1.AutoOrganizer; } });
Object.defineProperty(exports, "defaultAutoOrganizer", { enumerable: true, get: function () { return auto_organizer_1.defaultAutoOrganizer; } });
// Duplicate Detection
var duplicate_detector_1 = require("./duplicate-detector");
Object.defineProperty(exports, "DuplicateDetector", { enumerable: true, get: function () { return duplicate_detector_1.DuplicateDetector; } });
Object.defineProperty(exports, "defaultDuplicateDetector", { enumerable: true, get: function () { return duplicate_detector_1.defaultDuplicateDetector; } });
// Memory Merger
var memory_merger_1 = require("./memory-merger");
Object.defineProperty(exports, "MemoryMerger", { enumerable: true, get: function () { return memory_merger_1.MemoryMerger; } });
Object.defineProperty(exports, "defaultMemoryMerger", { enumerable: true, get: function () { return memory_merger_1.defaultMemoryMerger; } });
Object.defineProperty(exports, "MergeStrategy", { enumerable: true, get: function () { return memory_merger_1.MergeStrategy; } });
// Smart Suggestions
var conversation_analyzer_1 = require("./conversation-analyzer");
Object.defineProperty(exports, "ConversationAnalyzer", { enumerable: true, get: function () { return conversation_analyzer_1.ConversationAnalyzer; } });
Object.defineProperty(exports, "defaultConversationAnalyzer", { enumerable: true, get: function () { return conversation_analyzer_1.defaultConversationAnalyzer; } });
var suggestion_generator_1 = require("./suggestion-generator");
Object.defineProperty(exports, "SuggestionGenerator", { enumerable: true, get: function () { return suggestion_generator_1.SuggestionGenerator; } });
Object.defineProperty(exports, "defaultSuggestionGenerator", { enumerable: true, get: function () { return suggestion_generator_1.defaultSuggestionGenerator; } });
var suggestion_trigger_1 = require("./suggestion-trigger");
Object.defineProperty(exports, "SuggestionTrigger", { enumerable: true, get: function () { return suggestion_trigger_1.SuggestionTrigger; } });
Object.defineProperty(exports, "defaultSuggestionTrigger", { enumerable: true, get: function () { return suggestion_trigger_1.defaultSuggestionTrigger; } });
// Graph Memory (Phase 5)
var graph_types_1 = require("./graph-types");
Object.defineProperty(exports, "EntityType", { enumerable: true, get: function () { return graph_types_1.EntityType; } });
Object.defineProperty(exports, "RelationType", { enumerable: true, get: function () { return graph_types_1.RelationType; } });
var knowledge_graph_1 = require("./knowledge-graph");
Object.defineProperty(exports, "KnowledgeGraph", { enumerable: true, get: function () { return knowledge_graph_1.KnowledgeGraph; } });
Object.defineProperty(exports, "defaultKnowledgeGraph", { enumerable: true, get: function () { return knowledge_graph_1.defaultKnowledgeGraph; } });
var entity_extractor_1 = require("./entity-extractor");
Object.defineProperty(exports, "EntityExtractor", { enumerable: true, get: function () { return entity_extractor_1.EntityExtractor; } });
Object.defineProperty(exports, "defaultEntityExtractor", { enumerable: true, get: function () { return entity_extractor_1.defaultEntityExtractor; } });
var relation_inference_1 = require("./relation-inference");
Object.defineProperty(exports, "RelationInferenceEngine", { enumerable: true, get: function () { return relation_inference_1.RelationInferenceEngine; } });
Object.defineProperty(exports, "createInferenceEngine", { enumerable: true, get: function () { return relation_inference_1.createInferenceEngine; } });
//# sourceMappingURL=index.js.map