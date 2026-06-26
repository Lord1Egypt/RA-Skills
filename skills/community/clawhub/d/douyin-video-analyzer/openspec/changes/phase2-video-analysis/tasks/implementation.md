## 1. Setup and Configuration

- [x] 1.1 Add new dependencies to package.json (axios for API calls)
- [x] 1.2 Update .env.example with ZHIPU_API_KEY and GLM_MODEL option
- [x] 1.3 Create temp/ directory structure with .gitignore
- [x] 1.4 Verify ffmpeg is installed (add check in script)

## 2. Video Download Module

- [x] 2.1 Create lib/video-downloader.js
- [x] 2.2 Implement downloadVideo() function using https
- [x] 2.3 Integrate yt-dlp for video download
- [x] 2.4 Add fallback logic for download methods
- [x] 2.5 Add progress logging and error handling

## 3. Frame Extraction Module

- [x] 3.1 Create lib/frame-extractor.js
- [x] 3.2 Implement extractKeyframes() with ffmpeg
- [x] 3.3 Support configurable interval and max frames
- [x] 3.4 Save frames to temp/frames/{videoId}/
- [x] 3.5 Add cleanup function to remove temp files

## 4. AI Visual Analysis Module

- [x] 4.1 Create lib/ai-analyzer.js
- [x] 4.2 Implement analyzeFrames() function with model selection
- [x] 4.3 Integrate Zhipu API (open.bigmodel.cn) with GLM-4.6V series
- [x] 4.4 Support model switching: glm-4.6v-flash (default), glm-4.6v-flashx, glm-4.6v
- [x] 4.5 Implement batch processing (max 5 frames per request)
- [x] 4.6 Define structured output schema
- [x] 4.7 Add error handling and retries

## 5. Report Generator Enhancement

- [x] 5.1 Extend lib/utils.js with generateFullReport()
- [x] 5.2 Add generateLocalFileReport() for local video analysis
- [x] 5.3 Design new report template including visual analysis
- [x] 5.4 Add emoji and formatting for readability
- [x] 5.5 Include actionable recommendations section

## 6. Main Script Integration

- [x] 6.1 Update scripts/analyze.js
- [x] 6.2 Add local file analysis workflow
- [x] 6.3 Add Phase 2 execution flow with yt-dlp
- [x] 6.4 Add command-line flags (--skip-download, --max-frames)
- [x] 6.5 Update progress indicators and help text

## 7. Testing and Validation

- [x] 7.1 Test with local video files
- [x] 7.2 Verify frame extraction quality
- [x] 7.3 Validate Zhipu API integration
- [x] 7.4 Test yt-dlp integration
- [x] 7.5 Test error handling scenarios

## 8. Documentation

- [x] 8.1 Update SKILL.md with Phase 2 features
- [x] 8.2 Add usage examples for local file analysis
- [x] 8.3 Add documentation for third-party download tools (snapany.com)
- [x] 8.4 Document yt-dlp integration and limitations
- [x] 8.5 Add troubleshooting section
