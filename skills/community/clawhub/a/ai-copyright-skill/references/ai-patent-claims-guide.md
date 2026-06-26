---
AIGC:
  ContentProducer: '001191110102MAD55U9H0F10002'
  ContentPropagator: '001191110102MAD55U9H0F10002'
  Label: '1'
  ProduceID: 'f38efdde-a39a-4170-b359-e649d19fc6d5'
  PropagateID: 'f38efdde-a39a-4170-b359-e649d19fc6d5'
  ReservedCode1: 'aa7b4d2e-12db-44ec-8623-44ca0155b0e5'
  ReservedCode2: 'aa7b4d2e-12db-44ec-8623-44ca0155b0e5'
---

# AI Patent Claims Drafting Guide

## 1. General Principles

Method + System + Storage Medium triple required for every AI patent. Independent claims: preamble (prior art features) + "characterized by" (essential features). Dependent claims in decreasing scope.

## 2. Claim Templates (11 Types)

2.1 Model Architecture (Perception 2D): Acquire input→Model(sub-modules 1,2,3)→Process→Output. System: unit-per-sub-module correspondence.

2.2 3D Vision (Perception 3D): 4-stage: Acquire multi-view→Sparse reconstruction→Dense optimization→Render (with rendering computation sub-steps: per-primitive→volume rendering→per-pixel). Dependent: 3D repr type, rendering formula, adaptive density control, param ranges, training loss.

2.3 Training Method (Engineering): Construct data→Init params→Forward→Loss(with innovation)→Optimize→Converge.

2.4 Multimodal LLM (Language): Encode mod1+mod2→Project to unified space→Cross-modal fusion→Decode.

2.5 RAG (Language): 5-stage: Query parse→Retrieve→Rerank→Context reconstruct→Generate. Dependent: hybrid retrieval, reranking method, KB structure, context construction, incremental update.

2.6 Diffusion (Generative): Condition encode→Inject via cross-attention/adapter/ControlNet at specified layer→Denoise stepwise→Decode. Dependent: injection type, denoising arch, noise schedule, multi-condition fusion, training (freeze original, train injection only).

2.7 Agent (Decision): Intent→Plan→Tool execute→Observe/reflect→Respond.

2.8 Embodied AI/VLA (Decision): Sensor perceive+language→Visual+language encode→Cross-modal fuse→Policy→Actuator drive→Feedback. Dependent: action space (continuous/discrete), sensor binding, policy network, Sim2Real, safety constraints.

2.9 Inference Optimization (Engineering): Original model→Optimize→Determine strategy→Infer.

2.10 Data Processing (Engineering): Acquire→Preprocess→Augment→Downstream.

2.11 AI Watermark (Safety): Embed phase (determine position→generate→inject preserving quality) + Verify phase (extract→match→confirm if robustness met). Dependent: target layer, injection method, robustness after attacks, encoding scheme, multi-layer sharing.

## 3. Dependent Claim Expansion

General 5-layer: (1) Module internal structure (2) Specific computation (3) Parameter range (4) Preferred embodiment (5) Training features.

Domain-specific tables provided in §2 for 3D Vision, RAG, Diffusion, Embodied, Watermark - use instead of general when available.

> AI生成