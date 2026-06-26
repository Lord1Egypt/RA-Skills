## ADDED Requirements

### Requirement: Video Download Module
Implement video download functionality using yt-dlp or similar tool to download Douyin videos.

#### Scenario: Download video from URL
- **WHEN** a user provides a valid Douyin video URL
- **THEN** the system downloads the video to a temporary directory
- **AND** returns the local file path

### Requirement: Keyframe Extraction
Extract keyframes from downloaded videos using ffmpeg for visual analysis.

#### Scenario: Extract frames from video
- **WHEN** a video file is available locally
- **THEN** extract 1 frame per second (or configurable interval)
- **AND** save frames as PNG images to temp directory
- **AND** return array of frame file paths

### Requirement: AI Visual Analysis
Use Zhipu GLM-4.6V series models to analyze keyframes and identify visual patterns, text overlays, and scene types.

**Supported Models** (configurable):
- `glm-4.6v-flash` (Default) - Fastest, cost-effective
- `glm-4.6v-flashx` - Enhanced flash model
- `glm-4.6v` - Full capability model

#### Scenario: Analyze video frames
- **WHEN** keyframes are extracted
- **THEN** send frames to Zhipu API with selected model
- **AND** receive analysis including:
  - Visual style (大字报, 实拍, 混剪)
  - Text overlay patterns
  - Color scheme
  - Scene transition frequency
  - Visual hooks

### Requirement: Enhanced Report Generation
Combine Phase 1 data with Phase 2 visual analysis in comprehensive reports.

#### Scenario: Generate complete analysis report
- **WHEN** all analysis phases complete
- **THEN** generate Markdown report including:
  - Phase 1: Basic metrics (likes, comments, etc.)
  - Phase 2: Visual analysis insights
  - Actionable recommendations
