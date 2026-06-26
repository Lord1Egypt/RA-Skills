# ANFSF V1.5.6 Skill - Enhanced Hybrid Adaptive Parser

AI Native Full-Stack Software Factory V1.5.6 - Enhanced Hybrid Adaptive Parser with 100% health status (187/187 tests)

## Overview

This skill provides enhanced requirement refinement capabilities for ANFSF (AI Native Full-Stack Software Factory) architecture, featuring:

- **Hybrid Adaptive Parser**: Smart detection of complex requirements with weighted scoring system
- **Negation Handling**: Avoids false positives (e.g., "不需要多级审批" is not detected as complex)
- **Multi-format Support**: Supports Mermaid, PlantUML, and image references
- **Template Matching**: Automatically matches historical templates
- **Complete Rollback**: Automatic rollback mechanism with monitoring

## Key Features

### 1. Hybrid Adaptive Parser

Intelligently detects complex requirements using weighted scoring system:
- **Multi-level审批 workflow**: +3 points
- **Cross-department collaboration**: +1 point per department
- **Complex data visualization**: +2 points
- **External system integration**: +2 points
- **Complex permission system**: +2 points

### 2. Negation Processing

Detects negative keywords to reduce false positives:
- "不需要" (not required)
- "无需" (no need)
- "不要" (don't want)
- "no", "without", "not required"

### 3. Multi-format Content Support

- Mermaid flowcharts
- PlantUML diagrams
- Image references (OCR preparation)
- Markdown tables and lists

### 4. Template Matching

Automatically matches historical templates:
- `fixed-asset-investment` (固定资产投资)
- `project-management` (项目管理)
- `hr-system` (人力资源系统)

## Usage

The skill automatically selects the appropriate parsing strategy based on requirement complexity:

```typescript
const skill = new RequirementRefinerSkill(context);
const result = await skill.refine(rawRequirement);
```

## Architecture

- **Layer 8.5 Governance**: Full governance control plane
- **MemPalace Memory**: Enhanced memory architecture with isolated wings
- **Evolution Harness**: Supported for self-calibration

## Installation

```bash
clawhub install @anfsf-v1/openclaw-skill@1.5.6
```

## Requirements

- Node.js >= 20.0.0
- OpenClaw >= 2026.3.24

## License

MIT