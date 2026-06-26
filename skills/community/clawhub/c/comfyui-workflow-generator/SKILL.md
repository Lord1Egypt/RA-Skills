---
name: comfyui-workflow-generator
description: ComfyUI工作流生成器。从自然语言描述生成ComfyUI工作流。基于ComfyGPT研究架构，经历生成→验证→构建三阶段管道。触发词：ComfyUI工作流、生成工作流、ComfyUI自动化。
version: 1.0.0
---

# ComfyUI Workflow Generator

基于自然语言描述生成ComfyUI工作流的AI工具。

## 核心功能

- 自然语言 → ComfyUI工作流（JSON）
- 三阶段管道：Generator（生成）→ Validator（验证）→ Builder（构建）
- 支持 SDXL / Flux / Video 等多种节点类型
- 模块化设计，可在每个阶段介入检查

## 触发词

「ComfyUI工作流」「生成工作流」「帮我写ComfyUI流程」

## 使用限制

- 依赖ComfyUI本地环境
- 无法识别训练截止日期后发布的新节点
- 建议在使用前检查工作流的节点兼容性

## 版本

- **Skill 版本**: 1.0.0
