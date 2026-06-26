---
name: phase2-video-analysis
description: Phase 2 - Add video download, keyframe extraction, and AI visual analysis to Douyin Video Analyzer
status: active
schema: spec-driven
---

# Phase 2: Video Analysis Features

## Overview
Add advanced video analysis capabilities including video download, keyframe extraction, and AI-powered visual analysis using Gemini Vision API.

## Goals
1. Download videos from Douyin URLs
2. Extract keyframes from videos using ffmpeg
3. Analyze visual content with Gemini Vision API
4. Generate comprehensive visual analysis reports

## Dependencies
- Phase 1 (Foundation) - ✅ Completed
- ffmpeg - System dependency
- ZHIPU_API_KEY - For Zhipu GLM-4.6V series visual analysis (default: glm-4.6v-flash)
