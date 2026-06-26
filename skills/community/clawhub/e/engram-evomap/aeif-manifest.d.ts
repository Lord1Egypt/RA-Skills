/**
 * AEIF v1.0 Manifest - Agent Experience Interchange Format
 * 标准化的 Agent 经验胶囊协议类型定义
 */

export interface AEIFCapsule {
  capsuleId: string;           // UUID, unique across the system
  schemaVersion: "1.0";        // AEIF protocol version
  category: string;            // e.g., 'api_debugging', 'package_manager'
  createdAt: string;           // ISO8601 Timestamp
  trustScore: number;          // 0.0 - 1.0 (Higher is more reliable)
  useCount: number;            // How many times this was referenced
  
  triggerSignature: {
    errorPattern: string;      // Regex-compatible feature pattern
    taskIntent: string;        // Semantic intent description
    embedding: number[];       // 384-dimensional vector (all-MiniLM-L6-v2)
  };

  environment: {
    os: string;                // 'darwin', 'linux', 'win32', or 'any'
    runtime: string;           // e.g., 'node@18.x'
    dependencies?: Record<string, string>;
    compatibility: "cross-platform" | "os-specific";
  };

  actionSequence: Array<{
    step: number;
    type: "diagnosis" | "patch" | "config" | "workaround";
    instruction: string;       // Actionable text for the Agent
    codeDiff?: string;         // Optional code patch or command
    rationale: string;         // Why this step is necessary
  }>;

  verificationCriterion: string; // How to verify the fix works
  antipatternWarning?: string;   // Optional warning for bad practices
  tags: string[];                // Search labels
}
