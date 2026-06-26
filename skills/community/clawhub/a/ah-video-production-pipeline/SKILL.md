---
name: video-production-pipeline
description: 'Specialist in video production pipeline. Use when: stage 1: pre-production, stage 2: asset generation, stage 3: video assembly.'
---

# Video Production Pipeline

This is a **Multi-Agent Workflow** that orchestrates the entire video production process from concept to final export. It coordinates specialized agents for scripting, visual generation, audio synthesis, editing, and platform optimization.

**Workflow Type**: Multi-Agent Orchestration
**Price Tier**: Premium ($9.99)

---

## Workflow Overview

```typescript
// Complete video production pipeline
interface VideoProductionPipeline {
  input: ProductionInput;
  stages: PipelineStage[];
  agents: AgentOrchestration;
  output: FinalDeliverable;
}

interface ProductionInput {
  type: 'idea' | 'script' | 'novel' | 'url' | 'audio';
  content: string;
  format: VideoFormat;
  style: ProductionStyle;
  targetPlatform: Platform[];
  duration: DurationTarget;
}

type VideoFormat =
  | 'youtube-short' | 'youtube-video'
  | 'tiktok' | 'instagram-reel'
  | 'documentary' | 'explainer'
  | 'advertisement' | 'course-module';
```

---

## Pipeline Stages

### Stage 1: Pre-Production
> 📎 **Code example 1** (typescript) — see [references/examples.md](references/examples.md)

### Stage 2: Asset Generation
> 📎 **Code example 2** (typescript) — see [references/examples.md](references/examples.md)

### Stage 3: Video Assembly
> 📎 **Code example 3** (typescript) — see [references/examples.md](references/examples.md)

### Stage 4: Post-Production
> 📎 **Code example 4** (typescript) — see [references/examples.md](references/examples.md)

---

## Agent Coordination

> 📎 **Code example 5** (typescript) — see [references/examples.md](references/examples.md)

---

## Quality Gates

> 📎 **Code example 6** (typescript) — see [references/examples.md](references/examples.md)

---

## Human-in-the-Loop Integration

> 📎 **Code example 7** (typescript) — see [references/examples.md](references/examples.md)

---

## Configuration Templates

> 📎 **Code example 8** (typescript) — see [references/examples.md](references/examples.md)

---

## Output Deliverables

```typescript
// Final deliverable package
interface FinalDeliverable {
  videos: {
    primary: VideoFile;
    platformVariants: Map<Platform, VideoFile>;
    segments: VideoFile[]; // For repurposing
  };
  assets: {
    thumbnails: ThumbnailSet;
    graphics: GraphicAsset[];
    sourceFiles: SourcePackage;
  };
  metadata: {
    seo: SEOPackage;
    analytics: AnalyticsPrediction;
    schedule: PublishSchedule;
  };
  documentation: {
    script: FinalScript;
    storyboard: FinalStoryboard;
    editDecisionList: EDL;
  };
}

// Analytics predictions
interface AnalyticsPrediction {
  estimatedViews: { min: number; max: number };
  retentionCurve: number[];
  engagementRate: number;
  optimalPostingTimes: Date[];
  audienceMatch: number;
}
```

---

## Usage Examples

### Example 1: Idea to YouTube Short
```typescript
const request = {
  input: {
    type: 'idea',
    content: 'Explain why most people fail at learning programming in under 60 seconds',
    format: 'youtube-short',
    style: { tone: 'energetic', visual: 'dynamic-text' },
    targetPlatform: ['youtube-shorts', 'tiktok']
  },
  preferences: {
    voiceProvider: 'elevenlabs',
    imageStyle: 'modern-minimal',
    captionStyle: 'hormozi'
  }
};

// Pipeline executes:
// 1. Research: Programming learning challenges
// 2. Script: Write 60s script with hook
// 3. Voice: Generate energetic narration
// 4. Visuals: Create dynamic text overlays
// 5. Edit: Assemble with fast cuts
// 6. Captions: Add animated subtitles
// 7. Export: Render for both platforms
```

### Example 2: Blog Post to YouTube Video
```typescript
const request = {
  input: {
    type: 'url',
    content: 'https://example.com/blog/ai-trends-2025',
    format: 'youtube-video',
    targetDuration: 8, // minutes
    style: { tone: 'educational', visual: 'documentary' }
  }
};

// Pipeline executes:
// 1. Extract: Parse blog content
// 2. Research: Supplement with additional data
// 3. Script: Expand to video format
// 4. Storyboard: Plan visual scenes
// 5. Assets: Generate images + stock footage
// 6. Voice: Professional narration
// 7. Edit: Full video assembly
// 8. SEO: Optimize metadata
// 9. Export: YouTube-ready package
```

---

## Best Practices

### Pipeline Optimization
1. Run independent stages in parallel
2. Cache reusable assets
3. Batch similar operations
4. Use progressive quality checks
5. Enable partial recovery on failures

### Quality Assurance
1. Validate at every stage gate
2. Maintain consistency logs
3. Track version history
4. Enable rollback capabilities
5. Human review at critical points

### Resource Management
1. Prioritize based on platform deadlines
2. Balance quality vs. speed
3. Optimize API usage
4. Cache computed results
5. Clean up temporary files

---

## Related Agents

This workflow orchestrates the following agents:
- `video-script-writer` - Script generation
- `shorts-generator` - Short-form content
- `social-media-manager` - Platform optimization
- `prompt-engineer` - Image prompt crafting
- `ai-engineer` - Pipeline automation

---

*This Premium Workflow ($9.99) provides a complete end-to-end video production solution, coordinating multiple specialized agents for professional-quality output.*

## Reference Materials

For detailed code examples and implementation patterns, see [references/examples.md](references/examples.md).
